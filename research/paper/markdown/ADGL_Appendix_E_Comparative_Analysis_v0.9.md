**ADGL Appendix E - Comparative Analysis of Existing Governance
Mechanisms**

**GBSN Research**

Lisbon, Portugal \| Correspondence: publications@gbsnresearch.com

*Academic preprint edition \| Public Research Release 0.4.3*

Positioning ADGL as a complementary execution-semantic layer

# E.1 Comparison Principle

The comparison asks whether existing mechanisms standardize the same
governance object, not whether they are technically capable of
expressing overlapping rules. General-purpose policy systems can encode
many ADGL constraints, provenance systems can represent lineage,
AI-management standards can define organizational controls, and emerging
agent-governance systems can mediate actions. ADGL's narrower hypothesis
is that a shared semantic chain spanning knowledge influence, analytical
computation, consequence disposition, and end-to-end audit is useful
across those mechanisms.

# E.2 Traditional Data Governance and Documentation

Traditional data governance addresses ownership, stewardship,
classification, quality, lineage, retention, access, and lifecycle. Data
Statements, Datasheets for Datasets, and Model Cards add structured
documentation of origin, composition, intended use, evaluation, and
limitations \[11\]-\[13\]. ADGL consumes such information as policy
context but adds a runtime question: given this Case, may this object
influence this computation, under what evidentiary role, and with what
downstream restrictions? Documentation therefore supplies facts; ADGL
proposes decision semantics over those facts.

# E.3 IAM, RBAC, ABAC, XACML, OPA, and Cedar

IAM and access-control systems establish who or what may access a
resource or invoke an action. XACML defines a mature
authorization-policy processing model with combining algorithms and
obligations/advice \[1\]. OPA separates policy decision-making from
enforcement through declarative Rego \[2\]. Cedar evaluates
principal-action-resource-context authorization requests \[3\]. These
mechanisms are plausible substrates for ADGL decisions. The additional
ADGL vocabulary concerns evidentiary role, applicability, analytical
method, validation, consequence disposition, decision ownership, and
action capability; ADGL does not claim that general policy engines are
incapable of encoding such conditions.

# E.4 Usage Control and Information-Flow Control

UCON is important prior art because it rejects the assumption that
governance ends at initial access, adding ongoing authorizations,
obligations, conditions, continuity, and mutable attributes \[4\].
Information-flow systems such as SIF likewise track confidentiality and
integrity as information propagates through applications rather than
treating access as the only control boundary \[5\]. ADGL should
therefore not claim novelty from persistent or post-access control. Its
specialization is the decomposition of AI/analytical execution into
Knowledge, Analysis, and Consequence stages with explicit decision
rights and stage-qualified audit.

# E.5 W3C ODRL and Rights Expression

ODRL defines permissions, prohibitions, duties, constraints, conflict
strategies, inheritance, and extensible Profiles \[6\]. It is a close
standards precedent for expressing usage policy over assets. ADGL should
investigate an ODRL Profile or mapping rather than create unnecessary
incompatibility. Candidate ADGL-specific terms include evidence role,
governing authority, Case applicability, analytical method and
validation state, result disposition, human decision right, action
capability, and audit-stage semantics.

# E.6 W3C PROV and Provenance Infrastructure

PROV-O represents entities, activities, agents, generation, use,
derivation, and attribution \[7\]. ADGL can map KnowledgeObjects,
Analysis activities, AnalysisResults, HumanDecisions, and Action
outcomes into PROV structures while attaching policy meaning such as
admissibility or restriction propagation. Provenance answers where an
object came from and how it was produced; ADGL asks what that provenance
permits in a current Case. The two are complementary.

# E.7 Retrieval-Augmented Systems and Knowledge Infrastructure

REALM and RAG demonstrate how external, non-parametric knowledge can
become operational inside model inference \[8\], \[9\]. Search ranking,
vector similarity, and knowledge-graph relationships can supply
candidate objects and relevance signals. ADGL remains retrieval-neutral
because retrieval is not treated as admission: a correctly retrieved
object may still be superseded, inapplicable, quarantined, restricted,
or permitted only in a limited evidentiary role.

# E.8 Production ML Engineering and Accountability

Production-ML research identifies hidden data dependencies, feedback
loops, undeclared consumers, system entanglement, and monitoring gaps
that are not visible in model accuracy alone \[14\]-\[16\].
Algorithmic-auditing research likewise argues for end-to-end
accountability processes and infrastructure rather than isolated model
evaluation \[17\], \[18\]. ADGL aligns with this system-level
perspective but focuses on a narrower unit: the runtime governance
trajectory of a policy-bound Case.

