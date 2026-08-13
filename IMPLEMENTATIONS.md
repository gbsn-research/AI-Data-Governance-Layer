# ADGL implementations and evaluation artifacts

## Open Reference Toolkit

The Python Reference Toolkit is the public, openly licensed executable companion to Specification 0.3.0. It contains schemas, eight constructed reference cases, a conformance runner, tests, benchmarks, and illustrative profiles. Toolkit 0.5.3 reports 25 published normative checks and 11 candidate execution-integrity checks.

## Portable-subset interpreter

`portable_reference.py` is a deliberately separate, producer-authored mini-interpreter used by C15 for a limited portable subset. It does not import the primary engine modules. It is not a third-party, clean-room, cross-language, or independently governed implementation.

## KEE commercial MVP

KEE is an unpublished proprietary commercial MVP developed by GBSN Research. It vendors the paper-evaluated Reference Toolkit 0.5.0 baseline implementing Specification 0.3.0 and adds production-oriented model orchestration, release gating, trust registries, authorization hardening, quota accounting, and audit-integrity behavior. Its development supplied formative negative cases for candidate checks C26-C36.

KEE is not included in the public reproducibility package, is not required for conformance, and does not define normative ADGL behavior.

## Independent implementations

No third-party or clean-room implementation has yet been validated. Independent implementations and mappings to established policy/provenance systems are priority research milestones.

