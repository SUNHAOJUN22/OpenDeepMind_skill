# TRIZ Engineering Module / TRIZ 工程发明模块

> **Status: optional, opt-in, and separate from First Principles.**  
> This file is **not** part of the default `Φ → P` OpenDeepMind route. Do not load or apply it unless the user explicitly requests TRIZ or explicitly accepts a TRIZ route after it is suggested.

TRIZ is used here as a specialist module for **engineering invention and contradiction resolution**. It does not replace [FIRST_PHILOSOPHY.md](FIRST_PHILOSOPHY.md), [FIRST_PRINCIPLES.md](FIRST_PRINCIPLES.md), physical modeling, experiment, safety review, or professional engineering judgment.

---

## 0. Activation contract

### Load this module only when one of the following is explicit

- the user says `TRIZ`, `ARIZ`, `矛盾矩阵`, `40个发明原理`, `物场分析`, `Su-Field`, `理想最终结果`, `IFR`, `技术系统进化`, or equivalent;
- the user explicitly asks for a non-compromise inventive solution to a verified engineering contradiction;
- the user explicitly accepts a proposed TRIZ route after OpenDeepMind identifies a candidate technical or physical contradiction.

### Do not load it merely because

- the problem is difficult;
- the word “contradiction” appears in ordinary language;
- the user requests creativity or brainstorming;
- an optimization has trade-offs;
- the task concerns business, organization, policy, ethics, UX, or pure software architecture;
- a physical analogy can be invented after the fact.

**Hard rule:** detecting a possible contradiction is permission to **suggest** TRIZ once, not permission to execute it. The default route remains First Philosophy and/or First Principles.

### Canonical scope

Use TRIZ directly for:

- physical or technical engineering systems;
- measurable functions, effects, resources, fields, parameters, and constraints;
- technical contradictions: improving one parameter worsens another;
- physical contradictions: one parameter of one element requires opposing states;
- harmful, insufficient, excessive, or incomplete substance–field interactions;
- invention problems where conventional optimization has plateaued;
- explicit technology-evolution or S-curve roadmapping requests.

### Analogical scope

For software, service, management, or strategy problems, TRIZ may be used only when the user explicitly requests an **analogical** adaptation. Label the result:

```text
TRIZ status: analogical transfer, not canonical engineering TRIZ
```

Do not use a metaphorical mapping as engineering proof.

---

## 1. Relationship to the OpenDeepMind core

TRIZ is an optional specialist module, not a third foundational engine.

```text
Default:
First Philosophy (Φ) → First Principles (P) → rival models → quality gate

Explicit TRIZ route:
Φ/P qualification → TRIZ inventive synthesis (T) → P-based validation → quality gate
```

### Handoff into TRIZ

Before TRIZ begins, transfer:

- stable definitions;
- system, subsystem, and supersystem boundaries;
- main useful function;
- harmful or insufficient effect;
- verified physical constraints;
- current solution mechanism;
- evidence and measurement conditions;
- values, safety limits, and non-negotiable duties;
- unknowns that may invalidate the contradiction.

### Handoff out of TRIZ

TRIZ produces **inventive concepts and mechanism hypotheses**. Send them back to First Principles for:

- governing-equation or constraint checks;
- material and manufacturing feasibility;
- dimensional consistency;
- parameter provenance;
- uncertainty and sensitivity;
- safety, legal, ethical, and lifecycle review;
- prototype, simulation, or experiment design;
- competing-model and falsification analysis.

A TRIZ principle is a search direction, not evidence that a concept works.

---

## 2. TRIZ theory map

TRIZ is best understood as a layered system rather than as the contradiction matrix alone.

| Layer | Primary question | Typical tools |
|---|---|---|
| Problem identification | Which disadvantage is the right one to solve? | function analysis, flow analysis, cause–effect chain analysis, trimming, feature transfer |
| Problem modeling | What is the conflict or defective interaction? | engineering contradiction, physical contradiction, Su-Field model, mini-problem |
| Direction of invention | What would a more ideal result look like? | ideality, Ideal Final Result, resource analysis |
| Concept generation | Which generic transformation may resolve it? | 40 inventive principles, contradiction matrix, separation principles, scientific effects |
| Deep problem solving | How do we sharpen a stubborn problem? | ARIZ-85C, operational zone/time, substance–field resources |
| System evolution | Where might the system develop next? | S-curve, trends of engineering-system evolution, supersystem transition |
| Substantiation | Does the concept survive reality? | physical model, simulation, experiment, FMEA, patent and manufacturability review |

