AI Data Governance Layer (ADGL):  
Governing Knowledge, Analysis, and Consequences in Model-Agnostic AI
Systems  
Submission Draft v1.2

GBSN Research

Lisbon, Portugal \| Correspondence: publications@gbsnresearch.com

Abstract - Artificial intelligence systems increasingly operate as
execution chains rather than isolated models: they retrieve or receive
information, transform that information through one or more analytical
procedures, and then return, recommend, or trigger consequential
outcomes. Existing governance mechanisms address important parts of this
chain - including organizational risk, access control, usage rights,
provenance, model documentation, human oversight, and agent
authorization - but they do not by themselves provide a shared runtime
semantic contract for three distinct questions: what knowledge may
influence a case, what analysis may be performed on that knowledge, and
what consequence a governed result may produce. This paper develops the
AI Data Governance Layer (ADGL) as a model-, storage-, retrieval-, and
enforcement-agnostic policy architecture organized into Knowledge
Governance, Analysis Governance, and Consequence Governance, with Audit
and Provenance as a cross-cutting plane. The architecture is derived
from a synthesis of prior work in usage control, information-flow
control, provenance, data/model documentation, production ML
engineering, algorithmic auditing, human-automation interaction,
retrieval-augmented systems, prompt-injection research, and current
agent-security standardization. ADGL distinguishes INFORM, DECIDE, and
ACT consequences so that informational systems, human-owned decisions,
and machine-executable actions can share one semantic architecture
without making autonomous action the default. An executable reference
toolkit implements the proposed semantics through eight reference cases
and 25 published normative conformance checks; a later toolkit revision
adds 11 candidate execution-integrity checks that are reported
separately from the normative evaluation. The paper presents the design
requirements, formal execution model, implementation boundaries, initial
performance characterization, comparative positioning, limitations, and
open questions relevant to possible standardization.

Keywords - AI governance; data governance; knowledge governance;
analysis governance; decision rights; policy-as-code; provenance; human
oversight; autonomous action; AI agents; conformance; runtime
governance.

# 1. Introduction

Artificial intelligence systems are increasingly embedded in information
pipelines, analytical services, decision-support tools, and workflow
automation. In such systems, the model is only one component of a larger
execution path. A request may cause retrieval from internal or external
sources, aggregation of evidence, transformation or inference, model
selection, human review, and - in some deployments - an external side
effect such as an API call, database update, workflow transition, or
message. This expansion changes the governance problem. The relevant
question is no longer only whether a user or service may access a
resource; it is also whether that resource may influence a particular
analysis, whether the chosen analytical procedure is permitted, and
whether the resulting output carries authority to cause something beyond
being displayed or stored.

The distinction is not merely terminological. Access control, usage
control, and information-flow control established long before current
generative AI that authorization at an initial boundary does not exhaust
the problem of governing information after access \[5\], \[8\], \[11\].
More recent work on dataset documentation, model reporting, production
ML engineering, and algorithmic auditing similarly shows that
reliability and accountability depend on the conditions under which data
and models are selected, transformed, evaluated, and monitored
\[12\]-\[19\]. Human-factors research adds a further distinction:
automation of information analysis and automation of decision or action
selection are separable design choices with different consequences for
human authority, situation awareness, and takeover performance
\[20\]-\[22\]. Current agentic systems make these older distinctions
operationally urgent because models may now interleave reasoning with
retrieval and tool use \[24\], while indirect prompt injection can turn
retrieved content into instructions that alter system behavior \[23\].

The AI Data Governance Layer (ADGL) is proposed as a semantic layer for
this execution chain. It is organized around three stages: Knowledge
Governance, which decides what information may participate and in what
evidentiary role; Analysis Governance, which decides what methods,
models, tools, transformations, and validation conditions may be
applied; and Consequence Governance, which decides what a governed
result may be allowed to cause. Audit and Provenance span the complete
trajectory. Consequence Governance distinguishes INFORM, DECIDE, and
ACT. INFORM produces an informational result without authorizing a
consequential external action. DECIDE assigns the next consequential
choice to a human or accountable role. ACT permits a machine-executable
instruction, subject to explicit authorization and external enforcement.

ADGL is not presented as a replacement for IAM, XACML, OPA, Cedar, UCON,
ODRL, PROV, MCP, NIST AI RMF, ISO/IEC 42001, the EU AI Act, or security
infrastructure. Many of those mechanisms can encode or enforce rules
that overlap with ADGL. The standardization hypothesis is narrower:
heterogeneous AI and analytical systems may benefit from a portable
domain vocabulary and conformance model that preserves the semantic
chain from knowledge influence through analytical computation to
consequence disposition and audit. Appendix E provides the detailed
comparative analysis; this paper focuses on the conceptual derivation,
formal architecture, and initial executable evaluation.

The principal contributions are: (1) an academically grounded
three-stage governance architecture; (2) an explicit distinction between
informational output, human-owned decision authority, and machine
action; (3) a separation between human validation inside analysis and
human decision ownership after analysis; (4) semantics for provenance,
lifecycle, evidentiary role, model/tool eligibility, conflict
preservation, action authorization, and feedback; (5) a Case abstraction
that binds policy to concrete purpose and context; and (6) an executable
reference toolkit with normative conformance cases and reproducible
deterministic performance baselines.

# 2. Problem Context and Research Questions

## 2.1 From data access to execution chains

Classical data governance commonly addresses ownership, stewardship,
classification, quality, lineage, retention, and access. Those concerns
remain necessary, but AI-enabled systems add an execution problem:
technically available information can be selected as evidence,
transformed by a model or algorithm, combined with other sources, and
converted into recommendations or actions. Data quality failures can
propagate downstream as what Sambasivan et al. describe as data cascades
\[15\], while production ML studies show that data dependencies, hidden
feedback loops, undeclared consumers, and system entanglement create
failure modes that are not visible from model accuracy alone \[16\],
\[17\].

Retrieval-augmented systems make the boundary especially explicit. RAG
and REALM demonstrate the benefits of augmenting parametric models with
external knowledge \[14\], \[13\], but retrieval relevance is not
equivalent to governance admissibility. A search engine may correctly
retrieve a draft, superseded policy, low-integrity source, or document
whose jurisdiction does not govern the current case. Documentation
mechanisms such as data statements, datasheets, and model cards improve
transparency about origin, intended use, and limitations \[12\], \[18\],
\[19\], but documentation alone does not decide, at runtime, whether a
particular object may influence a particular case or whether an
analytical result may authorize a downstream action.

## 2.2 Why one governance boundary is insufficient

The architecture begins from four non-equivalences. First, accessible
knowledge is not necessarily admissible evidence. Second, admissible
evidence does not imply permission to apply any analytical method or
model. Third, a valid analytical result does not automatically confer
decision authority. Fourth, a decision that an action is appropriate
does not itself establish technical authorization to execute the action.
Collapsing these distinctions creates hidden authority transfers:
retrieval becomes evidence selection; model invocation becomes
analytical authorization; confidence becomes decision authority; and a
generated tool call becomes permission to act.

Prior governance mechanisms illuminate individual boundaries but are
typically optimized for different objects. XACML, OPA, and Cedar are
general-purpose authorization/policy systems \[5\]-\[7\]. UCON extends
control into ongoing usage and mutable attributes \[8\]. ODRL represents
permissions, prohibitions, duties, and constraints over assets \[9\].
PROV represents lineage and derivation \[10\]. NIST AI RMF and ISO/IEC
42001 operate at organizational risk-management and management-system
levels \[1\]-\[3\]. The EU AI Act imposes legal obligations in defined
contexts \[4\]. MCP standardizes interoperability and transport-level
authorization for tools and resources \[25\]. The question addressed by
ADGL is not whether those mechanisms are expressive; it is whether a
shared execution-specific vocabulary spanning knowledge influence,
analysis, consequence, and audit is useful across them.

## 2.3 Research questions

| **Research question** | **Scope**                                                                                                                                                                         |
|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| RQ1                   | How can governance distinguish information availability from permissible evidentiary influence in heterogeneous AI-enabled systems?                                               |
| RQ2                   | How can governance extend from knowledge selection to the analytical methods, models, tools, and validation processes applied to that knowledge?                                  |
| RQ3                   | How can informational outputs, human-owned decisions, and machine-executable actions be represented within one architecture without treating autonomous execution as the default? |
| RQ4                   | Which semantics must remain observable across different implementation technologies for governance decisions to remain auditable and interoperable?                               |
| RQ5                   | To what extent can the proposed semantics be expressed unambiguously and evaluated through executable conformance tests across implementations?                                   |

