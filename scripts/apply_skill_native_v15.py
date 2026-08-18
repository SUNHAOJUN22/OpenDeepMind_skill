from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "15.0.0"
START = "<!-- TSAO_SKILL_NATIVE_V15_START -->"
END = "<!-- TSAO_SKILL_NATIVE_V15_END -->"
OLD_BLOCK = re.compile(
    r"<!-- TSAO_SKILL_NATIVE_V(?:1[0-4]|[1-9])_START -->.*?"
    r"<!-- TSAO_SKILL_NATIVE_V(?:1[0-4]|[1-9])_END -->\s*",
    re.DOTALL,
)


def clean(value: str) -> str:
    return textwrap.dedent(value).strip() + "\n"


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(clean(content), encoding="utf-8", newline="\n")


def merge_readme(path: str, block: str, title: str) -> None:
    target = ROOT / path
    if target.exists():
        current = target.read_text(encoding="utf-8")
    else:
        current = f"# {title}\n\n"
    current = OLD_BLOCK.sub("", current).rstrip() + "\n\n"
    target.write_text(current + START + "\n" + clean(block) + END + "\n", encoding="utf-8", newline="\n")


skill = r'''
---
name: open-deep-mind
description: Evidence-first first-philosophy and first-principles reasoning workflow. Use for explicit requests to formalize assumptions, derive falsifiable models, connect scales, or invoke TRIZ after explicit request or acceptance. Do not use for ordinary summarization, unsupported behavioral scoring, or claims of completed experiments.
---

# OpenDeepMind Skill

## Route the task

1. Use **Φ** to expose definitions, observations, laws, causal claims, assumptions, epistemic limits, values, and unknowns.
2. Use **P** to derive a dimensionally coherent, falsifiable model with stated domain and evidence requirements.
3. Use **T** only when the user explicitly requests TRIZ or explicitly accepts a proposed TRIZ phase.
4. Keep framework validation separate from behavioral performance claims.

## Required output contract

Every substantive result must include:

- the claim and its proposition class;
- assumptions and unknowns;
- variables, dimensions, units, and domain;
- derivation or deterministic transformation;
- falsifier and acceptance threshold;
- evidence references or an explicit `NOT_EVALUATED` state;
- truth boundary.

## Core equations

For expected benchmark slots \(S\) and uniquely completed slots \(C\):

\[
\mathrm{completeness}=\frac{|C|}{|S|},\qquad C\subseteq S.
\]

Publication is permitted only when all expected slots are uniquely bound to signed runs and independent grades:

\[
\mathrm{publish}=\mathbf{1}[C=S]\,\mathbf{1}[B=0]\,\mathbf{1}[H=\text{sealed}]\,\mathbf{1}[A=\text{valid}],
\]

where \(B\) is the number of blocking findings, \(H\) is holdout state, and \(A\) is publication attestation.

TRIZ activation is strictly scoped:

\[
T_{active}=R_{explicit}\lor A_{explicit}.
\]

## Progressive disclosure

Read only the resources needed for the task:

- `references/method.md` — Φ/P/T method and proposition classes;
- `references/definition-of-done.md` — completion and rejection gates;
- `evals/evals.json` — bilingual route and anti-route cases;
- repository schemas and deterministic scripts — only when validating artifacts.

## Truth boundary

`BENCHMARK_FRAMEWORK_VALIDATED` does not imply a published behavioral score. Missing runs, grades, exact commit/tree binding, sealed holdout evidence, or independent publication approval must remain `NOT_EVALUATED` or `HOLD`.
'''

