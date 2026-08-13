from __future__ import annotations
from .engine import Engine
from .portable_reference import execute as portable_execute
from .pipeline import PipelineEngine


def _policy(case=None,rules=None,decision=None,pid='conformance',policies=None):
    return {'adgl':{'version':'0.3'},'policy':{'id':pid,'version':1},'case':{'id':'test_case',**(case or {})},
            'rules':rules or [],'policies':policies or [],'decision':decision or {'default':'PERMITTED'},'audit':{'required':True}}
def _obj(result,oid): return next(o for o in result['all_objects'] if str(o.get('id'))==str(oid))
def _run(p,d): return Engine(p).run(d)

def _checks():
    tests=[]
    p=_policy(rules=[{'id':'x','select':{'id':'x'},'do':[{'exclude':{}}]}]); r=_run(p,{'objects':[{'id':'x'},{'id':'y'}]})
    tests.append(('C01 exclusion safety', all(o['id']!='x' for o in r['admissible_objects']) and _obj(r,'x')['_adgl']['disposition']=='EXCLUDED'))
    p=_policy(rules=[{'id':'q','select':{'id':'q'},'do':[{'quarantine':{}}]}]); r=_run(p,{'objects':[{'id':'q'},{'id':'y'}]})
    tests.append(('C02 quarantine isolation', all(o['id']!='q' for o in r['admissible_objects']) and _obj(r,'q')['_adgl']['disposition']=='QUARANTINED'))
    p=_policy(rules=[{'id':'e','select':{'id':'e'},'do':[{'embargo':{'until':{'event':'publication'}}}]}]); r1=_run(p,{'objects':[{'id':'e'}]}); r2=_run(p,{'objects':[{'id':'e'}],'flags':{'events':['publication']}})
    tests.append(('C03 embargo enforcement', _obj(r1,'e')['_adgl']['disposition']=='EMBARGOED' and _obj(r2,'e')['_adgl']['disposition']=='ADMITTED'))
    p=_policy(rules=[{'id':'s','select':{'id':'old'},'do':[{'supersede':{'by':'new'}}]}]); r=_run(p,{'objects':[{'id':'old','evidence_role':'GOVERNING'},{'id':'new','evidence_role':'GOVERNING'}]})
    tests.append(('C04 supersession', _obj(r,'old')['_adgl']['disposition']=='SUPERSEDED' and all(o['id']!='old' for o in r['admissible_objects'])))
    p=_policy(rules=[{'id':'p','select':{'id':'a'},'do':[{'prioritize':{'rank':999}}]}]); r=_run(p,{'objects':[{'id':'a','authority':'organizational'},{'id':'b','authority':'regulatory'}]})
    tests.append(('C05 priority/authority separation', _obj(r,'a')['authority']=='organizational' and _obj(r,'a')['_adgl']['priority']==999))
    p=_policy(rules=[{'id':'r','select':{'id':'reg'},'do':[{'assign_role':{'role':'GOVERNING'}}]}]); r=_run(p,{'objects':[{'id':'reg','authority':'regulatory','applicability':'not_applicable'}]})
    tests.append(('C06 applicability gating', _obj(r,'reg')['_adgl'].get('governing_effective') is False))
    p=_policy(case={'classification':'RESTRICTED'}); r=_run(p,{'objects':[{'id':'d'}],'models':[{'id':'bad','approved':True,'region':'eu','deployment':'managed','allowed_classifications':['PUBLIC']},{'id':'good','approved':True,'region':'eu','deployment':'managed','allowed_classifications':['RESTRICTED']} ]})
    tests.append(('C07 model eligibility', r['selected_model']['id']=='good' and any(x['id']=='bad' for x in r['audit']['route_decision']['rejected'])))
    p=_policy(case={'classification':'RESTRICTED','approved_regions':['eu-central']}); r=_run(p,{'objects':[{'id':'d'}],'models':[{'id':'us','approved':True,'region':'us-east','deployment':'managed','allowed_classifications':['RESTRICTED']},{'id':'eu','approved':True,'region':'eu-central','deployment':'managed','allowed_classifications':['RESTRICTED']}]})
    tests.append(('C08 region safety', r['selected_model']['id']=='eu'))
    p=_policy(case={'classification':'RESTRICTED','approved_regions':['eu-central']},decision={'default':'PERMITTED','on_no_route':'BLOCKED'}); r=_run(p,{'objects':[{'id':'d'}],'models':[{'id':'fallback-us','approved':True,'region':'us-east','deployment':'managed','allowed_classifications':['RESTRICTED']}]})
    tests.append(('C09 fallback safety', r['selected_model'] is None and r['decision_state']=='BLOCKED' and r['reason_code']=='NO_COMPLIANT_ROUTE'))
    p=_policy(rules=[{'id':'req','do':[{'require':{'kind':'evidence_role','role':'GOVERNING'}}]}],decision={'default':'PERMITTED','on_missing_required':'ABSTAINED'}); r=_run(p,{'objects':[{'id':'x'}]})
    tests.append(('C10 mandatory evidence', r['decision_state']=='ABSTAINED' and r['reason_code']=='INSUFFICIENT_EVIDENCE'))
    p=_policy(decision={'default':'PERMITTED','on_unresolved_conflict':'AWAITING_REVIEW'}); c={'type':'AUTHORITY_CONFLICT','between':['a','b'],'resolved':False}; r=_run(p,{'objects':[{'id':'a'},{'id':'b'}],'conflicts':[c]})
    tests.append(('C11 conflict preservation', r['decision_state']=='AWAITING_REVIEW' and r['audit']['conflicts'][0]['type']=='AUTHORITY_CONFLICT'))
    p=_policy(rules=[{'id':'q','select':{'id':'source'},'do':[{'quarantine':{}}]}]); r=_run(p,{'objects':[{'id':'source'},{'id':'summary'}],'relationships':[{'subject':'summary','predicate':'DERIVES_FROM','object':'source'}]})
    tests.append(('C12 derived restriction propagation', _obj(r,'summary')['_adgl']['disposition']=='QUARANTINED'))
    p=_policy(rules=[{'id':'x','select':{'id':'x'},'do':[{'exclude':{'reason':'test'}}]}]); r=_run(p,{'objects':[{'id':'x'},{'id':'y'}]}); a=r['audit']; required=['case_id','policy_ids_and_versions','candidate_object_ids','object_dispositions','decision_state','events']
    tests.append(('C13 audit completeness', all(k in a and a[k] is not None for k in required) and len(a['events'])>=2))
    p=_policy(rules=[{'id':'q','select':{'status':'draft'},'do':[{'quarantine':{}}]},{'id':'p','select':{'status':'approved'},'do':[{'prioritize':{'rank':10}}]}]); data={'objects':[{'id':'a','status':'approved'},{'id':'b','status':'draft'}]}; r1=_run(p,data); r2=_run(p,data)
    sig=lambda r:(r['decision_state'],sorted(r['audit']['object_dispositions'].items()),[(o['id'],o.get('_adgl',{}).get('priority')) for o in r['all_objects']])
    tests.append(('C14 deterministic replay', sig(r1)==sig(r2)))
    native=_run(p,data); alt=portable_execute(p,data); native_sig=(native['decision_state'],native['audit']['object_dispositions'],{o['id']:o.get('_adgl',{}).get('priority') for o in native['all_objects'] if o.get('_adgl',{}).get('priority') is not None}); alt_sig=(alt['decision_state'],alt['object_dispositions'],alt['priorities'])
    tests.append(('C15 cross-implementation equivalence', native_sig==alt_sig))
    # Lower-precedence organizational ALLOW/role assignment is displaced by higher-precedence lifecycle quarantine.
    policies=[{'id':'org','version':1,'precedence_level':'organizational_defaults','rules':[{'id':'allow','select':{'id':'d'},'do':[{'allow':{}},{'assign_role':{'role':'PRIMARY'}}]}]},
              {'id':'life','version':1,'precedence_level':'lifecycle_restrictions','rules':[{'id':'q','select':{'id':'d'},'do':[{'quarantine':{}}]}]}]
    p=_policy(policies=policies); r=_run(p,{'objects':[{'id':'d'}]})
    tests.append(('C16 deterministic policy composition', _obj(r,'d')['_adgl']['disposition']=='QUARANTINED' and len(r['audit']['policy_ids_and_versions'])==3))

    # Three-stage architecture checks.
    p={'knowledge_policy':_policy(pid='analysis-method'),'analysis':{'method':'INFER','allowed_methods':['COMPARE']},'consequence':{'default':'INFORM'}}
    r=PipelineEngine(p).run({'objects':[{'id':'x'}],'analysis_result':{'confidence':0.9,'uses_inferred_missing':False}})
    tests.append(('C17 analysis method governance', r['analysis']['state']=='BLOCKED' and r['analysis']['reason_code']=='ANALYSIS_METHOD_NOT_PERMITTED' and r['consequence']['status']=='NOT_REACHED'))
    p={'knowledge_policy':_policy(pid='no-infer'),'analysis':{'method':'SUMMARIZE','allowed_methods':['SUMMARIZE'],'do_not_infer_missing':True},'consequence':{'default':'INFORM'}}
    r=PipelineEngine(p).run({'objects':[{'id':'x'}],'analysis_result':{'confidence':0.9,'uses_inferred_missing':False,'uses_inferred_missing':True}})
    tests.append(('C18 no-infer-missing', r['analysis']['state']=='BLOCKED' and r['consequence']['status']=='NOT_REACHED'))
    kp=_policy(pid='corroboration',rules=[{'id':'role','select':{'id':'primary'},'do':[{'assign_role':{'role':'PRIMARY'}}]}])
    p={'knowledge_policy':kp,'analysis':{'method':'COMPARE','allowed_methods':['COMPARE'],'require_corroboration':True},'consequence':{'default':'INFORM'}}
    r=PipelineEngine(p).run({'objects':[{'id':'primary'}],'analysis_result':{'confidence':0.9,'uses_inferred_missing':False}})
    tests.append(('C19 analysis corroboration gate', r['analysis']['state']=='INSUFFICIENT' and r['consequence']['status']=='NOT_REACHED'))
    p={'knowledge_policy':_policy(pid='inform'),'analysis':{'method':'SUMMARIZE','allowed_methods':['SUMMARIZE']},'consequence':{'default':'INFORM'}}
    r=PipelineEngine(p).run({'objects':[{'id':'x'}],'analysis_result':{'confidence':0.9,'uses_inferred_missing':False}})
    tests.append(('C20 INFORM disposition', r['consequence']['disposition']=='INFORM'))
    p={'knowledge_policy':_policy(pid='decide'),'analysis':{'method':'SCORE','allowed_methods':['SCORE']},'consequence':{'rules':[{'when':{'analysis.result.risk':'high'},'disposition':'DECIDE','decision_owner':'officer'}]}}
    r=PipelineEngine(p).run({'objects':[{'id':'x'}],'analysis_result':{'confidence':0.9,'uses_inferred_missing':False,'risk':'high'}})
    tests.append(('C21 DECIDE disposition', r['consequence']['disposition']=='DECIDE' and r['consequence']['decision_owner']=='officer'))
    p={'knowledge_policy':_policy(pid='act'),'analysis':{'method':'CLASSIFY','allowed_methods':['CLASSIFY']},'consequence':{'rules':[{'when':{'analysis.result.eligible':True},'disposition':'ACT','action':{'type':'api.write'},'executor':'api'}]}}
    r=PipelineEngine(p).run({'objects':[{'id':'x'}],'analysis_result':{'confidence':0.99,'uses_inferred_missing':False,'eligible':True},'capability_grant':{'id':'g','actions':['api.write'],'case_id':'test_case'}})
    tests.append(('C22 ACT capability authorization', r['consequence']['disposition']=='ACT' and r['consequence']['status']=='AUTHORIZED'))
    p={'knowledge_policy':_policy(pid='approve-act'),'analysis':{'method':'SCORE','allowed_methods':['SCORE']},'consequence':{'rules':[{'when':{'analysis.result.amount':{'between':[101,1000]}},'disposition':'DECIDE','decision_owner':'manager','then':'ACT','action':{'type':'refund'},'executor':'billing'}]}}
    r=PipelineEngine(p).run({'objects':[{'id':'x'}],'analysis_result':{'confidence':0.99,'uses_inferred_missing':False,'amount':420},'human_decision':{'decision':'APPROVE','role':'manager'},'capability_grant':{'id':'g','actions':['refund'],'case_id':'test_case'}})
    tests.append(('C23 DECIDE-to-ACT transition', r['consequence'].get('disposition_path')==['DECIDE','ACT'] and r['consequence']['status']=='AUTHORIZED'))
    stages={e['stage'] for e in r['audit']['events']}
    tests.append(('C24 end-to-end audit stage coverage', {'CASE','ANALYSIS','CONSEQUENCE','AUDIT'}.issubset(stages)))
    p={'knowledge_policy':_policy(pid='grant-scope'),'analysis':{'method':'CLASSIFY','allowed_methods':['CLASSIFY']},'consequence':{'rules':[{'when':{'analysis.result.eligible':True},'disposition':'ACT','action':{'type':'api.write'},'executor':'api'}]}}
    r=PipelineEngine(p).run({'objects':[{'id':'x'}],'analysis_result':{'confidence':0.99,'uses_inferred_missing':False,'eligible':True},'capability_grant':{'id':'g','actions':['api.write'],'case_id':'different_case'}})
    tests.append(('C25 task-scoped action grant', r['consequence']['status']=='BLOCKED' and r['consequence']['reason_code']=='ACTION_NOT_AUTHORIZED'))

    # Candidate execution-integrity checks discovered after the v0.9 paper package.
    p={'knowledge_policy':_policy(pid='upstream-block',decision={'default':'BLOCKED'}),'analysis':{'method':'SUMMARIZE','allowed_methods':['SUMMARIZE']},'consequence':{'default':'INFORM'}}
    r=PipelineEngine(p).run({'objects':[{'id':'x'}],'analysis_result':{'confidence':0.9,'uses_inferred_missing':False}})
    tests.append(('C26 [candidate] upstream terminal propagation', r['analysis']['state']=='NOT_REACHED' and r['consequence']['status']=='NOT_REACHED'))
    from .validation import RuntimeValidationError
    p={'knowledge_policy':_policy(pid='analysis-contract'),'analysis':{'method':'SUMMARIZE','allowed_methods':['SUMMARIZE']},'consequence':{'default':'INFORM'}}
    rejected=False
    try: PipelineEngine(p).run({'objects':[{'id':'x'}],'analysis_result':{}})
    except RuntimeValidationError: rejected=True
    tests.append(('C27 [candidate] minimum AnalysisResult contract', rejected))
    p={'knowledge_policy':_policy(pid='act-no-grant'),'analysis':{'method':'CLASSIFY','allowed_methods':['CLASSIFY']},'consequence':{'rules':[{'when':{'analysis.result.eligible':True},'disposition':'ACT','action':{'type':'api.write'},'executor':'api'}]}}
    r=PipelineEngine(p).run({'objects':[{'id':'x'}],'analysis_result':{'confidence':0.99,'uses_inferred_missing':False,'eligible':True}})
    tests.append(('C28 [candidate] ACT requires explicit authorization', r['consequence']['status']=='BLOCKED' and r['consequence']['reason_code']=='ACTION_AUTHORIZATION_REQUIRED'))
    p={'knowledge_policy':_policy(pid='expired-grant'),'analysis':{'method':'CLASSIFY','allowed_methods':['CLASSIFY']},'consequence':{'rules':[{'when':{'analysis.result.eligible':True},'disposition':'ACT','action':{'type':'api.write'},'executor':'api'}]}}
    r=PipelineEngine(p).run({'objects':[{'id':'x'}],'analysis_result':{'confidence':0.99,'uses_inferred_missing':False,'eligible':True},'capability_grant':{'id':'expired','actions':['api.write'],'case_id':'test_case','expires_at':'2020-01-01T00:00:00Z'}})
    tests.append(('C29 [candidate] expired action grant fails closed', r['consequence']['status']=='BLOCKED' and r['consequence']['reason_code']=='ACTION_GRANT_EXPIRED'))
    eng=PipelineEngine({'knowledge_policy':_policy(pid='grant-quota'),'analysis':{'method':'CLASSIFY','allowed_methods':['CLASSIFY']},'consequence':{'rules':[{'when':{'analysis.result.eligible':True},'disposition':'ACT','action':{'type':'api.write'},'executor':'api'}]}})
    payload={'objects':[{'id':'x'}],'analysis_result':{'confidence':0.99,'uses_inferred_missing':False,'eligible':True},'capability_grant':{'id':'quota','actions':['api.write'],'case_id':'test_case','max_calls':1}}
    first=eng.run(payload); second=eng.run(payload)
    tests.append(('C30 [candidate] in-process action quota enforcement', first['consequence']['status']=='AUTHORIZED' and second['consequence']['status']=='BLOCKED' and second['consequence']['reason_code']=='ACTION_QUOTA_EXCEEDED'))

    p={'knowledge_policy':_policy(pid='effective-action-value'),
       'analysis':{'method':'CLASSIFY','allowed_methods':['CLASSIFY']},
       'consequence':{'rules':[{'when':{'analysis.result.eligible':True},'disposition':'ACT','action':{'type':'billing.issue_refund'},'executor':'billing'}]}}
    r=PipelineEngine(p).run({'objects':[{'id':'x'}],
                             'analysis_result':{'confidence':0.99,'uses_inferred_missing':False,'eligible':True},
                             'action':{'type':'billing.issue_refund','target':'customer-1','financial_value':10000},
                             'capability_grant':{'id':'value','actions':['billing.issue_refund'],'case_id':'test_case','max_value':500}})
    tests.append(('C31 [candidate] effective action value authorization',
                  r['consequence']['status']=='BLOCKED'
                  and r['consequence']['reason_code']=='ACTION_VALUE_LIMIT_EXCEEDED'))

    p={'knowledge_policy':_policy(pid='approval-required'),
       'analysis':{'method':'CLASSIFY','allowed_methods':['CLASSIFY']},
       'consequence':{'rules':[{'when':{'analysis.result.eligible':True},'disposition':'ACT','approval_required':True,'decision_owner':'manager','action':{'type':'api.write'},'executor':'api'}]}}
    r=PipelineEngine(p).run({'objects':[{'id':'x'}],
                             'analysis_result':{'confidence':0.99,'uses_inferred_missing':False,'eligible':True},
                             'action':{'type':'api.write','target':'record-1'},
                             'capability_grant':{'id':'approval','actions':['api.write'],'case_id':'test_case'}})
    tests.append(('C32 [candidate] required human approval cannot be bypassed',
                  r['consequence']['disposition']=='DECIDE'
                  and r['consequence']['status']=='AWAITING_HUMAN_DECISION'))

    # C33 — finite/non-negative numeric governance.
    rejected=False
    try:
        PipelineEngine({'knowledge_policy':_policy(pid='finite-numeric'),
                        'analysis':{'method':'CLASSIFY','allowed_methods':['CLASSIFY']},
                        'consequence':{'default':'INFORM'}}).run({
                            'objects':[{'id':'x'}],
                            'analysis_result':{'confidence':float('nan'),'uses_inferred_missing':False}})
    except RuntimeValidationError:
        rejected=True
    tests.append(('C33 [candidate] finite numeric governance', rejected))

    # C34 — strict, case-scoped CapabilityGrant contract.
    rejected_typo=False
    p={'knowledge_policy':_policy(pid='grant-contract'),
       'analysis':{'method':'CLASSIFY','allowed_methods':['CLASSIFY']},
       'consequence':{'rules':[{'when':{'analysis.result.eligible':True},
                                'disposition':'ACT','action':{'type':'api.write'},'executor':'api'}]}}
    try:
        PipelineEngine(p).run({
            'objects':[{'id':'x'}],
            'analysis_result':{'confidence':0.99,'uses_inferred_missing':False,'eligible':True},
            'capability_grant':{'id':'g','actions':['api.write'],'case_id':'test_case','max_call':1}})
    except RuntimeValidationError:
        rejected_typo=True
    rejected_scope=False
    try:
        PipelineEngine(p).run({
            'objects':[{'id':'x'}],
            'analysis_result':{'confidence':0.99,'uses_inferred_missing':False,'eligible':True},
            'capability_grant':{'id':'g','actions':['api.write']}})
    except RuntimeValidationError:
        rejected_scope=True
    tests.append(('C34 [candidate] CapabilityGrant schema and scope integrity',
                  rejected_typo and rejected_scope))

    # C35 — a completed human decision must resolve a pure DECIDE consequence.
    p={'knowledge_policy':_policy(pid='decide-resolution'),
       'analysis':{'method':'SCORE','allowed_methods':['SCORE']},
       'consequence':{'rules':[{'when':{'analysis.result.risk':'high'},
                                'disposition':'DECIDE','decision_owner':'risk_officer'}]}}
    r=PipelineEngine(p).run({
        'objects':[{'id':'x'}],
        'analysis_result':{'confidence':0.9,'uses_inferred_missing':False,'risk':'high'},
        'human_decision':{'decision':'APPROVE','role':'risk_officer'}})
    tests.append(('C35 [candidate] human DECIDE resolution',
                  r['consequence']['disposition']=='DECIDE'
                  and r['consequence']['status']=='APPROVED_BY_HUMAN'))

    # C36 — policy Action template fields constrain the concrete requested Action.
    p={'knowledge_policy':_policy(pid='action-target'),
       'analysis':{'method':'CLASSIFY','allowed_methods':['CLASSIFY']},
       'consequence':{'rules':[{'when':{'analysis.result.eligible':True},
                                'disposition':'ACT',
                                'action':{'type':'api.write','target':'record-allowed'},
                                'executor':'api'}]}}
    r=PipelineEngine(p).run({
        'objects':[{'id':'x'}],
        'analysis_result':{'confidence':0.99,'uses_inferred_missing':False,'eligible':True},
        'action':{'type':'api.write','target':'record-other'},
        'capability_grant':{'id':'g','actions':['api.write'],'case_id':'test_case'}})
    tests.append(('C36 [candidate] Action target/template constraint enforcement',
                  r['consequence']['status']=='BLOCKED'
                  and r['consequence']['reason_code']=='ACTION_TEMPLATE_MISMATCH'))

    return tests

def run_conformance(verbose=True):
    tests=_checks(); okall=all(ok for _,ok in tests)
    if verbose:
        print('ADGL Conformance Suite v0.5.3 — 25 published normative + 11 candidate integrity checks')
        for name,ok in tests: print(('PASS' if ok else 'FAIL'), name)
        print(f'\n{sum(ok for _,ok in tests)}/{len(tests)} passed')
    return okall