### Classical and modern practice

- Classical TRIZ commonly starts from contradictions, 39 typical parameters, 40 inventive principles, Su-Field models, 76 standard inventive solutions, and ARIZ.
- Modern MATRIZ practice places greater emphasis on finding the **right key problem** first through function, flow, cause–effect, trimming, feature-transfer, S-curve, and evolution analysis.
- The contradiction matrix is a heuristic access mechanism to principles, not an exhaustive solver.
- Modern MATRIZ notes that classical substance–field analysis is less commonly used for identifying the problem after cause–effect analysis, although Su-Field models and standard inventive solutions remain useful solution-modeling tools.

---

## 3. Core concepts

### 3.1 Engineering system

An engineering system is an intentionally developed system that performs a function. Describe it at three levels:

```text
subsystem ↔ analyzed system ↔ supersystem
```

Do not treat the current component structure as necessary. Functions may be reassigned, trimmed, or transferred to the supersystem.

### 3.2 Function

Represent a function as:

```text
function carrier → action → function object
```

Classify the interaction as:

- useful and sufficient;
- useful but insufficient;
- useful but excessive;
- harmful;
- missing/incomplete;
- measurement or detection.

### 3.3 Key disadvantage and key problem

A visible symptom is not automatically the key problem. Build a branched cause–effect chain and select a disadvantage whose elimination materially advances the project goal.

```text
observed symptom
├── cause chain A
├── cause chain B
└── feedback / vicious circle
```

The selected key problem must remain connected to evidence, not only to a plausible story.

### 3.4 Engineering contradiction

An engineering contradiction, also called a technical contradiction, involves two parameters:

> An attempt to improve parameter `A` through a particular approach causes parameter `B` to deteriorate.

Use the `IF–THEN–BUT` form:

```text
IF    [a proposed action or state is introduced],
THEN  [the desired parameter improves],
BUT   [another justified parameter worsens].
```

Formulate the inverted contradiction as well. The contradiction matrix is directional and not symmetric.

### 3.5 Physical contradiction

A physical contradiction places two justified opposing requirements on **one parameter of one element**:

```text
Element X must have property A under requirement R1,
and must have property not-A under requirement R2.
```

The contradiction is not “two stakeholders disagree.” It must refer to an engineering parameter or state whose opposing requirements have physical or functional justification.

### 3.6 Ideality

TRIZ seeks increasing useful function with decreasing harm and cost. Use ideality comparatively:

\[
I=\frac{\sum U}{\sum H+\sum C}
\]

where:

- `U` = useful functions/effects;
- `H` = harmful functions/effects;
- `C` = resource, complexity, energy, material, maintenance, risk, and lifecycle costs.

Prefer the change relative to baseline:

\[
\Delta I=I_{\mathrm{concept}}-I_{\mathrm{baseline}}
\]

Do not fabricate exact ideality numbers. When inputs are not commensurable, report a qualitative band and the reasons.

### 3.7 Ideal Final Result and ideal system

These are not identical.

- **Ideal Final Result (IFR):** the specific problem is eliminated with minimal system change and without deterioration of relevant parameters.
- **Ideal system:** the desired function is delivered with vanishing components and costs—the system tends toward “not existing” while its function remains.

A practical IFR form is:

```text
The available system resource itself performs [required function]
in [operational zone] during [operational time],
while preserving [useful effect] and eliminating [harmful effect],
without adding unacceptable complexity, cost, or risk.
```

### 3.8 Resources

Inventory resources before adding components:

