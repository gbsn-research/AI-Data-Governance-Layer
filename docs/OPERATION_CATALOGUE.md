# Operation Catalogue — ADGL Semantic Specification 0.3.0

ADGL 0.3 separates operations by governance stage. Not every operation below is fully implemented by Toolkit 0.5.3; see `IMPLEMENTATION_STATUS.md` for the executable subset.

## Knowledge Governance

### Admission and requirements
`ALLOW`, `DENY`, `EXCLUDE`, `REQUIRE`

### Influence and evidentiary role
`PRIORITIZE`, `DEPRIORITIZE`, `DEFER_TO`, `OVERRIDE`, `REQUIRE_CORROBORATION`, `ASSIGN_ROLE`

### Lifecycle and isolation
`QUARANTINE`, `EMBARGO`, `ISOLATE`, `RELEASE`, `SUPERSEDE`, `EXPIRE`, `REVOKE`, `ARCHIVE`

### Collection operations
`FILTER`, `SAMPLE`, `GROUP`, `AGGREGATE`, `SORT`, `LIMIT`

### Provenance
`TRACE`, `VERIFY_SOURCE`, `REQUIRE_PROVENANCE`, `MARK_PROVENANCE`

## Analysis Governance

### Analytical method
`COMPARE`, `CLASSIFY`, `SUMMARIZE`, `CALCULATE`, `SCORE`, `ESTIMATE`, `INFER`

### Evidence treatment and transformation
`CORROBORATE`, `CHALLENGE`, `VERIFY`, `NORMALIZE`, `WEIGHT`, `BALANCE`

### Analytical constraints and validation
`REQUIRE_SECOND_SOURCE`, `REQUIRE_VALIDATION`, `REQUIRE_EXPLANATION`, `PRESERVE_CONFLICT`, `DO_NOT_INFER`, `LIMIT_INFERENCE`, `VALIDATE`, `REPROCESS`

## Model and Processing Governance

`ROUTE`, `REQUIRE_MODEL`, `DENY_MODEL`, `REQUIRE_REGION`, `DENY_REGION`, `LOCAL_ONLY`, `NO_FALLBACK`, `REQUIRE_VALIDATED_VERSION`

Model and processing-location policy belongs to Analysis Governance when it constrains which computational resource may perform the analysis. The same metadata may also constrain consequential actions where applicable.

## Consequence Governance

### Consequence dispositions
`INFORM`, `DECIDE`, `ACT`

- `INFORM`: the governed result is the endpoint for the current ADGL consequence decision.
- `DECIDE`: an accountable human decision right is required.
- `ACT`: a machine-executable consequential action may proceed subject to authorization and external enforcement.

### Human decision vocabulary
`APPROVE`, `DENY`, `MODIFY`, `CONSENT`, `REQUEST_EVIDENCE`, `DEFER`, `ESCALATE`

### Action vocabulary
`AUTHORIZE`, `EXECUTE`

`DECIDE -> ACT` is a valid transition after an authorized human decision. Analytical tool calls that merely retrieve or transform evidence are not automatically consequential `ACT` operations.

Toolkit 0.5.3 candidate integrity behavior treats `approval_required: true` on an `ACT` rule as an explicit `DECIDE -> ACT` gate. It also evaluates CapabilityGrant limits against the effective concrete Action. Fields stated in the policy Action template are runtime constraints; the request may add only fields that the template left unconstrained.

## Cross-stage control structures

`CASE`, `SELECT`, `IF`, `WHEN`, `THEN`, `DO`, `ELSE`, `FOR_EACH`, `UNTIL`, `STOP`, `FALLBACK`, `EXCEPTION`

## Core knowledge-decision operations and states

Operations: `PERMIT`, `QUALIFY`, `BLOCK`, `ABSTAIN`, `ESCALATE`, `REQUIRE_REVIEW`

Resulting states: `PERMITTED`, `QUALIFIED`, `BLOCKED`, `ABSTAINED`, `ESCALATED`, `AWAITING_REVIEW`

Failure reason codes remain separate from decision states, including `INSUFFICIENT_EVIDENCE`, `POLICY_CONFLICT`, `NO_COMPLIANT_ROUTE`, `ANALYSIS_METHOD_NOT_PERMITTED`, `ANALYSIS_VALIDATION_REQUIRED`, and `ACTION_NOT_AUTHORIZED`, `ACTION_AUTHORIZATION_REQUIRED`, `ACTION_TEMPLATE_MISMATCH`, `ACTION_VALUE_REQUIRED`, `ACTION_VALUE_LIMIT_EXCEEDED`, `ACTION_GRANT_EXPIRED`, and `ACTION_QUOTA_EXCEEDED`.

## Default base precedence

1. Legal/regulatory/sovereign constraints
2. Explicit prohibitions and mandatory security constraints
3. Data-classification and processing-location constraints
4. Lifecycle restrictions
5. Governing-authority rules
6. Mandatory evidence and human-review obligations
7. Case-specific policy
8. Organizational defaults
9. Priority and preference rules
10. Optional fallback behavior