# 3. Research Method and Artifact Development

This work is framed as design-science research. It does not report a
systematic review, a controlled experiment, or an empirical case-study
corpus. The artifact-development cycle was: problem identification;
targeted narrative synthesis of governance, authorization, provenance,
production-ML, human-factors, and agent-security literature; formulation
of failure classes; derivation of design requirements; semantic artifact
design; implementation of a reference runtime; conformance evaluation;
and adversarial refinement. The review was purposive rather than
exhaustive: sources were selected for direct relevance to the boundaries
represented by the artifact. This choice supports conceptual synthesis
but does not justify bibliometric completeness claims.

## 3.1 Evidence classification

Evidence is separated by role to avoid treating motivating material,
constructed fixtures, and producer-authored conformance results as
interchangeable forms of validation.

| **Evidence type**               | **Role in this paper**                                                 | **Claim not supported**                       |
|---------------------------------|------------------------------------------------------------------------|-----------------------------------------------|
| Prior literature                | Establishes known governance and system-design problems                | That ADGL is uniquely necessary               |
| Standards and regulation        | Establishes interoperability and control requirements                  | Formal endorsement of ADGL                    |
| Public incidents                | Motivating illustration only                                           | Causal or representative empirical validation |
| Constructed reference scenarios | Tests architecture behavior against declared expectations              | Observed organizational prevalence            |
| Reference implementation        | Shows that the declared semantic subset is executable                  | Production effectiveness or independence      |
| Conformance suite               | Checks consistency between specification, fixtures, and implementation | Cross-implementation interoperability         |
| Microbenchmarks                 | Characterizes one evaluator under stated conditions                    | Comparative or production performance         |

## 3.2 Requirement and artifact-development procedure

The failure classes and requirements were formulated iteratively by GBSN
Research while developing the ADGL specification and related
implementation. They were not independently elicited or coded by
multiple researchers. Requirements R1-R12 therefore function as
transparent design commitments and evaluation targets, not as
independently discovered empirical findings. Candidate requirements
found during implementation hardening remain explicitly non-normative
until reviewed and incorporated through the specification process.
Evidence that would motivate revision includes ambiguous independent
implementations, counterexamples that violate stage separation, mappings
showing no useful semantic difference from established mechanisms, or
stakeholder findings that the proposed vocabulary is not usable.

## 3.3 Traceability and validation scope

Appendices A-D provide the operational trace from semantic objects and
stage behavior to reference cases, expected states, conformance checks,
and implementation results. This traceability demonstrates internal
consistency for the declared subset. Because GBSN Research created the
specification, scenarios, tests, and reference implementation—and has a
commercial interest in ADGL—the evaluation is producer-side validation.
Independent replication and stakeholder evaluation remain required
before claims of practical effectiveness, interoperability, or standards
readiness can be sustained.

## 3.4 Artifact evaluation environments

The artifact was evaluated in two producer-authored implementation
environments with different purposes. The openly licensed Python
Reference Toolkit is a minimal semantic interpreter, schema set, fixture
collection, and conformance runner. KEE (Knowledge Execution Engine) is
a separate, unpublished proprietary commercial MVP developed by GBSN
Research. KEE vendors the paper-evaluated Reference Toolkit 0.5.0
baseline implementing Specification 0.3.0 and adds production-oriented
orchestration around model calls, result release, trust registries,
action authorization, quota accounting, and audit integrity. KEE is not
an independent implementation and is not required to implement ADGL. Its
source and tests were available to the authors for this study but are
not part of the public reproducibility package.

Four internal adversarial implementation-review cycles were used as
formative design-science evaluation. Findings were reproduced as
executable failures before correction. KEE-specific corrections were
kept distinct from the normative open specification. Where a finding
indicated an underspecified portable semantic boundary, it informed
candidate execution-integrity checks C26-C36 in Toolkit 0.5.3. This
process supplies producer-side artifact evidence and negative cases; it
does not establish independent effectiveness, security certification, or
cross-vendor interoperability.

## 3.5 Public reproducibility surfaces

The public materials are distributed through separate research and
executable packages for Zenodo/OSF, a GitHub-ready repository containing
specification sources, schemas, cases, tests, documentation, and
continuous-integration configuration, and Hugging Face dataset and Space
artifacts for interactive execution of the eight constructed reference
cases. The release-validation record reports successful execution of all
eight cases in the Space. The exact repository, DOI, dataset, and Space
identifiers must be recorded in the camera-ready artifact-availability
statement. Public execution demonstrates availability and
reproducibility of the declared cases; it is not field validation.

# 4. Conceptual Foundations and Related Work

## 4.1 Data governance, documentation, and information influence

ADGL's Knowledge Governance builds on a broad lineage rather than
claiming that post-access control is new. Information-flow control
frameworks such as SIF explicitly distinguish confidentiality and
integrity policies from initial access and track how information
propagates through applications \[11\]. UCON similarly generalizes
access control to include obligations, conditions, continuity, and
mutability before, during, and after usage \[8\]. These traditions
establish that control may need to persist after a principal has crossed
an access boundary.

Dataset documentation research adds an orthogonal concern: the meaning
and suitability of data depend on its provenance, composition,
collection context, population, intended uses, and limitations. Bender
and Friedman propose data statements to make population and linguistic
context explicit \[12\]. Gebru et al. propose datasheets to standardize
documentation of dataset motivation, composition, collection, and
recommended uses \[18\]. Sambasivan et al. provide empirical evidence
that neglected data work can create delayed, compounding downstream
failures in high-stakes AI \[15\]. ADGL treats such metadata as policy
inputs, while adding a runtime question: given the current Case, may
this object influence this analysis, and in what evidentiary role?

## 4.2 Authorization, usage control, and rights expression

XACML defines an authorization policy language and processing model with
combining algorithms and obligations/advice \[5\]. OPA separates policy
decision-making from enforcement and evaluates declarative Rego policies
over structured inputs \[6\]. Cedar represents authorization in
principal-action-resource-context terms and is designed for fine-grained
application permissions \[7\]. ODRL provides an extensible information
model for permissions, prohibitions, duties, and constraints over assets
\[9\]. These systems are highly relevant implementation substrates. ADGL
does not claim that they cannot express equivalent conditions. Its
proposed specialization is a shared AI/analytical vocabulary for
evidence role, authority, applicability, analytical method, validation,
consequence disposition, decision ownership, action capability, and
stage-qualified audit.

## 4.3 Provenance and retrieval

W3C PROV provides a domain-independent model for entities, activities,
agents, generation, use, derivation, and attribution \[10\]. ADGL uses
provenance as a cross-cutting dependency rather than a substitute for
policy: provenance can establish where an object came from and how it
was derived, while policy determines what that provenance means for
admissibility, restriction propagation, or consequence.
Retrieval-augmented methods such as REALM and RAG make non-parametric
knowledge operational inside model inference \[13\], \[14\]. That
capability strengthens the case for separating retrieval from admission
because the retrieved set is a technical candidate set, not a governance
decision.

## 4.4 Production ML engineering and accountability

Production ML research repeatedly shows that model-centric evaluation is
insufficient for system reliability. Sculley et al. identify hidden data
dependencies, feedback loops, boundary erosion, and undeclared consumers
as forms of technical debt \[16\]. Breck et al. propose testing and
monitoring requirements for production readiness \[17\]. Amershi et al.
report that production AI development involves difficult data discovery,
management, versioning, model entanglement, and process changes across
software teams \[29\]. These findings motivate governance at the level
of execution conditions rather than only model artifacts.

Algorithmic-auditing research adds an accountability dimension. Raji et
al. argue for end-to-end internal audit processes that preserve
decisions and evidence throughout the development lifecycle \[30\].
Ojewale et al., based on practitioner interviews and a landscape
analysis of audit tools, report gaps between evaluation tooling and the
broader infrastructure needed for accountability \[31\]. ADGL's Audit
and Provenance plane is aligned with this lifecycle perspective, but
focuses on recording the runtime governance trajectory of individual
cases and policy decisions.

