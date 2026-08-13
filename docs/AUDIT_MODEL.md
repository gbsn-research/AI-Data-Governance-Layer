# Audit Model

The base audit vocabulary follows Appendix A.17.

Where applicable, a governed execution records:

- `case_id` — required;
- `purpose` — required;
- exact `policy_ids_and_versions` — required;
- `candidate_object_ids` — required when enumerated;
- `object_dispositions` — required;
- `authority_and_applicability_results` — required when decision-relevant;
- `evidence_roles` — required when evidence is used;
- `model_resource` — required when a model is invoked;
- `processing_environment` — required when location/environment is governed;
- `route_decision` — required;
- `conflicts` — required when detected;
- `human_events` — required when review/override occurs;
- `decision_state` — required;
- `derivation_links` — required for governed derived objects;
- timestamps for material governance events.

Raw sensitive content does not need to be duplicated into audit storage. References, protected identifiers, hashes, or customer-controlled secure stores may be used if the governance path remains reconstructable.
