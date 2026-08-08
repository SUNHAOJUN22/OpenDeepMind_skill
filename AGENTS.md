# AGENTS.md

## Repository purpose

This repository packages a domain-general Agent Skill that combines:

1. First Philosophy — foundation qualification.
2. First Principles — decomposition, modeling, reconstruction, falsification, and decision.

The skill must remain portable, auditable, and vendor-neutral.

## Required reading order

Before modifying the method:

1. `open-deep-mind/SKILL.md`
2. `open-deep-mind/FIRST_PHILOSOPHY.md`
3. `open-deep-mind/FIRST_PRINCIPLES.md`
4. `open-deep-mind/references/quality-gates.md`
5. the reference file directly affected by the change

## Invariants

- Keep `FIRST_PHILOSOPHY.md` and `FIRST_PRINCIPLES.md` as separate files.
- Keep `open-deep-mind/SKILL.md` concise enough for progressive disclosure; target no more than 500 lines.
- Preserve the proposition types `D/O/L/C/A/E/V/U` unless a versioned migration is supplied.
- Never turn assumptions or empirical closures into laws through wording.
- Preserve the red-blocker-first quality gate.
- Preserve domain, scale, purpose, and boundary declarations.
- Preserve explicit values, stakeholders, falsifiers, alternatives, and review triggers.
- Do not add claims of affiliation with Google DeepMind or any AI vendor.
- Do not copy third-party licensed text without attribution and license review.
- Keep core validation free of third-party runtime dependencies.

## Editing rules

- Use UTF-8.
- Keep relative links valid.
- Use English as the operational language of the Skill; preserve Chinese trigger phrases and the Chinese README.
- Put detailed material in `references/` or `assets/`, not in the activation file.
- A new method card must state: use case, procedure, output, and failure risk.
- A new quality rule must state: defect detected, evidence needed, repair, and compatibility effect.
- A new diagram must be editable SVG when possible, at least 1600 px wide, with accessible `title` and `desc`.
- AI-generated raster images require a caption that they are conceptual unless every textual element is verified.

## Validation

Run before completion:

```bash
python open-deep-mind/scripts/validate_repository.py .
python open-deep-mind/scripts/validate_ledger.py \
  open-deep-mind/assets/example-ledger.json
```

Also inspect:

```bash
git diff --check
python -m compileall open-deep-mind/scripts
```

## Change protocol

A core-method change should record:

```text
Problem:
Failed assumption:
Evidence/use case:
Changed rule:
Expected improvement:
New failure risk:
Compatibility/migration:
Validation:
```

Update `CHANGELOG.md` for user-visible changes.

## Prohibited shortcuts

- Do not mark work complete while a validator fails.
- Do not suppress uncertainty to make examples sound decisive.
- Do not add decorative equations with undefined variables.
- Do not add a scoring dimension without a scoring anchor.
- Do not remove legal, ethical, or safety warnings as “verbosity.”
- Do not generate a large method catalog without routing and stopping rules.