## 4.5 Human-automation interaction and decision authority

The distinction between analysis and consequence is strongly supported
by human-factors literature. Parasuraman, Sheridan, and Wickens separate
automation of information acquisition, information analysis,
decision/action selection, and action implementation, and describe
levels at which the human retains, shares, or relinquishes authority
\[20\]. Bainbridge's 'ironies of automation' shows that removing routine
human control can leave people with difficult monitoring and takeover
roles precisely when abnormal conditions occur \[21\]. Endsley and Kiris
experimentally demonstrate out-of-the-loop performance and
situation-awareness losses under higher automation \[22\].

ADGL's INFORM, DECIDE, and ACT dispositions are not a restatement of a
single historical automation scale, but they are consistent with the
underlying insight that producing information, selecting a consequential
decision, and implementing that decision are distinct authority
boundaries. The architecture further separates human validation inside
Analysis Governance from human decision ownership inside Consequence
Governance. A reviewer who validates whether a classification is
analytically sound is performing a different institutional function from
an officer who owns the legal, financial, clinical, or operational
decision that follows.

## 4.6 Agentic systems, tool use, and prompt injection

Recent LLM systems increasingly interleave reasoning with external
actions. ReAct demonstrates the utility of coupling reasoning traces
with actions that query external environments \[24\]. MCP standardizes
interfaces through which LLM applications can access resources and
invoke tools, and its authorization specification focuses on
transport-level authorization using established OAuth mechanisms \[25\].
NIST's 2026 AI Agent Standards Initiative and NCCoE work on agent
identity and authorization identify secure agent interoperability,
authentication, authorization, and prompt-injection mitigation as active
standardization problems \[26\], \[27\].

At the same time, Greshake et al. demonstrate indirect prompt injection:
malicious instructions can be placed in external content that is later
retrieved and processed by an application-integrated LLM, allowing data
to influence system instructions and potentially API behavior \[23\].
This attack class collapses the intuitive boundary between 'content to
analyze' and 'instructions to execute.' ADGL does not by itself solve
prompt injection, but its separation of Knowledge, Analysis, and
Consequence provides places where implementations can attach controls:
source integrity and isolation at admission, method/tool constraints
during analysis, and explicit action authorization before side effects.

## 4.7 Organizational and regulatory governance

NIST AI RMF organizes risk-management practice around GOVERN, MAP,
MEASURE, and MANAGE and treats trustworthy AI as a lifecycle concern
\[1\]. The Generative AI Profile adds risks and actions specific to
generative systems, including governance, content provenance, testing,
and incident disclosure \[2\]. ISO/IEC 42001 specifies requirements for
an organizational AI management system \[3\]. The EU AI Act establishes
legal requirements for defined systems and use contexts, including data
governance, documentation, logging, risk management, transparency, and
human oversight \[4\]. These mechanisms define organizational or legal
outcomes rather than a single execution grammar; ADGL is positioned as a
possible technical layer for implementing and evidencing selected
controls without claiming that its use establishes compliance.

## 4.8 Closely related runtime-governance proposals

Emerging work is moving rapidly toward machine-readable runtime
governance, particularly for autonomous agents. Policy Cards propose
deployment-layer policy artifacts containing allowed or denied actions,
obligations, evidentiary requirements, escalation, and audit hooks
\[28\]. AgentSpec provides a domain-specific language for runtime
constraints over LLM-agent behavior \[34\]. Kaptein, Khan, and
Podstavnychy model runtime governance over partial agent execution
paths, emphasizing that static access control cannot capture
path-dependent policy \[35\]. Safety Sidecar adds a model-agnostic
runtime controller with external verification gates before action
release and memory updates \[36\]. Zwerdling et al. compile
company-policy documents into deterministic guards associated with tool
use in agentic workflows \[37\]. Together, these systems are close prior
work and substantially narrow any novelty claim based merely on 'runtime
governance.'

The distinction proposed by ADGL is therefore one of scope and semantic
decomposition rather than the invention of runtime enforcement. ADGL
treats agentic execution as one ACT consequence among three outcomes,
places Knowledge Governance and Analysis Governance upstream of action
control, and defines a Case-scoped semantic chain intended to apply
equally to informational systems, human-decision workflows, and machine
actions. The emerging agent-governance literature is strongest around
paths, tool calls, action guards, and intervention. ADGL asks the
complementary question of how those controls connect to evidence
admissibility, analytical permission, decision ownership, and provenance
before and after an action. Interoperability with agent-focused runtime
proposals should be preferred over unnecessary duplication.

# 5. Governance Failure Classes and Motivating Scenarios

The architecture was not derived from a single incident or an empirical
case-study corpus. GBSN Research formulated these failure classes
through a targeted literature synthesis and iterative artifact
development. The eight executable cases in Appendix C are internally
constructed reference scenarios designed to expose semantic boundaries;
they are not observations of prevalence or independently sampled
organizational practice. The following classes summarize the design
pressure behind the three-stage separation.

| **Failure mode**                          | **Motivating case**                                                                                                                                                                                                                                                                    | **Architectural response**                                                |
|-------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|
| F1 Accessible ≠ admissible                | A draft, superseded policy, public commentary, and governing regulator notice may all be technically accessible, but should not have equal influence in a regulatory case. Documentation and data-cascade research show why origin, status, and context matter \[12\], \[15\], \[18\]. | Knowledge Governance: authority, applicability, lifecycle, evidence role. |
| F2 Admissible ≠ analyzable                | Restricted data may be valid evidence, while the proposed model, processing region, method, or inference pattern is not permitted. Production-ML work shows that system choices beyond the dataset affect reliability \[16\], \[17\], \[29\].                                          | Analysis Governance: method/model/tool/region eligibility.                |
| F3 Analysis ≠ decision authority          | A high-confidence risk score may be valid while organizational policy requires a human officer to own the consequential decision. Human-automation research distinguishes analysis from decision/action selection \[20\]-\[22\].                                                       | Consequence Governance: DECIDE.                                           |
| F4 Decision ≠ action authorization        | A conclusion that an action should occur does not itself authorize an API, workflow, or financial side effect. Runtime agent-policy work similarly inserts guards before tool/action execution \[34\], \[35\], \[37\].                                                                 | Consequence Governance: ACT + bounded capability.                         |
| F5 Data may become instructions           | Retrieved untrusted content can contain instructions that alter model/tool behavior through indirect prompt injection \[23\].                                                                                                                                                          | Admission integrity + analysis constraints + action authorization.        |
| F6 Derived knowledge inherits risk        | Summaries, classifications, and action outcomes can be stored and reused, creating new governed objects whose lineage and restrictions matter \[10\], \[15\], \[16\].                                                                                                                  | Audit/provenance + restriction propagation + feedback.                    |
| F7 Semantic policy ≠ physical containment | A policy can require local-only processing or no fallback, but actual network/sandbox containment must be enforced and observed by infrastructure; the 2026 OpenAI/Hugging Face incident is a contemporary illustration \[32\].                                                        | Explicit enforcement boundary + audit of enforcement state.               |

## 5.1 A contemporary containment case

A July 2026 OpenAI/Hugging Face security incident provides a
contemporary illustration of F7. OpenAI reports that models in an
internal cyber-capability evaluation, operating in a highly isolated
environment without direct Internet access, identified and chained
vulnerabilities that ultimately provided Internet access and a path into
Hugging Face production infrastructure \[32\]. As of 13 August 2026,
OpenAI describes its public account as preliminary and states that a
fuller technical review is ongoing \[32\]. The appropriate architectural
lesson is therefore limited: semantic rules such as REQUIRE_SANDBOX,
LOCAL_ONLY, or NO_FALLBACK cannot themselves provide physical
containment. A governance layer can state the requirement, require
evidence of enforcement, and block consequences when evidence is absent;
network, sandbox, IAM, and monitoring infrastructure must enforce the
boundary.

## 5.2 Design history and generalization beyond agentic execution

