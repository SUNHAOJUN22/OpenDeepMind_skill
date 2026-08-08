<p align="center">
  <a href="open-deep-mind/assets/diagrams/homepage-bilingual-20260808.webp">
    <img src="https://raw.githubusercontent.com/SUNHAOJUN22/OpenDeepMind_skill/main/open-deep-mind/assets/diagrams/homepage-bilingual-20260808.webp" alt="OpenDeepMind_skill 中英双语思维系统总览 / Bilingual reasoning-system overview" width="100%">
  </a>
</p>

<h1 align="center">OpenDeepMind_skill</h1>

<p align="center">
  <strong>用第一哲学审查基础，用第一性原理重构方案。</strong><br>
  <strong>Qualify foundations with First Philosophy. Reconstruct solutions with First Principles.</strong>
</p>

<p align="center">
  <a href="README.zh-CN.md">中文文档</a> ·
  <a href="open-deep-mind/SKILL.md">Agent Skill</a> ·
  <a href="open-deep-mind/FIRST_PHILOSOPHY.md">第一哲学 / First Philosophy</a> ·
  <a href="open-deep-mind/FIRST_PRINCIPLES.md">第一性原理 / First Principles</a> ·
  <a href="open-deep-mind/references/method-atlas.md">方法图谱 / Method Atlas</a>
</p>

<p align="center">
  <img alt="Agent Skills" src="https://img.shields.io/badge/Agent_Skills-compatible-6f5cff?style=flat-square">
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-2aa8ff?style=flat-square">
  <img alt="Languages" src="https://img.shields.io/badge/languages-中文%20%7C%20English-3bc9a7?style=flat-square">
  <img alt="Core engines" src="https://img.shields.io/badge/core_engines-2-f2a649?style=flat-square">
  <img alt="Runtime dependencies" src="https://img.shields.io/badge/runtime_dependencies-0-91a7bd?style=flat-square">
</p>

> **OpenDeepMind_skill** 是一套面向复杂问题、科研论证、工程设计、战略决策和创造实践的通用双引擎思维系统。它先审查“什么有资格成为基础”，再从通过审查的基础向上推导，并要求每项关键结论都能追溯、竞争、证伪和修正。
>
> **OpenDeepMind_skill** is a domain-general dual-engine reasoning system for complex inquiry, scientific argument, engineering design, strategy, and creative practice. It first qualifies what may count as a foundation, then reasons upward while keeping every material claim traceable, contestable, falsifiable, and revisable.
>
> **独立项目声明 / Independent project:** 本项目与 Google DeepMind 无隶属、合作或背书关系。The repository name denotes an open methodology for deep and auditable reasoning; it is not affiliated with or endorsed by Google DeepMind.

---

## 1. 核心命题 / Core Thesis

普通的“第一性原理思维”经常直接拆解问题，却没有先审查问题框架本身。OpenDeepMind 在第一性原理之前加入第一哲学基础审查，并把推理组织为闭环：

Many “first-principles” workflows decompose too early. OpenDeepMind inserts a foundation audit before decomposition and organizes reasoning as a closed loop:

$$
\boxed{
\text{问题框架 / Frame}
\rightarrow
\text{第一哲学 / First Philosophy}
\rightarrow
\text{第一性原理 / First Principles}
\rightarrow
\text{竞争模型 / Rival Models}
\rightarrow
\text{证伪与质量门 / Falsification \& Quality Gate}
\rightarrow
\text{行动与修正 / Action \& Revision}
}
$$

这不是哲学百科，也不是任意发散的头脑风暴工具。它是一套可执行协议，用于把模糊问题转化为：

It is neither a philosophy encyclopedia nor an unconstrained brainstorming toy. It is an executable protocol for converting ambiguous questions into:

- 类型明确的命题 / typed claims;
- 可辩护的基础 / qualified foundations;
- 可比较的竞争模型 / comparable rival models;
- 可证伪的推导 / falsifiable derivations;
- 可执行、可监测、可复审的决策 / actionable, monitorable, reviewable decisions.

---

## 2. 双引擎架构 / Dual-Engine Architecture

