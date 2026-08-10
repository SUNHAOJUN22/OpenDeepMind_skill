# OpenDeepMind TRIZ Module / 完整 TRIZ 工程发明子系统

> **Opt-in only.** This directory is loaded only after an explicit TRIZ/ARIZ request or explicit user acceptance of a suggested TRIZ route. The default OpenDeepMind route remains `First Philosophy → First Principles`.

This package separates TRIZ from the First-Principles engine while making the TRIZ route self-contained enough for engineering contradiction work, deep ARIZ analysis, system-evolution roadmapping, and concept substantiation.

## Architecture

```text
TRIZ_ENGINEERING.md                 # opt-in orchestrator
triz/
├── README.md                       # this map
├── VENDORED_LICENSE.md             # MIT notice for adapted/vendored source material
├── resources/
│   ├── 39_parameters.md            # complete classical 39 parameters
│   ├── 40_principles.md            # complete 40 inventive principles
│   ├── contradiction_matrix.json   # complete 39×39 Altshuller matrix transcription
│   ├── separation_principles.md    # physical-contradiction separation
│   ├── 76_standard_solutions.md    # five-class / 76-solution Su-Field reference
│   ├── ariz_85c.md                 # ARIZ-85C operational reference
│   ├── evolution_trends.md         # classical evolution trends + roadmap use
│   ├── modern_problem_identification.md
│   ├── function_analysis.md
│   ├── flow_analysis.md
│   ├── cause_effect_chain.md
│   ├── trimming.md
│   ├── feature_transfer.md
│   ├── s_curve_and_tese.md
│   ├── effects_and_fos.md
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

## Three-layer logic

### Layer A — Problem identification

Do not start with the contradiction matrix by default. First identify the right problem using the smallest adequate subset of:

- function-cost analysis;
- flow analysis;
- cause-effect chain analysis (CECA);
- trimming;
- feature transfer;
- S-curve analysis;
- trends of engineering-system evolution (TESE);
- innovative benchmarking or function-oriented search where evidence is available.

### Layer B — Problem solving

TRIZ works through four main problem models:

1. engineering/technical contradiction;
2. physical contradiction;
3. Su-Field model;
4. function/effect request.

Routes:

```text
Engineering contradiction → 39 parameters → contradiction matrix → 40 principles
Physical contradiction    → separation in time/space/condition/system level
Su-Field problem           → 76 Standard Inventive Solutions
Hard mini-problem          → ARIZ-85C
Function/effect problem    → effects database / FOS route
Roadmap question           → S-curve + TESE
```

### Layer C — Concept substantiation

TRIZ generates inventive concepts; it does not prove them. Every leading concept returns to OpenDeepMind First Principles for:

- governing-equation and dimensional checks;
- material and manufacturing feasibility;
- parameter provenance;
- safety and regulatory review;
- uncertainty and sensitivity;
- simulation, experiment, prototype, FMEA and lifecycle validation;
- patent/novelty search when relevant;
- competing-model and falsification analysis.

## Provenance

The classical core files are adapted from the MIT-licensed [`Antropocosmist/triz-engineering-solver`](https://github.com/Antropocosmist/triz-engineering-solver), which itself documents matrix provenance through the MIT-licensed `kamil-szczepanik/TRIZ-Agents` transcription chain. The modern analytical layer is newly authored for OpenDeepMind using public MATRIZ Knowledge Base terminology and routing principles.

See [`resources/sources.md`](resources/sources.md), [`VENDORED_LICENSE.md`](VENDORED_LICENSE.md), and the repository [`NOTICE.md`](../../NOTICE.md).