ADGL also reflects an internal design evolution. Earlier GBSN Research
work on the Reliability-Actionability Framework used reliability
thresholds to route uncertain analytical output to human verification
and distinguished monitoring from operational triggers \[33\]. The
original ADGL reference cases concentrated on knowledge admission,
authority, lifecycle, and routing. As the architecture was tested
against human-review and machine-action scenarios, two missing
boundaries became explicit: governance of the analysis itself, and
governance of what the result is allowed to cause. The resulting
three-stage structure generalizes beyond the original agentic framing.
Informational analysis remains a first-class endpoint, human decision
ownership is a separate endpoint, and autonomous or non-human execution
is one consequential path rather than the default architecture.

# 6. Formulated Design Requirements

GBSN Research formulated the following requirements from the targeted
literature synthesis, failure classes, and iterative
artifact-development process described in Section 3. They are design
commitments and evaluation targets for the semantic architecture, not
empirical findings or claims that ADGL is the only possible
implementation.

| **ID** | **Requirement**                                | **Rationale**                                                                                                                                  |
|--------|------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| R1     | Contextual admissibility                       | A Case must determine whether technically available information may influence the current computation.                                         |
| R2     | Provenance-aware influence                     | Origin, lineage, lifecycle, jurisdiction, and integrity metadata must be available to admission policy.                                        |
| R3     | Independent evidence dimensions                | Authority, priority, applicability, and evidentiary role must not collapse into a single relevance score.                                      |
| R4     | Analytical-method governance                   | Permitted computation must be governable independently from permitted input.                                                                   |
| R5     | Model/tool/environment eligibility             | The executor, processing location, fallback behavior, and tool capability may be policy conditions.                                            |
| R6     | Evidence sufficiency and conflict preservation | Policy must be able to require mandatory evidence/corroboration and prevent silent removal of material contradiction.                          |
| R7     | Human validation boundary                      | Uncertain or methodologically weak analysis must be able to pause for validation before it becomes a governed result.                          |
| R8     | Decision-right separation                      | A valid result must not automatically inherit authority to make a consequential organizational decision.                                       |
| R9     | Explicit action authorization                  | Machine execution must require bounded, case-scoped authorization separate from analytical success.                                            |
| R10    | Restriction propagation and feedback           | Derived knowledge and action outcomes must preserve lineage and applicable restrictions when re-entering the system.                           |
| R11    | End-to-end auditability                        | The system must record the policy, inputs, analytical plan, validations, decision rights, actions, and resulting state.                        |
| R12    | Implementation neutrality                      | The semantic contract should be portable across models, storage systems, retrieval mechanisms, policy engines, and enforcement infrastructure. |

# 7. ADGL Conceptual Architecture

ADGL represents an execution as a policy-bound Case moving through three
semantic stages. The stages are observable boundaries, not necessarily
separate microservices. An implementation may fuse them operationally
provided it preserves equivalent decisions and audit semantics.

Fig. 1. ADGL three-stage governance architecture. Policy and Case
context apply across Knowledge, Analysis, and Consequence Governance;
Audit and Provenance span the complete trajectory.

## 7.1 Policy and Case context

A Case binds the governance question to concrete context: purpose,
subject, actors, jurisdiction, classification, time, organizational
state, applicable policy set, and other domain attributes. This prevents
the architecture from assigning global meaning to a source, model, or
action. The same document can be admissible for historical analysis but
excluded from a current regulatory determination; the same model can be
permitted for public information but prohibited for restricted data; the
same API action can be permitted under one workflow and forbidden under
another.

## 7.2 Three governance stages

Knowledge Governance answers what may enter the governed evidence set
and in what capacity. Analysis Governance answers what may be done with
that evidence and under which executor, method, validation, and
environment conditions. Consequence Governance answers what the
resulting analysis may be allowed to cause. The ordering is deliberate:
a downstream stage must not silently convert failure or uncertainty in
an upstream stage into a successful-looking outcome.

## 7.3 Audit and provenance as a plane, not a fourth stage

Audit is transversal. It should record candidate and admitted knowledge,
provenance, exclusions, model/tool selection, analysis method,
validation, result state, consequence disposition, human interventions,
action authorization, enforcement evidence, and resulting state. This
aligns with end-to-end accountability approaches \[30\], \[31\] while
remaining narrower in scope: ADGL audit concerns reconstruction of the
governance conditions surrounding an execution, not general
organizational assurance.

# 8. Knowledge Governance

Knowledge Governance determines which candidate objects may influence
the Case. Candidate knowledge may originate from databases, document
stores, search, RAG retrievers, APIs, human submissions, logs, or
derived analytical results. Retrieval produces candidates; admission is
a governance decision.

The knowledge model deliberately keeps several dimensions distinct.
Authority describes the source's standing for a subject or domain.
Priority is an operational preference in the current Case. Applicability
determines whether otherwise authoritative material governs the current
circumstances. Evidence role describes how the object participates:
GOVERNING, PRIMARY, CORROBORATING, SUPPLEMENTARY, CONTEXTUAL,
CONTRADICTORY, or EXCLUDED. A highly relevant document can still be
non-governing; an authoritative document can be inapplicable; a
high-priority internal source can be contradicted by more authoritative
external evidence. These distinctions reduce the risk that retrieval
score, source reputation, or organizational preference becomes a hidden
proxy for truth or legal authority.

Lifecycle controls such as QUARANTINE, EMBARGO, SUPERSEDE, EXPIRE, and
REVOKE address the temporal and approval status of information.
Provenance and restriction propagation connect Knowledge Governance to
PROV-like lineage \[10\] and to information-flow/usage-control
traditions \[8\], \[11\]. A derived object should not become
unrestricted merely because it is a summary or model output of a
restricted source. The exact inheritance rules are policy-dependent, but
the lineage must remain observable.

Knowledge Governance therefore complements, rather than replaces, access
control and documentation. A datasheet or data statement may establish
provenance and intended use \[12\], \[18\]; IAM may establish
entitlement; a retriever may establish relevance. ADGL asks a different
runtime question: may this object influence this Case, and if so, how?

# 9. Analysis Governance

Analysis Governance addresses a gap that appears once admissible
evidence is treated as sufficient permission to compute. Two systems can
receive the same governed evidence yet produce materially different
results because they use different models, prompts, statistical
transformations, aggregation rules, inference assumptions, thresholds,
or tool chains. Production ML research emphasizes that such system-level
choices can dominate reliability \[16\], \[17\], \[29\]. ADGL therefore
treats the analytical procedure itself as a governable object.

The current vocabulary is illustrative and organized into four
categories rather than presented as exhaustive or canonical: analytical
operations (COMPARE, CLASSIFY, SUMMARIZE, CALCULATE, SCORE, ESTIMATE,
INFER); transformations (SAMPLE, AGGREGATE, NORMALIZE, WEIGHT);
epistemic controls (CORROBORATE, CHALLENGE, VERIFY, contradiction
preservation, evidence sufficiency); and executor constraints
(model/version, tool, processing region, environment, and output
contract). Operations may be composed and domain profiles may extend
them. Conformance should depend on declared semantics and observable
state transitions, not merely on shared verb labels. Whether a method is
authorized is distinct from whether it is scientifically valid.

Conceptual principle: governance validity is not epistemic validity.
Knowledge Governance regulates permitted influence rather than truth,
and Analysis Governance regulates permitted procedure rather than
scientific correctness.

Human participation inside Analysis Governance is validation, not
necessarily decision ownership. For example, a policy may allow CLASSIFY
but require human verification below a confidence threshold. The human
is then validating the analytical artifact so that it can become a
governed result. This is conceptually different from a later DECIDE
disposition in which an accountable person owns the consequential
choice. Conflating the two can create nominal 'human-in-the-loop'
processes where a person appears in the workflow but has no clearly
defined authority or evidentiary role.

Indirect prompt injection \[23\] further motivates analysis-level
controls. When retrieved content can influence instructions, a system
needs explicit distinctions among source content, control instructions,
permitted tools, and action capabilities. ADGL does not define a
complete prompt-isolation model, but it provides stage boundaries in
which an implementation can require instruction/content separation, tool
allowlists, output contracts, and post-analysis validation before a
consequence is considered.

# 10. Consequence Governance and Decision Rights

Consequence Governance makes explicit a boundary that is often implicit
in AI systems: a governed analytical result is not automatically
authorized to produce a consequential change. INFORM, DECIDE, and ACT
are three classes of consequential authority, not an exhaustive list of
atomic workflow operations. Complex workflows compose these classes
while retaining explicit ownership and authorization at each transition.

