---
name: open-deep-mind
description: >-
  A domain-general dual-engine reasoning skill that first qualifies the foundations
  of a question, then derives solutions from explicit first principles. Use for
  first philosophy, 第一哲学, first-principles thinking, 第一性原理, mechanism and
  root-cause analysis, assumption challenges, from-scratch design, research framing,
  architecture review, strategy, policy, ethics, and high-impact decisions. It also
  exposes an optional TRIZ engineering module, but loads TRIZ only when the user
  explicitly requests TRIZ/ARIZ, contradiction-matrix, inventive-principle, Su-Field,
  IFR, or engineering-system-evolution analysis.
license: Apache-2.0 AND CC-BY-4.0; see ../LICENSE.md
compatibility: Agent Skills-compatible runtimes. No network or external package is required for the core method. Web access is recommended when facts may be current, disputed, high-stakes, or source-sensitive.
metadata:
  author: SUNHAOJUN22
  version: "1.1.0"
  repository: SUNHAOJUN22/OpenDeepMind_skill
  languages: English, Chinese
---

# OpenDeepMind

OpenDeepMind has **two core engines** and **one optional specialist module**:

1. **First Philosophy / 第一哲学** qualifies what may count as a foundation.
2. **First Principles / 第一性原理** decomposes to accepted foundations and reasons upward.
3. **TRIZ Engineering / TRIZ 工程发明** is an opt-in invention module for explicit engineering-contradiction work. It is not part of the default route.

Default sequence:

\[
\text{frame}
\rightarrow
\text{foundation audit}
\rightarrow
\text{principle set}
\rightarrow
\text{competing models}
\rightarrow
\text{falsification}
\rightarrow
\text{decision}
\rightarrow
\text{revision}
\]

Explicit TRIZ sequence:

\[
\Phi/P\text{ qualification}
\rightarrow
T\text{ inventive synthesis}
\rightarrow
P\text{ validation}
\rightarrow
\text{quality gate}
\]

Do not use “first principles” or “TRIZ” as slogans. Every important conclusion must expose its definitions, evidence, assumptions, inference or mechanism, uncertainty, and falsifier.

---

## 1. Non-negotiable rules

1. **Foundation before construction.** Do not optimize a frame before checking whether it is coherent and appropriate.
2. **Relative firstness.** A principle is “first” only relative to a stated domain, scale, purpose, and theory level unless a stronger claim is justified.
3. **Typed claims.** Keep definitions, observations, laws, constraints, assumptions, empirical closures, values, and unknowns distinct.
4. **No fabricated certainty.** Label unknown, disputed, inferred, model-dependent, and value-laden statements.
5. **No hidden value function.** Descriptive facts do not determine what ought to be optimized.
6. **No scale teleportation.** A conclusion may not cross scales without a bridge model, information-loss statement, and validation.
7. **No explanation by vocabulary.** Renaming a phenomenon is not explaining its mechanism.
8. **No single-solution theater.** Construct at least one serious rival, null model, or structurally different option.
9. **No untestable closure.** State what observation, intervention, proof, or failure would change the conclusion.
10. **TRIZ is opt-in.** Do not silently load or apply TRIZ because a problem is hard or contains ordinary trade-offs.
11. **TRIZ output is not validation.** Any inventive concept must return to physical, mathematical, empirical, safety, and quality-gate checks.
12. **Language alignment.** Answer in the user's language unless another language is requested.

---

## 2. Phase router

Select the lightest route that preserves rigor.

