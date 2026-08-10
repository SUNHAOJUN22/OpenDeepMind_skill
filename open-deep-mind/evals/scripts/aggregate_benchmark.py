#!/usr/bin/env python3
"""Aggregate completed OpenDeepMind benchmark run/grading artifacts."""

from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "benchmark-config.json").read_text(encoding="utf-8"))
EVALS = json.loads((ROOT / "evals.json").read_text(encoding="utf-8"))
CASE_MAP = {c["id"]: c for c in EVALS["evals"]}


def mean(values: list[float]) -> float | None:
    return statistics.fmean(values) if values else None


def rate(values: list[bool]) -> float | None:
    return statistics.fmean(1.0 if x else 0.0 for x in values) if values else None


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("workspace", help="iteration-N directory")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    if not workspace.is_dir():
        parser.error(f"workspace does not exist: {workspace}")

    by_cfg: dict[str, list[tuple[dict[str, Any], dict[str, Any], dict[str, Any]]]] = defaultdict(list)
    incomplete: list[str] = []

    for run_record_path in workspace.rglob("run_record.json"):
        run = read_json(run_record_path)
        grade = read_json(run_record_path.with_name("grading.json"))
        if not run or not grade:
            incomplete.append(str(run_record_path.parent))
            continue
        case = CASE_MAP.get(run.get("case_id"))
        if not case:
            incomplete.append(str(run_record_path.parent))
            continue
        by_cfg[str(run.get("configuration"))].append((case, run, grade))

    configurations: dict[str, dict[str, Any]] = {}
    for cfg, rows in sorted(by_cfg.items()):
        pass_rates: list[float] = []
        blocker_flags: list[bool] = []
        route_flags: list[bool] = []
        false_triz_flags: list[bool] = []
        leakage_flags: list[bool] = []
        judge_scores: list[float] = []
        rival_flags: list[bool] = []
        falsifier_flags: list[bool] = []
        tokens: list[float] = []
        durations: list[float] = []

        for case, run, grade in rows:
            summary = grade.get("summary", {})
            if isinstance(summary.get("pass_rate"), (int, float)):
                pass_rates.append(float(summary["pass_rate"]))
            blockers = grade.get("red_blockers", [])
            blocker_flags.append(bool(blockers))
            rc = grade.get("route_correct")
            if isinstance(rc, bool):
                route_flags.append(rc)
            ft = grade.get("triz_false_activation")
            if isinstance(ft, bool):
                false_triz_flags.append(ft)
            ml = grade.get("module_leakage")
            if isinstance(ml, bool):
                leakage_flags.append(ml)
            js = grade.get("judge_score")
            if isinstance(js, (int, float)):
                judge_scores.append(float(js))
            rp = grade.get("rival_model_present")
            if isinstance(rp, bool):
                rival_flags.append(rp)
            fp = grade.get("falsifier_present")
            if isinstance(fp, bool):
                falsifier_flags.append(fp)
            if isinstance(run.get("total_tokens"), (int, float)):
                tokens.append(float(run["total_tokens"]))
            if isinstance(run.get("duration_ms"), (int, float)):
                durations.append(float(run["duration_ms"]))

        configurations[cfg] = {
            "runs": len(rows),
            "assertion_pass_rate": mean(pass_rates),
            "red_blocker_rate": rate(blocker_flags),
            "routing_accuracy": rate(route_flags),
            "triz_false_activation_rate": rate(false_triz_flags),
            "module_leakage_rate": rate(leakage_flags),
            "judge_score_mean": mean(judge_scores),
            "rival_model_coverage": rate(rival_flags),
            "falsifier_coverage": rate(falsifier_flags),
            "mean_tokens": mean(tokens),
            "mean_duration_ms": mean(durations)
        }

    baseline = configurations.get("no_skill", {})
    deltas: dict[str, dict[str, float | None]] = {}
    for cfg, metrics in configurations.items():
        if cfg == "no_skill" or not baseline:
            continue
        delta: dict[str, float | None] = {}
        for key in ("assertion_pass_rate", "judge_score_mean", "mean_tokens", "mean_duration_ms"):
            a, b = metrics.get(key), baseline.get(key)
            delta[key] = (a - b) if isinstance(a, (int, float)) and isinstance(b, (int, float)) else None
        deltas[cfg] = delta

    result = {
        "benchmark_version": CONFIG["benchmark_version"],
        "generated_from": str(workspace),
        "configurations": configurations,
        "deltas_vs_no_skill": deltas,
        "incomplete_run_directories": sorted(set(incomplete)),
        "publication_ready": bool(configurations) and not incomplete
    }

    output = Path(args.output).resolve() if args.output else workspace / "benchmark.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "ok": True,
        "output": str(output),
        "configurations": list(configurations),
        "complete_runs": sum(v["runs"] for v in configurations.values()),
        "incomplete": len(set(incomplete)),
        "publication_ready": result["publication_ready"]
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
