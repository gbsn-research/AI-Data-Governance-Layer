from __future__ import annotations
import json, math
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parent
SCHEMAS={
 'knowledge_object':ROOT/'schemas'/'knowledge-object.schema.json',
 'model_resource':ROOT/'schemas'/'model-resource.schema.json',
 'audit':ROOT/'schemas'/'audit.schema.json',
 'analysis_result':ROOT/'schemas'/'analysis-result.schema.json',
 'pipeline_policy':ROOT/'schemas'/'pipeline-policy.schema.json',
 'profile':ROOT/'schemas'/'profile.schema.json',
 'action':ROOT/'schemas'/'action.schema.json',
 'capability_grant':ROOT/'schemas'/'capability-grant.schema.json'
}

class RuntimeValidationError(ValueError):
    pass

def _schema(name):
    return json.loads(SCHEMAS[name].read_text(encoding='utf-8'))

def _assert_finite(value, path='<root>'):
    """Reject NaN/Infinity anywhere in governed data."""
    if isinstance(value, bool) or value is None:
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise RuntimeValidationError(f'{path}: non-finite numeric value is not permitted')
        return
    if isinstance(value, (int, str)):
        return
    if isinstance(value, list):
        for i, item in enumerate(value):
            _assert_finite(item, f'{path}/{i}')
        return
    if isinstance(value, dict):
        for key, item in value.items():
            _assert_finite(item, f'{path}/{key}')
        return

def validate_instance(name,obj):
    _assert_finite(obj)
    errors=sorted(Draft202012Validator(_schema(name)).iter_errors(obj),key=lambda e:list(e.path))
    if errors:
        msg='; '.join(f"{'/'.join(map(str,e.path)) or '<root>'}: {e.message}" for e in errors)
        raise RuntimeValidationError(f'{name}: {msg}')

def validate_runtime_input(input_data):
    _assert_finite(input_data)
    for i,obj in enumerate(input_data.get('objects',[])):
        try:
            validate_instance('knowledge_object',obj)
        except RuntimeValidationError as e:
            raise RuntimeValidationError(f'objects[{i}] {e}') from e
    for i,m in enumerate(input_data.get('models',[])):
        try:
            validate_instance('model_resource',m)
        except RuntimeValidationError as e:
            raise RuntimeValidationError(f'models[{i}] {e}') from e

def validate_pipeline_input(input_data):
    validate_runtime_input(input_data)
    if input_data.get('analysis_result') is not None:
        validate_instance('analysis_result',input_data['analysis_result'])
    if input_data.get('action') is not None:
        validate_instance('action',input_data['action'])
    if input_data.get('capability_grant') is not None:
        validate_instance('capability_grant',input_data['capability_grant'])

def validate_audit(audit):
    validate_instance('audit',audit)

def validate_pipeline_policy(policy):
    """Validate the three-stage policy wrapper and embedded Knowledge policy."""
    _assert_finite(policy)
    validate_instance('pipeline_policy', policy)
    from .compiler import compile_policy, PolicyError
    try:
        compile_policy(policy['knowledge_policy'])
    except PolicyError as e:
        raise RuntimeValidationError(f"knowledge_policy: {e}") from e
    for i, rule in enumerate(policy.get('consequence', {}).get('rules', [])):
        if rule.get('action') is not None:
            try:
                validate_instance('action', rule['action'])
            except RuntimeValidationError as e:
                raise RuntimeValidationError(f"consequence.rules[{i}].action {e}") from e
    return True