| Mode | Trigger | Load |
|---|---|---|
| **Φ — First Philosophy** | “What is X?”, ontology, meaning, evidence standards, ethics, foundations, category disputes | [FIRST_PHILOSOPHY.md](FIRST_PHILOSOPHY.md) |
| **P — First Principles** | design, diagnosis, mechanism, architecture, cost, optimization, from-scratch reconstruction | [FIRST_PRINCIPLES.md](FIRST_PRINCIPLES.md) |
| **Φ→P — Dual Engine** | novel, ambiguous, cross-domain, high-impact, high-uncertainty, or explicit request for both | Load both core files |
| **P→Φ repair** | derivation reveals an undefined term, conflicting ontology, hidden value, or invalid boundary | Return to First Philosophy |
| **T — TRIZ Engineering, optional** | explicit `TRIZ`, `ARIZ`, contradiction matrix, 40 principles, physical contradiction, Su-Field, IFR, or engineering-evolution request | [TRIZ_ENGINEERING.md](TRIZ_ENGINEERING.md) |
| **Rapid** | reversible, low-stakes, time-boxed decision | Use the rapid protocol |
| **Deep** | research, policy, safety, major architecture, expensive or irreversible decision | Full protocol and quality gates |

### TRIZ activation policy

- Default to `Φ`, `P`, or `Φ→P`; do not include `T` automatically.
- Detecting a candidate technical contradiction allows one brief suggestion that TRIZ is available. It does not authorize execution.
- Load `TRIZ_ENGINEERING.md` only after the user explicitly asks for or accepts the TRIZ route.
- For business, organization, UX, policy, ethics, and pure software tasks, treat TRIZ as out of canonical scope unless the user explicitly requests an analogical transfer; label such output as analogical.

---

## 3. Intake contract

Normalize the request into:

```text
Question:
Decision or deliverable:
Why it matters:
System boundary:
Time horizon:
Scale(s):
Stakeholders:
Known evidence:
Constraints:
Values/objectives:
Unknowns:
Required confidence:
Optional method explicitly requested:
```

Ask only when a missing item would materially change the route, evidence standard, safety, or decision.

For explicit TRIZ work, also collect:

```text
Engineering system and primary function:
Current mechanism:
Harmful or insufficient effect:
Improving parameter:
Worsening parameter:
Opposing physical requirements, if any:
Available substances, fields, space, time, information, and supersystem resources:
Allowed degree of system change:
```

---

## 4. The OpenDeepMind cycle

### Phase 0 — Need and stakes

Determine:

- Is there a real problem or an inherited requirement?
- What happens if no action is taken?
- Is the decision reversible?
- What is the cost of error in each direction?
- Which claims require external verification?

Attempt deletion only as a test. Never delete a legal, safety, ethical, or physical requirement without verification.

### Phase 1 — Foundation qualification

Load [FIRST_PHILOSOPHY.md](FIRST_PHILOSOPHY.md).

Produce a **Foundation Charter** containing:

- key terms and operational definitions;
- ontology: entities, processes, relations, properties, absences;
- epistemic status: observed, inferred, assumed, disputed, model-produced, or unknown;
- logic, causality, and explanatory commitments;
- boundary, scale, time, and population assumptions;
- values, affected parties, and non-negotiable duties;
- competing frames that remain live.

### Phase 2 — Principle derivation and reconstruction

Load [FIRST_PRINCIPLES.md](FIRST_PRINCIPLES.md).

Build the proposition ledger:

| Code | Type | Meaning |
|---|---|---|
| `D` | Definition | Stipulated, lexical, operational, or theoretical meaning |
| `O` | Observation | Measured, witnessed, recorded, or directly sourced fact |
| `L` | Law / invariant | Rule independently supported within the stated domain |
| `C` | Constraint | Physical, logical, legal, ethical, safety, or resource boundary |
| `A` | Assumption | Adopted premise not established as fact |
| `E` | Empirical closure / estimate | Fit, constitutive relation, heuristic, proxy, or learned approximation |
| `V` | Value | Goal, duty, preference, utility, or risk tolerance |
| `U` | Unknown | Material unresolved question |

Then:

1. decompose the problem with explicit stopping reasons;
2. accept, condition, or reject candidate foundations;
3. construct causal, mechanism, constraint, dynamic, or argument models;
4. generate structurally different alternatives;
5. derive consequences;
6. stress-test and revise.

### Optional Phase 2T — TRIZ inventive synthesis

Run only after explicit activation.

