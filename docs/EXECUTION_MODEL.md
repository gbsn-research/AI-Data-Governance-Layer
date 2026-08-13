# ADGL 0.3 Execution Model

ADGL separates three governance questions:

1. **Knowledge Governance** — what may be considered and in what evidentiary capacity?
2. **Analysis Governance** — what analytical computation may be performed on admissible knowledge, with which model/tool/method and validation constraints?
3. **Consequence Governance** — what is the governed result permitted to cause?

Consequence dispositions are:

- `INFORM`: the governed result is returned/displayed/stored without a consequential external action being authorized by ADGL.
- `DECIDE`: a human decision right is required before the consequential path may continue.
- `ACT`: a machine-executable action may proceed subject to action authorization and external enforcement.

`DECIDE -> ACT` is a valid transition after an authorized human decision. Human validation can also occur *inside Analysis Governance* when the analytical result itself requires validation before consequence routing.

Audit/provenance is cross-cutting and records all three stages.

Analytical tool calls that retrieve or transform evidence are not automatically consequential `ACT` operations. Consequential action changes external state because of a governed result.
