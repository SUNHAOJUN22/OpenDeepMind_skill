# OpenDeepMind Benchmark / Evals

This directory is the **behavioral evaluation layer** for OpenDeepMind. It evaluates the three reasoning modules; it is **not a fourth reasoning module** and is never loaded as a problem-solving method.

The layout follows the Agent Skills evaluation pattern: author realistic cases in `evals.json`, run each case under comparable configurations, record grading/timing, aggregate results, inspect failures, revise the skill, and repeat.

Primary reference: <https://agentskills.io/skill-creation/evaluating-skills>

## 1. What this benchmark tests

OpenDeepMind is not a trivia skill. The benchmark therefore measures behavior rather than recall:

| Dimension | Question |
|---|---|
| Routing | Did the production agent select Φ, P, Φ→P, or explicit TRIZ correctly? |
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

Train cases may guide revisions. Validation cases measure generalization during development. Holdout cases are for release evaluation; do not patch the Skill around individual holdout prompts.

## 3. Configurations and ablation design

`benchmark-config.json` defines exactly four configurations:

1. **`no_skill`** — same prompt and tool access, no reasoning Skill;
2. **`first_principles_baseline`** — commit-pinned external lightweight first-principles Skill;
3. **`opendeepmind_full`** — production OpenDeepMind on all cases, with TRIZ remaining explicit-only;
4. **`opendeepmind_no_triz_ablation`** — research ablation on the same ten `triz-positive` cases; TRIZ is disabled and the First-Principles route is forced.

The declared comparisons are:

```text
opendeepmind_full  vs  no_skill
opendeepmind_full  vs  first_principles_baseline
opendeepmind_full  vs  opendeepmind_no_triz_ablation  [triz-positive]
```

The final pair directly measures the marginal contribution of the TRIZ module on tasks that explicitly request TRIZ. The no-TRIZ ablation is intentionally not production behavior, so routing accuracy is not scored for that ablation.

Use the same model, model version, sampling/reasoning settings, tool access, input files and repetition count across each comparable pair.

## 4. Repetitions

Default:

```text
repetitions = 3
```

A single successful response is not evidence of reliability. Multiple repetitions expose stochastic/flaky behavior and support paired comparisons.

## 5. Workspace and run artifact contract

Create the workspace with `create_workspace.py`. Its `manifest.json` enumerates **every expected run slot**; the aggregator uses that manifest as the source of truth, so a missing run directory cannot silently disappear from the denominator.

Each `(case_id, configuration, repetition)` identity contributes at most once.
Duplicate manifest entries are metadata errors, do not reweight metrics, and
prevent `artifact_set_complete`. Unknown cases/configurations and non-positive
or Boolean repetition indices are rejected before artifact lookup. Distinct
valid repetitions remain distinct observations; deduplication is not evidence
that external runs were statistically independent. Routing accuracy is omitted
for configurations whose `score_routing_accuracy` is false (the forced-route
TRIZ ablation), without changing their other metrics or publication gate.

每个“案例—配置—重复编号”最多计入一次；重复条目使产物完整性检查失败，
不能用于提高分数或充当新增试验。强制路由的消融配置不计生产路由准确率，
但仍计算其余指标。计数一致性不证明外部模型执行或统计独立性。

A benchmark harness writes one `run_record.json` for each expected case/configuration/repetition:

```json
{
  "case_id": "R01",
  "configuration": "opendeepmind_full",
  "repetition": 1,
  "model": "model-name",
  "model_version": "provider-version-or-snapshot",
  "execution_conditions": {
    "sampling_settings": {"temperature": 0.2, "top_p": 1.0},
    "reasoning_settings": {"effort": "medium"},
    "tool_access": {"python": {"definition_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"}},
    "input_files": [{"path": "dataset.csv", "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}]
  },
  "route": "phi",
  "loaded_modules": ["first-philosophy"],
  "response_text": "...",
  "total_tokens": 4200,
  "duration_ms": 18000,
  "repository_commit": "..."
}
```

