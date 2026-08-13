# Paper-to-Toolkit Mapping — Research Release 0.4.0

| Research artifact construct | Toolkit location |
|---|---|
| Appendix A core semantic objects | `adgl/vocabulary.py`, `schemas/` |
| Knowledge Governance | `adgl/engine.py`, `adgl/operations.py`, `adgl/selectors.py` |
| Analysis Governance | `adgl/analysis.py`, `schemas/analysis-result.schema.json` |
| Consequence Governance | `adgl/consequence.py`, action/grant schemas |
| Three-stage orchestration | `adgl/pipeline.py` |
| Policy validation / IR | `adgl/compiler.py`, `adgl/validation.py` |
| Audit/provenance trace | `adgl/audit.py`, `schemas/audit.schema.json` |
| Model & geography | `schemas/model-resource.schema.json`, routing in `adgl/engine.py` |
| Profiles | `schemas/profile.schema.json`, `profiles/illustrative/` |
| Conformance | `adgl/conformance.py`, `tests/`, `examples/` |
| Appendix C Cases 1-4 | original four example directories |
| Appendix C Cases 5-8 | human validation, human decision, autonomous action, approval-then-action directories |
| Appendix D benchmark results | `benchmarks/`, `benchmarks/results/` |
| Design-discussion superset | `extensions/EXPERIMENTAL_OPERATIONS.md` |

The toolkit deliberately distinguishes normative/reference semantics from experimental extensions and illustrative Profiles so GitHub experimentation does not silently redefine the specification.