# E.9 Human-Automation Interaction and Decision Authority

Parasuraman, Sheridan, and Wickens distinguish automation of information
analysis, decision/action selection, and action implementation \[19\].
Bainbridge and Endsley/Kiris show that nominal human oversight can
become fragile when automation leaves operators out of the loop or
responsible primarily for abnormal takeover \[20\], \[21\]. ADGL's
INFORM, DECIDE, and ACT vocabulary is consistent with the need to
distinguish informational output, human-owned consequential choice, and
machine implementation, while separately allowing human validation
inside Analysis Governance.

# E.10 MCP, Tool Use, and Agent Identity

MCP standardizes interfaces and authorization mechanisms for clients
accessing resources and tools \[22\]. NIST's 2026 AI Agent Standards
Initiative and NCCoE identity/authorization project emphasize secure
interoperability, agent identity, authentication, authorization, and
access to diverse datasets, tools, and applications \[23\], \[24\].
These mechanisms supply transport and identity prerequisites. ADGL
treats agentic behavior as one ACT consequence and asks whether a
governed result is permitted to authorize a specific action in the
current Case.

# E.11 Emerging Runtime Governance for Agents

Several recent proposals are directly relevant and narrow ADGL's novelty
boundary. Policy Cards encode deployment-layer runtime constraints and
audit hooks for autonomous agents \[25\]. AgentSpec supplies a DSL for
customizable runtime enforcement \[26\]. Policies on Paths models
compliance over partial agent trajectories and organizational state
\[27\]. Safety Sidecar adds a portable runtime controller with external
verification before action release and memory updates \[28\]. Zwerdling
et al. compile company-policy documents into deterministic guards linked
to tool use \[29\]. These works provide stronger agent/action-focused
runtime controls than ADGL currently demonstrates. ADGL's proposed
distinction is broader scope: upstream Knowledge and Analysis governance
plus a consequence model that includes informational and human-decision
outcomes, not only autonomous action.

# E.12 Prompt Injection and Tool-Layer Security

Indirect prompt injection demonstrates that retrieved content can
influence instructions and downstream API behavior \[10\]. This problem
is not solved by a governance vocabulary alone. ADGL can provide
explicit places to attach controls - source integrity and isolation
during Knowledge Governance, method/tool and instruction boundaries
during Analysis Governance, and bounded action authorization in
Consequence Governance - while specialized security systems enforce the
technical boundary.

# E.13 NIST AI RMF, ISO/IEC 42001, and the EU AI Act

NIST AI RMF and its Generative AI Profile provide organizational
risk-management structures and risk actions \[30\], \[31\]. ISO/IEC
42001 specifies requirements for an organizational AI management system
\[32\]. The EU AI Act establishes legal requirements for defined systems
and uses, including risk management, data governance, documentation,
logging, transparency, and human oversight \[33\]. ADGL can express and
record technical controls that an organization maps to such obligations,
but use of ADGL does not establish legal compliance or management-system
conformity.

# E.14 Contemporary Agent-Security Evidence

A July 2026 OpenAI/Hugging Face incident during model evaluation
illustrates the distinction between semantic requirements and physical
enforcement. OpenAI reports that models in a restricted cyber evaluation
chained vulnerabilities to obtain Internet access and reach Hugging Face
production infrastructure \[34\]. The public account remains
preliminary. The relevant comparison is therefore limited: a governance
rule may require a sandbox, region, or no-fallback condition, but
containment must be enforced and observed by infrastructure. NIST's 2026
analysis of public comments on agent security similarly reports broad
concern that existing cybersecurity practices need adaptation for agent
systems \[35\].

# E.15 Comparative Capability Matrix

