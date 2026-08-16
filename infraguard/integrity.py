from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class IntegrityCheck:
    artifact_id: str
    artifact_type: str
    expected_hash: str
    observed_hash: str
    verified: bool
    source: str


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def verify_provenance(path: Path) -> list[IntegrityCheck]:
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    checks = []
    for row in rows:
        expected_hash = digest(row["expected_content"])
        observed_hash = digest(row["observed_content"])
        checks.append(
            IntegrityCheck(
                artifact_id=row["artifact_id"],
                artifact_type=row["artifact_type"],
                expected_hash=expected_hash,
                observed_hash=observed_hash,
                verified=expected_hash == observed_hash,
                source=row["source"],
            )
        )
    return checks


def provenance_health(checks: list[IntegrityCheck]) -> float:
    if not checks:
        return 1.0
    return sum(check.verified for check in checks) / len(checks)


def checks_as_dict(checks: list[IntegrityCheck]) -> list[dict]:
    return [asdict(check) for check in checks]