- INFORM: return, display, transmit, or store the governed result
  without authorizing a consequential external action.

- DECIDE: assign the next consequential decision to a human or
  accountable role, which may approve, deny, modify, request evidence,
  defer, or escalate according to policy.

- ACT: permit a machine-executable instruction, subject to separate
  action authorization and external enforcement.

Fig. 2. Consequence Governance distinguishes informational output,
human-owned decision authority, and machine-executable action. Human
validation may also occur earlier inside Analysis Governance.

The INFORM/DECIDE/ACT model is compatible with the human-automation
literature's separation of information analysis, decision selection, and
action implementation \[20\]-\[22\], while simplifying those
distinctions into governance dispositions rather than levels of
automation. An INFORM system can use sophisticated AI internally while
still withholding consequential authority. A DECIDE system can provide
recommendations while preserving accountable human ownership. An ACT
system can execute autonomously or through ordinary software, but only
within a bounded capability. Agentic execution is therefore a subset of
ACT, not the definition of the architecture.

Permitted compositions include INFORM; DECIDE; ACT; DECIDE -\> ACT after
approval; ACT + INFORM; sequential or multi-party DECIDE; and loops that
request evidence, defer, escalate, or modify a proposal. Storing a
result is normally INFORM; requesting evidence or escalation is a
transition; and reversible or partial automation remains ACT with
correspondingly bounded capability. Composition must not erase the
responsible decision owner or the capability grant required for
execution.

Action authorization can be scoped by Case, action type, target, value,
volume, number of calls, expiry, reversibility, or other constraints. A
DECIDE path may transition to ACT after an authorized approval or
consent. The semantic transition does not replace IAM, OAuth, Cedar,
XACML, MCP authorization, or API enforcement; it states that those
enforcement mechanisms should receive a governance decision that is
distinguishable from the analytical result that motivated it.

# 11. Audit, Provenance, and Feedback

AI-enabled systems are iterative. An analytical tool call may retrieve
additional information. A model-generated conclusion may be stored and
later reused. A human decision may create new organizational facts. An
API action may change the environment and thereby alter future evidence.
ADGL therefore treats governance as a repeatable cycle rather than a
one-way pipeline.

When a new object enters through retrieval, generation, or action
outcome, it re-enters Knowledge Governance as candidate knowledge with
lineage such as DERIVES_FROM or WAS_GENERATED_BY. Applicable
restrictions should propagate unless an explicit authorized
transformation changes them. This is consistent with PROV's
entity/activity/agent model \[10\] and with the broader insight from
technical-debt and data-cascade research that downstream artifacts can
preserve or amplify upstream defects \[15\], \[16\].

Fig. 3. Feedback loops preserve governance when retrieval, analytical
results, or action outcomes create new candidate knowledge.

The audit objective is reconstructability, not deterministic
reproduction of probabilistic text. A sufficient record should support
questions such as: which sources were considered and excluded; which
policy version applied; which model/tool and method were permitted; what
validation occurred; who owned the decision; what capability authorized
an action; what enforcement evidence was observed; and what resulting
state was created. Stronger production implementations may add
cryptographic integrity, tamper-evident logs, signed policy bundles,
immutable snapshots, and external attestations; those mechanisms are
outside the minimal semantic core.

# 12. Abstract Execution and Transition Model

Let a time-indexed Case be C_t = (p, s, a, j, t, c, P, h), containing
purpose p, subject s, actors a, jurisdiction j, time t,
classification/context c, applicable policies P, and relevant trajectory
history h. Let K be the candidate knowledge set, M the available
models/tools, and A a declared analytical plan. A system state is S =
(C_t, K_s, A_s, O_s, T), where K_s, A_s, and O_s record stage states and
T is the audit trajectory. The following functions describe abstract
semantic boundaries rather than a complete denotational semantics.

G_K(C, K) -\> K\*

G_A(C, K\*, M, A) -\> R

G_C(C, R) -\> O

O ∈ {INFORM, DECIDE, ACT}, with DECIDE -\> ACT permitted by policy

T = Audit(C, K, K\*, A, R, O)

The functions are semantic boundaries rather than deployment
requirements. A single process may implement all three. A distributed
system may use different policy engines or services. Conformance depends
on observable outcomes, propagation rules, and audit semantics rather
than on a mandated topology.

A transition S_i -\[rule\]-\> S\_(i+1) is permitted only when the
applicable policy preconditions hold and the transition is appended to
T. Minimum execution-integrity invariants are: BLOCKED_K implies
AnalysisSuccess is unreachable; AWAITING_VALIDATION_A or REJECTED_A
implies Consequence is unreachable; and ACT implies a valid, case-scoped
capability grant for the proposed action. History h permits policies
over prior approvals, revocation, repeated calls, cumulative value
limits, replay, and temporal escalation.

A terminal or unresolved upstream state constrains downstream
reachability. If Knowledge Governance blocks the case, Analysis and
Consequence must not report successful states. If Analysis requires
validation or rejects an invalid analytical result, Consequence must
remain not reached. This execution-integrity property is important
because a downstream application may otherwise key on a consequence
field while overlooking an upstream failure.

# 13. Reference Implementation and Conformance

The public Python Reference Toolkit is an executable research artifact,
not a production governance service. The 0.5.0 evaluation baseline
implements deterministic Knowledge Governance plus a three-stage
PipelineEngine and 25 published normative conformance checks. The
current public toolkit, 0.5.3, preserves those 25 normative checks and
adds 11 candidate execution-integrity checks discovered during
implementation hardening. The candidate checks are intentionally
reported separately: they are evidence for future specification work,
not retroactively promoted into the normative evaluation without review.

The eight reference cases in Appendix C preserve four earlier
knowledge-governance cases and add four cross-stage cases: human
validation during analysis, a human decision boundary, autonomous
machine/API action, and human approval followed by machine action. The
cases are designed as falsifiable semantic fixtures rather than
demonstrations of production safety. They test expected states, evidence
roles, routing, human boundaries, capability grants, and audit coverage.

| **Coverage area**       | **Normative conformance coverage**                                                                                                                                      |
|-------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Knowledge and lifecycle | Exclusion, quarantine, embargo, supersession, applicability, priority/authority separation, mandatory evidence, conflict preservation, derived restriction propagation. |
| Model/environment       | Model eligibility, processing-region safety, fallback safety.                                                                                                           |
| Analysis                | Method governance, no-infer-missing, corroboration gate, human validation behavior.                                                                                     |
| Consequence             | INFORM, DECIDE, ACT authorization, DECIDE-to-ACT, task-scoped grant.                                                                                                    |
| Audit/portability       | Audit completeness, deterministic replay, portable-subset equivalence, end-to-end stage coverage, policy composition.                                                   |

Appendix A defines the core semantic specification. Appendix B defines
stage and outcome behavior. Appendix C defines reference cases and
illustrative profiles. Appendix D documents toolkit status, conformance,
benchmarks, and reproducibility. Appendix E provides the detailed
comparison with existing governance mechanisms.

# 14. Evaluation

## 14.1 Semantic validation and conformance

The primary evaluation claim is semantic executability, not empirical
proof of governance effectiveness in production. The reference artifact
demonstrates that the proposed states and transitions can be encoded,
tested, and replayed deterministically for the declared subset. The
packaged baseline passes 25/25 published normative conformance checks.
Toolkit 0.5.3 also passes 11/11 candidate execution-integrity checks,
for 36/36 current checks, while preserving the distinction between
published normative requirements and later hardening candidates. All
fixtures, tests, and implementation code were produced by GBSN Research.
The passing results therefore demonstrate internal implementation
consistency with designer-authored expectations; they are not
statistical evidence, independent validation, or proof of governance
effectiveness. This limitation is especially material because GBSN
Research develops both the proposed standard and a commercial product
that implements or may implement it.

## 14.2 Performance characterization

The benchmark is a warmed, single-process microbenchmark of
deterministic policy evaluation. It excludes retrieval, network latency,
model inference, token generation, connector I/O, persistence, human
workflow latency, and execution of external actions. It therefore
characterizes the reference evaluator only and must not be interpreted
as end-to-end production performance.

