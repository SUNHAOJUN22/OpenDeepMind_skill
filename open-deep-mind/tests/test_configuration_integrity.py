"""Public CLI regressions with synthetic artifacts, never model-quality results."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EVALS = REPO / "open-deep-mind/evals"
ABLATION = "opendeepmind_no_triz_ablation"


class ConfigurationIntegrityTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.invoke("create_workspace.py", "--iteration", "1", "--split", "validation",
                    "--workspace", str(self.root))
        self.workspace = self.root / "iteration-1"
        manifest = json.loads((self.workspace / "manifest.json").read_text(encoding="utf-8"))
        cases = {case["id"]: case for case in json.loads(
            (EVALS / "evals.json").read_text(encoding="utf-8"))["evals"]}
        modules = {"phi": ["first-philosophy"], "p": ["first-principles"],
                   "phi-p": ["first-philosophy", "first-principles"],
                   "triz": ["triz", "first-principles"]}
        self.ablation_records: dict[Path, dict] = {}
        self.production_non_triz: list[Path] = []
        for slot in manifest["expected_run_slots"]:
            cfg = slot["configuration"]
            case = cases[slot["case_id"]]
            directory = (self.workspace / f"eval-{slot['case_id']}" / cfg
                         / f"run-{slot['repetition']}")
            route = {"no_skill": "none", "first_principles_baseline": "p",
                     ABLATION: "p"}.get(cfg, case["expected_route"])
            run = {
                **slot, "model": "synthetic-software-regression-no-model-executed",
                "model_version": "fixture-only", "route": route,
                "loaded_modules": modules[route] if cfg.startswith("opendeepmind_") else [],
                "response_text": "Synthetic software fixture; no model was executed.",
                "total_tokens": 1, "duration_ms": 1,
                "execution_conditions": {"sampling_settings": {}, "reasoning_settings": {},
                                         "tool_access": {}, "input_files": []},
            }
            passed = cfg == ABLATION
            assertions = case["assertions"]
            grade = {
                "case_id": slot["case_id"], "configuration": cfg,
                "assertion_results": [{"text": text, "passed": passed,
                                       "evidence": run["response_text"]} for text in assertions],
                "red_blockers": [], "module_leakage": False,
                "summary": {"passed": len(assertions) if passed else 0,
                            "failed": 0 if passed else len(assertions),
                            "total": len(assertions), "pass_rate": float(passed),
                            "case_passed": passed},
            }
            path = directory / "run_record.json"
            path.write_text(json.dumps(run), encoding="utf-8")
            (directory / "grading.json").write_text(json.dumps(grade), encoding="utf-8")
            if cfg == ABLATION:
                self.ablation_records[path] = run
            if cfg == "opendeepmind_full" and case["triz_allowed"] is not True:
                self.production_non_triz.append(path)

    def invoke(self, name: str, *args: str) -> None:
        # Full workspaces exercise filesystem I/O; elapsed time is not a scoring assertion.
        result = subprocess.run([sys.executable, str(EVALS / "scripts" / name), *args],
                                cwd=REPO, text=True, capture_output=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def aggregate(self) -> dict:
        # Reports may change; source artifacts must retain their exact bytes.
        before = {path: path.read_bytes() for path in self.workspace.rglob("*") if path.is_file()}
        output = self.root / "report.json"
        self.invoke("aggregate_benchmark.py", str(self.workspace), "--output", str(output))
        self.assertEqual({path: path.read_bytes() for path in before}, before)
        return json.loads(output.read_text(encoding="utf-8"))

    def mutate_ablation(self, **updates) -> None:
        for path, original in self.ablation_records.items():
            path.write_text(json.dumps({**original, **updates}), encoding="utf-8")

    def assert_rejected_ablation(self, report: dict, diagnostic: str) -> None:
        self.assertEqual(report["expected_runs"], 114)
        self.assertEqual(report["complete_runs"], 108)
        self.assertFalse(report["artifact_set_complete"])
        self.assertFalse(report["publication_ready"])
        self.assertEqual(report["incomplete_run_directories"], [])
        self.assertNotIn(ABLATION, report["configurations"])
        errors = report["metadata_errors"]
        for path in self.ablation_records:
            self.assertTrue(any(str(path.parent) in error and diagnostic in error for error in errors), errors)
        comparison = report["comparisons"]["triz_module_ablation"]
        self.assertEqual(comparison["paired_runs"], 0)
        for field in ("left_case_pass_wins", "right_case_pass_wins", "case_pass_ties"):
            self.assertEqual(comparison[field], 0)
        for field in ("mean_assertion_pass_rate_delta_left_minus_right",
                      "mean_judge_score_delta_left_minus_right", "mean_tokens_delta_left_minus_right",
                      "mean_duration_ms_delta_left_minus_right"):
            self.assertIsNone(comparison[field])
        for comparison_id in ("full_vs_no_skill", "full_vs_first_principles_baseline"):
            self.assertEqual(report["comparisons"][comparison_id]["paired_runs"], 36)

    def test_complete_validation_workspace_preserves_valid_ablation_and_baselines(self) -> None:
        report = self.aggregate()
        self.assertEqual(report["expected_runs"], 114)
        self.assertEqual(report["complete_runs"], 114)
        self.assertEqual(report["metadata_errors"], [])
        self.assertTrue(report["artifact_set_complete"])
        self.assertFalse(report["publication_ready"])
        self.assertEqual(report["configurations"][ABLATION]["runs"], 6)
        self.assertIsNone(report["configurations"][ABLATION]["routing_accuracy"])
        for cfg in ("no_skill", "first_principles_baseline", "opendeepmind_full"):
            self.assertEqual(report["configurations"][cfg]["runs"], 36)
        comparison = report["comparisons"]["triz_module_ablation"]
        self.assertEqual(comparison["paired_runs"], 6)
        self.assertEqual(comparison["right_case_pass_wins"], 6)
        self.assertEqual(comparison["mean_assertion_pass_rate_delta_left_minus_right"], -1.0)

    def test_disabled_module_in_route_or_loads_cannot_enter_any_metrics(self) -> None:
        for route, modules in (("triz", []), ("p", ["first-principles", "triz"]),
                               ("triz", ["triz", "first-principles"])):
            with self.subTest(route=route, modules=modules):
                self.mutate_ablation(route=route, loaded_modules=modules)
                self.assert_rejected_ablation(self.aggregate(), "disabled_modules")

    def test_forced_route_requires_the_selected_method_even_without_forbidden_loads(self) -> None:
        for route in ("phi", "phi-p", "none", "unknown"):
            with self.subTest(route=route):
                self.mutate_ablation(route=route, loaded_modules=[])
                self.assert_rejected_ablation(self.aggregate(), "forced_route")

    def test_route_requires_its_modules_to_be_listed_as_loaded(self) -> None:
        path = self.production_non_triz[0]
        for route, loaded_modules, missing in (
            ("phi", [], ["first-philosophy"]),
            ("p", [], ["first-principles"]),
            ("phi-p", ["first-philosophy"], ["first-principles"]),
            ("triz", [], ["triz"]),
        ):
            with self.subTest(route=route, missing=missing):
                run = json.loads(path.read_text(encoding="utf-8"))
                run.update(route=route, loaded_modules=loaded_modules)
                path.write_text(json.dumps(run), encoding="utf-8")

                report = self.aggregate()

                self.assertFalse(report["artifact_set_complete"])
                self.assertEqual(report["configurations"]["opendeepmind_full"]["runs"], 35)
                self.assertTrue(any(
                    str(path.parent) in error and "route requires route modules" in error
                    and str(missing) in error
                    for error in report["metadata_errors"]
                ), report["metadata_errors"])

    def test_one_invalid_run_excludes_only_its_slot_and_pair(self) -> None:
        path, run = next(iter(self.ablation_records.items()))
        path.write_text(json.dumps({**run, "loaded_modules": ["first-principles", "triz"]}), encoding="utf-8")
        report = self.aggregate()
        self.assertEqual(report["complete_runs"], 113)
        self.assertFalse(report["artifact_set_complete"])
        self.assertEqual(report["configurations"][ABLATION]["runs"], 5)
        self.assertEqual(len(report["metadata_errors"]), 1)
        self.assertIn(str(path.parent), report["metadata_errors"][0])
        comparison = report["comparisons"]["triz_module_ablation"]
        self.assertEqual(comparison["paired_runs"], 5)
        self.assertEqual(comparison["right_case_pass_wins"], 5)
        self.assertEqual(comparison["mean_assertion_pass_rate_delta_left_minus_right"], -1.0)

    def test_production_routing_failure_remains_a_measured_observation(self) -> None:
        path = self.production_non_triz[0]
        run = json.loads(path.read_text(encoding="utf-8"))
        run.update(route="triz", loaded_modules=["triz", "first-principles"])
        path.write_text(json.dumps(run), encoding="utf-8")
        report = self.aggregate()
        self.assertEqual(report["complete_runs"], 114)
        self.assertEqual(report["metadata_errors"], [])
        self.assertTrue(report["artifact_set_complete"])
        self.assertFalse(report["publication_ready"])
        metrics = report["configurations"]["opendeepmind_full"]
        self.assertEqual(metrics["runs"], 36)
        self.assertAlmostEqual(metrics["triz_false_activation_rate"], 1 / 36)
        self.assertAlmostEqual(metrics["routing_accuracy"], 35 / 36)


if __name__ == "__main__":
    unittest.main()
