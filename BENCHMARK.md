# OpenDeepMind Behavioral Benchmark

The benchmark framework is part of the repository under:

[`open-deep-mind/evals/`](open-deep-mind/evals/)

## Current status

```text
Framework: implemented
Authored cases: 60
Train / validation / holdout: 36 / 12 / 12
Configurations: 4
Default repetitions: 3
CI definition validation: enabled
Published behavioral score: NONE YET
```

No score is published until real agent/model runs, raw outputs, grading artifacts, timing/token metadata, model/version information, repository commit, and aggregate results exist.

## Experimental design

The four configurations are:

```text
1. no_skill
   Same task and tools, no reasoning skill.

2. first_principles_baseline
   Commit-pinned awesome-skills/first-principles-skill.

3. opendeepmind_full
   Production OpenDeepMind behavior on all cases.
   TRIZ remains explicit-only.

4. opendeepmind_no_triz_ablation
   Research ablation on the same 10 explicit-TRIZ cases.
   TRIZ is disabled and the P route is forced.
```

The principal comparisons are therefore:

```text
OpenDeepMind full  vs  no skill
OpenDeepMind full  vs  first-principles baseline
OpenDeepMind full  vs  OpenDeepMind no-TRIZ ablation  [TRIZ-positive cases]
```

The third comparison directly estimates the marginal value of the TRIZ module on tasks that explicitly request TRIZ. The ablation is **not** production behavior and its routing accuracy is intentionally not scored.

Pinned external baseline:

```text
repository: awesome-skills/first-principles-skill
commit: 5623c2fa7c5a6ab47eee0d308431437f52c6ff1e
```

## Initial case distribution

| Category | Cases |
|---|---:|
| Routing / activation | 12 |
| First Philosophy | 10 |
| First Principles | 12 |
| Dual Engine Φ→P | 8 |
| Explicit TRIZ | 10 |
| TRIZ near-miss / anti-trigger | 8 |
| **Total** | **60** |

Split:

```text
train      36
validation 12
holdout    12
```

## Metrics

In addition to assertion quality, time and tokens, the benchmark tracks:

- case pass rate;
- assertion pass rate;
- routing accuracy;
- red-blocker rate;
- TRIZ false-activation rate;
- module-leakage rate;
- rival-model coverage;
- falsifier coverage;
- semantic judge score;
- blind pairwise result when supplied;
- mean tokens;
- mean duration.

The aggregator computes paired common-case deltas for the declared comparisons. It does not compare metrics across different task scopes as though they were directly interchangeable.

Paired deltas and win/tie counts require the same declared model/version and
matching `execution_conditions` (effective sampling/reasoning settings, tool
access, and input-file paths/digests). Missing or mismatched conditions are
listed in `excluded_pairs`; individual run metrics remain available. This is a
metadata comparison, not provider-side execution attestation.

## Commands

Validate the authored benchmark:

```bash
python open-deep-mind/evals/scripts/validate_evals.py
```

Create a reproducible iteration workspace:

```bash
python open-deep-mind/evals/scripts/create_workspace.py \
  --iteration 1 --split validation
```

Creation builds a complete iteration in a unique temporary sibling directory and
publishes it with one same-filesystem rename only after every manifest, case and
instruction file has been written. If a write fails, the temporary stage is
cleaned and the final iteration path remains absent, so the same iteration number
can be retried. Reusing an existing iteration still fails without modifying its
manifest, case definitions, instructions or recorded outputs, even when the
existing directory is empty. Use a new iteration number for another split or
revised configuration; aggregate the existing iteration without running the
creation command again. Concurrent creators of the same iteration cannot both
publish successfully. A hard process termination may leave a temporary sibling
directory; it is not a published iteration and should be inspected before any
manual cleanup.

### Workspace preservation change record

- **Problem / failed assumption:** directory reuse was treated as harmless, but
  creation rewrote metadata around any old outputs and could change the expected
  run denominator without executing a new model run.
- **Evidence / affected component:** temporary-workspace regressions reproduce
  same-split and changed-split overwrites, and two successful competing creators
  in `create_workspace.py`; existing grading and routing definitions are unchanged.
- **Rule / expected improvement:** build in a unique temporary sibling and
  rename the complete tree into place; preserve old evidence and make ordinary
  write failures retryable without publishing partial iterations.
- **Compatibility / new risk:** callers must choose a fresh iteration number;
  a hard process termination can leave an unpublished temporary sibling that
  requires inspection before manual cleanup.
- **Validation:** rerun the original workspace tests plus write-failure,
  preservation and competing-creator regressions, followed by repository and
  evaluation-definition checks. Synthetic fixtures do not establish model
  performance or publication readiness.

After the external agent/model runner has populated every expected run slot with `run_record.json` and `grading.json`:

```bash
python open-deep-mind/evals/scripts/aggregate_benchmark.py \
  ../OpenDeepMind_skill-workspace/iteration-1
```

The workspace manifest enumerates every expected run slot. Missing run slots prevent `publication_ready=true`; a partially populated directory can no longer be mistaken for a complete benchmark.

Detailed methodology, schemas, publication rules and rubric:

- [`open-deep-mind/evals/README.md`](open-deep-mind/evals/README.md)
- [`open-deep-mind/evals/evals.json`](open-deep-mind/evals/evals.json)
- [`open-deep-mind/evals/benchmark-config.json`](open-deep-mind/evals/benchmark-config.json)
- [`open-deep-mind/evals/rubric.md`](open-deep-mind/evals/rubric.md)

The evaluation pattern follows the Agent Skills evaluation guidance: realistic prompts, with/without-skill or version/baseline comparisons, grading artifacts with evidence, token/time capture, aggregation, and blind review where useful.

Reference: <https://agentskills.io/skill-creation/evaluating-skills>
