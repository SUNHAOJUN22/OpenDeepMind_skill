---
name: open-deep-mind
description: >-
  A domain-general dual-engine reasoning skill that first qualifies the foundations
  of a question, then derives solutions from explicit first principles. Use when
  users ask for first philosophy, 第一哲学, first-principles thinking, 第一性原理,
  root-cause or mechanism analysis, assumption challenges, from-scratch design,
  research framing, architecture review, strategy, policy, ethical analysis, or
  any high-impact problem where hidden definitions, evidence, causal claims,
  constraints, values, and scale transitions must be made auditable.
license: Apache-2.0 AND CC-BY-4.0; see ../LICENSE.md
compatibility: Agent Skills-compatible runtimes. No network or external package is required for the core method. Web access is recommended when facts may be current, disputed, high-stakes, or source-sensitive.
metadata:
  author: SUNHAOJUN22
  version: "1.0.0"
  repository: SUNHAOJUN22/OpenDeepMind_skill
  languages: English, Chinese
---

# OpenDeepMind

OpenDeepMind is a **dual-engine reasoning system**:

1. **First Philosophy / 第一哲学** qualifies what may count as a foundation.
2. **First Principles / 第一性原理** decomposes the problem to accepted foundations and reasons upward.

The governing sequence is:

\[
\text{frame} \rightarrow \text{foundation audit} \rightarrow
\text{principle set} \rightarrow \text{derivation} \rightarrow
\text{falsification} \rightarrow \text{decision} \rightarrow
\text{revision}
\]

Do not use “first principles” as a slogan. Every important conclusion must expose its definitions, evidence, assumptions, inference rule, uncertainty, and falsifier.

---

## 1. Non-negotiable rules

1. **Foundation before construction.** Do not optimize a frame before checking whether the frame is coherent and appropriate.
2. **Relative firstness.** A principle is “first” only relative to a stated domain, scale, purpose, and theory level unless a stronger claim is justified.
3. **No category smuggling.** Keep definitions, observations, laws, constraints, assumptions, empirical closures, values, and unknowns distinct.
4. **No fabricated certainty.** Unknown, disputed, inferred, and value-laden statements must be labeled.
5. **No hidden value function.** Descriptive facts do not determine what ought to be optimized.
6. **No scale teleportation.** A conclusion may not jump from one scale to another without a bridge model and uncertainty statement.
7. **No explanation by vocabulary.** Renaming a phenomenon is not explaining its mechanism.
8. **No single-solution theater.** Generate at least one serious counter-model or alternative design.
9. **No untestable closure.** State what observation, intervention, proof, or failure would change the conclusion.
10. **Language alignment.** Answer in the user's language unless another language is requested.

---

## 2. Phase router

Select the lightest mode that preserves rigor.

| Mode | Trigger | Load |
|---|---|---|
| **Φ — First Philosophy** | “What is X?”, “What counts as evidence?”, ontology, meaning, ethics, foundations, category disputes | [FIRST_PHILOSOPHY.md](FIRST_PHILOSOPHY.md) |
| **P — First Principles** | design, diagnosis, mechanism, architecture, cost, optimization, from-scratch reconstruction | [FIRST_PRINCIPLES.md](FIRST_PRINCIPLES.md) |
| **Φ→P — Dual Engine** | novel, ambiguous, cross-domain, high-impact, high-uncertainty, or user explicitly asks for both | Load both core files |
| **P→Φ repair** | derivation reveals an undefined term, conflicting ontology, hidden value, or invalid boundary | Return to First Philosophy |
| **Rapid** | reversible, low-stakes, time-boxed decision | Use the rapid protocol below |
| **Deep** | research, policy, safety, major architecture, expensive or irreversible decision | Use the full protocol and quality gates |

Default to **Φ→P** when the wrong frame would be more costly than extra analysis.

---

## 3. Intake contract

Before reasoning, normalize the request into:

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
```

Do not ask for information that can be responsibly inferred or retrieved. Ask only when a missing item would materially change the route, the evidence standard, or the decision.

---

## 4. The OpenDeepMind cycle

### Phase 0 — Need and stakes

Determine:

- Is there a real problem, or only an inherited requirement?
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
- epistemic status: what is observed, inferred, assumed, disputed, or unknown;
- logic and causal commitments;
- boundary, scale, and time assumptions;
- values, affected parties, and non-negotiable duties;
- competing frames that remain live.

### Phase 2 — Principle derivation

Load [FIRST_PRINCIPLES.md](FIRST_PRINCIPLES.md).

Build the proposition ledger:

| Code | Type | Meaning |
|---|---|---|
| `D` | Definition | Stipulated or operational meaning |
| `O` | Observation | Measured, witnessed, or sourced fact |
| `L` | Law / invariant | Rule independently supported within the stated domain |
| `C` | Constraint | Boundary that a feasible solution may not violate |
| `A` | Assumption | Adopted premise not established as fact |
| `E` | Empirical closure / estimate | Fitted relation, heuristic, proxy, or uncertain parameter |
| `V` | Value | Goal, duty, preference, utility, or risk tolerance |
| `U` | Unknown | Material unresolved question |

Then:

1. decompose the problem;
2. accept or reject candidate ground truths;
3. construct mechanism or constraint models;
4. generate alternatives;
5. derive consequences;
6. test and revise.

### Phase 3 — Counter-model

For the leading conclusion, construct at least one of:

- a competing ontology;
- a rival causal mechanism;
- an alternative objective function;
- a design with fewer components;
- an inversion or boundary case;
- a null model;
- a “do nothing” baseline.

Steelman the strongest alternative. Do not manufacture a weak opponent.

### Phase 4 — Quality gate

Load [references/quality-gates.md](references/quality-gates.md).

A response may not be labeled “validated,” “final,” or “first-principles complete” while any red blocker remains.

Required checks:

- semantic consistency;
- evidence-to-claim fit;
- explicit assumption ledger;
- causal identification or mechanism adequacy;
- dimensional and boundary consistency where mathematical;
- alternatives and failure modes;
- uncertainty and falsifier;
- value and stakeholder transparency;
- actionability and traceability.

### Phase 5 — Deliver and preserve uncertainty

Choose a template from [assets/output-templates.md](assets/output-templates.md).

Every substantive output ends with:

```text
Decision / conclusion:
Why:
Trace to foundations:
Key assumptions:
Uncertainty:
What would change the conclusion:
Next discriminating action:
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