| 引擎 / Engine | 核心问题 / Governing question | 主要输出 / Primary output | 文件 / File |
|---|---|---|---|
| **Φ 第一哲学 / First Philosophy** | 在当前问题中，什么有资格成为基础？ / What may legitimately count as a foundation? | 《基础章程》、定义、本体、证据状态、边界、价值与阻断项 / Foundation Charter | [`FIRST_PHILOSOPHY.md`](open-deep-mind/FIRST_PHILOSOPHY.md) |
| **P 第一性原理 / First Principles** | 从通过审查的基础能够推出什么？ / What follows from the qualified foundations? | 基底命题、模型、竞争方案、证伪条件、行动与复审触发器 / Derived models and decisions | [`FIRST_PRINCIPLES.md`](open-deep-mind/FIRST_PRINCIPLES.md) |

### Φ：第一哲学 / First Philosophy

第一哲学引擎审查八个基础维度：

The First Philosophy engine audits eight foundational dimensions:

$$
\mathcal{F}_{\Phi}
=
\{\text{语义},\text{本体},\text{认识},\text{逻辑},\text{因果},\text{边界},\text{价值},\text{实践}\}
$$

它要求明确：

- 核心术语如何定义；
- 对象、过程、关系和属性是什么；
- 哪些内容是观测、推断、模型输出、假设或价值判断；
- 因果主张依赖什么识别条件；
- 系统边界、时间尺度和适用域在哪里；
- 谁承担风险，谁获得收益，哪些义务不可被优化掉。

It clarifies definitions, ontology, epistemic status, causal commitments, system boundaries, scales, values, affected parties, and non-negotiable duties.

### P：第一性原理 / First Principles

第一性原理引擎执行 P9 拆解—重构协议：

The First Principles engine executes the P9 decomposition–reconstruction protocol:

1. 删除、修改或证明需求合理 / delete, modify, or justify the requirement;
2. 定义真实结果和系统边界 / define outcomes and boundaries;
3. 暴露并分类假设 / expose and type assumptions;
4. 沿依赖关系向下拆解 / decompose dependencies;
5. 审查候选基底命题 / qualify primitive claims;
6. 建立约束、因果、动态或数理模型 / build models and constraints;
7. 构造结构不同的竞争方案 / construct rival solutions;
8. 推导、计算、证伪和鲁棒性检验 / derive, compute, falsify, and stress-test;
9. 决策、监测、复审与更新 / decide, monitor, review, and update.

---

## 3. 命题账本 / Proposition Ledger

OpenDeepMind 不允许不同类型的命题互相借用权威。所有承重命题必须分类：

OpenDeepMind prevents unlike claims from borrowing one another’s authority. Every load-bearing claim is typed:

| 编码 | 类型 | 含义 |
|---|---|---|
| `D` | 定义 / Definition | 约定、词汇、操作性或理论定义 |
| `O` | 观测 / Observation | 测量、记录或直接来源 |
| `L` | 规律 / Law or invariant | 在明确适用域内得到支持的规律 |
| `C` | 约束 / Constraint | 物理、逻辑、法律、伦理或资源边界 |
| `A` | 假设 / Assumption | 仍需检验或敏感性审查的前提 |
| `E` | 经验闭合 / Empirical closure | 拟合、代理、本构关系、启发式或学习型近似 |
| `V` | 价值 / Value | 目标、义务、偏好、效用和风险容忍度 |
| `U` | 未知 / Unknown | 足以改变结论但尚未解决的事项 |

每项关键命题还应记录：

```text
status · scope · source · dependencies · confidence · falsifier · owner · review date
```

可直接使用：

- [`claim-ledger-template.md`](open-deep-mind/assets/claim-ledger-template.md)
- [`claim-ledger.schema.json`](open-deep-mind/assets/claim-ledger.schema.json)
- [`example-ledger.json`](open-deep-mind/assets/example-ledger.json)

---

## 4. 跨尺度推理 / Cross-Scale Reasoning

“第一”总是相对于领域、尺度、目标和理论层级而言。任何跨尺度箭头都必须声明映射、闭合和不确定性：

“First” is always relative to a domain, scale, purpose, and theory level. Every cross-scale bridge must expose its mapping, closure, and uncertainty:

$$
\text{低尺度状态 / Lower-scale state}
\xrightarrow[\text{uncertainty}]{\text{mapping + closure}}
\text{有效变量 / Effective variables}
\xrightarrow[\text{validation}]{\text{higher-scale model}}
\text{可观测结果 / Observable outcome}
$$

每个尺度桥必须回答：

