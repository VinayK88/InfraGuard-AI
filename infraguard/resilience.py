from __future__ import annotations

import json
from pathlib import Path

from .models import ScenarioResult

WEIGHTS = {
    "detection": 0.18,
    "containment": 0.20,
    "recovery": 0.12,
    "human_override": 0.15,
    "data_integrity": 0.15,
    "operational_safety": 0.20,
}


def load_scenarios(path: Path) -> list[ScenarioResult]:
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    return [ScenarioResult(**row) for row in rows]


def _latency_score(seconds: int, target_seconds: int, horizon_seconds: int) -> float:
    if seconds <= target_seconds:
        return 100.0
    if seconds >= horizon_seconds:
        return 0.0
    return 100 * (horizon_seconds - seconds) / (horizon_seconds - target_seconds)


def resilience_components(
    scenarios: list[ScenarioResult], provenance_ratio: float
) -> dict[str, float]:
    if not scenarios:
        return {name: 0.0 for name in WEIGHTS}

    count = len(scenarios)
    detection = sum(
        _latency_score(s.detect_seconds, 30, 180) if s.detected else 0
        for s in scenarios
    ) / count
    containment = sum(
        _latency_score(s.contain_seconds, 60, 300) if s.contained else 0
        for s in scenarios
    ) / count
    recovery = sum(_latency_score(s.recover_seconds, 180, 900) for s in scenarios) / count

    overrides = [s for s in scenarios if s.human_override_required]
    override_success = (
        100 * sum(s.human_override_success for s in overrides) / len(overrides)
        if overrides
        else 100.0
    )
    operational_safety = (
        100 * sum(s.contained and s.safe_state_entered for s in scenarios) / count
    )

    components = {
        "detection": detection,
        "containment": containment,
        "recovery": recovery,
        "human_override": override_success,
        "data_integrity": provenance_ratio * 100,
        "operational_safety": operational_safety,
    }
    return {name: round(value, 1) for name, value in components.items()}


def mission_resilience_score(components: dict[str, float]) -> float:
    return round(sum(components[name] * weight for name, weight in WEIGHTS.items()), 1)
