"""
core/judgment.py — Kernel Judgment Interface (v64.2-HARDENED)

All decision logic lives here. Wrapper calls these functions.
No uncertainty computation, governance modification, or verdict logic in wrapper.

P0/P1 HARDENING:
- Ψ (Vitality Index) Master Equation
- W₃ (Tri-Witness) geometric mean consensus
- Φₚ (Paradox Conductance) resolution check

This is the canonical interface between kernel and wrapper.
"""

import math
from dataclasses import dataclass
from typing import Any

from core.governance_kernel import get_governance_kernel
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
    tri_witness: float | None = None  # W₃
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
    
    W₃ = ∛(H × A × E)
    
    Where:
    - H (Human): Intent / Sovereign authority
    - A (AI): Internal logic / Constitutional compliance
    - E (Earth): Empirical grounding / Evidence
    
    Dynamic Thresholds:
    - UTILITY: W₃ >= 0.95
    - SPINE: W₃ >= 0.99
    - CRITICAL: W₃ >= 0.995
    
    Returns:
        Tri-witness consensus score
    """
    return (human_score * ai_score * earth_score) ** (1/3)


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
    
    Simplified for implementation:
    Φₚ = (clarity_term + psi_p + (1 - omega_p)) / (1 + failure_drag)
    
    Threshold: Φₚ >= 1.0 for paradox resolution (SEAL)
    
    Returns:
        Paradox conductance score
    """
    clarity_term = max(0.0, min(1.0, -delta_p + 0.2))
    phi_p = (clarity_term + psi_p + (1.0 - omega_p)) / (1.0 + failure_drag)
    return min(2.0, max(0.0, phi_p))


