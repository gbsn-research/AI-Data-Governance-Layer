import random
from collections import defaultdict
from .util import get_path, set_path
TERMINAL={'DENIED','EXCLUDED','QUARANTINED','EMBARGOED','REVOKED','EXPIRED','ARCHIVED','SUPERSEDED','ISOLATED'}

def disp(o): return o.setdefault('_adgl',{}).setdefault('disposition','CANDIDATE')
def set_disp(o,v): o.setdefault('_adgl',{})['disposition']=v
def restrict(o,r):
    arr=o.setdefault('_adgl',{}).setdefault('restrictions',[])
    if r not in arr: arr.append(r)

def apply_object_operation(name,obj,params,state,audit,rule_id=None):
    name=name.upper(); p=params if isinstance(params,dict) else {}; before=dict(obj.get('_adgl',{})); reason=p.get('reason')
    if name=='ALLOW':
        if disp(obj) not in TERMINAL: set_disp(obj,'ADMITTED')
    elif name=='DENY': set_disp(obj,'DENIED')
    elif name=='EXCLUDE': set_disp(obj,'EXCLUDED')
    elif name=='QUARANTINE': set_disp(obj,'QUARANTINED')
    elif name=='EMBARGO': set_disp(obj,'EMBARGOED'); obj.setdefault('_adgl',{})['release_condition']=p.get('until')
    elif name=='ISOLATE': set_disp(obj,'ISOLATED'); obj.setdefault('_adgl',{})['pool']=p.get('pool')
    elif name=='RELEASE':
        if disp(obj) in {'QUARANTINED','EMBARGOED','ISOLATED'}: set_disp(obj,'ADMITTED')
    elif name=='SUPERSEDE': set_disp(obj,'SUPERSEDED'); obj.setdefault('_adgl',{})['superseded_by']=p.get('by')
    elif name=='EXPIRE': set_disp(obj,'EXPIRED')
    elif name=='REVOKE': set_disp(obj,'REVOKED')
    elif name=='ARCHIVE': set_disp(obj,'ARCHIVED')
    elif name=='PRIORITIZE': obj.setdefault('_adgl',{})['priority']=p.get('rank',p.get('value',100))
    elif name=='DEPRIORITIZE': obj.setdefault('_adgl',{})['priority']=p.get('rank',p.get('value',-100))
    elif name=='ASSIGN_ROLE': obj.setdefault('_adgl',{})['evidence_role']=p.get('role',p.get('value'))
    elif name=='REQUIRE_CORROBORATION': restrict(obj,{'type':'require_corroboration',**p})
    elif name=='REQUIRE_PROVENANCE':
        required=p.get('status',p.get('value','verified'))
        if get_path(obj,'provenance_status') != required: set_disp(obj,'QUARANTINED'); obj.setdefault('_adgl',{})['failure']='PROVENANCE_UNRESOLVED'
    elif name=='MARK_PROVENANCE': set_path(obj,'provenance_status',p.get('status',p.get('value')))
    elif name in {'REQUIRE_MODEL','DENY_MODEL','REQUIRE_REGION','DENY_REGION','LOCAL_ONLY','NO_FALLBACK','REQUIRE_VALIDATED_VERSION'}: restrict(obj,{'type':name.lower(),**p})
    elif name in {'TRACE','VERIFY_SOURCE','FILTER','COMPARE','SORT','LIMIT','SAMPLE','GROUP','AGGREGATE','OVERRIDE','DEFER_TO'}:
        obj.setdefault('_adgl',{}).setdefault('operations',[]).append({'name':name,'params':p})
    else:
        obj.setdefault('_adgl',{}).setdefault('extensions',[]).append({'name':name,'params':p})
    audit.event(stage='APPLY',action=name,target_id=str(obj.get('id')),rule_id=rule_id,reason=reason,before=before,after=dict(obj.get('_adgl',{})))

def sample_objects(objects,params):
    method=params.get('method','random'); size=min(int(params.get('size',len(objects))),len(objects)); rng=random.Random(params.get('seed',0))
    if method=='random': return rng.sample(objects,size)
    if method=='systematic':
        if size<=0:return []
        step=max(1,len(objects)//size); return objects[::step][:size]
    return objects[:size]

def group_objects(objects,params):
    by=params.get('by'); g=defaultdict(list)
    for o in objects:g[str(get_path(o,by))].append(o)
    return dict(g)
