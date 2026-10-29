#!/usr/bin/env python3
"""Prepare only an explicitly selected method context; never execute a model."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ROUTES = {
    "phi": ("first-philosophy",),
    "p": ("first-principles",),
    "phi-p": ("first-philosophy", "first-principles"),
    "triz": ("triz", "first-principles"),
}
CANONICAL_ENTRIES = {
    "first-philosophy": "first-philosophy/METHOD.md",
    "first-principles": "first-principles/METHOD.md",
    "triz": "triz/ROUTER.md",
}
DEFAULT_MAX_BYTES = 256 * 1024


def read_resource(root: Path, relative: str, limit: int) -> bytes:
    """Read a bounded, regular resource from the installed skill tree."""
    path = root / relative
    if any(part in {"", ".", ".."} for part in relative.split("/")) or Path(relative).is_absolute():
        raise ValueError(f"invalid resource path: {relative}")
    for item in (path, *path.parents):
        if item == root:
            break
        if item.is_symlink():
            raise ValueError(f"symlink resource is not supported: {relative}")
    if not path.resolve().is_relative_to(root):
        raise ValueError(f"resource escapes the skill tree: {relative}")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0)
    with os.fdopen(os.open(path, flags), "rb") as handle:
        metadata = os.fstat(handle.fileno())
        if not stat.S_ISREG(metadata.st_mode):
            raise ValueError(f"resource is not a regular file: {relative}")
        data = handle.read(limit + 1)
    if len(data) > limit:
        raise ValueError(f"resource exceeds the remaining byte budget: {relative}")
    return data


def prepare_context(
    route: str, *, triz_requested: bool = False, max_bytes: int = DEFAULT_MAX_BYTES,
    root: Path = ROOT,
) -> dict[str, Any]:
    """Resolve fresh source bytes; prepared modules are not model execution evidence."""
    if route not in ROUTES:
        raise ValueError(f"unknown route: {route}")
    if route == "triz" and triz_requested is not True:
        raise ValueError("TRIZ requires an explicit user request or acceptance (--triz-requested)")
    if not isinstance(max_bytes, int) or isinstance(max_bytes, bool) or not 1 <= max_bytes <= 8 * 1024 * 1024:
        raise ValueError("max_bytes must be an integer from 1 to 8388608")
    root = root.resolve()
    registry_bytes = read_resource(root, "MODULES.json", 64 * 1024)
    registry = json.loads(registry_bytes)
    if not isinstance(registry, dict):
        raise ValueError("invalid module registry")
    modules = registry.get("modules")
    if not isinstance(modules, list) or any(not isinstance(item, dict) for item in modules):
        raise ValueError("invalid module registry")
    if [item.get("id") for item in modules] != list(CANONICAL_ENTRIES):
        raise ValueError("module registry must contain the three canonical modules in order")
    entries = {item["id"]: item for item in modules}
    for module_id, canonical in CANONICAL_ENTRIES.items():
        if entries[module_id].get("entry") != canonical:
            raise ValueError(f"noncanonical entry for {module_id}")
    if entries["triz"].get("activation") != "explicit-only" or registry.get("router") != "SKILL.md":
        raise ValueError("router or explicit-only TRIZ contract is invalid")

    paths = ["SKILL.md", "references/quality-gates.md"]
    paths.extend(entries[module_id]["entry"] for module_id in ROUTES[route])
    sections: list[str] = []
    resources = []
    source_bytes = 0
    for relative in paths:
        data = read_resource(root, relative, max_bytes - source_bytes)
        source_bytes += len(data)
        sections.append(f"\n<!-- OpenDeepMind source: {relative} -->\n\n{data.decode('utf-8')}\n")
        resources.append({"path": relative, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    context = "".join(sections)
    encoded = context.encode("utf-8")
    if len(encoded) > max_bytes:
        raise ValueError("prepared context including source labels exceeds max_bytes")
    return {
        "schema_version": 1,
        "status": "PREPARED_NOT_EXECUTED",
        "route": route,
        "prepared_modules": list(ROUTES[route]),
        "explicit_triz_request_declared": triz_requested is True,
        "registry_sha256": hashlib.sha256(registry_bytes).hexdigest(),
        "registry_bytes": len(registry_bytes),
        "resources": resources,
        "source_bytes": source_bytes,
        "context_bytes": len(encoded),
        "context_sha256": hashlib.sha256(encoded).hexdigest(),
        "max_bytes": max_bytes,
        "total_tokens": None,
        "cost": None,
        "model_duration_ms": None,
        "quality_score": None,
        "context": context,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--route", choices=tuple(ROUTES), required=True)
    parser.add_argument("--triz-requested", action="store_true", help="Declare an explicit user TRIZ request/acceptance")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    parser.add_argument("--format", choices=("json", "markdown", "manifest"), default="json")
    args = parser.parse_args()
    started = time.perf_counter()
    try:
        result = prepare_context(args.route, triz_requested=args.triz_requested, max_bytes=args.max_bytes)
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        parser.error(str(exc))
    result["preparation_ms"] = (time.perf_counter() - started) * 1000
    if args.format == "markdown":
        sys.stdout.write(result["context"])
    else:
        if args.format == "manifest":
            del result["context"]
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
