# ADGL 0.3 Semantic Model

## Governance stages

- **Knowledge Governance** — what may be considered and in what evidentiary capacity.
- **Analysis Governance** — what analytical computation may be performed on admissible knowledge.
- **Consequence Governance** — what a governed result is permitted to cause.

Audit/provenance spans all three stages.

## Primitive objects

KnowledgeObject, Source, Actor, Subject, Claim, Evidence, Policy, Profile, Case, Analysis, AnalyticalMethod, AnalysisResult, ValidationRule, ModelResource, ProcessingEnvironment, DecisionRight, ReviewRequest, HumanDecision, ActionProposal, Action, CapabilityGrant, Decision, Event, Jurisdiction, Connector, AuditRecord.

## Portable attributes

`id`, `type`, `source`, `author_or_actor`, `created_at`, `effective_from`, `effective_until`, `status`, `classification`, `jurisdiction`, `region`, `provenance_status`, `authority`, `priority`, `applicability`, `evidence_role`, `model_eligibility`, `processing_constraints`, `policy_version`, `derivation`, `confidence`, `purpose`, `retention`, `analysis_method`, `outcome_disposition`, `decision_owner`, `executor`.

## Core relationships

SUPPORTS, CONTRADICTS, QUALIFIES, CORROBORATES, DERIVES_FROM, SUPERSEDES, GOVERNS, APPLIES_TO, DEPENDS_ON, OVERRIDES, RESTRICTS, REQUIRES, GENERATES, VALIDATES, TRIGGERS.

## Consequence dispositions

`INFORM`, `DECIDE`, `ACT`.

`DECIDE -> ACT` may occur after authorized human approval or consent. Agentic execution is one possible executor of `ACT`; `ACT` does not require an AI agent.

## Feedback loops

An analytical retrieval/tool operation can create new candidate knowledge, which re-enters Knowledge Governance. A stored AnalysisResult becomes derived knowledge and should carry provenance/restriction lineage. Consequential action outcomes may likewise become new organizational facts for later Cases.

**Selection is not admission.** Selecting an object for evaluation never by itself makes it admissible to analysis.
