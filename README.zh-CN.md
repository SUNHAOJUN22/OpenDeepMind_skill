<p align="center">
  <img src="open-deep-mind/assets/diagrams/zh/hero.svg" alt="OpenDeepMind 中文方法总览" width="100%">
</p>

<h1 align="center">OpenDeepMind_skill</h1>

<p align="center">
  <strong>先审查什么有资格成为基础，再从基础向上推导、证伪、决策，并保留修正能力。</strong>
</p>

<p align="center">
  <a href="README.md">中英双语首页</a> ·
  <a href="open-deep-mind/SKILL.md">主 Skill</a> ·
  <a href="open-deep-mind/FIRST_PHILOSOPHY.md">第一哲学</a> ·
  <a href="open-deep-mind/FIRST_PRINCIPLES.md">第一性原理</a> ·
  <a href="open-deep-mind/TRIZ_ENGINEERING.md">TRIZ 路由</a> ·
  <a href="open-deep-mind/triz/README.md">完整 TRIZ 模块</a>
</p>

<p align="center">
  <img alt="版本" src="https://img.shields.io/badge/version-1.1.0-2a8cff?style=flat-square">
  <img alt="双引擎" src="https://img.shields.io/badge/core_engines-2-f2a649?style=flat-square">
  <img alt="TRIZ" src="https://img.shields.io/badge/optional_TRIZ-complete-e75f3c?style=flat-square">
  <img alt="矛盾矩阵" src="https://img.shields.io/badge/TRIZ_matrix-1190_cells-1565c0?style=flat-square">
  <img alt="标准解" src="https://img.shields.io/badge/TRIZ_SIS-76-7b61ff?style=flat-square">
  <img alt="依赖" src="https://img.shields.io/badge/runtime_dependencies-0-60758a?style=flat-square">
</p>

---

## 1. 核心架构

OpenDeepMind 仍然只有两个基础核心引擎：

```text
第一哲学 Φ
→ 第一性原理 P
→ 竞争模型
→ 证伪与质量门
→ 行动与修正
```

第一哲学负责回答：

> **什么有资格成为当前问题的基础？**

第一性原理负责回答：

> **在明确的领域、尺度、目的与条件下，从这些合格基础能够推出什么？**

独立核心文件：

- [`FIRST_PHILOSOPHY.md`](open-deep-mind/FIRST_PHILOSOPHY.md)
- [`FIRST_PRINCIPLES.md`](open-deep-mind/FIRST_PRINCIPLES.md)

TRIZ 不被提升为第三个基础引擎，而是一个**专业、独立、按需加载的工程发明子系统**。

---

## 2. TRIZ 默认不调用

默认流程不包含 TRIZ：

```text
Φ → P → 竞争模型 → 质量门
```

只有用户明确要求或明确接受以下路线时，才进入 TRIZ：

- TRIZ / ARIZ；
- 技术矛盾 / 物理矛盾；
- 39 参数、40 发明原理、矛盾矩阵；
- Su-Field / 物场、76 标准解；
- IFR / 理想最终结果；
- S 曲线、TESE、工程系统进化；
- 明确要求 TRIZ 工程创新分析。

完整显式路线：

```text
Φ/P 基础资格审查
→ TRIZ 发明构造 T
→ 第一性原理物理 / 数理 / 证据验证
→ OpenDeepMind 质量门
```

轻量入口：[`TRIZ_ENGINEERING.md`](open-deep-mind/TRIZ_ENGINEERING.md)  
完整子系统：[`open-deep-mind/triz/README.md`](open-deep-mind/triz/README.md)

---

## 3. 完整 TRIZ 模块包含什么

### 3.1 现代问题识别

不是一上来就查矩阵，而是先确定**真正关键问题**：

- 功能分析 / function-cost analysis；
- 物质、能量与信息流分析；
- CECA 因果链；
- 裁剪与部分裁剪；
- 特征迁移；
- 创新标杆分析；
- 多屏幕系统算子；
- S 曲线与 TESE；
- 关键问题路由。

主入口：[`modern_problem_identification.md`](open-deep-mind/triz/resources/modern_problem_identification.md)

