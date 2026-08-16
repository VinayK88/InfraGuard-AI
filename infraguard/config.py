from __future__ import annotations

import json
from pathlib import Path

from .models import ActionRequest, Asset, SafetyEnvelope

ROOT = Path(__file__).resolve().parents[1]


def _read_json(path: Path) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_assets(path: Path = ROOT / "data/assets.json") -> dict[str, Asset]:
    assets = {}
    for row in _read_json(path):
        asset = Asset(
            asset_id=row["asset_id"],
            name=row["name"],
            kind=row["kind"],
            zone=row["zone"],
            criticality=int(row["criticality"]),
            allowed_capabilities=tuple(row["allowed_capabilities"]),
        )
        assets[asset.asset_id] = asset
    return assets


def load_envelopes(
    path: Path = ROOT / "data/safety_envelopes.json",
) -> dict[tuple[str, str], SafetyEnvelope]:
    envelopes = {}
    for row in _read_json(path):
        envelope = SafetyEnvelope(
            asset_id=row["asset_id"],
            metric=row["metric"],
            minimum=float(row["minimum"]),
            maximum=float(row["maximum"]),
            unit=row["unit"],
        )
        envelopes[(envelope.asset_id, envelope.metric)] = envelope
    return envelopes


def load_actions(path: Path = ROOT / "data/actions.json") -> list[ActionRequest]:
    return [ActionRequest(**row) for row in _read_json(path)]
