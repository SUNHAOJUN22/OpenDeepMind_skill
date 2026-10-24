"""Synthetic artifact tests; these are not model execution or skill scores."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "pair_model_identity_aggregator", ROOT / "open-deep-mind/evals/scripts/aggregate_benchmark.py"
)
AGG = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AGG)


def row(configuration, model="synthetic-model", version="snapshot-1", passed=True):
    case = AGG.CASE_MAP["R01"]
    run = {
        "case_id": "R01", "configuration": configuration, "repetition": 1,
        "model": model, "model_version": version, "route": "phi", "loaded_modules": [],
        "response_text": "synthetic fixture, no model called", "total_tokens": 20, "duration_ms": 3,
        "execution_conditions": execution_conditions(),
    }
    assertions = case["assertions"]
    grade = {
        "case_id": "R01", "configuration": configuration,
        "red_blockers": [], "module_leakage": False,
        "assertion_results": [{"text": text, "passed": passed, "evidence": "synthetic fixture"} for text in assertions],
        "summary": {"passed": len(assertions) if passed else 0,
                    "failed": 0 if passed else len(assertions), "total": len(assertions),
                    "pass_rate": float(passed), "case_passed": passed},
    }
    return case, run, grade


def execution_conditions():
    return {
        "sampling_settings": {"temperature": 0.2, "top_p": 1.0},
        "reasoning_settings": {"effort": "medium"},
        "tool_access": {"python": {"definition_sha256": "b" * 64}, "web": {"definition_sha256": "c" * 64}},
        "input_files": [],
    }


class PairedModelIdentityTests(unittest.TestCase):
    def pair(self, left, right):
        return AGG.paired_comparison({("R01", 1): left}, {("R01", 1): right})

    def test_different_models_do_not_produce_a_skill_effect(self):
        result = self.pair(row("opendeepmind_full", model="model-a"), row("no_skill", model="model-b", passed=False))
        self.assertEqual(result["paired_runs"], 0)
        self.assertIsNone(result["mean_assertion_pass_rate_delta_left_minus_right"])
        self.assertEqual(result["excluded_pairs"][0]["reason_codes"], ["MODEL_MISMATCH"])

    def test_different_or_one_sided_versions_are_excluded(self):
        for version in ("snapshot-2", None):
            with self.subTest(version=version):
                right = row("no_skill", version=version, passed=False)
                if version is None:
                    del right[1]["model_version"]
                result = self.pair(row("opendeepmind_full"), right)
                self.assertEqual(result["paired_runs"], 0)
                self.assertEqual(result["excluded_pairs"][0]["reason_codes"], ["MODEL_VERSION_MISMATCH"])

    def test_matching_identity_retains_the_known_paired_delta(self):
        result = self.pair(row("opendeepmind_full"), row("no_skill", passed=False))
        self.assertEqual(result["paired_runs"], 1)
        self.assertEqual(result["mean_assertion_pass_rate_delta_left_minus_right"], 1.0)
        self.assertEqual(result["left_case_pass_wins"], 1)
        self.assertEqual(result["excluded_pairs"], [])
        self.assertEqual(result["unversioned_paired_runs"], 0)

    def test_different_sampling_reasoning_tools_or_inputs_exclude_the_pair(self):
        mutations = (
            ("sampling_settings", {"temperature": 0.0, "top_p": 1.0}),
            ("reasoning_settings", {"effort": "high"}),
            ("tool_access", {"python": {"definition_sha256": "b" * 64}}),
            ("input_files", [{"path": "data.csv", "sha256": "a" * 64}]),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                left, right = row("opendeepmind_full"), row("no_skill", passed=False)
                left[1]["execution_conditions"][field] = value
                result = self.pair(left, right)
                self.assertEqual(result["candidate_paired_runs"], 1)
                self.assertEqual(result["paired_runs"], 0)
                self.assertIsNone(result["mean_assertion_pass_rate_delta_left_minus_right"])
                self.assertEqual(result["excluded_pairs"][0]["reason_codes"], ["EXECUTION_CONDITIONS_MISMATCH"])

    def test_missing_execution_conditions_are_not_paired(self):
        left, right = row("opendeepmind_full"), row("no_skill", passed=False)
        del right[1]["execution_conditions"]
        result = self.pair(left, right)
        self.assertEqual(result["candidate_paired_runs"], 1)
        self.assertEqual(result["paired_runs"], 0)
        self.assertEqual(result["excluded_pairs"][0]["reason_codes"], ["EXECUTION_CONDITIONS_MISSING"])

    def test_execution_condition_contract_rejects_incomplete_or_invalid_profiles(self):
        run = row("opendeepmind_full")[1]
        del run["execution_conditions"]["tool_access"]
        self.assertTrue(any("tool_access" in error for error in AGG.validate_run_record(run)))

        run = row("opendeepmind_full")[1]
        run["execution_conditions"]["input_files"] = [{"path": "data.csv", "sha256": "bad"}]
        self.assertTrue(any("sha256" in error for error in AGG.validate_run_record(run)))

        run = row("opendeepmind_full")[1]
        run["execution_conditions"]["input_files"] = [{"path": " \t ", "sha256": "a" * 64}]
        self.assertTrue(any("path" in error for error in AGG.validate_run_record(run)))

        run = row("opendeepmind_full")[1]
        run["execution_conditions"]["sampling_settings"]["temperature"] = float("nan")
        self.assertTrue(any("finite JSON" in error for error in AGG.validate_run_record(run)))

        run = row("opendeepmind_full")[1]
        run["execution_conditions"]["sampling_profile_id"] = "profile-1"
        self.assertTrue(any("unsupported fields" in error for error in AGG.validate_run_record(run)))

    def test_legacy_unversioned_records_remain_explicitly_unverified(self):
        left, right = row("opendeepmind_full"), row("no_skill")
        del left[1]["model_version"]
        del right[1]["model_version"]
        result = self.pair(left, right)
        self.assertEqual(result["paired_runs"], 1)
        self.assertEqual(result["unversioned_paired_runs"], 1)

    def test_cli_preserves_individual_metrics_but_excludes_incompatible_pairs(self):
        rows = [row("opendeepmind_full", model="model-a"), row("no_skill", model="model-b", passed=False)]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slots = [{key: run[key] for key in ("case_id", "configuration", "repetition")} for _, run, _ in rows]
            (root / "manifest.json").write_text(json.dumps({"benchmark_version": "1.0.0", "expected_run_slots": slots}), encoding="utf-8")
            for _, run, grade in rows:
                directory = root / "eval-R01" / run["configuration"] / "run-1"
                directory.mkdir(parents=True)
                (directory / "run_record.json").write_text(json.dumps(run), encoding="utf-8")
                (directory / "grading.json").write_text(json.dumps(grade), encoding="utf-8")
            process = subprocess.run([sys.executable, str(ROOT / "open-deep-mind/evals/scripts/aggregate_benchmark.py"), str(root)], text=True, capture_output=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            report = json.loads((root / "benchmark.json").read_text(encoding="utf-8"))
            self.assertEqual(report["complete_runs"], 2)
            self.assertTrue(report["artifact_set_complete"])
            self.assertEqual(report["configurations"]["opendeepmind_full"]["case_pass_rate"], 1.0)
            paired = report["comparisons"]["full_vs_no_skill"]
            self.assertEqual(paired["candidate_paired_runs"], 1)
            self.assertEqual(paired["paired_runs"], 0)
            self.assertIsNone(paired["mean_assertion_pass_rate_delta_left_minus_right"])
            self.assertFalse(report["publication_ready"])

    def test_cli_preserves_individual_metrics_but_excludes_execution_mismatch(self):
        rows = [row("opendeepmind_full"), row("no_skill", passed=False)]
        rows[1][1]["execution_conditions"]["tool_access"] = {}
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slots = [{key: run[key] for key in ("case_id", "configuration", "repetition")} for _, run, _ in rows]
            (root / "manifest.json").write_text(json.dumps({"benchmark_version": "1.0.0", "expected_run_slots": slots}), encoding="utf-8")
            for _, run, grade in rows:
                directory = root / "eval-R01" / run["configuration"] / "run-1"
                directory.mkdir(parents=True)
                (directory / "run_record.json").write_text(json.dumps(run), encoding="utf-8")
                (directory / "grading.json").write_text(json.dumps(grade), encoding="utf-8")
            process = subprocess.run([sys.executable, str(ROOT / "open-deep-mind/evals/scripts/aggregate_benchmark.py"), str(root)], text=True, capture_output=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            report = json.loads((root / "benchmark.json").read_text(encoding="utf-8"))
            self.assertEqual(report["complete_runs"], 2)
            self.assertTrue(report["artifact_set_complete"])
            self.assertEqual(report["configurations"]["opendeepmind_full"]["case_pass_rate"], 1.0)
            paired = report["comparisons"]["full_vs_no_skill"]
            self.assertEqual(paired["candidate_paired_runs"], 1)
            self.assertEqual(paired["paired_runs"], 0)
            self.assertEqual(paired["excluded_pairs"][0]["reason_codes"], ["EXECUTION_CONDITIONS_MISMATCH"])
            self.assertIsNone(paired["mean_assertion_pass_rate_delta_left_minus_right"])


if __name__ == "__main__":
    unittest.main()
