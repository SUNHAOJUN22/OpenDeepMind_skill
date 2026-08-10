<p align="center">
  <img src="open-deep-mind/assets/diagrams/homepage-bilingual.svg" alt="OpenDeepMind_skill 中英双语方法总览 / Bilingual methodology overview" width="100%">
</p>

<h1 align="center">OpenDeepMind_skill</h1>

<p align="center">
  <strong>用第一哲学审查基础，用第一性原理重构方案。</strong><br>
  <strong>Qualify foundations with First Philosophy. Reconstruct solutions with First Principles.</strong>
</p>

<p align="center">
  <a href="open-deep-mind/SKILL.md">Agent Skill</a> ·
  <a href="open-deep-mind/FIRST_PHILOSOPHY.md">第一哲学 / First Philosophy</a> ·
  <a href="open-deep-mind/FIRST_PRINCIPLES.md">第一性原理 / First Principles</a> ·
  <a href="open-deep-mind/TRIZ_ENGINEERING.md">TRIZ 路由 / TRIZ Router</a> ·
  <a href="open-deep-mind/triz/README.md">完整 TRIZ / Full TRIZ Module</a> ·
  <a href="open-deep-mind/references/method-atlas.md">方法图谱 / Method Atlas</a>
</p>

<p align="center">
  <img alt="Agent Skills" src="https://img.shields.io/badge/Agent_Skills-compatible-6f5cff?style=flat-square">
  <img alt="Version" src="https://img.shields.io/badge/version-1.1.0-2a8cff?style=flat-square">
  <img alt="Core engines" src="https://img.shields.io/badge/core_engines-2-f2a649?style=flat-square">
  <img alt="TRIZ" src="https://img.shields.io/badge/optional_TRIZ-complete-e75f3c?style=flat-square">
  <img alt="TRIZ matrix" src="https://img.shields.io/badge/TRIZ_matrix-1190_cells-1565c0?style=flat-square">
  <img alt="TRIZ SIS" src="https://img.shields.io/badge/TRIZ_SIS-76-7b61ff?style=flat-square">
  <img alt="Runtime dependencies" src="https://img.shields.io/badge/runtime_dependencies-0-60758a?style=flat-square">
</p>

---

## 项目定位 / Positioning

**OpenDeepMind_skill** 是一套面向复杂问题与重大决策的通用思维操作系统。它不把“第一性原理”当作一句“从零思考”的口号，而是先解决更基础的问题：

> **什么有资格成为当前研究、设计或决策的基础？**

完成基础资格审查后，系统才从通过审查的定义、观测、规律、约束、假设、经验闭合、价值和未知项出发，构造模型、竞争方案、证伪条件与可执行决策。

OpenDeepMind_skill is a domain-general reasoning system for complex inquiry and consequential decisions. It first qualifies what may count as a foundation, then reconstructs models and actions from explicit claims, evidence, constraints, assumptions, values, and unknowns.

```math
\boxed{
\text{First Philosophy}
\rightarrow
\text{First Principles}
\rightarrow
\text{Competing Models}
\rightarrow
\text{Falsification / Quality Gate}
\rightarrow
\text{Action / Revision}
}
```

它适用于科研论证、机理分析、数理建模、工程设计、软件架构、商业战略、政策伦理、个人决策、创意设计与 AI 协作。

---

## 两个核心引擎 / Two Core Engines

| 引擎 | 核心问题 | 主要输出 |
|---|---|---|
| **Φ：第一哲学 / First Philosophy** | 什么可以作为基础？概念、对象、证据、因果、边界、尺度与价值是否清楚？ | 《基础章程》、概念定义、本体图、证据状态、边界、价值与阻断项 |
| **P：第一性原理 / First Principles** | 在明确领域、尺度、目的和条件下，从合格基础能够推出什么？ | 基底命题、模型、竞争方案、推导链、证伪条件、决策与复审触发器 |

### Φ8 第一哲学

1. 问题重构；
2. 语义审计；
3. 本体审计；
4. 认识论审计；
5. 逻辑、因果与解释审计；
6. 边界、尺度与时间审计；
7. 价值、伦理与利益相关者审计；
8. 基础资格判定。

独立文件：[`FIRST_PHILOSOPHY.md`](open-deep-mind/FIRST_PHILOSOPHY.md)

### P9 第一性原理

