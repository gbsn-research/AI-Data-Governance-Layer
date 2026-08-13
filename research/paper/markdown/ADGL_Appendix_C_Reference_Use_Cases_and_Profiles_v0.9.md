**GBSN Research**

Lisbon, Portugal \| Contact: www.gbsnresearch.com — use Contacts

*Eight reference cases; original four preserved*

The first four cases are preserved from the earlier ADGL research package. Cases 5-8 extend coverage to Analysis Governance and Consequence Governance. The final section illustrates reusable domain Profiles without presenting them as compliance products or normative standard content.

# C.1 Regulatory Product-Claim Review

Scenario. A pharmaceutical organization asks whether a proposed product claim can be used in Germany. Candidate information includes current European regulatory material, approved internal research, a superseded policy, a draft legal memo, and public commentary.

Knowledge Governance. Applicable regulatory material is GOVERNING; approved internal research is PRIMARY; drafts are QUARANTINED; superseded material is excluded from the current decision; public commentary is SUPPLEMENTARY.

Analysis Governance. The analysis must distinguish scientific support from regulatory permissibility, preserve contradiction, require mandatory regulatory evidence, and defer regulatory interpretation to applicable governing material.

Consequence Governance. If evidence is complete and unambiguous the result may INFORM. If policy or governing evidence requires accountable judgment, route to DECIDE for the regulatory officer.

Demonstrates. Authority, priority, applicability, evidence roles, lifecycle, conflict preservation, and the distinction between an analytical finding and a consequential regulatory decision.

# C.2 Restricted EU Data / Model and Geographic Routing

Scenario. A multinational organization analyzes restricted data originating in the EU using several available model endpoints.

Knowledge Governance. Data classification, origin, provenance, and applicable processing policy are attached to the Case.

Analysis Governance. Only approved models and approved processing regions may compute over the restricted evidence. Unauthorized regional/model routes are rejected before model exposure; no compliant route results in a fail-closed state.

Consequence Governance. The ordinary endpoint is INFORM: return the governed analysis. No agentic behavior is required.

Demonstrates. Model and region eligibility as Analysis Governance rather than as an agent-only feature.

# C.3 Knowledge-Pool Contamination and Derivative Invalidation

Scenario. Customer-research analysis encounters verified interviews, CRM notes, synthetic test conversations, duplicated social content, spam/test accounts, drafts, superseded studies, and unknown-provenance objects.

Knowledge Governance. Synthetic data is ISOLATED, prohibited users EXCLUDED, drafts and unknown provenance QUARANTINED, superseded material EXCLUDED, and trusted customer evidence prioritized.

Analysis Governance. The analytical plan may deduplicate/group repeated narratives, sample under declared rules, preserve provenance, and reprocess results if contaminated source material is later invalidated.

Consequence Governance. Normally INFORM. A material contamination discovered after prior analysis can force reprocessing or DECIDE if a human owner must determine whether an existing decision remains valid.

Demonstrates. Contamination control, lifecycle, sampling/aggregation governance, provenance propagation, and derived-result invalidation.

# C.4 Internal-First Strategic Research

Scenario. A company asks for product strategy while deliberately requiring approved internal research to establish the initial frame and external evidence to challenge it.

Knowledge Governance. Approved internal research is PRIMARY and high priority; verified customer interviews are CORROBORATING; industry research is comparative/contextual; public web is supplementary; drafts and unverified sources are restricted.

Analysis Governance. The analysis must not equate priority with authority. External evidence must remain able to challenge internal theses; contradictions are preserved and explained.

Consequence Governance. Usually INFORM, but a policy can route materially conflicted recommendations to DECIDE for a strategy owner.

Demonstrates. Case-specific priority, institutional knowledge ordering, corroboration, contradiction preservation, and priority/authority separation.

# C.5 Human Validation During Analysis

Scenario. A classification resembles the RAF reliability gate: an automated analytical result falls below a policy threshold before it is allowed to become a governed result.

Knowledge Governance. Only verified, admissible source material enters the classification.

Analysis Governance. CLASSIFY is permitted, but confidence below 0.80 triggers human validation inside Analysis Governance. The human is validating the analytical result, not owning the downstream business decision.

Consequence Governance. Consequence routing is paused. After successful validation, the result may INFORM or enter another consequence rule.

