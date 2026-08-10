# Changelog

All notable changes are documented here.

## [Unreleased] — Complete TRIZ subsystem

### Added

- Modular `open-deep-mind/triz/` subsystem behind the existing opt-in `TRIZ_ENGINEERING.md` router.
- Modern TRIZ problem-identification layer: function analysis, flow analysis, cause–effect chain analysis (CECA), trimming, feature transfer, innovative benchmarking, multi-screen analysis, and key-problem routing.
- Complete classical contradiction layer: 39 typical engineering parameters, 40 inventive principles, full 39×39 contradiction-matrix transcription, engineering/physical contradiction modeling, and separation principles.
- Su-Field modeling plus an explicit 76-item Standard Inventive Solutions index using the public MATRIZ five-class numbering (13 + 23 + 6 + 17 + 17).
- ARIZ-85C operational map with nine parts and three blocks.
- Ideality, Ideal Final Result (IFR), resource analysis, clone-problem transfer, Function-Oriented Search (FOS), scientific-effects routing, S-curve analysis, and modern TESE hierarchy.
- Concept-substantiation layer connecting TRIZ output back to OpenDeepMind First Principles, uncertainty, safety, simulation, experiment, manufacturability, lifecycle, FMEA, and prior-art validation.
- Four worked examples: brake-disc thermal management, EV battery thermal safety, heat-exchanger fouling, and a refusal/reframe anti-example.
- Dependency-free matrix lookup and full TRIZ integrity validator.
- TRIZ source/provenance map and vendored MIT license notice.

### Changed

- Replaced the monolithic TRIZ file with a lightweight opt-in router plus progressive-disclosure resources.
- Main repository validator now requires the TRIZ module map, critical classical resources, source map, and TRIZ scripts.
- GitHub Actions now executes complete TRIZ-module validation and a deterministic matrix-lookup smoke test.

## [1.1.0] — 2026-08-09

### Added

- Separate `open-deep-mind/TRIZ_ENGINEERING.md` optional engineering-invention module.
- Explicit TRIZ activation gate: the module is not loaded during normal First Philosophy/First Principles routing unless the user asks for or accepts TRIZ.
- T10 TRIZ workflow covering function and key-problem identification, ideality and IFR, engineering/physical contradictions, 39 typical parameters, 40 inventive principles, separation, Su-Field, standard-solution classes, ARIZ-85C, engineering-system evolution, concept scoring, and validation handoff.
- Current MATRIZ and Altshuller Institute source links and attribution to the MIT-licensed `Antropocosmist/triz-engineering-solver` design influence.

### Changed

- Updated `SKILL.md` routing, boundaries, output behavior, and version metadata.
- Updated the main README with an optional TRIZ section, invocation example, and repository structure.
- Extended repository validation to require a separate TRIZ file and enforce its opt-in routing markers.
- Updated intellectual-lineage, notice, and citation metadata.

## [1.0.0] — 2026-08-08

### Added

- Agent Skills-compatible `open-deep-mind/SKILL.md`.
- Separate `FIRST_PHILOSOPHY.md` and `FIRST_PRINCIPLES.md` engines.
- Foundation Charter and Φ8 foundation-qualification protocol.
- D/O/L/C/A/E/V/U proposition ledger and JSON schema.
- P9 first-principles decomposition, model, falsification, and decision protocol.
- Cross-domain routing for science, engineering, modeling, strategy, policy, personal decisions, and creative/product innovation.
- More than thirty executable method cards.
- Red-blocker gate and twelve-dimension 100-point quality rubric.
- Scale-bridge and uncertainty audit.
- Failure-mode catalog.
- Cross-domain worked examples.
- Output templates.
- Dependency-free repository and claim-ledger validators.
- GitHub Actions validation.
- English and Chinese README files.
- Eleven editable AI-generated SVG diagrams.
- Attribution, contribution, licensing, and agent-maintenance documentation.
