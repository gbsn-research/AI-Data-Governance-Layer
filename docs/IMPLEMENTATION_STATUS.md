# Implementation Status — Toolkit 0.5.3

| Capability | Spec 0.3 | Toolkit 0.5.3 |
|---|---|---|
| Knowledge admission/lifecycle | Normative | Implemented core subset |
| Authority / priority / applicability | Normative | Implemented core subset |
| Provenance / derivative restriction propagation | Normative | Implemented basic propagation |
| Model / processing-region eligibility | Normative | Implemented |
| Deterministic base policy composition | Normative | Implemented base precedence |
| Three-stage pipeline policy validation | Normative reference behavior | Implemented schema + embedded core validation |
| Stage-qualified analytical transformations | Normative architecture | Partial; legacy collection operations retained in core engine |
| Pipeline-native model/region stage placement | Normative architecture | Partial; core-compatible routing reused |
| Analysis method allowlist | Normative reference behavior | Implemented |
| Evidence sufficiency/corroboration gate | Normative reference behavior | Implemented |
| No-infer-missing constraint | Normative reference behavior | Implemented |
| Human validation inside analysis | Normative reference behavior | Implemented basic gate |
| INFORM / DECIDE / ACT | Normative | Implemented |
| Human decision ownership | Normative | Implemented reference representation |
| DECIDE -> ACT | Normative | Implemented reference transition |
| Mandatory `approval_required` gate | Candidate integrity behavior | Implemented `DECIDE -> ACT` gate |
| Capability-grant action authorization | Normative reference behavior | Implemented effective-Action type/case/value/expiry/reference-quota checks |
| Live API/tool enforcement | Integration boundary | Not implemented |
| Live agent discovery | External integration | Not implemented |
| Production IAM/workflow/sandbox | External enforcement | Not implemented |
| Full third-party implementation portability | Research objective | Portable-subset equivalence only |


## Toolkit 0.5.3 public-release hardening

- 25 published normative conformance checks remain unchanged.
- 7 additional candidate execution-integrity checks fail closed in the reference runtime.
- Human-decision and capability-grant assertions in the reference fixtures are not authenticated identities; production systems must bind them to trusted organizational sources.
- In-process `max_calls` accounting is demonstrative, not a distributed production quota service.

- Action templates now act as subset constraints over concrete requested Actions: any field specified by policy must match at runtime, while omitted fields remain unconstrained by that template.
- CapabilityGrant is strict and case-scoped in the current reference profile; unknown fields are rejected.
- Human DECIDE outcomes resolve APPROVE/CONSENT, DENY, MODIFY, REQUEST_EVIDENCE, DEFER, and ESCALATE to explicit statuses.