### 3.2 经典矛盾体系

完整文件：

- [`39_parameters.md`](open-deep-mind/triz/resources/39_parameters.md) — 39 个典型工程参数；
- [`40_principles.md`](open-deep-mind/triz/resources/40_principles.md) — 40 个发明原理；
- [`contradiction_matrix.json`](open-deep-mind/triz/resources/contradiction_matrix.json) — 39×39 完整矩阵转录，1190 个有内容单元；
- [`contradictions.md`](open-deep-mind/triz/resources/contradictions.md) — 工程矛盾、反向矛盾、物理矛盾、次生矛盾；
- [`separation_principles.md`](open-deep-mind/triz/resources/separation_principles.md) — 时间、空间、条件、系统层级分离。

### 3.3 Su-Field 与全部 76 标准解

- [`substance_field_modeling.md`](open-deep-mind/triz/resources/substance_field_modeling.md)
- [`76_standard_solutions.md`](open-deep-mind/triz/resources/76_standard_solutions.md)

标准解按公开 MATRIZ 五类编号组织：

```text
Class 1 = 13
Class 2 = 23
Class 3 = 6
Class 4 = 17
Class 5 = 17
Total   = 76
```

### 3.4 ARIZ-85C

[`ariz_85c.md`](open-deep-mind/triz/resources/ariz_85c.md) 按 9 Part / 3 Block 组织，用于普通矩阵、分离、物场路线持续产生妥协或问题仍然模糊的深层工程问题。

### 3.5 理想度、IFR 与资源

[`ideality_ifr_resources.md`](open-deep-mind/triz/resources/ideality_ifr_resources.md) 明确区分：

- Ideal System；
- Ideal Final Result；
- 相对理想度；
- 物质、场、空间、时间、信息、功能、超系统、有害因素与空缺资源。

不在数据与量纲不成立时伪造精确“理想度”数字。

### 3.6 FOS、科学效应与迁移

- [`effects_and_fos.md`](open-deep-mind/triz/resources/effects_and_fos.md)
- [`feature_transfer.md`](open-deep-mind/triz/resources/feature_transfer.md)
- [`clone_problems.md`](open-deep-mind/triz/resources/clone_problems.md)
- [`innovative_benchmarking.md`](open-deep-mind/triz/resources/innovative_benchmarking.md)

真实任务中的科学效应、专利、论文和产品技术资料需要联网检索；模块不会虚构一个“万能科学效应数据库”。

### 3.7 S 曲线与现代 TESE

- [`s_curve_and_tese.md`](open-deep-mind/triz/resources/s_curve_and_tese.md)
- [`evolution_trends.md`](open-deep-mind/triz/resources/evolution_trends.md)

覆盖 S 曲线、MPV、价值提升、向超系统转移、裁剪、系统完整性、人参与减少、流强化、协调、可控性、动态化和子系统非均衡发展等现代进化路由。

### 3.8 概念论证

TRIZ 输出首先只能标记为：

```text
TRIZ-derived concept
```

随后进入 [`concept_substantiation.md`](open-deep-mind/triz/resources/concept_substantiation.md) 和 OpenDeepMind 第一性原理质量门，检查物理、材料、制造、参数来源、不确定性、安全、可靠性、生命周期、仿真、实验、原型、FMEA 和专利现有技术等。

**TRIZ 原理名称、矩阵单元或标准解编号永远不等于工程验证。**

---

## 4. TRIZ T0–T10

```text
T0  明确显式调用与工程作用域
T1  系统 / 子系统 / 超系统 / 主功能 / 约束
T2  识别真正关键问题
T3  资源 + baseline ideality + IFR
T4  工程矛盾 / 物理矛盾 / Su-Field / function problem
T5  选择 matrix / separation / SIS / ARIZ / FOS-effects / TESE
T6  生成结构不同的概念族
T7  把 TRIZ 抽象原理翻译为具体材料 / 几何 / 场 / 时间 / 控制机制
T8  物理 / 安全 / 制造 / 集成硬门
T9  最小判别计算 / 仿真 / 实验 / 原型
T10 返回 First Principles 与 OpenDeepMind Quality Gate
```