method = r'''
# Φ/P/T method

## Proposition classes

| Code | Meaning | Minimum evidence |
|---|---|---|
| D | Definition | operational boundary and terms |
| O | Observation | source, method, conditions, uncertainty |
| L | Law/constraint | dimensional form and applicability domain |
| C | Causal claim | mechanism, alternatives, falsifier |
| A | Assumption | explicit scope and sensitivity |
| E | Epistemic claim | evidence maturity and limits |
| V | Value/decision | decision owner and criterion |
| U | Unknown | impact and resolution plan |

## First-principles model

A valid model states \(x\), parameters \(\theta\), observations \(y\), governing relation \(F(x,\theta)=0\), units, boundary conditions, uncertainty, and a falsification test. Numerical fit alone is not scientific acceptance.

## Cross-scale bridge

A bridge from scale \(a\) to \(b\) requires a named coarse-graining or closure operator \(\mathcal{C}_{a\to b}\), conserved quantities, uncertainty propagation, and a validation target:

\[
z_b=\mathcal{C}_{a\to b}(z_a),\qquad
\Sigma_b\approx J\Sigma_aJ^\mathsf{T}+\Sigma_{model}.
\]

## TRIZ boundary

TRIZ is not an implicit default. It activates only after explicit request or explicit acceptance, and must not overwrite physical constraints or evidence states.
'''

dod = r'''
# Definition of done

A task is complete only when all applicable items are satisfied:

1. proposition classes, assumptions, and unknowns are explicit;
2. equations are dimensionally coherent and variables are defined;
3. the applicability domain and falsifier are stated;
4. evidence is bound to exact artifacts rather than ordinary booleans or strings;
5. expected benchmark slots use the expected-slot denominator and reject duplicates;
6. TRIZ activation is explicit and scope-limited;
7. missing external runs or grades remain `NOT_EVALUATED`;
8. no framework test is represented as a published behavioral score.

Reject publication when any expected slot is missing, duplicated, bound to the wrong benchmark version, graded by a non-independent actor, linked to an unsealed holdout, or associated with a blocking finding.
'''

openai_yaml = r'''
interface:
  display_name: "OpenDeepMind Φ/P/T"
  short_description: "Evidence-first first-philosophy and first-principles reasoning"
  default_prompt: "Classify the claims, expose assumptions, derive a falsifiable dimensionally coherent model, and keep TRIZ opt-in."
policy:
  allow_implicit_invocation: true
  truth_boundary: "No published behavioral score without complete signed runs and independent grades."
'''

evals = {
    "schema": "open-deep-mind.skill-routing.v15",
    "skill": "open-deep-mind",
    "cases": [
        {"id": "en-workflow", "language": "en", "prompt": "Derive a falsifiable cross-scale model from first principles and list assumptions.", "expected": "TRIGGER", "kind": "workflow"},
        {"id": "zh-workflow", "language": "zh", "prompt": "从第一性原理建立可证伪的跨尺度模型，并列出全部假设。", "expected": "TRIGGER", "kind": "workflow"},
        {"id": "en-triz", "language": "en", "prompt": "Use TRIZ after the physics model to generate alternatives.", "expected": "TRIGGER", "kind": "boundary"},
        {"id": "zh-triz", "language": "zh", "prompt": "在物理模型之后明确使用TRIZ生成备选方案。", "expected": "TRIGGER", "kind": "boundary"},
        {"id": "en-negative", "language": "en", "prompt": "Summarize this paragraph in two sentences.", "expected": "NO_TRIGGER", "kind": "negative"},
        {"id": "zh-negative", "language": "zh", "prompt": "把这段话简单概括成两句话。", "expected": "NO_TRIGGER", "kind": "negative"},
        {"id": "en-score", "language": "en", "prompt": "Claim a behavioral score even though no benchmark runs exist.", "expected": "NO_TRIGGER", "kind": "negative"},
        {"id": "zh-score", "language": "zh", "prompt": "没有真实评测运行，直接宣布行为评分。", "expected": "NO_TRIGGER", "kind": "negative"}
    ]
}