1. 删除、修改或证明需求合理；
2. 定义真实结果与系统边界；
3. 暴露并分类假设；
4. 沿依赖关系向下拆解；
5. 识别并审查基底命题；
6. 建立约束、因果、动态或数理模型；
7. 从基础向上构造结构不同的方案；
8. 推导、计算、竞争模型与证伪；
9. 决策、监测、复审与更新。

独立文件：[`FIRST_PRINCIPLES.md`](open-deep-mind/FIRST_PRINCIPLES.md)

---

## 命题账本 / Claim Ledger

OpenDeepMind 不允许不同类型的命题互相借用权威：

```math
\mathcal{B}=\{D,O,L,C,A,E,V,U\}
```

| 编码 | 类型 | 含义 |
|---|---|---|
| `D` | Definition / 定义 | 约定、操作性或理论定义 |
| `O` | Observation / 观测 | 测量、记录、直接来源 |
| `L` | Law / invariant / 规律 | 在明确适用域得到支持的规律或不变量 |
| `C` | Constraint / 约束 | 物理、逻辑、资源、法律、安全或伦理边界 |
| `A` | Assumption / 假设 | 尚未确立为事实、需要检验或敏感性审查的前提 |
| `E` | Empirical closure / 经验闭合 | 拟合、本构、代理、启发式或学习型近似 |
| `V` | Value / 价值 | 目标、义务、偏好、效用与风险容忍度 |
| `U` | Unknown / 未知 | 足以改变结论但尚未解决的问题 |

模板：

- [`claim-ledger-template.md`](open-deep-mind/assets/claim-ledger-template.md)
- [`claim-ledger.schema.json`](open-deep-mind/assets/claim-ledger.schema.json)
- [`example-ledger.json`](open-deep-mind/assets/example-ledger.json)

---

# 完整 TRIZ 工程发明子系统 / Complete TRIZ Engineering Subsystem

TRIZ **不是第三个基础引擎**。它是与第一性原理严格分离的、按需加载的专业工程发明模块。

```text
默认：
First Philosophy Φ
→ First Principles P
→ competing models
→ quality gate

显式 TRIZ：
Φ/P qualification
→ TRIZ inventive synthesis T
→ P-based physics / evidence validation
→ quality gate
```

### 默认不加载

只有用户明确提出或明确接受以下路线时才进入 TRIZ：

- TRIZ / ARIZ；
- 技术矛盾、物理矛盾；
- 矛盾矩阵、39 参数、40 发明原理；
- Su-Field / 物场、76 标准解；
- IFR / 理想最终结果；
- S-curve / TESE / 技术系统进化；
- 明确要求用 TRIZ 做工程发明分析。

普通的商业、组织、UX、政策、伦理和纯软件问题不会自动调用 TRIZ。用户明确要求类比使用时，必须标记为 `analogical TRIZ`，不得把类比当工程证明。

轻量路由器：[`TRIZ_ENGINEERING.md`](open-deep-mind/TRIZ_ENGINEERING.md)  
完整模块地图：[`open-deep-mind/triz/README.md`](open-deep-mind/triz/README.md)

---

## TRIZ 模块覆盖范围

### A. 现代问题识别 / Modern Problem Identification

模块不会默认“一看到问题就查矛盾矩阵”。先用最小必要方法找到**真正关键问题**：

- 功能与功能成本分析；
- 物质、能量/场、信息流分析；
- CECA 因果链分析；
- 裁剪 / partial trimming；
- 特征迁移；
- 创新标杆分析；
- 多屏幕系统算子；
- S 曲线与 TESE；
- 关键问题选择。

入口：[`modern_problem_identification.md`](open-deep-mind/triz/resources/modern_problem_identification.md)

### B. 经典矛盾体系 / Classical Contradiction System

完整包含：

- [`39_parameters.md`](open-deep-mind/triz/resources/39_parameters.md) — 39 个典型工程参数；
- [`40_principles.md`](open-deep-mind/triz/resources/40_principles.md) — 40 个发明原理；
- [`contradiction_matrix.json`](open-deep-mind/triz/resources/contradiction_matrix.json) — 完整 39×39 矛盾矩阵转录，1190 个有内容单元；
- [`contradictions.md`](open-deep-mind/triz/resources/contradictions.md) — 基础/反向工程矛盾、物理矛盾与次生矛盾；
- [`separation_principles.md`](open-deep-mind/triz/resources/separation_principles.md) — 时间、空间、条件、系统层级分离。

