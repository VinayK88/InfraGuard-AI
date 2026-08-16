from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from .config import ROOT, load_actions, load_assets, load_envelopes
from .integrity import checks_as_dict, provenance_health, verify_provenance
from .policy import evaluate_action
from .resilience import load_scenarios, mission_resilience_score, resilience_components


def build_report(root: Path = ROOT) -> dict:
    assets = load_assets(root / "data/assets.json")
    envelopes = load_envelopes(root / "data/safety_envelopes.json")
    actions = load_actions(root / "data/actions.json")
    decisions = [evaluate_action(action, assets, envelopes) for action in actions]

    checks = verify_provenance(root / "data/provenance.json")
    provenance_ratio = provenance_health(checks)
    scenarios = load_scenarios(root / "data/scenarios.json")
    components = resilience_components(scenarios, provenance_ratio)

    summary = {
        "scenarios": len(scenarios),
        "contained": sum(s.contained for s in scenarios),
        "unsafe_actions_blocked": sum(d.decision == "BLOCK" for d in decisions),
        "approval_required": sum(
            d.decision == "REQUIRE_APPROVAL" for d in decisions
        ),
        "degraded_safe": sum(d.decision == "DEGRADED_SAFE" for d in decisions),
        "human_override_required": sum(
            s.human_override_required for s in scenarios
        ),
        "human_override_success": sum(
            s.human_override_success for s in scenarios if s.human_override_required
        ),
    }

    return {
        "mission_resilience_score": mission_resilience_score(components),
        "components": components,
        "provenance_health": round(provenance_ratio, 3),
        "assets": [asdict(asset) for asset in assets.values()],
        "provenance": checks_as_dict(checks),
        "decisions": [asdict(decision) for decision in decisions],
        "scenarios": [scenario.to_dict() for scenario in scenarios],
        "summary": summary,
    }
