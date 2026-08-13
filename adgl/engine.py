from __future__ import annotations
from .compiler import compile_policy
from .selectors import matches, filter_objects
from .operations import apply_object_operation, disp, sample_objects, group_objects
from .audit import AuditRecord
from .util import deep_copy_json, get_path
from .validation import validate_runtime_input, validate_audit
from .vocabulary import DECISION_OPERATION_TO_STATE

RESTRICTIVE = {'DENIED','EXCLUDED','QUARANTINED','EMBARGOED','REVOKED','EXPIRED','ARCHIVED','SUPERSEDED'}

class Engine:
    def __init__(self, policy):
        self.ir = compile_policy(policy)

    def _condition(self, cond, state):
        if not cond:
            return True
        obj = {
            'case': state['case'], 'state': state, 'flags': state.get('flags', {}),
            'selected_model': state.get('selected_model'),
            'processing_environment': state.get('processing_environment')
        }
        return matches(obj, cond, state)

    def _eligible_models(self, models, case, state):
        eligible, rejected = [], []
        cls = case.get('classification')
        regions = case.get('approved_regions')
        for m in models:
            reasons = []
            if cls and m.get('allowed_classifications') is not None and cls not in m.get('allowed_classifications', []):
                reasons.append('classification_not_permitted')
            if regions and m.get('region') not in regions:
                reasons.append('processing_region_not_permitted')
            if m.get('approved') is False:
                reasons.append('model_not_approved')
            if m.get('validated') is False and case.get('require_validated_model'):
                reasons.append('model_version_not_validated')
            if case.get('require_customer_controlled') and m.get('deployment') != 'customer_controlled':
                reasons.append('deployment_not_customer_controlled')
            (rejected if reasons else eligible).append({'model': m, 'reasons': reasons} if reasons else m)
        return eligible, rejected

    def _release_embargoes(self, objects, state, audit):
        now = state.get('flags', {}).get('now')
        events = set(state.get('flags', {}).get('events', []))
        for o in objects:
            meta = o.get('_adgl', {})
            if meta.get('disposition') != 'EMBARGOED':
                continue
            cond = meta.get('release_condition')
            released = False
            if isinstance(cond, dict):
                if 'event' in cond and cond['event'] in events:
                    released = True
                if 'date' in cond and now and str(now) >= str(cond['date']):
                    released = True
            if released:
                before = meta.get('disposition')
                meta['disposition'] = 'ADMITTED'
                audit.event(stage='LIFECYCLE', action='RELEASE', target_id=str(o.get('id')), before=before, after='ADMITTED')

    def _propagate_restrictions(self, objects, relationships, audit):
        by_id = {o.get('id'): o for o in objects}
        changed = True
        while changed:
            changed = False
            for rel in relationships:
                if rel.get('predicate') != 'DERIVES_FROM':
                    continue
                child = by_id.get(rel.get('subject'))
                parent = by_id.get(rel.get('object'))
                if not child or not parent:
                    continue
                pmeta, cmeta = parent.setdefault('_adgl', {}), child.setdefault('_adgl', {})
                pdisp = pmeta.get('disposition')
                if pdisp in RESTRICTIVE and cmeta.get('disposition') not in RESTRICTIVE:
                    before = cmeta.get('disposition')
                    cmeta['disposition'] = pdisp
                    cmeta.setdefault('inherited_restrictions', []).append({'from': parent.get('id'), 'disposition': pdisp})
                    audit.event(stage='PROPAGATE', action='INHERIT_RESTRICTION', target_id=str(child.get('id')), before=before, after=pdisp, metadata={'from': parent.get('id')})
                    changed = True
                for key in ('restrictions',):
                    for restriction in pmeta.get(key, []):
                        if restriction not in cmeta.setdefault(key, []):
                            cmeta[key].append(restriction)
                            changed = True

    def _resolve_authority_applicability(self, objects, audit):
        # Reference behavior: governing authority only has effect if applicability is not explicitly false/not_applicable.
        for o in objects:
            role = o.get('_adgl', {}).get('evidence_role') or o.get('evidence_role')
            app = o.get('applicability')
            if role == 'GOVERNING' and str(app).lower() in {'false','not_applicable','inapplicable'}:
                o.setdefault('_adgl', {})['governing_effective'] = False
            elif role == 'GOVERNING':
                o.setdefault('_adgl', {})['governing_effective'] = True
            oid = str(o.get('id'))
            if role or 'authority' in o or 'applicability' in o:
                audit.authority_and_applicability_results[oid] = {
                    'authority': o.get('authority'),
                    'applicability': o.get('applicability'),
                    'governing_effective': o.get('_adgl', {}).get('governing_effective')
                }

    def run(self, input_data):
        validate_runtime_input(input_data)
        objects = deep_copy_json(input_data.get('objects', []))
        models = deep_copy_json(input_data.get('models', []))
        case = deep_copy_json(self.ir['case'])
        case.update(input_data.get('case', {}))
        state = {
            'case': case, 'objects': objects, 'models': models,
            'flags': deep_copy_json(input_data.get('flags', {})),
            'relationships': deep_copy_json(input_data.get('relationships', [])),
            'conflicts': deep_copy_json(input_data.get('conflicts', [])),
            'human_events': [], 'reason_code': None, 'selected_model': None, 'processing_environment': None,
            'decision_state': None, 'requirements': [], 'groups': {}, 'errors': []
        }
        audit = AuditRecord(
            case_id=case['id'], purpose=case.get('purpose'),
            policy_ids_and_versions=self.ir.get('policy_versions',[{'id': self.ir['policy_id'], 'version': self.ir['policy_version']}]),
            candidate_object_ids=[str(o.get('id')) for o in objects]
        )
        audit.event(stage='CASE', action='INITIALIZE', metadata={'case': case})
        for o in objects:
            o.setdefault('_adgl', {})['disposition'] = 'CANDIDATE'

        for rule in self.ir['rules']:
            rid = rule.get('id')
            if not self._condition(rule.get('when') or rule.get('if'), state):
                continue
            targets = filter_objects(objects, rule.get('select'), state)
            for op in rule.get('do', []):
                opname = op if isinstance(op, str) else next(iter(op))
                params = {} if isinstance(op, str) else (op[opname] or {})
                up = opname.upper()
                if up == 'SAMPLE':
                    sampled = sample_objects(targets, params); chosen = {id(x) for x in sampled}
                    for obj in targets:
                        if id(obj) not in chosen: obj.setdefault('_adgl', {})['sampled_out'] = True
                    audit.event(stage='APPLY', action='SAMPLE', rule_id=rid, metadata={'selected':[o.get('id') for o in sampled], 'params': params})
                elif up == 'GROUP':
                    groups = group_objects(targets, params); state['groups'][rid or 'group'] = groups
                    audit.event(stage='APPLY', action='GROUP', rule_id=rid, metadata={'by': params.get('by')})
                elif up == 'REQUIRE':
                    state['requirements'].append({'rule_id': rid, **params})
                    audit.event(stage='APPLY', action='REQUIRE', rule_id=rid, metadata=params)
                elif up == 'ROUTE':
                    eligible, rejected = self._eligible_models(models, case, state); candidates = eligible
                    for k,v in params.items():
                        if k not in {'reason','fallback'}:
                            candidates = [m for m in candidates if get_path(m,k) == v]
                    if candidates:
                        state['selected_model'] = sorted(candidates, key=lambda m:m.get('priority',0), reverse=True)[0]
                        audit.model_resource = state['selected_model']
                        audit.processing_environment = {'region':state['selected_model'].get('region'),'deployment':state['selected_model'].get('deployment')}
                        audit.route_decision = {'selected':state['selected_model'].get('id'),'rejected':[{'id':r['model'].get('id'),'reasons':r['reasons']} for r in rejected]}
                        audit.event(stage='ROUTE', action='ROUTE', rule_id=rid, target_id=state['selected_model'].get('id'))
                    else:
                        state['errors'].append('NO_COMPLIANT_ROUTE')
                        audit.event(stage='ROUTE', action='NO_COMPLIANT_ROUTE', rule_id=rid)
                        if params.get('fallback') == 'deny' and state['decision_state'] is None:
                            state['decision_state'] = self.ir['decision'].get('on_no_route','BLOCKED'); state['reason_code']='NO_COMPLIANT_ROUTE'
                elif up in {'BLOCK','ABSTAIN','ESCALATE','QUALIFY','PERMIT','REQUIRE_REVIEW'}:
                    state['decision_state'] = DECISION_OPERATION_TO_STATE[up]
                    if up == 'REQUIRE_REVIEW': state['human_events'].append({'required_role':params.get('role'),'rule_id':rid})
                    audit.event(stage='DECIDE', action=up, rule_id=rid, metadata=params)
                elif up == 'STOP':
                    state['flags']['stopped'] = True; audit.event(stage='CONTROL', action='STOP', rule_id=rid); break
                else:
                    for obj in targets:
                        apply_object_operation(up, obj, params, state, audit, rule_id=rid)
            if state['flags'].get('stopped'):
                break

        # Release only where explicit release condition is satisfied.
        self._release_embargoes(objects, state, audit)

        # Candidates become admitted after policy evaluation; restrictive states remain restrictive.
        for o in objects:
            if disp(o) == 'CANDIDATE':
                o['_adgl']['disposition'] = 'ADMITTED'

        # Propagate source restrictions to derivatives.
        self._propagate_restrictions(objects, state['relationships'], audit)
        self._resolve_authority_applicability(objects, audit)

        for o in objects:
            oid = str(o.get('id'))
            audit.object_dispositions[oid] = o.get('_adgl', {}).get('disposition')
            if o.get('_adgl', {}).get('evidence_role'):
                audit.evidence_roles[oid] = o['_adgl']['evidence_role']
        audit.derivation_links = [r for r in state['relationships'] if r.get('predicate') == 'DERIVES_FROM']

        # Mandatory evidence/model requirements.
        missing = []
        for req in state['requirements']:
            if req.get('kind') == 'evidence_role':
                role = req.get('role')
                ok = any(o.get('_adgl',{}).get('evidence_role') == role and o.get('_adgl',{}).get('disposition') == 'ADMITTED' for o in objects)
                if not ok: missing.append(req)
            elif req.get('kind') == 'source':
                sid = req.get('source_id')
                ok = any(get_path(o,'source.id') == sid and o.get('_adgl',{}).get('disposition') == 'ADMITTED' for o in objects)
                if not ok: missing.append(req)
            elif req.get('kind') == 'model' and state['selected_model'] is None:
                missing.append(req)
        if missing and state['decision_state'] is None:
            state['decision_state'] = self.ir['decision'].get('on_missing_required', 'ABSTAINED'); state['reason_code']='INSUFFICIENT_EVIDENCE'
            audit.event(stage='VERIFY', action='MANDATORY_EVIDENCE_MISSING', metadata={'requirements':missing})

        # Conflict preservation.
        if state['conflicts']:
            audit.conflicts = state['conflicts']
            unresolved = [c for c in state['conflicts'] if not c.get('resolved')]
            if unresolved and state['decision_state'] is None:
                state['decision_state'] = self.ir['decision'].get('on_unresolved_conflict', 'AWAITING_REVIEW'); state['reason_code']='POLICY_CONFLICT'
                audit.event(stage='VERIFY', action='UNRESOLVED_CONFLICT', metadata={'conflicts':unresolved})

        # Default model route cannot bypass case constraints.
        if models and state['selected_model'] is None:
            eligible, rejected = self._eligible_models(models, case, state)
            if eligible:
                state['selected_model'] = sorted(eligible, key=lambda m:m.get('priority',0), reverse=True)[0]
                audit.model_resource = state['selected_model']
                audit.processing_environment = {'region':state['selected_model'].get('region'),'deployment':state['selected_model'].get('deployment')}
                audit.route_decision = {'selected':state['selected_model'].get('id'),'rejected':[{'id':r['model'].get('id'),'reasons':r['reasons']} for r in rejected]}
            elif state['decision_state'] is None:
                state['decision_state'] = self.ir['decision'].get('on_no_route','BLOCKED'); state['reason_code']='NO_COMPLIANT_ROUTE'
                audit.event(stage='ROUTE', action='NO_COMPLIANT_ROUTE')

        if state['decision_state'] is None:
            state['decision_state'] = self.ir['decision'].get('default', 'PERMITTED')
        audit.decision_state = state['decision_state']
        audit.reason_code = state.get('reason_code')
        audit.human_events = state['human_events']
        audit.event(stage='AUDIT', action='COMPLETE', metadata={'decision':state['decision_state']})
        audit_dict = audit.to_dict()
        validate_audit(audit_dict)

        admissible = [o for o in objects if o.get('_adgl',{}).get('disposition') == 'ADMITTED' and not o.get('_adgl',{}).get('sampled_out')]
        return {
            'case': case, 'decision_state': state['decision_state'],
            'admissible_objects': admissible, 'all_objects': objects,
            'selected_model': state['selected_model'], 'reason_code': state.get('reason_code'), 'errors': state['errors'],
            'audit': audit_dict
        }
