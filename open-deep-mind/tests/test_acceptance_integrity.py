"""Adversarial software fixtures, never behavioral model performance results."""
from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def module(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    result = importlib.util.module_from_spec(spec)
    sys.modules[name] = result
    spec.loader.exec_module(result)
    return result


AGG = module("acceptance_aggregator", "open-deep-mind/evals/scripts/aggregate_benchmark.py")
V16 = module("acceptance_v16", "open-deep-mind/scripts/scientific_contracts_v16.py")
V17 = module("acceptance_v17", "open-deep-mind/scripts/contracts_v17.py")


def grade():
    assertions = AGG.CASE_MAP["R01"]["assertions"]
    return {"case_id": "R01", "configuration": "no_skill",
            "assertion_results": [{"text": text, "passed": True,
                                   "evidence": "synthetic response excerpt"} for text in assertions],
            "red_blockers": [], "module_leakage": False,
            "summary": {"passed": len(assertions), "failed": 0, "total": len(assertions),
                                               "pass_rate": 1.0, "case_passed": True}}


class GradingIntegrityTests(unittest.TestCase):
    def test_consistent_fixture_is_valid(self):
        self.assertEqual(AGG.validate_grading_record(grade()), [])

    def test_failed_assertion_cannot_be_overridden_by_summary(self):
        record = grade()
        record["assertion_results"][0]["passed"] = False
        self.assertTrue(AGG.validate_grading_record(record))

    def test_summary_counts_and_rates_are_derived(self):
        for key, value in (("passed", 2), ("failed", 1), ("total", 2), ("pass_rate", 0.5)):
            with self.subTest(field=key):
                record = grade()
                record["summary"][key] = value
                self.assertTrue(AGG.validate_grading_record(record))

    def test_red_blocker_forces_case_failure(self):
        record = grade()
        record["red_blockers"] = ["fabricated_source_data_or_experiment"]
        self.assertTrue(AGG.validate_grading_record(record))

    def test_passing_grade_requires_explicit_blocker_and_leakage_status(self):
        case = AGG.CASE_MAP["R01"]
        run = {"configuration": "no_skill", "route": "none", "loaded_modules": []}
        for field in ("red_blockers", "module_leakage"):
            with self.subTest(field=field):
                record = grade()
                record.pop(field)
                self.assertTrue(AGG.validate_grading_record(record))
                self.assertIsNone(AGG.effective_case_pass(case, run, record))

    def test_empty_assertions_cannot_pass(self):
        record = grade()
        record["assertion_results"] = []
        record["summary"].update(passed=0, total=0, pass_rate=0.0)
        self.assertTrue(AGG.validate_grading_record(record))

    def test_pass_requires_response_evidence(self):
        record = grade()
        record["assertion_results"][0]["evidence"] = "  "
        self.assertTrue(AGG.validate_grading_record(record))

    def test_duplicate_assertions_cannot_reweight_score(self):
        record = grade()
        record["assertion_results"] *= 2
        record["summary"].update(passed=2, total=2)
        self.assertTrue(AGG.validate_grading_record(record))

    def test_structured_route_is_rejected_without_crash(self):
        self.assertTrue(AGG.validate_run_record({"route": []}))

    def test_huge_integer_is_not_a_finite_metric(self):
        self.assertIsNone(AGG.numeric(10 ** 400))

    def test_extreme_counters_are_rejected(self):
        self.assertTrue(AGG.validate_run_record({"total_tokens": 10 ** 400}))

    def test_json_nesting_budget_is_an_error_not_a_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "deep.json"
            path.write_text('{"x":' + '[' * 1100 + '0' + ']' * 1100 + '}', encoding="utf-8")
            value, error = AGG.read_json(path)
            self.assertIsNone(value)
            self.assertIsNotNone(error)

    def test_route_and_triz_metrics_use_recorded_run(self):
        case = {"expected_route": "phi", "triz_allowed": False}
        run = {"configuration": "opendeepmind_full", "route": "triz", "loaded_modules": ["triz"]}
        record = grade()
        record.update(route_correct=True, triz_false_activation=False)
        metrics = AGG.build_metrics([(case, run, record)])
        self.assertEqual(metrics["routing_accuracy"], 0.0)
        self.assertEqual(metrics["triz_false_activation_rate"], 1.0)
        self.assertEqual(metrics["case_pass_rate"], 0.0)

    def test_pairwise_uses_same_effective_case_verdict(self):
        case = {"expected_route": "phi", "triz_allowed": False}
        run = {"configuration": "opendeepmind_full", "route": "triz", "loaded_modules": ["triz"],
               "execution_conditions": {"sampling_settings": {}, "reasoning_settings": {},
                                        "tool_access": {}, "input_files": []}}
        left = (case, run, grade())
        right_grade = grade()
        right_grade["assertion_results"][0]["passed"] = False
        right_grade["summary"].update(passed=2, failed=1, pass_rate=2 / 3, case_passed=False)
        right = (case, {**run, "route": "phi", "loaded_modules": []}, right_grade)
        result = AGG.paired_comparison({("R01", 1): left}, {("R01", 1): right})
        self.assertEqual(result["left_case_pass_wins"], 0)
        self.assertEqual(result["case_pass_ties"], 1)


class AggregateCLIIntegrityTests(unittest.TestCase):
    def aggregate(self, mutate=None, orphan=False, manifest_repetition=1):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            slot = {"case_id": "R01", "configuration": "no_skill", "repetition": 1}
            (root / "manifest.json").write_text(json.dumps({
                "benchmark_version": "1.0.0", "expected_run_slots": [{**slot, "repetition": manifest_repetition}]
            }), encoding="utf-8")
            run_dir = root / "eval-R01/no_skill/run-1"
            run_dir.mkdir(parents=True)
            run = {**slot, "model": "synthetic-software-fixture", "route": "none", "loaded_modules": [],
                   "response_text": "synthetic response excerpt", "total_tokens": 4, "duration_ms": 1}
            record = grade()
            if mutate:
                mutate(run, record)
            (run_dir / "run_record.json").write_text(json.dumps(run), encoding="utf-8")
            (run_dir / "grading.json").write_text(json.dumps(record), encoding="utf-8")
            if orphan:
                extra = root / "eval-R01/no_skill/run-2"
                extra.mkdir()
                (extra / "run_record.json").write_text(json.dumps({**run, "repetition": 2}), encoding="utf-8")
            process = subprocess.run([sys.executable, str(ROOT / "open-deep-mind/evals/scripts/aggregate_benchmark.py"), str(root)],
                                     text=True, capture_output=True, check=False)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertNotIn("Traceback", process.stderr)
            return json.loads((root / "benchmark.json").read_text(encoding="utf-8"))

    def test_real_cli_excludes_contradictory_grade(self):
        result = self.aggregate(lambda run, record: record["assertion_results"][0].update(passed=False))
        self.assertEqual(result["complete_runs"], 0)
        self.assertFalse(result["artifact_set_complete"])
        self.assertTrue(result["metadata_errors"])

    def test_one_sided_orphan_is_detected(self):
        result = self.aggregate(orphan=True)
        self.assertFalse(result["artifact_set_complete"])
        self.assertTrue(any("orphan" in error for error in result["metadata_errors"]))

    def test_structured_route_does_not_crash_cli(self):
        result = self.aggregate(lambda run, record: run.update(route=[]))
        self.assertEqual(result["complete_runs"], 0)
        self.assertTrue(result["metadata_errors"])

    def test_extreme_repetition_rejected_before_path_creation(self):
        result = self.aggregate(manifest_repetition=10 ** 300)
        self.assertEqual(result["complete_runs"], 0)
        self.assertTrue(result["metadata_errors"])

    def test_complete_official_criteria_fixture_is_accepted(self):
        result = self.aggregate()
        self.assertEqual(result["complete_runs"], 1)
        self.assertTrue(result["artifact_set_complete"])
        self.assertFalse(result["publication_ready"])

    def test_deleting_criterion_and_recounting_summary_cannot_pass(self):
        def remove_criterion(run, record):
            record["assertion_results"].pop()
            count = len(record["assertion_results"])
            record["summary"].update(passed=count, total=count)
        result = self.aggregate(remove_criterion)
        self.assertEqual(result["complete_runs"], 0)
        self.assertTrue(any("official assertion" in e for e in result["metadata_errors"]))

    def test_replacing_criterion_with_easier_text_cannot_pass(self):
        result = self.aggregate(lambda run, record: record["assertion_results"][0].update(text="An easier fabricated criterion"))
        self.assertEqual(result["complete_runs"], 0)
        self.assertTrue(any("official assertion" in e for e in result["metadata_errors"]))

    def test_extra_criterion_cannot_reweight_score(self):
        def add_criterion(run, record):
            record["assertion_results"].append({"text": "An easier fabricated criterion", "passed": True, "evidence": "synthetic"})
            count = len(record["assertion_results"])
            record["summary"].update(passed=count, total=count)
        result = self.aggregate(add_criterion)
        self.assertEqual(result["complete_runs"], 0)
        self.assertTrue(any("official assertion" in e for e in result["metadata_errors"]))

    def test_noncanonical_and_duplicate_module_ids_are_rejected(self):
        for modules in (["TRIZ"], ["open-deep-mind/triz"], ["unknown"], ["triz", "triz"]):
            with self.subTest(modules=modules):
                result = self.aggregate(lambda run, record: run.update(loaded_modules=modules))
                self.assertEqual(result["complete_runs"], 0)
                self.assertTrue(any("loaded_modules" in e for e in result["metadata_errors"]))


class CompatibilityIntegrityTests(unittest.TestCase):
    def test_publication_flags_are_booleans(self):
        for value in ("false", "true", 1, None):
            with self.subTest(value=value), self.assertRaises(TypeError):
                V17.publication_decision(["a"], ["a"], holdout_sealed=value, exact_revision_bound=True)

    def test_framework_rejects_truthy_string_flags(self):
        with self.assertRaises(TypeError):
            V17.framework_status(publication_ready="false", actual_model_runs_present="false")

    def test_complete_slots_do_not_authorize_publication(self):
        result = V17.publication_decision(["a"], ["a"], holdout_sealed=True, exact_revision_bound=True)
        self.assertEqual(result.status, "ARTIFACT_SET_COMPLETE")
        self.assertFalse(result.publication_ready)
        self.assertNotEqual(V17.framework_status(publication_ready=True, actual_model_runs_present=True),
                            "BEHAVIORAL_SCORE_PUBLICATION_READY")

    def test_slot_ids_are_nonempty_strings(self):
        for value in (1, True, "  ", []):
            with self.subTest(value=value), self.assertRaises(ValueError):
                V17.publication_decision([value], [value], holdout_sealed=True, exact_revision_bound=True)

    def test_canonical_proposition_taxonomy(self):
        self.assertEqual(V17.validate_proposition_type("C"), "CONSTRAINT")
        self.assertEqual(V17.validate_proposition_type("E"), "EMPIRICAL_CLOSURE")
        with self.assertRaises(ValueError):
            V17.validate_proposition_type("CAUSAL")

    def test_duplicate_expected_slots_are_not_weights(self):
        with self.assertRaises(ValueError):
            V17.weighted_behavior_score({"a": 1.0, "b": 0.0}, ["a", "a", "b"])

    def test_scores_are_finite_normalized_numbers(self):
        for value in (-0.1, 1.1, 10 ** 400, True, float("inf")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                V17.weighted_behavior_score({"a": value}, ["a"])

    def test_v16_orphans_do_not_expand_completeness(self):
        result = V16.publication_gate({"a"}, [{"slot": "a", "status": "COMPLETED"},
                                               {"slot": "orphan", "status": "COMPLETED"}],
                                      [{"slot": "a", "status": "GRADED"}])
        self.assertEqual(result["status"], "BLOCKED")
        self.assertLessEqual(result["completeness"], 1.0)

    def test_v16_malformed_propositions_fail_closed(self):
        record = {"id": "C1", "type": "C", "text": "Pressure remains below its stated limit",
                  "status": "PROPOSED", "evidence_refs": []}
        for field, value in (("id", True), ("type", []), ("status", []), ("evidence_refs", [1])):
            with self.subTest(field=field):
                malformed = copy.deepcopy(record)
                malformed[field] = value
                self.assertNotEqual(V16.validate_proposition(malformed), "PASS")


if __name__ == "__main__":
    unittest.main()
