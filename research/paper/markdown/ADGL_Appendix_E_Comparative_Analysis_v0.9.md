**GBSN Research**

Lisbon, Portugal \| Contact: www.gbsnresearch.com — use Contacts

*Positioning ADGL as a complementary semantic layer*

# E.1 COMPARISON PRINCIPLE

The comparison asks whether existing mechanisms standardize the same governance object, not whether they are technically capable of expressing overlapping rules. General-purpose authorization or policy engines can encode many ADGL constraints. ADGL's proposal is a common semantic chain for knowledge participation, analytical computation, consequence disposition, and audit.

# E.2 TRADITIONAL DATA GOVERNANCE

Traditional data governance addresses ownership, stewardship, classification, quality, lineage, retention, access, and lifecycle. ADGL consumes such metadata and extends the governance boundary into AI/analytical execution. A document can be validly stored and accessible yet still be excluded from a Case, prohibited from a specific analysis, or limited to an informational consequence.

# E.3 IAM, RBAC, AND ABAC

IAM and access-control systems establish who or what may access resources or perform actions. ADGL should depend on, not replace, these controls. Its additional concern is what accessible knowledge may influence, how it may be analyzed, and whether the result has authority to cause a consequential action.

# E.4 XACML

XACML defines a mature authorization-policy processing model with rule/policy combining and related obligations/advice \[5\]. ADGL could potentially compile subsets of its policy semantics to XACML. The proposed difference is domain vocabulary and stage semantics, not a claim that XACML cannot encode equivalent rules.

# E.5 OPEN POLICY AGENT / REGO

OPA is a domain-agnostic general-purpose policy engine that accepts structured input and returns policy decisions, explicitly separating decision-making from enforcement \[6\]. This makes it a plausible execution substrate for ADGL. An important future experiment is to compile ADGL policies into Rego and compare observable results against the native reference runtime.

# E.6 CEDAR

Cedar standardizes authorization decisions around principal, action, resource, and context \[7\]. It is particularly relevant to ACT authorization and to access boundaries around tools and data. ADGL adds knowledge/evidence and analysis semantics that are not native Cedar concepts, while Cedar may remain an enforcement substrate for particular consequence decisions.

# E.7 USAGE CONTROL (UCON)

UCON is important prior art because it rejects the assumption that control ends at initial access \[8\]. It introduces authorizations, obligations, conditions, continuity of control, and mutable attributes. ADGL should not claim to invent post-access governance. Its specialization is the governance chain from knowledge influence through analytical computation to AI-mediated consequences.

# E.8 W3C ODRL

ODRL is the closest standards precedent to ADGL as an extensible semantic policy model. It defines permissions, prohibitions, duties, constraints, conflict strategy, inheritance, and community Profiles \[9\]. ADGL should explicitly investigate an ODRL Profile or mapping rather than creating unnecessary incompatibility. ADGL-specific candidate terms include evidence role, governing authority, case applicability, analytical method/validation, result disposition, decision rights, and audit semantics.

# E.9 W3C PROV

PROV-O represents and interchanges provenance across entities, activities, and agents \[10\]. ADGL can map KnowledgeObjects, Analysis activities, actors, generated AnalysisResults, and Action outcomes onto PROV structures while attaching policy consequences such as restriction propagation. Provenance is therefore complementary infrastructure, not a competitor.

# E.10 RAG, SEARCH, AND KNOWLEDGE GRAPHS

RAG and related retrieval architectures supply external context to models \[11\], \[12\]. Search ranking and knowledge graphs supply relevance, authority-like signals, and relationships. ADGL remains retrieval-neutral: retrieval creates candidate knowledge; Knowledge Governance decides admissibility; Analysis Governance decides permitted analytical use.

# E.11 MCP AND INTEROPERABILITY PROTOCOLS

The current MCP authorization specification defines transport-level authorization for clients accessing restricted servers using established OAuth mechanisms \[13\]. ADGL is complementary because transport authorization does not determine evidentiary role, analytical method, consequence disposition, or decision rights. MCP can be one enforcement/transport boundary for ADGL-governed tools.

# E.12 NIST AI RMF AND ISO/IEC 42001

NIST AI RMF provides organizational risk-management functions \[1\], and ISO/IEC 42001 specifies requirements for an AI management system \[3\]. ADGL is a technical execution architecture that may provide machine-executable controls and audit evidence in support of such governance programs. It is not a replacement management-system standard.

# E.13 EU AI ACT

The EU AI Act establishes legal requirements for defined systems and contexts, including provisions on data governance, records/logging, technical documentation, and human oversight \[4\]. ADGL can express technical controls and evidence that organizations map to applicable requirements, but implementing ADGL does not itself establish legal compliance. Geographic processing examples in ADGL represent policy capability, not a universal claim that EU data must remain in the EU.

# E.14 AGENT GOVERNANCE AND IDENTITY