Demonstrates. Human-in-the-loop validation as an Analysis Governance control distinct from DECIDE. This generalizes the earlier RAF concept of a reliability threshold that routes low-confidence output to human verification \[17\].

# C.6 Human Decision Boundary

Scenario. A system scores a high-risk transaction using governed evidence. The analysis is reliable, but organizational policy does not allow the AI to own the consequential decision.

Knowledge Governance. Required source and provenance rules are satisfied.

Analysis Governance. The permitted scoring method produces a verified high-risk result with an explanation and preserved evidence trace.

Consequence Governance. DECIDE. The risk officer owns APPROVE, DENY, INVESTIGATE, REQUEST_EVIDENCE, or ESCALATE.

Demonstrates. Decision rights: the AI may analyze and recommend without being authorized to make the consequential choice.

# C.7 Autonomous Machine / API Action

Scenario. A lead-qualification workflow determines with high confidence that a verified lead is eligible for an approved campaign.

Knowledge Governance. Consent/customer evidence and qualification data are admitted under policy.

Analysis Governance. The approved CLASSIFY method evaluates eligibility; confidence and evidence requirements are satisfied.

Consequence Governance. ACT. A task-scoped capability grant authorizes one \`crm.add_campaign_member\` API action for the active Case. The executor may be an agent or ordinary API client.

Demonstrates. Agentic/machine execution without making agents the core architecture; action authorization, case scope, API consequence, and audit.

# C.8 Human Approval Followed by Machine Action

Scenario. A support system recommends a EUR 420 refund. Policy permits automatic refunds only below a lower threshold.

Knowledge Governance. The case file and customer/account evidence are governed normally.

Analysis Governance. The refund amount and eligibility are calculated under approved rules.

Consequence Governance. DECIDE -\> ACT. A support manager approves; only then does a capability grant authorize the billing API to issue the refund.

Demonstrates. Human authorization of machine execution, responsibility assignment, and auditable transition from DECIDE to ACT.

# C.9 CROSS-CASE COVERAGE

| **Case**               | **Primary knowledge concern** | **Primary analysis concern** | **Consequence**          |
|------------------------|-------------------------------|------------------------------|--------------------------|
| 1 Regulatory           | Authority/applicability       | Governing-source reasoning   | INFORM or DECIDE         |
| 2 EU routing           | Classification/jurisdiction   | Model/region eligibility     | INFORM                   |
| 3 Contamination        | Lifecycle/provenance          | Sampling/dedup/reprocessing  | INFORM or DECIDE         |
| 4 Internal-first       | Priority/evidence role        | Corroboration/challenge      | INFORM or DECIDE         |
| 5 Validation           | Evidence sufficiency          | Human validation threshold   | Paused then INFORM/other |
| 6 Human boundary       | Required evidence             | Risk scoring/explanation     | DECIDE                   |
| 7 Machine action       | Consent/qualification data    | Eligibility classification   | ACT                      |
| 8 Approval then action | Case/account evidence         | Refund calculation           | DECIDE -\> ACT           |

# C.10 ILLUSTRATIVE DOMAIN GOVERNANCE PROFILES

A Profile packages reusable ADGL semantics for a domain or purpose. The following examples are illustrative and non-normative. They are intentionally described as governance/control profiles rather than compliance certifications.

| **Illustrative profile**   | **Potential contents**                                                                                 | **Boundary**                                                          |
|----------------------------|--------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| Sovereign Processing       | model/region eligibility, local-only processing, transfer constraints, no fallback, audit              | Implements organizational policy; does not infer law automatically.   |
| Life Sciences Evidence     | evidence hierarchy, provenance, scientific/regulatory distinction, validation and DECIDE gates         | Not a regulatory compliance guarantee.                                |
| Financial AI Controls      | decision rights, transaction/action limits, traceability, human approval, model controls               | External legal mapping remains informative unless separately assured. |
| Agent Least Privilege      | registered executor identity, task-scoped grants, action limits, delegation restrictions, action audit | Discovery/enforcement may require external infrastructure.            |
| Regulatory Control Mapping | mapping of ADGL technical controls to selected external requirements                                   | Mapping is informative and requires maintenance/review.               |

These Profiles also illustrate a possible ecosystem model: the open standard defines how Profiles are represented, while organizations, industry groups, or commercial maintainers may publish specialized, versioned policy bundles and conformance fixtures. The standard should remain neutral regarding who publishes them.
