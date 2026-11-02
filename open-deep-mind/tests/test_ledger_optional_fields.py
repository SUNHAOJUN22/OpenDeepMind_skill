"""Keep optional evidence and decision fields consistent with the ledger schema."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_ledger.py"
SPEC = importlib.util.spec_from_file_location("ledger_optional_fields", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
ledger = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ledger)


def example():
    return json.loads((ROOT / "assets/example-ledger.json").read_text(encoding="utf-8"))


class OptionalLedgerFieldTests(unittest.TestCase):
    def test_claim_provenance_fields_reject_non_strings(self):
        for field in ("source", "owner", "review_date"):
            for value in (None, False, 20270101, 0.5, [], {"text": "source"}):
                with self.subTest(field=field, value=value):
                    data = example()
                    data["claims"][1][field] = value
                    self.assertEqual(
                        ledger.validate(data), [f"claims[1].{field} must be a string"],
                    )

    def test_claim_provenance_fields_can_be_omitted(self):
        data = example()
        for claim in data["claims"]:
            for field in ("source", "owner", "review_date"):
                claim.pop(field)
        self.assertEqual(ledger.validate(data), [])

    def test_optional_claim_text_does_not_require_new_content_rules(self):
        # These properties have type:string but no minLength or date format.
        for value in ("", " ", "来源：测量记录；复核时间待定"):
            with self.subTest(value=value):
                data = example()
                for claim in data["claims"]:
                    for field in ("source", "owner", "review_date"):
                        claim[field] = value
                self.assertEqual(ledger.validate(data), [])

    def test_decision_uncertainty_rejects_non_strings(self):
        for value in (None, True, 1, 0.5, [], {"estimate": "low"}):
            with self.subTest(value=value):
                data = example()
                data["decision"]["uncertainty"] = value
                self.assertEqual(
                    ledger.validate(data), ["decision.uncertainty must be a string"],
                )

    def test_decision_uncertainty_can_be_omitted_or_empty(self):
        data = example()
        del data["decision"]["uncertainty"]
        self.assertEqual(ledger.validate(data), [])
        for value in ("", " ", "观察存在不确定性"):
            with self.subTest(value=value):
                data["decision"]["uncertainty"] = value
                self.assertEqual(ledger.validate(data), [])

    def test_optional_decision_must_be_an_object_when_present(self):
        for value in (None, False, 0, [], "pending"):
            with self.subTest(value=value):
                data = example()
                data["decision"] = value
                self.assertEqual(ledger.validate(data), ["decision must be an object"])

    def test_omitted_decision_remains_valid(self):
        data = example()
        del data["decision"]
        self.assertEqual(ledger.validate(data), [])

    def test_unknown_extension_metadata_remains_valid(self):
        data = example()
        for record in (data, data["claims"][0], data["inferences"][0], data["decision"]):
            record["extension"] = {"reviewed": False, "evidence": [None, {"id": 1}]}
        self.assertEqual(ledger.validate(data), [])

    def test_public_cli_rejects_malformed_optional_fields(self):
        cases = (
            (("claims", 1, "source"), {"uri": "measurement.csv"},
             "claims[1].source must be a string"),
            (("claims", 4, "owner"), ["engineering"],
             "claims[4].owner must be a string"),
            (("claims", 0, "review_date"), 20270101,
             "claims[0].review_date must be a string"),
            (("decision", "uncertainty"), ["unresolved calibration"],
             "decision.uncertainty must be a string"),
            (("decision",), None, "decision must be an object"),
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.json"
            for keys, value, error in cases:
                with self.subTest(path=keys):
                    data = example()
                    container = data
                    for key in keys[:-1]:
                        container = container[key]
                    container[keys[-1]] = value
                    path.write_text(json.dumps(data), encoding="utf-8")
                    result = subprocess.run(
                        [sys.executable, str(SCRIPT), str(path)],
                        text=True, capture_output=True, check=False, timeout=10,
                    )
                    self.assertEqual(result.returncode, 1, result.stdout)
                    self.assertEqual(json.loads(result.stdout), {"ok": False, "errors": [error]})
                    self.assertEqual(result.stderr.strip(), f"ERROR: {error}")


if __name__ == "__main__":
    unittest.main()
