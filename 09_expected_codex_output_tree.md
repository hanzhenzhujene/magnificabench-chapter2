# Expected Codex Output Tree

Codex should create this folder:

```text
magnificabench_chapter2_final/
├── README.md
├── chapter2_executive_brief.md
├── chapter2_principle_matrix.md
├── chapter2_ontology.json
├── chapter2_benchmark.jsonl
├── chapter2_rubric.yaml
├── chapter2_visual_map.mmd
├── chapter2_10min_update.md
├── chapter2_slide_outline.md
├── validation_report.md
└── scripts/
    ├── validate_jsonl.py
    └── render_mermaid_instructions.md
```

## Minimum validation requirements

- `chapter2_benchmark.jsonl` has at least 40 valid JSONL rows.
- Every row has `id`, `category`, `source_paragraphs`, `principles`, `prompt`, `ideal_answer`, `scoring_rubric`, and `difficulty`.
- Every `source_paragraphs` value is within 46–89.
- `chapter2_ontology.json` has all required nodes and edges.
- `chapter2_rubric.yaml` has all required rubric dimensions.
- `chapter2_visual_map.mmd` is valid Mermaid syntax.
- `chapter2_10min_update.md` can be used directly for a 10–15 minute update.

## Recommended Codex implementation order

1. Read `00_CODEX_GOAL.md`.
2. Use `01_chapter2_logic_brief.md` and `02_principle_matrix.md` as conceptual source.
3. Convert `05_ontology.json`, `06_seed_dataset.jsonl`, and `04_rubric.yaml` into polished final versions.
4. Add validation scripts.
5. Generate `validation_report.md` last.