- 映射变量是什么；
- 使用了何种粗粒化、同质化或闭合假设；
- 丢失了哪些信息；
- 参数来自理论、计算、实验还是拟合；
- 不确定性如何传播；
- 模型在哪些条件下失效。

---

## 5. 质量门 / Quality Gate

OpenDeepMind 采用“阻断项优先、评分随后”的两层质量体系。

OpenDeepMind uses a two-layer quality system: blockers first, scoring second.

### 红色阻断项 / Red Blockers

出现任意一项时，不得把结果称为最终、已验证或高可信：

- 核心术语未定义或前后变义；
- 关键事实无可靠来源；
- 结论不由前提推出；
- 把相关性写成因果性；
- 把模型输出写成直接观测；
- 隐藏目标函数或价值权重；
- 未建立尺度桥就跨尺度下结论；
- 没有严肃竞争模型或证伪条件；
- 虚构文献、数据、实验、引文或共识；
- 未核验就删除法律、安全或伦理保护。

### 100 分质量评分 / 100-Point Reasoning Score

$$
Q=\sum_{i=1}^{12} w_i s_i-\lambda B,
\qquad B>0\Rightarrow\text{阻断交付 / reject delivery}
$$

十二个维度覆盖基础清晰度、命题分类、证据质量、拆解完整性、因果解释、模型完整性、可追溯性、竞争方案、可证伪性、不确定性、价值伦理和可执行性。

Full rubric: [`quality-gates.md`](open-deep-mind/references/quality-gates.md)

---

## 6. 领域路由 / Domain Routing

同一套核心语法会根据任务领域切换证据标准和方法组合：

The same core grammar adapts its evidence standard and method bundle by domain:

| 领域 / Domain | 默认重点 / Default emphasis |
|---|---|
| 科学研究 / Scientific research | 测量、机制、竞争解释、前瞻预测与判别实验 |
| 工程与软件 / Engineering and software | 功能、硬约束、故障、运维、可逆性与安全裕度 |
| 数理建模 / Quantitative modeling | 控制方程、闭合、参数、初边值、收敛与不确定性 |
| 商业与战略 / Business and strategy | 价值机制、经济性、竞争响应、实物期权与退出条件 |
| 政策、法律与伦理 / Policy, law, and ethics | 权限、权利、证据、分配、申诉与退出机制 |
| 个人决策 / Personal decisions | 真实价值、观察行为、可逆试验与复审触发器 |
| 创意与产品 / Creative and product innovation | 张力、矛盾、结构性新颖、效用和价值验证 |

跨领域总规则：**采用所有相关领域中最严格的证据、安全、法律和伦理标准。**

Full router: [`domain-routing.md`](open-deep-mind/references/domain-routing.md)

---

## 7. 视觉图谱 / Visual Atlas

仓库包含中英文两套可编辑、公式化 SVG 思维图，用于解释而非替代正式方法文本。

The repository contains separate Chinese and English editable SVG systems. The visuals explain the method; the Markdown files remain authoritative.

| 中文视觉 / Chinese | English Visual |
|---|---|
| [双引擎架构](open-deep-mind/assets/diagrams/zh/dual-engine.svg) | [Dual-engine architecture](open-deep-mind/assets/diagrams/en/dual-engine.svg) |
| [第一哲学八重透镜](open-deep-mind/assets/diagrams/zh/philosophy-lenses.svg) | [First Philosophy lenses](open-deep-mind/assets/diagrams/en/philosophy-lenses.svg) |
| [第一性原理循环](open-deep-mind/assets/diagrams/zh/principles-loop.svg) | [First Principles loop](open-deep-mind/assets/diagrams/en/principles-loop.svg) |
| [命题账本](open-deep-mind/assets/diagrams/zh/proposition-ledger.svg) | [Proposition ledger](open-deep-mind/assets/diagrams/en/proposition-ledger.svg) |
| [跨尺度阶梯](open-deep-mind/assets/diagrams/zh/scale-ladder.svg) | [Cross-scale ladder](open-deep-mind/assets/diagrams/en/scale-ladder.svg) |
| [质量门](open-deep-mind/assets/diagrams/zh/quality-gates.svg) | [Quality gates](open-deep-mind/assets/diagrams/en/quality-gates.svg) |

---

## 8. 快速开始 / Quick Start

### 安装 / Install

```bash
git clone https://github.com/SUNHAOJUN22/OpenDeepMind_skill.git
```

将 `open-deep-mind/` 复制到目标 Agent 的 Skill 目录。常见项目级路径包括：

