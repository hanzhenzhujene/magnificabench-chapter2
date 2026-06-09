# Scoring With LLM Judges

MagnificaBench Chapter 2 supports two scoring modes:

1. `heuristic`: local smoke scoring based on item-level must-include term coverage.
2. `llm`: an LLM-as-judge workflow that returns JSON scores.

Use the heuristic scorer only to prove the package runs. Use an LLM judge or human review for research claims.

## Supported Providers

The CLI uses the Python standard library and calls provider HTTP APIs directly.

| Provider | Use | Required environment |
|---|---|---|
| `openai` | OpenAI chat-completions compatible scoring | `OPENAI_API_KEY`, optional `OPENAI_BASE_URL` |
| `anthropic` | Anthropic Messages API scoring | `ANTHROPIC_API_KEY`, optional `ANTHROPIC_BASE_URL` |
| `ollama` | Local Ollama model scoring | optional `OLLAMA_BASE_URL` |
| `openai-compatible` | vLLM, LM Studio, local gateways, compatible APIs | `OPENAI_COMPATIBLE_BASE_URL`, optional key |

## Judge Command

```bash
python3 -m magnificabench_chapter2 score \
  --predictions runs/model_predictions.jsonl \
  --judge llm \
  --judge-provider openai \
  --judge-model YOUR_JUDGE_MODEL \
  --out runs/model_scores.jsonl \
  --summary runs/model_summary.json
```

## What The Judge Receives

For each item, the judge receives:

- item ID, category, difficulty, source paragraphs, and principles;
- benchmark prompt;
- ideal answer as a reference target;
- item-level `must_include`, `penalize_if`, and `excellent_answer`;
- selected global and principle-specific rubric dimensions;
- model answer.

The judge must return valid JSON with:

- `overall_score`: integer 0-3;
- `dimension_scores`: integer 0-3 for each requested dimension;
- `rationale`: short explanation;
- `missing`: important missing elements;
- `penalties`: penalized issues.

## Calibration Protocol

Before reporting results:

1. Score a 5-10 item calibration subset with the intended judge.
2. Manually inspect low, medium, and high scored examples.
3. Check that the judge penalizes generic AI ethics language.
4. Check that the judge rewards concrete remedies: appeal, audit, participation, transparency, recourse, monitoring, and repair.
5. Keep the same judge model and temperature for every compared answer model.

## Reporting Checklist

Any result table should state:

- answer model and provider;
- judge model and provider;
- item count;
- whether scoring used `auto` or `all` dimensions;
- temperature and max token settings;
- whether scores were heuristically generated, LLM-judged, human-reviewed, or calibrated.