| **Mechanism**                                 | **Primary scope**                       | **Knowledge**                     | **Analysis**                     | **Consequence**                        | **Audit / provenance** |
|-----------------------------------------------|-----------------------------------------|-----------------------------------|----------------------------------|----------------------------------------|------------------------|
| ADGL                                          | Execution-semantic chain                | Native evidence roles/admission   | Native method/model/validation   | INFORM / DECIDE / ACT                  | Cross-stage audit      |
| IAM / RBAC / ABAC                             | Identity and entitlement                | Indirect                          | No common analytical semantics   | Action entitlement                     | Access/audit logs      |
| XACML / OPA / Cedar                           | General authorization/policy evaluation | Custom                            | Custom                           | Custom / action authorization          | Decision telemetry     |
| UCON / information-flow control               | Ongoing usage and propagation           | Generic/persistent control        | Generic conditions               | Ongoing usage                          | Policy/flow events     |
| ODRL                                          | Rights and usage policy                 | Asset use / constraints           | Constraints/duties               | Actions/permissions/duties             | Policy representation  |
| W3C PROV                                      | Provenance and derivation               | Lineage                           | Activities                       | Action lineage possible                | Native provenance      |
| Datasheets / Data Statements / Model Cards    | Documentation/transparency              | Rich metadata                     | Evaluation/intended-use metadata | No runtime consequence model           | Documentation record   |
| NIST AI RMF / ISO 42001 / EU AI Act           | Risk, management, legal obligations     | Governance-level                  | Governance-level                 | Governance/human-oversight obligations | Governance evidence    |
| MCP / agent identity                          | Transport/tool/resource authorization   | No evidence semantics             | No common analytical semantics   | Tool/server authorization              | Protocol logs          |
| Policy Cards / AgentSpec / path/guard systems | Runtime autonomous-agent control        | Some evidence/context constraints | Trajectory/guard-specific        | Strong action/tool mediation           | Runtime/audit hooks    |

# E.16 Novelty Boundary and Non-Claim of Exclusivity

ADGL does not claim to invent allow/deny policy, post-access control,
provenance, obligations, dataset/model documentation, human review,
action authorization, runtime interception, or audit. Recent
runtime-governance research makes especially clear that policy
enforcement for autonomous agents is already an active field. The
proposed contribution should instead be evaluated as a domain-specific
semantic composition: a shared Case-scoped chain that distinguishes what
may influence computation, what analysis is permitted, and what
consequence rights attach to the resulting analysis, with audit across
all stages.

This is a falsifiable and deliberately conservative novelty claim. If
existing standards can carry the same semantics through profiles or
mappings with equivalent conformance behavior, interoperability is
preferable to a parallel ecosystem. If independent implementations
cannot agree on the meaning of the proposed states and transitions, the
standardization hypothesis is weakened.

# E.17 Interoperability and Research Agenda

- Formalize mappings or profiles for ODRL permissions, duties,
  constraints, and inheritance.

- Compile a defined portable subset to XACML, Rego, and/or Cedar and
  test cross-engine equivalence.

- Map KnowledgeObjects, Analysis activities, results, human decisions,
  and actions to W3C PROV.

- Define MCP/tool integration guidance that separates transport
  authorization from semantic action authorization.

- Compare ADGL ACT semantics empirically with AgentSpec, Policy Cards,
  path-based runtime policies, and action-guard systems rather than
  relying only on conceptual comparison.

- Conduct independent implementation and adversarial
  cross-implementation conformance testing.

- Evaluate whether human DECIDE Profiles create meaningful oversight
  rather than nominal checkpoints.

# E.18 EVIDENTIARY LIMIT OF THE COMPARISON

The comparisons in this appendix are analytical feature and scope
comparisons. They do not constitute completed semantic translations,
empirical interoperability experiments, or evidence that established
mechanisms cannot represent ADGL cases.

The decisive next evaluation remains a full mapping of representative
ADGL cases to Rego/OPA or Cedar and to ODRL plus PROV, followed by
third-party implementation of shared test vectors. Until then,
compositional portability and interoperability remain design hypotheses.

# References

\[1\] OASIS, eXtensible Access Control Markup Language (XACML) Version
3.0, OASIS Standard, 2013.

\[2\] Open Policy Agent, Policy Language and Authorization
Documentation, accessed Aug. 2026.

\[3\] Cedar Policy Language, Cedar Policy Language Reference Guide,
version 4.5, accessed Aug. 2026.

\[4\] J. Park and R. Sandhu, "The UCONABC Usage Control Model," ACM
Transactions on Information and System Security, vol. 7, no. 1, pp.
128-174, 2004.

\[5\] S. Chong, K. Vikram, and A. C. Myers, "SIF: Enforcing
Confidentiality and Integrity in Web Applications," 16th USENIX Security
Symposium, 2007.

\[6\] W3C, ODRL Information Model 2.2, W3C Recommendation, Feb. 2018.

\[7\] W3C, PROV-O: The PROV Ontology, W3C Recommendation, Apr. 2013.

