# Policy Composition and Precedence

Toolkit 0.5.3 implements the ADGL 0.3 base precedence order:

1. legal / regulatory / sovereign constraints;
2. explicit prohibitions and mandatory security constraints;
3. data-classification and processing-location constraints;
4. lifecycle restrictions;
5. governing-authority rules;
6. mandatory evidence and human-review obligations;
7. case-specific policy;
8. organizational defaults;
9. priority and preference rules;
10. optional fallback behavior.

Rules can declare `precedence_level`. Optional top-level `policies` can carry their own `precedence_level`. The compiler normalizes supported knowledge-governance rules into one execution plan. Lower-precedence rules execute first; higher-precedence rules execute later. At the same level, restrictive rules execute after permissive/preference rules. Restrictive lifecycle dispositions are terminal with respect to ordinary `ALLOW`.

This is a deterministic **base composition algorithm**, not a claim that all future stage-, Profile-, `OVERRIDE`-, or `EXCEPTION`-specific composition semantics are complete. Those advanced semantics remain partial and must be disclosed in any conformance claim.

Analysis and Consequence Governance in Toolkit 0.5.3 are intentionally small reference evaluators layered after the supported Knowledge Governance plan. A future specification revision should define composition when multiple independent Analysis or Consequence Profiles apply simultaneously.
