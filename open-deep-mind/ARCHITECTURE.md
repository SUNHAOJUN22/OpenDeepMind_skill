# OpenDeepMind Architecture / 模块架构

## 1. Architectural rule

OpenDeepMind is one Agent Skill with **three isolated reasoning modules** and shared infrastructure:

```text
                 ┌──────────────────────────────┐
                 │        SKILL.md Router       │
                 └──────────────┬───────────────┘
                                │
                 ┌──────────────┼───────────────┐
                 │              │               │ explicit only
                 v              v               v
       ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
       │ First Philosophy│ │ First Principles│ │      TRIZ      │
       │       Φ          │ │       P         │ │       T        │
       └────────┬─────────┘ └───────┬────────┘ └────────┬───────┘
                │ Foundation Charter │                  │ concepts
                └───────────────────>│<─────────────────┘
                                    │ validation
                                    v
                           shared quality gate
```

The modules share common schemas, evidence discipline, quality gates, and output infrastructure, but **do not share method bodies**.

## 2. Canonical module locations

| Module | Canonical entry | Activation | Responsibility |
|---|---|---|---|
| First Philosophy | `first-philosophy/METHOD.md` | core or explicit | qualify definitions, ontology, evidence, logic, causality, boundaries, values, praxis |
| First Principles | `first-principles/METHOD.md` | core or explicit | decompose, classify, model, reconstruct, derive, falsify, decide |
| TRIZ | `triz/ROUTER.md` | explicit only | engineering invention, contradiction resolution, ARIZ, Su-Field, TESE, FOS |

Root files `FIRST_PHILOSOPHY.md`, `FIRST_PRINCIPLES.md`, and `TRIZ_ENGINEERING.md` are compatibility aliases only. New code and documentation must target the canonical module paths.

## 3. Dependency direction

The runtime dependency graph is intentionally asymmetric:

```text
First Philosophy ──Foundation Charter──> First Principles
First Principles ──repair request──────> First Philosophy
First Principles ──explicit opt-in─────> TRIZ
TRIZ ──concept candidates──────────────> First Principles validation
```

A handoff is not an import. Each module must remain usable and auditable without copying another module's method text.

### Forbidden coupling

- First Philosophy must not load or invoke TRIZ.
- First Principles must not auto-load TRIZ.
- TRIZ must not replace First-Principles physical/evidence validation.
- Shared domain routing must not make TRIZ a default creative method.
- A module may read shared `references/` or `assets/`, but module-specific rules belong inside that module.

## 4. Shared contracts

### Proposition ledger

All modules may exchange typed claims using:

```text
D Definition
O Observation
L Law / invariant
C Constraint
A Assumption
E Empirical closure / estimate
V Value
U Unknown
```

Canonical machine-readable schema:

`assets/claim-ledger.schema.json`

### Φ → P contract

First Philosophy outputs a **Foundation Charter**. The machine-readable example/schema live inside `first-philosophy/`.

### P output contract

First Principles outputs a model contract, alternatives, falsifiers, and a decision record. Machine-readable schemas live inside `first-principles/`.

### P → T activation contract

TRIZ activation requires explicit user request or explicit user acceptance after a suggestion. Merely detecting a trade-off or contradiction is insufficient.

### T → P return contract

TRIZ returns candidate concepts with mechanism, resource, contradiction resolved, secondary contradiction, ideality direction, and validation requirement. It does not return a validated engineering conclusion.

## 5. Protocol numbering invariants

- First Philosophy is **Φ8**: `Φ0` through `Φ7` = 8 stages.
- First Principles is **P9**: `P1` through `P9` = 9 stages. Stage `P8` contains both derivation/trace and falsification/stress testing.
- TRIZ is **T10**: `T1` through `T10` = 10 stages.

Validators must fail when these invariants are violated.

## 6. Progressive disclosure

The root `SKILL.md` is the only default activation file. It should stay below the Agent Skills progressive-disclosure target and link directly to the three module entries plus shared references. Detailed knowledge remains in module resources and is loaded only when the selected route needs it.

## 7. Validation layers

```text
repository validator
├── root structure / version / links / frontmatter
├── First Philosophy module validator
├── First Principles module validator
├── TRIZ module validator
├── claim-ledger validator
└── smoke tests / deterministic lookups
```

The CI workflow runs all layers.

## 8. Completeness definition

A module is considered structurally complete when it has:

1. a canonical entry;
2. a machine-readable manifest;
3. explicit activation rules;
4. input/output contracts;
5. stopping/repair conditions;
6. examples or fixtures;
7. a validator;
8. documented dependencies and prohibited dependencies;
9. provenance/license information where third-party material is used;
10. CI coverage.

This is a repository completeness criterion, not a claim that any methodology is philosophically or scientifically exhaustive.
