# Contributing

Contributions are welcome when they improve correctness, portability, auditability, evidence discipline, or practical usefulness.

## Repository architecture

OpenDeepMind has three isolated modules:

- `open-deep-mind/first-philosophy/`
- `open-deep-mind/first-principles/`
- `open-deep-mind/triz/` — explicit opt-in only

Read [`open-deep-mind/ARCHITECTURE.md`](open-deep-mind/ARCHITECTURE.md) before changing routing or method contracts.

Root compatibility files are not canonical method files. New method content must go to the owning module.

## Contribution types

- correction of philosophical, scientific, logical, or technical errors;
- improved module routing or handoff contracts;
- stronger failure-mode diagnostics;
- schemas, fixtures, validators, or deterministic tools;
- domain-specific worked examples;
- TRIZ data/provenance corrections with source evidence;
- accessible diagrams/translations;
- evidence-backed revisions to quality gates.

## Before opening a change

Describe:

1. the problem;
2. affected module/file/rule;
3. evidence or reproducible example;
4. proposed change;
5. new failure modes introduced;
6. compatibility/migration impact;
7. validation performed.

A preference alone is not enough to modify a foundational rule or canonical historical dataset.

## Module-specific requirements

### First Philosophy

Preserve:

- `Φ8 = Φ0..Φ7`;
- Foundation Charter output;
- explicit semantics/ontology/epistemic/logic/causal/boundary/value audits;
- strict separation from TRIZ.

A change to the Foundation Charter requires updating its schema, fixture, validator, and version/migration note if incompatible.

### First Principles

Preserve:

- `P9 = P1..P9`;
- D/O/L/C/A/E/V/U claim types unless a versioned migration exists;
- explicit model contracts and validity domains;
- rival/falsification/uncertainty requirements;
- no embedded or auto-loaded TRIZ procedure.

A change to model or decision contracts requires schema + fixture + validator updates.

### TRIZ

Preserve:

- `T10 = T1..T10`;
- explicit-only activation;
- progressive loading of resources;
- T → First Principles validation handoff;
- source/provenance and applicable MIT notice for adapted resources.

For matrix/39-parameter/40-principle/76-SIS/ARIZ corrections:

- cite the source edition/reference;
- distinguish historical-source fidelity from modern operational conventions;
- do not silently alter vendored data;
- update `matrix_anomalies.json` or provenance notes when appropriate;
- add/adjust a regression test.

## Method-card format

```markdown
### Method name

**Use when:**
**Do not use when:**

**Procedure**
1.
2.
3.

**Output:**
**Failure risk:**
**Evidence/source:**
```

## Example requirements

Worked examples must:

- distinguish observations from scenario assumptions;
- label assumptions, closures, and values;
- include a serious rival/alternative;
- avoid implying universal validity;
- include a falsifier or review trigger;
- avoid confidential/personally identifying data;
- for TRIZ, distinguish matrix-/SIS-/separation-/ARIZ-derived suggestions from agent inference and current engineering evidence.

## Schema and validator requirements

Any new machine-readable contract must have:

1. a schema or explicit structural specification;
2. a valid example fixture;
3. negative or edge-case coverage where material;
4. validator or test coverage;
5. a documented owner module.

## Visual requirements

- Prefer SVG for diagrams.
- Include `<title>` and `<desc>` where SVG is directly user-facing.
- Maintain readable contrast and text size.
- Do not use copied third-party graphics without clear rights.
- Captions distinguish conceptual art from verified technical diagrams.

## Validation

```bash
python open-deep-mind/scripts/validate_repository.py .
python open-deep-mind/scripts/validate_ledger.py open-deep-mind/assets/example-ledger.json
python open-deep-mind/first-philosophy/scripts/validate_module.py
python open-deep-mind/first-principles/scripts/validate_module.py
python open-deep-mind/triz/scripts/validate_triz_module.py
python open-deep-mind/triz/scripts/lookup_matrix.py --improve 1 --worsen 3 --json
python open-deep-mind/triz/scripts/lookup_standard_solution.py 1.2.1 --json
python -m unittest discover -s open-deep-mind/tests -p "test_*.py"
python -m compileall -q open-deep-mind
```

Also run `git diff --check` in a checkout.

## Licensing

By contributing, you agree that:

- original code contributions are licensed under Apache-2.0 unless explicitly excepted;
- original documentation/visual contributions are licensed under CC BY 4.0 unless explicitly excepted;
- adapted/vendored third-party material remains under its applicable license;
- you have the right to submit the contribution;
- required attribution/provenance is included.

See [`LICENSE.md`](LICENSE.md), [`NOTICE.md`](NOTICE.md), and TRIZ-specific [`open-deep-mind/triz/VENDORED_LICENSE.md`](open-deep-mind/triz/VENDORED_LICENSE.md).
