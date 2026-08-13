from __future__ import annotations
import json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator
from .vocabulary import CORE_OPERATIONS, DECISION_STATES, EVIDENCE_ROLES, DEFAULT_PRECEDENCE

SCHEMA_PATH = Path(__file__).resolve().parent/'schemas'/'policy.schema.json'
class PolicyError(ValueError): pass

EXTENSION_PREFIXES = ('x-', 'x_', 'ext:')

def load_policy(path_or_obj):
    if isinstance(path_or_obj,dict): return path_or_obj
    return yaml.safe_load(Path(path_or_obj).read_text(encoding='utf-8'))

def validate_schema(policy):
    schema=json.loads(SCHEMA_PATH.read_text(encoding='utf-8'))
    errors=sorted(Draft202012Validator(schema).iter_errors(policy),key=lambda e:list(e.path))
    if errors:
        raise PolicyError('\n'.join(f"{'/'.join(map(str,e.path)) or '<root>'}: {e.message}" for e in errors))

def _is_extension(name):
    return name.lower().startswith(EXTENSION_PREFIXES) or ':' in name

def _validate_rule(rule):
    lvl = rule.get('precedence_level','case_specific')
    if lvl not in DEFAULT_PRECEDENCE:
        raise PolicyError(f"rule {rule.get('id')}: unknown precedence_level {lvl!r}")
    for item in rule.get('do',[]):
        if isinstance(item,str):
            name=item
            params={}
        elif isinstance(item,dict) and len(item)==1:
            name=next(iter(item)); params=item[name] or {}
        else:
            raise PolicyError(f"rule {rule.get('id')}: every do item must be a string or single-key mapping")
        up=name.upper()
        if up not in CORE_OPERATIONS and not _is_extension(name):
            raise PolicyError(f"rule {rule.get('id')}: unknown operation {name!r}; extensions must be namespaced")
        if up=='ASSIGN_ROLE':
            role=(params or {}).get('role',(params or {}).get('value'))
            if role not in EVIDENCE_ROLES:
                raise PolicyError(f"rule {rule.get('id')}: invalid evidence role {role!r}")

def validate_semantics(policy):
    decisions=policy.get('decision',{})
    for key in ('default','on_missing_required','on_unresolved_conflict','on_no_route'):
        if key in decisions and decisions[key] not in DECISION_STATES:
            raise PolicyError(f"decision.{key}: {decisions[key]!r} is not a canonical decision state")
    for r in policy.get('rules',[]): _validate_rule(r)
    for pol in policy.get('policies',[]):
        if pol.get('precedence_level','organizational_defaults') not in DEFAULT_PRECEDENCE:
            raise PolicyError(f"policy {pol.get('id')}: invalid precedence_level")
        for r in pol.get('rules',[]): _validate_rule({**r, 'precedence_level': r.get('precedence_level',pol.get('precedence_level','organizational_defaults'))})

def _rank(level): return DEFAULT_PRECEDENCE.index(level)

def _rule_restrictiveness(rule):
    restrictive={'DENY','EXCLUDE','QUARANTINE','EMBARGO','REVOKE','EXPIRE','BLOCK','ABSTAIN','REQUIRE_REVIEW','REQUIRE','NO_FALLBACK','DENY_MODEL','DENY_REGION','LOCAL_ONLY'}
    ops=[]
    for x in rule.get('do',[]):
        name=x if isinstance(x,str) else next(iter(x))
        ops.append(name.upper())
    return 1 if any(o in restrictive for o in ops) else 0

def compile_policy(path_or_obj):
    policy=load_policy(path_or_obj); validate_schema(policy); validate_semantics(policy); case=policy['case']
    rules=[]
    # Lower-precedence rules run first. Higher-precedence rules run later and therefore control overwritable dimensions.
    # Within a level, permissive/preference rules run before restrictive rules so stricter constraints dominate.
    def add_rules(source_rules, pid, pver, default_level):
        for order,r in enumerate(source_rules):
            rr=dict(r)
            rr['_policy_id']=pid; rr['_policy_version']=pver
            rr['_precedence_level']=rr.get('precedence_level',default_level)
            rr['_source_order']=order
            rules.append(rr)
    primary=policy.get('policy',{})
    add_rules(policy.get('rules',[]), primary.get('id',case['id']), primary.get('version',case.get('version',1)), 'case_specific')
    for pol in policy.get('policies',[]):
        add_rules(pol.get('rules',[]), pol['id'], pol.get('version',1), pol.get('precedence_level','organizational_defaults'))
    rules.sort(key=lambda r:(-_rank(r['_precedence_level']), _rule_restrictiveness(r), r['_source_order']))
    policy_versions=[{'id':primary.get('id',case['id']),'version':primary.get('version',case.get('version',1))}]
    policy_versions += [{'id':p['id'],'version':p.get('version',1)} for p in policy.get('policies',[])]
    return {
      'adgl_version':policy['adgl']['version'],
      'policy_id':primary.get('id',case['id']), 'policy_version':primary.get('version',case.get('version',1)),
      'policy_versions':policy_versions,
      'case':case,'rules':rules,'decision':policy.get('decision',{}),
      'audit':policy.get('audit',{}),'precedence':DEFAULT_PRECEDENCE,'profiles':policy.get('profiles',['core'])
    }
