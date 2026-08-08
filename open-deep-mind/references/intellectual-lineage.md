# Intellectual Lineage and Sources

OpenDeepMind is an original synthesis. It does not claim that all listed thinkers endorse this workflow, nor that historical concepts map one-to-one onto modern engineering methods. The sources below provide conceptual lineage, constraints, and vocabulary.

---

## 1. First Philosophy

### Aristotle

- *Metaphysics*, especially Book IV: inquiry into being qua being and the principles belonging to being as such.
- *Physics* and *Posterior Analytics*: causes, demonstration, and scientific explanation.
- Reference overview: [Stanford Encyclopedia of Philosophy — Aristotle's Metaphysics](https://plato.stanford.edu/entries/aristotle-metaphysics/)

**Used here for:** ontology, category discipline, explanatory roles, and the distinction between a special science and inquiry into general principles.

### René Descartes

- *Meditations on First Philosophy*.
- Reference overview: [Stanford Encyclopedia of Philosophy — Descartes' Epistemology](https://plato.stanford.edu/entries/descartes-epistemology/)

**Used here for:** methodic doubt and explicit reconstruction from scrutinized premises.

**Not adopted:** a requirement that ordinary empirical decisions achieve absolute certainty.

### Immanuel Kant

- *Critique of Pure Reason*.
- Reference overview: [Stanford Encyclopedia of Philosophy — Kant's Transcendental Arguments](https://plato.stanford.edu/entries/kant-transcendental/)

**Used here for:** conditions-of-possibility analysis and the distinction between conditions that constitute an inquiry and contingent implementations.

### Edmund Husserl and phenomenology

- Reference overview: [Stanford Encyclopedia of Philosophy — Edmund Husserl](https://plato.stanford.edu/entries/husserl/)
- Reference overview: [Stanford Encyclopedia of Philosophy — Phenomenology](https://plato.stanford.edu/entries/phenomenology/)

**Used here for:** bracketing premature explanations and describing how a phenomenon is given to an observer or participant.

### Martin Heidegger

- *Being and Time*.
- Reference overview: [Stanford Encyclopedia of Philosophy — Martin Heidegger](https://plato.stanford.edu/entries/heidegger/)

**Used here for:** distinction between beings and the meaning/conditions of being, practical context, and the danger of treating entities as context-free objects.

### Emmanuel Levinas

- Reference overview: [Stanford Encyclopedia of Philosophy — Emmanuel Levinas](https://plato.stanford.edu/entries/levinas/)

**Used here for:** the claim that responsibility to others may be foundational rather than an after-the-fact optimization criterion.

### W. V. O. Quine

- “Epistemology Naturalized,” in *Ontological Relativity and Other Essays*.
- Reference overview: [Stanford Encyclopedia of Philosophy — Naturalism in Epistemology](https://plato.stanford.edu/entries/epistemology-naturalized/)

**Used here for:** fallibilism about purported absolute foundations and continuity between epistemology and empirical inquiry.

---

## 2. First-principles reasoning and scientific method

### Axiomatic and formal reasoning

- Euclidean and modern axiomatic traditions.
- Interactive theorem-proving practice: Lean, Rocq/Coq, Isabelle, and related systems.

**Used here for:** explicit premises, inference rules, and machine-auditable validity.

**Caution:** formal validity is conditional on definitions and axioms; empirical premises still require real-world warrant.

### Karl Popper

- *The Logic of Scientific Discovery*.

**Used here for:** risky tests, falsifiability, and the asymmetry between confirmation and refutation.

**Caution:** contemporary scientific confirmation also uses Bayesian, causal, mechanistic, and model-comparison approaches.

### Bayesian inference

- Bayes' theorem and modern Bayesian statistics.

**Used here for:** explicit updating under uncertainty, sensitivity to priors, and decision-relevant probability.

### Causal inference

- Judea Pearl, *Causality: Models, Reasoning, and Inference*.
- Judea Pearl, “Causal diagrams for empirical research,” *Biometrika* 82(4), 1995. [DOI](https://doi.org/10.1093/biomet/82.4.669)

**Used here for:** structural causal models, interventions, counterfactuals, and identification assumptions.

### Mechanistic explanation

- Contemporary philosophy of science work on mechanisms, entities, activities, and organization.

**Used here for:** separating labels and correlations from generative explanations.

---

## 3. Engineering, design, and systems

### Herbert A. Simon

- *The Sciences of the Artificial*.

**Used here for:** design as transformation from existing to preferred states under constraints, bounded rationality, and hierarchical systems.

### Systems thinking

- Donella H. Meadows, *Thinking in Systems*.

**Used here for:** stocks, flows, feedback, delays, leverage points, and unintended effects.

### TRIZ

- Genrich Altshuller and the theory of inventive problem solving.

**Used here for:** explicit contradiction analysis, separation principles, and structured invention.

### Morphological analysis

- Fritz Zwicky, morphological approaches to complex problem configuration.

**Used here for:** systematic exploration of parameter combinations and design spaces.

### Failure and safety methods

- FMEA, fault-tree analysis, hazard analysis, pre-mortem, and reliability engineering traditions.

**Used here for:** adversarial validation, early warning, safeguards, and recovery.

---

## 4. Computational first principles

### Density functional theory

- P. Hohenberg and W. Kohn, “Inhomogeneous Electron Gas,” *Physical Review* 136, B864–B871 (1964). [DOI](https://doi.org/10.1103/PhysRev.136.B864)
- W. Kohn and L. J. Sham, “Self-Consistent Equations Including Exchange and Correlation Effects,” *Physical Review* 140, A1133–A1138 (1965). [DOI](https://doi.org/10.1103/PhysRev.140.A1133)

**Used here for:** the distinction between foundational equations and the approximations, discretizations, pseudopotentials, exchange-correlation choices, convergence settings, and scale bridges required in practical computation.

### Physics-informed and hybrid modeling

- Governing equations, constitutive closure, parameter estimation, uncertainty quantification, and machine-learned residuals.

**Used here for:** classifying a model component as law, closure, assumption, estimate, or learned approximation rather than labeling the entire pipeline “first principles.”

---

## 5. Skill architecture

The packaging follows the open [Agent Skills specification](https://agentskills.io/specification): a `SKILL.md` with optional `references/`, `scripts/`, and `assets/`, using progressive disclosure.

Two repositories informed the design review:

1. [danyuchn/first-principles-skill](https://github.com/danyuchn/first-principles-skill), MIT License — especially the explicit requirement-deletion phase and upward reconstruction pattern.
2. [smixs/creative-director-skill](https://github.com/smixs/creative-director-skill), CC BY 4.0 — especially its phase router, method-selection matrix, recursive evaluation loop, output templates, and visual README discipline.

OpenDeepMind's terminology, dual-engine architecture, proposition ledger, quality rubric, domain routing, files, diagrams, and examples are newly authored. See the repository `NOTICE.md` for attribution.

---

## 6. How to cite this repository

Suggested software citation:

```text
SUNHAOJUN22. OpenDeepMind_skill: A Dual-Engine First Philosophy and
First-Principles Reasoning Skill. Version 1.0.0.
https://github.com/SUNHAOJUN22/OpenDeepMind_skill
```

When using a specific historical or technical method, cite the underlying source rather than citing OpenDeepMind as the origin of that method.
