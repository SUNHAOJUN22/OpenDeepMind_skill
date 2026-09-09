from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_ledger.py"
SPEC = importlib.util.spec_from_file_location("ledger_raw_budgets", SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load ledger validator")
ledger = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ledger)


def claim(index=0, dependencies=None):
    result = {
        "id": f"D{index}", "type": "D", "claim": "Reference definition",
        "status": "supported", "scope": "reference", "falsifier": "",
    }
    if dependencies is not None:
        result["dependencies"] = dependencies
    return result


def document():
    return {
        "analysis_id": "budget-case", "question": "bounded validation?",
        "domain": "software", "scale": "local", "purpose": "regression",
        "claims": [claim()],
    }


class RawLedgerBudgetTests(unittest.TestCase):
    def test_repeated_records_rejected_before_graph_or_diagnostics_expand(self):
        data = document()
        data["claims"] = [claim()] * 10_001
        with patch.object(ledger, "find_cycles", side_effect=AssertionError("graph must not run")):
            self.assertEqual(ledger.validate(data), ["ledger record count exceeds the 10000-record budget"])

    def test_claim_and_inference_counts_share_one_budget(self):
        data = document()
        data["claims"] = [claim()] * 5_001
        data["inferences"] = [{}] * 5_000
        with patch.object(ledger, "find_cycles", side_effect=AssertionError("graph must not run")):
            self.assertEqual(ledger.validate(data), ["ledger record count exceeds the 10000-record budget"])

    def test_repeated_dependencies_are_counted_before_set_deduplication(self):
        data = document()
        data["claims"].append(claim(1, ["D0"] * 100_001))
        self.assertEqual(ledger.validate(data), ["ledger reference count exceeds the 100000-reference budget"])

    def test_invalid_reference_types_cannot_bypass_the_budget(self):
        data = document()
        data["claims"][0]["dependencies"] = [None] * 100_001
        self.assertEqual(ledger.validate(data), ["ledger reference count exceeds the 100000-reference budget"])

    def test_all_reference_surfaces_share_the_same_budget(self):
        data = document()
        data["claims"].append(claim(1, ["D0"] * 50_000))
        data["inferences"] = [{"id": "I0", "premises": ["D0"] * 50_000,
                               "rule": "deduction", "conclusion": "reference"}]
        data["decision"] = {"recommendation": "review", "foundation_trace": ["I0"]}
        self.assertEqual(ledger.validate(data), ["ledger reference count exceeds the 100000-reference budget"])

    def test_exact_record_budget_and_forward_references_remain_valid(self):
        data = document()
        data["claims"] = [claim(i) for i in range(10_000)]
        data["claims"][0]["dependencies"] = ["D9999"]
        self.assertEqual(ledger.validate(data), [])

    def test_exact_reference_budget_remains_valid(self):
        data = document()
        data["claims"].append(claim(1, ["D0"] * 100_000))
        self.assertEqual(ledger.validate(data), [])

    def test_malformed_containers_keep_structured_validation(self):
        for field in ("claims", "inferences", "decision"):
            with self.subTest(field=field):
                data = document()
                data[field] = "not a container"
                self.assertTrue(ledger.validate(data))
        self.assertEqual(ledger.validate([]), ["top-level JSON must be an object"])

    def test_cli_reports_oversized_reference_list_as_one_error(self):
        data = document()
        data["claims"].append(claim(1, ["D0"] * 100_001))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)],
                                    capture_output=True, text=True, check=False, timeout=10)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout), {
            "ok": False, "errors": ["ledger reference count exceeds the 100000-reference budget"]
        })
        self.assertLess(len(result.stderr), 200)


if __name__ == "__main__":
    unittest.main()
