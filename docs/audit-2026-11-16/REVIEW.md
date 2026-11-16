# Logical review and automated validation — 2026-11-16

## Baseline and assessed paths

This fresh review starts at main commit
`17e7ecc94a0ff387599721639137c5e5de66db4f`. Initial live GitHub inspection found
only `main` and no open pull requests. No branch integration was necessary.

The review inspected the benchmark's experiment-arm assumptions, grading and
aggregation, paired comparison identity, cost/missingness handling, workspace
creation and source preservation, publication contracts, and claim-ledger
dependency validation. The relevant implementation paths were
`aggregate_benchmark.py`, `create_workspace.py`, `contracts_v17.py`,
`scientific_contracts_v16.py`, and `validate_ledger.py`, together with their
schemas, benchmark configuration, rubric, architecture and regression tests.
The prior metadata-parser repair was retained; this review targeted experimental
logic beyond that earlier change.

## Reproduced defect: a contaminated no-skill control was admitted

The benchmark defines `no_skill` as a control with no reasoning skill loaded.
Its generic run schema nevertheless permits canonical module IDs, and the
configuration validator only enforced forced routes and explicit disabled-module
lists. A record could therefore declare `configuration="no_skill"` and
`loaded_modules=["first-principles"]`, yet enter control metrics and paired wins.
This contradicts the declared experiment even when its JSON is structurally valid.

A synthetic, complete 114-slot validation workspace demonstrates the consequence:

| Observation | Baseline | Repaired |
| --- | ---: | ---: |
| Expected run slots | 114 | 114 |
| Admitted complete records | 114 | 113 |
| Admitted no-skill records | 36 | 35 |
| Compatible full-vs-no-skill pairs | 36 | 35 |
| No-skill wins attributable to the contaminated fixture | 1 | 0 |
| Metadata diagnostics | 0 | 1 |
| Artifact set complete | true | false |
| Publication authorized | false | false |

These numbers are a software regression using constructed run/grading records.
They are not observed model-performance results. The same source artifacts were
evaluated by the original baseline implementation and the repaired implementation.

## Repair and compatibility

The configuration validator now rejects a nonempty reported module-load list for
`kind="no-skill-baseline"` before metrics, paired counts or completeness are
computed. Each rejected record receives a path-specific diagnostic. Original
run and grading artifacts remain unchanged; contamination is not repaired by
relabeling the evidence. The other experiment arms retain their original metrics.

A route label alone is not proof of a loaded skill. Valid control records with
an empty load list remain admitted for all six route labels, including observed
routing mistakes. External baselines and valid no-TRIZ ablations retain their
existing contracts. No case, split, repetition count, rubric, module method,
versioned protocol or publication authorization rule was changed.

The benchmark documentation records the changed admission rule and its
compatibility boundary. This is an unreleased framework correctness repair;
the skill version remains 1.3.0.

## Before-and-after tests

Three new test methods exercise one contaminated control, complete contamination
of all 36 control slots, and valid unassisted route behavior. They cover each
canonical module and their union, pair exclusion, unaffected comparison arms,
and source-byte preservation through the public workspace/aggregation CLIs.

- Against the baseline, the 10-test configuration suite produced five failures:
  four single-slot variants and the complete contaminated arm.
- After repair, all 10 configuration tests pass, including all existing controls.
- The complete deterministic suite passes **186 tests**.
- All 11 required command gates pass: repository, ledger, the three module
  validators, evaluation definitions, both deterministic TRIZ lookups, the full
  suite, Python compilation, and whitespace checks.
- An independent read-only review confirmed that the existing schema validation
  precedes the new configuration guard and that route labels are not conflated
  with actual module loads.

Exact commands, exit codes, runtime and the synthetic before/after proof are
recorded in [validation.json](validation.json).

## Limits retained

The guard establishes consistency of declared experimental metadata. It cannot
detect undeclared instructions, authenticate provider execution, certify grader
independence, or make causal claims about real model performance. Publication
remains closed pending independent attestation. No external model was run.

The existing TRIZ matrix transcription anomaly at cell 19,9 remains documented
with its original provenance. This review did not alter vendored knowledge data
or the runtime reasoning protocols.
