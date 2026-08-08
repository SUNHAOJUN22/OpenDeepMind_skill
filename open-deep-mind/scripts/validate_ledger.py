#!/usr/bin/env python3
"""Validate an OpenDeepMind proposition ledger JSON file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

TYPES = {"D", "O", "L", "C", "A", "E", "V", "U"}
STATUSES = {"verified", "supported", "plausible", "contested", "unknown"}
RULES = {
    "deduction",
    "induction",
    "abduction",
    "analogy",
    "simulation",
    "optimization",
    "normative",
}
ID_RE = re.compile(r"^[A-Z][A-Z0-9_-]*$")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for key in ("analysis_id", "question", "domain", "scale", "purpose", "claims"):
        require(key in data, f"missing top-level field: {key}", errors)

    claims = data.get("claims", [])
    require(isinstance(claims, list) and len(claims) > 0, "claims must be a non-empty list", errors)

    ids: set[str] = set()
    if isinstance(claims, list):
        for index, claim in enumerate(claims):
            prefix = f"claims[{index}]"
            require(isinstance(claim, dict), f"{prefix} must be an object", errors)
            if not isinstance(claim, dict):
                continue
            for key in ("id", "type", "claim", "status", "scope", "falsifier"):
                require(key in claim, f"{prefix} missing field: {key}", errors)
            cid = claim.get("id")
            ctype = claim.get("type")
            status = claim.get("status")
            if isinstance(cid, str):
                require(bool(ID_RE.fullmatch(cid)), f"{prefix}.id is invalid: {cid}", errors)
                require(cid not in ids, f"duplicate claim id: {cid}", errors)
                ids.add(cid)
            else:
                errors.append(f"{prefix}.id must be a string")
            require(ctype in TYPES, f"{prefix}.type must be one of {sorted(TYPES)}", errors)
            if isinstance(cid, str) and ctype in TYPES:
                require(cid.startswith(ctype), f"{prefix}.id should start with its type {ctype}", errors)
            require(status in STATUSES, f"{prefix}.status must be one of {sorted(STATUSES)}", errors)
            confidence = claim.get("confidence")
            if confidence is not None:
                require(
                    isinstance(confidence, (int, float)) and 0 <= confidence <= 1,
                    f"{prefix}.confidence must be between 0 and 1",
                    errors,
                )
            deps = claim.get("dependencies", [])
            require(isinstance(deps, list), f"{prefix}.dependencies must be a list", errors)

    if isinstance(claims, list):
        for index, claim in enumerate(claims):
            if not isinstance(claim, dict):
                continue
            for dep in claim.get("dependencies", []):
                require(dep in ids, f"claims[{index}] has unknown dependency: {dep}", errors)

    inference_ids: set[str] = set()
    inferences = data.get("inferences", [])
    require(isinstance(inferences, list), "inferences must be a list", errors)
    if isinstance(inferences, list):
        for index, inference in enumerate(inferences):
            prefix = f"inferences[{index}]"
            require(isinstance(inference, dict), f"{prefix} must be an object", errors)
            if not isinstance(inference, dict):
                continue
            for key in ("id", "premises", "rule", "conclusion"):
                require(key in inference, f"{prefix} missing field: {key}", errors)
            iid = inference.get("id")
            if isinstance(iid, str):
                require(iid not in inference_ids, f"duplicate inference id: {iid}", errors)
                inference_ids.add(iid)
            else:
                errors.append(f"{prefix}.id must be a string")
            premises = inference.get("premises", [])
            require(isinstance(premises, list), f"{prefix}.premises must be a list", errors)
            if isinstance(premises, list):
                for premise in premises:
                    require(
                        premise in ids or premise in inference_ids,
                        f"{prefix} has unknown premise: {premise}",
                        errors,
                    )
            require(inference.get("rule") in RULES, f"{prefix}.rule is invalid", errors)
            confidence = inference.get("confidence")
            if confidence is not None:
                require(
                    isinstance(confidence, (int, float)) and 0 <= confidence <= 1,
                    f"{prefix}.confidence must be between 0 and 1",
                    errors,
                )

    decision = data.get("decision")
    if decision is not None:
        require(isinstance(decision, dict), "decision must be an object", errors)
        if isinstance(decision, dict):
            require(
                isinstance(decision.get("recommendation"), str)
                and bool(decision["recommendation"].strip()),
                "decision.recommendation must be non-empty",
                errors,
            )
            trace = decision.get("foundation_trace", [])
            require(isinstance(trace, list), "decision.foundation_trace must be a list", errors)
            if isinstance(trace, list):
                known = ids | inference_ids
                for item in trace:
                    require(item in known, f"decision trace references unknown id: {item}", errors)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger", help="path to ledger JSON")
    args = parser.parse_args()

    path = Path(args.ledger)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1

    if not isinstance(data, dict):
        print(json.dumps({"ok": False, "error": "top-level JSON must be an object"}))
        return 1

    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(json.dumps({"ok": False, "errors": errors}, ensure_ascii=False))
        return 1

    print(
        json.dumps(
            {
                "ok": True,
                "analysis_id": data.get("analysis_id"),
                "claims": len(data.get("claims", [])),
                "inferences": len(data.get("inferences", [])),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
