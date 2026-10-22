# Artifact integrity repair / 工件完整性修复

Problem: valid-looking summaries, compatibility flags and partial artifact lists could overstate the underlying evidence. A structured route could raise a type error; a huge repetition could become an invalid filesystem path.

Failed invariant: declared success must not replace the assertions, recorded route, complete identity set or independent publication authority.

Affected layer: benchmark aggregation and v16/v17 compatibility contracts. Core Φ8/P9/T10 methods, case distributions and vendored TRIZ data are unchanged.

Changes:

- Bind every grading record to the complete official case assertion set, rejecting omitted, replaced or extra criteria even when the summary is self-consistent. Derive totals/rates from unique records; require response evidence for PASS and reject empty PASS or red-blocker contradictions.
- Derive mechanical routing/TRIZ checks from canonical, unique module IDs and run metadata. Aggregate and paired comparisons use one effective-case rule.
- Reject orphan artifacts and unsafe integer counters; bound JSON bytes, depth and Unicode/numeric representations.
- Align C/E proposition semantics with the canonical constraint/empirical-closure taxonomy.
- Reject truthy string flags, invalid slot IDs, duplicate expected scores, scores outside [0,1], and one-sided orphan records.
- Convert four previously uncollected v16 regression functions into unittest cases. Add 31 regression methods, including public CLI failures and adversarial subcases.

Compatibility: v16/v17 complete-record status changes from READY to ARTIFACT_SET_COMPLETE. publication_ready remains false. Consumers must use this as completeness only and obtain independent publication attestation separately. CAUSAL and EPISTEMIC are not aliases for C/E. Normalized slot scores and the 0–100 semantic rubric are distinct interfaces.

Validation: run every command in AGENTS.md and the README. The original 26 new methods were executed against the baseline and exposed failures before repair; the independent criterion/module audit added five methods and reproduced seven failing cases before its fix. The final suite contains 92 tests. Current delivery status belongs to the exact commit's CI, not this historical description. The known vendored matrix anomaly is retained and documented.

中文说明：本次修复针对真实评测聚合入口与兼容接口，使计数、状态和工件身份互相一致；工件完整不等于模型已执行、科学结论正确或具备发布资格。旧 READY 状态迁移为 ARTIFACT_SET_COMPLETE；C/E 分别为约束与经验闭合；0–1 槽位分数不能混用 0–100 语义分。合成测试夹具不代表真实模型性能。

## JSON numeric underflow follow-up / JSON 数值下溢补充修复

- **Problem / failed invariant:** a nonzero JSON number could become floating-point zero before range validation. Both a ledger confidence and a benchmark judge score of `-1e-999` were accepted as `-0.0`, despite their nonnegative field contracts.
- **Evidence / affected layer:** the real ledger CLI returned `ok: true`; the real benchmark aggregator accepted the malformed grading artifact into its complete-run count. This affects the two bounded JSON readers, not the Φ8/P9/T10 methods or the benchmark's authored assertions and distribution.
- **Changed rule / expected improvement:** reject a parsed float of zero whenever the JSON significand contains a nonzero digit. Exponent digits are excluded from that check. Negative input cannot bypass a range boundary through underflow, and nonzero extension values cannot silently disappear.
- **Compatibility / new failure risk:** previously accepted nonzero literals below the representable range now produce structured input errors. Exact signed zeros, including extreme exponents, and representable subnormals remain valid numeric inputs. Existing field ranges, resource budgets and ordinary floating-point rounding remain unchanged; this is not arbitrary-precision arithmetic.
- **Validation:** eight new public-CLI test methods cover 26 subcases, including negative confidence/score, extension fields, signed zeros and representable subnormals. On the original readers, the four rejection methods expose 12 failing subcases; the four valid-input methods pass. Run all original repository CI commands after repair. Synthetic fixtures are software tests, never model performance measurements or publication attestations.

中文说明：两处 JSON 入口现在会在字段范围检查之前拒绝“非零数下溢为零”；合法零值和可表示的次正规数继续保留。修复不改变评分标准、不提高测试分数，也不赋予评测结果发布资格。