\[8\] K. Guu et al., "REALM: Retrieval-Augmented Language Model
Pre-Training," ICML, 2020.

\[9\] P. Lewis et al., "Retrieval-Augmented Generation for
Knowledge-Intensive NLP Tasks," NeurIPS, 2020.

\[10\] K. Greshake et al., "More than you've asked for: A Comprehensive
Analysis of Novel Prompt Injection Threats to Application-Integrated
Large Language Models," arXiv:2302.12173, 2023.

\[11\] E. M. Bender and B. Friedman, "Data Statements for Natural
Language Processing," TACL, vol. 6, pp. 587-604, 2018.

\[12\] T. Gebru et al., "Datasheets for Datasets," Communications of the
ACM, vol. 64, no. 12, pp. 86-92, 2021.

\[13\] M. Mitchell et al., "Model Cards for Model Reporting," FAT\*
2019, pp. 220-229, 2019.

\[14\] D. Sculley et al., "Hidden Technical Debt in Machine Learning
Systems," NeurIPS, 2015.

\[15\] E. Breck et al., "The ML Test Score," IEEE Big Data, 2017.

\[16\] S. Amershi et al., "Software Engineering for Machine Learning: A
Case Study," ICSE SEIP, 2019.

\[17\] I. D. Raji et al., "Closing the AI Accountability Gap," FAT\*
2020, 2020.

\[18\] V. Ojewale et al., "Towards AI Accountability Infrastructure:
Gaps and Opportunities in AI Audit Tooling," arXiv:2402.17861, revised
2025.

\[19\] R. Parasuraman, T. B. Sheridan, and C. D. Wickens, "A Model for
Types and Levels of Human Interaction with Automation," IEEE SMC-A, vol.
30, no. 3, pp. 286-297, 2000.

\[20\] L. Bainbridge, "Ironies of Automation," Automatica, vol. 19, no.
6, pp. 775-779, 1983.

\[21\] M. R. Endsley and E. O. Kiris, "The Out-of-the-Loop Performance
Problem and Level of Control in Automation," Human Factors, vol. 37, no.
2, pp. 381-394, 1995.

\[22\] Model Context Protocol, Authorization Specification, version
2026-07-28, 2026.

\[23\] National Institute of Standards and Technology, AI Agent
Standards Initiative, 2026.

\[24\] H. Booth, B. Fisher, R. Galluzzo, and J. Roberts, Accelerating
the Adoption of Software and AI Agent Identity and Authorization, NCCoE
Draft Concept Paper, Feb. 2026.

\[25\] J. Mavračić, "Policy Cards: Machine-Readable Runtime Governance
for Autonomous AI Agents," arXiv:2510.24383, 2025.

\[26\] H. Wang, C. M. Poskitt, and J. Sun, "AgentSpec: Customizable
Runtime Enforcement for Safe and Reliable LLM Agents," arXiv:2503.18666,
2025.

\[27\] M. Kaptein, V.-J. Khan, and A. Podstavnychy, "Runtime Governance
for AI Agents: Policies on Paths," arXiv:2603.16586, 2026.

\[28\] B. Wang et al., "Safety Sidecar: Reflection-Driven Runtime
Control for Safer Agents," Findings of ACL 2026, pp. 30842-30856, 2026.

\[29\] N. Zwerdling et al., "Towards Enforcing Company Policy Adherence
in Agentic Workflows," EMNLP 2025 Industry Track, pp. 595-606, 2025.

\[30\] E. Tabassi, Artificial Intelligence Risk Management Framework (AI
RMF 1.0), NIST AI 100-1, 2023.

\[31\] C. Autio et al., Artificial Intelligence Risk Management
Framework: Generative Artificial Intelligence Profile, NIST AI 600-1,
2024.

\[32\] ISO/IEC 42001:2023, Information technology - Artificial
intelligence - Management system, 2023.

\[33\] European Parliament and Council, Regulation (EU) 2024/1689 laying
down harmonised rules on artificial intelligence, 2024.

\[34\] OpenAI, "OpenAI and Hugging Face partner to address security
incident during model evaluation," July 21, 2026, with updates through
July 29, 2026.

\[35\] J. Riggs, M. Hamin, N. Perry, B. Edelman, and P. Cihon, Summary
Analysis of Responses to the Request for Information Regarding Security
Considerations for AI Agents, NIST AI 800-5, May 2026.
