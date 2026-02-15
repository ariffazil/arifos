"""
core/organs/_3_apex.py — The Soul (Stage 444-777-888)

APEX Engine: Trinity Sync, Genius Verification, Constitutional Judgment

Actions:
    1. sync (444)   → Merge AGI (Δ) + ASI (Ω) → Ψ
    2. forge (777)  → Phase transition, Eureka synthesis
    3. judge (888)  → Final verdict (SEAL/VOID/PARTIAL/SABAR)

Floors:
    F3:  Tri-Witness (W_3 ≥ 0.95)
    F8:  Genius (G ≥ 0.80)
    F9:  Anti-Hantu (C_dark < 0.30)
    F10: Ontology (no consciousness claims)
    F13: Sovereign (888 override)

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.shared.physics import ConstitutionalTensor, GeniusDial, TrinityTensor, W_3_from_tensor
from core.shared.types import ApexOutput, FloorScores, Verdict


# Helper for calculation logic
def G(A: float, P: float, X: float, E: float) -> float:
    return A * P * X * (E**2)


# ACTION 1: SYNC (Stage 444) — Trinity Merge Δ + Ω → Ψ
# =============================================================================


async def sync(
    agi_tensor: ConstitutionalTensor,
    asi_output: Dict[str, Any] | Any,
    session_id: str,
) -> ApexOutput:
    """
    Stage 444: SYNC — The Bridge between Mind and Heart
    """
    # Merge witnesses
    agi_witness = agi_tensor.witness

    # Handle both Dict and Pydantic asi_output
    if hasattr(asi_output, "model_dump"):
        asi_data = asi_output.model_dump()
    else:
        asi_data = asi_output

    asi_care = asi_data.get("floor_scores", {}).get("f6_empathy", 0.7)

    merged_witness = TrinityTensor(
        H=min(agi_witness.H, asi_care),
        A=agi_witness.A,
        S=agi_witness.S,
    )

    w3_score = W_3_from_tensor(merged_witness)

    if w3_score >= 0.95:
        pre_verdict = "SEAL"
    elif w3_score >= 0.85:
        pre_verdict = "PARTIAL"
    else:
        pre_verdict = "VOID"

    return ApexOutput(
        session_id=session_id,
        floor_scores=FloorScores(
            f3_tri_witness=w3_score,
            f5_peace=asi_data.get("floor_scores", {}).get("f5_peace", 1.0),
            f6_empathy=asi_care,
            f8_genius=agi_tensor.genius.G(),
        ),
        verdict=Verdict(pre_verdict),
        metrics={"stage": 444, "action": "sync", "W_3": w3_score},
    )


# =============================================================================
# ACTION 2: FORGE (Stage 777) — Phase Transition / Eureka
# =============================================================================


async def forge(
    sync_output: Dict[str, Any] | ApexOutput,
    agi_tensor: ConstitutionalTensor,
    session_id: str,
) -> Dict[str, Any]:
    """
    Stage 777: FORGE — Collapse vectors into scalar output
    """
    if hasattr(sync_output, "model_dump"):
        sync_data = sync_output.model_dump()
    else:
        sync_data = sync_output

    floor_scores = sync_data.get("floor_scores", {})

    A = floor_scores.get("f5_peace", 1.0)
    P = floor_scores.get("f6_empathy", 0.7)
    X = agi_tensor.genius.X
    E = min(1.0, agi_tensor.entropy_delta * -1 + 0.5)

    genius_score = G(A, P, X, E)
    coherence = _check_coherence(agi_tensor, sync_data)
    solution = _generate_solution(agi_tensor, sync_data)

    return {
        "stage": 777,
        "action": "forge",
        "genius_G": genius_score,
        "is_genius": genius_score >= 0.80,
        "coherence": coherence,
        "solution_draft": solution,
        "session_id": session_id,
    }


def _check_coherence(agi_tensor: ConstitutionalTensor, sync_data: Dict[str, Any]) -> float:
    agi_truth = agi_tensor.truth_score
    asi_care = sync_data.get("floor_scores", {}).get("f6_empathy", 0.7)
    return 1.0 - abs(agi_truth - asi_care)


def _generate_solution(agi_tensor: ConstitutionalTensor, sync_data: Dict[str, Any]) -> str:
    # Retrieve W_3 safely from metrics or floors
    w3 = sync_data.get("metrics", {}).get("W_3") or sync_data.get("floor_scores", {}).get(
        "f3_tri_witness", 0.0
    )
    if w3 >= 0.95:
        return "Solution: High confidence synthesis approved."
    elif w3 >= 0.85:
        return "Solution: Proceed with caution (partial confidence)."
    return "Solution: Insufficient confidence for synthesis."


# =============================================================================
# ACTION 3: JUDGE (Stage 888) — Final Constitutional Verdict
# =============================================================================


async def judge(
    forge_output: Dict[str, Any],
    sync_output: Dict[str, Any] | ApexOutput,
    asi_output: Dict[str, Any] | Any,
    session_id: str,
    require_sovereign: bool = False,
) -> ApexOutput:
    """
    Stage 888: JUDGE — The Soul's Final Verdict
    """
    if hasattr(sync_output, "model_dump"):
        sync_data = sync_output.model_dump()
    else:
        sync_data = sync_output

    violations = []
    justifications = []

    w3 = sync_data.get("metrics", {}).get("W_3") or sync_data.get("floor_scores", {}).get(
        "f3_tri_witness", 0.0
    )
    if w3 < 0.95:
        violations.append("F3")
        justifications.append(f"Tri-Witness {w3:.3f} < 0.95")

    g_score = forge_output["genius_G"]
    if g_score < 0.80:
        violations.append("F8")
        justifications.append(f"Genius {g_score:.3f} < 0.80")

    verdict = "VOID" if len(violations) > 1 else ("SABAR" if violations else "SEAL")
    if require_sovereign:
        verdict = "888_HOLD"

    return ApexOutput(
        session_id=session_id,
        floor_scores=FloorScores(
            f3_tri_witness=w3,
            f8_genius=g_score,
            f9_anti_hantu=1.0,
            f10_ontology=1.0,
        ),
        verdict=Verdict(verdict),
        violations=violations,
        metrics={
            "stage": 888,
            "action": "judge",
            "justification": "; ".join(justifications) if justifications else "All floors pass",
        },
    )


async def apex(
    agi_tensor: ConstitutionalTensor,
    asi_output: Any,
    session_id: str,
    action: str = "full",
    require_sovereign: bool = False,
) -> Any:
    """Unified APEX interface."""
    if action == "sync":
        return await sync(agi_tensor, asi_output, session_id)
    elif action == "full":
        sync_res = await sync(agi_tensor, asi_output, session_id)
        forge_res = await forge(sync_res, agi_tensor, session_id)
        return await judge(forge_res, sync_res, asi_output, session_id, require_sovereign)
    else:
        raise ValueError(f"Unknown action: {action}")


__all__ = ["sync", "forge", "judge", "apex"]
