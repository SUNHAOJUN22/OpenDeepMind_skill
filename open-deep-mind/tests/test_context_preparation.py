"""Runtime routing and file-boundary checks, not model quality measurements."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("context_preparation", ROOT / "scripts/prepare_context.py")
PREP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREP)


class ContextPreparationTests(unittest.TestCase):
    def test_each_route_loads_only_selected_entries_and_shared_contracts(self):
        for route, expected in PREP.ROUTES.items():
            with self.subTest(route=route), patch.object(PREP, "read_resource", wraps=PREP.read_resource) as reader:
                result = PREP.prepare_context(route, triz_requested=route == "triz")
                paths = [call.args[1] for call in reader.call_args_list]
                self.assertEqual(paths, ["MODULES.json", "SKILL.md", "references/quality-gates.md"] + [PREP.CANONICAL_ENTRIES[m] for m in expected])
                self.assertEqual(result["prepared_modules"], list(expected))
                self.assertFalse(any(path.startswith("evals/") for path in paths))
                self.assertEqual(result["status"], "PREPARED_NOT_EXECUTED")
                for field in ("total_tokens", "cost", "model_duration_ms", "quality_score"):
                    self.assertIsNone(result[field])
                data = result["context"].encode("utf-8")
                self.assertEqual(result["context_bytes"], len(data))
                self.assertEqual(result["context_sha256"], hashlib.sha256(data).hexdigest())

    def test_triz_rejected_before_read_without_explicit_request(self):
        for declared in (False, None, "true", 1):
            with self.subTest(declared=declared), patch.object(PREP, "read_resource") as reader:
                with self.assertRaisesRegex(ValueError, "explicit user"):
                    PREP.prepare_context("triz", triz_requested=declared)
                reader.assert_not_called()

    def test_context_budget_includes_source_labels(self):
        normal = PREP.prepare_context("p")
        self.assertGreater(normal["context_bytes"], normal["source_bytes"])
        with self.assertRaisesRegex(ValueError, "source labels"):
            PREP.prepare_context("p", max_bytes=normal["source_bytes"])
        exact = PREP.prepare_context("p", max_bytes=normal["context_bytes"])
        self.assertEqual(exact["context_sha256"], normal["context_sha256"])

    def test_invalid_route_and_budget_fail_before_loading(self):
        for route, budget in (("auto", 1000), ("p", 0), ("p", True), ("p", 8388609)):
            with self.subTest(route=route, budget=budget), patch.object(PREP, "read_resource") as reader:
                with self.assertRaises(ValueError):
                    PREP.prepare_context(route, max_bytes=budget)
                reader.assert_not_called()

    def fixture(self, tmp):
        root = Path(tmp) / "skill"
        for relative in ("MODULES.json", "SKILL.md", "references/quality-gates.md", "first-principles/METHOD.md"):
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        return root

    def test_fresh_context_detects_same_size_same_mtime_content_change(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(tmp)
            first = PREP.prepare_context("p", root=root)
            method = root / "first-principles/METHOD.md"
            before = method.stat()
            method.write_bytes(method.read_bytes().replace(b"Principles", b"PRINCIPLES", 1))
            import os
            os.utime(method, ns=(before.st_atime_ns, before.st_mtime_ns))
            second = PREP.prepare_context("p", root=root)
            self.assertNotEqual(first["context_sha256"], second["context_sha256"])

    def test_symlink_or_noncanonical_entry_cannot_load_an_eval_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(tmp)
            target = root / "first-principles/METHOD.md"
            target.unlink()
            target.symlink_to(ROOT / "evals/README.md")
            with self.assertRaisesRegex(ValueError, "symlink"):
                PREP.prepare_context("p", root=root)
            registry = json.loads((root / "MODULES.json").read_text())
            registry["modules"][1]["entry"] = "evals/README.md"
            (root / "MODULES.json").write_text(json.dumps(registry))
            with self.assertRaisesRegex(ValueError, "noncanonical"):
                PREP.prepare_context("p", root=root)

    def test_missing_required_shared_gate_does_not_publish_partial_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.fixture(tmp)
            (root / "references/quality-gates.md").unlink()
            with self.assertRaises(FileNotFoundError):
                PREP.prepare_context("p", root=root)

    def test_public_cli_outputs_manifest_and_rejects_unauthorized_triz(self):
        script = str(ROOT / "scripts/prepare_context.py")
        result = subprocess.run([sys.executable, script, "--route", "p", "--format", "manifest"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertNotIn("context", data)
        self.assertGreaterEqual(data["preparation_ms"], 0)
        denied = subprocess.run([sys.executable, script, "--route", "triz"], capture_output=True, text=True)
        self.assertEqual(denied.returncode, 2)
        self.assertEqual(denied.stdout, "")
        self.assertIn("explicit user", denied.stderr)


if __name__ == "__main__":
    unittest.main()
