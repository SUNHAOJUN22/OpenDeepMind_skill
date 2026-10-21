"""Strict proposition, explicit-TRIZ, and benchmark-publication contracts."""

from __future__ import annotations


_PROPOSITION_TYPES = {"D", "O", "L", "C", "A", "E", "V", "U"}


def validate_proposition(record: dict[str, object]) -> str:
    required = {"id", "type", "text", "status", "evidence_refs"}
    if not isinstance(record, dict) or set(record) != required:
        return "INVALID_SCHEMA"
    if not isinstance(record["id"], str) or not record["id"].strip():
        return "INVALID_PROPOSITION"
    if not isinstance(record["type"], str) or record["type"] not in _PROPOSITION_TYPES:
        return "INVALID_PROPOSITION"
    if not isinstance(record["text"], str) or not record["text"].strip():
        return "INVALID_PROPOSITION"
    if not isinstance(record["status"], str) or record["status"] not in {"PROPOSED", "SUPPORTED", "CHALLENGED", "UNKNOWN"}:
        return "INVALID_STATUS"
    if not isinstance(record["evidence_refs"], list) or any(
        not isinstance(ref, str) or not ref.strip() for ref in record["evidence_refs"]
    ):
        return "INVALID_EVIDENCE_REFS"
    return "PASS"


def triz_enabled(
    *,
    explicit_request: bool,
    explicit_acceptance: bool,
    negated: bool = False,
) -> bool:
    flags = (explicit_request, explicit_acceptance, negated)
    if any(type(flag) is not bool for flag in flags):
        raise TypeError("typed Boolean flags are required")
    return not negated and (explicit_request or explicit_acceptance)


def publication_gate(
    expected_slots: set[str],
    runs: list[dict[str, object]],
    grades: list[dict[str, object]],
    *,
    red_blockers: list[str] | None = None,
) -> dict[str, object]:
    if not expected_slots:
        return {"status": "BLOCKED", "reason": "NO_EXPECTED_SLOTS", "completeness": 0.0,
                "publication_ready": False}
    if any(not isinstance(slot, str) or not slot.strip() for slot in expected_slots):
        raise ValueError("expected slots must be non-empty strings")
    for records in (runs, grades):
        if not isinstance(records, list) or any(
            not isinstance(item, dict) or not isinstance(item.get("slot"), str)
            or not item["slot"].strip() or not isinstance(item.get("status"), str)
            for item in records
        ):
            raise ValueError("run and grade records require string slot and status")
    if red_blockers is not None and (not isinstance(red_blockers, list) or any(
        not isinstance(item, str) or not item.strip() for item in red_blockers
    )):
        raise ValueError("red blockers must be non-empty strings")
    run_slots = [item.get("slot") for item in runs if item.get("status") == "COMPLETED"]
    grade_slots = [item.get("slot") for item in grades if item.get("status") == "GRADED"]
    completed = set(run_slots) & set(grade_slots) & expected_slots
    all_runs = [item["slot"] for item in runs]
    all_grades = [item["slot"] for item in grades]
    duplicate_slots = len(all_runs) != len(set(all_runs)) or len(all_grades) != len(set(all_grades))
    orphans = (set(all_runs) | set(all_grades)) - expected_slots
    blockers = red_blockers or []
    ready = completed == expected_slots and not duplicate_slots and not orphans and not blockers
    return {
        "status": "ARTIFACT_SET_COMPLETE" if ready else "BLOCKED",
        "publication_ready": False,
        "completeness": len(completed) / len(expected_slots),
        "missing": sorted(expected_slots - completed),
        "duplicates": duplicate_slots,
        "orphans": sorted(orphans),
        "red_blockers": blockers,
    }
