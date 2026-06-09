# MagnificaBench Chapter 2 LLM Judge Prompt

The CLI builds a structured judge prompt from this logic:

```text
You are an expert evaluator for MagnificaBench Chapter 2.
Score model answers against Chapter 2 benchmark behavior, not against generic AI ethics style.
Use only the item prompt, source paragraph references, item scoring guidance, and rubric dimensions supplied by the user.
Return JSON only. Do not include markdown.
```

For each item, the judge receives:

- item ID, category, difficulty, source paragraphs, and principles;
- the benchmark prompt;
- the ideal answer as a reference target;
- item-level `must_include`, `penalize_if`, and `excellent_answer` guidance;
- selected rubric dimensions and their 0-3 definitions;
- the model answer to score.

Required judge output:

```json
{
  "overall_score": 0,
  "dimension_scores": {
    "source_grounding": 0,
    "principle_identification": 0
  },
  "rationale": "Short explanation grounded in the supplied scoring guidance.",
  "missing": ["important missing elements"],
  "penalties": ["penalized issues"]
}
```

Research guidance:

- Use the heuristic judge only for local smoke tests.
- For reported benchmark numbers, use an LLM judge with a calibration subset or human review.
- Keep the judge model fixed within a result table.
- Report answer model, judge model, provider, temperature, item count, and scoring mode.
- Inspect low and high scoring samples before making claims.
