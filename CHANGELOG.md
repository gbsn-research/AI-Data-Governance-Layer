# Changelog

## 0.5.3

- Authorizes the **effective concrete Action** (policy template + requested Action), so value and runtime parameters cannot be bypassed by a generic policy template.
- Enforces `approval_required` as a `DECIDE -> ACT` human gate rather than treating it as metadata only.
- Adds candidate checks C31-C32 and regression tests for value limits, mandatory approval, and action-template type mismatch.
- Repairs the current pipeline benchmark fixture and records Toolkit/Specification versions in pipeline benchmark output.
- Makes the generic reference-case regression test assert all eight cases.
- Synchronizes current-toolkit documentation while preserving the paper-evaluated 0.5.0 benchmark lineage.

## 0.5.1

- Added five candidate execution-integrity checks after implementation testing: upstream terminal propagation, minimum AnalysisResult contract, explicit ACT authorization, trusted-time grant expiry, and in-process action quota enforcement.
- Hardened the public reference runtime without representing these post-paper checks as already normative in Specification 0.3.0.

## 0.5.0

- Wheel packaging now includes the runtime JSON Schemas so the installed CLI validates policies outside a source checkout. — 2026-08-12
- Rebased on the pre-agentic 0.3.0 reference runtime.
- Introduced the three-stage ADGL architecture: Knowledge, Analysis and Consequence Governance.
- Added `INFORM`, `DECIDE`, and `ACT` consequence dispositions.
- Added human validation inside analysis and `DECIDE -> ACT` human-authorization transition.
- Added basic capability-grant action authorization without making agentic execution the core architecture.
- Preserved all four original reference cases and added four new stage/consequence cases.
- Added illustrative non-normative governance profiles.
- Expanded conformance to 25 executable checks.
- Added a pipeline-policy schema, `adgl pipeline` CLI execution, and explicit disclosure of remaining stage-placement compatibility behavior.

## 0.3.0
- Corrected conformance, benchmark labeling, decision-state vocabulary and policy composition from prior research artifact.
