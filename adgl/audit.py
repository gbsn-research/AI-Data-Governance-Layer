from dataclasses import dataclass, field, asdict
from .util import now_iso

@dataclass
class AuditEvent:
    stage: str
    action: str
    target_id: str | None = None
    rule_id: str | None = None
    reason: str | None = None
    before: object | None = None
    after: object | None = None
    metadata: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=now_iso)

@dataclass
class AuditRecord:
    case_id: str
    purpose: str | None = None
    policy_ids_and_versions: list = field(default_factory=list)
    candidate_object_ids: list = field(default_factory=list)
    object_dispositions: dict = field(default_factory=dict)
    authority_and_applicability_results: dict = field(default_factory=dict)
    evidence_roles: dict = field(default_factory=dict)
    model_resource: dict | None = None
    processing_environment: dict | None = None
    route_decision: dict = field(default_factory=dict)
    conflicts: list = field(default_factory=list)
    human_events: list = field(default_factory=list)
    analysis: dict = field(default_factory=dict)
    consequence: dict = field(default_factory=dict)
    decision_state: str | None = None
    reason_code: str | None = None
    derivation_links: list = field(default_factory=list)
    timestamps: list = field(default_factory=list)
    events: list = field(default_factory=list)
    def event(self, **kwargs):
        ev = AuditEvent(**kwargs); self.events.append(ev); self.timestamps.append(ev.timestamp)
    def to_dict(self): return asdict(self)
