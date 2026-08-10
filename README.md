<p align="center">
  <img src="open-deep-mind/assets/diagrams/homepage-bilingual.svg" alt="OpenDeepMind_skill 中英双语方法总览 / Bilingual methodology overview" width="100%">
</p>

<h1 align="center">OpenDeepMind_skill</h1>

<p align="center">
  <strong>先审查基础，再从基础推导；需要发明时，显式进入 TRIZ。</strong><br>
  <strong>Qualify the foundation, derive from it, and enter TRIZ only by explicit choice.</strong>
</p>

<p align="center">
  <a href="open-deep-mind/SKILL.md">Agent Skill Router</a> ·
  <a href="open-deep-mind/ARCHITECTURE.md">Architecture</a> ·
  <a href="open-deep-mind/MODULES.json">MODULES.json</a> ·
  <a href="open-deep-mind/first-philosophy/METHOD.md">第一哲学 / First Philosophy</a> ·
  <a href="open-deep-mind/first-principles/METHOD.md">第一性原理 / First Principles</a> ·
  <a href="open-deep-mind/triz/ROUTER.md">TRIZ Router</a> ·
  <a href="open-deep-mind/triz/README.md">完整 TRIZ / Full TRIZ</a>
</p>

<p align="center">
  <img alt="Agent Skills" src="https://img.shields.io/badge/Agent_Skills-compatible-6f5cff?style=flat-square">
  <img alt="Version" src="https://img.shields.io/badge/version-1.2.0-2a8cff?style=flat-square">
  <img alt="Core modules" src="https://img.shields.io/badge/core_modules-2-f2a649?style=flat-square">
  <img alt="Optional TRIZ" src="https://img.shields.io/badge/optional_TRIZ-explicit--only-e75f3c?style=flat-square">
  <img alt="TRIZ matrix" src="https://img.shields.io/badge/TRIZ_matrix-1190_cells-1565c0?style=flat-square">
  <img alt="TRIZ SIS" src="https://img.shields.io/badge/TRIZ_SIS-76-7b61ff?style=flat-square">
  <img alt="Runtime dependencies" src="https://img.shields.io/badge/runtime_dependencies-0-60758a?style=flat-square">
</p>

> **Independent project / 独立项目：** OpenDeepMind_skill is not affiliated with, sponsored by, or endorsed by Google DeepMind, OpenAI, Anthropic, MATRIZ, the Altshuller Institute, or the maintainers of referenced repositories.

---

## 1. Repository thesis / 仓库核心命题

OpenDeepMind is a **reasoning operating system**, not a single thinking trick.

It separates three different jobs that are often mixed together:

1. **First Philosophy / 第一哲学** — decide what is qualified to serve as a foundation.
2. **First Principles / 第一性原理** — decompose to explicit foundations, reconstruct models/solutions, and test them.
3. **TRIZ Engineering / TRIZ 工程发明** — when explicitly requested, systematically generate engineering invention concepts from contradictions, functions, resources, Su-Fields, ARIZ, effects, and evolution patterns.

The default route is:

```text
Frame
  -> First Philosophy Φ
  -> First Principles P
  -> rival models / falsification
  -> shared quality gate
  -> action / revision
```

TRIZ is deliberately outside the default path:

```text
explicit TRIZ request/acceptance
  -> Φ/P qualification
  -> TRIZ T inventive synthesis
  -> P validation
  -> shared quality gate
```

A named philosophy, principle, matrix cell, invention pattern, equation, or model output is never treated as proof by vocabulary alone.

---

## 2. True module isolation / 真正的模块隔离

Version 1.2.0 moves the canonical method bodies into separate directories.

```text
open-deep-mind/
├── SKILL.md                         # thin router only
├── ARCHITECTURE.md                  # module boundaries / handoffs
├── MODULES.json                     # machine-readable registry
│
├── first-philosophy/
│   ├── METHOD.md                    # canonical Φ8 method
│   ├── README.md                    # module contract
│   ├── module.json                  # manifest
│   ├── foundation-charter.schema.json
│   ├── example-foundation-charter.json
│   └── scripts/validate_module.py
│
├── first-principles/
│   ├── METHOD.md                    # canonical P9 method
│   ├── README.md                    # module contract
│   ├── module.json                  # manifest
│   ├── model-contract.schema.json
│   ├── decision-record.schema.json
│   ├── example-model-contract.json
│   ├── example-decision-record.json
│   └── scripts/validate_module.py
│
├── triz/
│   ├── ROUTER.md                    # canonical explicit-only T10 router
│   ├── README.md                    # complete TRIZ subsystem map
│   ├── module.json                  # manifest
│   ├── resources/                   # classical + modern operational resources
│   ├── examples/
│   └── scripts/
│
├── references/                      # shared method-neutral references
├── assets/                          # shared schemas/templates/visuals
└── scripts/                         # repository + ledger validators
```