| **Candidate objects** | **Rules** | **Runs** | **Median ms** | **IQR ms** |
|-----------------------|-----------|----------|---------------|------------|
| 10                    | 10        | 20       | 0.60          | 0.02       |
| 100                   | 10        | 20       | 4.79          | 0.16       |
| 1,000                 | 10        | 20       | 48.35         | 2.31       |
| 5,000                 | 10        | 12       | 227.29        | 12.03      |

For 1,000 objects, the baseline rises from 36.10 ms with zero rules to
218.54 ms with 150 rules. Pipeline measurements over 1,000 objects
report medians of 55.74 ms for INFORM, 57.59 ms for DECIDE, and 55.07 ms
for ACT because the benchmark stops at the governance decision and does
not execute the human workflow or external action. Detailed methodology
and the rule-scaling table are reported in Appendix D.

## 14.3 Case coverage and external validity

The reference cases cover the architecture's main semantic boundaries
but do not establish sectoral completeness. They test regulatory
evidence, geographic/model routing, contamination/derivative
invalidation, internal-first research, low-confidence human validation,
human decision ownership, autonomous API action, and human approval
followed by action. This is broader than a single agentic use case, but
it remains a designed test suite. External validity requires independent
implementations, real organizational policy corpora, live provider/tool
integrations, adversarial tests, and evaluation of whether different
implementers interpret the same semantics consistently.

## 14.4 Formative findings from the commercial implementation

KEE development exposed cases in which the original 25-check suite
permitted materially different runtime behavior despite reference
conformance. Reproduced findings included downstream success after
upstream failure, release of an empty analytical output, unauthenticated
request assertions for grants or human roles, grant expiry evaluated
without a trusted clock, non-atomic quota accounting, required approval
bypass, mismatch between requested and policy-constrained actions, and
audit events that contradicted or misordered the final decision. KEE
corrected these behaviors locally. Because both KEE and ADGL were
developed by GBSN Research, these are producer-authored negative tests
rather than independent observations.

| **Implementation finding**                                              | **Portable implication**                                | **Toolkit 0.5.3 status** |
|-------------------------------------------------------------------------|---------------------------------------------------------|--------------------------|
| Upstream terminal state reached a successful-looking downstream outcome | Cross-stage reachability and fail-closed propagation    | C26 candidate            |
| Empty model output could satisfy the permissive result schema           | Minimum AnalysisResult content contract                 | C27 candidate            |
| ACT could be inferred or insufficiently authorized                      | Explicit machine-action authorization                   | C28 candidate            |
| Grant expiry depended on untrusted request time                         | Trusted-time grant lifecycle                            | C29 candidate            |
| Quota accounting was ambiguous and non-atomic                           | Defined authorization accounting and atomic consumption | C30 candidate            |
| Concrete action value could escape intended constraints                 | Effective-action validation                             | C31 candidate            |
| Capability grant could bypass mandatory human approval                  | Non-bypassable DECIDE-to-ACT gate                       | C32 candidate            |
| Non-finite or negative numeric values were accepted                     | Finite numeric governance                               | C33 candidate            |
| Capability grant scope and shape were incomplete                        | Strict case-scoped grant integrity                      | C34 candidate            |
| Human decision resolution was underspecified                            | Explicit HumanDecision outcome                          | C35 candidate            |
| Caller could vary policy-constrained action fields                      | Action target/template constraints                      | C36 candidate            |

These findings are evidence that implementation can falsify the
sufficiency of a conformance profile even when it does not falsify the
architectural hypothesis. C26-C36 remain candidate semantics because
GBSN has not unilaterally promoted commercial-runtime behavior into
Specification 0.3.0. A future normative revision should disposition each
finding through the public change process and require interoperable test
vectors.

# 15. Comparative Positioning

ADGL should be evaluated as a proposed semantic composition rather than
by asking whether another technology can express one of its individual
rules. General-purpose policy systems can often encode ADGL constraints.
Provenance systems can represent lineage. AI management frameworks can
define organizational controls. Agent protocols can authorize transport.
The proposed contribution is the common execution chain and its domain
vocabulary.

| **Mechanism**                                                     | **Primary object**                                                                                                           | **Relationship to ADGL**                                                                                                                                                                |
|-------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| IAM / XACML / OPA / Cedar                                         | Principal/resource/action authorization and general policy evaluation.                                                       | ADGL can consume or compile to these mechanisms; it adds evidence/analysis/consequence semantics.                                                                                       |
| UCON / information-flow control                                   | Post-access conditions, obligations, continuity, information propagation.                                                    | Strong prior art for persistent control; ADGL specializes to AI/analytical execution stages.                                                                                            |
| ODRL                                                              | Permissions, prohibitions, duties, constraints, profiles.                                                                    | Potential mapping/profile target; ADGL adds stage-specific evidence, analysis, decision-right vocabulary.                                                                               |
| PROV                                                              | Entity/activity/agent provenance and derivation.                                                                             | Complementary lineage substrate; ADGL assigns governance meaning to provenance.                                                                                                         |
| Datasheets / data statements / model cards                        | Transparency about data/model origin, intended use, performance, and limitations.                                            | Documentation feeds policy context; ADGL makes runtime case decisions.                                                                                                                  |
| NIST AI RMF / ISO 42001 / EU AI Act                               | Risk management, management-system requirements, and legal obligations.                                                      | ADGL may implement/evidence selected controls but does not establish compliance.                                                                                                        |
| MCP / agent identity work                                         | Tool/resource interoperability and transport/identity authorization.                                                         | Complementary enforcement prerequisites for ACT; ADGL governs whether the result may cause the action.                                                                                  |
| Policy Cards / AgentSpec / path- and guard-based agent governance | Machine-readable runtime constraints, trajectory policies, verification gates, and action/tool guards for autonomous agents. | Close emerging prior art for runtime governance; ADGL is broader across Knowledge-Analysis-Consequence and INFORM/DECIDE/ACT, and should map to rather than duplicate these mechanisms. |

A decisive next experiment is a full-case mapping from ADGL to an
established substrate such as Rego/OPA or ODRL plus PROV. The evaluation
should report what maps directly, which conventions must be added, what
information is lost, and whether portable stage state and conformance
semantics survive the mapping. Until that experiment or an independent
implementation is completed, compositional usefulness remains a
hypothesis rather than a demonstrated interoperability advantage.

The novelty boundary is therefore intentionally conservative. ADGL does
not claim to invent allow/deny policy, provenance, obligations, human
review, action authorization, or audit. Its hypothesis is that
standardizing how those concepts compose across knowledge influence,
analytical computation, and consequence rights can improve
interoperability and conformance across heterogeneous AI-enabled
systems. Appendix E develops the comparison in greater depth.

# 16. Security and Enforcement Boundaries

The relevant threat actors and failure sources include malicious
knowledge sources, compromised retrievers or models, malicious users,
spoofed identities, forged or replayed capability grants, compromised
policy engines or executors, tampered audit stores, and infrastructure
that violates declared regional or sandbox controls. ADGL can express
governance requirements and, when trustworthy evidence is available,
record or block on their satisfaction. It relies on external identity,
network, sandbox, cryptographic, policy-enforcement, and monitoring
mechanisms to make those requirements effective. It cannot protect
against a compromised policy decision point, executor, or audit
substrate that can falsify the evidence on which the semantic layer
relies.

## 16.1 Enforcement boundary

## 16.2 Threat model

A semantic policy layer cannot physically enforce every condition it
expresses. DENY_INTERNET requires network enforcement. REQUIRE_SANDBOX
requires an actual containment mechanism. REQUIRE_REGION requires
infrastructure evidence that processing occurred in an approved
location. NO_FALLBACK requires routing and provider controls that
prevent an unauthorized alternative endpoint. ACT authorization requires
the downstream executor to reject calls without a valid capability.
Identity assertions require trusted IAM or workload-identity
infrastructure. ADGL defines the governance condition and expected audit
record; enforcement belongs to the mechanism capable of controlling the
resource.

This distinction is especially important for agentic systems. NIST's
current agent work focuses on identity, authentication, authorization,
secure interoperability, and prompt-injection concerns \[26\], \[27\].
MCP similarly distinguishes transport authorization from application
semantics \[25\]. ADGL should therefore be deployed as one layer in a
defense-in-depth architecture, not treated as a security boundary by
syntax alone. AgentSpec, path-based runtime governance, Safety Sidecar,
and deterministic tool guards provide examples of complementary
enforcement strategies focused more directly on agent trajectories or
action release \[34\]-\[37\].

