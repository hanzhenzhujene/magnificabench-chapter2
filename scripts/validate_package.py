#!/usr/bin/env python3
"""Validate the public MagnificaBench Chapter 2 runnable benchmark package."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_FILES = [
    ".gitignore",
    "00_CODEX_GOAL.md",
    "01_chapter2_logic_brief.md",
    "02_principle_matrix.md",
    "03_magnificabench_chapter2_spec.md",
    "04_rubric.yaml",
    "05_ontology.json",
    "06_seed_dataset.jsonl",
    "07_visual_logic_map.mmd",
    "07_visual_logic_map.svg",
    "08_10min_update_outline.md",
    "09_expected_codex_output_tree.md",
    ".env.example",
    "Makefile",
    "PACKAGE_VALIDATION.json",
    "README.md",
    "chapter2_slide_outline.md",
    "configs/judge_prompt.md",
    "configs/model_backends.example.json",
    "configs/scoring_plan.json",
    "docs/EXTENDING_DIMENSIONS.md",
    "docs/LLM_JUDGES.md",
    "docs/OUTPUT_SCHEMAS.md",
    "docs/RESEARCHER_READINESS_AUDIT.md",
    "docs/RUN_BENCHMARK.md",
    "examples/predictions/README.md",
    "examples/predictions/demo_mixed.jsonl",
    "magnificabench_chapter2/__init__.py",
    "magnificabench_chapter2/__main__.py",
    "magnificabench_chapter2/cli.py",
    "magnificabench_chapter2/data.py",
    "magnificabench_chapter2/judge.py",
    "magnificabench_chapter2/llm_clients.py",
    "magnificabench_chapter2/scoring.py",
    "manifest.json",
    "presentation/README.md",
    "presentation/8min_oral_script.md",
    "presentation/magnificabench_chapter2_8min_presentation.pptx",
    "presentation/magnificabench_chapter2_8min_preview.png",
    "pyproject.toml",
    "requirements.txt",
    "scripts/validate_package.py",
    "tests/test_cli_smoke.py",
]

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

REQUIRED_NODES = {
    "human_person_image_of_god",
    "equal_dignity",
    "ontological_dignity",
    "human_rights",
    "common_good",
    "universal_destination_of_goods",
    "private_property_subordinate_to_common_good",
    "digital_goods",
    "subsidiarity",
    "digital_subsidiarity",
    "solidarity",
    "digital_solidarity",
    "social_justice",
    "digital_social_justice",
    "migrants_refugees",
    "integral_human_development",
    "integral_ecology",
    "church_examen",
    "transparency_accountability_evaluation",
    "AI_evaluation",
    "credibility_of_witness",
}

REQUIRED_RUBRIC_DIMS = {
    "source_grounding",
    "principle_identification",
    "anthropological_reasoning",
    "rights_and_dignity",
    "common_good_reasoning",
    "digital_goods_and_access",
    "participation_and_subsidiarity",
    "solidarity_and_interdependence",
    "structural_social_justice",
    "integral_human_development",
    "concrete_policy_translation",
    "clarity_and_non_reductionism",
}

SECRET_PATTERN = re.compile(
    r"("
    r"-----" r"BEGIN (?:RSA |OPENSSH |PRIVATE )?PRIVATE KEY-----"
    r"|sk-[A-Za-z0-9]{20,}"
    r"|gh[pousr]_[A-Za-z0-9_]{20,}"
    r"|(?i:(?:api[_-]?key|secret|password|credential)\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{12,})"
    r")"
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def validate_files() -> None:
    missing = [path for path in EXPECTED_FILES if not (ROOT / path).exists()]
    if missing:
        fail(f"missing expected files: {missing}")


def validate_dataset() -> None:
    rows = []
    for line_number, line in enumerate((ROOT / "06_seed_dataset.jsonl").read_text().splitlines(), 1):
        item = json.loads(line)
        missing = REQUIRED_ITEM_FIELDS - set(item)
        if missing:
            fail(f"row {line_number} missing fields {sorted(missing)}")
        if item["category"] not in ALLOWED_CATEGORIES:
            fail(f"{item['id']} has invalid category {item['category']}")
        if item["difficulty"] not in ALLOWED_DIFFICULTIES:
            fail(f"{item['id']} has invalid difficulty {item['difficulty']}")
        if not all(isinstance(p, int) and 46 <= p <= 89 for p in item["source_paragraphs"]):
            fail(f"{item['id']} has invalid paragraph references {item['source_paragraphs']}")
        rubric = item["scoring_rubric"]
        for key in ("must_include", "penalize_if", "excellent_answer"):
            if key not in rubric:
                fail(f"{item['id']} scoring_rubric missing {key}")
        rows.append(item)

    if len(rows) != 40:
        fail(f"expected 40 dataset rows, found {len(rows)}")

    counts = Counter(item["category"] for item in rows)
    if dict(counts) != EXPECTED_CATEGORY_COUNTS:
        fail(f"unexpected category counts: {dict(counts)}")


def validate_ontology() -> None:
    ontology = json.loads((ROOT / "05_ontology.json").read_text())
    node_ids = {node["id"] for node in ontology["nodes"]}
    missing = REQUIRED_NODES - node_ids
    if missing:
        fail(f"ontology missing required nodes: {sorted(missing)}")
    if len(ontology.get("edges", [])) < 21:
        fail("ontology has fewer than 21 edges")


def validate_rubric() -> None:
    text = (ROOT / "04_rubric.yaml").read_text()
    dims: dict[str, set[int]] = {}
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
            dims[current_dim] = set()
            continue
        level_match = re.fullmatch(r"    ([0-3]):\s+.+", line)
        if current_dim and level_match:
            dims[current_dim].add(int(level_match.group(1)))

    missing = REQUIRED_RUBRIC_DIMS - set(dims)
    if missing:
        fail(f"rubric missing dimensions: {sorted(missing)}")
    for dim, levels in dims.items():
        if levels != {0, 1, 2, 3}:
            fail(f"rubric dimension {dim} does not define levels 0-3")


def validate_readme_visuals() -> None:
    readme = (ROOT / "README.md").read_text()
    if "07_visual_logic_map.svg" not in readme:
        fail("README does not embed the rendered visual map")
    if "```mermaid" not in readme:
        fail("README does not include a GitHub-rendered Mermaid diagram")
    if "presentation/magnificabench_chapter2_8min_preview.png" not in readme:
        fail("README does not include the eight-minute presentation preview")


def validate_presentation() -> None:
    deck = ROOT / "presentation/magnificabench_chapter2_8min_presentation.pptx"
    script = ROOT / "presentation/8min_oral_script.md"
    preview = ROOT / "presentation/magnificabench_chapter2_8min_preview.png"
    if deck.stat().st_size <= 20_000:
        fail("presentation deck is missing or unexpectedly small")
    if preview.stat().st_size <= 20_000:
        fail("presentation preview is missing or unexpectedly small")
    with zipfile.ZipFile(deck) as pptx:
        slides = [
            name
            for name in pptx.namelist()
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
        ]
    if len(slides) != 8:
        fail(f"presentation deck should contain 8 slides, found {len(slides)}")
    script_text = script.read_text()
    for marker in (
        "0:00-0:55",
        "0:55-1:50",
        "1:50-3:10",
        "3:10-4:15",
        "4:15-5:15",
        "5:15-6:25",
        "6:25-7:20",
        "7:20-8:00",
    ):
        if marker not in script_text:
            fail(f"oral script missing timing marker {marker}")


def validate_example_predictions() -> None:
    item_ids = {json.loads(line)["id"] for line in (ROOT / "06_seed_dataset.jsonl").read_text().splitlines()}
    for line_number, line in enumerate((ROOT / "examples/predictions/demo_mixed.jsonl").read_text().splitlines(), 1):
        row = json.loads(line)
        if row.get("id") not in item_ids:
            fail(f"example prediction row {line_number} references unknown id {row.get('id')}")
        if not row.get("answer"):
            fail(f"example prediction row {line_number} has empty answer")


def run_command(args: list[str]) -> str:
    result = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        fail(f"command failed: {' '.join(args)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
    return result.stdout


def validate_runnable_cli() -> None:
    validate_output = run_command([sys.executable, "-m", "magnificabench_chapter2", "validate"])
    if "OK: runnable benchmark artifacts validate" not in validate_output:
        fail("CLI validate did not report runnable benchmark success")
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp) / "smoke"
        run_command(
            [
                sys.executable,
                "-m",
                "magnificabench_chapter2",
                "run",
                "--answer-provider",
                "demo",
                "--judge",
                "heuristic",
                "--limit",
                "3",
                "--out-dir",
                str(out_dir),
            ]
        )
        for path in ("predictions.jsonl", "scores.jsonl", "summary.json"):
            if not (out_dir / path).exists():
                fail(f"CLI smoke run did not create {path}")
        summary = json.loads((out_dir / "summary.json").read_text())
        if summary.get("count") != 3:
            fail(f"CLI smoke run summary expected 3 rows, found {summary.get('count')}")


def validate_public_hygiene() -> None:
    text_suffixes = {".md", ".json", ".jsonl", ".yaml", ".py", ".toml", ".txt", ".example"}
    checked = [
        path
        for path in EXPECTED_FILES
        if Path(path).suffix in text_suffixes or Path(path).name in {"Makefile", ".gitignore"}
    ]
    matches = []
    for path in checked:
        for line_number, line in enumerate((ROOT / path).read_text().splitlines(), 1):
            if SECRET_PATTERN.search(line):
                matches.append(f"{path}:{line_number}")
    if matches:
        fail(f"secret-like strings found: {matches}")


def main() -> None:
    validate_files()
    validate_dataset()
    validate_ontology()
    validate_rubric()
    validate_readme_visuals()
    validate_presentation()
    validate_example_predictions()
    validate_runnable_cli()
    validate_public_hygiene()
    print("OK: package validates")
    print("OK: 40 JSONL items, 21 ontology nodes, 12 rubric dimensions, 8-slide presentation")
    print("OK: runnable CLI smoke run, example predictions, and researcher docs validate")


if __name__ == "__main__":
    main()
