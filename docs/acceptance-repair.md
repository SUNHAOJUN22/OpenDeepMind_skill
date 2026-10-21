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
