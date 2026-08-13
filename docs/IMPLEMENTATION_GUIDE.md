# Implementation Guide

## Validate
```bash
python -m adgl.cli validate examples/regulatory_product_claim_review/policy.yaml
```

## Execute
```bash
python -m adgl.cli run examples/regulatory_product_claim_review/policy.yaml --input examples/regulatory_product_claim_review/input.json
```

## Conformance
```bash
python -m adgl.cli conformance
```

## Add a new operation
1. Define the semantic behavior.
2. Define precedence/failure behavior.
3. Add a falsifiable conformance fixture.
4. Implement it in `operations.py` or `engine.py`.
5. Only then propose it for the normative standard.
