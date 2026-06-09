# Researcher Readiness Audit

This file states what was missing from the original context package and what the runnable package now provides.

## Previously Missing

The repository originally had strong conceptual artifacts but lacked direct-run benchmark infrastructure:

- no installable Python package;
- no CLI entry point;
- no prompt export command;
- no prediction schema;
- no model answer generation workflow;
- no LLM-as-judge workflow;
- no local smoke scorer;
- no aggregate summary output;
- no example predictions;
- no backend configuration examples;
- no tests for end-to-end execution;
- no runbook explaining how to evaluate different LLMs;
- no installed-package resource fallback for non-editable installs;
- no release metadata for citation, license, or continuous validation.

## Added Runnable Components

- `pyproject.toml`: installable package metadata and CLI entry point.
- `magnificabench_chapter2/`: data loading, validation, scoring, LLM clients, judge prompt construction, and CLI.
- `magnificabench_chapter2/resources/`: packaged copies of the dataset, ontology, and rubric for installed-package runs outside a source checkout.
- `configs/`: scoring plan, model backend examples, and judge prompt notes.
- `examples/predictions/`: sample prediction JSONL and format guide.
- `docs/RUN_BENCHMARK.md`: end-to-end runbook.
- `docs/LLM_JUDGES.md`: judge provider and calibration protocol.
- `docs/OUTPUT_SCHEMAS.md`: dataset, prediction, score, and summary schemas.
- `docs/EXTENDING_DIMENSIONS.md`: implementation checklist for new dimensions.
- `tests/`: smoke tests for validation, run, and score commands.
- `Makefile`: short validation, smoke, and test commands.
- `.github/workflows/ci.yml`: validation across supported Python versions.
- `LICENSE`, `CITATION.cff`, and `CHANGELOG.md`: public repository metadata.

## Current Scope

This is still a Chapter 2 benchmark slice, not a full MagnificaBench release. It is runnable and extensible, but any published result should use calibrated LLM judges or human review rather than the heuristic smoke scorer alone.