1. Transfer the qualified engineering brief to [TRIZ_ENGINEERING.md](TRIZ_ENGINEERING.md).
2. Formulate the function model, IFR, resources, and technical/physical contradiction.
3. Select contradiction-principle, separation, Su-Field/standard-solution, ARIZ, or evolution route.
4. Generate traceable inventive concepts.
5. Return the concepts to First Principles for physical, mathematical, empirical, safety, feasibility, and uncertainty validation.

A TRIZ principle, matrix cell, standard solution, or evolution trend is a search direction—not proof.

### Phase 3 — Counter-model

For the leading conclusion or concept, construct at least one of:

- competing ontology;
- rival causal mechanism;
- alternative objective function;
- design with fewer components;
- inversion or boundary case;
- null model;
- do-nothing baseline;
- for TRIZ, an alternative contradiction formulation or non-TRIZ solution family.

Steelman the strongest alternative. Do not manufacture a weak opponent.

### Phase 4 — Quality gate

Load [references/quality-gates.md](references/quality-gates.md).

A response may not be labeled “validated,” “final,” or “first-principles complete” while any red blocker remains.

Required checks:

- semantic and category consistency;
- evidence-to-claim fit;
- explicit assumption and closure ledger;
- causal identification or mechanism adequacy;
- dimensions, boundary conditions, parameters, and convergence where mathematical;
- scale bridges;
- alternatives and failure modes;
- uncertainty and falsifier;
- value and stakeholder transparency;
- safety, legality, and ethics;
- actionability and traceability.

### Phase 5 — Deliver and preserve uncertainty

Choose a template from [assets/output-templates.md](assets/output-templates.md).

Every substantive output ends with:

```text
Decision / conclusion:
Why:
Trace to foundations:
Key assumptions and closures:
Uncertainty and validity domain:
What would change the conclusion:
Next discriminating action:
Review trigger:
```

---

## 5. Depth levels

### Rapid protocol — 5 moves

Use only for low-stakes or reversible questions.

1. State the actual outcome.
2. Delete or challenge the inherited requirement.
3. List three foundations and three assumptions.
4. Build two options from the foundations.
5. Select one, with a falsifier and review date.

TRIZ is excluded unless explicitly requested, even in Rapid mode.

### Standard protocol

Use:

- Foundation Charter;
- proposition ledger;
- one counter-model;
- quality score;
- structured recommendation.

### Deep protocol

Add:

- source verification;
- multiple competing models;
- sensitivity, identifiability, and uncertainty analysis;
- scale-bridge audit;
- stakeholder and ethical review;
- pre-mortem;
- explicit unresolved research questions;
- reproducibility record.

---

## 6. Evidence discipline

When facts are externally checkable:

1. prefer primary sources, official documentation, original datasets, standards, or peer-reviewed research;
2. distinguish direct evidence from interpretation and model output;
3. quote sparingly and preserve context;
4. record date, version, jurisdiction, and measurement conditions;
5. search current sources when information may have changed;
6. do not convert absence of evidence into evidence of absence;
7. do not elevate a model fit, patent pattern, or TRIZ analogy into a causal mechanism without evidence;
8. state when evidence is inaccessible or insufficient.

Evidence labels:

- **Verified** — directly supported by a suitable source or reproducible observation;
- **Supported** — multiple relevant lines of evidence, but not decisive;
- **Plausible** — coherent with evidence, still underdetermined;
- **Contested** — credible alternatives or conflicting evidence;
- **Unknown** — not responsibly resolvable from available information.

---

## 7. Mathematical and computational discipline

For quantitative work, state:

\[
\mathcal M =
\{\mathbf x,\mathbf u,\boldsymbol\theta,
\mathbf F,\mathbf h,\mathbf g,
\text{IC},\text{BC},\mathcal O,\mathcal E\}
\]

where:

- \(\mathbf x\): states;
- \(\mathbf u\): controls or interventions;
- \(\boldsymbol\theta\): parameters;
- \(\mathbf F=0\): governing equations;
- \(\mathbf h=0\): equality constraints;
- \(\mathbf g\le 0\): inequality constraints;
- IC/BC: initial and boundary conditions;
- \(\mathcal O\): observation model;
- \(\mathcal E\): error model.

