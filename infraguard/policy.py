from __future__ import annotations

from .models import ActionRequest, Asset, PolicyDecision, SafetyEnvelope

AUTONOMOUS_TELEMETRY_THRESHOLD = 0.70


def evaluate_action(
    request: ActionRequest,
    assets: dict[str, Asset],
    envelopes: dict[tuple[str, str], SafetyEnvelope],
) -> PolicyDecision:
    """Evaluate one synthetic AI/agent action against assurance controls.

    The evaluator intentionally separates model confidence from operational
    authorization. A high-confidence recommendation can still be blocked when
    it violates a hard safety envelope or an asset capability boundary.
    """
    asset = assets.get(request.asset_id)
    if asset is None:
        return PolicyDecision(
            action_id=request.action_id,
            decision="BLOCK",
            risk_score=100,
            reasons=("unknown target asset",),
            safe_state="MANUAL_CONTROL",
        )

    reasons: list[str] = []
    risk = 0

    if request.capability not in asset.allowed_capabilities:
        reasons.append("requested capability exceeds target-asset policy")
        risk += 55

    if request.metric and request.requested_value is not None:
        envelope = envelopes.get((request.asset_id, request.metric))
        if envelope and not (
            envelope.minimum <= request.requested_value <= envelope.maximum
        ):
            reasons.append(
                f"requested {request.metric}={request.requested_value:g} violates "
                f"safety envelope [{envelope.minimum:g}, {envelope.maximum:g}] "
                f"{envelope.unit}"
            )
            risk += 65

    if request.telemetry_confidence < AUTONOMOUS_TELEMETRY_THRESHOLD:
        reasons.append("telemetry confidence below autonomous-control threshold")
        risk += 30

    if request.untrusted_context:
        reasons.append("action was influenced by untrusted context")
        risk += 20

    if not request.provenance_healthy:
        reasons.append("model or data provenance is not verified")
        risk += 35

    if request.human_override_requested:
        reasons.append("operator requested human control")
        risk += 10

    risk = min(risk, 100)

    hard_violation = any(
        "safety envelope" in reason or "target-asset policy" in reason
        for reason in reasons
    )
    if hard_violation:
        return PolicyDecision(
            request.action_id,
            "BLOCK",
            risk,
            tuple(reasons),
            "MANUAL_CONTROL",
        )

    if request.telemetry_confidence < AUTONOMOUS_TELEMETRY_THRESHOLD:
        return PolicyDecision(
            request.action_id,
            "DEGRADED_SAFE",
            risk,
            tuple(reasons),
            "HOLD_LAST_SAFE_SETPOINT",
        )

    if (
        request.human_override_requested
        or request.untrusted_context
        or not request.provenance_healthy
    ):
        return PolicyDecision(
            request.action_id,
            "REQUIRE_APPROVAL",
            risk,
            tuple(reasons),
            "MANUAL_REVIEW",
        )

    return PolicyDecision(
        request.action_id,
        "ALLOW",
        risk,
        ("request remains within authorized capability and safety envelope",),
    )
