import json,yaml
from pathlib import Path
from adgl.pipeline import PipelineEngine
ROOT=Path(__file__).resolve().parents[1]

def run_case(name):
    d=ROOT/'examples'/name
    p=yaml.safe_load((d/'policy.yaml').read_text())
    data=json.loads((d/'input.json').read_text())
    exp=json.loads((d/'expected.json').read_text())
    return PipelineEngine(p).run(data),exp

def test_human_validation():
    r,e=run_case('human_validation_during_analysis'); assert r['analysis']['state']==e['analysis_state']; assert r['consequence']['disposition']==e['consequence']; assert r['consequence']['status']==e['consequence_status']; assert not any(x['stage']=='CONSEQUENCE' for x in r['audit']['events'])
def test_human_decision():
    r,e=run_case('human_decision_boundary'); assert r['consequence']['disposition']==e['consequence']
def test_autonomous_action():
    r,e=run_case('autonomous_machine_action'); assert r['consequence']['disposition']==e['consequence']; assert r['consequence']['status']==e['consequence_status']
def test_human_approval_then_action():
    r,e=run_case('human_approval_then_action'); assert r['consequence'].get('disposition_path')==e['path']; assert r['consequence']['status']==e['consequence_status']

def test_pipeline_policy_validation():
    from adgl.validation import validate_pipeline_policy, RuntimeValidationError
    import yaml
    good=yaml.safe_load((ROOT/'examples'/'autonomous_machine_action'/'policy.yaml').read_text())
    assert validate_pipeline_policy(good)
    bad=dict(good); bad['consequence']={'default':'TELEPORT'}
    try:
        validate_pipeline_policy(bad)
    except RuntimeValidationError:
        pass
    else:
        raise AssertionError('invalid consequence disposition was accepted')


def _base_pipeline(pid='p', decision='PERMITTED'):
    return {'knowledge_policy':{'adgl':{'version':'0.3'},'policy':{'id':pid,'version':1},'case':{'id':pid},'rules':[],'decision':{'default':decision},'audit':{'required':True}},'analysis':{'method':'SUMMARIZE','allowed_methods':['SUMMARIZE']},'consequence':{'default':'INFORM'}}

def test_upstream_block_stops_downstream_stages():
    r=PipelineEngine(_base_pipeline('blocked','BLOCKED')).run({'objects':[{'id':'x'}],'analysis_result':{'confidence':0.9,'uses_inferred_missing':False}})
    assert r['analysis']['state']=='NOT_REACHED'; assert r['consequence']['status']=='NOT_REACHED'

def test_empty_analysis_result_rejected_by_schema():
    from adgl.validation import RuntimeValidationError
    try: PipelineEngine(_base_pipeline('analysis-contract')).run({'objects':[{'id':'x'}],'analysis_result':{}})
    except RuntimeValidationError: return
    raise AssertionError('empty AnalysisResult was accepted')

def test_act_without_grant_fails_closed():
    p=_base_pipeline('act-no-grant'); p['analysis']={'method':'CLASSIFY','allowed_methods':['CLASSIFY']}; p['consequence']={'rules':[{'when':{'analysis.result.eligible':True},'disposition':'ACT','action':{'type':'api.write'},'executor':'api'}]}
    r=PipelineEngine(p).run({'objects':[{'id':'x'}],'analysis_result':{'confidence':0.99,'uses_inferred_missing':False,'eligible':True}})
    assert r['consequence']['status']=='BLOCKED'; assert r['consequence']['reason_code']=='ACTION_AUTHORIZATION_REQUIRED'


