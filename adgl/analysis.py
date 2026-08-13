from __future__ import annotations
class AnalysisGovernanceError(ValueError): pass
DEFAULT_METHODS={"COMPARE","CLASSIFY","SUMMARIZE","CALCULATE","SCORE","ESTIMATE","INFER","CORROBORATE","CHALLENGE","VERIFY"}

def govern_analysis(config:dict|None,context:dict,audit=None)->dict:
    config=config or {}; method=str(config.get('method','SUMMARIZE')).upper(); allowed={str(x).upper() for x in config.get('allowed_methods',list(DEFAULT_METHODS))}
    result=dict(context.get('analysis_result') or {}); state='READY'; reason=None
    if not result: state='INVALID_RESULT'; reason='ANALYSIS_RESULT_REQUIRED'
    if state=='READY' and method not in allowed: state='BLOCKED'; reason='ANALYSIS_METHOD_NOT_PERMITTED'
    evidence=context.get('admissible_objects',[]); min_evidence=int(config.get('min_evidence',0) or 0)
    if state=='READY' and len(evidence)<min_evidence: state='INSUFFICIENT'; reason='INSUFFICIENT_EVIDENCE'
    if state=='READY' and config.get('require_corroboration'):
        roles={o.get('_adgl',{}).get('evidence_role') or o.get('evidence_role') for o in evidence}
        if 'CORROBORATING' not in roles: state='INSUFFICIENT'; reason='INSUFFICIENT_EVIDENCE'
    if state=='READY' and config.get('do_not_infer_missing') and result.get('uses_inferred_missing'): state='BLOCKED'; reason='ANALYSIS_METHOD_NOT_PERMITTED'
    threshold=config.get('validation_below_confidence'); confidence=result.get('confidence')
    if state=='READY' and threshold is not None and confidence is not None and float(confidence)<float(threshold):
        validation=context.get('human_validation') or {}
        if str(validation.get('decision','')).upper() in {'APPROVE','VALIDATE','VERIFIED'}: state='VERIFIED'
        else: state='AWAITING_VALIDATION'; reason='ANALYSIS_VALIDATION_REQUIRED'
    elif state=='READY':
        state=str(result.get('state','VERIFIED')).upper()
        if state not in {'VERIFIED','QUALIFIED'}: state='VERIFIED'
    governed={'method':method,'state':state,'reason_code':reason,'confidence':confidence,'result':result,'evidence_count':len(evidence),'human_validation':context.get('human_validation')}
    if audit:
        audit.analysis=governed
        audit.event(stage='ANALYSIS',action='EVALUATE' if state!='INVALID_RESULT' else 'REJECT_RESULT',metadata={'method':method,'state':state,'reason_code':reason,'evidence_count':len(evidence)})
    return governed
