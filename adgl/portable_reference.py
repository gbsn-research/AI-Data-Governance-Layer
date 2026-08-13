"""Independent minimal interpreter used only for cross-implementation conformance.
It intentionally does not import Engine, operations.py, selectors.py, or compiler.py.
"""
from copy import deepcopy

def _get(o,path):
    cur=o
    for part in path.split('.'):
        if not isinstance(cur,dict) or part not in cur:return None
        cur=cur[part]
    return cur

def _match(o,sel):
    if not sel:return True
    if 'all' in sel:return all(_match(o,x) for x in sel['all'])
    if 'any' in sel:return any(_match(o,x) for x in sel['any'])
    for k,v in sel.items():
        a=_get(o,k)
        if isinstance(v,dict) and 'in' in v:
            if a not in v['in']:return False
        elif a!=v:return False
    return True

def execute(policy,data):
    objs=deepcopy(data.get('objects',[]))
    states={str(o.get('id')):'ADMITTED' for o in objs}
    priorities={}
    for rule in policy.get('rules',[]):
        targets=[o for o in objs if _match(o,rule.get('select'))]
        for op in rule.get('do',[]):
            name=op if isinstance(op,str) else next(iter(op)); params={} if isinstance(op,str) else (op[name] or {})
            up=name.upper()
            for o in targets:
                oid=str(o.get('id'))
                if up=='EXCLUDE': states[oid]='EXCLUDED'
                elif up=='QUARANTINE': states[oid]='QUARANTINED'
                elif up=='DENY': states[oid]='DENIED'
                elif up=='ALLOW' and states[oid]=='ADMITTED': states[oid]='ADMITTED'
                elif up=='PRIORITIZE': priorities[oid]=params.get('rank',params.get('value',100))
    return {'decision_state':policy.get('decision',{}).get('default','PERMITTED'),'object_dispositions':states,'priorities':priorities}
