from __future__ import annotations

import json
import os
import re
from collections import Counter
from pathlib import Path
from typing import Any


PACKAGE_ROOT = Path(__file__).resolve().parent
RESOURCE_ROOT = PACKAGE_ROOT / "resources"


def repo_root() -> Path:
    override = os.environ.get("MAGNIFICABENCH_CH2_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    source_root = Path(__file__).resolve().parents[1]
    if (source_root / "06_seed_dataset.jsonl").exists():
        return source_root
    return RESOURCE_ROOT


ROOT = repo_root()
DATASET_PATH = ROOT / "06_seed_dataset.jsonl"
RUBRIC_PATH = ROOT / "04_rubric.yaml"
ONTOLOGY_PATH = ROOT / "05_ontology.json"

ALLOWED_CATEGORIES = {
    "direct_comprehension",
    "principle_identification",
    "ai_digital_scenario_application",
    "conflict_resolution_reasoning",
    "critique_diagnose_weak_answer",
    "synthesis_visual_explanation",
}

EXPECTED_CATEGORY_COUNTS = {
    "direct_comprehension": 8,
    "principle_identification": 8,
    "ai_digital_scenario_application": 12,
    "conflict_resolution_reasoning": 6,
    "critique_diagnose_weak_answer": 4,
    "synthesis_visual_explanation": 2,
}

ALLOWED_DIFFICULTIES = {"easy", "medium", "hard"}

REQUIRED_ITEM_FIELDS = {
    "id",
    "category",
    "source_paragraphs",
    "principles",
    "prompt",
    "ideal_answer",
    "scoring_rubric",
    "difficulty",
}


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
        rows.append(item)
    return rows


def load_items(path: Path = DATASET_PATH) -> list[dict[str, Any]]:
    return read_jsonl(path)


def load_items_by_id(path: Path = DATASET_PATH) -> dict[str, dict[str, Any]]:
    items = load_items(path)
    return {item["id"]: item for item in items}


def load_ontology(path: Path = ONTOLOGY_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_rubric_text(path: Path = RUBRIC_PATH) -> str:
    return path.read_text(encoding="utf-8")


def parse_rubric_dimensions(text: str | None = None) -> dict[str, dict[int, str]]:
    if text is None:
        text = load_rubric_text()
    dims: dict[str, dict[int, str]] = {}
    current_dim: str | None = None
    in_dimensions = False
    for line in text.splitlines():
        if line.strip() == "dimensions:":
            in_dimensions = True
            continue
        if not in_dimensions:
            continue
        dim_match = re.fullmatch(r"  ([a-z_]+):\s*", line)
        if dim_match:
            current_dim = dim_match.group(1)
            dims[current_dim] = {}
            continue
        level_match = re.fullmatch(r"    ([0-3]):\s+\"(.+)\"", line)
        if current_dim and level_match:
            dims[current_dim][int(level_match.group(1))] = level_match.group(2)
    return dims


def validate_items(items: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    for index, item in enumerate(items, 1):
        item_id = item.get("id", f"row-{index}")
        missing = REQUIRED_ITEM_FIELDS - set(item)
        if missing:
            errors.append(f"{item_id}: missing fields {sorted(missing)}")
        if item_id in seen_ids:
            errors.append(f"{item_id}: duplicate id")
        seen_ids.add(item_id)
        if item.get("category") not in ALLOWED_CATEGORIES:
            errors.append(f"{item_id}: invalid category {item.get('category')}")
        if item.get("difficulty") not in ALLOWED_DIFFICULTIES:
            errors.append(f"{item_id}: invalid difficulty {item.get('difficulty')}")
        paragraphs = item.get("source_paragraphs", [])
        if not isinstance(paragraphs, list) or not paragraphs:
            errors.append(f"{item_id}: source_paragraphs must be a non-empty list")
        elif not all(isinstance(p, int) and 46 <= p <= 89 for p in paragraphs):
            errors.append(f"{item_id}: source_paragraphs outside Chapter 2 range 46-89")
        rubric = item.get("scoring_rubric", {})
        if not isinstance(rubric, dict):
            errors.append(f"{item_id}: scoring_rubric must be an object")
        else:
            for key in ("must_include", "penalize_if", "excellent_answer"):
                if key not in rubric:
                    errors.append(f"{item_id}: scoring_rubric missing {key}")
    counts = Counter(item.get("category") for item in items)
    if len(items) != 40:
        errors.append(f"expected 40 dataset rows, found {len(items)}")
    if dict(counts) != EXPECTED_CATEGORY_COUNTS:
        errors.append(f"unexpected category counts: {dict(counts)}")
    return errors


def validate_artifacts() -> list[str]:
    errors: list[str] = []
    for path in (DATASET_PATH, RUBRIC_PATH, ONTOLOGY_PATH):
        if not path.exists():
            errors.append(f"missing required artifact: {path.relative_to(ROOT)}")
    if errors:
        return errors
    items = load_items()
    errors.extend(validate_items(items))
    ontology = load_ontology()
    if len(ontology.get("nodes", [])) < 21:
        errors.append("ontology has fewer than 21 nodes")
    if len(ontology.get("edges", [])) < 22:
        errors.append("ontology has fewer than 22 edges")
    dims = parse_rubric_dimensions()
    if len(dims) < 12:
        errors.append(f"rubric has fewer than 12 dimensions: {len(dims)}")
    for dim, levels in dims.items():
        if set(levels) != {0, 1, 2, 3}:
            errors.append(f"rubric dimension {dim} does not define levels 0-3")
    return errors


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def read_predictions(path: Path) -> list[dict[str, Any]]:
    rows = read_jsonl(path)
    for index, row in enumerate(rows, 1):
        if "id" not in row:
            raise ValueError(f"{path}:{index}: prediction missing id")
        if "answer" not in row:
            raise ValueError(f"{path}:{index}: prediction missing answer")
    return rows
