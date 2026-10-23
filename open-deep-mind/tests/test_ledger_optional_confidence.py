"""Public CLI checks for optional numeric confidence in claim and inference records."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OMITTED = object()


class OptionalConfidenceTests(unittest.TestCase):
    def validate_confidence(self, collection, value=OMITTED):
        document = json.loads((ROOT / "assets/example-ledger.json").read_text(encoding="utf-8"))
        record = document[collection][0]
        if value is OMITTED:
            record.pop("confidence", None)
        else:
            record["confidence"] = value
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "ledger.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            process = subprocess.run(
                [sys.executable, str(ROOT / "scripts/validate_ledger.py"), str(path)],
                text=True, capture_output=True, check=False, timeout=10,
            )
        self.assertNotIn("Traceback", process.stderr)
        return process.returncode, json.loads(process.stdout)

    def test_claim_null_confidence_is_not_an_omitted_number(self):
        code, result = self.validate_confidence("claims", None)
        self.assertEqual(code, 1, result)
        self.assertFalse(result["ok"])
        self.assertTrue(any("claims[0].confidence" in error for error in result["errors"]))

    def test_inference_null_confidence_is_not_an_omitted_number(self):
        code, result = self.validate_confidence("inferences", None)
        self.assertEqual(code, 1, result)
        self.assertFalse(result["ok"])
        self.assertTrue(any("inferences[0].confidence" in error for error in result["errors"]))

    def test_confidence_can_be_omitted_in_both_record_types(self):
        for collection in ("claims", "inferences"):
            with self.subTest(collection=collection):
                code, result = self.validate_confidence(collection)
                self.assertEqual(code, 0, result)
                self.assertTrue(result["ok"])

    def test_numeric_endpoints_remain_valid_in_both_record_types(self):
        for collection in ("claims", "inferences"):
            for value in (0, 1):
                with self.subTest(collection=collection, value=value):
                    code, result = self.validate_confidence(collection, value)
                    self.assertEqual(code, 0, result)
                    self.assertTrue(result["ok"])


if __name__ == "__main__":
    unittest.main()
