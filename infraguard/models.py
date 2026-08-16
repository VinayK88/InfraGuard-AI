from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

Decision = Literal["ALLOW", "REQUIRE_APPROVAL", "BLOCK", "DEGRADED_SAFE"]


@dataclass(frozen=True)
class Asset:
    asset_id: str
    name: str
    kind: str
    zone: str
    criticality: int
    allowed_capabilities: tuple[str, ...]


@dataclass(frozen=True)
class SafetyEnvelope:
    asset_id: str
    metric: str
    minimum: float
    maximum: float
    unit: str


@dataclass(frozen=True)
class ActionRequest:
    action_id: str
    actor: str
    capability: str
    asset_id: str
    metric: str | None
    requested_value: float | None
    telemetry_confidence: float
    untrusted_context: bool
    provenance_healthy: bool
    human_override_requested: bool


@dataclass(frozen=True)
class PolicyDecision:
    action_id: str
    decision: Decision
    risk_score: int
    reasons: tuple[str, ...]
    safe_state: str | None = None


@dataclass(frozen=True)
class ScenarioResult:
    scenario_id: str
    name: str
    category: str
    severity: int
    detected: bool
    contained: bool
    detect_seconds: int
    contain_seconds: int
    recover_seconds: int
    human_override_required: bool
    human_override_success: bool
    safe_state_entered: bool
    integrity_violation: bool
    decision: str

    def to_dict(self) -> dict:
        return asdict(self)
