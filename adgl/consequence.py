from __future__ import annotations
from datetime import datetime, timezone
import math

from .selectors import matches

class ConsequenceGovernanceError(ValueError):
    pass

TERMINAL_ANALYSIS_BLOCKS = {
    "BLOCKED", "INSUFFICIENT", "AWAITING_VALIDATION", "INVALID_RESULT", "NOT_REACHED"
}

APPROVAL_DECISIONS = {"APPROVE", "CONSENT"}
DENIAL_DECISIONS = {"DENY"}
RESOLUTION_STATUS = {
    "APPROVE": "APPROVED_BY_HUMAN",
    "CONSENT": "APPROVED_BY_HUMAN",
    "DENY": "DENIED_BY_HUMAN",
    "MODIFY": "MODIFICATION_REQUIRED",
    "REQUEST_EVIDENCE": "EVIDENCE_REQUESTED",
    "DEFER": "DEFERRED",
    "ESCALATE": "ESCALATED",
}

def _choose_rule(rules, context):
    for rule in rules or []:
        if matches(context, rule.get("when") or {}, context):
            return rule
    return None

def _parse_utc(value):
    if value is None:
        return None
    dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def _template_matches(template, requested):
    """Policy Action templates are subset constraints over concrete Actions."""
    if isinstance(template, dict):
        if not isinstance(requested, dict):
            return False
        for key, expected in template.items():
            if key not in requested or not _template_matches(expected, requested[key]):
                return False
        return True
    if isinstance(template, list):
        return template == requested
    return template == requested

def _effective_action(rule_action, requested_action):
    template = dict(rule_action or {})
    requested = dict(requested_action or {})
    if template and requested and not _template_matches(template, requested):
        return None, "ACTION_TEMPLATE_MISMATCH", template
    effective = dict(template)
    effective.update(requested)
    return effective, None, template

def _human_gate(rule, context):
    human = context.get("human_decision") or {}
    decision = str(human.get("decision", "")).upper()
    owner = (rule or {}).get("decision_owner")
    asserted_role = human.get("role")
    if not decision:
        return "AWAITING", human, "HUMAN_DECISION_REQUIRED"
    if owner and asserted_role != owner:
        return "AWAITING", human, "HUMAN_DECISION_OWNER_REQUIRED"
    if decision in APPROVAL_DECISIONS:
        return "APPROVED", human, None
    if decision in DENIAL_DECISIONS:
        return "DENIED", human, None
    if decision in RESOLUTION_STATUS:
        return "RESOLVED", human, None
    return "AWAITING", human, "HUMAN_DECISION_REQUIRED"

def _finite_nonnegative(value):
    try:
        v = float(value)
    except Exception:
        return None
    if not math.isfinite(v) or v < 0:
        return None
    return v

def govern_consequence(config: dict | None, context: dict, audit=None) -> dict:
    config = config or {}
    analysis = context.get("analysis", {})

    if analysis.get("state") in TERMINAL_ANALYSIS_BLOCKS:
        out = {
            "disposition": None, "status": "NOT_REACHED",
            "blocked_at": "ANALYSIS", "reason_code": analysis.get("reason_code")
        }
        if audit:
            audit.consequence = out
        return out

    rule = _choose_rule(config.get("rules", []), context)
    disposition = str((rule or {}).get("disposition", config.get("default", "INFORM"))).upper()
    if disposition not in {"INFORM", "DECIDE", "ACT"}:
        raise ConsequenceGovernanceError(f"unknown disposition {disposition}")

    out = {"disposition": disposition, "status": "READY"}
    if rule:
        for key in ("decision_owner", "executor", "action", "approval_required", "reason"):
            if key in rule:
                out[key] = rule[key]

    if disposition == "DECIDE":
        out["status"] = "AWAITING_HUMAN_DECISION"
        gate, human, reason = _human_gate(rule or {}, context)
        out["human_decision"] = human or None
        decision = str(human.get("decision", "")).upper()
        if reason:
            out["reason_code"] = reason
        elif gate == "APPROVED" and (rule or {}).get("then") == "ACT":
            out["disposition_path"] = ["DECIDE", "ACT"]
            out["disposition"] = "ACT"
            out["status"] = "PENDING_ACTION_AUTHORIZATION"
            out["executor"] = (rule or {}).get("executor")
            out["action"] = (rule or {}).get("action")
        elif gate in {"APPROVED", "DENIED", "RESOLVED"}:
            out["status"] = RESOLUTION_STATUS.get(decision, "RESOLVED_BY_HUMAN")

    if disposition == "ACT" and bool((rule or {}).get("approval_required")):
        gate, human, reason = _human_gate(rule or {}, context)
        out["human_decision"] = human or None
        out["disposition_path"] = ["DECIDE", "ACT"]
        decision = str(human.get("decision", "")).upper()
        if gate == "APPROVED":
            out["disposition"] = "ACT"
            out["status"] = "PENDING_ACTION_AUTHORIZATION"
        else:
            out["disposition"] = "DECIDE"
            if gate in {"DENIED", "RESOLVED"}:
                out["status"] = RESOLUTION_STATUS.get(decision, "RESOLVED_BY_HUMAN")
            else:
                out["status"] = "AWAITING_HUMAN_DECISION"
                out["reason_code"] = reason or "HUMAN_DECISION_REQUIRED"

    if out["disposition"] == "ACT":
        grant = context.get("capability_grant") or {}
        effective_action, template_reason, action_template = _effective_action(
            out.get("action"), context.get("action")
        )
        if action_template:
            out["action_template"] = action_template
        out["action"] = effective_action

        if template_reason:
            out["status"] = "BLOCKED"
            out["reason_code"] = template_reason
        elif not grant:
            out["status"] = "BLOCKED"
            out["reason_code"] = "ACTION_AUTHORIZATION_REQUIRED"
        else:
            allowed = set(grant.get("actions", []))
            requested_type = effective_action.get("type") if isinstance(effective_action, dict) else str(effective_action)
            reason = None

            if not allowed or requested_type not in allowed:
                reason = "ACTION_NOT_AUTHORIZED"

            case_id = (context.get("case") or {}).get("id")
            if not reason and grant.get("case_id") != case_id:
                reason = "ACTION_NOT_AUTHORIZED"

            if not reason and grant.get("max_value") is not None:
                if not isinstance(effective_action, dict) or effective_action.get("financial_value") is None:
                    reason = "ACTION_VALUE_REQUIRED"
                else:
                    action_value = _finite_nonnegative(effective_action.get("financial_value"))
                    limit = _finite_nonnegative(grant.get("max_value"))
                    if action_value is None or limit is None:
                        reason = "ACTION_VALUE_INVALID"
                    elif action_value > limit:
                        reason = "ACTION_VALUE_LIMIT_EXCEEDED"

            if not reason and grant.get("expires_at"):
                try:
                    if datetime.now(timezone.utc) > _parse_utc(grant.get("expires_at")):
                        reason = "ACTION_GRANT_EXPIRED"
                except Exception:
                    reason = "ACTION_GRANT_INVALID"

            used = int(context.get("_grant_calls_used", 0) or 0)
            if not reason and grant.get("max_calls") is not None and used >= int(grant.get("max_calls")):
                reason = "ACTION_QUOTA_EXCEEDED"

            if reason:
                out["status"] = "BLOCKED"
                out["reason_code"] = reason
            else:
                out["grant_id"] = grant.get("id")
                out["status"] = "AUTHORIZED"

    if audit:
        audit.consequence = out
        audit.event(
            stage="CONSEQUENCE",
            action=out.get("disposition") or "NOT_REACHED",
            metadata=out,
        )
    return out
