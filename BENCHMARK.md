# OpenDeepMind Behavioral Benchmark

The benchmark framework is now part of the repository under:

[`open-deep-mind/evals/`](open-deep-mind/evals/)

## Current status

```text
Framework: implemented
Authored cases: 60
Train / validation / holdout: 36 / 12 / 12
Comparison configurations: 4
Default repetitions: 3
CI definition validation: enabled
Published behavioral score: NONE YET
```

No score is published until real agent/model runs, raw outputs, grading artifacts, timing/token metadata, model/version information, and aggregate results exist.

## What is compared

```text
no_skill
vs
pinned awesome-skills/first-principles-skill
vs
OpenDeepMind core Φ/P
vs
OpenDeepMind explicit TRIZ (TRIZ-authorized cases only)
```

Pinned external baseline commit:

```text
awesome-skills/first-principles-skill
5623c2fa7c5a6ab47eee0d308431437f52c6ff1e
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

## OpenDeepMind-specific metrics

In addition to assertion quality, time and tokens, the benchmark tracks:

- routing accuracy;
- red-blocker rate;
- TRIZ false-activation rate;
- module-leakage rate;
- rival-model coverage;
- falsifier coverage;
- semantic judge score;
- blind pairwise win rate when pairwise grading is supplied.

## Commands

```bash
python open-deep-mind/evals/scripts/validate_evals.py

python open-deep-mind/evals/scripts/create_workspace.py \
  --iteration 1 --split validation

python open-deep-mind/evals/scripts/aggregate_benchmark.py \
  ../OpenDeepMind_skill-workspace/iteration-1
```

Detailed methodology, schemas, publication rules and rubric:

- [`open-deep-mind/evals/README.md`](open-deep-mind/evals/README.md)
- [`open-deep-mind/evals/evals.json`](open-deep-mind/evals/evals.json)
- [`open-deep-mind/evals/benchmark-config.json`](open-deep-mind/evals/benchmark-config.json)
- [`open-deep-mind/evals/rubric.md`](open-deep-mind/evals/rubric.md)

The evaluation pattern follows the Agent Skills official evaluation guidance: realistic prompts, with/without-skill or version baselines, grading artifacts, timing/token capture, aggregation, and human/blind review where needed.

Reference: <https://agentskills.io/skill-creation/evaluating-skills>
