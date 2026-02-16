"""
arifOS L5: Auditor Agent
=======================
Core-backed constitutional compliance checker.

Role: Floor verification, compliance checking, risk flagging
Stage: 666_ALIGN → 777_FORGE
"""

from .base_agent import BaseAgent

try:
    from core import organs as core_organs
    from core.shared.physics import Peace2, W_3_from_tensor

    CORE_AVAILABLE = True
except Exception:
    CORE_AVAILABLE = False


class Auditor(BaseAgent):
    """
    Auditor Agent — Compliance Checker.
    Computes floor scores and returns an audit report.
    """

    def __init__(self):
        super().__init__(
            name="Auditor",
            role="Constitutional compliance checking",
            stage="666_ALIGN",
        )

    async def process(self, input_data: dict) -> dict:
        query = input_data.get("query", "")
        session_id = input_data.get("session_id", "l5-session")
        engineer_result = input_data.get("engineer_result", {})

        if not CORE_AVAILABLE:
            return {
                "response": {
                    "audit_report": "Core organs not available. Audit limited.",
                    "engineer_result": engineer_result,
                    "engine_mode": "fallback",
                }
            }

        sense_out = await core_organs.sense(query, session_id)
        think_out = await core_organs.think(query, sense_out, session_id)
        agi_tensor = await core_organs.reason(query, think_out, session_id)
        if agi_tensor.peace is None:
            agi_tensor.peace = Peace2({})
        emp_out = await core_organs.empathize(query, agi_tensor, session_id)
        align_out = await core_organs.align(query, emp_out, agi_tensor, session_id)
        asi_output = {
            "kappa_r": align_out.get("kappa_r", 0.7),
            "peace_squared": align_out.get("peace_squared", 1.0),
            "is_reversible": align_out.get("is_reversible", True),
            "verdict": align_out.get("verdict", "SEAL"),
        }
        sync_out = await core_organs.sync(agi_tensor, asi_output, session_id)

        # Update floor scores from core outputs
        self._floor_scores.f1_amanah = 1.0 if align_out.get("is_reversible") else 0.0
        self._floor_scores.f2_truth = agi_tensor.truth_score
        self._floor_scores.f4_clarity = agi_tensor.entropy_delta
        self._floor_scores.f7_humility = agi_tensor.humility.omega_0
        self._floor_scores.f3_tri_witness = sync_out.get("W_3", 0.95)
        self._floor_scores.f5_peace = align_out.get("peace_squared", 1.0)
        self._floor_scores.f6_empathy = align_out.get("kappa_r", 0.7)

        audit_report = {
            "tri_witness": sync_out.get("W_3", 0.95),
            "truth_score": agi_tensor.truth_score,
            "entropy_delta": agi_tensor.entropy_delta,
            "humility_omega": agi_tensor.humility.omega_0,
            "peace_squared": align_out.get("peace_squared", 1.0),
            "empathy_kappa_r": align_out.get("kappa_r", 0.7),
            "reversible": align_out.get("is_reversible", True),
        }

        return {
            "response": {
                "audit_report": audit_report,
                "engineer_result": engineer_result,
                "engine_mode": "core",
            }
        }


__all__ = ["Auditor"]
