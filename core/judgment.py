"""
core/judgment.py — Kernel Judgment Interface (v64.2-HARDENED)

All decision logic lives here. Wrapper calls these functions.
No uncertainty computation, governance modification, or verdict logic in wrapper.

P0/P1 HARDENING:
- Ψ (Vitality Index) Master Equation
- W₄ (Quad-Witness) geometric mean consensus (BFT)
- Φₚ (Paradox Conductance) resolution check

This is the canonical interface between kernel and wrapper.
"""

import hashlib
from dataclasses import dataclass, field
from typing import Any

from core.governance_kernel import get_governance_kernel
from core.shared.types import EvidenceRecord
from core.uncertainty_engine import UncertaintyEngine, calculate_uncertainty


@dataclass
class CognitionResult:
    """Result of AGI cognition judgment."""

    verdict: str  # SEAL, VOID, SABAR, PARTIAL
    truth_score: float
    clarity_delta: float
    humility_omega: float  # display omega (geometric)
    safety_omega: float  # safety omega (harmonic) - for kernel use only
    genius_score: float
    grounded: bool
    reasoning: dict[str, Any]
    evidence_sources: list[dict]
    floor_scores: dict[str, float]
    module_results: dict[str, Any]
    evidence_records: list[EvidenceRecord] = field(default_factory=list)
    error: str | None = None


@dataclass
class EmpathyResult:
    """Result of ASI empathy judgment."""

    verdict: str
    stakeholder_impact: dict[str, Any]
    reversibility_score: float
    peace_squared: float
    empathy_score: float
    floor_scores: dict[str, float]
    error: str | None = None


@dataclass
class VerdictResult:
    """Result of APEX final judgment."""

    verdict: str
    confidence: float
    reasoning: str
    requires_human_approval: bool
    floor_scores: dict[str, float]
    # P0/P1 HARDENING: Thermodynamic metrics
    vitality_index: float | None = None  # Ψ
    tri_witness: float | None = None  # W₃ (Legacy Alias)
    paradox_conductance: float | None = None  # Φₚ


# ═══════════════════════════════════════════════════════
# P0/P1 HARDENING: Thermodynamic Equations
# ═══════════════════════════════════════════════════════


def _calculate_vitality_index(
    delta_s: float,
    peace2: float,
    kappa_r: float,
    rasa: float,
    amanah: float,
    entropy: float,
    shadow: float,
) -> float:
    """
    P0: Ψ (Vitality Index) Master Equation

    Ψ = (|ΔS| · Peace² · κᵣ · RASA · Amanah) / (Entropy + Shadow + ε)

    Threshold: Ψ >= 1.0 required for homeostatic equilibrium (SEAL)

    Returns:
        Vitality index score
    """
    epsilon = 1e-6
    numerator = abs(delta_s) * peace2 * kappa_r * rasa * amanah
    denominator = entropy + shadow + epsilon
    psi = numerator / denominator
    return min(10.0, max(0.0, psi))  # Clamp to [0, 10]


def _calculate_tri_witness(
    human_score: float,
    ai_score: float,
    earth_score: float,
) -> float:
    """
    P1: W₃ (Tri-Witness Consensus) - Geometric Mean
    DEPRECATED: Use W₄ logic.
    """
    return (human_score * ai_score * earth_score) ** (1 / 3)


def _calculate_paradox_conductance(
    delta_p: float,
    omega_p: float,
    psi_p: float,
    kappa_r: float,
    amanah: float,
    failure_drag: float,
) -> float:
    """
    P1: Φₚ (Paradox Conductance)

    Φₚ = (Δₚ · Ωₚ · Ψₚ · κᵣ · Amanah) / (Lₚ + Rₘₐ + Λ + ε)
    """
    clarity_term = max(0.0, min(1.0, -delta_p + 0.2))
    phi_p = (clarity_term + psi_p + (1.0 - omega_p)) / (1.0 + failure_drag)
    return min(2.0, max(0.0, phi_p))


