#!/usr/bin/env python3
"""Create an empty, reproducible OpenDeepMind benchmark iteration workspace."""

from __future__ import annotations

import argparse
import ctypes
import errno
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVALS = ROOT / "evals.json"
CONFIG = ROOT / "benchmark-config.json"


def _rename_directory_no_replace(source: Path, destination: Path) -> None:
    """Atomically publish a directory only if its destination is still absent."""
    source_name = os.fsencode(source)
    destination_name = os.fsencode(destination)
    if sys.platform == "win32":
        # Windows rename semantics fail if any destination already exists.
        os.rename(source, destination)
        return

    libc = ctypes.CDLL(None, use_errno=True)
    if sys.platform.startswith("linux"):
        rename = getattr(libc, "renameat2", None)
        if rename is None:
            raise OSError(errno.ENOTSUP, "atomic no-replace directory rename is unavailable")
        rename.argtypes = [
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        ]
        rename.restype = ctypes.c_int
        result = rename(
            -100, source_name, -100, destination_name, 1
        )  # AT_FDCWD, RENAME_NOREPLACE
    elif sys.platform == "darwin":
        rename = getattr(libc, "renamex_np", None)
        if rename is None:
            raise OSError(errno.ENOTSUP, "atomic no-replace directory rename is unavailable")
        rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
        rename.restype = ctypes.c_int
        result = rename(source_name, destination_name, 0x00000004)  # RENAME_EXCL
    else:
        raise OSError(
            errno.ENOTSUP,
            "atomic no-replace directory rename is unsupported on this platform",
        )

    if result != 0:
        error = ctypes.get_errno()
        if error in (errno.EEXIST, errno.ENOTEMPTY):
            raise FileExistsError(error, os.strerror(error), os.fspath(destination))
        raise OSError(error, os.strerror(error), os.fspath(destination))


def applies_to_case(cfg: dict, case: dict) -> bool:
    categories = cfg.get("case_categories", ["all"])
    return "all" in categories or case.get("category") in categories


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iteration", type=int, required=True)
    parser.add_argument("--split", choices=["train", "validation", "holdout", "all"], default="validation")
    parser.add_argument("--workspace", default="../OpenDeepMind_skill-workspace")
    args = parser.parse_args()

    if args.iteration < 1:
        parser.error("--iteration must be >= 1")

    data = json.loads(EVALS.read_text(encoding="utf-8"))
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    cases = [c for c in data["evals"] if args.split == "all" or c["split"] == args.split]
    configs = config["configurations"]
    repetitions = int(config["repetitions"])

    workspace_root = (ROOT.parent.parent / args.workspace).resolve()
    iteration = workspace_root / f"iteration-{args.iteration}"
    if os.path.lexists(iteration):
        parser.error(
            f"iteration already exists: {iteration}; choose a new --iteration. "
            "Existing artifacts were not modified."
        )

    expected_slots: list[dict] = []
    for case in cases:
        for cfg in configs:
            if not applies_to_case(cfg, case):
                continue
            for rep in range(1, repetitions + 1):
                expected_slots.append({
                    "case_id": case["id"],
                    "configuration": cfg["id"],
                    "repetition": rep,
                })

    created = 0
    try:
        workspace_root.mkdir(parents=True, exist_ok=True)
        # Build a complete iteration off to the side so a write failure cannot leave
        # a partial final directory that blocks a safe retry.
        with tempfile.TemporaryDirectory(
            prefix=f".iteration-{args.iteration}-",
            dir=workspace_root,
        ) as staging_root:
            staged_iteration = Path(staging_root) / iteration.name
            staged_iteration.mkdir()
            manifest = {
                "benchmark_version": config["benchmark_version"],
                "iteration": args.iteration,
                "split": args.split,
                "cases": [c["id"] for c in cases],
                "configurations": [c["id"] for c in configs],
                "repetitions": repetitions,
                "expected_run_slots": expected_slots,
                "status": "workspace-created-no-model-runs-yet"
            }
            (staged_iteration / "manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
            )

            for case in cases:
                case_dir = staged_iteration / f"eval-{case['id']}"
                case_dir.mkdir(exist_ok=True)
                (case_dir / "case.json").write_text(
                    json.dumps(case, ensure_ascii=False, indent=2), encoding="utf-8"
                )
                for cfg in configs:
                    if not applies_to_case(cfg, case):
                        continue
                    for rep in range(1, repetitions + 1):
                        run_dir = case_dir / cfg["id"] / f"run-{rep}"
                        (run_dir / "outputs").mkdir(parents=True, exist_ok=True)
                        instructions = {
                            "case_id": case["id"],
                            "category": case["category"],
                            "split": case["split"],
                            "configuration": cfg["id"],
                            "configuration_kind": cfg.get("kind"),
                            "repetition": rep,
                            "prompt": case["prompt"],
                            "expected_route_for_production": case["expected_route"],
                            "score_routing_accuracy": cfg.get("score_routing_accuracy", True),
                            "skill": cfg.get("skill_path"),
                            "external_repository": cfg.get("repository"),
                            "external_commit": cfg.get("commit"),
                            "disabled_modules": cfg.get("disabled_modules", []),
                            "forced_route": cfg.get("forced_route"),
                            "required_artifacts": ["run_record.json", "grading.json"]
                        }
                        (run_dir / "run_instructions.json").write_text(
                            json.dumps(instructions, ensure_ascii=False, indent=2), encoding="utf-8"
                        )
                        created += 1

            # Recheck immediately before publishing. If another creator won the
            # iteration name, leave its directory untouched and discard our stage.
            if os.path.lexists(iteration):
                raise FileExistsError(f"iteration already exists: {iteration}")
            _rename_directory_no_replace(staged_iteration, iteration)
    except FileExistsError:
        parser.error(
            f"iteration already exists: {iteration}; choose a new --iteration. "
            "Existing artifacts were not modified."
        )
    except OSError as exc:
        parser.error(f"unable to create benchmark workspace: {exc}")

    print(json.dumps({
        "ok": True,
        "workspace": str(iteration),
        "cases": len(cases),
        "run_slots": created,
        "note": "No model/API calls were executed; this command creates the evaluation workspace only."
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
