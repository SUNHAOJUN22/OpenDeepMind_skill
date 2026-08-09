#!/usr/bin/env python3
"""Validate the OpenDeepMind repository without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from pathlib import Path
from xml.etree import ElementTree

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FORBIDDEN = ("NEEDS" + "_CHECK", "PLACEHOLDER" + "_CITATION", "INSERT" + "_SOURCE_HERE")
REQUIRED = (
    "README.md",
    "README.zh-CN.md",
    "LICENSE.md",
    "NOTICE.md",
    "open-deep-mind/SKILL.md",
    "open-deep-mind/FIRST_PHILOSOPHY.md",
    "open-deep-mind/FIRST_PRINCIPLES.md",
    "open-deep-mind/TRIZ_ENGINEERING.md",
    "open-deep-mind/references/method-atlas.md",
    "open-deep-mind/references/domain-routing.md",
    "open-deep-mind/references/quality-gates.md",
    "open-deep-mind/references/failure-modes.md",
    "open-deep-mind/references/intellectual-lineage.md",
    "open-deep-mind/references/glossary.md",
    "open-deep-mind/references/worked-examples.md",
    "open-deep-mind/assets/output-templates.md",
    "open-deep-mind/assets/claim-ledger-template.md",
    "open-deep-mind/assets/claim-ledger.schema.json",
    "open-deep-mind/assets/example-ledger.json",
)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must begin with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter is not closed")
    raw = text[4:end]
    data: dict[str, str] = {}
    current_key: str | None = None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if re.match(r"^\s", line) and current_key:
            data[current_key] = (data[current_key] + " " + line.strip()).strip()
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        current_key = key.strip()
        data[current_key] = value.strip().strip("'\"")
    return data


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as fh:
        header = fh.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("invalid PNG signature")
    return struct.unpack(">II", header[16:24])


def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")

    skill_path = root / "open-deep-mind" / "SKILL.md"
    if skill_path.is_file():
        text = skill_path.read_text(encoding="utf-8")
        try:
            fm = parse_frontmatter(text)
        except ValueError as exc:
            errors.append(str(exc))
            fm = {}
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if not name:
            errors.append("SKILL.md frontmatter missing name")
        elif not NAME_RE.fullmatch(name):
            errors.append(f"invalid skill name: {name!r}")
        elif name != skill_path.parent.name:
            errors.append("skill folder name must match frontmatter name")
        if not desc:
            errors.append("SKILL.md frontmatter missing description")
        elif len(desc) > 1024:
            errors.append(f"description exceeds 1024 characters: {len(desc)}")
        line_count = len(text.splitlines())
        if line_count > 500:
            warnings.append(f"SKILL.md is {line_count} lines; progressive-disclosure target is <=500")
        if "TRIZ is opt-in" not in text:
            errors.append("SKILL.md must state that TRIZ is opt-in")
        if "TRIZ_ENGINEERING.md" not in text:
            errors.append("SKILL.md must route explicit TRIZ requests to TRIZ_ENGINEERING.md")

    triz_path = root / "open-deep-mind" / "TRIZ_ENGINEERING.md"
    if triz_path.is_file():
        triz_text = triz_path.read_text(encoding="utf-8")
        required_triz_markers = (
            "optional, opt-in",
            "Do not load",
            "Engineering contradiction",
            "Physical contradiction",
            "Ideal Final Result",
            "ARIZ-85C",
            "Return to OpenDeepMind",
        )
        for marker in required_triz_markers:
            if marker not in triz_text:
                errors.append(f"TRIZ module missing routing/theory marker: {marker!r}")

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if path.suffix.lower() in {".md", ".py", ".json", ".yml", ".yaml", ".svg"}:
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                errors.append(f"non-UTF-8 text file: {rel}")
                continue
            for token in FORBIDDEN:
                if token in text:
                    errors.append(f"forbidden unresolved token {token!r} in {rel}")
            if path.suffix.lower() == ".md":
                for target in LINK_RE.findall(text):
                    target = target.strip().split()[0].strip("<>")
                    if (
                        not target
                        or target.startswith(("http://", "https://", "mailto:", "#", "data:"))
                    ):
                        continue
                    target_path = target.split("#", 1)[0]
                    if not target_path:
                        continue
                    resolved = (path.parent / target_path).resolve()
                    try:
                        resolved.relative_to(root.resolve())
                    except ValueError:
                        errors.append(f"link escapes repository in {rel}: {target}")
                        continue
                    if not resolved.exists():
                        errors.append(f"broken relative link in {rel}: {target}")
            elif path.suffix.lower() == ".json":
                try:
                    json.loads(text)
                except json.JSONDecodeError as exc:
                    errors.append(f"invalid JSON in {rel}: {exc}")
            elif path.suffix.lower() == ".svg":
                try:
                    ElementTree.fromstring(text)
                except ElementTree.ParseError as exc:
                    errors.append(f"invalid SVG XML in {rel}: {exc}")
            elif path.suffix.lower() == ".py":
                try:
                    compile(text, rel, "exec")
                except SyntaxError as exc:
                    errors.append(f"invalid Python in {rel}: {exc}")

        if path.suffix.lower() == ".png":
            try:
                width, height = png_dimensions(path)
                if width < 1200 or height < 600:
                    warnings.append(f"README PNG may be too small: {rel} ({width}x{height})")
            except ValueError as exc:
                errors.append(f"{rel}: {exc}")

    diagram_dir = root / "open-deep-mind" / "assets" / "diagrams"
    diagram_count = len(list(diagram_dir.glob("*.svg"))) if diagram_dir.exists() else 0
    if diagram_count < 8:
        errors.append(f"expected at least 8 SVG diagrams, found {diagram_count}")

    core_paths = [
        root / "open-deep-mind/FIRST_PHILOSOPHY.md",
        root / "open-deep-mind/FIRST_PRINCIPLES.md",
        root / "open-deep-mind/TRIZ_ENGINEERING.md",
    ]
    resolved = [path.resolve() for path in core_paths]
    if len(set(resolved)) != len(resolved):
        errors.append("First Philosophy, First Principles, and TRIZ must be separate files")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    errors, warnings = validate(root)
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(json.dumps({"ok": False, "errors": len(errors), "warnings": len(warnings)}))
        return 1

    print(json.dumps({"ok": True, "errors": 0, "warnings": len(warnings)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
