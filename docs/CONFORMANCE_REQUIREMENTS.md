# ADGL 0.3 Minimum Reference Conformance Fixtures

The v0.9 paper package defines twenty-five published normative falsifiable checks (C01-C25). Toolkit 0.5.3 preserves those checks and adds eleven candidate execution-integrity checks (C26-C36) for the next specification-hardening cycle:

1. C01 Exclusion safety
2. C02 Quarantine isolation
3. C03 Embargo enforcement and release
4. C04 Supersession
5. C05 Priority/authority separation
6. C06 Applicability gating
7. C07 Model eligibility
8. C08 Region safety
9. C09 Fallback safety
10. C10 Mandatory evidence
11. C11 Conflict preservation
12. C12 Derived restriction propagation
13. C13 Audit completeness
14. C14 Deterministic replay
15. C15 Portable-subset equivalence
16. C16 Deterministic policy composition
17. C17 Analysis method governance
18. C18 No-infer-missing
19. C19 Analysis corroboration gate
20. C20 INFORM disposition
21. C21 DECIDE disposition
22. C22 ACT capability authorization
23. C23 DECIDE-to-ACT transition
24. C24 End-to-end audit stage coverage
25. C25 Task-scoped action grant

C15 compares the primary Engine against `portable_reference.py`, a deliberately independent mini-interpreter that does not import the primary compiler, selector, operation, or engine modules. It is evidence for portability only on the subset exercised by that fixture; it is not evidence of full cross-language or independent third-party interoperability.

Passing C01-C25 demonstrates the behaviors tested by the published paper-era suite. Passing C26-C36 additionally demonstrates the current candidate integrity behavior of Toolkit 0.5.3. It is not a blanket claim of production readiness or full conformance with future ADGL Profiles.


## Candidate execution-integrity checks (Toolkit 0.5.3)

26. C26 Upstream terminal propagation
27. C27 Minimum AnalysisResult contract
28. C28 ACT requires explicit authorization
29. C29 Expired action grant fails closed
30. C30 In-process action quota enforcement
31. C31 Effective Action value authorization
32. C32 Required human approval cannot be bypassed

33. C33 Finite numeric governance
34. C34 CapabilityGrant schema and scope integrity
35. C35 Human DECIDE resolution
36. C36 Action target/template constraint enforcement
