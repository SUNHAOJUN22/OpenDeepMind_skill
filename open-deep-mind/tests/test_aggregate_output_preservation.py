"""Synthetic CLI regressions for preserving benchmark source evidence."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

# The cross-repository acceptance runner uses pytest's importlib mode, which
# does not put sibling test modules on sys.path. Keep this helper import valid
# for both that runner and unittest's direct discovery mode.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_benchmark_identity import run_script, valid_grade, valid_run


class AggregateOutputPreservationTests(unittest.TestCase):
    def workspace(self, root: Path) -> Path:
        slot = {"case_id": "R01", "configuration": "no_skill", "repetition": 1}
        root.mkdir()
        (root / "manifest.json").write_text(json.dumps({
            "benchmark_version": "1.0.0", "expected_run_slots": [slot],
        }), encoding="utf-8")
        run_dir = root / "eval-R01" / "no_skill" / "run-1"
        run_dir.mkdir(parents=True)
        (run_dir / "run_record.json").write_text(json.dumps(valid_run(slot)), encoding="utf-8")
        (run_dir / "grading.json").write_text(json.dumps(valid_grade(slot, True)), encoding="utf-8")
        (root / "eval-R01" / "case.json").write_text('{"original_case": true}', encoding="utf-8")
        (run_dir / "run_instructions.json").write_text('{"original_instructions": true}', encoding="utf-8")
        (run_dir / "outputs").mkdir()
        (run_dir / "outputs" / "response.txt").write_text("Original raw response", encoding="utf-8")
        return run_dir

    def test_output_cannot_replace_manifest_or_case_evidence(self):
        for relative in (
            "manifest.json", "eval-R01/case.json",
            "eval-R01/no_skill/run-1/run_record.json",
            "eval-R01/no_skill/run-1/grading.json",
            "eval-R01/no_skill/run-1/run_instructions.json",
            "eval-R01/no_skill/run-1/outputs/response.txt",
        ):
            with self.subTest(output=relative), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / "workspace"
                self.workspace(root)
                originals = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
                process = run_script("open-deep-mind/evals/scripts/aggregate_benchmark.py",
                                     str(root), "--output", str(root / relative))
                self.assertNotEqual(process.returncode, 0, process.stdout)
                self.assertIn("benchmark source evidence", process.stderr)
                self.assertEqual({p: p.read_bytes() for p in originals}, originals)

    def test_parent_directory_alias_cannot_bypass_evidence_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workspace"
            run_dir = self.workspace(root)
            alias = Path(tmp) / "alias"
            try:
                alias.symlink_to(run_dir, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"directory symlinks unavailable: {exc}")
            original = (run_dir / "grading.json").read_bytes()
            process = run_script("open-deep-mind/evals/scripts/aggregate_benchmark.py", str(root),
                                 "--output", str(alias / "grading.json"))
            self.assertNotEqual(process.returncode, 0, process.stdout)
            self.assertIn("benchmark source evidence", process.stderr)
            self.assertEqual((run_dir / "grading.json").read_bytes(), original)

    def test_default_and_custom_reports_remain_refreshable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workspace"
            self.workspace(root)
            original = (root / "manifest.json").read_bytes()
            for destination in (root / "benchmark.json", root / "custom-report.json",
                                root / "eval-summary.json", Path(tmp) / "report.json"):
                for _ in range(2):
                    process = run_script("open-deep-mind/evals/scripts/aggregate_benchmark.py", str(root),
                                         "--output", str(destination))
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(json.loads(destination.read_text(encoding="utf-8"))["complete_runs"], 1)
            self.assertEqual((root / "manifest.json").read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