A grader then writes `grading.json` conforming to `grading.schema.json`.
Each `assertion_results[].text` must reproduce one official assertion from the
case in `evals.json` (outer whitespace is ignored), and every official assertion
must appear exactly once. Deleting a failed criterion, replacing it with an
easier one, or adding criteria to reweight the score is rejected even when the
self-reported summary is numerically consistent. `loaded_modules` accepts only
unique canonical IDs: `first-philosophy`, `first-principles`, and `triz`.
For `route="triz"`, both `triz` and `first-principles` must be listed: TRIZ
generates candidate concepts, which the repository contract requires to return
to First Principles for engineering validation. A missing module is a
path-specific metadata error, excludes the run from metrics, and blocks
`artifact_set_complete`.

`route="triz"` 时必须同时列出 `triz` 和 `first-principles`：仓库约定要求将 TRIZ 生成的候选概念交回第一性原理进行工程验证。缺少模块属于路径级元数据错误，该运行不计入指标，并会阻止 `artifact_set_complete` 为真。

评分记录必须完整覆盖 `evals.json` 对应案例的官方断言，每条恰好一次；不能删减、
替换或增添评分项。模块标识必须使用上述规范名称，不能用大写或路径别名绕过检查。

The aggregator also checks each run against its configuration before admitting it
to individual metrics or paired comparisons. `forced_route` specifies the selected
method: a no-TRIZ ablation must record `route="p"`, including when production
routing accuracy is intentionally not scored. A module in `disabled_modules`
must appear in neither `loaded_modules` nor the selected route. Contradictory
records produce path-specific `metadata_errors`, do not count toward
`complete_runs`, and block `artifact_set_complete`; their source artifacts remain
unchanged. Pair candidate counts include only admitted records. Production
routing errors remain measured observations, and no-skill/external baselines
are not required to load OpenDeepMind modules.

聚合前须核验运行记录与实验配置一致：禁用模块既不能出现在加载列表中，也不能由
选定路由调用；强制 P 路由的消融记录必须报告 `route="p"`。不计生产路由准确率
不等于免除配置校验。违例记录保留原始文件和路径诊断，但不进入完整运行数、
单配置指标或配对统计。这些检查仅验证自报元数据的一致性，不能证明真实模型执行。

### Configuration integrity change record

- **Problem / failed invariant:** schema-valid records could declare a no-TRIZ
  ablation while selecting or loading TRIZ and still contribute ablation wins
  and deltas.
- **Evidence / affected layer:** public workspace-creation and aggregation CLI
  regressions populate all 114 validation slots with synthetic artifacts, then
  contradict the configuration in one or all six ablation slots.
- **Rule / expected improvement:** validate forced routes and disabled modules
  before admitting a record to any configuration or paired metric. Invalid arm
  records cannot establish complete evidence for that experiment.
- **Compatibility / new risk:** no schema fields or case distributions change;
  previously admitted contradictory records are now excluded and require
  investigation of the original run. Do not relabel an observed TRIZ run as P
  merely to pass validation. Valid baselines and ablations remain compatible.
- **Validation / remaining limit:** CLI controls cover forbidden routes, forbidden
  loads, alternative forced routes, partial contamination, production failures,
  source preservation, and valid full workspaces. Self-reported metadata remains
  insufficient for model-execution attestation or causal performance claims.

## 6. Grading layers

### Layer A — deterministic

Use code for mechanically verifiable facts:

- case/config/repetition metadata;
- production expected route;
- explicit-only TRIZ policy;
- module-load leakage;
- artifact existence;
- valid JSON where a structured artifact is required;
- intentional route override for the no-TRIZ ablation.

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

For `opendeepmind_full` versus the no-skill baseline, pinned first-principles baseline, or no-TRIZ ablation, hide configuration labels and ask the judge/human reviewer which output is stronger and why.

## 7. Red blockers

Any of the following can force a case failure regardless of average rubric score:

- fabricated source/data/experiment;
- unsupported load-bearing factual claim presented as verified;
- correlation promoted to intervention causality without identification;
- model output presented as observation;
- unbridged scale jump;
- hidden value/objective controlling the recommendation;
- TRIZ auto-activation without explicit authorization in production behavior;
- TRIZ principle/matrix/SIS treated as proof of engineering feasibility;
- no serious rival/falsifier where the case explicitly requires one;
- unsafe removal of a verified legal/safety/ethical constraint.

