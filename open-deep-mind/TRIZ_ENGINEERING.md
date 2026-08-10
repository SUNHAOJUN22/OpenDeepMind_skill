# TRIZ Engineering Module / TRIZ 工程发明模块

TRIZ is an optional, explicit-use engineering module. It is separate from `FIRST_PHILOSOPHY.md` and `FIRST_PRINCIPLES.md` and is not part of the default OpenDeepMind route.

Complete module: [`triz/README.md`](triz/README.md)

Default route:

```text
First Philosophy -> First Principles -> competing models -> quality gate
```

Explicit TRIZ route:

```text
First Philosophy / First Principles qualification
-> TRIZ inventive synthesis
-> First Principles validation
-> quality gate
```

Do not load TRIZ automatically. Load it only when the user explicitly asks for TRIZ/ARIZ, the contradiction matrix, inventive principles, Su-Field analysis, IFR, Standard Inventive Solutions, or engineering-system evolution, or explicitly accepts a suggested TRIZ route.

For non-engineering tasks, TRIZ is not the default method. If the user explicitly requests an analogical transfer, label it as analogical rather than canonical engineering TRIZ.

## Route by problem type

| Problem type | Load |
|---|---|
| Identify the right engineering problem | `triz/resources/modern_problem_identification.md` |
| Function architecture | `triz/resources/function_analysis.md` |
| Substance / energy / information flow | `triz/resources/flow_analysis.md` |
| Cause structure | `triz/resources/cause_effect_chain.md` |
| Remove or redistribute components/functions | `triz/resources/trimming.md` |
| Transfer a superior feature | `triz/resources/feature_transfer.md` |
| Engineering contradiction | `triz/resources/39_parameters.md`, matrix, `40_principles.md` |
| Physical contradiction | `triz/resources/separation_principles.md` |
| Su-Field problem | `triz/resources/76_standard_solutions.md` |
| Difficult minimal-change problem | `triz/resources/ariz_85c.md` |
| Function/effect search | `triz/resources/effects_and_fos.md` |
| Technology roadmap | `triz/resources/s_curve_and_tese.md`, `evolution_trends.md` |
| Concept selection and proof plan | `triz/resources/concept_substantiation.md` |

## Workflow

```text
T0 explicit activation and scope
T1 system / supersystem / main function / constraints
T2 identify key problem
T3 resources + ideality + IFR
T4 formulate contradiction or other problem model
T5 select matrix / separation / SIS / ARIZ / FOS-effects / TESE route
T6 generate distinct concept families
T7 translate TRIZ abstractions into concrete mechanisms
T8 apply physical / safety / manufacturing hard gates
T9 define the smallest discriminating calculation or test
T10 Return to OpenDeepMind First Principles and the quality gate
```

TRIZ produces inventive concepts, not proof. Every leading concept must return to First Principles for physical equations, dimensions, materials, manufacturing, uncertainty, safety, testing, lifecycle and competing-model checks.

Use [`triz/resources/output_template.md`](triz/resources/output_template.md) for deliverables.

## Scripts

```bash
python open-deep-mind/triz/scripts/lookup_matrix.py --improve 10 --worsen 17
python open-deep-mind/triz/scripts/validate_triz_module.py
```

Sources and provenance: [`triz/resources/sources.md`](triz/resources/sources.md).  
MIT notice for adapted TRIZ implementation resources: [`triz/VENDORED_LICENSE.md`](triz/VENDORED_LICENSE.md).