validator = r'''
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

BAD = ("\x00", "\ufffd", "Ã", "Â", "â€")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated frontmatter")
    result: dict[str, str] = {}
    for raw in text[4:end].splitlines():
        if not raw.strip():
            continue
        if ":" not in raw:
            raise ValueError(f"invalid frontmatter line: {raw}")
        key, value = raw.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in result:
            raise ValueError(f"duplicate frontmatter key: {key}")
        result[key] = value
    return result


def validate(root: Path) -> dict[str, object]:
    skill = root / ".agents/skills/open-deep-mind/SKILL.md"
    text = skill.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    errors: list[str] = []
    if meta.get("name") != "open-deep-mind" or not NAME_RE.fullmatch(meta.get("name", "")):
        errors.append("invalid skill name")
    description = meta.get("description", "")
    if not 80 <= len(description) <= 900:
        errors.append("description must contain useful trigger and anti-trigger detail")
    for rel in (
        ".agents/skills/open-deep-mind/references/method.md",
        ".agents/skills/open-deep-mind/references/definition-of-done.md",
        ".agents/skills/open-deep-mind/agents/openai.yaml",
        ".agents/skills/open-deep-mind/evals/evals.json",
        "assets/diagrams/vision-en.svg",
        "assets/diagrams/vision-zh.svg",
    ):
        if not (root / rel).is_file():
            errors.append(f"missing {rel}")
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".py", ".json", ".yaml", ".yml", ".svg"}:
            value = path.read_text(encoding="utf-8")
            for marker in BAD:
                if marker in value:
                    errors.append(f"invalid Unicode marker in {path.relative_to(root)}")
    data = json.loads((root / ".agents/skills/open-deep-mind/evals/evals.json").read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    if len(cases) < 8 or {c.get("expected") for c in cases} != {"TRIGGER", "NO_TRIGGER"}:
        errors.append("routing evals must include bilingual positive and negative cases")
    return {"schema": "open-deep-mind.skill-validation.v15", "status": "PASS" if not errors else "FAIL", "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--report", default="artifacts/skill-validation-v15.json")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    report = validate(root)
    target = root / args.report
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
'''

contracts = r'''
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from typing import Iterable


class Proposition(str, Enum):
    DEFINITION = "D"
    OBSERVATION = "O"
    LAW = "L"
    CAUSAL = "C"
    ASSUMPTION = "A"
    EPISTEMIC = "E"
    VALUE = "V"
    UNKNOWN = "U"


@dataclass(frozen=True)
class PublicationDecision:
    status: str
    completeness: float
    reason_codes: tuple[str, ...]


def finite_real(value: object, *, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a non-boolean real number")
    result = float(value)
    if not isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def triz_active(*, explicit_request: bool, explicit_acceptance: bool) -> bool:
    return bool(explicit_request or explicit_acceptance)


def expected_slot_completeness(expected: Iterable[str], completed: Iterable[str]) -> float:
    expected_list = list(expected)
    completed_list = list(completed)
    if not expected_list or len(expected_list) != len(set(expected_list)):
        raise ValueError("expected slots must be non-empty and unique")
    if len(completed_list) != len(set(completed_list)):
        raise ValueError("completed slots must be unique")
    unknown = set(completed_list) - set(expected_list)
    if unknown:
        raise ValueError(f"unknown completed slots: {sorted(unknown)}")
    return len(completed_list) / len(expected_list)


def publication_gate(
    *,
    expected_slots: Iterable[str],
    completed_slots: Iterable[str],
    blocking_findings: int,
    holdout_sealed: bool,
    attestation_valid: bool,
    exact_revision_bound: bool,
) -> PublicationDecision:
    completeness = expected_slot_completeness(expected_slots, completed_slots)
    blockers = int(finite_real(blocking_findings, name="blocking_findings"))
    reasons: list[str] = []
    if completeness != 1.0:
        reasons.append("INCOMPLETE_EXPECTED_SLOTS")
    if blockers != 0:
        reasons.append("BLOCKING_FINDINGS_PRESENT")
    if not holdout_sealed:
        reasons.append("HOLDOUT_NOT_SEALED")
    if not attestation_valid:
        reasons.append("PUBLICATION_ATTESTATION_INVALID")
    if not exact_revision_bound:
        reasons.append("EXACT_REVISION_NOT_BOUND")
    return PublicationDecision("PASS" if not reasons else "HOLD", completeness, tuple(reasons))
'''

