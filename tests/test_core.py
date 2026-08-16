import unittest

from infraguard.api import healthz, home
from infraguard.config import ROOT, load_actions, load_assets, load_envelopes
from infraguard.integrity import provenance_health, verify_provenance
from infraguard.policy import evaluate_action
from infraguard.report import build_report


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.assets = load_assets()
        self.envelopes = load_envelopes()
        self.actions = load_actions()

    def test_safety_envelope_blocks_unsafe_setpoint(self):
        decision = evaluate_action(self.actions[0], self.assets, self.envelopes)
        self.assertEqual(decision.decision, "BLOCK")
        self.assertEqual(decision.safe_state, "MANUAL_CONTROL")

    def test_low_confidence_enters_degraded_safe_mode(self):
        decision = evaluate_action(self.actions[3], self.assets, self.envelopes)
        self.assertEqual(decision.decision, "DEGRADED_SAFE")
        self.assertEqual(decision.safe_state, "HOLD_LAST_SAFE_SETPOINT")

    def test_clean_recommendation_is_allowed(self):
        decision = evaluate_action(self.actions[2], self.assets, self.envelopes)
        self.assertEqual(decision.decision, "ALLOW")


class IntegrityTests(unittest.TestCase):
    def test_tampered_model_is_detected(self):
        checks = verify_provenance(ROOT / "data/provenance.json")
        failed = [check.artifact_id for check in checks if not check.verified]
        self.assertEqual(failed, ["grid-load-model-v14"])
        self.assertEqual(provenance_health(checks), 0.75)


class ReportAndDashboardTests(unittest.TestCase):
    def test_baseline_report_contains_all_scenarios(self):
        report = build_report()
        self.assertEqual(report["summary"]["contained"], 6)
        self.assertGreater(report["mission_resilience_score"], 70)
        self.assertGreaterEqual(report["summary"]["unsafe_actions_blocked"], 2)

    def test_dashboard_and_health_endpoint(self):
        self.assertIn("Mission resilience score", home())
        self.assertEqual(healthz()["status"], "ok")


if __name__ == "__main__":
    unittest.main()
