# Output Schemas

## Dataset Item

Source file: `06_seed_dataset.jsonl`

Required fields:

```json
{
  "id": "MH2-011",
  "category": "principle_identification",
  "source_paragraphs": [71, 72],
  "principles": ["digital_subsidiarity"],
  "prompt": "Benchmark prompt.",
  "ideal_answer": "Reference target answer.",
  "scoring_rubric": {
    "must_include": ["required ideas"],
    "penalize_if": ["known failure modes"],
    "excellent_answer": "What distinguishes a level-3 answer."
  },
  "difficulty": "easy"
}
```

## Prompt Export Row

Created by:

```bash
python3 -m magnificabench_chapter2 export-prompts --out runs/prompts.jsonl
```

Fields:

```json
{
  "id": "MH2-011",
  "category": "principle_identification",
  "difficulty": "easy",
  "source_paragraphs": [71, 72],
  "principles": ["digital_subsidiarity"],
  "prompt": "Benchmark prompt.",
  "model_instruction": "System instruction for the answer model."
}
```

## Prediction Row

Input to `score`:

```json
{
  "id": "MH2-011",
  "model": "answer-model-name",
  "answer_provider": "openai-compatible",
  "answer": "The answer model response."
}
```

## Score Row

Created by `score`:

```json
{
  "id": "MH2-011",
  "model": "answer-model-name",
  "answer_provider": "openai-compatible",
  "judge": "llm-or-heuristic-provider",
  "judge_model": "judge-model-name",
  "overall_score": 3,
  "dimension_scores": {
    "source_grounding": 3,
    "principle_identification": 3,
    "participation_and_subsidiarity": 3,
    "concrete_policy_translation": 3,
    "clarity_and_non_reductionism": 3
  },
  "category": "principle_identification",
  "difficulty": "easy",
  "principles": ["digital_subsidiarity"],
  "source_paragraphs": [71, 72],
  "rationale": "Short scoring explanation."
}
```

## Summary JSON

Created by `score` or `run`:

```json
{
  "count": 40,
  "overall_mean": 2.35,
  "score_scale": {"min": 0, "max": 3},
  "by_category": {
    "ai_digital_scenario_application": {"count": 12, "mean": 2.1}
  },
  "by_difficulty": {
    "hard": {"count": 12, "mean": 2.0}
  },
  "by_model": {
    "answer-model-name": {"count": 40, "mean": 2.35}
  },
  "by_dimension": {
    "source_grounding": {"count": 40, "mean": 2.4}
  }
}
```
