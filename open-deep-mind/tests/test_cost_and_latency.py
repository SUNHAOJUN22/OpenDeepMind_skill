"""Known synthetic records test accounting, never model benchmark outcomes."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

_HELPER_SPEC = importlib.util.spec_from_file_location(
    "cost_latency_pair_fixtures", Path(__file__).with_name("test_pair_model_identity.py")
)
_HELPERS = importlib.util.module_from_spec(_HELPER_SPEC)
_HELPER_SPEC.loader.exec_module(_HELPERS)
AGG, ROOT, row = _HELPERS.AGG, _HELPERS.ROOT, _HELPERS.row


def cost(amount=250, currency="USD", basis="usage_priced", reference="synthetic-rate-snapshot"):
    return {"amount_microunits": amount, "currency": currency, "basis": basis, "pricing_reference": reference}


class CostAndLatencyTests(unittest.TestCase):
    def test_quantiles_use_declared_nearest_rank_and_report_absence(self):
        self.assertEqual(AGG.distribution([]), {"count": 0, "quantile_method": "nearest_rank", "p50": None, "p95": None})
        values = list(range(1, 21))
        self.assertEqual(AGG.distribution(values)["p50"], 10)
        self.assertEqual(AGG.distribution(values)["p95"], 19)
        self.assertEqual(AGG.distribution([7])["p95"], 7)

    def test_cost_contract_rejects_bad_or_ambiguous_accounting(self):
        for amount in (True, -1, 0.1, float("nan"), float("inf"), AGG.MAX_SAFE_INTEGER + 1):
            run = row("opendeepmind_full")[1]
            run["cost"] = cost(amount)
            with self.subTest(amount=amount):
                self.assertTrue(any("cost.amount" in item for item in AGG.validate_run_record(run)))
        for record in (None, {}, cost(currency="usd"), cost(basis="token_guess"), cost(reference=" ")):
            self.assertTrue(AGG.validate_cost(record))
        self.assertEqual(AGG.validate_cost(cost(0)), [])
        self.assertEqual(AGG.validate_cost(cost(AGG.MAX_SAFE_INTEGER)), [])

    def test_missing_cost_is_not_zero_and_mixed_currencies_are_not_averaged(self):
        rows = [row("opendeepmind_full") for _ in range(4)]
        for item, value in zip(rows, (cost(0), cost(20), cost(90, currency="EUR"))):
            item[1]["cost"] = value
        result = AGG.build_metrics(rows)
        self.assertEqual(result["cost_observed_runs"], 3)
        self.assertEqual(result["cost_missing_runs"], 1)
        self.assertEqual(len(result["cost_summaries"]), 2)
        usd = next(item for item in result["cost_summaries"] if item["currency"] == "USD")
        self.assertEqual(usd["mean_microunits"], 10)
        self.assertEqual(usd["distribution_microunits"]["count"], 2)
        self.assertEqual(result["tokens_distribution"]["count"], 4)
        self.assertEqual(result["duration_ms_distribution"]["p95"], 3)

    def pair(self, left_cost, right_cost, **right_kwargs):
        left, right = row("opendeepmind_full"), row("no_skill", **right_kwargs)
        if left_cost is not None:
            left[1]["cost"] = left_cost
        if right_cost is not None:
            right[1]["cost"] = right_cost
        return AGG.paired_comparison({("R01", 1): left}, {("R01", 1): right})

    def test_paired_cost_uses_only_identical_currency_basis_and_rate_snapshot(self):
        result = self.pair(cost(10), cost(30))
        self.assertEqual(result["cost_paired_runs"], 1)
        self.assertEqual(result["cost_delta_summaries_left_minus_right"][0]["mean_microunits"], -20)
        for right in (None, cost(currency="EUR"), cost(basis="provider_reported"), cost(reference="different")):
            with self.subTest(right=right):
                result = self.pair(cost(10), right)
                self.assertEqual(result["paired_runs"], 1)
                self.assertEqual(result["cost_paired_runs"], 0)
                self.assertEqual(result["cost_delta_summaries_left_minus_right"], [])
                self.assertEqual(len(result["excluded_cost_pairs"]), 1)

    def test_existing_model_identity_gate_also_blocks_cost_effect(self):
        result = self.pair(cost(10), cost(30), model="another-synthetic-model")
        self.assertEqual(result["paired_runs"], 0)
        self.assertEqual(result["cost_paired_runs"], 0)
        self.assertEqual(result["excluded_pairs"][0]["reason_codes"], ["MODEL_MISMATCH"])

    def test_cli_preserves_publication_block_and_outputs_route_observations(self):
        item = row("opendeepmind_full")
        item[1]["cost"] = cost()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            case, run, grade = item
            slot = {field: run[field] for field in ("case_id", "configuration", "repetition")}
            (root / "manifest.json").write_text(json.dumps({"benchmark_version": "1.0.0", "expected_run_slots": [slot]}))
            directory = root / "eval-R01/opendeepmind_full/run-1"
            directory.mkdir(parents=True)
            (directory / "run_record.json").write_text(json.dumps(run))
            (directory / "grading.json").write_text(json.dumps(grade))
            process = subprocess.run([sys.executable, str(ROOT / "open-deep-mind/evals/scripts/aggregate_benchmark.py"), str(root)], capture_output=True, text=True)
            self.assertEqual(process.returncode, 0, process.stderr)
            report = json.loads((root / "benchmark.json").read_text())
            self.assertFalse(report["publication_ready"])
            self.assertTrue(report["publication_blockers"])
            metrics = report["configurations"]["opendeepmind_full"]
            self.assertEqual(metrics["by_route"]["phi"]["cost_observed_runs"], 1)
            self.assertEqual(metrics["by_route"]["phi"]["duration_ms_distribution"]["p95"], 3)
            self.assertEqual(json.loads((directory / "run_record.json").read_text()), run)


if __name__ == "__main__":
    unittest.main()
