.PHONY: validate smoke test install-smoke clean-runs

validate:
	python3 scripts/validate_package.py
	python3 -m magnificabench_chapter2 validate

smoke:
	python3 -m magnificabench_chapter2 run --answer-provider demo --judge heuristic --limit 5 --out-dir runs/smoke

test:
	python3 -m unittest discover -s tests

install-smoke:
	tmpdir=$$(mktemp -d); \
	python3 -m venv "$$tmpdir/venv"; \
	"$$tmpdir/venv/bin/python" -m pip install .; \
	cd "$$tmpdir"; \
	"$$tmpdir/venv/bin/python" -m magnificabench_chapter2 validate; \
	"$$tmpdir/venv/bin/python" -m magnificabench_chapter2 run --answer-provider demo --judge heuristic --limit 2 --out-dir smoke; \
	rm -rf "$$tmpdir"

clean-runs:
	rm -rf runs
