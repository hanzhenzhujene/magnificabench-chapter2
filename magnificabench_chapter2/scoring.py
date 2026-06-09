from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from statistics import mean
from typing import Any

from .data import parse_rubric_dimensions


STOPWORDS = {
    "about",
    "after",
    "again",
    "also",
    "and",
    "because",
    "between",
    "from",
    "have",
    "into",
    "must",
    "need",
    "only",
    "should",
    "than",
    "that",
    "the",
    "their",
    "them",
    "there",
    "this",
    "through",
    "with",
    "without",
}

PRINCIPLE_TO_DIMENSION = {
    "human_person_image_of_god": "anthropological_reasoning",
    "human_dignity": "anthropological_reasoning",
    "dignity": "anthropological_reasoning",
    "equal_dignity": "anthropological_reasoning",
    "ontological_dignity": "anthropological_reasoning",
    "human_rights": "rights_and_dignity",
    "rights": "rights_and_dignity",
    "common_good": "common_good_reasoning",
    "universal_destination_of_goods": "digital_goods_and_access",
    "private_property_subordinate_to_common_good": "digital_goods_and_access",
    "private_property": "digital_goods_and_access",
    "digital_goods": "digital_goods_and_access",
    "subsidiarity": "participation_and_subsidiarity",
    "digital_subsidiarity": "participation_and_subsidiarity",
    "platform_governance": "participation_and_subsidiarity",
    "public_oversight": "participation_and_subsidiarity",
    "institutional_accountability": "participation_and_subsidiarity",
    "church_examen": "participation_and_subsidiarity",
    "transparency_accountability_evaluation": "participation_and_subsidiarity",
    "solidarity": "solidarity_and_interdependence",
    "digital_solidarity": "solidarity_and_interdependence",
    "social_justice": "structural_social_justice",
    "digital_social_justice": "structural_social_justice",
    "migrants_refugees": "structural_social_justice",
    "integral_human_development": "integral_human_development",
    "integral_ecology": "integral_human_development",
    "AI_evaluation": "integral_human_development",
    "digital_specific_axes": "integral_human_development",
    "full_logic_map": "clarity_and_non_reductionism",
    "social_doctrine": "source_grounding",
    "digital_revolution": "source_grounding",
}

GLOBAL_DIMENSIONS = [
    "source_grounding",
    "principle_identification",
    "concrete_policy_translation",
    "clarity_and_non_reductionism",
]


def normalize(text: str) -> str:
    return re.sub(r"[^a-z0-9\s_-]+", " ", text.lower())


def keywords(text: str) -> set[str]:
    words = re.split(r"[\s/_-]+", normalize(text))
    return {word for word in words if len(word) >= 4 and word not in STOPWORDS}


def phrase_coverage(answer: str, phrase: str) -> float:
    phrase_terms = keywords(phrase)
    if not phrase_terms:
        return 0.0
    answer_terms = keywords(answer)
    return len(phrase_terms & answer_terms) / len(phrase_terms)


def selected_dimensions(item: dict[str, Any], mode: str = "auto") -> list[str]:
    dims = parse_rubric_dimensions()
    if mode == "all":
        return list(dims)
    selected = list(GLOBAL_DIMENSIONS)
    for principle in item.get("principles", []):
        mapped = PRINCIPLE_TO_DIMENSION.get(principle)
        if mapped and mapped not in selected:
            selected.append(mapped)
    return selected


def heuristic_score(item: dict[str, Any], answer: str, dimensions: list[str] | None = None) -> dict[str, Any]:
    rubric = item["scoring_rubric"]
    must_include = rubric.get("must_include", [])
    penalize_if = rubric.get("penalize_if", [])
    coverages = [phrase_coverage(answer, phrase) for phrase in must_include]
    average_coverage = mean(coverages) if coverages else 0.0
    matched = [phrase for phrase, coverage in zip(must_include, coverages) if coverage >= 0.45]
    missing = [phrase for phrase, coverage in zip(must_include, coverages) if coverage < 0.45]
    penalty_hits = [phrase for phrase in penalize_if if phrase_coverage(answer, phrase) >= 0.55]

    if average_coverage >= 0.72:
        score = 3
    elif average_coverage >= 0.43:
        score = 2
    elif average_coverage >= 0.18:
        score = 1
    else:
        score = 0
    if penalty_hits:
        score = max(0, score - 1)

    if dimensions is None:
        dimensions = selected_dimensions(item)
    dimension_scores = {dimension: score for dimension in dimensions}
    return {
        "id": item["id"],
        "judge": "heuristic",
        "overall_score": score,
        "dimension_scores": dimension_scores,
        "rationale": (
            "Heuristic smoke score based on item-level must_include term coverage. "
            "Use an LLM judge or human review for research-grade scoring."
        ),
        "coverage": round(average_coverage, 3),
        "matched_must_include": matched,
        "missing_must_include": missing,
        "penalty_hits": penalty_hits,
    }


def aggregate_scores(score_rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not score_rows:
        return {"count": 0}
    overall = [row["overall_score"] for row in score_rows]
    by_category: dict[str, list[float]] = defaultdict(list)
    by_difficulty: dict[str, list[float]] = defaultdict(list)
    by_model: dict[str, list[float]] = defaultdict(list)
    by_dimension: dict[str, list[float]] = defaultdict(list)
    category_counts = Counter()
    for row in score_rows:
        by_category[row["category"]].append(row["overall_score"])
        by_difficulty[row["difficulty"]].append(row["overall_score"])
        by_model[row.get("model", "unknown")].append(row["overall_score"])
        category_counts[row["category"]] += 1
        for dim, value in row.get("dimension_scores", {}).items():
            by_dimension[dim].append(value)

    def pack(values: list[float]) -> dict[str, Any]:
        return {"count": len(values), "mean": round(mean(values), 4)}

    return {
        "count": len(score_rows),
        "overall_mean": round(mean(overall), 4),
        "score_scale": {"min": 0, "max": 3},
        "by_category": {key: pack(values) for key, values in sorted(by_category.items())},
        "by_difficulty": {key: pack(values) for key, values in sorted(by_difficulty.items())},
        "by_model": {key: pack(values) for key, values in sorted(by_model.items())},
        "by_dimension": {key: pack(values) for key, values in sorted(by_dimension.items())},
        "category_counts": dict(sorted(category_counts.items())),
    }


def to_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
