# What the ADGL Reference Toolkit Does

**Toolkit version:** 0.5.3  
**ADGL semantic specification:** 0.3.0  
**Status:** Experimental research reference implementation

The toolkit is the executable companion to the ADGL paper and appendices. It demonstrates that the proposed three-stage governance architecture can be represented as structured policy, evaluated deterministically for a supported subset, tested for conformance, and audited without embedding those semantics in a particular foundation model.

## Three governance stages

1. **Knowledge Governance** — determines what knowledge may participate and in what capacity.
2. **Analysis Governance** — constrains the analytical method, evidence sufficiency, inference behavior, model/tool choice, validation, and related processing conditions.
3. **Consequence Governance** — routes a governed result to `INFORM`, `DECIDE`, or `ACT`.

Audit and provenance span all three stages.

## Inputs

The reference runtime can accept:
- an ADGL policy and Case;
- structured candidate KnowledgeObjects;
- relationships such as `DERIVES_FROM`;
- structured conflicts;
- ModelResource metadata such as approval status, classification eligibility, region, and deployment type;
- an AnalysisResult supplied by an external analytical executor or test fixture;
- optional human-validation or human-decision input;
- optional Action and CapabilityGrant metadata for an `ACT` consequence.

## Governance behavior implemented

### Knowledge Governance
- admission, denial, exclusion, and mandatory requirements;
- quarantine, embargo/release, isolation, supersession, expiry, revocation, and archive states;
- evidence-role assignment;
- authority/priority separation and applicability gating;
- provenance checks;
- deterministic base policy composition;
- mandatory-evidence gates;
- conflict preservation;
- model eligibility and processing-region routing;
- fail-closed behavior when no compliant route exists;
- propagation of mandatory restrictions to derived objects;
- canonical decision states with separate failure reason codes.

### Analysis Governance
- allowed analytical-method checks;
- minimum-evidence and corroboration gates;
- `do_not_infer_missing` reference behavior;
- confidence-triggered human validation;
- structured AnalysisResult state.

### Consequence Governance
- `INFORM`, `DECIDE`, and `ACT` dispositions;
- human decision ownership and `DECIDE -> ACT` after approval/consent;
- task-scoped action authorization over the effective concrete Action, with Case, value, expiry, and reference in-process quota checks; and mandatory human approval when `approval_required` is set.

### Audit
- one end-to-end structured trace containing Knowledge, Analysis, Consequence, and final audit events.

## What is deliberately external

The toolkit contains no foundation model and does not require RAG, embeddings, a vector database, or a specific connector system. Analytical computation itself can be performed by a foundation model, classical ML system, statistical routine, deterministic algorithm, human analyst, or composite workflow.

It also does not provide production IAM, agent discovery, secret management, hardened sandboxing, network enforcement, live enterprise connectors, a human workflow product, or real API side-effect execution. ADGL can express policy requirements for those boundaries; external infrastructure must enforce them.

## Conformance

The v0.9 paper package defined **25 published normative executable checks**. Toolkit 0.5.3 preserves C01-C25 and adds **11 candidate execution-integrity checks (C26-C36)** identified through implementation testing. The candidate checks cover upstream terminal propagation, AnalysisResult contracts, explicit ACT authorization, trusted-time expiry, reference quota enforcement, effective-Action value authorization, mandatory human approval, finite numeric governance, strict case-scoped CapabilityGrant validation, human DECIDE resolution, and Action template constraints. They are deliberately not represented as already normative in Specification 0.3.0.

C15 compares the primary reference engine with an independent mini-interpreter bundled in the same research project on a deliberately limited portable subset. It is not evidence of full cross-language or independent third-party interoperability.

## Performance evaluation

The core benchmark uses warmed workloads, fresh Python subprocesses per workload, a zero-rule baseline, and reports median/IQR as the primary publication statistics. The current published artifact uses 20 measured runs for ordinary workloads and 12 for the largest workloads. A separate pipeline microbenchmark measures the three-stage governance decision over 1,000 objects for `INFORM`, `DECIDE`, and `ACT` without executing an external human workflow or API side effect.

These are reference-artifact baselines, not production performance claims.