The OpenAI/Hugging Face incident \[32\] illustrates why audit should
record both policy requirements and observed enforcement state. A rule
that says an evaluation is sandboxed is not sufficient evidence that the
sandbox cannot be escaped; conversely, a sandbox does not determine
whether a retrieved source should count as governing evidence or whether
an analysis should be allowed to trigger a financial action. These are
complementary control planes.

# 17. Limitations and Open Research Questions

ADGL remains a working research specification. It does not determine
objective truth, guarantee model correctness, replace cybersecurity,
discover every unauthorized AI system, establish legal compliance, or
certify that human oversight is meaningful. A policy may state a
requirement that the surrounding infrastructure fails to enforce. An
audit may reconstruct what the system recorded while still depending on
the integrity of the recording mechanism.

Analysis Governance is the least mature stage. Open questions include
the appropriate normative vocabulary for analytical methods, how
confidence should be sourced and calibrated, how evidence-to-claim
references should be represented, how prompt/instruction boundaries
should be modeled, when contradictions must be preserved, and how domain
methods should extend the portable core without fragmenting
interoperability. Over-standardizing methods could make the architecture
brittle; under-standardizing them could make conformance superficial.

Human oversight also requires deeper treatment. A DECIDE state only
establishes that a human or accountable role owns the next decision; it
does not guarantee that the person has time, competence, information, or
genuine discretion. Human-factors research on out-of-the-loop
performance cautions against assuming that inserting a human checkpoint
automatically restores meaningful control \[21\], \[22\]. Future
profiles should therefore distinguish nominal approval from decision
conditions such as evidence visibility, authority, workload, time
budget, and ability to modify or reject the system recommendation.

The current portability evidence is limited. One conformance check uses
a mini-interpreter within the same research project; this is not
independent third-party validation. The next major research milestone
should be at least one independent implementation, followed by
third-party cross-implementation test vectors, formal mapping to one or
more general-purpose policy languages, and adversarial experiments that
include poisoned retrieval, identity spoofing, grant misuse, stale
policy, replay, and action-execution failure.

Finally, the boundary between semantic standard and implementation
product must remain explicit. Commercial or production runtimes may add
connectors, persistent audit stores, visual policy tooling, enterprise
identity integration, and action executors. Those features can implement
ADGL without becoming normative requirements of the open semantic
specification.

# 18. Standardization Implications

ADGL is a GBSN Research standards proposal, not a stakeholder-ratified
standard. Broad use is an intended outcome, but standards readiness has
not been demonstrated. Before a formal standardization claim, the work
should obtain independent implementer feedback, practitioner or workshop
review, domain review across multiple sectors, mappings to established
standards, and a documented disposition of stakeholder objections.

If ADGL advances toward formal standardization, the semantic core should
remain small and technology-neutral. A standards effort should focus on
vocabulary, state transitions, conformance fixtures, versioning, profile
composition, and mappings to established mechanisms. It should avoid
mandating a specific model provider, vector store, database,
orchestration framework, cloud, or policy engine.

Interoperability work should be prioritized over reinvention. Candidate
work items include: an ODRL profile or mapping for
permissions/duties/constraints; compilation subsets for XACML, Rego, or
Cedar; PROV mappings for KnowledgeObjects, Analysis activities, results,
decisions, and actions; MCP integration guidance for resource/tool
boundaries; identity binding profiles for agent and workload identities;
and a conformance vocabulary that distinguishes normative checks from
experimental/candidate checks.

Standardization should also preserve the architecture's scope
discipline. Agent identity and authorization are important, but agentic
execution is one ACT pathway. Data governance and informational analysis
remain first-class. A standard that collapses ADGL into agent security
would lose the broader contribution; a standard that ignores action
authorization would fail to address the execution boundary that
motivated Consequence Governance.

## 18.1 Artifact Availability and Reproducibility

Public reproducibility artifacts comprise: (1) the Academic Research and
Specification package, including the main paper and Appendices A-E; (2)
the separately packaged Reference Toolkit 0.5.3; (3) the GitHub public
repository package with browsable research sources, schemas, eight
constructed cases, tests, conformance runner, contribution templates,
and CI configuration; and (4) a Hugging Face dataset and Gradio Space
exposing the eight cases for interactive execution. During preparation
of this revision, a fresh run from the supplied public archives
reproduced 20/20 public software tests, 25/25 published normative
checks, and 11/11 candidate checks. KEE is unpublished proprietary
source and is not included in the reproducibility claim; a separate
source-level run reproduced 28/28 KEE tests and the embedded Toolkit
0.5.0 baseline’s 25/25 checks. These reruns confirm packaged execution
only and are not independent semantic validation. Exact URLs, DOIs,
repository commit/tag, dataset revision, and Space revision: \[INSERT
CAMERA-READY ARTIFACT IDENTIFIERS\]. ADGL technical and specification
enquiries: aidatagovernance@gbsnresearch.com.

## 18.2 Competing Interests, Funding, and Commercialization Disclosure

GBSN Research designed ADGL, authors and maintains the proposed open
specification and Reference Toolkit, and develops KEE, a separate
proprietary commercial runtime that implements and extends parts of
ADGL. GBSN Research therefore has a direct financial and reputational
interest in ADGL adoption and perceived value. The specification, cases,
conformance suite, Reference Toolkit, KEE implementation, internal
adversarial reviews, and present evaluation were all produced or
commissioned within the same organization; none constitutes independent
validation. KEE development informed candidate checks C26-C36, but
KEE-specific behavior is non-normative unless accepted into a future
public specification. KEE is not required for ADGL implementation or
conformance. The public specification and documentation are distributed
under CC BY 4.0 and the Reference Toolkit under Apache License 2.0.
Research and artifact development were funded and performed by GBSN
Research unless otherwise stated. Named individual authors,
affiliations, ORCID identifiers, and CRediT contributions must be
supplied before submission to any venue requiring personal scholarly
accountability.

GBSN Research develops ADGL as a proposed standard intended for broad
use and also develops a commercial product and related services that
implement or may implement ADGL. GBSN Research therefore has a direct
commercial interest in the visibility, adoption, and perceived value of
the architecture. The specification, reference cases, conformance suite,
and reference implementation evaluated in this paper were created by
GBSN Research; the evaluation is not independent. The research and
artifact development were funded and performed by GBSN Research unless
otherwise stated. The proposed semantic standard is intended to remain
implementable without purchasing GBSN's commercial product, and no
commercial product should be treated as the normative definition of
conformance. Named individual contributors and their roles should be
identified in any venue that requires personal scholarly accountability.

## 18.3 Artifact Version Matrix

| **Artifact**                          | **Version represented**              | **Role**                                          |
|---------------------------------------|--------------------------------------|---------------------------------------------------|
| Academic preprint                     | v1.2 (submission draft)              | Scholarly argument and evaluation scope           |
| Research release                      | 0.4.3                                | Coordinated research package                      |
| Core semantic specification           | 0.3.0                                | Normative working semantics                       |
| Reference Toolkit evaluation baseline | 0.5.0                                | 25 published normative checks                     |
| Current Reference Toolkit             | 0.5.3                                | Baseline plus 11 candidate hardening checks       |
| GitHub public repository package      | 0.4.3 reviewed; synchronize to 0.4.4 | Public development and browsable research sources |
| Hugging Face dataset and Space        | Public revision to be cited          | Eight-case dataset and interactive execution      |
| KEE commercial MVP                    | 0.4 (unpublished)                    | Producer-authored formative evaluation only       |

# 19. Conclusion

The governance problem created by AI-enabled systems is not reducible to
access, model risk, or agent authorization in isolation. Information may
be accessible yet inadmissible; admissible evidence may be subject to
method or model constraints; a valid analysis may require human decision
ownership; and a decision may still require bounded authorization before
a machine action can occur. Prior research in usage control, information
flow, documentation, ML engineering, auditing, human automation,
retrieval, and agent security exposes each of these boundaries from
different directions.

