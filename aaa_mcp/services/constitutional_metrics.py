"""Constitutional metrics recording & Stage Result Storage."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

# In-memory storage for lightweight runtime tracking
_STAGE_RESULTS: Dict[str, Dict[str, Any]] = {}
_VERDICT_LOG: list[dict] = []
_METABOLIC_STATE: Dict[str, Dict[str, Any]] = {}


def record_verdict(tool: str, verdict: str, duration: float, mode: str):
    """Record verdict metrics."""
    _VERDICT_LOG.append(
        {
            "tool": tool,
            "verdict": verdict,
            "duration_ms": duration,
            "mode": mode,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )


def update_metabolic_state(
    session_id: str,
    *,
    delta_bundle: Optional[Dict[str, Any]] = None,
    omega_bundle: Optional[Dict[str, Any]] = None,
    verdict: Optional[str] = None,
) -> Dict[str, Any]:
    """Update lightweight metabolizer state from bundles."""
    state = _METABOLIC_STATE.get(session_id, {})
    if delta_bundle:
        confidence = delta_bundle.get("confidence") or {}
        state["omega_0"] = confidence.get("omega_0", state.get("omega_0", 0.04))
        state["entropy_delta"] = delta_bundle.get("entropy_delta", state.get("entropy_delta", 0.0))
        state["tri_witness"] = delta_bundle.get("floor_scores", {}).get(
            "F8", state.get("tri_witness", 0.95)
        )
    if omega_bundle:
        state["peace_squared"] = omega_bundle.get("floor_scores", {}).get(
            "F5", state.get("peace_squared", 1.0)
        )
        state["kappa_r"] = omega_bundle.get("empathy_kappa_r", state.get("kappa_r", 1.0))
    if verdict:
        state["verdict"] = verdict
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    _METABOLIC_STATE[session_id] = state
    return state


def store_stage_result(session_id: str, stage: str, result: Dict[str, Any]):
    """Store the result of a pipeline stage."""
    if session_id not in _STAGE_RESULTS:
        _STAGE_RESULTS[session_id] = {}
    _STAGE_RESULTS[session_id][stage] = result

    # Opportunistically update metabolic state when bundles are present.
    delta_bundle = result.get("delta_bundle") if isinstance(result, dict) else None
    omega_bundle = result.get("omega_bundle") if isinstance(result, dict) else None
    verdict = result.get("verdict") if isinstance(result, dict) else None
    update_metabolic_state(
        session_id,
        delta_bundle=delta_bundle if isinstance(delta_bundle, dict) else None,
        omega_bundle=omega_bundle if isinstance(omega_bundle, dict) else None,
        verdict=verdict,
    )


def get_stage_result(session_id: str, stage: str) -> Optional[Dict[str, Any]]:
    """Retrieve a stored stage result."""
    return _STAGE_RESULTS.get(session_id, {}).get(stage)
