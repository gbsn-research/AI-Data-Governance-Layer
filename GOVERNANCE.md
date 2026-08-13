# ADGL specification governance — working public model

ADGL is currently a GBSN Research-maintained public working specification with open issue and contribution processes. It is not yet governed by a neutral standards body or a multi-stakeholder voting organization.

## Roles

- **Maintainer and current specification editor:** GBSN Research.
- **Contributors:** any participant submitting issues, fixtures, mappings, documentation, or implementation changes under the repository contribution terms.
- **Reviewers:** maintainers and identified technical reviewers participating in public discussion.

GBSN Research currently has final acceptance and release authority. Because GBSN also develops a proprietary implementation, decisions affecting normative semantics must record relevant commercial interests and alternatives raised by external contributors.

## Change lifecycle

`PROPOSED -> DISCUSSED -> DRAFT -> ACCEPTED -> STABLE -> DEPRECATED`

A normative proposal must identify:

- affected objects, operations, states, profiles, and audit behavior;
- motivating problem and available evidence;
- compatibility and migration impact;
- at least one positive and one negative executable fixture where practical;
- interaction with existing precedence and extension rules;
- specification version and rationale;
- known commercial implementations or interests affected by the proposal.

Acceptance requires a public disposition explaining the decision and unresolved objections. Rejected or deferred proposals remain visible with reasons. Material objections may be resubmitted with new evidence. Experimental operations remain outside the normative profile until explicitly accepted and versioned.

## Conformance independence

No commercial product defines ADGL conformance. Normative text and versioned public fixtures control. Product-specific extensions must be namespaced and must not be described as Core ADGL semantics.

## Future governance transition

If external implementation and stakeholder participation becomes substantial, GBSN intends to evaluate transfer or joint stewardship through an appropriate standards or foundation structure. Until such a transition occurs, documentation must describe the project as GBSN-maintained rather than community-ratified.

