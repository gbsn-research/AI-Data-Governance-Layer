# Reference Threat Model

ADGL treats policy definitions, compiled policy plans, model/resource metadata supplied by trusted control planes, and the enforcement runtime as higher-integrity inputs than retrieved or user-supplied content.

The research model considers at least the following threats:
- policy tampering, unauthorized policy mutation, and rollback to older policy versions;
- compromised or falsified governance metadata;
- time-of-check/time-of-use gaps between route approval and actual model transmission;
- direct or indirect prompt injection attempting to modify policy behavior;
- connector over-fetch or accidental admission of material outside the Case scope;
- provider or orchestration fallback to an unapproved model or processing region;
- tool-mediated exfiltration after evidence admission;
- audit-log suppression, deletion, or tampering;
- laundering restrictions through summaries or other derived objects;
- malicious, mistaken, or unauthorized human override;
- stale authority, applicability, model-approval, or jurisdiction metadata.

Toolkit 0.5.3 demonstrates policy semantics but does not claim to mitigate all of these threats in production. Production implementations need authenticated policy distribution, integrity protection, identity and secret management, route enforcement at the network/model boundary, tamper-evident audit storage, and appropriately authorized human-review workflows.


## Three-stage additions
- Analysis-method substitution or unapproved inference strategy.
- Analysis-result laundering into future knowledge without provenance.
- Consequence misclassification (INFORM treated as ACT, or ACT bypassing DECIDE).
- Human-decision spoofing or unauthorized approval.
- Action authorization exceeding task scope, call/value/data limits or grant lifetime.
- TOCTOU between consequence authorization and external action execution.

ADGL expresses governance requirements; physical enforcement remains the responsibility of integrated IAM, gateway, workflow, sandbox, network, tool and application controls.
