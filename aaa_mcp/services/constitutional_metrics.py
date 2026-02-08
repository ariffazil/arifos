"""Constitutional metrics recording & Stage Result Storage."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, TypedDict, Union


# --- Universal Evidence Schema v2.1 (APEX-Hardened) ---
class EvidenceType(str, Enum):
    VAULT = "vault"
    WEB = "web"
    EMPIRICAL = "empirical"
    AXIOM = "axiom"
    CONFLICT = "conflict"


class ConflictStatus(str, Enum):
    SEAL = "SEAL"
    VOID = "VOID"
    PARTIAL = "PARTIAL"
    SABAR = "SABAR"
    CONFLICT = "CONFLICT"
    INSUFFICIENT = "INSUFFICIENT"
    STALE = "STALE"
    DISPUTED = "DISPUTED"


class EvidenceObject(TypedDict):
    """
    Universal Evidence Object v2 (Chain of Custody).
    Includes cryptographic grounding to prevent 'Hantu' hallucinations.
    """
    evidence_id: str
    content: Dict[str, str]  # {"text": "...", "hash": "sha256:...", "language": "..."}
    source_meta: Dict[str, Any]  # {"uri": "...", "type": "...", "author": "...", "timestamp": "..."}
    metrics: Dict[str, float]  # {"trust_weight": 1.0, "relevance_score": 0.9}
    lifecycle: Dict[str, str]  # {"status": "active", "retrieved_by": "..."}


class PlanObject(TypedDict):
    """Universal Tool Router Plan Object v1."""
    plan_id: str
    recommended_pipeline: List[str]
    justification: str
    grounding_required: bool
    entropy_score: float


# --- Offline Axiom Engine Database (Property-Aware) ---
AXIOM_DATABASE = {
    "co2": {
        "critical_point": {
            "temperature": {"value": 31.1, "unit": "C", "name": "CO2 Critical Temperature"},
            "pressure": {"value": 73.8, "unit": "bar", "name": "CO2 Critical Pressure"},
        },
        "triple_point": {
            "temperature": {"value": -56.6, "unit": "C", "name": "CO2 Triple Point Temperature"},
            "pressure": {"value": 5.18, "unit": "bar", "name": "CO2 Triple Point Pressure"},
        },
        "general": {
            "molar_mass": {"value": 44.01, "unit": "g/mol"},
            "ideal_gas_constant": {"value": 8.314, "unit": "J/mol/K"}
        }
    },
    "physics_constants": {
        "speed_of_light": {"value": 299792458, "unit": "m/s"},
        "planck_constant": {"value": 6.626e-34, "unit": "J*s"}
    },
    "photosynthesis": {
        "value": "6CO2 + 6H2O + light -> C6H12O6 + 6O2",
        "units": "chemical_equation",
        "uncertainty": 0.0,
        "source": "AXIOM_BIOPHYSICS_STD",
        "trust_level": 1.0,
    },
    "AX003_o3_vs_gpt52_benchmark_jan2026": {
        "value": "AAA MCP benchmark Jan 2026: o3 latency 95 ms, GPT-5.2 latency 140 ms; o3 floor violations 0, GPT-5.2 floor violations 3.",
        "units": "governance_benchmark",
        "uncertainty": 0.0,
        "source": "AXIOM_GOV_BENCH_STD",
        "trust_level": 1.0,
    },
    "thermodynamics_2nd_law": {
        "value": "dS >= 0",
        "units": "entropy_inequality",
        "uncertainty": 0.0,
        "source": "AXIOM_PHYSICS_STD",
        "trust_level": 1.0,
    },
}


# In-memory storage for lightweight runtime tracking
_STAGE_RESULTS: Dict[str, Dict[str, Any]] = {}
_VERDICT_LOG: list[dict] = []
_METABOLIC_STATE: Dict[str, Dict[str, Any]] = {}
_EVIDENCE_VAULT: Dict[str, List[EvidenceObject]] = {}
_SESSION_EVENT_LOG: Dict[str, List[Dict[str, Any]]] = {}  # The "Flight Recorder"


def generate_content_hash(text: str) -> str:
    """GEMINI ADDITION: Generate a SHA-256 hash for content integrity."""
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


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
        state["ambiguity_reduction"] = delta_bundle.get("ambiguity_reduction", state.get("ambiguity_reduction", 0.0))
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
    """Store the result of a pipeline stage, track evidence, and record event."""
    if session_id not in _STAGE_RESULTS:
        _STAGE_RESULTS[session_id] = {}
        _SESSION_EVENT_LOG[session_id] = []
        
    _STAGE_RESULTS[session_id][stage] = result
    
    # Flight Recorder Addition: Record the transition
    _SESSION_EVENT_LOG[session_id].append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "stage": stage,
        "verdict": result.get("verdict", "UNKNOWN"),
        "transition": f"Completed {stage}",
        "ambiguity_reduction": result.get("ambiguity_reduction", 0.0)
    })

    # Universal Evidence Tracking (v2 awareness)
    evidence = result.get("evidence", [])
    if evidence:
        if session_id not in _EVIDENCE_VAULT:
            _EVIDENCE_VAULT[session_id] = []
        _EVIDENCE_VAULT[session_id].extend(evidence)

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


def get_session_evidence(session_id: str) -> List[EvidenceObject]:
    """Retrieve all evidence collected in a session."""
    return _EVIDENCE_VAULT.get(session_id, [])


def get_stage_result(session_id: str, stage: str) -> Optional[Dict[str, Any]]:
    """Retrieve a stored stage result."""
    return _STAGE_RESULTS.get(session_id, {}).get(stage)


def get_flight_recorder(session_id: str) -> List[Dict[str, Any]]:
    """Retrieve the event log for a session."""
    return _SESSION_EVENT_LOG.get(session_id, [])
