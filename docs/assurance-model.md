# Assurance model

InfraGuard evaluates an AI-assisted action through independent control layers instead of treating model confidence as authorization.

1. **Asset context** — identify the target, zone, criticality, and allowed capabilities.
2. **Operational safety envelope** — reject setpoints outside known-safe bounds.
3. **Telemetry confidence** — enter a degraded-safe mode when observability is insufficient.
4. **Provenance integrity** — require review when model/data artifacts cannot be verified.
5. **Untrusted-context signal** — increase scrutiny when an action is influenced by untrusted input.
6. **Human override** — preserve manual control for consequential or ambiguous situations.
7. **Resilience evidence** — measure detection, containment, recovery, and safe-state transitions.

The Mission Resilience Score is a transparent portfolio metric composed from these dimensions. It is not an official government or sector benchmark.
