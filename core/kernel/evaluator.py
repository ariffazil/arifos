"""
core/kernel/evaluator.py — Constitutional Evaluation Engine

Pure kernel logic for enforcing the 13 Constitutional Floors.
This engine is transport-agnostic and handles the pre/post execution
validation lifecycle.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import logging
import time
from typing import Any, Dict, List, Optional, Tuple, Set

logger = logging.getLogger(__name__)

# ─── Floor Classification ───────────────────────────────────────────────────

# Mandatory floors run on EVERY evaluation (the "immune system").
MANDATORY_PRE_FLOORS: Set[str] = {"F12"}

# Pre-execution floors: validate INPUT before action
PRE_FLOORS: Set[str] = {"F1", "F5", "F6", "F11", "F12", "F13"}

# Post-execution floors: validate OUTPUT after action
POST_FLOORS: Set[str] = {"F2", "F3", "F4", "F7", "F8", "F9", "F10"}

# Hard floors: failure -> VOID (block)
HARD_FLOORS: Set[str] = {"F1", "F2", "F7", "F10", "F11", "F12", "F13"}

# Soft/Derived floors: failure -> PARTIAL (warn)
SOFT_FLOORS: Set[str] = {"F3", "F4", "F5", "F6", "F8", "F9"}


class ConstitutionalEvaluator:
    """
    Orchestrates the validation of constitutional floors.

    Can be used by decorators, API gateways, or internal pipelines.
    """

    def __init__(self):
        self._floor_cache: Dict[str, Any] = {}
        self._floors_available: Optional[bool] = None

    def _load_all_floors(self) -> Optional[Dict[str, Any]]:
        """Lazy-load ALL_FLOORS from core.shared.floors."""
        if self._floors_available is False:
            return None
        try:
            from core.shared.floors import ALL_FLOORS

            self._floors_available = True
            return ALL_FLOORS
        except Exception as e:
            self._floors_available = False
            logger.error(f"Failed to load constitutional_floors: {e}")
            return None

    def _get_floor(self, floor_id: str):
        """Get or create a cached floor validator instance."""
        if floor_id in self._floor_cache:
            return self._floor_cache[floor_id]

        all_floors = self._load_all_floors()
        if all_floors is None:
            return None

        floor_cls = all_floors.get(floor_id)
        if floor_cls is None:
            return None

        try:
            instance = floor_cls()
            self._floor_cache[floor_id] = instance
            return instance
        except Exception as e:
            logger.error(f"Failed to instantiate {floor_id}: {e}")
            return None

    def check_floor(self, floor_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single floor check."""
        floor = self._get_floor(floor_id)
        if floor is None:
            return {
                "floor": floor_id,
                "passed": False,
                "score": 0.0,
                "reason": "Floor unavailable (fail-closed)",
            }

        try:
            result = floor.check(context)
            return {
                "floor": floor_id,
                "passed": result.passed,
                "score": result.score,
                "reason": result.reason,
            }
        except Exception as e:
            logger.error(f"Floor {floor_id} check error: {e}")
            return {
                "floor": floor_id,
                "passed": False,
                "score": 0.0,
                "reason": f"Floor check error (fail-closed): {e}",
            }

    def build_pre_context(
        self, query: str, context_overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Build context dict for pre-execution floor checks."""
        ctx = {
            "query": query,
            "action": query,
            "session_id": "",
            "role": "ANONYMOUS",
            "authority_token": "",
        }
        if context_overrides:
            ctx.update(context_overrides)

        # F11 normalization: ensure role/token logic if session exists
        if ctx.get("session_id") and not ctx.get("authority_token"):
            ctx["role"] = "AGENT"
            ctx["authority_token"] = "arifos_internal"

        return ctx

    def build_post_context(
        self, query: str, result: Any, context_overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Build context dict for post-execution floor checks."""
        # Extract response text from result
        response = ""
        if isinstance(result, dict):
            for key in ("response", "result", "reasoning", "analysis", "output"):
                val = result.get(key, "")
                if val:
                    response = str(val)
                    break
            if not response:
                response = str(result)
        else:
            response = str(result)

        ctx = {
            "query": query,
            "response": response,
            "confidence": 0.96,
            "entropy_input": 0.5,
            "entropy_output": 0.45,
            "human_witness": 0.8,
            "ai_witness": 1.0,
            "earth_witness": 1.0,
        }

        if context_overrides:
            ctx.update(context_overrides)

        # Override defaults with explicit metrics from result
        if isinstance(result, dict):
            for key in (
                "truth_score",
                "confidence",
                "entropy_delta",
                "human_witness",
                "ai_witness",
                "earth_witness",
                "empathy_kappa_r",
                "weakest_stakeholder_impact",
                "entropy_input",
                "entropy_output",
                "humility_omega",
                "f2_threshold",
            ):
                if key in result:
                    ctx[key] = result[key]

            if "entropy_delta" in result and "entropy_input" in ctx:
                ctx["entropy_output"] = ctx["entropy_input"] + result["entropy_delta"]

        return ctx

    def accumulate_floor_scores(self, floor_details: List[Dict[str, Any]]) -> Dict[str, float]:
        """Normalize accumulated scores for Genius engine."""
        scores: Dict[str, float] = {}
        for d in floor_details:
            fid = d["floor"]
            score = d.get("score", 0.0)
            if fid == "F7":
                scores[fid] = 1.0 - score  # omega_0 -> confidence
            elif fid == "F9":
                scores[fid] = 1.0 - score  # c_dark -> anti-hantu safety
            elif fid == "F12":
                scores[fid] = 1.0 - score  # injection prob -> defense
            else:
                scores[fid] = score
        return scores

    def evaluate_verdict(self, floor_details: List[Dict[str, Any]]) -> str:
        """Compute aggregate verdict (VOID | PARTIAL | SEAL)."""
        hard_fails = [d for d in floor_details if not d["passed"] and d["floor"] in HARD_FLOORS]
        soft_fails = [d for d in floor_details if not d["passed"] and d["floor"] in SOFT_FLOORS]

        if hard_fails:
            return "VOID"
        elif soft_fails:
            return "PARTIAL"
        return "SEAL"


# Singleton instance
evaluator = ConstitutionalEvaluator()