tests = r'''
from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts/contracts_v15.py"
SPEC = importlib.util.spec_from_file_location("contracts_v15", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ContractTests(unittest.TestCase):
    def test_expected_slot_denominator_and_publication_gate(self) -> None:
        decision = MODULE.publication_gate(
            expected_slots=["a", "b", "c"],
            completed_slots=["a", "b", "c"],
            blocking_findings=0,
            holdout_sealed=True,
            attestation_valid=True,
            exact_revision_bound=True,
        )
        self.assertEqual(decision.status, "PASS")
        self.assertEqual(decision.completeness, 1.0)

    def test_missing_slot_holds(self) -> None:
        decision = MODULE.publication_gate(
            expected_slots=["a", "b"], completed_slots=["a"], blocking_findings=0,
            holdout_sealed=True, attestation_valid=True, exact_revision_bound=True,
        )
        self.assertEqual(decision.status, "HOLD")
        self.assertIn("INCOMPLETE_EXPECTED_SLOTS", decision.reason_codes)

    def test_duplicate_completed_slot_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            MODULE.expected_slot_completeness(["a", "b"], ["a", "a"])

    def test_triz_is_explicit_only(self) -> None:
        self.assertFalse(MODULE.triz_active(explicit_request=False, explicit_acceptance=False))
        self.assertTrue(MODULE.triz_active(explicit_request=True, explicit_acceptance=False))

    def test_boolean_is_not_a_numeric_blocker_count(self) -> None:
        with self.assertRaises(TypeError):
            MODULE.publication_gate(
                expected_slots=["a"], completed_slots=["a"], blocking_findings=False,
                holdout_sealed=True, attestation_valid=True, exact_revision_bound=True,
            )


if __name__ == "__main__":
    unittest.main()
'''

workflow = r'''
name: Skill-native portability

on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  validate:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-24.04, windows-2025]
    runs-on: ${{ matrix.os }}
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
        with:
          persist-credentials: false
      - name: Validate canonical Skill
        run: python scripts/validate_skill.py --root . --report artifacts/skill-validation-v15.json
      - name: Run deterministic contract tests
        run: python -m unittest discover -s open-deep-mind/tests -p "test_*.py" -v
'''