The historical root files remain only as thin compatibility aliases:

```text
FIRST_PHILOSOPHY.md  -> first-philosophy/METHOD.md
FIRST_PRINCIPLES.md  -> first-principles/METHOD.md
TRIZ_ENGINEERING.md  -> triz/ROUTER.md
```

New maintenance targets the canonical module paths, not the aliases.

Full contract: [`open-deep-mind/ARCHITECTURE.md`](open-deep-mind/ARCHITECTURE.md).

---

## 3. Module Φ — First Philosophy / 第一哲学

Canonical file:

[`open-deep-mind/first-philosophy/METHOD.md`](open-deep-mind/first-philosophy/METHOD.md)

First Philosophy asks:

> **What must be clarified, accepted, or justified before this can count as a coherent problem and before a solution can count as warranted?**

Its eight-stage protocol is exactly:

```text
Φ0 Suspend the inherited frame
Φ1 Semantic audit
Φ2 Ontology map
Φ3 Epistemic audit
Φ4 Logical audit
Φ5 Causality and explanation audit
Φ6 Boundary, scale and time audit
Φ7 Value, ethics and praxis audit
```

That is **Φ8 = Φ0..Φ7**, eight stages.

Its main output is a **Foundation Charter**, not a solution:

```text
neutral + rival frames
definitions
ontology
epistemic status
logic / causality / explanation commitments
boundary / scale / time
values / duties / stakeholders
accepted / conditional / rejected foundations
blocking unknowns
```

Machine-readable contract:

- [`foundation-charter.schema.json`](open-deep-mind/first-philosophy/foundation-charter.schema.json)
- [`example-foundation-charter.json`](open-deep-mind/first-philosophy/example-foundation-charter.json)

**Hard separation:** this module does not load or invoke TRIZ.

---

## 4. Module P — First Principles / 第一性原理

Canonical file:

[`open-deep-mind/first-principles/METHOD.md`](open-deep-mind/first-principles/METHOD.md)

The P9 protocol is normalized to exactly **P1..P9**:

```text
P1 Delete, modify, or justify the requirement
P2 Define outcome and boundary
P3 Expose assumptions and proposition types
P4 Decompose to irreducibles
P5 Qualify foundations
P6 Build the model
P7 Reconstruct alternatives
P8 Derive, trace, falsify, and stress-test
P9 Decide, act, monitor, and update
```

Earlier versions used a `P0..P9` numbering while calling the procedure “P9”; v1.2.0 removes that inconsistency.

### Typed proposition ledger

All load-bearing claims are typed before inference:

\[
\mathcal B=\{D,O,L,C,A,E,V,U\}
\]

| Code | Type |
|---|---|
| `D` | Definition |
| `O` | Observation |
| `L` | Law / invariant |
| `C` | Constraint |
| `A` | Assumption |
| `E` | Empirical closure / estimate |
| `V` | Value |
| `U` | Unknown |

This prevents a fitted relation from masquerading as a law, a value from masquerading as a fact, or a model output from masquerading as an observation.

### Model contract

Quantitative work exposes the relevant subset of:

\[
\mathcal M=
\{\mathbf x,\mathbf u,\boldsymbol\theta,
\mathbf F,\mathbf h,\mathbf g,
\mathrm{IC},\mathrm{BC},\mathcal O,\mathcal E\}
\]

including parameter provenance, assumptions/closures, observation/error models, validity domain, and falsifiers.

Machine-readable contracts:

- [`model-contract.schema.json`](open-deep-mind/first-principles/model-contract.schema.json)
- [`decision-record.schema.json`](open-deep-mind/first-principles/decision-record.schema.json)

**Hard separation:** the canonical P method body contains no TRIZ procedure and never auto-loads TRIZ.