def test_effective_action_value_limit_uses_requested_action():
    policy = {
        "knowledge_policy": {
            "adgl":{"version":"0.3"}, "policy":{"id":"value-limit","version":1},
            "case":{"id":"value-limit"}, "rules":[],
            "decision":{"default":"PERMITTED"}, "audit":{"required":True},
        },
        "analysis":{"method":"CLASSIFY","allowed_methods":["CLASSIFY"]},
        "consequence":{"rules":[{
            "when":{"analysis.result.eligible":True},
            "disposition":"ACT",
            "action":{"type":"billing.issue_refund"},
            "executor":"billing",
        }]},
    }
    result = PipelineEngine(policy).run({
        "objects":[{"id":"x"}],
        "analysis_result":{"confidence":0.99,"uses_inferred_missing":False,"eligible":True},
        "action":{"type":"billing.issue_refund","target":"customer-1","financial_value":10000},
        "capability_grant":{"id":"g","actions":["billing.issue_refund"],"case_id":"value-limit","max_value":500},
    })
    assert result["consequence"]["status"] == "BLOCKED"
    assert result["consequence"]["reason_code"] == "ACTION_VALUE_LIMIT_EXCEEDED"
    assert result["consequence"]["action"]["financial_value"] == 10000

    missing_value = PipelineEngine(policy).run({
        "objects":[{"id":"x"}],
        "analysis_result":{"confidence":0.99,"uses_inferred_missing":False,"eligible":True},
        "action":{"type":"billing.issue_refund","target":"customer-1"},
        "capability_grant":{"id":"g2","actions":["billing.issue_refund"],"case_id":"value-limit","max_value":500},
    })
    assert missing_value["consequence"]["status"] == "BLOCKED"
    assert missing_value["consequence"]["reason_code"] == "ACTION_VALUE_REQUIRED"


def test_approval_required_cannot_be_bypassed():
    policy = {
        "knowledge_policy": {
            "adgl":{"version":"0.3"}, "policy":{"id":"approval-required","version":1},
            "case":{"id":"approval-required"}, "rules":[],
            "decision":{"default":"PERMITTED"}, "audit":{"required":True},
        },
        "analysis":{"method":"CLASSIFY","allowed_methods":["CLASSIFY"]},
        "consequence":{"rules":[{
            "when":{"analysis.result.eligible":True},
            "disposition":"ACT",
            "approval_required":True,
            "decision_owner":"manager",
            "action":{"type":"api.write"},
            "executor":"api",
        }]},
    }
    engine = PipelineEngine(policy)
    payload = {
        "objects":[{"id":"x"}],
        "analysis_result":{"confidence":0.99,"uses_inferred_missing":False,"eligible":True},
        "action":{"type":"api.write","target":"record-1"},
        "capability_grant":{"id":"g","actions":["api.write"],"case_id":"approval-required"},
    }
    result = engine.run(payload)
    assert result["consequence"]["disposition"] == "DECIDE"
    assert result["consequence"]["status"] == "AWAITING_HUMAN_DECISION"

    approved = dict(payload)
    approved["human_decision"] = {"decision":"APPROVE","role":"manager","actor":"manager-1"}
    result2 = PipelineEngine(policy).run(approved)
    assert result2["consequence"]["disposition"] == "ACT"
    assert result2["consequence"]["status"] == "AUTHORIZED"
    assert result2["consequence"]["disposition_path"] == ["DECIDE", "ACT"]


def test_action_template_type_mismatch_fails_closed():
    policy = {
        "knowledge_policy": {
            "adgl":{"version":"0.3"}, "policy":{"id":"action-mismatch","version":1},
            "case":{"id":"action-mismatch"}, "rules":[],
            "decision":{"default":"PERMITTED"}, "audit":{"required":True},
        },
        "analysis":{"method":"CLASSIFY","allowed_methods":["CLASSIFY"]},
        "consequence":{"rules":[{
            "when":{"analysis.result.eligible":True},
            "disposition":"ACT",
            "action":{"type":"api.write"},
            "executor":"api",
        }]},
    }
    result = PipelineEngine(policy).run({
        "objects":[{"id":"x"}],
        "analysis_result":{"confidence":0.99,"uses_inferred_missing":False,"eligible":True},
        "action":{"type":"api.delete","target":"record-1"},
        "capability_grant":{"id":"g","actions":["api.delete","api.write"],"case_id":"action-mismatch"},
    })
    assert result["consequence"]["status"] == "BLOCKED"
    assert result["consequence"]["reason_code"] == "ACTION_TEMPLATE_MISMATCH"


def test_nonfinite_and_negative_numeric_values_fail_closed():
    from adgl.validation import RuntimeValidationError
    p=_base_pipeline('numeric')
    try:
        PipelineEngine(p).run({
            'objects':[{'id':'x'}],
            'analysis_result':{'confidence':float('nan'),'uses_inferred_missing':False},
        })
    except RuntimeValidationError:
        pass
    else:
        raise AssertionError('NaN confidence was accepted')

    p['analysis']={'method':'CLASSIFY','allowed_methods':['CLASSIFY']}
    p['consequence']={'rules':[{
        'when':{'analysis.result.eligible':True},
        'disposition':'ACT','action':{'type':'api.write'},'executor':'api'
    }]}
    try:
        PipelineEngine(p).run({
            'objects':[{'id':'x'}],
            'analysis_result':{'confidence':0.99,'uses_inferred_missing':False,'eligible':True},
            'action':{'type':'api.write','financial_value':-1},
            'capability_grant':{'id':'g','actions':['api.write'],'case_id':'numeric','max_value':500},
        })
    except RuntimeValidationError:
        pass
    else:
        raise AssertionError('negative financial value was accepted')