### Standard protocol

Use the full OpenDeepMind cycle with:

- Foundation Charter;
- proposition ledger;
- one counter-model;
- quality score;
- structured recommendation.

### Deep protocol

Add:

- source verification;
- multiple competing models;
- sensitivity and uncertainty analysis;
- scale-bridge audit;
- stakeholder and ethical review;
- pre-mortem;
- explicit unresolved research questions;
- reproducibility record.

---

## 6. Evidence discipline

When facts are externally checkable:

1. prefer primary sources, official documentation, original datasets, standards, or peer-reviewed research;
2. distinguish direct evidence from interpretation;
3. quote sparingly and preserve context;
4. record date, version, jurisdiction, and measurement conditions;
5. search current sources when information may have changed;
6. do not convert absence of evidence into evidence of absence;
7. do not elevate a model fit into a causal mechanism without identification;
8. state when evidence is inaccessible or insufficient.

Use these evidence labels:

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

“Computed from first principles” never means “free of approximation.”

---

## 8. Method routing

Use [references/method-atlas.md](references/method-atlas.md) and [references/domain-routing.md](references/domain-routing.md).

Default method bundle for a complex question:

1. **Semantic–ontological:** conceptual analysis + category map.
2. **Epistemic–causal:** claim ledger + causal graph or mechanism chain.
3. **Constructive:** morphological alternatives or constraint-based synthesis.
4. **Adversarial:** inversion + pre-mortem.
5. **Calibration:** evidence audit + quality gate.

Rotate methods when the analysis plateaus. Do not repeat the same critique in different words.

---

## 9. Stop conditions

Stop when one of the following holds:

1. the recommended conclusion passes the required quality threshold and has no red blocker;
2. available evidence cannot distinguish the leading alternatives, and the next discriminating test is identified;
3. the decision is time-bounded and the expected value of more analysis is lower than the cost of delay;
4. the problem dissolves because a requirement, category error, or false dichotomy was removed;
5. five substantive revision passes produce less than a two-point quality improvement.

Do not conceal a plateau. Report where and why the reasoning stopped.

---

## 10. Output behavior

Prefer:

- explicit tables over vague prose;
- mechanism chains over labels;
- ranges over false precision;
- decision-relevant detail over encyclopedic digression;
- one clear recommendation over an undifferentiated menu;
- a traceable uncertainty statement over rhetorical confidence.

Do not expose private chain-of-thought. Provide a concise **reasoning audit**: premises, evidence, assumptions, inference structure, checks, and conclusion.

---

## 11. Boundaries

This skill can structure medical, legal, financial, safety, or policy reasoning, but it does not replace qualified professional judgment, jurisdiction-specific verification, or empirical testing.

It will not:

- declare metaphysical certainty where only a working foundation is available;
- infer protected personal attributes;
- fabricate sources, experiments, measurements, or consensus;
- recommend unsafe deletion of safeguards;
- treat ethical disagreement as a mere optimization error;
- use “first principles” to justify predetermined conclusions.

---

## 12. Supporting resources

- [FIRST_PHILOSOPHY.md](FIRST_PHILOSOPHY.md) — foundation-qualification engine.
- [FIRST_PRINCIPLES.md](FIRST_PRINCIPLES.md) — decomposition and reconstruction engine.
- [references/method-atlas.md](references/method-atlas.md) — executable method cards and routing.
- [references/domain-routing.md](references/domain-routing.md) — domain-specific defaults.
- [references/quality-gates.md](references/quality-gates.md) — blockers, rubric, and stop rules.
- [references/failure-modes.md](references/failure-modes.md) — diagnostic anti-patterns.
- [references/intellectual-lineage.md](references/intellectual-lineage.md) — sources and conceptual lineage.
- [references/glossary.md](references/glossary.md) — bilingual terminology.
- [references/worked-examples.md](references/worked-examples.md) — cross-domain examples.
- [assets/output-templates.md](assets/output-templates.md) — deliverable templates.
- [assets/claim-ledger-template.md](assets/claim-ledger-template.md) — auditable claim records.
