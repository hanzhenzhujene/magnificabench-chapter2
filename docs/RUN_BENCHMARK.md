# Run The Benchmark

This repo is now runnable as a small benchmark package. A researcher can clone it, validate the artifacts, generate answers, score predictions, and inspect aggregate summaries.

## 1. Setup

```bash
git clone https://github.com/hanzhenzhujene/magnificabench-chapter2.git
cd magnificabench-chapter2
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install .
```

No package dependencies are required beyond Python 3.10+.

## 2. Validate The Package

```bash
python3 scripts/validate_package.py
python3 -m magnificabench_chapter2 validate
```

Expected result:

```text
OK: package validates
OK: runnable benchmark artifacts validate
```

## 3. Run A Local Smoke Benchmark

This requires no API keys. It uses the built-in deterministic demo answer backend and local heuristic scorer.

```bash
python3 -m magnificabench_chapter2 run \
  --answer-provider demo \
  --judge heuristic \
  --limit 5 \
  --out-dir runs/smoke
```

Expected outputs:

```text
runs/smoke/predictions.jsonl
runs/smoke/scores.jsonl
runs/smoke/summary.json
```

The heuristic scorer is not a research-grade judge. It exists so the package can be run immediately after download.

The input for `run` is the bundled dataset file `06_seed_dataset.jsonl`. Each row contains an item ID, prompt, source paragraph references, principles, ideal answer, scoring rubric, and difficulty. The command first generates `predictions.jsonl`, then scores that file into `scores.jsonl` and `summary.json`.

## 4. Export Prompts For An External Model

If you want to run the prompts in another system, export them:

```bash
python3 -m magnificabench_chapter2 export-prompts \
  --out runs/prompts.jsonl
```

Your model should return prediction rows shaped like:

```json
{"id": "MH2-011", "model": "my-model", "answer_provider": "my-backend", "answer": "Model answer here."}
```

## 5. Score Existing Predictions

```bash
python3 -m magnificabench_chapter2 score \
  --predictions examples/predictions/demo_mixed.jsonl \
  --out runs/example_scores.jsonl \
  --summary runs/example_summary.json
```

## 6. Generate Answers With A Live Model

OpenAI-compatible example:

```bash
export OPENAI_API_KEY="..."
python3 -m magnificabench_chapter2 answer \
  --provider openai \
  --model YOUR_OPENAI_MODEL \
  --limit 10 \
  --out runs/openai_predictions.jsonl
```

Ollama local example:

```bash
ollama serve
ollama pull llama3.1
python3 -m magnificabench_chapter2 answer \
  --provider ollama \
  --model llama3.1 \
  --limit 10 \
  --out runs/ollama_predictions.jsonl
```

## 7. Score With An LLM Judge

```bash
python3 -m magnificabench_chapter2 score \
  --predictions runs/openai_predictions.jsonl \
  --judge llm \
  --judge-provider openai \
  --judge-model YOUR_JUDGE_MODEL \
  --out runs/openai_judged_scores.jsonl \
  --summary runs/openai_judged_summary.json
```

Use `--dimensions all` if every item should receive all 12 rubric dimension scores. The default `--dimensions auto` scores global dimensions plus dimensions inferred from the item's principles.

## 8. Compare Multiple Answer Models

Run each answer model into a separate predictions file:

```bash
python3 -m magnificabench_chapter2 answer --provider openai --model YOUR_OPENAI_MODEL --out runs/openai_predictions.jsonl
python3 -m magnificabench_chapter2 answer --provider ollama --model llama3.1 --out runs/llama31_predictions.jsonl
```

Score both with the same judge:

```bash
python3 -m magnificabench_chapter2 score --predictions runs/openai_predictions.jsonl --judge llm --judge-provider openai --judge-model YOUR_JUDGE_MODEL --out runs/openai_scores.jsonl --summary runs/openai_summary.json
python3 -m magnificabench_chapter2 score --predictions runs/llama31_predictions.jsonl --judge llm --judge-provider openai --judge-model YOUR_JUDGE_MODEL --out runs/llama31_scores.jsonl --summary runs/llama31_summary.json
```

Then compare `overall_mean`, `by_category`, `by_difficulty`, and `by_dimension` in the summary JSON files.