| Resource class | Examples |
|---|---|
| Substance | components, coatings, particles, waste streams, voids, byproducts |
| Field | mechanical, acoustic, thermal, chemical, electrical, magnetic/electromagnetic |
| Space | cavities, surfaces, interfaces, gradients, unused geometry |
| Time | pre-action, pulse, delay, idle period, post-action, sequencing |
| Information | existing signals, noise, state variables, measurement history |
| Functional | idle or duplicated functions, self-service, feedback |
| Supersystem | environment, adjacent equipment, gravity, ambient heat, infrastructure |
| Harmful resource | heat, vibration, pressure, waste, friction, contamination that may be redirected |

A “free resource” is not cost-free in every sense. Verify safety, availability, variability, and control.

---

## 4. T10 opt-in workflow

### T0 — Confirm activation and scope

Record:

```text
Activation phrase:
Canonical engineering TRIZ or analogical transfer:
System and primary function:
Decision/deliverable:
```

If the problem is outside canonical scope, refuse or reframe instead of forcing a TRIZ interpretation.

### T1 — Establish the engineering brief

Collect or responsibly infer:

```text
System / subsystem / supersystem:
Main useful function:
Target object:
Current mechanism:
Undesired effect or limitation:
Measured conditions:
Hard constraints:
Allowed degree of change:
Available resources:
Safety and lifecycle constraints:
```

Do not proceed with invented measurements or placeholder constraints.

### T2 — Identify the right problem

Use only the tools materially needed:

1. function model;
2. flow model for substance, energy, or information;
3. cause–effect chain analysis;
4. trimming test;
5. feature-transfer comparison;
6. key-disadvantage selection.

**Trimming test:** remove a component only if its useful functions can be eliminated, reassigned, or performed by the remaining system or supersystem without violating hard constraints.

### T3 — Formulate the IFR and baseline ideality

Define:

- baseline useful effects;
- baseline harmful effects;
- baseline cost/complexity;
- IFR;
- the gap between current state and IFR.

The IFR guides the search; it does not waive physics, regulation, or safety.

### T4 — Formulate contradictions

Produce:

1. base engineering contradiction;
2. inverted engineering contradiction;
3. physical contradiction when one element carries opposite requirements;
4. operational zone and operating time if localization matters.

Reject contradictions created only by vague adjectives such as “better,” “smart,” or “efficient.” Map them to measurable parameters.

### T5 — Select the TRIZ route

```text
IF explicit technology-roadmap question:
    use S-curve + engineering-system evolution trends
ELSE IF complex mini-problem and quick methods fail:
    use ARIZ-85C
ELSE IF one parameter needs opposite states:
    use physical-contradiction separation
ELSE IF improving one parameter worsens another:
    use typical parameters + contradiction matrix + inventive principles
ELSE IF interaction is incomplete, insufficient, excessive, harmful, or measurement-related:
    use Su-Field model + standard inventive solutions
ELSE:
    return to First Principles; do not force TRIZ
```

### T6 — Generate concept families

Generate at least three structurally distinct concept families, where practical:

- one low-change/resource-reuse concept;
- one contradiction-separation concept;
- one mechanism or field-change concept;
- optionally one supersystem or trimming concept;
- optionally one high-risk frontier concept.

Every concept must identify:

```text
TRIZ route:
Principle / separation / standard / trend:
Mechanism:
Resource used:
Contradiction resolved:
New contradiction introduced:
Expected ideality change:
Validation requirement:
```

### T7 — Translate principles into mechanisms

Do not output principle names as solutions. Translate each principle into:

```text
principle
→ concrete change to geometry/material/field/timing/control
→ altered interaction or mechanism
→ predicted useful and harmful effects
```

Reject “use segmentation,” “add feedback,” or “make it dynamic” unless the engineering implementation is stated.

### T8 — Screen and rank concepts

First apply hard gates:

- physical feasibility;
- safety;
- legal/regulatory constraints;
- material compatibility;
- manufacturability;
- operating envelope;
- lifecycle and maintainability;
- no hidden scale jump.

Then compare:

\[
S_j=w_I\Delta I_j+w_RR_j+w_FF_j-w_UU_j-w_KK_j
\]

where:

