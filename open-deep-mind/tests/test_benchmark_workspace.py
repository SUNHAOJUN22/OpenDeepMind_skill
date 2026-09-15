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


class BenchmarkWorkspaceTests(unittest.TestCase):
    def test_empty_validation_workspace_cannot_be_publication_ready(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            create = run_script(
                "open-deep-mind/evals/scripts/create_workspace.py",
                "--iteration", "1",
                "--split", "validation",
                "--workspace", tmp,
            )
            self.assertEqual(create.returncode, 0, msg=create.stderr + create.stdout)
            created = json.loads(create.stdout.strip().splitlines()[-1])
            self.assertEqual(created["cases"], 12)
            # 12 validation cases x 3 full-scope configs x 3 reps = 108,
            # plus 2 validation TRIZ-positive cases x no-TRIZ ablation x 3 reps = 6.
            self.assertEqual(created["run_slots"], 114)

            iteration = Path(tmp) / "iteration-1"
            manifest = json.loads((iteration / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(len(manifest["expected_run_slots"]), 114)

            aggregate = run_script(
                "open-deep-mind/evals/scripts/aggregate_benchmark.py",
                str(iteration),
            )
            self.assertEqual(aggregate.returncode, 0, msg=aggregate.stderr + aggregate.stdout)
            summary = json.loads(aggregate.stdout.strip().splitlines()[-1])
            self.assertEqual(summary["expected_runs"], 114)
            self.assertEqual(summary["complete_runs"], 0)
            self.assertEqual(summary["incomplete"], 114)
            self.assertFalse(summary["publication_ready"])

            benchmark = json.loads((iteration / "benchmark.json").read_text(encoding="utf-8"))
            self.assertEqual(benchmark["expected_runs"], 114)
            self.assertEqual(benchmark["complete_runs"], 0)
            self.assertEqual(len(benchmark["incomplete_run_directories"]), 114)
            self.assertFalse(benchmark["publication_ready"])

    def test_complete_synthetic_slot_still_requires_independent_attestation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            iteration = Path(tmp) / "iteration-1"
            run_dir = iteration / "eval-R01" / "no_skill" / "run-1"
            run_dir.mkdir(parents=True)
            (iteration / "manifest.json").write_text(
                json.dumps(
                    {
                        "benchmark_version": "1.0.0",
                        "split": "validation",
                        "expected_run_slots": [
                            {"case_id": "R01", "configuration": "no_skill", "repetition": 1}
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (run_dir / "run_record.json").write_text(
                json.dumps(
                    {
                        "case_id": "R01",
                        "configuration": "no_skill",
                        "repetition": 1,
                        "model": "synthetic-test",
                        "route": "none",
                        "loaded_modules": [],
                        "response_text": "synthetic test response",
                        "total_tokens": 4,
                        "duration_ms": 1,
                    }
                ),
                encoding="utf-8",
            )
            (run_dir / "grading.json").write_text(
                json.dumps(
                    {
                        "case_id": "R01",
                        "configuration": "no_skill",
                        "assertion_results": [],
                        "red_blockers": [],
                        "summary": {
                            "passed": 0,
                            "failed": 0,
                            "total": 0,
                            "pass_rate": 0.0,
                            "case_passed": False,
                        },
                    }
                ),
                encoding="utf-8",
            )

            aggregate = run_script(
                "open-deep-mind/evals/scripts/aggregate_benchmark.py",
                str(iteration),
            )
            self.assertEqual(aggregate.returncode, 0, msg=aggregate.stderr + aggregate.stdout)
            benchmark = json.loads((iteration / "benchmark.json").read_text(encoding="utf-8"))
            self.assertTrue(benchmark["artifact_set_complete"])
            self.assertFalse(benchmark["publication_ready"])
            self.assertEqual(
                benchmark["publication_status"],
                "EVIDENCE_COMPLETE_AWAITING_INDEPENDENT_ATTESTATION",
            )
            self.assertIn(
                "INDEPENDENT_PUBLICATION_ATTESTATION_NOT_VERIFIED",
                benchmark["publication_blockers"],
            )

    def test_nonfinite_artifacts_are_rejected_before_completeness_or_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            iteration = Path(tmp) / "iteration-1"
            run_dir = iteration / "eval-R01" / "no_skill" / "run-1"
            run_dir.mkdir(parents=True)
            (iteration / "manifest.json").write_text(
                json.dumps(
                    {
                        "benchmark_version": "1.0.0",
                        "split": "validation",
                        "expected_run_slots": [
                            {"case_id": "R01", "configuration": "no_skill", "repetition": 1}
                        ],
                    }
                ),
                encoding="utf-8",
            )
            (run_dir / "run_record.json").write_text(
                '{"case_id":"R01","configuration":"no_skill","repetition":1,'
                '"model":"synthetic-test","route":"none","loaded_modules":[],'
                '"response_text":"synthetic","total_tokens":NaN,"duration_ms":1}',
                encoding="utf-8",
            )
            (run_dir / "grading.json").write_text(
                json.dumps(
                    {
                        "case_id": "R01",
                        "configuration": "no_skill",
                        "assertion_results": [],
                        "red_blockers": [],
                        "summary": {
                            "passed": 0,
                            "failed": 1,
                            "total": 1,
                            "pass_rate": 0.0,
                            "case_passed": False,
                        },
                    }
                ),
                encoding="utf-8",
            )

            aggregate = run_script(
                "open-deep-mind/evals/scripts/aggregate_benchmark.py",
                str(iteration),
            )
            self.assertEqual(aggregate.returncode, 0, msg=aggregate.stderr + aggregate.stdout)
            raw = (iteration / "benchmark.json").read_text(encoding="utf-8")
            self.assertNotIn("NaN", raw)
            self.assertNotIn("Infinity", raw)
            benchmark = json.loads(raw)
            self.assertEqual(benchmark["complete_runs"], 0)
            self.assertFalse(benchmark["artifact_set_complete"])
            self.assertEqual(benchmark["publication_status"], "INCOMPLETE_ARTIFACT_SET")
            self.assertTrue(any("nonfinite JSON constant" in error for error in benchmark["metadata_errors"]))
            self.assertNotIn("no_skill", benchmark["configurations"])


class WorkspacePreservationTests(unittest.TestCase):
    """Creation never adopts or rewrites an existing iteration's evidence."""

    def _create(self, root: str, iteration: int = 1, split: str = "validation"):
        return run_script(
            "open-deep-mind/evals/scripts/create_workspace.py",
            "--iteration", str(iteration), "--split", split, "--workspace", root,
        )

    @staticmethod
    def _snapshot(root: Path) -> dict[str, bytes | None]:
        return {
            str(path.relative_to(root)): path.read_bytes() if path.is_file() else None
            for path in sorted(root.rglob("*"))
        }

    def test_recreation_never_rewrites_completed_or_edited_evidence(self) -> None:
        for split in ("validation", "train"):
            with self.subTest(split=split), tempfile.TemporaryDirectory() as tmp:
                created = self._create(tmp)
                self.assertEqual(created.returncode, 0, created.stderr)
                iteration = Path(tmp) / "iteration-1"
                manifest_path = iteration / "manifest.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest["status"] = "synthetic-evidence-present-not-published"
                manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                instruction = next(iteration.rglob("run_instructions.json"))
                instruction.write_text('{"operator_note":"preserve this exact record"}', encoding="utf-8")
                (instruction.parent / "run_record.json").write_text(
                    '{"model":"synthetic-regression-no-model-execution"}', encoding="utf-8"
                )
                (instruction.parent / "outputs" / "response.txt").write_text(
                    "synthetic recorded output", encoding="utf-8"
                )
                before = self._snapshot(iteration)
                repeated = self._create(tmp, split=split)
                self.assertNotEqual(repeated.returncode, 0, repeated.stdout)
                self.assertIn("already exists", repeated.stderr)
                self.assertNotIn("Traceback", repeated.stderr)
                self.assertEqual(self._snapshot(iteration), before)

    def test_existing_empty_directory_is_not_silently_adopted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            iteration = Path(tmp) / "iteration-1"
            iteration.mkdir()
            result = self._create(tmp)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("already exists", result.stderr)
            self.assertEqual(list(iteration.iterdir()), [])

    def test_existing_file_is_preserved_with_a_cli_diagnostic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            iteration = Path(tmp) / "iteration-1"
            iteration.write_bytes(b"existing user content")
            result = self._create(tmp)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("already exists", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertEqual(iteration.read_bytes(), b"existing user content")

    def test_new_iteration_preserves_previous_iteration(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first = self._create(tmp)
            self.assertEqual(first.returncode, 0, first.stderr)
            previous = Path(tmp) / "iteration-1"
            before = self._snapshot(previous)
            second = self._create(tmp, iteration=2, split="train")
            self.assertEqual(second.returncode, 0, second.stderr)
            manifest = json.loads((Path(tmp) / "iteration-2/manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["iteration"], 2)
            self.assertEqual(manifest["split"], "train")
            self.assertEqual(self._snapshot(previous), before)

    def test_competing_creators_cannot_both_claim_the_same_iteration(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = [sys.executable, str(REPO / "open-deep-mind/evals/scripts/create_workspace.py"),
                    "--iteration", "1", "--workspace", tmp]
            processes = [subprocess.Popen(base + ["--split", split], cwd=REPO,
                         text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                         for split in ("train", "validation")]
            try:
                outputs = [process.communicate(timeout=30) for process in processes]
            finally:
                for process in processes:
                    if process.poll() is None:
                        process.kill()
                    process.wait()
            codes = [process.returncode for process in processes]
            self.assertEqual(codes.count(0), 1, (codes, outputs))
            winner = codes.index(0)
            loser = 1 - winner
            self.assertIn("already exists", outputs[loser][1])
            manifest = json.loads((Path(tmp) / "iteration-1/manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["split"], ("train", "validation")[winner])
            expected = {(slot["case_id"], slot["configuration"], slot["repetition"])
                        for slot in manifest["expected_run_slots"]}
            actual = set()
            for path in (Path(tmp) / "iteration-1").rglob("run_instructions.json"):
                record = json.loads(path.read_text(encoding="utf-8"))
                actual.add((record["case_id"], record["configuration"], record["repetition"]))
                self.assertEqual(record["split"], manifest["split"])
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
