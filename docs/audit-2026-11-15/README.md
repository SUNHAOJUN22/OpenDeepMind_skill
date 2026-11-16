# Code audit — 2026-11-15

## Scope and baseline

Reviewed repository source, metadata validation, context preparation, claim-ledger
validation, benchmark workspace and aggregation boundaries, and the CI entrypoints.
The baseline was `d3db917bad76fc93e1740a63fadbd51af0ed4caa` on `main`.
GitHub branch and open-pull-request inspection found only `main` and no open PRs.
No branch merge or deletion was necessary.

The original full suite passed 173 tests. New malformed-input regressions exposed
validation gaps that the original suite did not exercise.

## Reproduced defects and repairs

1. **Metadata shape errors:** arrays, nulls, scalar roots, malformed module lists,
   and malformed publication objects could cause uncaught exceptions. Metadata
   reads now require objects and validate collection shapes before field access.
2. **Ambiguous JSON:** repeated keys could silently replace earlier fields;
   nonfinite constants, overflowing floating values, and nonzero underflow values
   could be accepted. Strict decoding now reports those inputs with the source
   path. Exact zero and finite representable values remain valid.
3. **Boolean contract aliasing:** numeric `1` and `0` could satisfy the explicit-TRIZ
   and model-execution flags because Python boolean equality accepts those numeric
   aliases. Those flags now require the actual JSON boolean values.
4. **Text and link diagnostics:** non-UTF-8 required text and whitespace-only link
   targets could crash validation. They now produce path-specific diagnostics.

The first eight added regression methods on the baseline produced 10 failed
subtests and 28 exception subtests. The additional required-text test reproduced
8 encoding exceptions before repair. The numeric-boolean probe independently
confirmed that numeric aliases were accepted before repair. All ten new test
methods now pass as part of the full suite.

## Validation

Local environment: Linux, Python 3.12.14. All required repository gates passed;
the full suite now runs **183 tests**. These results exercise deterministic code
and synthetic fixtures, not an external model-performance benchmark. The existing
TRIZ matrix transcription warning for cell 19,9 remains documented; its source
data and anomaly record were preserved.

| Command | Result |
|---|---|
| `python open-deep-mind/scripts/validate_repository.py .` | PASS |
| `python open-deep-mind/scripts/validate_ledger.py open-deep-mind/assets/example-ledger.json` | PASS |
| `python open-deep-mind/first-philosophy/scripts/validate_module.py` | PASS |
| `python open-deep-mind/first-principles/scripts/validate_module.py` | PASS |
| `python open-deep-mind/triz/scripts/validate_triz_module.py` | PASS |
| `python open-deep-mind/evals/scripts/validate_evals.py` | PASS |
| `python open-deep-mind/triz/scripts/lookup_matrix.py --improve 1 --worsen 3 --json` | PASS |
| `python open-deep-mind/triz/scripts/lookup_standard_solution.py 1.2.1 --json` | PASS |
| `python -m unittest discover -s open-deep-mind/tests -p test_*.py` | PASS |
| `python -m compileall -q open-deep-mind` | PASS |
| `git diff --check` | PASS |

A compact raw gate transcript is retained in [validation.txt](validation.txt).
No external model was run, no behavioral score was created, and no benchmark
case, split, rubric, method protocol, or activation rule was changed.

## Compatibility

Valid repository metadata and the three-module architecture are unchanged.
Malformed or ambiguous metadata now fails with explicit diagnostics. This is a
validator repair, not a protocol or architecture release; `VERSION` stays 1.3.0.
