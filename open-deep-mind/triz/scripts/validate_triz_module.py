#!/usr/bin/env python3
"""Validate the OpenDeepMind TRIZ module without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "resources"
EXAMPLES = ROOT / "examples"

REQUIRED = [
    ROOT / "README.md",
    ROOT / "VENDORED_LICENSE.md",
    RES / "39_parameters.md",
    RES / "40_principles.md",
    RES / "contradiction_matrix.json",
    RES / "separation_principles.md",
    RES / "76_standard_solutions.md",
    RES / "ariz_85c.md",
    RES / "evolution_trends.md",
    RES / "modern_problem_identification.md",
    RES / "function_analysis.md",
    RES / "flow_analysis.md",
    RES / "cause_effect_chain.md",
    RES / "trimming.md",
    RES / "feature_transfer.md",
    RES / "s_curve_and_tese.md",
    RES / "effects_and_fos.md",
    RES / "concept_substantiation.md",
    RES / "glossary.md",
    RES / "output_template.md",
    RES / "sources.md",
    EXAMPLES / "brake_disc.md",
    EXAMPLES / "battery_pack.md",
    EXAMPLES / "heat_exchanger_fouling.md",
    EXAMPLES / "anti_example_misframed.md",
    ROOT / "scripts" / "lookup_matrix.py",
]

PARAM_ROW = re.compile(r"^\|\s*(\d+)\s*\|", re.MULTILINE)
PRINCIPLE_ROW = re.compile(r"^\|\s*(\d+)\s*\|", re.MULTILINE)
SIS_ID = re.compile(r"^\*\*(\d+\.\d+\.\d+)\s+—", re.MULTILINE)

ANCHORS = {
    "1,3": [15, 8, 29, 34],
    "1,9": [2, 8, 15, 38],
    "1,14": [28, 27, 18, 40],
    "1,27": [1, 3, 11, 27],
    "14,1": [1, 8, 40, 15],
}


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for path in REQUIRED:
        if not path.is_file():
            fail(errors, f"missing: {path.relative_to(ROOT)}")

    # 39 parameters
    p39 = RES / "39_parameters.md"
    if p39.is_file():
        ids = [int(x) for x in PARAM_ROW.findall(p39.read_text(encoding="utf-8"))]
        ids = [x for x in ids if 1 <= x <= 39]
        if sorted(set(ids)) != list(range(1, 40)):
            fail(errors, f"39_parameters.md does not contain exactly IDs 1..39; got {sorted(set(ids))}")

    # 40 principles
    p40 = RES / "40_principles.md"
    if p40.is_file():
        ids = [int(x) for x in PRINCIPLE_ROW.findall(p40.read_text(encoding="utf-8"))]
        ids = [x for x in ids if 1 <= x <= 40]
        if sorted(set(ids)) != list(range(1, 41)):
            fail(errors, f"40_principles.md does not contain exactly IDs 1..40; got {sorted(set(ids))}")

    # Matrix integrity
    matrix_path = RES / "contradiction_matrix.json"
    if matrix_path.is_file():
        try:
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(errors, f"matrix JSON parse failed: {exc}")
            matrix = {}
        cells = matrix.get("cells", {}) if isinstance(matrix, dict) else {}
        if not isinstance(cells, dict):
            fail(errors, "matrix cells is not a mapping")
            cells = {}
        if len(cells) != 1190:
            fail(errors, f"expected 1190 populated matrix cells, found {len(cells)}")
        for key, values in cells.items():
            try:
                a_s, b_s = key.split(",", 1)
                a, b = int(a_s), int(b_s)
            except Exception:
                fail(errors, f"invalid matrix key: {key!r}")
                continue
            if not (1 <= a <= 39 and 1 <= b <= 39):
                fail(errors, f"matrix key out of range: {key}")
            if a == b:
                fail(errors, f"diagonal matrix cell should not be populated: {key}")
            if not isinstance(values, list) or not 1 <= len(values) <= 4:
                fail(errors, f"matrix cell {key} must contain 1..4 principle IDs")
                continue
            if any(not isinstance(v, int) or not 1 <= v <= 40 for v in values):
                fail(errors, f"matrix cell {key} contains invalid principle ID: {values}")
        for key, expected in ANCHORS.items():
            if cells.get(key) != expected:
                fail(errors, f"matrix anchor mismatch {key}: expected {expected}, got {cells.get(key)}")

    # 76 standard solutions count based on official numbered headings.
    sis_path = RES / "76_standard_solutions.md"
    if sis_path.is_file():
        ids = SIS_ID.findall(sis_path.read_text(encoding="utf-8"))
        if len(ids) != 76:
            fail(errors, f"expected 76 numbered SIS entries, found {len(ids)}")
        if len(set(ids)) != len(ids):
            fail(errors, "duplicate SIS identifiers found")

    # ARIZ architecture
    ariz_path = RES / "ariz_85c.md"
    if ariz_path.is_file():
        text = ariz_path.read_text(encoding="utf-8")
        for part in range(1, 10):
            if f"# Part {part}" not in text:
                fail(errors, f"ARIZ missing Part {part}")

    # Router integrity
    orchestrator = ROOT.parent / "TRIZ_ENGINEERING.md"
    if not orchestrator.is_file():
        fail(errors, "missing ../TRIZ_ENGINEERING.md orchestrator")
    else:
        text = orchestrator.read_text(encoding="utf-8")
        for marker in ("opt-in", "Return to OpenDeepMind", "triz/README.md"):
            if marker not in text:
                fail(errors, f"TRIZ orchestrator missing marker: {marker!r}")

    # Lookup script syntax
    lookup = ROOT / "scripts" / "lookup_matrix.py"
    if lookup.is_file():
        try:
            compile(lookup.read_text(encoding="utf-8"), str(lookup), "exec")
        except SyntaxError as exc:
            fail(errors, f"lookup_matrix.py syntax error: {exc}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(json.dumps({"ok": False, "errors": len(errors), "warnings": len(warnings)}))
        return 1

    print(json.dumps({"ok": True, "errors": 0, "warnings": len(warnings), "matrix_cells": 1190, "sis": 76}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
