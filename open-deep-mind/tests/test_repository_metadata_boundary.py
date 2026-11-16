"""Malformed repository metadata must fail validation, not crash or hide fields."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "repository_metadata_boundary", ROOT / "open-deep-mind/scripts/validate_repository.py"
)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class RepositoryMetadataBoundaryTests(unittest.TestCase):
    def validate_metadata(self, relative: str, content: str | bytes) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "VERSION").write_text("1.3.0\n", encoding="utf-8")
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))
            errors, _ = VALIDATOR.validate(root)
        return errors

    def test_metadata_roots_must_be_objects(self) -> None:
        for relative in (
            "open-deep-mind/MODULES.json",
            "open-deep-mind/first-philosophy/module.json",
            "open-deep-mind/first-principles/module.json",
            "open-deep-mind/triz/module.json",
            "open-deep-mind/evals/benchmark-config.json",
        ):
            for value in ([], None, 1, "metadata"):
                with self.subTest(relative=relative, value=value):
                    errors = self.validate_metadata(relative, json.dumps(value))
                    self.assertTrue(any("must be an object" in error and relative in error for error in errors), errors)

    def test_registry_modules_must_be_a_list_of_objects(self) -> None:
        for value in (None, 1, "first-philosophy", {}, [None], [1]):
            with self.subTest(value=value):
                errors = self.validate_metadata("open-deep-mind/MODULES.json", json.dumps({"modules": value}))
                self.assertTrue(any("modules must be an array of objects" in error for error in errors), errors)

    def test_publication_policy_requires_an_object(self) -> None:
        for value in (None, [], 1, "false"):
            with self.subTest(value=value):
                errors = self.validate_metadata(
                    "open-deep-mind/evals/benchmark-config.json", json.dumps({"publication": value})
                )
                self.assertTrue(any("publication must be an object" in error for error in errors), errors)

    def test_context_preparation_flags_require_actual_booleans(self) -> None:
        registry = json.loads((ROOT / "open-deep-mind/MODULES.json").read_text(encoding="utf-8"))
        for field, values in (
            ("triz_requires_explicit_request", (1, 1.0, "true", None)),
            ("model_execution", (0, 0.0, "false", None)),
        ):
            for value in values:
                with self.subTest(field=field, value=value):
                    changed = json.loads(json.dumps(registry))
                    changed["context_preparation"][field] = value
                    errors = self.validate_metadata("open-deep-mind/MODULES.json", json.dumps(changed))
                    self.assertTrue(any("context preparation contract is invalid" in error for error in errors), errors)
        errors = self.validate_metadata("open-deep-mind/MODULES.json", json.dumps(registry))
        self.assertFalse(any("context preparation contract is invalid" in error for error in errors), errors)

    def test_duplicate_keys_in_metadata_cannot_hide_an_earlier_value(self) -> None:
        errors = self.validate_metadata(
            "open-deep-mind/MODULES.json", '{"repository_version":"wrong","repository_version":"1.3.0"}'
        )
        self.assertTrue(any("duplicate JSON key" in error for error in errors), errors)

    def test_unreadable_metadata_encoding_is_a_path_specific_error(self) -> None:
        errors = self.validate_metadata("open-deep-mind/MODULES.json", b"\xff")
        self.assertTrue(any("invalid open-deep-mind/MODULES.json" in error for error in errors), errors)

    def test_unreadable_required_text_is_a_path_specific_error(self) -> None:
        for relative in (
            "VERSION", "README.md", "CITATION.cff", "open-deep-mind/SKILL.md",
            "open-deep-mind/FIRST_PHILOSOPHY.md", "open-deep-mind/FIRST_PRINCIPLES.md",
            "open-deep-mind/TRIZ_ENGINEERING.md", "open-deep-mind/references/domain-routing.md",
        ):
            with self.subTest(relative=relative):
                errors = self.validate_metadata(relative, b"\xff")
                self.assertTrue(any(f"invalid {relative}:" in error for error in errors), errors)

    def test_nonfinite_or_overflowing_json_numbers_are_rejected(self) -> None:
        for token in ("NaN", "Infinity", "-Infinity", "1e309", "1e-999"):
            with self.subTest(token=token):
                errors = self.validate_metadata("arbitrary.json", '{"number":' + token + '}')
                self.assertTrue(any("invalid JSON in arbitrary.json" in error for error in errors), errors)

    def test_exact_zero_exponents_are_valid_json_numbers(self) -> None:
        errors = self.validate_metadata("arbitrary.json", '{"number":0e-999}')
        self.assertFalse(any("invalid JSON in arbitrary.json" in error for error in errors), errors)

    def test_whitespace_link_target_is_reported_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "example.md"
            path.write_text("[broken](   )", encoding="utf-8")
            errors: list[str] = []
            for target in VALIDATOR.local_targets(path.read_text(encoding="utf-8")):
                VALIDATOR.validate_local_target(path, root, target, errors)
            self.assertTrue(any("empty link target" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