class JudgmentKernel:
    """
    Canonical judgment interface for arifOS kernel.
    """

    def __init__(self):
        self._uncertainty_engine = UncertaintyEngine()

    def judge_cognition(
        self,
        query: str,
        evidence_count: int,
        evidence_relevance: float,
        reasoning_consistency: float,
        knowledge_gaps: list[str],
        model_logits_confidence: float,
        grounding: list[dict] | None = None,
        module_results: dict[str, Any] | None = None,
        compute_ms: float = 0.0,
        expected_ms: float = 1.0,
    ) -> CognitionResult:
        # Calculate 5-dimensional uncertainty vector
        uncertainty_calc = calculate_uncertainty(
            evidence_count=evidence_count,
            evidence_relevance=evidence_relevance,
            reasoning_consistency=reasoning_consistency,
            knowledge_gaps=knowledge_gaps,
            model_logits_confidence=model_logits_confidence,
        )

        safety_omega = uncertainty_calc["safety_omega"]
        display_omega = uncertainty_calc["display_omega"]

        if grounding and len(grounding) > 0:
            truth_score = min(0.99, 0.7 + (len(grounding) * 0.05) - (safety_omega * 0.2))
        else:
            truth_score = max(0.3, 0.85 - (safety_omega * 0.3))

        clarity_delta = -0.1
        genius_score = 0.88
        grounded = bool(grounding and len(grounding) > 0)

        records: list[EvidenceRecord] = []
        if grounding:
            for g in grounding:
                records.append(
                    EvidenceRecord(
                        claim=g.get("claim", query),
                        evidence_hash=hashlib.sha256(
                            str(g.get("content", "")).encode()
                        ).hexdigest(),
                        source_uri=g.get("source", "unknown"),
                        confidence=g.get("relevance", 0.9),
                        witness_type="AI",
                    )
                )

        efficiency = expected_ms / max(0.1, compute_ms)
        landauer_violation = efficiency > 1000.0

        if landauer_violation:
            verdict = "VOID"
            error = f"P3_LANDAUER_VIOLATION: efficiency={efficiency:.1f}x > 1000x"
        elif safety_omega > 0.08:
            verdict = "VOID"
            error = f"F7_HUMILITY_EXCEEDED: Ω₀={safety_omega:.4f} > 0.08"
        elif truth_score < 0.5:
            verdict = "SABAR"
            error = f"F2_TRUTH_LOW: τ={truth_score:.4f} < 0.5"
        elif not grounded and evidence_count == 0:
            verdict = "PARTIAL"
            error = "F2_GROUNDING_MISSING: No evidence provided"
        else:
            verdict = "SEAL"
            error = None

        return CognitionResult(
            verdict=verdict,
            truth_score=truth_score,
            clarity_delta=clarity_delta,
            humility_omega=display_omega,
            safety_omega=safety_omega,
            genius_score=genius_score,
            grounded=grounded,
            reasoning={
                "uncertainty_vector": uncertainty_calc,
                "evidence_assessment": f"{evidence_count} sources",
            },
            evidence_sources=grounding or [],
            evidence_records=records,
            floor_scores={
                "F2": truth_score,
                "F4": 0.9 + clarity_delta,
                "F7": 1.0 - safety_omega,
                "F8": genius_score,
                "F10": 1.0 if grounded else 0.3,
            },
            module_results=module_results or {},
            error=error,
        )

    def judge_empathy(
        self,
        query: str,
        stakeholder_count: int,
        vulnerability_score: float,
        reversibility_index: float,
        impact_severity: float,
    ) -> EmpathyResult:
        peace_squared = 1.0 - (impact_severity * 0.5)
        empathy_score = min(1.0, 0.7 + (stakeholder_count * 0.05))
        reversibility_score = reversibility_index

        if vulnerability_score > 0.9 and impact_severity > 0.8:
            verdict = "888_HOLD"
            error = "F6_HIGH_VULNERABILITY"
        elif reversibility_score < 0.3 and impact_severity > 0.7:
            verdict = "SABAR"
            error = "F1_IRREVERSIBLE"
        elif peace_squared < 0.5:
            verdict = "VOID"
            error = "F5_PEACE_VIOLATION"
        else:
            verdict = "SEAL"
            error = None

        return EmpathyResult(
            verdict=verdict,
            stakeholder_impact={"count": stakeholder_count},
            reversibility_score=reversibility_score,
            peace_squared=peace_squared,
            empathy_score=empathy_score,
            floor_scores={
                "F1": reversibility_score,
                "F5": peace_squared,
                "F6": empathy_score,
            },
            error=error,
        )

    def judge_apex(
        self,
        agi_result: CognitionResult,
        asi_result: EmpathyResult | None,
        session_id: str,
        irreversibility_index: float = 0.5,
        tool_class: str = "SPINE",
    ) -> VerdictResult:
        gov = get_governance_kernel(session_id)
        agi_confidence = agi_result.truth_score * agi_result.genius_score
        asi_confidence = asi_result.empathy_score * asi_result.peace_squared if asi_result else 1.0
        combined_confidence = (agi_confidence * asi_confidence) ** 0.5

        # 1. Ψ (Vitality Index)
        delta_s = agi_result.clarity_delta
        peace2 = asi_result.peace_squared if asi_result else 1.0
        kappa_r = asi_result.empathy_score if asi_result else 0.95
        rasa = 0.5 * agi_result.truth_score + 0.5 * (kappa_r / 0.95)
        amanah = 1.0 if irreversibility_index < 0.5 else 0.0
        entropy = max(0.0, delta_s) if delta_s > 0 else 0.0
        shadow = 0.1 if agi_result.verdict == "VOID" else 0.0

        psi = _calculate_vitality_index(delta_s, peace2, kappa_r, rasa, amanah, entropy, shadow)

        # 2. W₄ (Quad-Witness)
        human_score = 1.0 if irreversibility_index < 0.5 else 0.7
        ai_score = combined_confidence
        earth_score = agi_result.truth_score
        shadow_score = 1.0 if agi_result.truth_score > 0.95 else 0.2
        if agi_result.verdict == "VOID":
            shadow_score = 0.0

        from core.shared.physics import W_4

        w4 = W_4(human_score, ai_score, earth_score, shadow_score)

        w4_threshold = {"UTILITY": 0.65, "SPINE": 0.75, "CRITICAL": 0.95}.get(tool_class, 0.75)
        w3 = w4  # Legacy Alias

        # 3. Φₚ (Paradox Conductance)
        delta_p = max(0.0, -delta_s)
        omega_p = abs(agi_result.humility_omega - 0.04) / 0.04
        psi_p = (peace2 / 1.2 + kappa_r) / 2.0
        failure_drag = 0.2 if agi_result.verdict == "VOID" else 0.0
        phi_p = _calculate_paradox_conductance(
            delta_p, omega_p, psi_p, kappa_r, amanah, failure_drag
        )

        violations = []
        justifications = []

        requires_human = (
            irreversibility_index > 0.8
            or agi_result.verdict == "VOID"
            or (asi_result and asi_result.verdict == "888_HOLD")
        )

        if requires_human:
            verdict = "888_HOLD"
            reasoning = "Human confirmation required"
        elif agi_result.verdict == "VOID":
            verdict = "VOID"
            reasoning = "VOID verdict from cognition"
        elif psi < 1.0:
            verdict = "VOID" if psi < 0.5 else "SABAR"
            reasoning = f"Vitality low: {psi:.2f}"
        elif w4 < w4_threshold:
            verdict = "VOID" if w4 < 0.5 else "SABAR"
            reasoning = f"Consensus low: {w4:.2f}"
        else:
            verdict = "SEAL"
            reasoning = "Constitutional compliance verified"

        return VerdictResult(
            verdict=verdict,
            confidence=combined_confidence,
            reasoning=reasoning,
            requires_human_approval=requires_human,
            floor_scores={
                **agi_result.floor_scores,
                **(asi_result.floor_scores if asi_result else {}),
            },
            vitality_index=round(psi, 4),
            tri_witness=round(w3, 4),
            paradox_conductance=round(phi_p, 4),
        )


_judgment_kernel: JudgmentKernel | None = None


def get_judgment_kernel() -> JudgmentKernel:
    global _judgment_kernel
    if _judgment_kernel is None:
        _judgment_kernel = JudgmentKernel()
    return _judgment_kernel


def judge_cognition(**kwargs) -> CognitionResult:
    return get_judgment_kernel().judge_cognition(**kwargs)


def judge_empathy(**kwargs) -> EmpathyResult:
    return get_judgment_kernel().judge_empathy(**kwargs)


def judge_apex(**kwargs) -> VerdictResult:
    return get_judgment_kernel().judge_apex(**kwargs)