The intentional no-TRIZ ablation is not scored as a TRIZ false-activation/routing failure merely because the experiment disables the module; its purpose is causal contribution measurement.

## 8. Key metrics

The aggregator reports at least:

```text
case_pass_rate
assertion_pass_rate
red_blocker_rate
routing_accuracy
triz_false_activation_rate
module_leakage_rate
judge_score_mean
rival_model_coverage
falsifier_coverage
mean_tokens
mean_duration_ms
```

For each declared comparison it also computes common-case/repetition paired deltas for assertion score, judge score, tokens and duration. Blind pairwise results remain a separate grading artifact when supplied.

Pairing checks the declared `model` and `model_version` and requires matching
`execution_conditions`: effective sampling settings, reasoning settings, tool
access/definitions, and ordered input-file paths and SHA-256 digests. Object keys
are compared without regard to order; array order remains significant. Missing
conditions exclude a pair with `EXECUTION_CONDITIONS_MISSING`; differing
conditions exclude it with `EXECUTION_CONDITIONS_MISMATCH`. These reasons appear
with the case and repetition in `excluded_pairs`. `candidate_paired_runs` counts
common case/repetition identities before compatibility checks; `paired_runs`
counts only compatible pairs. Individual configuration metrics and artifact
completeness still describe all valid observations and are not rewritten or
discarded. If both versions are absent/empty but conditions match, descriptive
pairing is preserved and counted in `unversioned_paired_runs`; it does not
establish matched model snapshots. Legacy records without execution conditions
remain usable for individual metrics but do not contribute paired deltas or wins.
The run harness must record the effective request conditions in this field. The
aggregator compares declared metadata; it cannot attest provider execution,
independent grading, or a causal skill improvement. The independent publication
gate remains closed.

配对比较除模型及版本外，还要求双方都提供且完全匹配的 `execution_conditions`，
包括有效采样/推理设置、工具访问条件以及输入文件路径和 SHA-256。条件缺失或不匹配时，
配对差值及胜负计数会排除该样本并记录原因；各配置的单独指标仍保留。旧记录缺少
执行条件时仍可用于单独指标，但不参与配对差值。双方都没有模型版本但执行条件匹配时，
仍保留描述性配对并计入未验证版本数。上述字段均为运行器自报，不能证明服务端实际执行身份。

### Pair identity change record

- **Problem / failed invariant:** case and repetition identity alone admitted
  comparisons between explicitly different models or model snapshots. Even after
  model/version matching, settings, tool access and input differences could still
  produce a paired delta.
- **Evidence / affected layer:** synthetic regression artifacts reproduce a
  one-point assertion delta with the same model/version but different temperature
  and tool access. The aggregator now excludes missing or differing execution
  conditions from pair deltas and wins.
- **API / compatibility:** existing fields remain; exclusion records, candidate
  counts and unversioned counts are additive. Only incompatible paired metrics
  change. Source records, per-configuration metrics and runtime methods are unchanged.
- **Expected improvement / remaining risk:** prevents reported settings, tools or
  input differences from being attributed to the skill. Conditions remain
  self-reported; this does not attest provider-side execution or grading
  independence. These fixtures are software checks, not model experiments.
- **Validation:** paired-identity and CLI regressions, run-record schema,
  repository/module/evaluation validators and the complete unittest suite.

Do not publish benchmark scores until actual runs and grading artifacts exist.

### Cost and latency records

Optional `run_record.json` cost example (illustrative units, not a measured bill):

```json
{
  "cost": {
    "amount_microunits": 250,
    "currency": "USD",
    "basis": "usage_priced",
    "pricing_reference": "provider-rate-snapshot-id"
  }
}
```

One microunit is one millionth of the named currency unit. Supply a non-negative
safe integer, a three-letter uppercase currency code, `provider_reported` or
`usage_priced`, and the billing/rate snapshot used. For `usage_priced`, preserve
the actual usage breakdown and applied rates with the raw run evidence. The
aggregator does not fetch prices, infer costs from total tokens, or convert
currencies. Omit `cost` when unmeasured; explicit null and malformed cost records
are metadata errors. An observed zero is valid and distinct from absence.

