from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_ledger.py"


class LedgerJsonBoundaryTests(unittest.TestCase):
    def check_rejected(self, content: bytes, expected: str) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "ledger.json"
            path.write_bytes(content)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(path)],
                text=True, capture_output=True, check=False, timeout=10,
            )
        self.assertEqual(result.returncode, 1, result.stdout)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["ok"])
        self.assertRegex(payload.get("error", ""), expected)
        self.assertNotIn("Traceback", result.stderr)

    def check_path_rejected(self, path: Path, expected: str) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(path)],
            text=True, capture_output=True, check=False, timeout=3,
        )
        self.assertEqual(result.returncode, 1, result.stdout)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["ok"])
        self.assertRegex(payload.get("error", ""), expected)
        self.assertNotIn("Traceback", result.stderr)

    def test_duplicate_fields_are_not_silently_overwritten(self) -> None:
        self.check_rejected(b'{"analysis_id":"first","analysis_id":"last"}', "duplicate JSON key")

    def test_nonfinite_extension_fields_are_rejected(self) -> None:
        for token in ("NaN", "Infinity", "-Infinity", "1e999"):
            with self.subTest(token=token):
                self.check_rejected(('{"extra":' + token + '}').encode(), 'nonfinite|finite range')

    def test_invalid_utf8_is_structured_failure(self) -> None:
        self.check_rejected(b'{"analysis_id":"\xff"}', 'decode')

    def test_lone_surrogate_is_structured_failure(self) -> None:
        self.check_rejected(b'{"analysis_id":"\\ud800"}', 'surrogates')

    def test_excessive_depth_is_structured_failure(self) -> None:
        self.check_rejected(b'[' * 2000 + b'0' + b']' * 2000, 'recursion|nesting')

    def test_directory_input_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            self.check_path_rejected(Path(folder), "regular file")

    def test_symbolic_link_input_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            target = root / "target.json"
            target.write_text("{}", encoding="utf-8")
            link = root / "ledger.json"
            try:
                link.symlink_to(target)
            except (OSError, NotImplementedError) as exc:
                self.skipTest(f"symbolic links unavailable: {exc}")
            self.check_path_rejected(link, "regular file|symbolic link|too many levels")

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO support is unavailable")
    def test_fifo_input_is_rejected_without_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            fifo = Path(folder) / "ledger.fifo"
            os.mkfifo(fifo)
            self.check_path_rejected(fifo, "regular file")

    def test_input_budget_is_enforced(self) -> None:
        self.check_rejected(b' ' * (8 * 1024 * 1024 + 1), 'input budget')


if __name__ == "__main__":
    unittest.main()