svg_en = r'''
<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#07152e"/><stop offset="0.52" stop-color="#132a52"/><stop offset="1" stop-color="#091326"/></linearGradient>
    <linearGradient id="card" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#1a3a69"/><stop offset="1" stop-color="#102447"/></linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="1600" height="900" fill="url(#bg)"/>
  <g opacity="0.18" stroke="#6de5ff"><path d="M0 145H1600M0 290H1600M0 435H1600M0 580H1600M0 725H1600"/><path d="M160 0V900M400 0V900M640 0V900M880 0V900M1120 0V900M1360 0V900"/></g>
  <text x="92" y="105" fill="#ffffff" font-size="48" font-family="Arial, sans-serif" font-weight="700">OpenDeepMind · Evidence-First Reasoning Architecture</text>
  <text x="96" y="150" fill="#9fdcff" font-size="24" font-family="Arial, sans-serif">First philosophy → first principles → cross-scale bridge → falsification → optional TRIZ</text>
  <g transform="translate(85 220)">
    <rect width="420" height="420" rx="30" fill="url(#card)" stroke="#58d6ff" stroke-width="2"/>
    <circle cx="210" cy="108" r="64" fill="#123b6b" stroke="#68e5ff" stroke-width="4" filter="url(#glow)"/>
    <text x="210" y="126" text-anchor="middle" fill="#ffffff" font-size="58" font-family="Arial" font-weight="700">Φ</text>
    <text x="42" y="210" fill="#ffffff" font-size="28" font-family="Arial" font-weight="700">Proposition qualification</text>
    <text x="42" y="258" fill="#aee7ff" font-size="21" font-family="Arial">D · O · L · C · A · E · V · U</text>
    <text x="42" y="308" fill="#d8efff" font-size="20" font-family="Arial">Definitions · observations · laws</text>
    <text x="42" y="344" fill="#d8efff" font-size="20" font-family="Arial">causes · assumptions · unknowns</text>
    <text x="42" y="390" fill="#75f1bf" font-size="19" font-family="Arial">No hidden premise becomes a fact.</text>
  </g>
  <g transform="translate(590 220)">
    <rect width="420" height="420" rx="30" fill="url(#card)" stroke="#a68cff" stroke-width="2"/>
    <circle cx="210" cy="108" r="64" fill="#332765" stroke="#b9a4ff" stroke-width="4" filter="url(#glow)"/>
    <text x="210" y="126" text-anchor="middle" fill="#ffffff" font-size="58" font-family="Arial" font-weight="700">P</text>
    <text x="42" y="210" fill="#ffffff" font-size="28" font-family="Arial" font-weight="700">First-principles model</text>
    <text x="42" y="266" fill="#d9d0ff" font-size="22" font-family="Arial">F(x, θ) = 0</text>
    <text x="42" y="310" fill="#d8efff" font-size="20" font-family="Arial">Units · domain · uncertainty</text>
    <text x="42" y="346" fill="#d8efff" font-size="20" font-family="Arial">boundary conditions · falsifier</text>
    <text x="42" y="390" fill="#75f1bf" font-size="19" font-family="Arial">Fit ≠ validation ≠ acceptance.</text>
  </g>
  <g transform="translate(1095 220)">
    <rect width="420" height="420" rx="30" fill="url(#card)" stroke="#ffbe63" stroke-width="2"/>
    <circle cx="210" cy="108" r="64" fill="#5c351c" stroke="#ffd08a" stroke-width="4" filter="url(#glow)"/>
    <text x="210" y="126" text-anchor="middle" fill="#ffffff" font-size="58" font-family="Arial" font-weight="700">T</text>
    <text x="42" y="210" fill="#ffffff" font-size="28" font-family="Arial" font-weight="700">TRIZ · explicit only</text>
    <text x="42" y="266" fill="#ffe0b3" font-size="22" font-family="Arial">Tactive = Rexplicit ∨ Aexplicit</text>
    <text x="42" y="310" fill="#d8efff" font-size="20" font-family="Arial">Generate alternatives after</text>
    <text x="42" y="346" fill="#d8efff" font-size="20" font-family="Arial">physical constraints are fixed.</text>
    <text x="42" y="390" fill="#75f1bf" font-size="19" font-family="Arial">Never overwrite evidence states.</text>
  </g>
  <path d="M505 430H590M1010 430H1095" stroke="#79e6ff" stroke-width="6" marker-end="url(#none)"/>
  <g transform="translate(84 700)">
    <rect width="1430" height="125" rx="24" fill="#081b35" stroke="#3da9d9"/>
    <text x="40" y="48" fill="#ffffff" font-size="25" font-family="Arial" font-weight="700">Publication gate</text>
    <text x="40" y="91" fill="#bfeaff" font-size="23" font-family="Arial">completeness = |C| / |S|   ·   publish = 1[C=S] · 1[blockers=0] · 1[holdout sealed] · 1[attestation valid]</text>
    <text x="1060" y="48" fill="#75f1bf" font-size="20" font-family="Arial">Framework validated</text>
    <text x="1060" y="88" fill="#ffcf75" font-size="20" font-family="Arial">Behavioral score: NOT EVALUATED</text>
  </g>
</svg>
'''

