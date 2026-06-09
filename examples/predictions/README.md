# Prediction JSONL Format

Model outputs are stored as JSONL. Each row must include:

```json
{
  "id": "MH2-011",
  "model": "my-model-name",
  "answer_provider": "openai-compatible",
  "answer": "The model's answer to the benchmark prompt."
}
```

The `id` must match an item in `06_seed_dataset.jsonl`.

Score this example file with:

```bash
python3 -m magnificabench_chapter2 score \
  --predictions examples/predictions/demo_mixed.jsonl \
  --out runs/example_scores.jsonl \
  --summary runs/example_summary.json
```
