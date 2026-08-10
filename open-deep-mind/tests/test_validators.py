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


class ModuleValidationTests(unittest.TestCase):
    def assert_ok(self, rel: str, *args: str) -> subprocess.CompletedProcess[str]:
        proc = run_script(rel, *args)
        self.assertEqual(proc.returncode, 0, msg=f"{rel}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
        return proc

    def test_module_registry_and_activation_boundaries(self) -> None:
        registry = json.loads((REPO / "open-deep-mind/MODULES.json").read_text(encoding="utf-8"))
        modules = {m["id"]: m for m in registry["modules"]}
        self.assertEqual(set(modules), {"first-philosophy", "first-principles", "triz"})
        self.assertEqual(modules["first-philosophy"]["entry"], "first-philosophy/METHOD.md")
        self.assertEqual(modules["first-principles"]["entry"], "first-principles/METHOD.md")
        self.assertEqual(modules["triz"]["entry"], "triz/ROUTER.md")
        self.assertEqual(modules["triz"]["activation"], "explicit-only")
        self.assertIn("triz", modules["first-philosophy"]["must_not_auto_load"])
        self.assertIn("triz", modules["first-principles"]["must_not_auto_load"])

    def test_compatibility_aliases_are_thin(self) -> None:
        aliases = {
            "open-deep-mind/FIRST_PHILOSOPHY.md": "first-philosophy/METHOD.md",
            "open-deep-mind/FIRST_PRINCIPLES.md": "first-principles/METHOD.md",
            "open-deep-mind/TRIZ_ENGINEERING.md": "triz/ROUTER.md",
        }
        for rel, target in aliases.items():
            text = (REPO / rel).read_text(encoding="utf-8")
            self.assertIn(target, text)
            self.assertLessEqual(len(text.splitlines()), 45)

    def test_canonical_core_methods_do_not_embed_triz(self) -> None:
        for rel in (
            "open-deep-mind/first-philosophy/METHOD.md",
            "open-deep-mind/first-principles/METHOD.md",
        ):
            text = (REPO / rel).read_text(encoding="utf-8").upper()
            self.assertNotIn("TRIZ", text, msg=f"canonical core method is coupled to TRIZ: {rel}")

    def test_domain_router_has_no_default_triz(self) -> None:
        text = (REPO / "open-deep-mind/references/domain-routing.md").read_text(encoding="utf-8")
        self.assertIn("TRIZ isolation rule", text)
        self.assertIn("Explicit TRIZ engineering route", text)
        self.assertNotIn("- TRIZ contradiction", text)

    def test_first_philosophy_module(self) -> None:
        proc = self.assert_ok("open-deep-mind/first-philosophy/scripts/validate_module.py")
        data = json.loads(proc.stdout.strip().splitlines()[-1])
        self.assertEqual(data["stages"], 8)

    def test_first_principles_module(self) -> None:
        proc = self.assert_ok("open-deep-mind/first-principles/scripts/validate_module.py")
        data = json.loads(proc.stdout.strip().splitlines()[-1])
        self.assertEqual(data["stages"], 9)

    def test_triz_module(self) -> None:
        proc = self.assert_ok("open-deep-mind/triz/scripts/validate_triz_module.py")
        data = json.loads(proc.stdout.strip().splitlines()[-1])
        self.assertEqual(data["t_stages"], 10)
        self.assertEqual(data["matrix_cells"], 1190)
        self.assertEqual(data["sis"], 76)

    def test_matrix_anchor_lookup(self) -> None:
        proc = self.assert_ok(
            "open-deep-mind/triz/scripts/lookup_matrix.py",
            "--improve", "1", "--worsen", "3", "--json",
        )
        data = json.loads(proc.stdout)
        self.assertEqual([p["id"] for p in data["principles"]], [15, 8, 29, 34])
        self.assertFalse(data["normalization_applied"])

    def test_known_matrix_anomaly_is_explicitly_normalized(self) -> None:
        proc = self.assert_ok(
            "open-deep-mind/triz/scripts/lookup_matrix.py",
            "--improve", "19", "--worsen", "9", "--json",
        )
        data = json.loads(proc.stdout)
        self.assertEqual(data["raw_principle_ids"], [8, 35, 35])
        self.assertEqual([p["id"] for p in data["principles"]], [8, 35])
        self.assertTrue(data["normalization_applied"])
        self.assertIsInstance(data["known_anomaly"], dict)

    def test_standard_solution_lookup(self) -> None:
        proc = self.assert_ok(
            "open-deep-mind/triz/scripts/lookup_standard_solution.py",
            "1.2.1", "--json",
        )
        data = json.loads(proc.stdout)
        self.assertTrue(data["ok"])
        self.assertEqual(data["id"], "1.2.1")
        self.assertTrue(data["title"])

    def test_example_ledger(self) -> None:
        self.assert_ok(
            "open-deep-mind/scripts/validate_ledger.py",
            "open-deep-mind/assets/example-ledger.json",
        )

    def test_ledger_cycle_is_rejected(self) -> None:
        cyclic = {
            "analysis_id": "cycle-test",
            "question": "Is this dependency graph valid?",
            "domain": "test",
            "scale": "unit",
            "purpose": "validator regression",
            "claims": [
                {
                    "id": "A1",
                    "type": "A",
                    "claim": "Assumption one",
                    "status": "plausible",
                    "scope": "test",
                    "falsifier": "counterexample",
                    "dependencies": ["A2"],
                },
                {
                    "id": "A2",
                    "type": "A",
                    "claim": "Assumption two",
                    "status": "plausible",
                    "scope": "test",
                    "falsifier": "counterexample",
                    "dependencies": ["A1"],
                },
            ],
            "inferences": [],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cycle.json"
            path.write_text(json.dumps(cyclic), encoding="utf-8")
            proc = run_script("open-deep-mind/scripts/validate_ledger.py", str(path))
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("dependency cycle detected", proc.stderr)


if __name__ == "__main__":
    unittest.main()