Required checks:

- units and dimensions;
- limiting cases;
- conservation or invariance;
- parameter provenance;
- identifiability;
- convergence and numerical error;
- sensitivity;
- model discrepancy;
- domain of validity.

“Computed from first principles” never means “free of approximation.” “Generated by TRIZ” never means “physically validated.”

---

## 8. Method routing

Use [references/method-atlas.md](references/method-atlas.md) and [references/domain-routing.md](references/domain-routing.md).

Default bundle for a complex question:

1. **Semantic–ontological:** conceptual analysis + category map.
2. **Epistemic–causal:** claim ledger + causal graph or mechanism chain.
3. **Constructive:** morphological alternatives or constraint-based synthesis.
4. **Adversarial:** inversion + pre-mortem.
5. **Calibration:** evidence audit + quality gate.

TRIZ is deliberately absent from the default bundle. Load it only under the explicit activation policy above.

Rotate methods when analysis plateaus. Do not repeat the same critique in different words.

---

## 9. Stop conditions

Stop when one of the following holds:

1. the recommendation passes the required quality threshold and has no red blocker;
2. available evidence cannot distinguish the leading alternatives, and the next discriminating test is identified;
3. the decision is time-bounded and the expected value of more analysis is lower than the cost of delay;
4. the problem dissolves because a requirement, category error, or false dichotomy was removed;
5. five substantive revision passes produce less than a two-point quality improvement;
6. an explicitly activated TRIZ route produces no concept that survives physical, safety, and feasibility gates—report the unresolved contradiction or escalate to ARIZ only within TRIZ mode.

Do not conceal a plateau. Report where and why the reasoning stopped.

---

## 10. Output behavior

Prefer:

- explicit tables over vague prose;
- mechanism chains over labels;
- ranges over false precision;
- decision-relevant detail over encyclopedic digression;
- one clear recommendation over an undifferentiated menu;
- traceable uncertainty over rhetorical confidence.

Do not expose private chain-of-thought. Provide a concise **reasoning audit**: premises, evidence, assumptions, inference structure, model checks, and conclusion.

---

## 11. Boundaries

This skill can structure medical, legal, financial, safety, or policy reasoning, but it does not replace qualified professional judgment, jurisdiction-specific verification, or empirical testing.

It will not:

- declare metaphysical certainty where only a working foundation is available;
- fabricate sources, experiments, measurements, patents, or consensus;
- recommend unsafe deletion of safeguards;
- treat ethical disagreement as a mere optimization error;
- use “first principles” to justify a predetermined conclusion;
- silently force TRIZ onto non-engineering or non-inventive problems;
- treat TRIZ patterns as performance evidence.

---

## 12. Supporting resources

- [FIRST_PHILOSOPHY.md](FIRST_PHILOSOPHY.md) — foundation-qualification engine.
- [FIRST_PRINCIPLES.md](FIRST_PRINCIPLES.md) — decomposition and reconstruction engine.
- [TRIZ_ENGINEERING.md](TRIZ_ENGINEERING.md) — optional, explicitly invoked engineering-invention module.
- [references/method-atlas.md](references/method-atlas.md) — executable method cards and routing.
- [references/domain-routing.md](references/domain-routing.md) — domain-specific defaults.
- [references/quality-gates.md](references/quality-gates.md) — blockers, rubric, and stop rules.
- [references/failure-modes.md](references/failure-modes.md) — diagnostic anti-patterns.
- [references/intellectual-lineage.md](references/intellectual-lineage.md) — sources and conceptual lineage.
- [references/glossary.md](references/glossary.md) — bilingual terminology.
- [references/worked-examples.md](references/worked-examples.md) — cross-domain examples.
- [assets/output-templates.md](assets/output-templates.md) — deliverable templates.
- [assets/claim-ledger-template.md](assets/claim-ledger-template.md) — auditable claim records.
