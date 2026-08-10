#!/usr/bin/env python3
"""Lookup a cell in the local 39x39 TRIZ contradiction matrix.

No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "resources" / "contradiction_matrix.json"
PARAMS = ROOT / "resources" / "39_parameters.md"
PRINCIPLES = ROOT / "resources" / "40_principles.md"

ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|", re.MULTILINE)


def parse_numbered_table(path: Path, max_id: int) -> dict[int, str]:
    text = path.read_text(encoding="utf-8")
    out: dict[int, str] = {}
    for n, name in ROW_RE.findall(text):
        i = int(n)
        if 1 <= i <= max_id and i not in out:
            out[i] = name.strip()
    return out


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Lookup TRIZ matrix principles by improving and worsening parameter IDs."
    )
    parser.add_argument("--improve", "-i", type=int, required=True, help="improving parameter ID 1..39")
    parser.add_argument("--worsen", "-w", type=int, required=True, help="worsening parameter ID 1..39")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()

    if not 1 <= args.improve <= 39 or not 1 <= args.worsen <= 39:
        parser.error("parameter IDs must be in 1..39")
    if args.improve == args.worsen:
        parser.error("diagonal cells are not contradiction lookups")

    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    params = parse_numbered_table(PARAMS, 39)
    principles = parse_numbered_table(PRINCIPLES, 40)
    key = f"{args.improve},{args.worsen}"
    ids = data["cells"].get(key, [])

    result = {
        "cell": key,
        "improving_parameter": {
            "id": args.improve,
            "name": params.get(args.improve, "unknown"),
        },
        "worsening_parameter": {
            "id": args.worsen,
            "name": params.get(args.worsen, "unknown"),
        },
        "principles": [
            {"id": pid, "name": principles.get(pid, "unknown")} for pid in ids
        ],
        "source": "matrix" if ids else "empty-cell/direct-principle-fallback",
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(
        f"Cell ({args.improve}, {args.worsen}): "
        f"improve {params.get(args.improve, '?')} -> "
        f"worsen {params.get(args.worsen, '?')}"
    )
    if ids:
        for pid in ids:
            print(f"  #{pid}: {principles.get(pid, 'unknown')}")
        print("Source: matrix-derived")
    else:
        print("  EMPTY CELL")
        print("Fallback: search all 40 principles; label output inferred/direct-principle.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