- `ΔI` = relative ideality improvement;
- `R` = reuse of available resources;
- `F` = feasibility and controllability;
- `U` = uncertainty;
- `K` = safety, implementation, and secondary-contradiction risk.

Weights must be explicit. Do not let a score override a hard blocker.

### T9 — Define discriminating validation

For each leading concept specify the smallest useful next test:

- calculation or governing-equation check;
- material compatibility test;
- multiphysics simulation;
- benchtop experiment;
- prototype;
- accelerated aging;
- FMEA or hazard analysis;
- patent/novelty search;
- manufacturability and cost estimate.

State what result would reject or materially weaken the concept.

### T10 — Return to OpenDeepMind

Hand the shortlisted concepts back to the normal quality gate. A concept is not “validated” merely because it matches a TRIZ pattern or historical patent pattern.

---

## 5. Engineering contradiction route

### 5.1 Map to typical parameters

The classical matrix uses 39 generalized parameters. A specific variable may map to more than one typical parameter; explore multiple justified mappings rather than pretending there is one mechanically correct translation.

| # | Typical parameter / 典型参数 | # | Typical parameter / 典型参数 |
|---:|---|---:|---|
| 1 | Weight of moving object / 移动物体重量 | 21 | Power / 功率 |
| 2 | Weight of stationary object / 静止物体重量 | 22 | Loss of energy / 能量损失 |
| 3 | Length of moving object / 移动物体长度 | 23 | Loss of substance / 物质损失 |
| 4 | Length of stationary object / 静止物体长度 | 24 | Loss of information / 信息损失 |
| 5 | Area of moving object / 移动物体面积 | 25 | Loss of time / 时间损失 |
| 6 | Area of stationary object / 静止物体面积 | 26 | Quantity of substance / 物质量 |
| 7 | Volume of moving object / 移动物体体积 | 27 | Reliability / 可靠性 |
| 8 | Volume of stationary object / 静止物体体积 | 28 | Measurement accuracy / 测量精度 |
| 9 | Speed / 速度 | 29 | Manufacturing precision / 制造精度 |
| 10 | Force or intensity / 力或作用强度 | 30 | Object-affected harmful factor / 外部有害因素作用 |
| 11 | Stress or pressure / 应力或压力 | 31 | Object-generated harmful factor / 系统产生的有害因素 |
| 12 | Shape / 形状 | 32 | Ease of manufacture / 制造便利性 |
| 13 | Stability of composition / 组成稳定性 | 33 | Ease of operation / 操作便利性 |
| 14 | Strength / 强度 | 34 | Ease of repair / 维修便利性 |
| 15 | Duration of moving-object action / 移动物体作用持续时间 | 35 | Adaptability or versatility / 适应性或通用性 |
| 16 | Duration of stationary-object action / 静止物体作用持续时间 | 36 | Device complexity / 装置复杂性 |
| 17 | Temperature / 温度 | 37 | Difficulty of detection / 检测难度 |
| 18 | Illumination intensity / 光照强度 | 38 | Extent of automation / 自动化程度 |
| 19 | Energy use by moving object / 移动物体能耗 | 39 | Productivity / 生产率 |
| 20 | Energy use by stationary object / 静止物体能耗 |  |  |

### 5.2 Use the contradiction matrix correctly

- Row: parameter to improve.
- Column: parameter that worsens.
- The matrix is not symmetric.
- Principles in a cell are statistically frequent historical directions, not proof, ranking, or exhaustive options.
- Principle order inside a cell is not a priority order.
- An empty cell means no principle was statistically dominant; it does not mean no solution exists.
- If exact matrix data are not locally available, reason over all 40 principles and label the route `direct-principle search`, not `matrix-derived`.

This module deliberately does **not** reproduce a full 39×39 matrix. For a licensed structured matrix implementation, see the MIT-licensed source repository listed in the references section and preserve its attribution and provenance.

---

## 6. The 40 inventive principles

Each principle is a transformation prompt, not a complete design.

