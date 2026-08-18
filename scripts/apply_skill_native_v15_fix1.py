from pathlib import Path

root = Path(__file__).resolve().parents[1]
target = root / "open-deep-mind/tests/test_contracts_v15.py"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text('''from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts/contracts_v15.py"
SPEC = importlib.util.spec_from_file_location("contracts_v15", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ContractTests(unittest.TestCase):
    def test_expected_slot_denominator_and_publication_gate(self) -> None:
        decision = MODULE.publication_gate(
            expected_slots=["a", "b", "c"],
            completed_slots=["a", "b", "c"],
            blocking_findings=0,
            holdout_sealed=True,
            attestation_valid=True,
            exact_revision_bound=True,
        )
        self.assertEqual(decision.status, "PASS")
        self.assertEqual(decision.completeness, 1.0)

    def test_missing_slot_holds(self) -> None:
        decision = MODULE.publication_gate(
            expected_slots=["a", "b"],
            completed_slots=["a"],
            blocking_findings=0,
            holdout_sealed=True,
            attestation_valid=True,
            exact_revision_bound=True,
        )
        self.assertEqual(decision.status, "HOLD")
        self.assertIn("INCOMPLETE_EXPECTED_SLOTS", decision.reason_codes)

    def test_duplicate_completed_slot_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            MODULE.expected_slot_completeness(["a", "b"], ["a", "a"])

    def test_triz_is_explicit_only(self) -> None:
        self.assertFalse(MODULE.triz_active(explicit_request=False, explicit_acceptance=False))
        self.assertTrue(MODULE.triz_active(explicit_request=True, explicit_acceptance=False))

    def test_boolean_is_not_a_numeric_blocker_count(self) -> None:
        with self.assertRaises(TypeError):
            MODULE.publication_gate(
                expected_slots=["a"],
                completed_slots=["a"],
                blocking_findings=False,
                holdout_sealed=True,
                attestation_valid=True,
                exact_revision_bound=True,
            )


if __name__ == "__main__":
    unittest.main()
''', encoding="utf-8", newline="\n")
print("fixed dynamic import registration")
