#!/usr/bin/env python3
"""Validate the complete OpenDeepMind TRIZ module without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "resources"
EXAMPLES = ROOT / "examples"

RESOURCE_NAMES = [
    "modern_problem_identification.md",
    "innovative_benchmarking.md",
    "function_analysis.md",
    "flow_analysis.md",
    "cause_effect_chain.md",
    "trimming.md",
    "feature_transfer.md",
    "multiscreen_operator.md",
    "ideality_ifr_resources.md",
    "contradictions.md",
    "39_parameters.md",
    "40_principles.md",
    "contradiction_matrix.json",
    "separation_principles.md",
    "substance_field_modeling.md",
    "76_standard_solutions.md",
    "ariz_85c.md",
    "clone_problems.md",
    "effects_and_fos.md",
    "evolution_trends.md",
    "s_curve_and_tese.md",
    "concept_substantiation.md",
    "glossary.md",
    "output_template.md",
    "sources.md",
]

REQUIRED = [
    ROOT / "README.md",
    ROOT / "VENDORED_LICENSE.md",
    *[RES / name for name in RESOURCE_NAMES],
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

EXPECTED_SIS_BY_CLASS = {1: 13, 2: 23, 3: 6, 4: 17, 5: 17}


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    def fail(message: str) -> None:
        errors.append(message)

    for path in REQUIRED:
        if not path.is_file():
            fail(f"missing: {path.relative_to(ROOT)}")

    # No unresolved placeholder tokens in text resources.
    for path in [ROOT / "README.md", *[RES / n for n in RESOURCE_NAMES if n.endswith(".md")]]:
        if path.is_file():
            text = path.read_text(encoding="utf-8")
            for token in ("TODO", "TBD", "PLACEHOLDER_CITATION", "INSERT_SOURCE_HERE"):
                if token in text:
                    fail(f"unresolved token {token!r} in {path.relative_to(ROOT)}")

    # 39 parameters.
    p39 = RES / "39_parameters.md"
    if p39.is_file():
        ids = [int(x) for x in PARAM_ROW.findall(p39.read_text(encoding="utf-8"))]
        ids = sorted(set(x for x in ids if 1 <= x <= 39))
        if ids != list(range(1, 40)):
            fail(f"39_parameters.md must contain IDs 1..39 exactly; got {ids}")

    # 40 principles.
    p40 = RES / "40_principles.md"
    if p40.is_file():
        ids = [int(x) for x in PRINCIPLE_ROW.findall(p40.read_text(encoding="utf-8"))]
        ids = sorted(set(x for x in ids if 1 <= x <= 40))
        if ids != list(range(1, 41)):
            fail(f"40_principles.md must contain IDs 1..40 exactly; got {ids}")

    # Matrix integrity.
    matrix_path = RES / "contradiction_matrix.json"
    if matrix_path.is_file():
        try:
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(f"matrix JSON parse failed: {exc}")
            matrix = {}
        cells = matrix.get("cells", {}) if isinstance(matrix, dict) else {}
        if not isinstance(cells, dict):
            fail("matrix cells is not a mapping")
            cells = {}
        if len(cells) != 1190:
            fail(f"expected 1190 populated matrix cells, found {len(cells)}")
        for key, values in cells.items():
            try:
                a_s, b_s = key.split(",", 1)
                a, b = int(a_s), int(b_s)
            except Exception:
                fail(f"invalid matrix key: {key!r}")
                continue
            if not (1 <= a <= 39 and 1 <= b <= 39):
                fail(f"matrix key out of range: {key}")
            if a == b:
                fail(f"diagonal matrix cell should not be populated: {key}")
            if not isinstance(values, list) or not 1 <= len(values) <= 4:
                fail(f"matrix cell {key} must contain 1..4 principle IDs")
                continue
            if len(values) != len(set(values)):
                warnings.append(f"matrix cell {key} contains duplicate IDs: {values}")
            if any(not isinstance(v, int) or not 1 <= v <= 40 for v in values):
                fail(f"matrix cell {key} contains invalid principle ID: {values}")
        for key, expected in ANCHORS.items():
            if cells.get(key) != expected:
                fail(f"matrix anchor mismatch {key}: expected {expected}, got {cells.get(key)}")

    # 76 SIS exact count and class distribution.
    sis_path = RES / "76_standard_solutions.md"
    if sis_path.is_file():
        ids = SIS_ID.findall(sis_path.read_text(encoding="utf-8"))
        if len(ids) != 76:
            fail(f"expected 76 numbered SIS entries, found {len(ids)}")
        if len(set(ids)) != len(ids):
            fail("duplicate SIS identifiers found")
        counts = {i: 0 for i in range(1, 6)}
        for sis_id in ids:
            counts[int(sis_id.split(".")[0])] += 1
        if counts != EXPECTED_SIS_BY_CLASS:
            fail(f"SIS class distribution mismatch: expected {EXPECTED_SIS_BY_CLASS}, got {counts}")

    # ARIZ must contain all 9 parts.
    ariz_path = RES / "ariz_85c.md"
    if ariz_path.is_file():
        text = ariz_path.read_text(encoding="utf-8")
        for part in range(1, 10):
            if f"# Part {part}" not in text:
                fail(f"ARIZ missing Part {part}")

    # Router integrity and opt-in guarantee.
    orchestrator = ROOT.parent / "TRIZ_ENGINEERING.md"
    if not orchestrator.is_file():
        fail("missing ../TRIZ_ENGINEERING.md orchestrator")
    else:
        text = orchestrator.read_text(encoding="utf-8")
        for marker in ("optional", "Do not load TRIZ automatically", "triz/README.md", "Return to OpenDeepMind"):
            if marker not in text:
                fail(f"TRIZ orchestrator missing marker: {marker!r}")

    # Module map should reference all resources.
    module_readme = ROOT / "README.md"
    if module_readme.is_file():
        text = module_readme.read_text(encoding="utf-8")
        for name in RESOURCE_NAMES:
            if name not in text:
                fail(f"triz/README.md does not list resource: {name}")

    # Python syntax.
    for script in (ROOT / "scripts").glob("*.py"):
        try:
            compile(script.read_text(encoding="utf-8"), str(script), "exec")
        except SyntaxError as exc:
            fail(f"{script.name} syntax error: {exc}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        for warning in warnings:
            print(f"WARNING: {warning}", file=sys.stderr)
        print(json.dumps({"ok": False, "errors": len(errors), "warnings": len(warnings)}))
        return 1

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    print(json.dumps({
        "ok": True,
        "errors": 0,
        "warnings": len(warnings),
        "resources": len(RESOURCE_NAMES),
        "matrix_cells": 1190,
        "sis": 76,
        "ariz_parts": 9,
        "examples": 4,
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
