**ADGL Appendix D - Reference Toolkit, Conformance, and Evaluation**

**GBSN Research**

Lisbon, Portugal \| Correspondence: publications@gbsnresearch.com

*Academic preprint edition \| Public Research Release 0.4.3*

Paper-evaluated Toolkit 0.5.0 \| Current Public Toolkit 0.5.3 \| Public
Distribution 0.4.3

# D.1 Purpose and Scope

The ADGL Reference Toolkit is an executable research artifact intended
to make the proposed semantic architecture inspectable, falsifiable, and
reproducible. It is not a production governance service, does not
contain a foundation model, does not retrieve enterprise data, and does
not execute live external actions. Its role is to encode reference
semantics, machine-readable schemas, test fixtures, conformance checks,
and deterministic benchmark workloads.

# D.2 Version Relationship

Two implementation states must be distinguished. The v0.9 paper
evaluated Reference Toolkit 0.5.0 and its 25 published normative
conformance checks. The current public toolkit, 0.5.3, preserves that
paper-era normative suite and adds 11 candidate execution-integrity
checks (C26-C36) discovered during subsequent implementation hardening.
Those candidate checks are evidence for the next specification revision;
they are not retroactively represented as normative requirements of Core
Semantic Specification 0.3.0.

# D.3 Repository Structure and Implementation Status

> adgl/ core and pipeline engines, analysis, consequence, audit  
> schemas/ policy, knowledge, model, analysis-result, action, grant,
> profile  
> examples/ eight executable reference cases  
> profiles/ illustrative non-normative governance profiles  
> conformance/ normative and candidate executable results  
> benchmarks/ reproducible deterministic benchmark harness and results  
> docs/ semantics, threat model, profiles, implementation status  
> tests/ software regression tests

| **Capability**                               | **Toolkit 0.5.3 status**                                      |
|----------------------------------------------|---------------------------------------------------------------|
| Knowledge admission/lifecycle/evidence roles | Implemented core subset                                       |
| Authority/priority/applicability             | Implemented core subset                                       |
| Derived restriction propagation              | Implemented basic propagation                                 |
| Model/processing-region eligibility          | Implemented                                                   |
| Deterministic base policy composition        | Implemented base precedence                                   |
| Three-stage pipeline policy validation       | Implemented schema + embedded core validation                 |
| Stage-qualified analytical transformations   | Partial; legacy collection operations retained in core engine |
| Pipeline-native model/region stage placement | Partial; core-compatible routing reused                       |
| Analysis method allowlist                    | Implemented                                                   |
| Evidence sufficiency/corroboration           | Implemented                                                   |
| No-infer-missing                             | Implemented                                                   |
| Human validation inside Analysis             | Implemented basic gate                                        |
| INFORM / DECIDE / ACT                        | Implemented                                                   |
| Human decision ownership / DECIDE -\> ACT    | Implemented reference representation and transition           |
| Mandatory approval-required gate             | Implemented as candidate integrity behavior                   |
| Capability-grant action authorization        | Implemented reference type/case/value/expiry/quota checks     |
| Live API/tool enforcement                    | Not implemented; external integration boundary                |
| Production IAM/workflow/sandbox              | Not implemented; external enforcement boundary                |
| Independent third-party portability          | Not established; portable-subset equivalence only             |

# D.4 Conformance Results

The paper-evaluated 0.5.0 baseline passed 10/10 software tests and 25/25
published normative conformance checks. The current 0.5.3 public
distribution passes 20/20 software regression tests, preserves 25/25
normative checks, and passes 11/11 candidate execution-integrity checks,
for 36/36 current checks in total. This is internal conformance evidence
against the published fixtures, not independent certification.

| **Check** | **Published normative behavior** | **Result** |
|-----------|----------------------------------|------------|
| C01       | Exclusion safety                 | PASS       |
| C02       | Quarantine isolation             | PASS       |
| C03       | Embargo enforcement              | PASS       |
| C04       | Supersession                     | PASS       |
| C05       | Priority/authority separation    | PASS       |
| C06       | Applicability gating             | PASS       |
| C07       | Model eligibility                | PASS       |
| C08       | Region safety                    | PASS       |
| C09       | Fallback safety                  | PASS       |
| C10       | Mandatory evidence               | PASS       |
| C11       | Conflict preservation            | PASS       |
| C12       | Derived restriction propagation  | PASS       |
| C13       | Audit completeness               | PASS       |
| C14       | Deterministic replay             | PASS       |
| C15       | Portable-subset equivalence      | PASS       |
| C16       | Deterministic policy composition | PASS       |
| C17       | Analysis method governance       | PASS       |
| C18       | No-infer-missing                 | PASS       |
| C19       | Analysis corroboration gate      | PASS       |
| C20       | INFORM disposition               | PASS       |
| C21       | DECIDE disposition               | PASS       |
| C22       | ACT capability authorization     | PASS       |
| C23       | DECIDE-to-ACT transition         | PASS       |
| C24       | End-to-end audit stage coverage  | PASS       |
| C25       | Task-scoped action grant         | PASS       |

## D.4.1 Candidate execution-integrity hardening

