"""
arifOS L5: Validator Agent
=========================
Final consensus using core organs, with optional vault seal.
"""

from .base_agent import BaseAgent

try:
    from core import organs as core_organs
    from core.shared.physics import Peace2

    CORE_AVAILABLE = True
except Exception:
    CORE_AVAILABLE = False


class Validator(BaseAgent):
    """
    Validator Agent — Final Consensus.
    Computes Tri-Witness consensus and issues final verdict.
    """

    def __init__(self):
        super().__init__(
            name="Validator",
            role="Tri-Witness consensus and final verdict",
            stage="888_JUDGE",
        )

    async def process(self, input_data: dict) -> dict:
        query = input_data.get("query", "")
        session_id = input_data.get("session_id", "l5-session")
        audit_report = input_data.get("audit_report", {})
        tri_witness_threshold = input_data.get("tri_witness_threshold", 0.95)

        if not CORE_AVAILABLE:
            return {
                "response": {
                    "verdict": "HOLD_888",
                    "reason": "Core organs not available. Validation limited.",
                    "audit_report": audit_report,
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
        apex_out = await core_organs.apex(agi_tensor, asi_output, session_id, action="full")
        judge_out = apex_out.get("judge", {})

        # Update floor scores for final verdict
        self._floor_scores.f1_amanah = 1.0 if align_out.get("is_reversible") else 0.0
        self._floor_scores.f2_truth = agi_tensor.truth_score
        self._floor_scores.f4_clarity = agi_tensor.entropy_delta
        self._floor_scores.f7_humility = agi_tensor.humility.omega_0
        self._floor_scores.f3_tri_witness = judge_out.get("W_3", 0.95)
        self._floor_scores.f5_peace = align_out.get("peace_squared", 1.0)
        self._floor_scores.f6_empathy = align_out.get("kappa_r", 0.7)
        self._floor_scores.f8_genius = judge_out.get("genius_G", 0.8)

        verdict = judge_out.get("verdict", "SEAL")
        if self._floor_scores.f3_tri_witness < tri_witness_threshold:
            verdict = "PARTIAL"

        return {
            "response": {
                "verdict": verdict,
                "judge": judge_out,
                "audit_report": audit_report,
                "engine_mode": "core",
            }
        }


__all__ = ["Validator"]
