from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def run_script(rel: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(REPO / rel), *args],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )


def valid_run(slot: dict) -> dict:
    return {
        **slot,
        "model": "synthetic-regression-no-real-model-execution",
        "route": "none",
        "loaded_modules": [],
        "response_text": "synthetic regression response",
        "total_tokens": 4,
        "duration_ms": 1,
    }


def valid_grade(slot: dict, passed: bool) -> dict:
    cases = json.loads((REPO / "open-deep-mind/evals/evals.json").read_text(encoding="utf-8"))["evals"]
    criteria = next(case["assertions"] for case in cases if case["id"] == slot["case_id"])
    return {
        "case_id": slot["case_id"],
        "configuration": slot["configuration"],
        "assertion_results": [{"text": text, "passed": passed, "evidence": "synthetic regression response"} for text in criteria],
        "route_correct": passed,
        "red_blockers": [],
        "triz_false_activation": False,
        "module_leakage": False,
        "rival_model_present": False,
        "falsifier_present": False,
        "summary": {
            "passed": len(criteria) * int(passed),
            "failed": len(criteria) * int(not passed),
            "total": len(criteria),
            "pass_rate": float(passed),
            "case_passed": passed,
        },
    }


class BenchmarkIdentityTests(unittest.TestCase):
    def _aggregate_slots(self, slots: list[dict], records: list[tuple[dict, bool]]) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            iteration = Path(tmp)
            (iteration / "manifest.json").write_text(json.dumps({
                "benchmark_version": "1.0.0", "split": "validation",
                "expected_run_slots": slots,
            }), encoding="utf-8")
            for slot, passed in records:
                run_dir = iteration / f"eval-{slot['case_id']}" / slot["configuration"] / f"run-{slot['repetition']}"
                run_dir.mkdir(parents=True, exist_ok=True)
                (run_dir / "run_record.json").write_text(json.dumps(valid_run(slot)), encoding="utf-8")
                (run_dir / "grading.json").write_text(json.dumps(valid_grade(slot, passed)), encoding="utf-8")
            process = run_script("open-deep-mind/evals/scripts/aggregate_benchmark.py", str(iteration))
            self.assertEqual(process.returncode, 0, msg=process.stderr + process.stdout)
            return json.loads((iteration / "benchmark.json").read_text(encoding="utf-8"))

    def test_duplicate_slots_do_not_reweight_scores_or_pair_counts(self) -> None:
        left1 = {"case_id": "R01", "configuration": "opendeepmind_full", "repetition": 1}
        left2 = {**left1, "repetition": 2}
        right1 = {**left1, "configuration": "no_skill"}
        right2 = {**right1, "repetition": 2}
        records = [(left1, True), (left2, False), (right1, False), (right2, False)]
        for slots in ([left1, left1, left2, right1, right2], [left2, right1, left1, right2, left1]):
            with self.subTest(slots=slots):
                report = self._aggregate_slots(slots, records)
                metrics = report["configurations"]["opendeepmind_full"]
                self.assertEqual(metrics["runs"], 2)
                self.assertEqual(metrics["case_pass_rate"], 0.5)
                self.assertEqual(metrics["assertion_pass_rate"], 0.5)
                self.assertEqual(report["complete_runs"], 4)
                self.assertFalse(report["artifact_set_complete"])
                self.assertTrue(any("duplicate expected run slot" in e for e in report["metadata_errors"]))
                paired = report["comparisons"]["full_vs_no_skill"]
                self.assertEqual(paired["paired_runs"], 2)
                self.assertEqual(paired["mean_assertion_pass_rate_delta_left_minus_right"], 0.5)
                self.assertFalse(report["publication_ready"])

    def test_valid_repetitions_remain_distinct_observations(self) -> None:
        slot = {"case_id": "R01", "configuration": "no_skill", "repetition": 1}
        slots = [slot, {**slot, "repetition": 2}]
        report = self._aggregate_slots(slots, [(slots[0], True), (slots[1], False)])
        self.assertEqual(report["complete_runs"], 2)
        self.assertEqual(report["configurations"]["no_skill"]["case_pass_rate"], 0.5)
        self.assertTrue(report["artifact_set_complete"])
        self.assertFalse(report["publication_ready"])

    def test_slot_configuration_and_repetition_are_validated_before_reading(self) -> None:
        valid = {"case_id": "R01", "configuration": "no_skill", "repetition": 1}
        for invalid in ({**valid, "repetition": True}, {**valid, "repetition": 0},
                        {**valid, "repetition": -1}, {**valid, "configuration": "unregistered"},
                        {**valid, "configuration": []}, {**valid, "case_id": "UNKNOWN_CASE"}):
            with self.subTest(slot=invalid):
                report = self._aggregate_slots([invalid], [])
                self.assertEqual(report["complete_runs"], 0)
                self.assertFalse(report["artifact_set_complete"])
                self.assertTrue(report["metadata_errors"])
                self.assertEqual(report["incomplete_run_directories"], [])

    def test_boolean_run_repetition_cannot_impersonate_integer_repetition(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slot = {"case_id": "R01", "configuration": "no_skill", "repetition": 1}
            (root / "manifest.json").write_text(json.dumps({"benchmark_version": "1.0.0", "expected_run_slots": [slot]}))
            run_dir = root / "eval-R01/no_skill/run-1"
            run_dir.mkdir(parents=True)
            malformed = valid_run(slot)
            malformed["repetition"] = True
            (run_dir / "run_record.json").write_text(json.dumps(malformed))
            (run_dir / "grading.json").write_text(json.dumps(valid_grade(slot, False)))
            process = run_script("open-deep-mind/evals/scripts/aggregate_benchmark.py", str(root))
            self.assertEqual(process.returncode, 0, msg=process.stderr)
            report = json.loads((root / "benchmark.json").read_text())
            self.assertEqual(report["complete_runs"], 0)
            self.assertFalse(report["artifact_set_complete"])
            self.assertTrue(any("repetition must be an integer" in error for error in report["metadata_errors"]))

    def test_schema_invalid_artifacts_cannot_count_as_complete_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slot = {"case_id": "R01", "configuration": "no_skill", "repetition": 1}
            (root / "manifest.json").write_text(json.dumps({"benchmark_version": "1.0.0", "expected_run_slots": [slot]}))
            run_dir = root / "eval-R01/no_skill/run-1"
            run_dir.mkdir(parents=True)
            malformed_run = valid_run(slot)
            malformed_run["route"] = "invented-route"
            malformed_grade = valid_grade(slot, False)
            malformed_grade["summary"].pop("total")
            (run_dir / "run_record.json").write_text(json.dumps(malformed_run))
            (run_dir / "grading.json").write_text(json.dumps(malformed_grade))

            process = run_script("open-deep-mind/evals/scripts/aggregate_benchmark.py", str(root))
            self.assertEqual(process.returncode, 0, msg=process.stderr + process.stdout)
            report = json.loads((root / "benchmark.json").read_text())
            self.assertEqual(report["complete_runs"], 0)
            self.assertFalse(report["artifact_set_complete"])
            self.assertEqual(report["publication_status"], "INCOMPLETE_ARTIFACT_SET")
            self.assertTrue(any("run_record schema violation" in error for error in report["metadata_errors"]))
            self.assertTrue(any("grading schema violation" in error for error in report["metadata_errors"]))

    def test_forced_route_ablation_is_not_scored_as_production_routing(self) -> None:
        slot = {"case_id": "T01", "configuration": "opendeepmind_no_triz_ablation", "repetition": 1}
        report = self._aggregate_slots([slot], [(slot, False)])
        metrics = report["configurations"][slot["configuration"]]
        self.assertIsNone(metrics["routing_accuracy"])
        self.assertEqual(metrics["runs"], 1)
        self.assertEqual(metrics["case_pass_rate"], 0.0)


if __name__ == "__main__":
    unittest.main()
