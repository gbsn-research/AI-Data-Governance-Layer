# Candidate Execution-Integrity Semantics

The ADGL v0.9 paper package reports a 25-check published normative conformance suite. Subsequent implementation testing exposed additional fail-closed conditions at the boundaries between governance stages. Toolkit 0.5.3 implements eleven **candidate** integrity checks while these semantics are prepared for the next normative specification revision.

1. **C26 — Upstream terminal propagation.** A blocked/paused Knowledge stage prevents successful Analysis or Consequence states.
2. **C27 — Minimum AnalysisResult contract.** An empty analytical result is rejected rather than silently treated as verified.
3. **C28 — Explicit ACT authorization.** ACT never self-authorizes; a matching CapabilityGrant is required.
4. **C29 — Trusted-time action-grant expiry.** Grant expiry is evaluated against runtime time rather than requester-supplied time.
5. **C30 — Reference in-process action quota enforcement.** `max_calls` is enforced within a single PipelineEngine instance.
6. **C31 — Effective Action value authorization.** The policy action template is merged with the concrete requested Action before grant limits such as `max_value` are evaluated; when a value limit applies, a concrete `financial_value` is required.
7. **C32 — Mandatory human approval.** `approval_required: true` creates a `DECIDE -> ACT` gate and cannot be bypassed by a CapabilityGrant alone.

8. **C33 — Finite numeric governance.** Non-finite numeric values such as NaN/Infinity are rejected and financial values are non-negative.
9. **C34 — CapabilityGrant schema and scope integrity.** Authorization grants are strict objects, reject unknown fields, and require explicit `case_id` scope.
10. **C35 — Human DECIDE resolution.** Supported human decisions resolve a pure DECIDE consequence to an explicit status rather than remaining indefinitely awaiting a decision.
11. **C36 — Action target/template constraint enforcement.** Fields explicitly present in a policy Action template constrain the concrete requested Action; mismatches fail closed.

Production distributed systems require authenticated governance assertions, durable/atomic quota consumption, trusted policy distribution, and authenticated action-target and parameter authorization beyond the reference template-subset semantics. These candidate checks are not independent certification and are not represented as already normative in Specification 0.3.0.