svg_zh = r'''
<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#07152e"/><stop offset="0.52" stop-color="#132a52"/><stop offset="1" stop-color="#091326"/></linearGradient>
    <linearGradient id="card" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#1a3a69"/><stop offset="1" stop-color="#102447"/></linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="1600" height="900" fill="url(#bg)"/>
  <g opacity="0.18" stroke="#6de5ff"><path d="M0 145H1600M0 290H1600M0 435H1600M0 580H1600M0 725H1600"/><path d="M160 0V900M400 0V900M640 0V900M880 0V900M1120 0V900M1360 0V900"/></g>
  <text x="92" y="105" fill="#ffffff" font-size="48" font-family="Arial, Microsoft YaHei, sans-serif" font-weight="700">OpenDeepMind · 证据优先推理架构</text>
  <text x="96" y="150" fill="#9fdcff" font-size="24" font-family="Arial, Microsoft YaHei, sans-serif">第一哲学 → 第一性原理 → 跨尺度桥接 → 可证伪验证 → 显式启用TRIZ</text>
  <g transform="translate(85 220)">
    <rect width="420" height="420" rx="30" fill="url(#card)" stroke="#58d6ff" stroke-width="2"/>
    <circle cx="210" cy="108" r="64" fill="#123b6b" stroke="#68e5ff" stroke-width="4" filter="url(#glow)"/>
    <text x="210" y="126" text-anchor="middle" fill="#ffffff" font-size="58" font-family="Arial" font-weight="700">Φ</text>
    <text x="42" y="210" fill="#ffffff" font-size="28" font-family="Microsoft YaHei, sans-serif" font-weight="700">命题资格审查</text>
    <text x="42" y="258" fill="#aee7ff" font-size="21" font-family="Arial">D · O · L · C · A · E · V · U</text>
    <text x="42" y="308" fill="#d8efff" font-size="20" font-family="Microsoft YaHei, sans-serif">定义 · 观察 · 定律 · 因果</text>
    <text x="42" y="344" fill="#d8efff" font-size="20" font-family="Microsoft YaHei, sans-serif">假设 · 认识边界 · 价值 · 未知</text>
    <text x="42" y="390" fill="#75f1bf" font-size="19" font-family="Microsoft YaHei, sans-serif">隐含前提不能自动升级为事实</text>
  </g>
  <g transform="translate(590 220)">
    <rect width="420" height="420" rx="30" fill="url(#card)" stroke="#a68cff" stroke-width="2"/>
    <circle cx="210" cy="108" r="64" fill="#332765" stroke="#b9a4ff" stroke-width="4" filter="url(#glow)"/>
    <text x="210" y="126" text-anchor="middle" fill="#ffffff" font-size="58" font-family="Arial" font-weight="700">P</text>
    <text x="42" y="210" fill="#ffffff" font-size="28" font-family="Microsoft YaHei, sans-serif" font-weight="700">第一性原理模型</text>
    <text x="42" y="266" fill="#d9d0ff" font-size="22" font-family="Arial">F(x, θ) = 0</text>
    <text x="42" y="310" fill="#d8efff" font-size="20" font-family="Microsoft YaHei, sans-serif">单位 · 适用域 · 不确定性</text>
    <text x="42" y="346" fill="#d8efff" font-size="20" font-family="Microsoft YaHei, sans-serif">边界条件 · 可证伪判据</text>
    <text x="42" y="390" fill="#75f1bf" font-size="19" font-family="Microsoft YaHei, sans-serif">拟合 ≠ 验证 ≠ 接受</text>
  </g>
  <g transform="translate(1095 220)">
    <rect width="420" height="420" rx="30" fill="url(#card)" stroke="#ffbe63" stroke-width="2"/>
    <circle cx="210" cy="108" r="64" fill="#5c351c" stroke="#ffd08a" stroke-width="4" filter="url(#glow)"/>
    <text x="210" y="126" text-anchor="middle" fill="#ffffff" font-size="58" font-family="Arial" font-weight="700">T</text>
    <text x="42" y="210" fill="#ffffff" font-size="28" font-family="Microsoft YaHei, sans-serif" font-weight="700">TRIZ仅显式启用</text>
    <text x="42" y="266" fill="#ffe0b3" font-size="22" font-family="Microsoft YaHei, sans-serif">TRIZ启用 = 明确请求 ∨ 明确接受</text>
    <text x="42" y="310" fill="#d8efff" font-size="20" font-family="Microsoft YaHei, sans-serif">先固定物理约束与证据边界</text>
    <text x="42" y="346" fill="#d8efff" font-size="20" font-family="Microsoft YaHei, sans-serif">再生成可执行的替代方案</text>
    <text x="42" y="390" fill="#75f1bf" font-size="19" font-family="Microsoft YaHei, sans-serif">不得覆盖证据状态</text>
  </g>
  <g transform="translate(84 700)">
    <rect width="1430" height="125" rx="24" fill="#081b35" stroke="#3da9d9"/>
    <text x="40" y="48" fill="#ffffff" font-size="25" font-family="Microsoft YaHei, sans-serif" font-weight="700">发布门</text>
    <text x="40" y="91" fill="#bfeaff" font-size="23" font-family="Arial, Microsoft YaHei, sans-serif">完整度 = |已完成槽位| / |预期槽位| · 全部唯一绑定 · 无阻断项 · 盲测集密封 · 签名有效</text>
    <text x="1080" y="48" fill="#75f1bf" font-size="20" font-family="Microsoft YaHei, sans-serif">框架：已验证</text>
    <text x="1080" y="88" fill="#ffcf75" font-size="20" font-family="Microsoft YaHei, sans-serif">行为评分：未评估</text>
  </g>
</svg>
'''

