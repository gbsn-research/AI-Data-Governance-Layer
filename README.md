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
| Public distribution package | 0.4.3 |
| Core semantic specification | 0.3.0 |
| Reference toolkit | 0.5.3 |
| Main research paper | 0.9 |
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

ADGL separates those questions so the same portable governance semantics can be implemented across different models,
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
evaluation, and standards discussion. The high-level architecture is intentionally model-, storage-, and
retrieval-neutral.

## Licensing

- Reference software: **Apache License 2.0**
- Specification and documentation: **CC BY 4.0**

See `LICENSE` and `LICENSE-DOCUMENTATION.md`.

## Maintainer

**GBSN Research**  
Lisbon, Portugal  
Contact: **www.gbsnresearch.com** — use **Contacts**.

## Citation

See `CITATION.cff`. When persistent publication identifiers are assigned, cite the specific version used in your work.