| # | Principle / 原理 | Engineering prompt / 工程提示 |
|---:|---|---|
| 1 | Segmentation / 分割 | Divide into independent, replaceable, graded, or controllable parts. |
| 2 | Taking out / 抽取 | Separate the harmful part or isolate only the useful property. |
| 3 | Local quality / 局部质量 | Make different regions perform different functions under local conditions. |
| 4 | Asymmetry / 非对称 | Replace uniform symmetry with load-, flow-, or direction-adapted asymmetry. |
| 5 | Merging / 合并 | Combine similar objects or operations in space or time. |
| 6 | Universality / 多用性 | Let one component perform several functions and remove redundant parts. |
| 7 | Nested doll / 嵌套 | Place one object inside another or use cavities and telescoping structures. |
| 8 | Anti-weight / 反重量 | Counteract weight with buoyancy, lift, suspension, or balancing forces. |
| 9 | Preliminary anti-action / 预先反作用 | Introduce a compensating action before the expected harm occurs. |
| 10 | Preliminary action / 预先作用 | Perform the needed change, placement, or preparation in advance. |
| 11 | Beforehand cushioning / 预先防护 | Prepare backup, buffering, or damage-limiting means before failure. |
| 12 | Equipotentiality / 等势 | Remove unnecessary work against a potential gradient. |
| 13 | The other way round / 反向 | Reverse the action, orientation, motion, or active/passive role. |
| 14 | Curvature / 曲面化 | Replace straight or planar forms with curves, spheres, rollers, or rotation. |
| 15 | Dynamics / 动态化 | Make geometry, properties, or connections adjustable by operating state. |
| 16 | Partial or excessive action / 未达到或过度作用 | Overshoot or undershoot when exact action is difficult, then correct. |
| 17 | Another dimension / 多维化 | Use additional dimensions, layers, orientations, or the opposite surface. |
| 18 | Mechanical vibration / 机械振动 | Use oscillation, resonance, ultrasound, or frequency control. |
| 19 | Periodic action / 周期性作用 | Replace continuous action with pulses, cycles, or controlled pauses. |
| 20 | Continuity of useful action / 有效作用连续性 | Eliminate idle states and keep useful functions operating continuously. |
| 21 | Skipping / 快速通过 | Pass rapidly through a harmful or unstable regime. |
| 22 | Convert harm into benefit / 变害为利 | Redirect, combine, or amplify a harmful factor until it becomes useful. |
| 23 | Feedback / 反馈 | Sense output or state and adapt the action. |
| 24 | Intermediary / 中介 | Introduce a temporary carrier, converter, interface, or transferable medium. |
| 25 | Self-service / 自服务 | Make the system maintain, clean, calibrate, or protect itself using its own resources. |
| 26 | Copying / 复制 | Replace a costly or inaccessible object with a model, image, signal, or surrogate. |
| 27 | Cheap short-living objects / 廉价短寿命 | Replace one durable expensive element with disposable or renewable low-cost elements. |
| 28 | Mechanics substitution / 机械系统替代 | Replace mechanical action with optical, acoustic, electrical, magnetic, or other fields. |
| 29 | Pneumatics and hydraulics / 气压与液压 | Use gas or liquid structures, pressure, jets, cushions, or fluidic control. |
| 30 | Flexible shells and thin films / 柔性壳与薄膜 | Replace bulky structures with membranes, films, skins, or flexible barriers. |
| 31 | Porous materials / 多孔材料 | Introduce, grade, fill, or exploit pores and capillary structure. |
| 32 | Color changes / 颜色改变 | Change optical properties, contrast, transparency, emissivity, or indication. |
| 33 | Homogeneity / 同质性 | Match interacting materials or properties to reduce incompatibility. |
| 34 | Discarding and recovering / 抛弃与再生 | Remove fulfilled parts or regenerate consumed elements during operation. |
| 35 | Parameter changes / 参数改变 | Change state, concentration, density, flexibility, temperature, or another controllable parameter. |
| 36 | Phase transitions / 相变 | Use latent heat, volume change, solubility, crystallization, or phase-boundary effects. |
| 37 | Thermal expansion / 热膨胀 | Use differential expansion, contraction, or bimetal-like response. |
| 38 | Strong oxidants / 强氧化剂 | Intensify oxidation or use higher-reactivity media when justified and safe. |
| 39 | Inert atmosphere / 惰性环境 | Use inert, vacuum, neutral, or protective environments/additives. |
| 40 | Composite materials / 复合材料 | Replace homogeneous material with a designed multi-material architecture. |

