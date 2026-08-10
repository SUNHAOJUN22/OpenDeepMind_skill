#!/usr/bin/env python3
"""Validate OpenDeepMind behavioral benchmark definitions without third-party packages."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals.json"
CONFIG = ROOT / "benchmark-config.json"

EXPECTED_CATEGORIES = {
    "routing": 12,
    "first-philosophy": 10,
    "first-principles": 12,
    "dual-engine": 8,
    "triz-positive": 10,
    "triz-negative": 8,
}
EXPECTED_SPLITS = {"train": 36, "validation": 12, "holdout": 12}
EXPECTED_PREFIX = {
    "routing": "R",
    "first-philosophy": "F",
    "first-principles": "P",
    "dual-engine": "D",
    "triz-positive": "T",
    "triz-negative": "N",
}
VALID_ROUTES = {"phi", "p", "phi-p", "triz"}
ID_RE = re.compile(r"^[RFPDTN][0-9]{2}$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        data = json.loads(EVALS.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"ok": False, "error": f"cannot parse evals.json: {exc}"}))
        return 1

    try:
        config = json.loads(CONFIG.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"ok": False, "error": f"cannot parse benchmark-config.json: {exc}"}))
        return 1

    if data.get("skill_name") != "open-deep-mind":
        errors.append("skill_name must be open-deep-mind")
    if data.get("benchmark_version") != config.get("benchmark_version"):
        errors.append("evals benchmark_version != benchmark-config benchmark_version")

    evals = data.get("evals")
    if not isinstance(evals, list):
        errors.append("evals must be a list")
        evals = []
    if len(evals) != 60:
        errors.append(f"expected exactly 60 evals, found {len(evals)}")

    ids: set[str] = set()
    categories: Counter[str] = Counter()
    splits: Counter[str] = Counter()

    for index, case in enumerate(evals):
        prefix = f"evals[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for key in (
            "id", "category", "split", "prompt", "expected_output",
            "expected_route", "triz_allowed", "assertions", "red_blockers"
        ):
            if key not in case:
                errors.append(f"{prefix} missing {key}")
        cid = case.get("id")
        category = case.get("category")
        split = case.get("split")
        route = case.get("expected_route")
        if not isinstance(cid, str) or not ID_RE.fullmatch(cid):
            errors.append(f"{prefix}.id invalid: {cid!r}")
        elif cid in ids:
            errors.append(f"duplicate eval id: {cid}")
        else:
            ids.add(cid)
        if category not in EXPECTED_CATEGORIES:
            errors.append(f"{prefix}.category invalid: {category!r}")
        else:
            categories[category] += 1
            if isinstance(cid, str) and not cid.startswith(EXPECTED_PREFIX[category]):
                errors.append(f"{cid}: ID prefix does not match category {category}")
        if split not in EXPECTED_SPLITS:
            errors.append(f"{prefix}.split invalid: {split!r}")
        else:
            splits[split] += 1
        if route not in VALID_ROUTES:
            errors.append(f"{prefix}.expected_route invalid: {route!r}")
        prompt = case.get("prompt")
        if not isinstance(prompt, str) or len(prompt.strip()) < 20:
            errors.append(f"{prefix}.prompt too short")
        expected = case.get("expected_output")
        if not isinstance(expected, str) or len(expected.strip()) < 20:
            errors.append(f"{prefix}.expected_output too short")
        assertions = case.get("assertions")
        if not isinstance(assertions, list) or len(assertions) < 2 or not all(isinstance(x, str) and len(x) >= 8 for x in assertions):
            errors.append(f"{prefix}.assertions must contain at least two substantive strings")
        blockers = case.get("red_blockers")
        if not isinstance(blockers, list) or len(blockers) < 1 or not all(isinstance(x, str) and len(x) >= 8 for x in blockers):
            errors.append(f"{prefix}.red_blockers must be a non-empty list")
        triz_allowed = case.get("triz_allowed")
        if not isinstance(triz_allowed, bool):
            errors.append(f"{prefix}.triz_allowed must be boolean")
        if category == "triz-positive":
            if route != "triz" or triz_allowed is not True:
                errors.append(f"{cid}: triz-positive must route triz and allow TRIZ")
            p = prompt.lower() if isinstance(prompt, str) else ""
            if not any(token in p for token in ("triz", "ariz", "su-field", "if r", "ifr")) and "物场" not in p:
                warnings.append(f"{cid}: positive TRIZ case may lack an explicit trigger token")
        else:
            if triz_allowed is not False:
                errors.append(f"{cid}: non-positive case must not pre-authorize TRIZ")
            if route == "triz":
                errors.append(f"{cid}: non-positive case must not expect TRIZ route")
        if category == "triz-negative" and route == "triz":
            errors.append(f"{cid}: near-miss case cannot expect TRIZ")

    if dict(categories) != EXPECTED_CATEGORIES:
        errors.append(f"category distribution mismatch: expected {EXPECTED_CATEGORIES}, got {dict(categories)}")
    if dict(splits) != EXPECTED_SPLITS:
        errors.append(f"split distribution mismatch: expected {EXPECTED_SPLITS}, got {dict(splits)}")

    cfgs = config.get("configurations")
    if not isinstance(cfgs, list) or len(cfgs) < 4:
        errors.append("benchmark-config must define at least four configurations")
        cfgs = []
    cfg_ids = [c.get("id") for c in cfgs if isinstance(c, dict)]
    required_cfgs = {
        "no_skill", "first_principles_baseline",
        "opendeepmind_core", "opendeepmind_explicit_triz"
    }
    if not required_cfgs.issubset(set(cfg_ids)):
        errors.append(f"missing benchmark configurations: {sorted(required_cfgs - set(cfg_ids))}")
    for cfg in cfgs:
        if isinstance(cfg, dict) and cfg.get("id") == "first_principles_baseline":
            sha = cfg.get("commit", "")
            if not isinstance(sha, str) or not SHA_RE.fullmatch(sha):
                errors.append("external first-principles baseline must be pinned to a 40-hex commit")
    if config.get("repetitions", 0) < 3:
        errors.append("benchmark repetitions must be at least 3")
    if config.get("publication", {}).get("publish_scores_before_real_runs") is not False:
        errors.append("publication policy must forbid publishing scores before real runs")

    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(json.dumps({"ok": False, "errors": len(errors), "warnings": len(warnings)}))
        return 1

    print(json.dumps({
        "ok": True,
        "errors": 0,
        "warnings": len(warnings),
        "cases": len(evals),
        "categories": dict(categories),
        "splits": dict(splits),
        "configurations": len(cfgs),
        "repetitions": config.get("repetitions"),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