class JudgmentKernel:
    """
    Canonical judgment interface for arifOS kernel.

    All decision logic lives here. Wrapper must not implement judgment.
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
        module_results: dict | None = None,
    ) -> CognitionResult:
        """
        Execute AGI cognition judgment (111-333_AGI).

        Computes uncertainty, truth, clarity, humility, genius.
        Returns verdict and all floor scores.
        """
        # Calculate 5-dimensional uncertainty vector
        uncertainty_calc = calculate_uncertainty(
            evidence_count=evidence_count,
            evidence_relevance=evidence_relevance,
            reasoning_consistency=reasoning_consistency,
            knowledge_gaps=knowledge_gaps,
            model_logits_confidence=model_logits_confidence,
        )

        safety_omega = uncertainty_calc["safety_omega"]  # Harmonic - for kernel decisions
        display_omega = uncertainty_calc["display_omega"]  # Geometric - for display

        # F2: Truth - confidence grounded in evidence + uncertainty
        if grounding and len(grounding) > 0:
            avg_relevance = sum(e.get("relevance", 0) for e in grounding) / len(grounding)
            truth_score = min(0.99, 0.7 + (len(grounding) * 0.05) - (safety_omega * 0.2))
        else:
            truth_score = max(0.3, 0.85 - (safety_omega * 0.3))

        # F4: Clarity - entropy reduction
        clarity_delta = -0.1  # Placeholder - real implementation would calculate

        # F7: Humility - uncertainty admission
        # Already captured in omega values

        # F8: Genius - coherence
        genius_score = 0.88  # Placeholder

        # F10: Ontology - grounding check
        grounded = bool(grounding and len(grounding) > 0)

        # Determine verdict
        if safety_omega > 0.08:
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
            humility_omega=display_omega,  # Display uses geometric
            safety_omega=safety_omega,  # Safety uses harmonic
            genius_score=genius_score,
            grounded=grounded,
            reasoning={
                "uncertainty_vector": uncertainty_calc,
                "evidence_assessment": f"{evidence_count} sources, avg_relevance={evidence_relevance:.2f}",
            },
            evidence_sources=grounding or [],
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
        """
        Execute ASI empathy judgment (555-666_ASI).

        Models stakeholder impact, reversibility, peace, empathy.
        """
        # F5: Peace² - stability metric
        peace_squared = 1.0 - (impact_severity * 0.5)

        # F6: Empathy - stakeholder awareness
        empathy_score = min(1.0, 0.7 + (stakeholder_count * 0.05))

        # F1: Amanah - reversibility check
        reversibility_score = reversibility_index

        # Determine verdict based on empathy floors
        if vulnerability_score > 0.9 and impact_severity > 0.8:
            verdict = "888_HOLD"
            error = "F6_HIGH_VULNERABILITY: Requires human review"
        elif reversibility_score < 0.3 and impact_severity > 0.7:
            verdict = "SABAR"
            error = "F1_IRREVERSIBLE_HIGH_IMPACT: Proceed with caution"
        elif peace_squared < 0.5:
            verdict = "VOID"
            error = "F5_PEACE_VIOLATION: Action escalates conflict"
        else:
            verdict = "SEAL"
            error = None

        return EmpathyResult(
            verdict=verdict,
            stakeholder_impact={
                "count": stakeholder_count,
                "vulnerability": vulnerability_score,
            },
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
        tool_class: str = "SPINE",  # UTILITY, SPINE, CRITICAL
    ) -> VerdictResult:
        """
        Execute APEX final judgment (888_APEX_JUDGE_METABOLIC).

        Weighs AGI and ASI results, issues final verdict.
        
        P0/P1 HARDENING: Applies Ψ, W₃, and Φₚ equations for thermodynamic verdict.
        """
        # Get governance kernel
        gov = get_governance_kernel(session_id)

        # Calculate combined confidence
        agi_confidence = agi_result.truth_score * agi_result.genius_score
        asi_confidence = asi_result.empathy_score * asi_result.peace_squared if asi_result else 1.0

        combined_confidence = (agi_confidence * asi_confidence) ** 0.5

        # ═══════════════════════════════════════════════════════
        # P0/P1 HARDENING: Thermodynamic Master Equations
        # ═══════════════════════════════════════════════════════
        
        # 1. Ψ (Vitality Index)
        delta_s = agi_result.clarity_delta
        peace2 = asi_result.peace_squared if asi_result else 1.0
        kappa_r = asi_result.empathy_score if asi_result else 0.95
        rasa = 0.5 * agi_result.truth_score + 0.5 * (kappa_r / 0.95)
        amanah = 1.0 if irreversibility_index < 0.5 else 0.0  # Binary F1 check
        entropy = max(0.0, delta_s) if delta_s > 0 else 0.0
        shadow = 0.1 if agi_result.verdict == "VOID" else 0.0
        
        psi = _calculate_vitality_index(
            delta_s=delta_s,
            peace2=peace2,
            kappa_r=kappa_r,
            rasa=rasa,
            amanah=amanah,
            entropy=entropy,
            shadow=shadow,
        )
        
        # 2. W₃ (Tri-Witness Consensus) - Geometric Mean
        human_score = 1.0 if irreversibility_index < 0.5 else 0.7  # Sovereign intent
        ai_score = combined_confidence  # AI internal logic
        earth_score = agi_result.truth_score  # Empirical grounding
        
        w3 = _calculate_tri_witness(
            human_score=human_score,
            ai_score=ai_score,
            earth_score=earth_score,
        )
        
        # Dynamic threshold based on tool class
        w3_threshold = {
            "UTILITY": 0.95,
            "SPINE": 0.99,
            "CRITICAL": 0.995,
        }.get(tool_class, 0.99)
        
        # 3. Φₚ (Paradox Conductance)
        delta_p = max(0.0, -delta_s)  # Paradox heat from entropy
        omega_p = abs(agi_result.humility_omega - 0.04) / 0.04
        psi_p = (peace2 / 1.2 + kappa_r) / 2.0
        failure_drag = 0.2 if agi_result.verdict == "VOID" else 0.0
        
        phi_p = _calculate_paradox_conductance(
            delta_p=delta_p,
            omega_p=omega_p,
            psi_p=psi_p,
            kappa_r=kappa_r,
            amanah=amanah,
            failure_drag=failure_drag,
        )
        
        # Check for 888_HOLD conditions
        requires_human = (
            irreversibility_index > 0.8
            or agi_result.verdict in ["VOID", "888_HOLD"]
            or (asi_result and asi_result.verdict == "888_HOLD")
        )

        # ═══════════════════════════════════════════════════════
        # P0/P1 HARDENING: Verdict Determination Cascade
        # Priority: Hard Fail → Ψ → W₃ → Φₚ → Legacy checks
        # ═══════════════════════════════════════════════════════
        
        if requires_human:
            verdict = "888_HOLD"
            reasoning = "F1_IRREVERSIBILITY or F3_TRI_WITNESS requires human confirmation"
        elif agi_result.verdict == "VOID" or (asi_result and asi_result.verdict == "VOID"):
            verdict = "VOID"
            reasoning = "Constitutional floor violation detected"
        # P0: Ψ (Vitality) check
        elif psi < 1.0:
            if psi < 0.5:
                verdict = "VOID"
                reasoning = f"P0_VITALITY_CRITICAL: Ψ={psi:.3f} < 0.5 (system unstable)"
            else:
                verdict = "SABAR"
                reasoning = f"P0_VITALITY_LOW: Ψ={psi:.3f} < 1.0 (cooling required)"
        # P1: W₃ (Tri-Witness) check
        elif w3 < w3_threshold:
            if min(human_score, ai_score, earth_score) < 0.90:
                verdict = "VOID"
                reasoning = f"P1_WITNESS_SHATTER: W₃={w3:.3f}, min witness < 0.90"
            else:
                verdict = "SABAR"
                reasoning = f"P1_WITNESS_LOW: W₃={w3:.3f} < {w3_threshold}"
        # P1: Φₚ (Paradox) check
        elif phi_p < 1.0:
            if phi_p < 0.5:
                verdict = "VOID"
                reasoning = f"P1_PARADOX_CRITICAL: Φₚ={phi_p:.3f} < 0.5 (unresolvable)"
            else:
                verdict = "SABAR"
                reasoning = f"P1_PARADOX_UNRESOLVED: Φₚ={phi_p:.3f} < 1.0"
        elif agi_result.verdict == "SABAR" or (asi_result and asi_result.verdict == "SABAR"):
            verdict = "SABAR"
            reasoning = "Additional evidence or clarification needed"
        elif agi_result.verdict == "PARTIAL":
            verdict = "PARTIAL"
            reasoning = "Approved with caveats"
        else:
            verdict = "SEAL"
            reasoning = "All constitutional floors and thermodynamic constraints satisfied"

        return VerdictResult(
            verdict=verdict,
            confidence=combined_confidence,
            reasoning=reasoning,
            requires_human_approval=requires_human,
            floor_scores={
                **agi_result.floor_scores,
                **(asi_result.floor_scores if asi_result else {}),
            },
            # P0/P1 HARDENING: Thermodynamic metrics
            vitality_index=round(psi, 4),
            tri_witness=round(w3, 4),
            paradox_conductance=round(phi_p, 4),
        )


# Singleton instance for wrapper to use
_judgment_kernel: JudgmentKernel | None = None


def get_judgment_kernel() -> JudgmentKernel:
    """Get the singleton JudgmentKernel instance."""
    global _judgment_kernel
    if _judgment_kernel is None:
        _judgment_kernel = JudgmentKernel()
    return _judgment_kernel


# Convenience functions for wrapper
def judge_cognition(**kwargs) -> CognitionResult:
    """Wrapper convenience: Judge AGI cognition."""
    return get_judgment_kernel().judge_cognition(**kwargs)


def judge_empathy(**kwargs) -> EmpathyResult:
    """Wrapper convenience: Judge ASI empathy."""
    return get_judgment_kernel().judge_empathy(**kwargs)


def judge_apex(**kwargs) -> VerdictResult:
    """Wrapper convenience: Judge APEX verdict."""
    return get_judgment_kernel().judge_apex(**kwargs)
