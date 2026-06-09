# Extending The Benchmark With New Dimensions

Use this guide with `03_magnificabench_chapter2_spec.md`.

## The Standard

A new dimension is ready only when it can be run and scored. It must include:

1. Source paragraphs in Chapter 2, paragraphs 46-89.
2. A one-sentence source claim.
3. An AI/digital translation.
4. Observable positive answer behavior.
5. Observable failure modes.
6. Ontology anchors or a new ontology node.
7. Rubric levels 0, 1, 2, and 3.
8. JSONL benchmark items.
9. Validator coverage.
10. A smoke run showing the new items can be scored.

## Minimal Implementation Checklist

1. Update `05_ontology.json` if the new concept needs a reusable node.
2. Update `04_rubric.yaml` if the new concept needs an independently scored dimension.
3. Add items to `06_seed_dataset.jsonl`.
4. Update `scripts/validate_package.py` if item counts or required dimensions change.
5. Run:

```bash
python3 scripts/validate_package.py
python3 -m magnificabench_chapter2 validate
python3 -m magnificabench_chapter2 run --answer-provider demo --judge heuristic --limit 5 --out-dir runs/smoke
python3 -m unittest discover -s tests
```

## What To Avoid

- A dimension that is only a topic label.
- A dimension with no paragraph anchor.
- A dimension that duplicates an existing principle under a new name.
- Items that reward generic ethics language.
- Items that can be answered well without concrete AI/digital governance mechanisms.
- Scoring criteria that cannot be observed in the answer.
