"""Synthetic registry checks; no model execution or method-quality claims."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "audited_prepare_context", Path(__file__).parents[1] / "scripts/prepare_context.py"
)
assert SPEC is not None and SPEC.loader is not None
PREPARE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREPARE)


class ContextRegistryIntegrityTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        registry = {
            "router": "SKILL.md",
            "modules": [
                {"id": key, "entry": entry,
                 "activation": "explicit-only" if key == "triz" else "core-or-explicit"}
                for key, entry in PREPARE.CANONICAL_ENTRIES.items()
            ],
        }
        self.registry = self.root / "MODULES.json"
        self.original = json.dumps(registry)
        self.registry.write_text(self.original, encoding="utf-8")
        names = ["SKILL.md", "references/quality-gates.md", *PREPARE.CANONICAL_ENTRIES.values()]
        for name in names:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("Synthetic resource: " + name + "\n", encoding="utf-8")
        (self.root / "evals").mkdir()
        (self.root / "evals/DO_NOT_LOAD.txt").write_text("NEVER_RUNTIME_EVAL_SENTINEL", encoding="utf-8")

    def test_duplicate_keys_fail_closed(self):
        changes = [
            ('{"router":', '{"router": "wrong.md", "router":'),
            ('{"router":', '{"router": "SKILL.md", "router":'),
            ('"modules":', '"modules": [], "modules":'),
            ('"entry":', '"entry": "other.md", "entry":'),
            ('"activation": "explicit-only"',
             '"activation": "implicit", "activation": "explicit-only"'),
        ]
        for before, after in changes:
            with self.subTest(before=before, after=after):
                self.registry.write_text(self.original.replace(before, after, 1), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "duplicate"):
                    PREPARE.prepare_context("phi-p", root=self.root)

    def test_nonfinite_and_underflow_numbers_fail_closed(self):
        for number in ("NaN", "Infinity", "-Infinity", "1e9999", "1e-9999", "-1e-9999"):
            with self.subTest(number=number):
                self.registry.write_text(self.original[:-1] + ', "extra": ' + number + '}', encoding="utf-8")
                with self.assertRaises(ValueError):
                    PREPARE.prepare_context("p", root=self.root)

    def test_exact_zero_and_representable_subnormal_remain_valid(self):
        for number in ("0e-9999", "-0e9999", "5e-324", "1.25"):
            with self.subTest(number=number):
                self.registry.write_text(self.original[:-1] + ', "extra": ' + number + '}', encoding="utf-8")
                self.assertEqual(PREPARE.prepare_context("p", root=self.root)["status"], "PREPARED_NOT_EXECUTED")

    def test_valid_routes_preserve_hashes_and_evaluation_isolation(self):
        for route in PREPARE.ROUTES:
            with self.subTest(route=route):
                result = PREPARE.prepare_context(route, root=self.root, triz_requested=route == "triz")
                self.assertEqual(result["status"], "PREPARED_NOT_EXECUTED")
                self.assertEqual(result["prepared_modules"], list(PREPARE.ROUTES[route]))
                self.assertNotIn("NEVER_RUNTIME_EVAL_SENTINEL", result["context"])
                self.assertEqual(result["context_sha256"], hashlib.sha256(result["context"].encode()).hexdigest())
                self.assertLessEqual(result["context_bytes"], result["max_bytes"])
                for field in ("total_tokens", "cost", "model_duration_ms", "quality_score"):
                    self.assertIsNone(result[field])
                for item in result["resources"]:
                    self.assertEqual(item["sha256"], hashlib.sha256((self.root / item["path"]).read_bytes()).hexdigest())

    def test_explicit_boolean_consent_remains_required(self):
        for consent in (False, 1, "true", None):
            with self.subTest(consent=consent), self.assertRaisesRegex(ValueError, "explicit"):
                PREPARE.prepare_context("triz", root=self.root, triz_requested=consent)

    def test_invalid_or_insufficient_budgets_fail_closed(self):
        for budget in (0, -1, True, 1, 16, 8388609):
            with self.subTest(budget=budget), self.assertRaises(ValueError):
                PREPARE.prepare_context("p", root=self.root, max_bytes=budget)

    def test_exact_budget_and_fresh_resource_bytes(self):
        first = PREPARE.prepare_context("p", root=self.root)
        exact = PREPARE.prepare_context("p", root=self.root, max_bytes=first["context_bytes"])
        self.assertEqual(first["context_sha256"], exact["context_sha256"])
        with self.assertRaises(ValueError):
            PREPARE.prepare_context("p", root=self.root, max_bytes=first["context_bytes"] - 1)
        (self.root / "first-principles/METHOD.md").write_text("Changed fixture\n", encoding="utf-8")
        self.assertNotEqual(first["context_sha256"], PREPARE.prepare_context("p", root=self.root)["context_sha256"])

    def test_invalid_utf8_is_not_silently_replaced(self):
        (self.root / "first-principles/METHOD.md").write_bytes(b"\xff")
        with self.assertRaises(UnicodeError):
            PREPARE.prepare_context("p", root=self.root)


if __name__ == "__main__":
    unittest.main()
