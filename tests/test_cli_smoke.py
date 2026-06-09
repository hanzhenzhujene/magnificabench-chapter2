from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CliSmokeTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "magnificabench_chapter2", *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )

    def test_validate(self) -> None:
        result = self.run_cli("validate")
        self.assertIn("OK: runnable benchmark artifacts validate", result.stdout)

    def test_demo_run_writes_scores_and_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "smoke"
            self.run_cli("run", "--answer-provider", "demo", "--judge", "heuristic", "--limit", "3", "--out-dir", str(out_dir))
            predictions = out_dir / "predictions.jsonl"
            scores = out_dir / "scores.jsonl"
            summary = out_dir / "summary.json"
            self.assertTrue(predictions.exists())
            self.assertTrue(scores.exists())
            self.assertTrue(summary.exists())
            score_rows = [json.loads(line) for line in scores.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(score_rows), 3)
            data = json.loads(summary.read_text(encoding="utf-8"))
            self.assertEqual(data["count"], 3)

    def test_score_example_predictions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scores = Path(tmp) / "scores.jsonl"
            summary = Path(tmp) / "summary.json"
            self.run_cli(
                "score",
                "--predictions",
                "examples/predictions/demo_mixed.jsonl",
                "--out",
                str(scores),
                "--summary",
                str(summary),
            )
            self.assertTrue(scores.exists())
            self.assertTrue(summary.exists())

    def test_packaged_resources_match_source_artifacts(self) -> None:
        for filename in ("04_rubric.yaml", "05_ontology.json", "06_seed_dataset.jsonl"):
            source = ROOT / filename
            packaged = ROOT / "magnificabench_chapter2" / "resources" / filename
            self.assertTrue(packaged.exists(), filename)
            self.assertEqual(
                source.read_text(encoding="utf-8"),
                packaged.read_text(encoding="utf-8"),
                filename,
            )


if __name__ == "__main__":
    unittest.main()
