"""
arifOS L5: Engineer Agent
========================
Core-backed implementation that executes a plan and returns a
governed draft via the 5-organ kernel.

Role: Implementation, execution, artifact creation
Stage: 444_EVIDENCE → 555_EMPATHIZE
"""

from .base_agent import BaseAgent

try:
    from core import organs as core_organs
    from core.shared.physics import Peace2

    CORE_AVAILABLE = True
except Exception:
    CORE_AVAILABLE = False


class Engineer(BaseAgent):
    """
    Engineer Agent — Implementation and execution.
    Uses core organs to generate a governed draft solution.
    """

    def __init__(self):
        super().__init__(
            name="Engineer",
            role="Implementation and execution",
            stage="444_EVIDENCE",
        )

    async def process(self, input_data: dict) -> dict:
        query = input_data.get("query", "")
        plan = input_data.get("plan")
        session_id = input_data.get("session_id", "l5-session")

        if not CORE_AVAILABLE:
            # Fallback: return plan summary if core not available
            return {
                "response": {
                    "solution_draft": "Core organs not available. Plan is ready for execution.",
                    "plan": plan,
                    "engine_mode": "fallback",
                }
            }

        # Core pipeline for a governed draft
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
        forge_out = await core_organs.forge(sync_out, agi_tensor, session_id)

        # Update floor scores from core outputs
        self._floor_scores.f1_amanah = 1.0 if align_out.get("is_reversible") else 0.0
        self._floor_scores.f2_truth = agi_tensor.truth_score
        self._floor_scores.f4_clarity = agi_tensor.entropy_delta
        self._floor_scores.f7_humility = agi_tensor.humility.omega_0
        self._floor_scores.f3_tri_witness = sync_out.get("W_3", 0.95)
        self._floor_scores.f5_peace = align_out.get("peace_squared", 1.0)
        self._floor_scores.f6_empathy = align_out.get("kappa_r", 0.7)
        self._floor_scores.f8_genius = forge_out.get("genius_G", 0.8)

        return {
            "response": {
                "solution_draft": forge_out.get("solution_draft"),
                "coherence": forge_out.get("coherence"),
                "genius_G": forge_out.get("genius_G"),
                "plan": plan,
                "engine_mode": "core",
            }
        }


__all__ = ["Engineer"]