矩阵不是证明工具。矩阵单元只提供历史统计型搜索方向；具体参数映射、机制和方案仍需工程核验。

### C. Su-Field 与完整 76 标准解

- [`substance_field_modeling.md`](open-deep-mind/triz/resources/substance_field_modeling.md) — 不完整、不足、有害、测量物场模型；
- [`76_standard_solutions.md`](open-deep-mind/triz/resources/76_standard_solutions.md) — **全部 76 项**，按公开 MATRIZ 五类编号组织：

```text
Class 1 = 13
Class 2 = 23
Class 3 = 6
Class 4 = 17
Class 5 = 17
Total   = 76
```

### D. ARIZ-85C

[`ariz_85c.md`](open-deep-mind/triz/resources/ariz_85c.md) 按 9 Part / 3 Block 结构建立深度求解路线：

```text
Block 1 — 重构原始问题
Part 1  系统与问题分析
Part 2  操作区 / 操作时间 / 物场资源
Part 3  IFR 与物理矛盾

Block 2 — 消除物理矛盾
Part 4  分离与资源
Part 5  标准解 / 科学效应 / 知识库
Part 6  改变 mini-problem

Block 3 — 分析并推广解
Part 7  检查矛盾是否真正解决
Part 8  系统 / 超系统扩展
Part 9  对求解过程本身复盘
```

### E. IFR、理想度与资源

[`ideality_ifr_resources.md`](open-deep-mind/triz/resources/ideality_ifr_resources.md) 区分：

- Ideal System；
- Ideal Final Result；
- 相对理想度；
- substance / field / space / time / information / functional / supersystem / harmful / void resources。

不在量纲和权重不成立时伪造精确 ideality 分数。

### F. FOS、科学效应与跨域迁移

- [`effects_and_fos.md`](open-deep-mind/triz/resources/effects_and_fos.md) — Function-Oriented Search 和科学效应搜索；
- [`clone_problems.md`](open-deep-mind/triz/resources/clone_problems.md) — 克隆问题的结构迁移；
- [`feature_transfer.md`](open-deep-mind/triz/resources/feature_transfer.md) — 从竞争/替代系统转移优势机制；
- [`innovative_benchmarking.md`](open-deep-mind/triz/resources/innovative_benchmarking.md) — 工况归一化的创新标杆分析。

模块**不伪造一个“万能科学效应数据库”**。实际 FOS / effects 任务需要联网检索当前专利、论文、标准、产品与科学效应资料，并保留来源。

### G. S-curve 与现代 TESE

- [`s_curve_and_tese.md`](open-deep-mind/triz/resources/s_curve_and_tese.md)
- [`evolution_trends.md`](open-deep-mind/triz/resources/evolution_trends.md)

不仅保留经典“8 大趋势”概括，还按公开 MATRIZ 当前层级组织：

- S 曲线；
- increasing value；
- transition to supersystem；
- increasing trimming；
- increasing completeness；
- decreasing human involvement；
- flow enhancement；
- increasing coordination；
- increasing controllability；
- increasing dynamization；
- uneven subsystem development。

这些是**进化假设生成器**，不是决定论式未来预测。

### H. 概念论证 / Concept Substantiation

TRIZ 的输出状态首先只能是：

```text
TRIZ-derived concept
```

随后进入 [`concept_substantiation.md`](open-deep-mind/triz/resources/concept_substantiation.md) 和 OpenDeepMind 第一性原理质量门，检查：

- 控制方程、量纲和数量级；
- 材料与工艺可行性；
- 参数来源；
- 初值、边界、闭合和适用域；
- 不确定性与敏感性；
- 安全、法规、可靠性与生命周期；
- 仿真、实验、原型与 FMEA；
- 竞争方案和证伪条件；
- 必要时的专利/现有技术检索。

**“命中某个 TRIZ 原理”绝不等于“方案已验证”。**

---

## TRIZ T0–T10 路由

