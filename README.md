# AI Data Governance Layer (ADGL)

**ADGL — the AI Data Governance Layer — is an open research specification and reference implementation for governing
what knowledge may participate in computation, how that knowledge may be analyzed, and what consequences the resulting
analysis may produce.**

```text
KNOWLEDGE GOVERNANCE
        ↓
ANALYSIS GOVERNANCE
        ↓
CONSEQUENCE GOVERNANCE
   INFORM · DECIDE · ACT

AUDIT + PROVENANCE spans the complete governance trajectory.
```

## Current public research release

| Artifact | Version |
|---|---:|
| Public research release | 0.4.4 (Release 2) |
| Core semantic specification | 0.3.0 |
| Reference toolkit | 0.5.3 |
| Main research paper | 1.2 submission master |
| Reference cases | 8 |
| Published normative conformance checks | 25 |
| Candidate execution-integrity checks | 11 |

**Status:** Working research specification and experimental reference implementation. This repository is not a
production enterprise security appliance or a legal-compliance certification product.

## Why ADGL

Traditional governance controls where information is stored and who can access it. AI systems introduce two further
governance questions:

1. **Analysis Governance:** what may be done with admitted knowledge?
2. **Consequence Governance:** what may happen because of the resulting analysis?

ADGL separates those questions through governance semantics designed to support implementation across different models,
clouds, databases, retrieval systems, workflow tools, and agent frameworks.

## Quick start

Requires Python 3.10+.

```bash
python -m pip install -e .

adgl validate examples/regulatory_product_claim_review/policy.yaml

adgl run   examples/regulatory_product_claim_review/policy.yaml   --input examples/regulatory_product_claim_review/input.json

adgl pipeline   examples/autonomous_machine_action/policy.yaml   --input examples/autonomous_machine_action/input.json

adgl conformance
```

The current toolkit reports **25/25 published normative checks** plus **11/11 candidate execution-integrity checks** passing. The candidate checks were added after implementation testing and are explicitly separated from the published normative suite.

## Reference cases

1. Regulatory Product-Claim Review
2. Restricted EU Data / Model & Geographic Routing
3. Knowledge-Pool Contamination & Derivative Invalidation
4. Internal-First Strategic Research
5. Human Validation During Analysis
6. Human Decision Boundary
7. Autonomous Machine / API Action
8. Human Approval Followed by Machine Action

## Repository map

```text
adgl/                  Python reference implementation
schemas/               Machine-readable schemas
specification/         Human-readable semantic specification
examples/              Eight executable reference cases
profiles/              Illustrative domain governance profiles
conformance/           Conformance results
benchmarks/            Reproducible performance baselines
docs/                  Architecture and implementation documentation
research/              Research paper and companion appendices
tests/                 Automated tests
extensions/            Experimental, non-normative vocabulary
```

## Illustrative profiles

The repository currently includes non-normative examples for:

- sovereign processing;
- life-sciences evidence governance;
- financial AI controls;
- agent least privilege;
- regulatory control mapping.

They demonstrate how reusable ADGL profiles can be packaged. They are **not** compliance guarantees.

## Standard vs. implementation

ADGL conformance is intended to attach to **observable semantics**, not to Python, YAML, a particular model vendor,
or this reference engine. The Python toolkit exists to make the proposal executable, reproducible, and testable.

## Research and standards status

ADGL is being released for public technical review, independent implementation, interoperability testing, empirical
evaluation, and standards discussion. The high-level architecture is designed to be model-, storage-, and
retrieval-neutral. ADGL is a GBSN Research-maintained working specification, not a stakeholder-ratified standard or
independent certification scheme.

GBSN Research also develops KEE, a separate proprietary commercial implementation. KEE is not required to implement
ADGL and does not define normative conformance. See `COMMERCIAL_DISCLOSURE.md`, `IMPLEMENTATIONS.md`, and
`CONFORMANCE_CLAIMS.md`.

## Licensing

- Reference software: **Apache License 2.0**
- Specification and documentation: **CC BY 4.0**

See `LICENSE` and `LICENSE-DOCUMENTATION.md`.

## Contact and maintainer

**GBSN Research**, Lisbon, Portugal

- Scholarly correspondence and publication enquiries: **publications@gbsnresearch.com**
- ADGL technical and specification enquiries: **aidatagovernance@gbsnresearch.com**
- Security vulnerabilities: follow `SECURITY.md`.

## Citation

See `CITATION.cff`. When persistent publication identifiers are assigned, cite the specific version used in your work.
