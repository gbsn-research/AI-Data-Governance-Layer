# Model and Geographic Governance

ADGL treats the reasoning model and processing environment as governed resources.

Core operations:

- `ROUTE`
- `REQUIRE_MODEL`
- `DENY_MODEL`
- `REQUIRE_REGION`
- `DENY_REGION`
- `LOCAL_ONLY`
- `NO_FALLBACK`
- `REQUIRE_VALIDATED_VERSION`

Before transmitting governed content to a model, tool, connector, or processing environment, an implementation should evaluate applicable location, classification, model eligibility, version, and transfer constraints.

If a mandatory processing location cannot be established, the base semantics are fail-closed.

The standard expresses organizational policy; it does not itself determine what any jurisdiction legally requires.
