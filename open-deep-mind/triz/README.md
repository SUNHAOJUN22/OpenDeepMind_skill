# OpenDeepMind TRIZ Module / 完整 TRIZ 工程发明子系统

> **Opt-in only.** This directory is loaded only after an explicit TRIZ/ARIZ request or explicit user acceptance of a suggested TRIZ route. The default OpenDeepMind route remains `First Philosophy → First Principles`.

This is the complete TRIZ specialist subsystem for OpenDeepMind: **problem identification → problem modeling → inventive synthesis → evolution/roadmapping → concept substantiation**. It is intentionally separated from `FIRST_PRINCIPLES.md` so ordinary OpenDeepMind tasks do not pay the context cost of TRIZ.

## Architecture

```text
open-deep-mind/
├── TRIZ_ENGINEERING.md                 # lightweight opt-in router
└── triz/
    ├── README.md                       # this module map
    ├── VENDORED_LICENSE.md             # MIT notice for adapted/vendored material
    ├── resources/
    │   ├── modern_problem_identification.md
    │   ├── innovative_benchmarking.md
    │   ├── function_analysis.md
    │   ├── flow_analysis.md
    │   ├── cause_effect_chain.md
    │   ├── trimming.md
    │   ├── feature_transfer.md
    │   ├── multiscreen_operator.md
    │   ├── ideality_ifr_resources.md
    │   ├── contradictions.md
    │   ├── 39_parameters.md
    │   ├── 40_principles.md
    │   ├── contradiction_matrix.json   # full 39×39 matrix transcription
    │   ├── separation_principles.md
    │   ├── substance_field_modeling.md
    │   ├── 76_standard_solutions.md    # all 76, official 5-class numbering
    │   ├── ariz_85c.md
    │   ├── clone_problems.md
    │   ├── effects_and_fos.md
    │   ├── evolution_trends.md
    │   ├── s_curve_and_tese.md
    │   ├── concept_substantiation.md
    │   ├── glossary.md
    │   ├── output_template.md
    │   └── sources.md
    ├── examples/
    │   ├── brake_disc.md
    │   ├── battery_pack.md
    │   ├── heat_exchanger_fouling.md
    │   └── anti_example_misframed.md
    └── scripts/
        ├── lookup_matrix.py
        └── validate_triz_module.py
```

## Module coverage

| Layer | Covered tools |
|---|---|
| **Problem identification** | function-cost analysis, flow analysis, CECA, trimming, feature transfer, innovative benchmarking, S-curve and TESE routing |
| **Problem models** | engineering contradiction, physical contradiction, Su-Field, generalized function, trimming/feature-transfer problems, ARIZ mini-problem |
| **Classical solution knowledge** | 39 typical parameters, full contradiction matrix, 40 inventive principles, physical-contradiction separation, full 76 SIS, ARIZ-85C |
| **Resource/ideality** | IFR vs ideal system, substance/field/space/time/information/supersystem resources, relative ideality |
| **Knowledge transfer** | FOS, scientific-effects route, clone-problem transfer, multi-screen operator |
| **Evolution** | S-curve, MPV, modern TESE hierarchy, supersystem, trimming, completeness, flow, coordination, controllability, dynamization |
| **Substantiation** | hard feasibility gates, First-Principles modeling, uncertainty, simulation/experiment/prototype, FMEA, prior art/patent search |
| **Execution** | deterministic matrix lookup, module integrity validator, output template, worked examples |

## Three-layer logic

### Layer A — Problem identification

Do not start with the contradiction matrix by default. First identify the right problem using the smallest adequate subset of:

- function-cost analysis;
- flow analysis;
- cause-effect chain analysis (CECA);
- trimming;
- feature transfer;
- innovative benchmarking;
- S-curve/TESE analysis.

The output is a **key problem**, not a large collection of symptoms.

### Layer B — Problem solving

Modern routing recognizes four main key-problem models:

```text
Engineering contradiction → 39 parameters → matrix → 40 principles
Physical contradiction    → separation / effects / FOS / clone-problem transfer
Su-Field problem           → 76 Standard Inventive Solutions
Function problem           → FOS / scientific effects
```

Additional routes:

```text
Difficult minimal-change key problem → ARIZ-85C
Trimming problem                     → contradictions / Su-Field / FOS / ARIZ
Feature-transfer problem             → contradictions / effects / ARIZ
Roadmap question                     → S-curve + TESE
```

### Layer C — Concept substantiation

TRIZ generates **inventive concepts**, not proof. Every leading concept returns to OpenDeepMind First Principles for:

- governing-equation and dimensional checks;
- material/manufacturing feasibility;
- parameter and data provenance;
- boundary/initial/closure assumptions;
- safety, regulatory and lifecycle review;
- uncertainty and sensitivity;
- simulation, experiment, prototype and FMEA;
- patent/novelty search when relevant;
- competing-model and falsification analysis.

## Progressive loading

The router loads only what the current problem needs. Examples:

```text
Explicit EC only
→ contradictions.md + 39_parameters.md + matrix + 40_principles.md

Physical contradiction
→ contradictions.md + separation_principles.md
  (+ effects/FOS if required)

Fouling / harmful interaction
→ function/flow/CECA → substance_field_modeling.md → 76_standard_solutions.md

Deep stuck problem
→ ariz_85c.md + only the knowledge resources reached by ARIZ

Technology roadmap
→ s_curve_and_tese.md + evolution_trends.md
```

## Deterministic tools

Matrix lookup:

```bash
python open-deep-mind/triz/scripts/lookup_matrix.py --improve 10 --worsen 17
```

Complete module validation:

```bash
python open-deep-mind/triz/scripts/validate_triz_module.py
```

## Provenance

The classical implementation/data layer is adapted from the MIT-licensed [`Antropocosmist/triz-engineering-solver`](https://github.com/Antropocosmist/triz-engineering-solver), which documents matrix provenance through the MIT-licensed `kamil-szczepanik/TRIZ-Agents` transcription chain. The extended problem-identification, modern MATRIZ routing, First Philosophy/First Principles handoff, concept-substantiation layer, validators, and most explanatory text are newly authored for OpenDeepMind.

The 76 Standard Inventive Solutions file was cross-checked against the **official public MATRIZ 5-class / 76-item numbering**, rather than relying only on the reference repository's condensed working summary.

See [`resources/sources.md`](resources/sources.md), [`VENDORED_LICENSE.md`](VENDORED_LICENSE.md), and the root [`NOTICE.md`](../../NOTICE.md).
