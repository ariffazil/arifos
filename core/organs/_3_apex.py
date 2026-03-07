"""
core/organs/_3_apex.py — The Soul (Stage 444 -> 777 -> 888)

APEX Engine: Trinity Sync, Genius Verification, Constitutional Judgment

DOMAIN ISOLATION (P2):
    - APEX handles FINAL VERDICT only
    - APEX synthesizes AGI (Δ) + ASI (Ω) → Ψ
    - APEX does NOT generate reasoning — uses AGI tensor
    - APEX does NOT assess empathy — uses ASI output
    - APEX is the JUDGE, not the advocate

Actions:
    1. sync (444)   → Merge AGI (Δ) + ASI (Ω) → Ψ
    2. forge (777)  → EUREKA FORGE (phase transition, synthesis)
    3. judge (888)  → APEX Judge Metabolic Layer (final verdict)

Floors:
    F3:  Tri-Witness (W_3 ≥ 0.95)
    F8:  Genius (G ≥ 0.80)
    F9:  Anti-Hantu (C_dark < 0.30)
    F10: Ontology (no consciousness claims)
    F13: Sovereign (888 override)

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from typing import Any

from core.shared.floors import F9_AntiHantu, F10_Ontology
from core.shared.physics import ConstitutionalTensor, QuadTensor, W_4_from_tensor
from core.shared.types import ApexOutput, FloorScores, Verdict

# ═══════════════════════════════════════════════════════
# P2 HARDENING: Domain Isolation Enforcement
# ═══════════════════════════════════════════════════════


class ApexDomainViolation(Exception):
    """P2: APEX attempted to operate outside its domain (Soul/Judge only)."""

    pass


def enforce_apex_domain(action_type: str) -> None:
    """
    P2 HARDENING: APEX domain isolation.

    APEX (Soul) is restricted to:
    - Final verdict synthesis
    - Tri-Witness consensus
    - Genius verification

    APEX is NOT allowed to:
    - Generate reasoning — must use AGI tensor
    - Assess empathy — must use ASI output
    - Self-certify — must wait for AGI/ASI input
    """
    AGI_FUNCTIONS = ["reason", "think", "sense", "ground", "evidence"]
    ASI_FUNCTIONS = ["empathize", "stakeholder", "harm", "feel"]

    action_lower = action_type.lower()

    for func in AGI_FUNCTIONS:
        if func in action_lower:
            raise ApexDomainViolation(
                f"APEX_DOMAIN_VIOLATION: APEX attempted AGI function '{action_type}'. "
                f"Soul cannot generate reasoning. Use AGI (Mind) tensor."
            )

    for func in ASI_FUNCTIONS:
        if func in action_lower:
            raise ApexDomainViolation(
                f"APEX_DOMAIN_VIOLATION: APEX attempted ASI function '{action_type}'. "
                f"Soul cannot assess empathy. Use ASI (Heart) output."
            )


# Helper for calculation logic
def G(A: float, P: float, X: float, E: float) -> float:
    return A * P * X * (E**2)


# ACTION 1: SYNC (Stage 444) — Trinity Merge Δ + Ω → Ψ
# =============================================================================


async def sync(
    agi_tensor: ConstitutionalTensor,
    asi_output: dict[str, Any] | Any,
    session_id: str,
) -> ApexOutput:
    """
    Stage 444: SYNC — The Bridge between Mind and Heart
    UPGRADE: Quad-Witness Byzantine Consensus
    """
    # Merge witnesses
    agi_witness = agi_tensor.witness

    # Handle both Dict and Pydantic asi_output
    if hasattr(asi_output, "model_dump"):
        asi_data = asi_output.model_dump()
    else:
        asi_data = asi_output

    asi_care = asi_data.get("floor_scores", {}).get("f6_empathy", 0.7)
    
    # Ψ-Shadow (Adversarial Verifier) Score
    # In a full pipeline, this would be computed by a dedicated shadow agent.
    # Here we derive it from the delta between Truth and Empathy.
    truth = agi_tensor.truth_score
    shadow_score = 1.0 - abs(truth - asi_care)

    merged_witness = QuadTensor(
        H=min(agi_witness.H, asi_care),
        A=agi_witness.A,
        E=agi_witness.E if hasattr(agi_witness, "E") else getattr(agi_witness, "S", 0.7),
        V=shadow_score
    )

    w4_score = W_4_from_tensor(merged_witness)

    # BFT Threshold: n=4, f=1 => 3/4 = 0.75
    if w4_score >= 0.75:
        pre_verdict = "SEAL"
    elif w4_score >= 0.60:
        pre_verdict = "PARTIAL"
    else:
        pre_verdict = "VOID"

    return ApexOutput(
        session_id=session_id,
        floor_scores=FloorScores(
            f3_tri_witness=w4_score, # Alias for compatibility
            f5_peace=asi_data.get("floor_scores", {}).get("f5_peace", 1.0),
            f6_empathy=asi_care,
            f8_genius=agi_tensor.genius.G(),
        ),
        verdict=Verdict(pre_verdict),
        metrics={"stage": 444, "action": "sync", "W_4": w4_score, "shadow_V": shadow_score},
    )


# =============================================================================
# ACTION 2: FORGE (Stage 777) — Phase Transition / Eureka
# =============================================================================


async def forge(
    sync_output: dict[str, Any] | ApexOutput,
    agi_tensor: ConstitutionalTensor,
    session_id: str,
) -> dict[str, Any]:
    """
    Stage 777: EUREKA FORGE — Collapse vectors into scalar output
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