For every selected principle ask:

```text
What physical change does this imply?
Which interaction changes?
Which resource enables it?
What new harm or contradiction appears?
How will the change be tested?
```

---

## 7. Physical contradiction route

Test separation in this order unless the problem suggests otherwise:

| Separation axis | Question | Typical implementation families |
|---|---|---|
| Time / 时间 | Can opposite states occur at different times? | pulsing, sequencing, retracting, pre-action, duty cycling |
| Space / 空间 | Can opposite states exist in different regions? | gradients, layers, local quality, segmentation, interfaces |
| Condition / 条件 | Can the state switch according to load, temperature, field, concentration, or phase? | smart materials, thresholds, feedback, phase transition |
| System level / 系统层级 | Can parts have one property while the whole has the opposite, or can the supersystem carry a function? | composites, nested systems, modularity, distributed functions |

A separation concept must specify:

```text
contradictory parameter:
state A and justification:
state not-A and justification:
separation variable:
transition mechanism:
control and failure mode:
```

---

## 8. Su-Field and standard inventive solutions

### 8.1 Model

A minimally functioning Su-Field model contains:

- `S1`: product or object receiving the action;
- `S2`: tool or agent producing the action;
- `F`: field carrying the interaction.

```text
S2 --F--> S1
```

Use field classes such as mechanical, acoustic, thermal, chemical, electrical, and magnetic/electromagnetic when appropriate.

### 8.2 Problem types

| Problem type | Diagnostic question |
|---|---|
| Incomplete | Is a necessary substance or field missing? |
| Insufficient | Is the useful interaction too weak, unstable, or poorly controlled? |
| Excessive/harmful | Does the interaction create damage, contamination, noise, heat, wear, or another harm? |
| Measurement | Is the required state difficult to detect or infer? |

### 8.3 Five classical standard-solution classes

1. improve with little or no system change;
2. improve by changing the system;
3. transition to another system level or structure;
4. detection and measurement solutions;
5. simplification and improvement strategies.

Do not cite a standard-solution number unless the exact rule and source have been verified. Otherwise cite the class and describe the transformation.

---

## 9. ARIZ-85C deep route

Use ARIZ only after TRIZ has been explicitly activated and either:

- the user explicitly requests deep TRIZ/ARIZ;
- the quick contradiction, separation, and resource routes produce only compromises or weak concepts;
- a complex mini-problem must be solved with minimal acceptable system change.

Compressed nine-part route:

1. formulate the mini-problem, conflicting pair, and base/inverted technical contradictions;
2. identify operational zone, operational time, and substance–field resources;
3. formulate IFR-1, macro physical contradiction, micro physical contradiction, and IFR-2;
4. mobilize resources, separation, standard solutions, smart substances, and voids;
5. search scientific effects by required function;
6. reformulate, widen, decompose, or invert the problem if stuck;
7. test whether the contradiction is resolved and identify secondary problems;
8. assess system and supersystem implementation consequences;
9. post-mortem the solution path and update the knowledge base.

ARIZ is a disciplined reframing algorithm, not a license to produce longer prose.

---

## 10. Engineering-system evolution route

Use only for explicit prognostic, roadmap, or next-generation questions.

Relevant lenses include:

- increasing value/ideality;
- S-curve stage and main parameters of value;
- increasing dynamization and controllability;
- increasing coordination;
- transition to the supersystem;
- flow enhancement;
- trimming and convolution;
- decreasing direct human involvement;
- transitions in structure, fields, and system level.

Treat trends as hypothesis generators, not deterministic laws of future products. State:

```text
current system and MPV:
current S-curve evidence:
candidate trend:
predicted transition:
required enabling resources:
competing evolution path:
early observable signal:
falsifier:
```

---

## 11. Output contract

