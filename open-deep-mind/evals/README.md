# OpenDeepMind Benchmark / Evals

This directory is the **behavioral evaluation layer** for OpenDeepMind. It evaluates the three reasoning modules; it is **not a fourth reasoning module** and is never loaded as a problem-solving method.

The layout follows the Agent Skills evaluation pattern: author realistic cases in `evals/evals.json`, run each case under comparable configurations, record grading/timing, aggregate results, inspect failures, revise the skill, and repeat.

Primary reference: <https://agentskills.io/skill-creation/evaluating-skills>

## 1. What this benchmark tests

OpenDeepMind is not a trivia skill. The benchmark therefore measures behavior rather than recall:

| Dimension | Question |
|---|---|
| Routing | Did the agent select Φ, P, Φ→P, or explicit TRIZ correctly? |
| Foundation quality | Did it expose semantic, ontological, epistemic, logical, boundary and value defects? |
| First-principles quality | Did it test requirements, type claims, decompose, model, reconstruct alternatives and falsify? |
| TRIZ quality | When explicitly requested, did it select an appropriate TRIZ problem model and return concepts to engineering validation? |
| TRIZ false activation | Did TRIZ appear where it was not explicitly authorized? |
| Module leakage | Did a module silently import another module's method body or authority? |
| Evidence discipline | Were observations, assumptions, closures, laws, values and unknowns kept distinct? |
| Rival/falsifier coverage | Was at least one serious competing model or falsifier supplied where material? |
| Efficiency | What quality improvement was purchased with additional tokens and time? |

## 2. Initial benchmark set

`evals.json` contains **60 realistic cases**:

```text
12 routing / activation
10 First Philosophy
12 First Principles
 8 Dual Engine Φ→P
10 explicit TRIZ
 8 TRIZ anti-trigger / near-miss
-------------------------------
60 total
```

Split policy:

```text
train      36
validation 12
holdout    12
```

Train cases may guide revisions. Validation cases measure generalization during development. Holdout cases should be inspected only for release evaluation; do not patch the Skill around individual holdout prompts.

## 3. Configurations

The initial comparison matrix is defined in `benchmark-config.json`:

1. `no_skill` — same prompt, no Skill;
2. `first_principles_baseline` — pinned external lightweight first-principles Skill;
3. `opendeepmind_core` — OpenDeepMind with normal Φ/P routing and TRIZ disabled unless the prompt explicitly authorizes it;
4. `opendeepmind_explicit_triz` — OpenDeepMind on explicit TRIZ cases.

Use the same model, model version, temperature/reasoning settings, tool access, input files and repetition count across comparable configurations.

## 4. Repetitions

Default:

```text
repetitions = 3
```

A single successful response is not evidence of reliability. Multiple repetitions expose stochastic/flaky behavior and allow standard-deviation estimates.

## 5. Run artifact contract

A benchmark harness should write one `run_record.json` for each case/configuration/repetition:

```json
{
  "case_id": "R01",
  "configuration": "opendeepmind_core",
  "repetition": 1,
  "model": "model-name",
  "model_version": "provider-version-or-snapshot",
  "route": "phi",
  "loaded_modules": ["first-philosophy"],
  "response_text": "...",
  "total_tokens": 4200,
  "duration_ms": 18000
}
```

A grader then writes `grading.json` conforming to `grading.schema.json`.

## 6. Grading layers

### Layer A — deterministic

Use code for mechanically verifiable facts:

- case/config/repetition metadata;
- expected route for OpenDeepMind runs;
- explicit-only TRIZ policy;
- module-load leakage;
- required output artifact existence;
- valid JSON where a structured artifact is required.

### Layer B — rubric/model judge

Use `rubric.md` for semantic quality:

- foundation audit quality;
- typed-claim discipline;
- causal/mechanistic adequacy;
- decomposition/model quality;
- rival model;
- falsifiability;
- uncertainty;
- actionability.

Every PASS or high score requires concrete evidence from the response.

### Layer C — blind pairwise review

For comparisons such as `opendeepmind_core` vs `no_skill` or vs the pinned first-principles baseline, remove configuration labels and ask the judge/human reviewer which output is stronger and why.

## 7. Red blockers

Any of the following can force a case failure regardless of average rubric score:

- fabricated source/data/experiment;
- unsupported load-bearing factual claim presented as verified;
- correlation promoted to intervention causality without identification;
- model output presented as observation;
- unbridged scale jump;
- hidden value/objective controlling the recommendation;
- TRIZ auto-activation without explicit authorization;
- TRIZ principle/matrix/SIS treated as proof of engineering feasibility;
- no serious rival/falsifier where the case explicitly requires one;
- unsafe removal of a verified legal/safety/ethical constraint.

## 8. Key metrics

The aggregator reports at least:

```text
assertion_pass_rate
red_blocker_rate
routing_accuracy
triz_false_activation_rate
module_leakage_rate
judge_score
blind_pairwise_win_rate (when supplied)
rival_model_coverage
falsifier_coverage
mean_tokens
mean_duration_ms
```

Do not publish benchmark scores until actual runs and grading artifacts exist.

## 9. Commands

Validate the authored benchmark:

```bash
python open-deep-mind/evals/scripts/validate_evals.py
```

Create an empty iteration workspace:

```bash
python open-deep-mind/evals/scripts/create_workspace.py \
  --iteration 1 --split validation
```

Aggregate completed run artifacts:

```bash
python open-deep-mind/evals/scripts/aggregate_benchmark.py \
  ../OpenDeepMind_skill-workspace/iteration-1
```

The scripts are dependency-free and do not call any model API. The actual model/agent harness is intentionally external so the benchmark can run across Codex, Claude Code, Cursor, other Agent-Skills-compatible runtimes, or a custom provider without changing the benchmark definitions.

## 10. Publication rule

A public benchmark result must record:

```text
repository commit
benchmark version
model/provider/version
configuration
repetitions
sampling/reasoning settings
tool access
run date
raw grading artifacts
aggregated benchmark.json
human/model-judge rubric and identity when applicable
```

Do not claim that a benchmark result proves universal superiority. It establishes performance only on the disclosed task distribution, models, settings and graders.