---

## 5. Module T — Complete TRIZ Engineering / 完整 TRIZ 工程发明

Canonical explicit-only router:

[`open-deep-mind/triz/ROUTER.md`](open-deep-mind/triz/ROUTER.md)

Complete subsystem:

[`open-deep-mind/triz/README.md`](open-deep-mind/triz/README.md)

TRIZ is a **specialist engineering invention subsystem**, not a third foundational engine. It activates only after explicit user request or explicit acceptance of a suggested TRIZ route.

The normalized **T10 = T1..T10** workflow covers:

```text
T1 explicit activation / engineering scope
T2 key-problem identification
T3 resources / ideality / IFR
T4 problem model
T5 route selection
T6 distinct concept families
T7 translate abstractions into mechanisms
T8 hard engineering gates
T9 discriminating validation
T10 return to First Principles
```

### TRIZ coverage

The subsystem includes:

- function analysis / function-cost analysis;
- flow analysis;
- CECA cause-effect chains;
- trimming and feature transfer;
- innovative benchmarking;
- Nine Windows/System Operator, STC, Smart Little People;
- ideality, IFR, resource analysis;
- engineering and physical contradictions;
- **39 engineering parameters**;
- **40 inventive principles**;
- **full contradiction-matrix transcription with 1190 populated cells**;
- separation principles;
- Su-Field modeling;
- **76 Standard Inventive Solutions** in the public five-class numbering;
- ARIZ-85C;
- clone-problem transfer;
- scientific-effects / FOS route;
- S-curve and TESE/evolution routes;
- concept substantiation;
- worked examples and deterministic lookup/validation scripts.

### Historical-data discipline

The matrix is a vendored historical transcription with provenance, not an infallible oracle. Known transcription anomalies are tracked separately in:

[`open-deep-mind/triz/resources/matrix_anomalies.json`](open-deep-mind/triz/resources/matrix_anomalies.json)

The lookup utility returns both raw and normalized values where an anomaly is documented rather than silently changing the vendored source.

### TRIZ never equals proof

A TRIZ result must return to First Principles:

```text
inventive concept
  -> governing physics / equations
  -> material and manufacturing feasibility
  -> parameter/data provenance
  -> uncertainty and sensitivity
  -> safety / regulatory / lifecycle
  -> simulation / experiment / prototype
  -> rival model / falsifier
```

---

## 6. Shared quality system / 共享质量门

All modules use the shared red-blocker-first gate:

[`open-deep-mind/references/quality-gates.md`](open-deep-mind/references/quality-gates.md)

A high numerical score cannot compensate for:

- undefined load-bearing terms;
- unsupported key facts;
- invalid inference;
- correlation written as causality;
- model output written as observation;
- hidden cross-scale jumps;
- missing parameter provenance/closure/boundary conditions;
- no serious rival/falsifier;
- hidden value function;
- unsafe deletion of safeguards;
- fabricated sources/data/experiments.

The shared quality score remains diagnostic rather than a substitute for evidence or professional judgment.

---

## 7. Cross-scale discipline / 跨尺度纪律

A chain such as:

\[
\hat H\Psi=E\Psi
\rightarrow
m_i\ddot{\mathbf r}_i=-\nabla_iU
\rightarrow
\frac{\partial\phi}{\partial t}=-L\frac{\delta\mathcal F}{\delta\phi}
\rightarrow
\frac{\partial u}{\partial t}+\nabla\cdot F=S
\rightarrow
x^*=\arg\min J
\]

is **not** one automatic derivation. Every arrow requires a declared bridge:

```text
mapping variables
closure/coarse-graining
information lost
parameter/calibration source
uncertainty propagation
validation domain
failure conditions
```

---

## 8. Domain routing / 领域路由

Shared domain router:

[`open-deep-mind/references/domain-routing.md`](open-deep-mind/references/domain-routing.md)

Key invariant:

> **No science, engineering, strategy, policy, personal, creative, software, or modeling route activates TRIZ by default.**

Canonical TRIZ exists only as a separate explicit engineering route.

For cross-domain tasks, the strictest active evidence, safety, legal, and ethical standard governs the shared decision.

---

## 9. Deterministic tools and validation / 确定性工具与验证

### Repository architecture

```bash
python open-deep-mind/scripts/validate_repository.py .
```