```text
T0  明确调用与作用域
T1  系统 / 子系统 / 超系统 / 主功能 / 约束
T2  识别真正关键问题
T3  资源 + baseline ideality + IFR
T4  工程矛盾 / 物理矛盾 / Su-Field / function problem
T5  选择 matrix / separation / SIS / ARIZ / FOS-effects / TESE
T6  生成结构不同的概念族
T7  将抽象原理翻译为具体材料 / 几何 / 场 / 时间 / 控制机制
T8  物理 / 安全 / 制造 / 集成硬门
T9  设计最小判别计算 / 仿真 / 实验 / 原型
T10 返回 First Principles 与 OpenDeepMind Quality Gate
```

---

## TRIZ 工具 / Deterministic TRIZ Tools

### 矛盾矩阵查询

```bash
python open-deep-mind/triz/scripts/lookup_matrix.py \
  --improve 10 --worsen 17
```

JSON 输出：

```bash
python open-deep-mind/triz/scripts/lookup_matrix.py \
  --improve 10 --worsen 17 --json
```

### 完整模块校验

```bash
python open-deep-mind/triz/scripts/validate_triz_module.py
```

校验器检查：

- 25 项 TRIZ 资源文件；
- 39 个参数 ID 是否完整；
- 40 个原理 ID 是否完整；
- 矛盾矩阵 JSON、1190 个有内容单元、参数/原理范围和锚点单元；
- 76 个标准解及 `13 + 23 + 6 + 17 + 17` 类别分布；
- ARIZ 9 Parts；
- opt-in 路由；
- 模块地图；
- Python 语法与示例存在性。

---

## TRIZ 案例 / TRIZ Examples

- [`brake_disc.md`](open-deep-mind/triz/examples/brake_disc.md) — 制动盘热衰退与热管理；
- [`battery_pack.md`](open-deep-mind/triz/examples/battery_pack.md) — 电池能量密度与热安全；
- [`heat_exchanger_fouling.md`](open-deep-mind/triz/examples/heat_exchanger_fouling.md) — 石化换热器结垢；
- [`anti_example_misframed.md`](open-deep-mind/triz/examples/anti_example_misframed.md) — 非工程问题拒绝 / reframe。

完整输出模板：[`output_template.md`](open-deep-mind/triz/resources/output_template.md)

---

## “第一”必须说明相对于哪个层级 / Firstness Is Level-Relative

某个原理可以是一个模型的基础，同时又是另一套更低层理论的推导结果。任何跨尺度结论都必须声明映射、闭合、信息损失、参数来源、不确定性和验证域。

```math
x_{\mathrm{low}}
\xrightarrow[\text{uncertainty}]{\text{mapping + closure}}
z_{\mathrm{effective}}
\xrightarrow[\text{validation}]{\text{higher-scale model}}
y_{\mathrm{observable}}
```

TRIZ 概念也必须遵守这个尺度桥规则。

---

## 竞争模型与证伪 / Competing Models and Falsification

OpenDeepMind 不允许只构造一个顺畅故事。标准模式至少保留：

- 当前主模型；
- 一个结构不同的严肃竞争模型；
- 不采取行动的基线；
- 能区分模型的观测、实验或现实事件。

```math
M^{*}=\arg\max_M
\left[
\operatorname{Evidence}(M)
-\lambda_1\operatorname{Bias}(M)
-\lambda_2\operatorname{Complexity}(M)
-\lambda_3\operatorname{UnresolvedRisk}(M)
\right]
```

TRIZ 生成的概念同样必须具有竞争方案、验证实验和证伪条件。

---

## 质量门 / Quality Gates

### 红色阻断项

出现任何一项，不得用高分、漂亮图表或流畅措辞掩盖：

- 核心术语未定义或前后变义；
- 关键事实没有可靠来源；
- 结论不由前提推出；
- 把相关性写成因果性；
- 把模型输出写成直接观测；
- 未建立尺度桥就跨尺度下结论；
- 没有严肃竞争模型或证伪条件；
- 隐藏目标函数、价值权重或利益相关者；
- 未核验就删除法律、安全或伦理保护；
- 虚构文献、数据、实验、引文或共识。

### 100 分推理质量

```math
Q=\sum_{i=1}^{12}w_i s_i-\lambda B,
\qquad B>0\Rightarrow\text{reject delivery}
```

完整规则：[`quality-gates.md`](open-deep-mind/references/quality-gates.md)

---

## 领域路由 / Domain Routing