---

## 5. 矩阵查询与模块验证

确定性矩阵查询：

```bash
python open-deep-mind/triz/scripts/lookup_matrix.py \
  --improve 10 --worsen 17
```

完整 TRIZ 模块校验：

```bash
python open-deep-mind/triz/scripts/validate_triz_module.py
```

校验器检查 25 项 TRIZ 资源、39 参数、40 原理、矩阵单元与锚点、76 标准解类分布、ARIZ 9 Parts、TRIZ opt-in 路由、脚本语法和案例完整性。

GitHub Actions 已把 TRIZ 校验和矩阵查询 smoke test 加入主 CI。

---

## 6. TRIZ 工程案例

- [`brake_disc.md`](open-deep-mind/triz/examples/brake_disc.md) — 制动盘热管理；
- [`battery_pack.md`](open-deep-mind/triz/examples/battery_pack.md) — EV 电池热安全；
- [`heat_exchanger_fouling.md`](open-deep-mind/triz/examples/heat_exchanger_fouling.md) — 石化换热器结垢；
- [`anti_example_misframed.md`](open-deep-mind/triz/examples/anti_example_misframed.md) — 非工程问题拒绝 / reframe。

输出模板：[`output_template.md`](open-deep-mind/triz/resources/output_template.md)

---

## 7. 证据、尺度与质量门

所有 OpenDeepMind 模块共同遵守：

```math
\text{模型输出}\neq\text{直接观测}
```

```math
\text{相关性}\neq\text{干预因果}\neq\text{物理机制}
```

任何跨尺度结论都必须给出：

```text
映射变量
闭合 / 粗粒化假设
信息损失
参数来源
不确定性传播
验证域
失效条件
```

TRIZ 只负责拓展/重构发明空间，不豁免这些要求。

---

## 8. 调用示例

### 普通 OpenDeepMind

```text
调用 open-deep-mind，执行第一哲学 → 第一性原理双引擎分析。
除非我明确要求 TRIZ，否则不要加载 TRIZ。
```

### 完整 TRIZ

```text
显式调用 OpenDeepMind TRIZ 工程模块。
先用第一哲学/第一性原理核验系统、功能、工况、证据、边界、硬约束与安全条件；
再读取 TRIZ_ENGINEERING.md 和 triz/README.md，按关键问题类型懒加载所需资源。
必须完成问题识别 → 发明构造 → 工程验证链，不能把 TRIZ 原理名称当作物理证明。
```

---

## 9. 验证

```bash
python open-deep-mind/scripts/validate_repository.py .
python open-deep-mind/scripts/validate_ledger.py \
  open-deep-mind/assets/example-ledger.json
python open-deep-mind/triz/scripts/validate_triz_module.py
python open-deep-mind/triz/scripts/lookup_matrix.py \
  --improve 1 --worsen 3 --json
```

---

## 10. 来源与许可

完整来源和证据图谱：

- [`open-deep-mind/triz/resources/sources.md`](open-deep-mind/triz/resources/sources.md)
- [`open-deep-mind/triz/VENDORED_LICENSE.md`](open-deep-mind/triz/VENDORED_LICENSE.md)
- [`NOTICE.md`](NOTICE.md)
- [`intellectual-lineage.md`](open-deep-mind/references/intellectual-lineage.md)

TRIZ 经典实现/数据层保留 `Antropocosmist/triz-engineering-solver` 的 MIT 归因及其矩阵转录来源链；现代问题识别、完整 MATRIZ 编号 76 标准解操作索引、OpenDeepMind 交接、渐进加载、概念论证、验证脚本和新案例在本仓库中重新组织和撰写。

OpenDeepMind_skill 与 Google DeepMind、MATRIZ、Altshuller Institute、OpenAI、Anthropic 及引用仓库维护者均无隶属或背书关系。

---

<p align="center">
<strong>基础资格 → 第一性原理 → 选择性 TRIZ 发明 → 物理验证 → 质量门 → 行动与修正</strong>
</p>
