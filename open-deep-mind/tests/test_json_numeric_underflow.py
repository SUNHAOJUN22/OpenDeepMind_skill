"""Public CLI regressions for numeric input loss, not model benchmark results."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NUMBER = "__raw_json_number__"


def raw_number_json(document, token):
    return json.dumps(document).replace(json.dumps(NUMBER), token)


class LedgerNumericUnderflowTests(unittest.TestCase):
    def validate_confidence(self, token, *, extension=False):
        document = json.loads((ROOT / "assets/example-ledger.json").read_text(encoding="utf-8"))
        if extension:
            document["extension"] = NUMBER
        else:
            document["claims"][0]["confidence"] = NUMBER
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "ledger.json"
            path.write_text(raw_number_json(document, token), encoding="utf-8")
            process = subprocess.run(
                [sys.executable, str(ROOT / "scripts/validate_ledger.py"), str(path)],
                text=True, capture_output=True, check=False, timeout=10,
            )
        self.assertNotIn("Traceback", process.stderr)
        return process.returncode, json.loads(process.stdout)

    def test_negative_confidence_cannot_underflow_into_valid_zero(self):
        for token in ("-1e-999", "-1E-999", "-0.1e-323"):
            with self.subTest(token=token):
                code, result = self.validate_confidence(token)
                self.assertEqual(code, 1)
                self.assertFalse(result["ok"])
                self.assertIn("underflows", result["error"])

    def test_nonzero_extension_numbers_cannot_silently_disappear(self):
        for token in ("1e-999", "1e-324", "-1e-324"):
            with self.subTest(token=token):
                code, result = self.validate_confidence(token, extension=True)
                self.assertEqual(code, 1)
                self.assertIn("underflows", result["error"])

    def test_zero_significands_remain_valid_at_extreme_exponents(self):
        for token in ("0e-999", "-0e-999", "0e999", "-0.0E999"):
            with self.subTest(token=token):
                code, result = self.validate_confidence(token)
                self.assertEqual(code, 0, result)
                self.assertTrue(result["ok"])

    def test_representable_positive_subnormal_confidence_remains_valid(self):
        for token in ("5e-324", "1e-320", "2.2250738585072014e-308"):
            with self.subTest(token=token):
                code, result = self.validate_confidence(token)
                self.assertEqual(code, 0, result)
                self.assertTrue(result["ok"])


class BenchmarkNumericUnderflowTests(unittest.TestCase):
    def aggregate_score(self, token, *, run_extension=False):
        cases = json.loads((ROOT / "evals/evals.json").read_text(encoding="utf-8"))["evals"]
        assertions = next(case for case in cases if case["id"] == "R01")["assertions"]
        slot = {"case_id": "R01", "configuration": "no_skill", "repetition": 1}
        run = {
            **slot, "model": "synthetic-software-fixture", "route": "none",
            "loaded_modules": [], "response_text": "synthetic response excerpt",
            "total_tokens": 4, "duration_ms": 1,
        }
        grade = {
            "case_id": "R01", "configuration": "no_skill", "judge_score": NUMBER,
            "assertion_results": [
                {"text": text, "passed": True, "evidence": "synthetic response excerpt"}
                for text in assertions
            ],
            "red_blockers": [],
            "module_leakage": False,
            "summary": {"passed": len(assertions), "failed": 0, "total": len(assertions),
                        "pass_rate": 1.0, "case_passed": True},
        }
        if run_extension:
            run["extension"] = NUMBER
            grade["judge_score"] = 0.0
        with tempfile.TemporaryDirectory() as folder:
            workspace = Path(folder)
            (workspace / "manifest.json").write_text(json.dumps({
                "benchmark_version": "1.0.0", "expected_run_slots": [slot],
            }), encoding="utf-8")
            run_dir = workspace / "eval-R01/no_skill/run-1"
            run_dir.mkdir(parents=True)
            (run_dir / "run_record.json").write_text(raw_number_json(run, token), encoding="utf-8")
            (run_dir / "grading.json").write_text(raw_number_json(grade, token), encoding="utf-8")
            process = subprocess.run(
                [sys.executable, str(ROOT / "evals/scripts/aggregate_benchmark.py"), str(workspace)],
                text=True, capture_output=True, check=False, timeout=10,
            )
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertNotIn("Traceback", process.stderr)
            result = json.loads((workspace / "benchmark.json").read_text(encoding="utf-8"))
        self.assertFalse(result["publication_ready"])
        return result

    def test_negative_judge_score_cannot_underflow_into_valid_zero(self):
        for token in ("-1e-999", "-1E-999", "-0.1e-323"):
            with self.subTest(token=token):
                result = self.aggregate_score(token)
                self.assertEqual(result["complete_runs"], 0)
                self.assertFalse(result["artifact_set_complete"])
                self.assertTrue(any("underflows" in error for error in result["metadata_errors"]))

    def test_nonzero_run_extension_cannot_silently_disappear(self):
        for token in ("1e-999", "1e-324", "-1e-324"):
            with self.subTest(token=token):
                result = self.aggregate_score(token, run_extension=True)
                self.assertEqual(result["complete_runs"], 0)
                self.assertTrue(any("underflows" in error for error in result["metadata_errors"]))

    def test_zero_judge_score_remains_valid_at_extreme_exponents(self):
        for token in ("0e-999", "-0e-999", "0e999", "-0.0E999"):
            with self.subTest(token=token):
                result = self.aggregate_score(token)
                self.assertEqual(result["complete_runs"], 1)
                self.assertTrue(result["artifact_set_complete"])
                self.assertEqual(result["configurations"]["no_skill"]["judge_score_mean"], 0.0)

    def test_representable_positive_subnormal_score_is_preserved(self):
        for token in ("5e-324", "1e-320", "2.2250738585072014e-308"):
            with self.subTest(token=token):
                result = self.aggregate_score(token)
                self.assertEqual(result["complete_runs"], 1)
                self.assertTrue(result["artifact_set_complete"])
                self.assertEqual(result["configurations"]["no_skill"]["judge_score_mean"], float(token))


if __name__ == "__main__":
    unittest.main()