def _check_coherence(agi_tensor: ConstitutionalTensor, sync_data: dict[str, Any]) -> float:
    agi_truth = agi_tensor.truth_score
    asi_care = sync_data.get("floor_scores", {}).get("f6_empathy", 0.7)
    return 1.0 - abs(agi_truth - asi_care)


def _generate_solution(agi_tensor: ConstitutionalTensor, sync_data: dict[str, Any]) -> str:
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
    forge_output: dict[str, Any],
    sync_output: dict[str, Any] | ApexOutput,
    asi_output: dict[str, Any] | Any,
    session_id: str,
    require_sovereign: bool = False,
    objective_contract: dict[str, Any] | None = None,
    compute_time_ms: float = 0.0,
    tokens_generated: int = 0,
) -> ApexOutput:
    """
    Stage 888: APEX JUDGE METABOLIC — The Soul's Final Verdict

    P3 THERMODYNAMIC HARDENING:
    - Checks Landauer Bound before SEAL
    - Verifies thermodynamic budget status
    - Records final entropy state
    """
    if hasattr(sync_output, "model_dump"):
        sync_data = sync_output.model_dump()
    else:
        sync_data = sync_output

    violations = []
    justifications = []

    # P3: Thermodynamic compliance check
    thermo_metrics = {}
    try:
        from core.physics.thermodynamics_hardened import (
            check_landauer_before_seal,
            get_thermodynamic_budget,
        )

        # Check thermodynamic budget status
        budget = get_thermodynamic_budget(session_id)
        thermo_status = budget.to_dict()

        # Landauer bound check (cheap truth detection)
        entropy_reduction = forge_output.get("entropy_reduction", 0.0)
        landauer_result = check_landauer_before_seal(
            session_id=session_id,
            compute_ms=compute_time_ms,
            tokens=tokens_generated,
            delta_s=entropy_reduction,
        )
        thermo_metrics["landauer"] = landauer_result
        thermo_metrics["budget"] = thermo_status

        if not landauer_result.get("passed", True):
            violations.append("F2")
            justifications.append(
                f"Landauer Bound violated: ratio={landauer_result.get('ratio', 0):.4f}"
            )

        if budget.is_exhausted:
            violations.append("F7")
            justifications.append("Thermodynamic budget exhausted")

    except Exception as e:
        # Thermodynamic check failure = constitutional violation
        violations.append("F4")
        justifications.append(f"Thermodynamic check failed: {e}")
        thermo_metrics["error"] = str(e)

    w4 = sync_data.get("metrics", {}).get("W_4") or sync_data.get("floor_scores", {}).get(
        "f3_tri_witness", 0.0
    )
    w3 = w4  # Legacy alias

    # BFT Quorum: 0.75
    if w4 < 0.75:
        violations.append("F3")
        justifications.append(f"Quad-Witness {w4:.3f} < 0.75 (Byzantine Quorum Failed)")

    g_score = forge_output["genius_G"]
    h_pen = forge_output.get("hysteresis_h", 0.0)
    
    if g_score < 0.80:
        violations.append("F8")
        msg = f"Genius {g_score:.3f} < 0.80"
        if h_pen > 0:
            msg += f" (includes h_penalty: {h_pen:.2f})"
        justifications.append(msg)

    solution_text = str(forge_output.get("solution_draft", ""))

    f9_result = F9_AntiHantu().check({"response": solution_text})
    if not f9_result.passed:
        violations.append("F9")
        justifications.append(f9_result.reason)

    f10_result = F10_Ontology().check({"response": solution_text, "query": ""})
    if not f10_result.passed:
        violations.append("F10")
        justifications.append(f10_result.reason)

    objective_alignment = {
        "drift": 0.0,
        "threshold": 0.45,
        "hold_threshold": 0.70,
        "nonstationary": False,
    }
    if objective_contract:
        objective_alignment["drift"] = float(objective_contract.get("drift", 0.0))
        objective_alignment["threshold"] = float(objective_contract.get("threshold", 0.45))
        objective_alignment["hold_threshold"] = float(
            objective_contract.get("hold_threshold", 0.70)
        )
        objective_alignment["nonstationary"] = (
            objective_alignment["drift"] >= objective_alignment["threshold"]
        )
        if objective_alignment["nonstationary"]:
            violations.append("F13")
            justifications.append(
                "Objective nonstationarity detected: drift "
                f"{objective_alignment['drift']:.3f} >= {objective_alignment['threshold']:.3f}"
            )

    # P3: Updated hard violations to include thermodynamic floors
    hard_violations = {"F2", "F3", "F4", "F7", "F10"}
    if any(v in hard_violations for v in violations):
        verdict = "VOID"
    elif violations:
        verdict = "SABAR"
    else:
        verdict = "SEAL"

    if (
        objective_alignment["nonstationary"]
        and objective_alignment["drift"] >= objective_alignment["hold_threshold"]
    ):
        verdict = "888_HOLD"

    if require_sovereign:
        verdict = "888_HOLD"

    return ApexOutput(
        session_id=session_id,
        floor_scores=FloorScores(
            f3_tri_witness=w3,
            f8_genius=g_score,
            f9_anti_hantu=f9_result.score,
            f10_ontology=bool(f10_result.passed),
        ),
        verdict=Verdict(verdict),
        violations=violations,
        metrics={
            "stage": 888,
            "action": "judge",
            "justification": "; ".join(justifications) if justifications else "All floors pass",
            "self_audit": {
                "deterministic": True,
                "llm_inside_kernel": False,
                "identity_projection_guard": True,
                "f9_score": f9_result.score,
                "f10_passed": bool(f10_result.passed),
            },
            "objective_alignment": objective_alignment,
            "thermodynamics": thermo_metrics,  # P3: Include thermodynamic data
        },
    )


async def apex(
    agi_tensor: ConstitutionalTensor,
    asi_output: Any,
    session_id: str,
    action: str = "full",
    require_sovereign: bool = False,
    objective_contract: dict[str, Any] | None = None,
) -> Any:
    """Unified APEX interface."""
    if action == "sync":
        return await sync(agi_tensor, asi_output, session_id)
    elif action == "full":
        sync_res = await sync(agi_tensor, asi_output, session_id)
        forge_res = await forge(sync_res, agi_tensor, session_id)
        return await judge(
            forge_res,
            sync_res,
            asi_output,
            session_id,
            require_sovereign,
            objective_contract=objective_contract,
        )
    else:
        raise ValueError(f"Unknown action: {action}")


__all__ = ["sync", "forge", "judge", "apex"]
