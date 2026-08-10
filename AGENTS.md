# AGENTS.md

## Repository purpose

OpenDeepMind_skill is one portable Agent Skill with **three isolated reasoning modules**:

1. `open-deep-mind/first-philosophy/` — First Philosophy / foundation qualification.
2. `open-deep-mind/first-principles/` — First Principles / decomposition, modeling, reconstruction, falsification, decision.
3. `open-deep-mind/triz/` — complete TRIZ engineering subsystem, **explicit opt-in only**.

The root `open-deep-mind/SKILL.md` is a thin router. Shared evidence, quality, templates, and ledgers live in `references/`, `assets/`, and `scripts/`.

Architecture contract: `open-deep-mind/ARCHITECTURE.md`  
Machine-readable registry: `open-deep-mind/MODULES.json`  
Canonical version: root `VERSION`

## Required reading order

Before modifying the repository:

1. `open-deep-mind/ARCHITECTURE.md`
2. `open-deep-mind/SKILL.md`
3. the affected module `README.md` and `module.json`
4. the affected module canonical method (`METHOD.md` or `ROUTER.md`)
5. `open-deep-mind/references/quality-gates.md`
6. the directly affected shared reference/resource

For TRIZ changes also read:

- `open-deep-mind/triz/resources/sources.md`
- `open-deep-mind/triz/VENDORED_LICENSE.md`
- `NOTICE.md`

## Module invariants

### First Philosophy

- Canonical method: `open-deep-mind/first-philosophy/METHOD.md`.
- Protocol is exactly **Φ8 = Φ0..Φ7**.
- Must not import, invoke, or route to TRIZ.
- Output contract is the Foundation Charter.
- May hand off only qualified foundations/statuses to First Principles.

### First Principles

- Canonical method: `open-deep-mind/first-principles/METHOD.md`.
- Protocol is exactly **P9 = P1..P9**.
- Must not contain TRIZ method bodies or auto-load TRIZ.
- Must preserve `D/O/L/C/A/E/V/U` proposition types.
- Quantitative models must expose parameters/provenance, equations/relations, boundaries/closures, observation/error model, validity domain, and falsifiers as applicable.

### TRIZ

- Canonical router: `open-deep-mind/triz/ROUTER.md`.
- Protocol is exactly **T10 = T1..T10**.
- Activation is **explicit-only**.
- TRIZ output is concept generation, not validation.
- Every leading concept returns to First Principles validation.
- Vendored/transcribed data must preserve provenance and license.
- Known matrix transcription anomalies must be documented in `matrix_anomalies.json`, not silently erased.

### Compatibility files

The following root files are aliases only and must stay thin:

- `open-deep-mind/FIRST_PHILOSOPHY.md`
- `open-deep-mind/FIRST_PRINCIPLES.md`
- `open-deep-mind/TRIZ_ENGINEERING.md`

Do not put canonical method text back into them.

## Shared invariants

- Keep `open-deep-mind/SKILL.md` below 500 lines and route to canonical module entries.
- Never turn assumptions or empirical closures into laws through wording.
- Preserve red-blocker-first quality gates.
- Preserve domain, scale, purpose, boundary, values, stakeholders, alternatives, falsifiers, and review triggers.
- Cross-scale conclusions require bridge variables/models, information-loss statements, uncertainty, and validation.
- Domain routing must never auto-enable TRIZ.
- Do not add claims of affiliation with Google DeepMind or any referenced organization/vendor.
- Keep core validators free of third-party runtime dependencies.

## Editing rules

- UTF-8 only for text.
- Keep all relative Markdown/HTML links valid.
- Put module-specific method content inside that module, not shared files.
- Shared references must remain method-neutral unless they explicitly route to an optional module.
- New method cards state: use case, non-use case, procedure, output, failure risk, evidence/source.
- New schemas need a valid fixture and validator coverage.
- New module functionality requires manifest + validator + CI coverage.
- New diagrams should be editable SVG where practical, readable, and accessible with `title`/`desc`.
- Do not copy third-party text/data without license and provenance review.

## Validation

Run all of the following before claiming completion:

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

Also inspect:

```bash
git diff --check
```

A file being present is not proof of module completeness; its module validator and repository validator must pass.

## Change protocol

A core-method or architecture change records:

```text
Problem:
Failed assumption/invariant:
Evidence/use case:
Affected module:
Changed rule/API/schema:
Expected improvement:
New failure risk:
Compatibility/migration:
Validation:
```

Update `CHANGELOG.md` and `VERSION` for user-visible architecture/protocol changes.

## Prohibited shortcuts

- Do not mark work complete while a validator fails.
- Do not bypass explicit-only TRIZ activation.
- Do not suppress uncertainty to make examples sound decisive.
- Do not add decorative equations with undefined variables.
- Do not add a scoring dimension without an anchor.
- Do not remove legal, ethical, safety, or provenance warnings as verbosity.
- Do not expand `SKILL.md` into a duplicate of module method files.
- Do not silently “repair” historical/vendored datasets without a documented provenance decision.