| **Check** | **Candidate behavior**                        | **Result** |
|-----------|-----------------------------------------------|------------|
| C26       | Upstream terminal propagation                 | PASS       |
| C27       | Minimum AnalysisResult contract               | PASS       |
| C28       | ACT requires explicit authorization           | PASS       |
| C29       | Expired action grant fails closed             | PASS       |
| C30       | In-process action quota enforcement           | PASS       |
| C31       | Effective Action value authorization          | PASS       |
| C32       | Required human approval cannot be bypassed    | PASS       |
| C33       | Finite numeric governance                     | PASS       |
| C34       | CapabilityGrant schema and scope integrity    | PASS       |
| C35       | Human DECIDE resolution                       | PASS       |
| C36       | Action target/template constraint enforcement | PASS       |

The candidate checks specifically target cross-stage propagation,
analytical-output contracts, action-grant lifecycle and scope,
human-decision transitions, effective-action authorization, and
malformed numeric or policy assertions. They remain intentionally
separate from the normative suite until the next specification-hardening
cycle.

# D.5 Deterministic Runtime Benchmark

The benchmark measures deterministic governance-engine overhead only. It
excludes retrieval, model inference, network latency, connector I/O,
token generation, external persistence, human-workflow latency, and
execution of real actions. Smaller workloads use 20 measured runs after
warmup; the largest 5,000-object and 150-rule workloads use 12 measured
runs. Median and interquartile range (IQR) are reported.

| **Objects** | **Rules** | **Runs** | **Median ms** | **IQR ms** |
|-------------|-----------|----------|---------------|------------|
| 10          | 10        | 20       | 0.60          | 0.02       |
| 100         | 10        | 20       | 4.79          | 0.16       |
| 1,000       | 10        | 20       | 48.35         | 2.31       |
| 5,000       | 10        | 12       | 227.29        | 12.03      |

*Fig. D-1. Object-scaling benchmark for the deterministic reference
evaluator.*

| **Objects** | **Rules** | **Runs** | **Median ms** | **IQR ms** |
|-------------|-----------|----------|---------------|------------|
| 1,000       | 0         | 20       | 36.10         | 0.85       |
| 1,000       | 5         | 20       | 42.46         | 1.79       |
| 1,000       | 25        | 20       | 64.85         | 2.61       |
| 1,000       | 100       | 20       | 155.75        | 31.22      |
| 1,000       | 150       | 12       | 218.54        | 93.80      |

*Fig. D-2. Rule-scaling benchmark for the deterministic reference
evaluator.*

# D.6 Three-Stage Pipeline Benchmark

A second microbenchmark executes the three-stage reference pipeline over
1,000 objects for INFORM, DECIDE, and ACT routing. The benchmark stops
at the governance decision and does not execute a human workflow or
external action. The similar medians therefore characterize
consequence-routing overhead only, not equivalent end-to-end operational
latency.

| **Disposition** | **Objects** | **Runs** | **Median ms** | **IQR ms** |
|-----------------|-------------|----------|---------------|------------|
| INFORM          | 1,000       | 20       | 55.74         | 3.00       |
| DECIDE          | 1,000       | 20       | 57.59         | 7.24       |
| ACT             | 1,000       | 20       | 55.07         | 3.11       |

# D.7 Reproducibility

The public repository contains the fixtures and benchmark harness.
Representative commands are:

> python -m pip install -e .  
> adgl validate examples/regulatory_product_claim_review/policy.yaml  
> adgl run examples/regulatory_product_claim_review/policy.yaml --input
> examples/regulatory_product_claim_review/input.json  
> adgl pipeline examples/autonomous_machine_action/policy.yaml --input
> examples/autonomous_machine_action/input.json  
> adgl conformance  
> PYTHONPATH=. python benchmarks/benchmark.py --iterations 20  
> PYTHONPATH=. python benchmarks/pipeline_benchmark.py

# D.8 Interpretation and Validity Limits

The reference implementation demonstrates executability, regression
behavior, and internal conformance against declared fixtures. It does
not establish production safety, sectoral completeness, or independent
interoperability. C15 uses a mini-interpreter distributed within the
same research project and is therefore not third-party validation. The
performance numbers are microbenchmarks of policy evaluation, not
service-level objectives.

Production use would require authenticated identity and governance
assertions, trusted policy distribution, durable and atomic quota
consumption, secure secret management, persistent/tamper-evident audit,
external enforcement of network/sandbox/region controls, robust
connector boundaries, and transactional action execution. The reference
in-process max_calls accounting is demonstrative rather than a
distributed quota service.

The strongest next evaluation steps are an independent implementation,
cross-implementation test vectors, live provider/tool integrations,
adversarial tests for poisoned retrieval and prompt injection, identity
and grant spoofing, policy replay/staleness, and action-execution
failure, together with domain-specific evaluations of whether Profiles
preserve the intended semantics.

# D.9 REVISED EVALUATION SCOPE

The public Toolkit 0.5.3 reports 20 software tests, 25 published
normative checks (C01-C25), and 11 candidate execution-integrity checks
(C26-C36). All were reproduced in the reviewed package. The GitHub
release materials also report successful execution of all eight cases in
the public Hugging Face Space. These results demonstrate executable
producer-authored fixtures and reproducible internal consistency, not
independent semantic validation or production effectiveness.

The unpublished proprietary KEE 0.4 MVP was reviewed as a second
producer-authored artifact environment. Its 28 tests and embedded
Toolkit 0.5.0 baseline’s 25 checks were reproduced. KEE’s adversarial
development supplied negative cases that motivated C26-C36. KEE is not
public reproducibility evidence, an independent implementation, or the
normative definition of ADGL.