```markdown
# TRIZ Engineering Analysis

## 0. Activation and scope
- Explicit trigger:
- Canonical or analogical:
- System and primary function:

## 1. Foundation handoff
- Definitions:
- Boundary and supersystem:
- Evidence and measurements:
- Hard constraints and duties:
- Unknowns:

## 2. Function and problem model
- Function carrier → action → object:
- Useful function:
- Harmful/insufficient effect:
- Cause–effect chain:
- Key disadvantage:

## 3. IFR and ideality
- Baseline:
- IFR:
- Available resources:
- Ideality comparison:

## 4. Contradictions
- Base engineering contradiction:
- Inverted contradiction:
- Physical contradiction:
- Operational zone/time:

## 5. Route selected
- Matrix/principles | separation | Su-Field/standards | ARIZ | evolution
- Why this route:
- Source/provenance:

## 6. Inventive concepts
| Concept | Principle/route | Mechanism | Resource | Δ ideality | New risk | Validation |

## 7. Rejected compromises
| Candidate | Why it does not resolve the contradiction |

## 8. Recommendation
- Leading concept:
- Why:
- Hard blockers:
- Next discriminating test:
- Falsifier:
- Escalation/review trigger:

## 9. Return to OpenDeepMind quality gate
- First-Principles checks required:
- Evidence still missing:
- Competing model:
```

---

## 12. Stop and refusal conditions

Stop with concepts when:

- at least one concept resolves the formulated contradiction rather than merely averaging it;
- the concept passes the current hard constraints;
- the mechanism and used resource are explicit;
- a feasible discriminating test exists;
- secondary contradictions and uncertainty are visible.

Stop without a recommendation when:

- the contradiction depends on unverified facts;
- no concept survives safety or physical feasibility;
- the user has not provided decision-critical constraints;
- the task is outside canonical scope and analogical use was not requested;
- the evidence cannot distinguish the proposed mechanism from a rival.

Do not invent a TRIZ solution to avoid reporting underdetermination.

---

## 13. Sources, provenance, and cautions

### Primary theoretical lineage

- Genrich Altshuller, *Creativity as an Exact Science*.
- Genrich Altshuller, *The Innovation Algorithm*.
- Classical TRIZ work on inventive principles, contradictions, standard inventive solutions, ARIZ, resources, and engineering-system evolution.

### Current reference sources

- [MATRIZ TRIZ Knowledge Base](https://wiki.matriz.org/)
- [MATRIZ — contradiction matrix](https://wiki.matriz.org/docs/triz/problem-solving-tools-5890/contradictions/engineering-contradiction-5995/contradiction-matrix-6026/)
- [MATRIZ — Ideal Final Result](https://wiki.matriz.org/docs/triz/problem-solving-tools-5890/ariz-5892/ideal-final-result-5922/)
- [MATRIZ — ARIZ](https://wiki.matriz.org/docs/triz/problem-solving-tools-5890/ariz-5892/)
- [MATRIZ — substance-field modeling](https://wiki.matriz.org/knowledge-base/triz/problem-solving-tools-5890/substance-field-modeling/)
- [Altshuller Institute — 40 Principles](https://triz.org/principles/)
- [Altshuller Institute — contradictions](https://triz.org/contradictions/)
- [Altshuller Institute — ideality](https://triz.org/ideality/)

### Repository influence

- [Antropocosmist/triz-engineering-solver](https://github.com/Antropocosmist/triz-engineering-solver), MIT License.

This OpenDeepMind module is an original synthesis. It adopts the external repository's useful design lessons—explicit scope gates, IFR, contradiction classification, resource analysis, separation, Su-Field, ARIZ escalation, traceable concept output, and refuse-with-reframe discipline—without copying its full contradiction-matrix dataset or resource corpus.

### Cautions

- Patent-derived patterns are heuristic transfer knowledge, not universal laws.
- Matrix recommendations are statistical prompts, not ranked proofs.
- Historical TRIZ terminology and modern MATRIZ terminology do not always map one-to-one.
- “No compromise” means seek contradiction resolution; it does not permit ignoring feasibility, safety, economics, or duty.
- TRIZ can generate a novel mechanism hypothesis, but only modeling and evidence can establish performance.