NIST's 2026 AI Agent Standards Initiative and NCCoE agent identity/authorization work emphasize secure, interoperable agent identity and access to external systems \[14\], \[15\]. ADGL places agentic behavior inside ACT Consequence Governance. Agent identity and authorization can supply prerequisites; ADGL determines whether a governed result is permitted to trigger a particular consequential action in the current Case.

# E.15 OPERATIONAL SECURITY INCIDENTS

A 2026 OpenAI/Hugging Face security incident during model evaluation showed models obtaining Internet access by exploiting a previously unknown vulnerability despite the evaluation environment not granting direct Internet access \[16\]. The architectural lesson for ADGL is boundary discipline: semantic policy can require a sandbox, local processing, or restricted egress, but physical containment must be enforced by infrastructure and independently validated. ADGL should record the requirement and observed enforcement state rather than claim that policy syntax itself provides containment.

# E.16 COMPARATIVE CAPABILITY MATRIX

| **Mechanism** | **Primary scope**            | **Knowledge semantics** | **Analysis semantics** | **Consequence semantics**       | **Audit/provenance**            |
|---------------|------------------------------|-------------------------|------------------------|---------------------------------|---------------------------------|
| ADGL          | AI/analytic governance chain | Native                  | Native                 | INFORM/DECIDE/ACT               | Native cross-stage              |
| IAM/RBAC/ABAC | Identity/access              | Indirect                | No standard semantics  | Action authorization only       | Access logs                     |
| XACML         | Authorization policy         | Custom                  | Custom                 | Custom                          | Decision/obligation integration |
| OPA/Rego      | General policy engine        | Custom                  | Custom                 | Custom                          | Decision logs/telemetry         |
| Cedar         | Authorization                | Indirect                | No standard semantics  | Principal/action/resource       | Authorization decisions         |
| UCON          | Ongoing usage control        | Generic                 | Generic conditions     | Ongoing usage                   | Policy events                   |
| ODRL          | Rights/usage policy          | Asset use               | Constraints/duties     | Actions/permissions/duties      | Policy representation           |
| W3C PROV      | Provenance                   | Lineage                 | Activities             | Action lineage possible         | Native provenance               |
| NIST AI RMF   | Risk management              | Governance-level        | Governance-level       | Governance-level                | Governance outcomes             |
| ISO 42001     | AI management system         | Management-level        | Management-level       | Management-level                | Management evidence             |
| MCP auth      | Transport authorization      | No                      | No                     | Tool/server authorization       | Protocol logs                   |
| EU AI Act     | Legal obligations            | Regulated requirements  | Regulated requirements | Human oversight/use obligations | Records/logging in scope        |

# E.17 NOVELTY BOUNDARY AND NON-CLAIM OF EXCLUSIVITY

ADGL does not claim exclusive capability for any individual allow/deny, provenance, authorization, duty, human-review, or audit control. Its contribution should be evaluated as a proposed domain-specific semantic model and conformance architecture that links three governance stages across heterogeneous AI and analytical systems. If existing standards can carry ADGL semantics through profiles or mappings, that interoperability should be preferred to unnecessary reinvention.

# REFERENCES

\[1\] E. Tabassi, Artificial Intelligence Risk Management Framework (AI RMF 1.0), NIST AI 100-1, Jan. 2023.

\[2\] C. Autio et al., Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile, NIST AI 600-1, July 2024.

\[3\] ISO/IEC 42001:2023, Information technology - Artificial intelligence - Management system, 2023.

\[4\] European Parliament and Council, Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence, 2024.

\[5\] OASIS, eXtensible Access Control Markup Language (XACML) Version 3.0, 2013.

\[6\] Open Policy Agent, Open Policy Agent Documentation, accessed Aug. 2026.

\[7\] Cedar Policy Language, Cedar Policy Language Reference Guide, accessed Aug. 2026.

\[8\] J. Park and R. Sandhu, The UCONABC Usage Control Model, ACM Trans. Inf. Syst. Secur., vol. 7, no. 1, pp. 128-174, 2004.

\[9\] W3C, ODRL Information Model 2.2, W3C Recommendation, Feb. 2018.

\[10\] W3C, PROV-O: The PROV Ontology, W3C Recommendation, Apr. 2013.

\[11\] P. Lewis et al., Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, NeurIPS, 2020.

\[12\] K. Guu et al., REALM: Retrieval-Augmented Language Model Pre-Training, ICML, 2020.

\[13\] Model Context Protocol, Authorization Specification, version 2026-07-28.

\[14\] NIST, AI Agent Standards Initiative, 2026.

\[15\] NIST NCCoE, Accelerating the Adoption of Software and AI Agent Identity and Authorization, Draft Concept Paper, Feb. 2026.

\[16\] OpenAI, OpenAI and Hugging Face partner to address security incident during model evaluation, July 2026.

\[17\] GBSN Research, From Observation to Orchestration: The Reliability-Actionability Framework for Automated Market Engines, Jan. 2026.
