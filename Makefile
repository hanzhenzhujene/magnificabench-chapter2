.PHONY: validate smoke test clean-runs

validate:
	python3 scripts/validate_package.py
	python3 -m magnificabench_chapter2 validate

smoke:
	python3 -m magnificabench_chapter2 run --answer-provider demo --judge heuristic --limit 5 --out-dir runs/smoke

test:
	python3 -m unittest discover -s tests

clean-runs:
	rm -rf runs