`cost_missing_runs` counts absent observations. `cost_summaries` groups by
currency, basis and pricing reference. A compatible quality/token/latency pair
contributes a cost delta only if both costs have matching identities; otherwise
`excluded_cost_pairs` records why and the other valid paired metrics remain.
No aggregate combines unlike currencies or pricing snapshots.

Token and duration distributions report their sample count and nearest-rank
P50/P95: sort the observations and take rank `ceil(p*n)`, with one-based ranks.
An empty sample has null quantiles. Paired delta distributions are quantiles of
individual left-minus-right differences, not differences of marginal quantiles.
`by_route` is descriptive and can have different case mixes; it is not an
independent experiment or a causal comparison of routing choices.

成本未测量时应省略 `cost`，不得填零。不同币种、计费方式或价格快照不会混合汇总；
配对成本差额仍受原模型身份、执行设置和输入一致性检查约束。P50/P95 同时提供
样本数和最近秩定义。按路由汇总是描述性观测，任务组成不同不能当作路由因果效应。
所有外部运行与评分证据仍需独立审核，`publication_ready` 保持 false。

#### Accounting change record

- **Problem / evidence:** mean-only token/latency output hid tails and absent
  costs could not be distinguished from zero cost. Known synthetic records test
  the arithmetic and incompatible-accounting exclusions.
- **Affected layer / API:** optional cost schema, run validation, additive
  distribution/route/cost output. Fixed cases, splits, configurations, grading
  assertions and publication gates are unchanged.
- **Expected improvement / new risk:** comparable observed costs and explicit
  missingness; supplied billing metadata can still be wrong. No pricing,
  provider execution or scientific quality is attested by the aggregator.
- **Compatibility / validation:** legacy cost-free records remain valid with
  missing-cost counts. Public CLI regressions and the original complete CI
  validate accounting. Actual model quality, tokens, costs and latency require
  a configured external runner and independent grading.

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

The scripts are dependency-free and do not call any model API. The actual model/agent harness is intentionally external so the benchmark can run across different Agent-Skills-compatible runtimes or model providers without changing the benchmark definitions.

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
raw run records
raw grading artifacts
aggregated benchmark.json
human/model-judge rubric and identity when applicable
```

`artifact_set_complete=true` means only that every expected run slot has consistent run and grading artifacts. The dependency-free aggregator deliberately keeps `publication_ready=false` until a separate, independently verified publication attestation binds the exact repository revision, model/provider settings, raw artifacts, holdout seal, grader identity and release authority.

Authored cases, complete slots, or aggregated scores are not themselves a published model result. Do not claim that a benchmark result proves universal superiority. It establishes performance only on the disclosed task distribution, models, settings and graders.

## Artifact integrity checks

The aggregator validates assertion counts and rates against their records; passing assertions need response evidence. Every grading record must explicitly include its red-blocker list and module-leakage verdict; missing status is unknown and cannot count as clear. Empty assertions, red blockers and reported leakage cannot yield a passing case. Routing and forbidden TRIZ activation derive from recorded metadata, and aggregate/paired case verdicts share one rule. Expected artifacts must be regular files within the workspace; symlinks and special files are rejected. Reports are written atomically, and output symlinks are refused. Orphan artifacts prevent completeness. JSON inputs are bounded to 8 MiB and 128 levels, with finite metrics and safe integer counters. These checks establish internal consistency, not external model execution or publication authority.

### Report destination preservation

`--output` cannot target the workspace manifest or any path below a workspace `eval-*` directory, including case definitions, instructions, run/grading records and raw outputs. Resolved parent-directory aliases receive the same check. Keep derived reports at the workspace root or outside case directories; existing report destinations there remain refreshable. The path precheck does not provide isolation from concurrent directory replacement.

输出位置不得覆盖工作区清单或 `eval-*` 目录中的案例、指令、运行/评分记录及原始输出；解析父目录别名后采用相同规则。派生报告应位于工作区根目录或案例目录之外，原有报告可重复更新。路径预检查不提供并发目录替换隔离。
