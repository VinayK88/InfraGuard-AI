# Threat model

InfraGuard AI models **defensive assurance failures** around AI-enabled critical-infrastructure-style operations. It is intentionally simulation-only.

## Protected properties

- Operational safety constraints remain authoritative over model confidence.
- AI/model/data artifacts are traceable and integrity-checked before consequential use.
- Automation degrades safely when telemetry quality falls below a defined threshold.
- High-impact actions remain least-privileged and reviewable.
- Operators retain a tested manual-control path.
- Detection, containment, and recovery are measurable rather than assumed.

## Synthetic threat scenarios

| Threat | Security property at risk | Defensive response |
|---|---|---|
| Sensor spoofing | Telemetry integrity | Cross-check confidence, enter degraded-safe state, require operator review |
| Poisoned retraining data | AI supply-chain integrity | Provenance mismatch, block deployment, restore known-good artifact |
| Excessive agent privilege | Authorization | Reject capability, preserve manual-control boundary |
| Telemetry loss | Availability | Hold last safe setpoint and transition to human control |
| Model artifact tampering | Model integrity | Hash mismatch, deployment approval/rollback |
| Unsafe high-confidence recommendation | Operational safety | Hard safety-envelope block regardless of model confidence |

## Out of scope

No scanning, exploitation, credential use, PLC protocol implementation, live SCADA access, weapon-system logic, or autonomous physical actuation is included.