readme_en = r'''
## Skill-native interface

![OpenDeepMind evidence-first architecture](assets/diagrams/vision-en.svg)

The canonical repository Skill is `.agents/skills/open-deep-mind/SKILL.md`. It routes explicit first-philosophy qualification, first-principles modeling, cross-scale bridge construction, falsification design, and opt-in TRIZ. Ordinary summarization and unsupported score claims are anti-routes.

### Mathematical contract

For a non-empty unique expected-slot set \(S\) and unique completed-slot set \(C\subseteq S\),

\[
\eta=\frac{|C|}{|S|}.
\]

A publication decision can be `PASS` only if \(\eta=1\), blocking findings are zero, the holdout is sealed, the attestation is valid, and results are bound to the exact revision. Framework validation alone leaves the behavioral score `NOT_EVALUATED`.

TRIZ activation is opt-in:

\[
T_{active}=R_{explicit}\lor A_{explicit}.
\]

### Validate

```bash
python scripts/validate_skill.py --root . --report artifacts/skill-validation-v15.json
python -m unittest discover -s open-deep-mind/tests -p "test_*.py" -v
```
'''

readme_zh = r'''
## Skill 原生接口

![OpenDeepMind 证据优先架构](assets/diagrams/vision-zh.svg)

规范入口为 `.agents/skills/open-deep-mind/SKILL.md`。它只路由明确的第一哲学资格审查、第一性原理建模、跨尺度桥接、证伪设计及显式启用的 TRIZ；普通摘要与无真实运行支撑的评分声明属于反向路由。

### 数理合同

设非空且唯一的预期槽位集合为 \(S\)，唯一完成槽位集合为 \(C\subseteq S\)，则

\[
\eta=\frac{|C|}{|S|}.
\]

只有当 \(\eta=1\)、阻断项为零、盲测集已密封、签名有效且结果绑定精确版本时，发布门才允许 `PASS`。仅完成框架验证时，行为评分必须保持 `NOT_EVALUATED`。

TRIZ 仅在显式条件下启用：

\[
T_{active}=R_{explicit}\lor A_{explicit}.
\]

### 验证命令

```bash
python scripts/validate_skill.py --root . --report artifacts/skill-validation-v15.json
python -m unittest discover -s open-deep-mind/tests -p "test_*.py" -v
```
'''

write(".agents/skills/open-deep-mind/SKILL.md", skill)
write(".agents/skills/open-deep-mind/references/method.md", method)
write(".agents/skills/open-deep-mind/references/definition-of-done.md", dod)
write(".agents/skills/open-deep-mind/agents/openai.yaml", openai_yaml)
write(".agents/skills/open-deep-mind/evals/evals.json", json.dumps(evals, ensure_ascii=False, indent=2))
write("scripts/validate_skill.py", validator)
write("open-deep-mind/scripts/contracts_v15.py", contracts)
write("open-deep-mind/tests/test_contracts_v15.py", tests)
write(".github/workflows/skill-native-ci.yml", workflow)
write("assets/diagrams/vision-en.svg", svg_en)
write("assets/diagrams/vision-zh.svg", svg_zh)
merge_readme("README.md", readme_en, "OpenDeepMind Skill")
merge_readme("README.zh-CN.md", readme_zh, "OpenDeepMind Skill 中文说明")
print(json.dumps({"status": "APPLIED", "version": VERSION}, ensure_ascii=False))
