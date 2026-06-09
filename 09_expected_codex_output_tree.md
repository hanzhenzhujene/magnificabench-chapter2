# Expected Runnable Benchmark Output Tree

The repository should remain downloadable and directly runnable:

```text
magnificabench-chapter2/
├── .github/
│   └── workflows/
│       └── ci.yml
├── README.md
├── LICENSE
├── CITATION.cff
├── CHANGELOG.md
├── MANIFEST.in
├── pyproject.toml
├── requirements.txt
├── Makefile
├── .env.example
├── 01_chapter2_logic_brief.md
├── 02_principle_matrix.md
├── 03_magnificabench_chapter2_spec.md
├── 04_rubric.yaml
├── 05_ontology.json
├── 06_seed_dataset.jsonl
├── 07_visual_logic_map.mmd
├── 07_visual_logic_map.svg
├── configs/
│   ├── judge_prompt.md
│   ├── model_backends.example.json
│   └── scoring_plan.json
├── docs/
│   ├── EXTENDING_DIMENSIONS.md
│   ├── LLM_JUDGES.md
│   ├── OUTPUT_SCHEMAS.md
│   ├── RESEARCHER_READINESS_AUDIT.md
│   └── RUN_BENCHMARK.md
├── examples/
│   └── predictions/
│       ├── README.md
│       └── demo_mixed.jsonl
├── magnificabench_chapter2/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── data.py
│   ├── judge.py
│   ├── llm_clients.py
│   ├── resources/
│   │   ├── 04_rubric.yaml
│   │   ├── 05_ontology.json
│   │   └── 06_seed_dataset.jsonl
│   └── scoring.py
├── presentation/
│   ├── 8min_oral_script.md
│   ├── README.md
│   ├── magnificabench_chapter2_8min_presentation.pptx
│   └── magnificabench_chapter2_8min_preview.png
├── scripts/
│   └── validate_package.py
└── tests/
    └── test_cli_smoke.py
```

## Minimum Validation Requirements

- `06_seed_dataset.jsonl` has 40 valid JSONL rows.
- Every row has `id`, `category`, `source_paragraphs`, `principles`, `prompt`, `ideal_answer`, `scoring_rubric`, and `difficulty`.
- Every `source_paragraphs` value is within 46-89.
- `05_ontology.json` has all required nodes and at least 22 edges.
- `04_rubric.yaml` has all required rubric dimensions and levels 0-3.
- The CLI can validate artifacts with `python3 -m magnificabench_chapter2 validate`.
- The installed package can validate artifacts outside the source checkout.
- The CLI can run a local smoke benchmark with `python3 -m magnificabench_chapter2 run --answer-provider demo --judge heuristic --limit 5 --out-dir runs/smoke`.
- Example prediction JSONL can be scored.
- LLM judge documentation explains OpenAI, Anthropic, Ollama, and OpenAI-compatible workflows.
- README gives a complete clone-to-run path.

## Researcher Definition Of Done

A new benchmark dimension is not done until:

1. It is anchored in Chapter 2 paragraphs 46-89.
2. It has observable answer behavior, not only a topic label.
3. Ontology, rubric, dataset, and validation artifacts agree.
4. At least one smoke run can generate scores for the new items.
5. The runbook explains how another researcher can reproduce the evaluation.