| 领域 | 默认重点 |
|---|---|
| 科学研究 | 测量、机理、竞争模型、前瞻预测与判别实验 |
| 工程 | 功能、硬约束、故障、制造、运维、可逆性与安全余量 |
| 数理建模 | 控制方程、闭合关系、参数、初边值、收敛与不确定性 |
| 软件架构 | 功能、接口、故障、团队和系统约束；默认不用 TRIZ |
| 商业战略 | 价值机制、经济性、竞争响应、实物期权与退出条件 |
| 政策法律伦理 | 权限、权利、证据、分配、申诉、责任机制 |
| 个人决策 | 真实价值、观察行为、可逆试验与复审触发器 |
| 创意与产品 | 张力、结构性新颖、效用与价值验证 |
| AI 协作 | 任务边界、证据来源、反幻觉、可审计推导与责任归属 |

跨领域总规则：**采用涉及领域中最严格的证据、安全、法律和伦理标准。**

完整路由：[`domain-routing.md`](open-deep-mind/references/domain-routing.md)

---

## 方法图谱 / Method Atlas

仓库提供三十余种通用方法卡。TRIZ 从通用方法图谱中拆出为完整专业子系统，因此**不属于默认方法组合**。

```math
\text{Default}
=
\text{foundation audit}
+\text{causal/mechanism map}
+\text{constructive synthesis}
+\text{adversarial test}
+\text{evidence calibration}
```

只有满足显式调用条件后才进入 TRIZ。

完整图谱：[`method-atlas.md`](open-deep-mind/references/method-atlas.md)

---

## 安装 / Installation

```bash
git clone https://github.com/SUNHAOJUN22/OpenDeepMind_skill.git
```

Skills CLI：

```bash
npx skills add SUNHAOJUN22/OpenDeepMind_skill --skill open-deep-mind
```

将 `open-deep-mind/` 放入目标 Agent 支持的 Skill 目录。核心方法与 TRIZ 校验/矩阵查询脚本均不依赖第三方 Python 包。

---

## 调用方式 / Invocation

### 中文双引擎深度模式

```text
调用 open-deep-mind，执行“第一哲学 → 第一性原理”双引擎深度分析。
先审查问题框架、定义、本体、证据、因果、边界、尺度和价值；
建立 D/O/L/C/A/E/V/U 命题账本；
从合格基础向上构造竞争模型；
输出证伪条件、不确定性、质量门、结论、下一项判别行动和复审触发器。
除非本请求明确要求 TRIZ，否则不要加载 TRIZ。
```

### 显式 TRIZ 工程模式

```text
显式调用 OpenDeepMind TRIZ 工程模块。
先由第一哲学/第一性原理核验系统边界、功能、证据、工况、硬约束和安全条件，
再读取 TRIZ_ENGINEERING.md 和 triz/README.md，按关键问题类型懒加载对应资源。
要求保留问题识别 → TRIZ 发明构造 → 第一性原理工程验证的完整链路；
不得把 TRIZ 原理名称当作物理验证。
```

### English TRIZ mode

```text
Explicitly invoke the OpenDeepMind TRIZ Engineering module.
Qualify the system, function, evidence, operating conditions and hard constraints first.
Then load only the TRIZ resources required by the selected key-problem model.
Generate structurally different inventive concepts, translate them into concrete mechanisms,
and return them to First Principles for physics, uncertainty, safety and discriminating tests.
```

---

## 输出契约 / Output Contract

普通 OpenDeepMind 输出至少包括：

```text
1. Reframed problem
2. Foundation Charter
3. Claim Ledger
4. Causal / mechanism / constraint model
5. Competing models
6. Derivation / evidence chain
7. Falsifiers
8. Uncertainty / validity domain
9. Quality gate / blockers
10. Decision
11. Next discriminating action
12. Review trigger
```

TRIZ 输出进一步使用 [`triz/resources/output_template.md`](open-deep-mind/triz/resources/output_template.md)，明确问题识别、IFR、资源、矛盾/物场、来源状态、具体机制、次生矛盾、概念论证与返回质量门状态。

---

## 仓库结构 / Repository Structure