```text
.codex/skills/
.claude/skills/
.cursor/skills/
.github/skills/
.gemini/skills/
.agent/skills/
```

### 直接调用 / Direct Invocation

```text
读取 open-deep-mind/SKILL.md。
对当前问题执行“第一哲学 → 第一性原理”双引擎模式。
先审查定义、本体、证据、因果、边界和价值，再拆解至基底命题并向上重构。
输出基础章程、命题账本、竞争模型、质量门、结论、证伪条件和复审触发器。
```

```text
Read open-deep-mind/SKILL.md.
Apply the First Philosophy → First Principles dual-engine mode.
Return the Foundation Charter, proposition ledger, rival models,
quality gate, recommendation, falsifier, and review trigger.
```

### 示例任务 / Example Tasks

```text
从第一性原理审查这个软件架构，但不要默认需求本身合理。
```

```text
审计这项科研机制主张，区分直接观测、模型输出、假设、经验闭合和尺度桥。
```

```text
Rebuild this strategy from first principles. Include the no-action baseline,
competitor response, uncertainty, falsifiers, and reversible next steps.
```

Worked cases: [`worked-examples.md`](open-deep-mind/references/worked-examples.md)

---

## 9. 仓库结构 / Repository Structure

```text
OpenDeepMind_skill/
├── README.md
├── README.zh-CN.md
├── AGENTS.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE.md
├── NOTICE.md
├── .github/
│   └── workflows/
│       └── validate.yml
└── open-deep-mind/
    ├── SKILL.md
    ├── FIRST_PHILOSOPHY.md
    ├── FIRST_PRINCIPLES.md
    ├── references/
    │   ├── method-atlas.md
    │   ├── domain-routing.md
    │   ├── quality-gates.md
    │   ├── failure-modes.md
    │   ├── intellectual-lineage.md
    │   ├── glossary.md
    │   └── worked-examples.md
    ├── assets/
    │   ├── output-templates.md
    │   ├── claim-ledger-template.md
    │   ├── claim-ledger.schema.json
    │   ├── example-ledger.json
    │   └── diagrams/
    │       ├── homepage-bilingual-20260808.webp
    │       ├── zh/
    │       └── en/
    └── scripts/
        ├── validate_repository.py
        └── validate_ledger.py
```

---

## 10. 验证 / Validation

核心验证不依赖第三方 Python 包：

```bash
python open-deep-mind/scripts/validate_repository.py .
python open-deep-mind/scripts/validate_ledger.py \
  open-deep-mind/assets/example-ledger.json
```

验证范围包括：

- Agent Skills frontmatter；
- 第一哲学与第一性原理两个核心文件的独立性；
- Markdown 相对链接；
- JSON 与 Schema；
- SVG XML；
- Python 语法；
- 未解决阻断标记；
- 示例命题账本的结构和语义。

GitHub Actions 在 push 和 pull request 时执行相同检查。

---

## 11. 思想谱系与许可 / Intellectual Lineage and License

仓库架构与方法表达受到以下开源项目启发：

- [`danyuchn/first-principles-skill`](https://github.com/danyuchn/first-principles-skill)：需求删除测试与第一性原理拆解；
- [`smixs/creative-director-skill`](https://github.com/smixs/creative-director-skill)：阶段路由、方法选择、递归评估、交付纪律与视觉 README；
- Open Agent Skills pattern：简洁入口文件与按需加载的 references、assets 和 scripts。

OpenDeepMind 的双引擎架构、Φ8/P9 协议、《基础章程》、命题账本、跨尺度审计、质量门、领域路由、图形、脚本和示例均在本仓库中重新创作与封装。

详细来源与归因：[`intellectual-lineage.md`](open-deep-mind/references/intellectual-lineage.md) · [`NOTICE.md`](NOTICE.md)

- 代码、脚本、Schema 和工作流：Apache-2.0；
- 方法、文档和视觉资产：CC BY 4.0。

完整条款：[`LICENSE.md`](LICENSE.md)

---

## 12. 状态 / Status

**Version 1.0.0 — universal dual-engine methodology build.**

本项目坚持可证伪和可修正：未来任何规则变更都应记录失败假设、触发证据、修改内容、预期改善及兼容性影响。

The project is intentionally falsifiable and revisable. Future rule changes should record the failed assumption, triggering evidence, method change, expected improvement, and compatibility impact.
