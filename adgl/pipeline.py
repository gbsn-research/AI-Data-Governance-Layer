from __future__ import annotations
from .engine import Engine
from .analysis import govern_analysis
from .consequence import govern_consequence
from .validation import validate_pipeline_input, validate_pipeline_policy

KNOWLEDGE_STATES_PERMITTING_ANALYSIS = {"PERMITTED", "QUALIFIED"}

class PipelineEngine:
    """Reference orchestrator for Knowledge -> Analysis -> Consequence Governance.

    Toolkit 0.5.3 includes fail-closed candidate integrity behavior identified during
    implementation testing. Checks C26-C36 are explicitly marked candidate
    semantics for the next specification-hardening revision.
    """
    def __init__(self, policy):
        validate_pipeline_policy(policy)
        self.policy=policy
        self.knowledge_engine=Engine(policy.get('knowledge_policy',policy))
        self.analysis_config=policy.get('analysis',{})
        self.consequence_config=policy.get('consequence',{})
        self._grant_call_counts={}

    def _rehydrate_audit(self,knowledge):
        from .audit import AuditRecord, AuditEvent
        a=knowledge['audit']
        audit_obj=AuditRecord(case_id=a['case_id'],purpose=a.get('purpose'),policy_ids_and_versions=a.get('policy_ids_and_versions',[]),candidate_object_ids=a.get('candidate_object_ids',[]))
        for field in ('object_dispositions','authority_and_applicability_results','evidence_roles','model_resource','processing_environment','route_decision','conflicts','human_events','decision_state','reason_code','derivation_links','timestamps'):
            setattr(audit_obj,field,a.get(field))
        audit_obj.events=[AuditEvent(**e) for e in a.get('events',[])]
        if audit_obj.events and audit_obj.events[-1].stage=='AUDIT' and audit_obj.events[-1].action=='COMPLETE':
            audit_obj.events[-1].stage='KNOWLEDGE'; audit_obj.events[-1].action='KNOWLEDGE_COMPLETE'
        return audit_obj

    def run(self,input_data):
        validate_pipeline_input(input_data)
        knowledge=self.knowledge_engine.run(input_data)
        audit_obj=self._rehydrate_audit(knowledge)
        context={**input_data,'case':knowledge['case'],'admissible_objects':knowledge['admissible_objects'],'selected_model':knowledge['selected_model'],'knowledge_decision_state':knowledge['decision_state']}

        if knowledge['decision_state'] not in KNOWLEDGE_STATES_PERMITTING_ANALYSIS:
            analysis={'method':str(self.analysis_config.get('method','SUMMARIZE')).upper(),'state':'NOT_REACHED','reason_code':'KNOWLEDGE_STAGE_NOT_PERMITTED','confidence':None,'result':None,'evidence_count':len(knowledge['admissible_objects']),'human_validation':input_data.get('human_validation')}
            consequence={'disposition':None,'status':'NOT_REACHED','blocked_at':'KNOWLEDGE','reason_code':knowledge.get('reason_code') or 'KNOWLEDGE_STAGE_NOT_PERMITTED'}
            audit_obj.analysis=analysis; audit_obj.consequence=consequence; audit_obj.decision_state=knowledge['decision_state']
            audit_obj.event(stage='AUDIT',action='PIPELINE_PAUSED',metadata={'analysis_state':analysis['state'],'consequence':None,'blocked_at':'KNOWLEDGE'})
            return {'case':knowledge['case'],'knowledge':knowledge,'analysis':analysis,'consequence':consequence,'audit':audit_obj.to_dict()}

        if input_data.get('analysis_result') is None:
            analysis={'method':str(self.analysis_config.get('method','SUMMARIZE')).upper(),'state':'INVALID_RESULT','reason_code':'ANALYSIS_RESULT_REQUIRED','confidence':None,'result':None,'evidence_count':len(knowledge['admissible_objects']),'human_validation':input_data.get('human_validation')}
            consequence={'disposition':None,'status':'NOT_REACHED','blocked_at':'ANALYSIS','reason_code':'ANALYSIS_RESULT_REQUIRED'}
            audit_obj.analysis=analysis; audit_obj.consequence=consequence
            audit_obj.event(stage='ANALYSIS',action='REJECT_RESULT',metadata={'state':'INVALID_RESULT','reason_code':'ANALYSIS_RESULT_REQUIRED'})
            audit_obj.event(stage='AUDIT',action='PIPELINE_PAUSED',metadata={'analysis_state':'INVALID_RESULT','blocked_at':'ANALYSIS'})
            return {'case':knowledge['case'],'knowledge':knowledge,'analysis':analysis,'consequence':consequence,'audit':audit_obj.to_dict()}

        analysis=govern_analysis(self.analysis_config,context,audit_obj)
        context['analysis']=analysis
        grant=input_data.get('capability_grant') or {}; grant_id=grant.get('id')
        if grant_id: context['_grant_calls_used']=self._grant_call_counts.get(str(grant_id),0)
        consequence=govern_consequence(self.consequence_config,context,audit_obj)
        if consequence.get('disposition')=='ACT' and consequence.get('status')=='AUTHORIZED' and grant_id:
            self._grant_call_counts[str(grant_id)]=self._grant_call_counts.get(str(grant_id),0)+1
        audit_obj.decision_state=knowledge['decision_state']
        final='PIPELINE_COMPLETE' if consequence.get('status')!='NOT_REACHED' else 'PIPELINE_PAUSED'
        audit_obj.event(stage='AUDIT',action=final,metadata={'analysis_state':analysis['state'],'consequence':consequence.get('disposition'),'blocked_at':consequence.get('blocked_at')})
        return {'case':knowledge['case'],'knowledge':knowledge,'analysis':analysis,'consequence':consequence,'audit':audit_obj.to_dict()}
