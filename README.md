# OpenDeepMind_skill

![Version](https://img.shields.io/badge/version-1.3.0-1f6feb)

**Qualify the question, build an explicit model, and choose a testable next action.**

[简体中文](README.zh-CN.md) · [Scientific guide](docs/scientific-guide.en.md) · [Skill router](open-deep-mind/SKILL.md) · [Architecture contract](open-deep-mind/ARCHITECTURE.md) · [Benchmark](BENCHMARK.md) · [Module registry](open-deep-mind/MODULES.json) · [Version](VERSION)

![AI-generated architecture of three isolated reasoning modules and a separate evaluation layer](docs/assets/ai-generated/architecture.png)

OpenDeepMind is one portable Agent Skill with three isolated method modules. An Agent-Skills-compatible host supplies the model. This repository supplies canonical methods, typed evidence contracts, a source-bound context preparer and dependency-free Python validators. Its evaluation layer observes recorded behavior and never participates in runtime routing.

## 1. Select the route and expected artifact

| Route or tool | Purpose | Concrete output |
|---|---|---|
| **Φ8**, Φ0–Φ7 | Qualify definitions, evidence, boundary, scale and values | [Foundation Charter](open-deep-mind/first-philosophy/METHOD.md) |
| **P9**, P1–P9 | Decompose, model, compare rivals, falsify and decide | [Model and decision contracts](open-deep-mind/first-principles/METHOD.md) |
| **T10**, T1–T10 | Generate engineering concepts after explicit request | [TRIZ candidates](open-deep-mind/triz/ROUTER.md), returned to P validation |
| Context preparation | Read only the selected canonical route and shared gates | `PREPARED_NOT_EXECUTED`, source hashes and byte counts |
| Claim ledger | Check types, references, cycles and numeric boundaries | Structural diagnostics; confidence requires calibration |
| Behavioral evaluation | Validate run/grade artifacts and comparable pairs | Descriptive aggregate JSON; independent attestation still required |

TRIZ is **explicit-only**. A difficult task or detected contradiction does not activate it. Φ never calls TRIZ; TRIZ concepts return to P for physical and evidential validation. The evaluation layer is not a fourth reasoning module.

## 2. Run the first checks

Core tools need Python's standard library; the maintained CI uses Python 3.12. From a source checkout:

```bash
git clone https://github.com/SUNHAOJUN22/OpenDeepMind_skill.git
cd OpenDeepMind_skill
python open-deep-mind/scripts/validate_repository.py .
python open-deep-mind/scripts/validate_ledger.py open-deep-mind/assets/example-ledger.json
python open-deep-mind/scripts/prepare_context.py --route phi-p --format manifest
```

Expose `open-deep-mind/` through your host's skill discovery mechanism. The default context budget is 256 KiB including labels. `--route triz --triz-requested` declares an explicit TRIZ request and includes P for validation; it is not independent proof of consent. Preparing context does not execute a model or measure quality, tokens, cost or model latency.

Supply a decision, system boundary, conditions, evidence, hard constraints, unknowns and a review trigger. Request one serious rival and a discriminating falsifier. Keep the eight claim types separate: **D** definition, **O** observation, **L** law, **C** constraint, **A** assumption, **E** empirical closure, **V** value, **U** unknown.

## 3. Compact technical route

![Complete AI-generated technical route with explicit TRIZ request and return to validation](docs/assets/ai-generated/roadmap.png)

The route binds each conclusion to its premises and evidence. For a quantitative problem, write an observation model and feasible domain:

$$
y=\mathcal H(x,\theta)+\epsilon,\qquad \mathcal X_f=\{x:h(x)=0,\ g(x)\le0\}.
$$

Here $x$ is the state or decision, $\theta$ the parameters, $\mathcal H$ the observation operator, and $\epsilon$ the stated noise/model-discrepancy term. Units, parameter provenance, initial/boundary conditions, closures, validity limits and falsifiers belong to the contract. A high diagnostic score cannot override a red blocker.

## 4. Statistical mechanics and physical reasoning

![AI-generated concept of ensemble assumptions, observable prediction, competing models and falsification](docs/assets/ai-generated/algorithm.png)

For a declared equilibrium NVT ensemble with $T>0$ and microstate energies $E_i$:

$$
\beta=(k_BT)^{-1},\quad Z=\sum_i e^{-\beta E_i},\quad p_i=\frac{e^{-\beta E_i}}Z,\quad \langle A\rangle=\sum_i p_i A_i.
$$

$$
F=-k_BT\ln Z,\qquad S=-k_B\sum_i p_i\ln p_i.
$$

These are **physical modeling templates**, with dimensionless $\beta E_i$; the skill does not implement an ensemble solver. Thermodynamic entropy is distinct from uncertainty about a claim. Cross-scale reasoning needs a bridge model, lost-information statement and validation domain. The [scientific guide](docs/scientific-guide.en.md) explains sources, degeneracy, limits, conservation, Bayesian updates, EVSI and implementation mappings. Primary background: [Tong, Statistical Physics](https://www.damtp.cam.ac.uk/user/tong/statphys/statmechhtml/S1.html).

## 5. Evaluate declared evidence before reporting effects

The [authored benchmark](open-deep-mind/evals/benchmark-config.json) has 60 cases, fixed 36/12/12 train/validation/holdout splits, four configurations and three repetitions. The validation design has 114 expected slots. These are design counts, not completed model runs.

```bash
python open-deep-mind/evals/scripts/validate_evals.py
python open-deep-mind/evals/scripts/create_workspace.py --iteration 1 --split validation --workspace ../OpenDeepMind_skill-workspace
```

An authorized external runner must supply actual raw responses, run records and grading evidence. Pairing requires compatible model/version and exact declared execution conditions: sampling, reasoning settings, tool access, input path/hash arrays and their order. The same literal input path with conflicting SHA-256 digests invalidates the run; distinct paths with identical digests remain valid.

After supplying real records:

```bash
python open-deep-mind/evals/scripts/aggregate_benchmark.py ../OpenDeepMind_skill-workspace/iteration-1
```

For accepted comparable pairs $I$, a recorded metric $z$ is summarized over pairs that actually have it:

$$
\overline{\Delta z}=|I_z|^{-1}\sum_{i\in I_z}(z_{L,i}-z_{R,i}),\qquad I_z\subseteq I.
$$

An empty metric sample returns null; missing measurements are not zero. Individual valid observations remain available if a pair is excluded. The full CLI uses `publication_status=EVIDENCE_COMPLETE_AWAITING_INDEPENDENT_ATTESTATION` for a complete artifact set; the compatibility helper uses `status=ARTIFACT_SET_COMPLETE`. **Both keep `publication_ready=false`.** Metadata consistency does not attest execution, actual input bytes, grading independence or release authority. See the [evaluation contract](open-deep-mind/evals/README.md).

## 6. Maintain the original software gates

```bash
python open-deep-mind/scripts/validate_repository.py .
python open-deep-mind/scripts/validate_ledger.py open-deep-mind/assets/example-ledger.json
python open-deep-mind/first-philosophy/scripts/validate_module.py
python open-deep-mind/first-principles/scripts/validate_module.py
python open-deep-mind/triz/scripts/validate_triz_module.py
python open-deep-mind/evals/scripts/validate_evals.py
python open-deep-mind/triz/scripts/lookup_matrix.py --improve 1 --worsen 3 --json
python open-deep-mind/triz/scripts/lookup_standard_solution.py 1.2.1 --json
python -m unittest discover -s open-deep-mind/tests -p 'test_*.py'
python -m compileall -q open-deep-mind
git diff --check
```

[CI](https://github.com/SUNHAOJUN22/OpenDeepMind_skill/actions/workflows/validate.yml) verifies the exact submitted source. Software checks establish repository contracts; behavioral improvement requires real paired experiments. Retain original case distributions, holdout separation, baseline pin, rubric and publication rules. Troubleshooting and detailed numerical bounds are in the [guide](docs/scientific-guide.en.md) and [repair record](docs/acceptance-repair.md).

## 7. Seven independent repositories, one conceptual research route

![Complete AI-generated overview of the seven independent repositories](docs/assets/ai-generated/seven-repo-roadmap.png)

Dotted cross-repository links are proposed handoffs requiring explicit data contracts, units, provenance and acceptance checks. They do not assert an implemented integrated platform. Every current scientific illustration above is a complete imagegen output; exact prompts, byte hashes and review notes are in the [AI image record](docs/assets/ai-generated/README.md). Historical vector assets are [linked in the archive](docs/assets/README.md).

This independent project has no affiliation with or endorsement by Google DeepMind, OpenAI, Anthropic, MATRIZ, the Altshuller Institute or referenced maintainers. [License](LICENSE.md) · [Third-party notices](NOTICE.md) · [Changelog](CHANGELOG.md).