### Shared proposition ledger

```bash
python open-deep-mind/scripts/validate_ledger.py \
  open-deep-mind/assets/example-ledger.json
```

The ledger validator checks IDs, type/status consistency, references, decision traces, and dependency cycles.

### First Philosophy

```bash
python open-deep-mind/first-philosophy/scripts/validate_module.py
```

### First Principles

```bash
python open-deep-mind/first-principles/scripts/validate_module.py
```

### TRIZ

```bash
python open-deep-mind/triz/scripts/validate_triz_module.py
python open-deep-mind/triz/scripts/lookup_matrix.py --improve 10 --worsen 17 --json
python open-deep-mind/triz/scripts/lookup_standard_solution.py 1.2.1 --json
```

### Regression suite

```bash
python -m unittest discover -s open-deep-mind/tests -p "test_*.py"
python -m compileall -q open-deep-mind
```

GitHub Actions executes the same architecture/module/lookup/regression layers on pushes and pull requests.

---

## 10. Installation / 安装

```bash
git clone https://github.com/SUNHAOJUN22/OpenDeepMind_skill.git
```

For Agent Skills-compatible clients, point the runtime at:

```text
open-deep-mind/SKILL.md
```

The router progressively loads only the selected module and shared resources needed by the task.

---

## 11. Invocation / 调用示例

### First Philosophy

```text
调用 OpenDeepMind 第一哲学模块。
先审查这个问题的定义、本体、认识状态、逻辑、因果/解释、边界尺度、价值与实践条件；
输出 Foundation Charter，不要提前优化解决方案。
```

### First Principles

```text
调用 OpenDeepMind 第一性原理 P9。
拆解需求和假设，建立 D/O/L/C/A/E/V/U 命题账本与完整模型契约，
从合格基础重构多个方案，建立强竞争模型、证伪条件、不确定性和决策记录。
不要调用 TRIZ。
```

### Explicit TRIZ

```text
明确调用 OpenDeepMind TRIZ 工程模块。
先完成必要的 Φ/P 资格审查，再按 T1..T10 识别关键工程问题、IFR、资源和矛盾，
按需使用矩阵/40原理、分离、Su-Field/76标准解、ARIZ、FOS/效应或 TESE，
生成具体工程机制概念，最后返回第一性原理做物理、证据、安全和试验验证。
```

---

## 12. Completeness boundary / 完备性边界

“Repository complete” means the repository has explicit module contracts, manifests, schemas/fixtures, validators, shared quality infrastructure, deterministic TRIZ data tools, CI, version/provenance/license controls, and regression tests.

It does **not** mean:

- philosophy is exhausted by one file;
- every scientific discipline shares one evidence model;
- every TRIZ book/patent/scientific effect is copied into the repository;
- first-principles computation is assumption-free;
- a validator can prove a real-world engineering conclusion true.

The design principle is instead:

\[
\boxed{\text{explicit boundary}+\text{traceable reasoning}+\text{testable failure}+\text{revisability}}
\]

---

## 13. Provenance and licenses / 来源与许可

OpenDeepMind is an original synthesis informed by philosophical, scientific, systems, engineering, and open Agent Skill traditions.

Key implementation influences include:

- `danyuchn/first-principles-skill` — first-principles requirement challenge/reconstruction;
- `smixs/creative-director-skill` — routing, recursive evaluation, output discipline, visual documentation;
- `Antropocosmist/triz-engineering-solver` — MIT-licensed TRIZ implementation/data reference;
- public MATRIZ knowledge-base terminology/routing and Altshuller/TRIZ theoretical lineage.

See:

- [`NOTICE.md`](NOTICE.md)
- [`LICENSE.md`](LICENSE.md)
- [`open-deep-mind/triz/VENDORED_LICENSE.md`](open-deep-mind/triz/VENDORED_LICENSE.md)
- [`open-deep-mind/triz/resources/sources.md`](open-deep-mind/triz/resources/sources.md)
- [`open-deep-mind/references/intellectual-lineage.md`](open-deep-mind/references/intellectual-lineage.md)

---

<p align="center">
  <strong>Foundation → Principle → Model → Test → Action → Revision</strong><br>
  <sub>模块隔离 / Explicit provenance / Falsifiable reasoning / Revisable decisions</sub>
</p>
