from __future__ import annotations

import importlib.util
import random
import sys
import unittest
from collections import Counter
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "contracts_v17.py"
SPEC = importlib.util.spec_from_file_location("open_deep_mind_contracts_v17", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"cannot load {MODULE_PATH}")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class OpenDeepMindContractsV17Tests(unittest.TestCase):
    def test_triz_requires_explicit_request_or_acceptance(self) -> None:
        self.assertFalse(MODULE.triz_enabled(explicit_request=False, explicit_acceptance=False))
        self.assertTrue(MODULE.triz_enabled(explicit_request=True, explicit_acceptance=False))
        self.assertTrue(MODULE.triz_enabled(explicit_request=False, explicit_acceptance=True))

    def test_negated_triz_request_remains_disabled(self) -> None:
        self.assertFalse(
            MODULE.triz_enabled(
                explicit_request=True,
                explicit_acceptance=False,
                negated=True,
            )
        )

    def test_expected_slots_are_the_only_completeness_denominator(self) -> None:
        decision = MODULE.publication_decision(
            ["phi-1", "p-1", "t-1"],
            ["phi-1", "p-1"],
            holdout_sealed=True,
            exact_revision_bound=True,
        )
        self.assertEqual(decision.status, "BLOCKED")
        self.assertAlmostEqual(decision.completeness or 0.0, 2.0 / 3.0)
        self.assertEqual(decision.missing_slots, ("t-1",))

    def test_duplicate_and_orphan_runs_block_publication(self) -> None:
        decision = MODULE.publication_decision(
            ["phi-1", "p-1"],
            ["phi-1", "phi-1", "p-1", "orphan"],
            holdout_sealed=True,
            exact_revision_bound=True,
        )
        self.assertEqual(decision.status, "BLOCKED")
        self.assertEqual(decision.duplicate_slots, ("phi-1",))
        self.assertEqual(decision.orphan_slots, ("orphan",))

    def test_complete_unique_slots_do_not_self_authorize_publication(self) -> None:
        decision = MODULE.publication_decision(
            ["phi-1", "p-1"],
            ["phi-1", "p-1"],
            holdout_sealed=True,
            exact_revision_bound=True,
        )
        self.assertEqual(decision.status, "ARTIFACT_SET_COMPLETE")
        self.assertFalse(decision.publication_ready)
        self.assertEqual(decision.completeness, 1.0)

    def test_missing_slot_scores_do_not_produce_a_behavior_score(self) -> None:
        self.assertIsNone(MODULE.weighted_behavior_score({"phi-1": 0.9}, ["phi-1", "p-1"]))

    def test_framework_does_not_publish_without_actual_model_runs(self) -> None:
        status = MODULE.framework_status(publication_ready=True, actual_model_runs_present=False)
        self.assertEqual(
            status,
            "BENCHMARK_FRAMEWORK_VALIDATED / NO_PUBLISHED_BEHAVIORAL_SCORE",
        )

    def test_slot_decisions_match_an_independent_multiset_oracle(self) -> None:
        rng = random.Random(20261102)
        for trial in range(200):
            expected = [f"case-{i}" for i in range(rng.randint(1, 30))]
            observed = rng.choices(expected + ["orphan-a", "orphan-b"], k=rng.randrange(80))
            sealed, bound = bool(trial % 2), bool(trial % 3)
            frequencies = Counter(observed)
            missing = tuple(sorted(set(expected) - set(observed)))
            duplicates = tuple(sorted(key for key, count in frequencies.items() if count > 1))
            orphans = tuple(sorted(set(observed) - set(expected)))
            reasons = tuple(code for condition, code in (
                (missing, "MISSING_EXPECTED_SLOT"),
                (duplicates, "DUPLICATE_SLOT"),
                (orphans, "ORPHAN_SLOT"),
                (not sealed, "HOLDOUT_NOT_SEALED"),
                (not bound, "EXACT_REVISION_NOT_BOUND"),
            ) if condition)
            with self.subTest(trial=trial):
                result = MODULE.publication_decision(
                    iter(expected), iter(observed),
                    holdout_sealed=sealed, exact_revision_bound=bound,
                )
                self.assertEqual(result.missing_slots, missing)
                self.assertEqual(result.duplicate_slots, duplicates)
                self.assertEqual(result.orphan_slots, orphans)
                self.assertEqual(result.reason_codes, reasons)
                self.assertEqual(result.completeness,
                                 sum(observed.count(slot) == 1 for slot in expected) / len(expected))
                self.assertEqual(result.status, "BLOCKED" if reasons else "ARTIFACT_SET_COMPLETE")
                self.assertFalse(result.publication_ready)

    def test_large_slot_inventory_preserves_missing_duplicate_and_orphan_evidence(self) -> None:
        expected = [f"slot-{i:05d}" for i in range(10_000)]
        observed = expected[:-10] + expected[:7] + ["external-z", "external-a", "external-m"]
        result = MODULE.publication_decision(
            iter(expected), iter(observed), holdout_sealed=True, exact_revision_bound=True,
        )
        self.assertEqual(result.missing_slots, tuple(expected[-10:]))
        self.assertEqual(result.duplicate_slots, tuple(expected[:7]))
        self.assertEqual(result.orphan_slots, ("external-a", "external-m", "external-z"))
        self.assertEqual(result.completeness, (10_000 - 10 - 7) / 10_000)
        self.assertEqual(result.reason_codes,
                         ("MISSING_EXPECTED_SLOT", "DUPLICATE_SLOT", "ORPHAN_SLOT"))
        self.assertFalse(result.publication_ready)

    def test_slot_membership_work_has_a_linear_hash_budget(self) -> None:
        class CountedSlot(str):
            calls = 0

            def __hash__(self) -> int:
                CountedSlot.calls += 1
                return super().__hash__()

        size = 500
        expected = [CountedSlot(f"slot-{i}") for i in range(size)]
        observed = [CountedSlot(f"slot-{i}") for i in range(size)]
        CountedSlot.calls = 0
        result = MODULE.publication_decision(
            expected, observed, holdout_sealed=True, exact_revision_bound=True,
        )
        self.assertEqual(result.completeness, 1.0)
        # A deterministic work budget, independent of CPU speed or wall-clock noise.
        self.assertLessEqual(CountedSlot.calls, 12 * (len(expected) + len(observed)))


if __name__ == "__main__":
    unittest.main()