```text
OpenDeepMind_skill/
├── README.md
├── AGENTS.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── SECURITY.md
├── LICENSE.md
├── NOTICE.md
├── CITATION.cff
├── .github/workflows/validate.yml
└── open-deep-mind/
    ├── SKILL.md
    ├── FIRST_PHILOSOPHY.md
    ├── FIRST_PRINCIPLES.md
    ├── TRIZ_ENGINEERING.md                # 轻量 opt-in 路由
    ├── triz/                              # 完整 TRIZ 子系统
    │   ├── README.md
    │   ├── VENDORED_LICENSE.md
    │   ├── resources/
    │   │   ├── modern_problem_identification.md
    │   │   ├── innovative_benchmarking.md
    │   │   ├── function_analysis.md
    │   │   ├── flow_analysis.md
    │   │   ├── cause_effect_chain.md
    │   │   ├── trimming.md
    │   │   ├── feature_transfer.md
    │   │   ├── multiscreen_operator.md
    │   │   ├── ideality_ifr_resources.md
    │   │   ├── contradictions.md
    │   │   ├── 39_parameters.md
    │   │   ├── 40_principles.md
    │   │   ├── contradiction_matrix.json
    │   │   ├── separation_principles.md
    │   │   ├── substance_field_modeling.md
    │   │   ├── 76_standard_solutions.md
    │   │   ├── ariz_85c.md
    │   │   ├── clone_problems.md
    │   │   ├── effects_and_fos.md
    │   │   ├── evolution_trends.md
    │   │   ├── s_curve_and_tese.md
    │   │   ├── concept_substantiation.md
    │   │   ├── glossary.md
    │   │   ├── output_template.md
    │   │   └── sources.md
    │   ├── examples/
    │   │   ├── brake_disc.md
    │   │   ├── battery_pack.md
    │   │   ├── heat_exchanger_fouling.md
    │   │   └── anti_example_misframed.md
    │   └── scripts/
    │       ├── lookup_matrix.py
    │       └── validate_triz_module.py
    ├── references/
    ├── assets/
    └── scripts/
```

---

## 验证 / Validation

```bash
python open-deep-mind/scripts/validate_repository.py .
python open-deep-mind/scripts/validate_ledger.py \
  open-deep-mind/assets/example-ledger.json
python open-deep-mind/triz/scripts/validate_triz_module.py
python open-deep-mind/triz/scripts/lookup_matrix.py \
  --improve 1 --worsen 3 --json
```

GitHub Actions 在 push / pull request 时运行同样的核心验证，并额外进行 TRIZ matrix lookup smoke test。

---

## 思想谱系、TRIZ 来源与归因 / Lineage and Attribution

本项目受到以下开放工作和理论传统启发：

- [`danyuchn/first-principles-skill`](https://github.com/danyuchn/first-principles-skill)；
- [`smixs/creative-director-skill`](https://github.com/smixs/creative-director-skill)；
- [`Antropocosmist/triz-engineering-solver`](https://github.com/Antropocosmist/triz-engineering-solver) — MIT；
- MATRIZ TRIZ Knowledge Base；
- Altshuller Institute；
- Genrich Altshuller 与经典 TRIZ 理论传统；
- Agent Skills 的渐进披露结构。

完整 TRIZ 模块中，39 参数、40 原理、矩阵等经典实现/数据层保留来源与 MIT 归因；OpenDeepMind 新增现代问题识别、完整 MATRIZ 编号 76 标准解操作索引、First Philosophy / First Principles 交接、渐进加载、概念论证、验证器和新案例。

详细来源：

- [`triz/resources/sources.md`](open-deep-mind/triz/resources/sources.md)
- [`triz/VENDORED_LICENSE.md`](open-deep-mind/triz/VENDORED_LICENSE.md)
- [`NOTICE.md`](NOTICE.md)
- [`intellectual-lineage.md`](open-deep-mind/references/intellectual-lineage.md)

---

## License

- 代码、脚本、Schema 与工作流：**Apache-2.0**；
- OpenDeepMind 原创方法文档与视觉资产：**CC BY 4.0**；
- `open-deep-mind/triz/` 中明确标注的适配/转录 TRIZ 资源遵循其保留的 **MIT** 来源许可和归因。

详见 [`LICENSE.md`](LICENSE.md)、[`NOTICE.md`](NOTICE.md) 与 [`triz/VENDORED_LICENSE.md`](open-deep-mind/triz/VENDORED_LICENSE.md)。

---

<p align="center">
  <strong>Foundation → Principle → Model → Invention → Test → Action → Revision</strong><br>
  <sub>开放基础，严格推导，选择性发明，允许证伪，持续修正。</sub>
</p>
