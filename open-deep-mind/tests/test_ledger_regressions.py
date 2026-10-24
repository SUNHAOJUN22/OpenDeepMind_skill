from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ledger_regression_target", ROOT / "scripts/validate_ledger.py")
assert SPEC is not None and SPEC.loader is not None
ledger = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ledger)


class LedgerRegressionTests(unittest.TestCase):
    def test_malformed_enum_types_are_validation_errors(self) -> None:
        for field in ("type", "status"):
            for value in ([], {}, None):
                with self.subTest(field=field, value=value):
                    data = json.loads((ROOT / "assets/example-ledger.json").read_text(encoding="utf-8"))
                    data["claims"][0][field] = value
                    self.assertTrue(ledger.validate(data))

    def test_invalid_rule_is_reported(self) -> None:
        data = json.loads((ROOT / "assets/example-ledger.json").read_text(encoding="utf-8"))
        data["inferences"][0]["rule"] = []
        self.assertTrue(ledger.validate(data))

    def test_defeaters_must_match_schema_item_type(self) -> None:
        for invalid in (None, 1, [], {}):
            with self.subTest(invalid=invalid):
                data = json.loads((ROOT / "assets/example-ledger.json").read_text(encoding="utf-8"))
                data["inferences"][0]["defeaters"] = [invalid]
                self.assertIn(
                    "inferences[0].defeaters must contain strings",
                    ledger.validate(data),
                )

    def test_cli_rejects_non_string_defeaters(self) -> None:
        data = json.loads((ROOT / "assets/example-ledger.json").read_text(encoding="utf-8"))
        data["inferences"][0]["defeaters"] = [None]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            process = subprocess.run(
                [sys.executable, str(ROOT / "scripts/validate_ledger.py"), str(path)],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(process.returncode, 1)
        self.assertIn("defeaters must contain strings", process.stdout)

    def test_deep_acyclic_graph_does_not_use_recursion(self) -> None:
        graph = {f"A{i}": {f"A{i+1}"} for i in range(2000)}
        graph["A2000"] = set()
        self.assertEqual(ledger.find_cycles(graph), [])

    def test_cycle_diagnostics_are_order_independent(self) -> None:
        graph = {"A": {"B"}, "B": {"A"}, "C": set()}
        self.assertEqual(ledger.find_cycles(graph), ledger.find_cycles(dict(reversed(list(graph.items())))))


if __name__ == "__main__":
    unittest.main()
