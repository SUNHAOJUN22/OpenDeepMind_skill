# Contributing

Contributions are welcome when they improve correctness, portability, auditability, or practical usefulness.

## Contribution types

- correction of a philosophical, scientific, logical, or technical error;
- improved method routing;
- stronger failure-mode diagnostics;
- domain-specific worked examples;
- validator and schema improvements;
- accessible diagrams or translations;
- evidence-backed revisions to quality gates.

## Before opening a change

Describe:

1. the problem;
2. the affected file and rule;
3. the evidence or reproducible example;
4. the proposed change;
5. new failure modes introduced;
6. compatibility impact;
7. validation performed.

A preference alone is not enough to modify a foundational rule.

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

- distinguish real observations from invented scenario inputs;
- label assumptions and values;
- include at least one rival;
- avoid implying universal validity;
- include a falsifier or review trigger;
- avoid confidential or personally identifying data.

## Visual requirements

- Prefer SVG for diagrams.
- Include `<title>` and `<desc>`.
- Maintain readable contrast and text size.
- Do not use copied third-party graphics without clear rights.
- Captions must distinguish conceptual AI art from verified technical diagrams.

## Validation

```bash
python open-deep-mind/scripts/validate_repository.py .
python open-deep-mind/scripts/validate_ledger.py \
  open-deep-mind/assets/example-ledger.json
python -m compileall open-deep-mind/scripts
```

## Licensing

By contributing, you agree that:

- code contributions are licensed under Apache-2.0;
- documentation and visual contributions are licensed under CC BY 4.0;
- you have the right to submit the contribution;
- required third-party attribution is included.