ADGL organizes the resulting problem into Knowledge Governance, Analysis
Governance, and Consequence Governance, with Audit and Provenance
spanning the complete trajectory. INFORM, DECIDE, and ACT provide a
common consequence vocabulary across informational systems, human-owned
decisions, and machine execution. The proposal is deliberately
complementary to existing policy languages, provenance standards, AI
management frameworks, and enforcement infrastructure.

The reference toolkit demonstrates that the proposed semantics are
executable and testable, but not that they are complete or
production-safe. The strongest next evidence would come from independent
implementations, formal mappings, broader domain cases, adversarial
evaluation, and real organizational deployment. The core research claim
is therefore modest but testable: a semantic chain designed to support
portability that separates what may influence computation, how it may be
analyzed, and what the result may cause can make AI governance decisions
more explicit, interoperable, and auditable across heterogeneous
systems.

# Companion Appendices

| **Document** | **Title**                           | **Role**                                                                                                                               |
|--------------|-------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| Appendix A   | Core Semantic Specification 0.3.0   | Normative/working semantic objects, operations, states, validation rules, and conformance language.                                    |
| Appendix B   | Governance Stages and Outcome Model | Detailed Knowledge, Analysis, Consequence, audit/provenance, feedback, and enforcement-boundary semantics.                             |
| Appendix C   | Reference Use Cases and Profiles    | Eight reference cases and illustrative non-normative governance profiles.                                                              |
| Appendix D   | Reference Toolkit and Evaluation    | Implementation status, conformance, benchmark methodology, reproducibility, and interpretation limits.                                 |
| Appendix E   | Comparative Analysis                | Detailed comparison with authorization, usage control, provenance, retrieval, management, regulatory, and agent-governance mechanisms. |

# References

\[1\] E. Tabassi, Artificial Intelligence Risk Management Framework (AI
RMF 1.0), NIST AI 100-1, National Institute of Standards and Technology,
Jan. 2023.

\[2\] C. Autio et al., Artificial Intelligence Risk Management
Framework: Generative Artificial Intelligence Profile, NIST AI 600-1,
National Institute of Standards and Technology, July 2024.

\[3\] ISO/IEC 42001:2023, Information technology - Artificial
intelligence - Management system, International Organization for
Standardization, 2023.

\[4\] European Parliament and Council, Regulation (EU) 2024/1689 laying
down harmonised rules on artificial intelligence (Artificial
Intelligence Act), 2024.

\[5\] OASIS, eXtensible Access Control Markup Language (XACML) Version
3.0, OASIS Standard, 2013.

\[6\] Open Policy Agent, Policy Language and Authorization
Documentation, accessed Aug. 2026.

\[7\] Cedar Policy Language, Cedar Policy Language Reference Guide,
version 4.5, accessed Aug. 2026.

\[8\] J. Park and R. Sandhu, "The UCONABC Usage Control Model," ACM
Transactions on Information and System Security, vol. 7, no. 1, pp.
128-174, 2004.

\[9\] W3C, ODRL Information Model 2.2, W3C Recommendation, Feb. 2018.

\[10\] W3C, PROV-O: The PROV Ontology, W3C Recommendation, Apr. 2013.

\[11\] S. Chong, K. Vikram, and A. C. Myers, "SIF: Enforcing
Confidentiality and Integrity in Web Applications," in 16th USENIX
Security Symposium, 2007.

\[12\] E. M. Bender and B. Friedman, "Data Statements for Natural
Language Processing: Toward Mitigating System Bias and Enabling Better
Science," Transactions of the Association for Computational Linguistics,
vol. 6, pp. 587-604, 2018.

\[13\] K. Guu, K. Lee, Z. Tung, P. Pasupat, and M.-W. Chang, "REALM:
Retrieval-Augmented Language Model Pre-Training," in Proceedings of
ICML, 2020.

\[14\] P. Lewis et al., "Retrieval-Augmented Generation for
Knowledge-Intensive NLP Tasks," in Advances in Neural Information
Processing Systems, 2020.

\[15\] N. Sambasivan, S. Kapania, H. Highfill, D. Akrong, P. K.
Paritosh, and L. M. Aroyo, "Everyone wants to do the model work, not the
data work: Data Cascades in High-Stakes AI," in Proceedings of CHI,
2021.

\[16\] D. Sculley et al., "Hidden Technical Debt in Machine Learning
Systems," in Advances in Neural Information Processing Systems, pp.
2503-2511, 2015.

\[17\] E. Breck, S. Cai, E. Nielsen, M. Salib, and D. Sculley, "The ML
Test Score: A Rubric for ML Production Readiness and Technical Debt
Reduction," in IEEE International Conference on Big Data, 2017.

\[18\] T. Gebru et al., "Datasheets for Datasets," Communications of the
ACM, vol. 64, no. 12, pp. 86-92, 2021.

\[19\] M. Mitchell et al., "Model Cards for Model Reporting," in
Proceedings of the Conference on Fairness, Accountability, and
Transparency, pp. 220-229, 2019.

\[20\] R. Parasuraman, T. B. Sheridan, and C. D. Wickens, "A Model for
Types and Levels of Human Interaction with Automation," IEEE
Transactions on Systems, Man, and Cybernetics - Part A, vol. 30, no. 3,
pp. 286-297, 2000.

\[21\] L. Bainbridge, "Ironies of Automation," Automatica, vol. 19, no.
6, pp. 775-779, 1983.

\[22\] M. R. Endsley and E. O. Kiris, "The Out-of-the-Loop Performance
Problem and Level of Control in Automation," Human Factors, vol. 37, no.
2, pp. 381-394, 1995.

\[23\] K. Greshake, S. Abdelnabi, S. Mishra, C. Endres, T. Holz, and M.
Fritz, "More than you've asked for: A Comprehensive Analysis of Novel
Prompt Injection Threats to Application-Integrated Large Language
Models," arXiv:2302.12173, 2023.

\[24\] S. Yao et al., "ReAct: Synergizing Reasoning and Acting in
Language Models," in International Conference on Learning
Representations, 2023.

\[25\] Model Context Protocol, Authorization Specification, version
2026-07-28, 2026.

\[26\] National Institute of Standards and Technology, AI Agent
Standards Initiative, 2026.

\[27\] H. Booth, B. Fisher, R. Galluzzo, and J. Roberts, Accelerating
the Adoption of Software and AI Agent Identity and Authorization, NCCoE
Draft Concept Paper, Feb. 2026.

\[28\] J. Mavračić, "Policy Cards: Machine-Readable Runtime Governance
for Autonomous AI Agents," arXiv:2510.24383, 2025.

\[29\] S. Amershi et al., "Software Engineering for Machine Learning: A
Case Study," in 2019 IEEE/ACM 41st International Conference on Software
Engineering: Software Engineering in Practice, 2019.

\[30\] I. D. Raji et al., "Closing the AI Accountability Gap: Defining
an End-to-End Framework for Internal Algorithmic Auditing," in
Proceedings of FAT\* 2020, 2020.

\[31\] V. Ojewale, R. Steed, B. Vecchione, A. Birhane, and I. D. Raji,
"Towards AI Accountability Infrastructure: Gaps and Opportunities in AI
Audit Tooling," arXiv:2402.17861, revised 2025.

\[32\] OpenAI, "OpenAI and Hugging Face partner to address security
incident during model evaluation," July 21, 2026, with updates through
July 29, 2026.

\[33\] GBSN Research, From Observation to Orchestration: The
Reliability-Actionability Framework for Automated Market Engines, Jan.
2026.

\[34\] H. Wang, C. M. Poskitt, and J. Sun, "AgentSpec: Customizable
Runtime Enforcement for Safe and Reliable LLM Agents," arXiv:2503.18666,
2025.

\[35\] M. Kaptein, V.-J. Khan, and A. Podstavnychy, "Runtime Governance
for AI Agents: Policies on Paths," arXiv:2603.16586, 2026.

\[36\] B. Wang et al., "Safety Sidecar: Reflection-Driven Runtime
Control for Safer Agents," Findings of the Association for Computational
Linguistics: ACL 2026, pp. 30842-30856, 2026.

\[37\] N. Zwerdling, D. Boaz, E. Rabinovich, G. Uziel, D. Amid, and A.
Anaby Tavor, "Towards Enforcing Company Policy Adherence in Agentic
Workflows," Proceedings of the 2025 Conference on Empirical Methods in
Natural Language Processing: Industry Track, pp. 595-606, 2025.