def test_capability_grant_is_strict_and_case_scoped():
    from adgl.validation import RuntimeValidationError
    p=_base_pipeline('grant-contract')
    p['analysis']={'method':'CLASSIFY','allowed_methods':['CLASSIFY']}
    p['consequence']={'rules':[{
        'when':{'analysis.result.eligible':True},
        'disposition':'ACT','action':{'type':'api.write'},'executor':'api'
    }]}
    base={
        'objects':[{'id':'x'}],
        'analysis_result':{'confidence':0.99,'uses_inferred_missing':False,'eligible':True},
    }
    for grant in (
        {'id':'g','actions':['api.write']},
        {'id':'g','actions':['api.write'],'case_id':'grant-contract','max_call':1},
    ):
        payload=dict(base); payload['capability_grant']=grant
        try:
            PipelineEngine(p).run(payload)
        except RuntimeValidationError:
            continue
        raise AssertionError(f'invalid CapabilityGrant accepted: {grant}')


def test_human_decide_resolves_all_supported_decisions():
    policy={
        'knowledge_policy':{
            'adgl':{'version':'0.3'},'policy':{'id':'human-resolve','version':1},
            'case':{'id':'human-resolve'},'rules':[],
            'decision':{'default':'PERMITTED'},'audit':{'required':True}},
        'analysis':{'method':'SCORE','allowed_methods':['SCORE']},
        'consequence':{'rules':[{
            'when':{'analysis.result.risk':'high'},
            'disposition':'DECIDE','decision_owner':'risk_officer'}]},
    }
    expected={
        'APPROVE':'APPROVED_BY_HUMAN',
        'CONSENT':'APPROVED_BY_HUMAN',
        'DENY':'DENIED_BY_HUMAN',
        'MODIFY':'MODIFICATION_REQUIRED',
        'REQUEST_EVIDENCE':'EVIDENCE_REQUESTED',
        'DEFER':'DEFERRED',
        'ESCALATE':'ESCALATED',
    }
    for decision,status in expected.items():
        r=PipelineEngine(policy).run({
            'objects':[{'id':'x'}],
            'analysis_result':{'confidence':0.9,'uses_inferred_missing':False,'risk':'high'},
            'human_decision':{'decision':decision,'role':'risk_officer'},
        })
        assert r['consequence']['status']==status


def test_action_template_target_and_nested_parameters_are_constraints():
    policy={
        'knowledge_policy':{
            'adgl':{'version':'0.3'},'policy':{'id':'action-constraint','version':1},
            'case':{'id':'action-constraint'},'rules':[],
            'decision':{'default':'PERMITTED'},'audit':{'required':True}},
        'analysis':{'method':'CLASSIFY','allowed_methods':['CLASSIFY']},
        'consequence':{'rules':[{
            'when':{'analysis.result.eligible':True},
            'disposition':'ACT',
            'action':{'type':'api.write','target':'record-allowed','parameters':{'mode':'safe'}},
            'executor':'api'}]},
    }
    payload={
        'objects':[{'id':'x'}],
        'analysis_result':{'confidence':0.99,'uses_inferred_missing':False,'eligible':True},
        'capability_grant':{'id':'g','actions':['api.write'],'case_id':'action-constraint'},
    }
    bad=dict(payload)
    bad['action']={'type':'api.write','target':'record-other','parameters':{'mode':'safe'}}
    r=PipelineEngine(policy).run(bad)
    assert r['consequence']['status']=='BLOCKED'
    assert r['consequence']['reason_code']=='ACTION_TEMPLATE_MISMATCH'

    good=dict(payload)
    good['action']={
        'type':'api.write','target':'record-allowed',
        'parameters':{'mode':'safe','extra':'allowed-runtime-field'}
    }
    r2=PipelineEngine(policy).run(good)
    assert r2['consequence']['status']=='AUTHORIZED'
