"""
core/judgment.py — Kernel Judgment Interface (v64.1-GAGI)

All decision logic lives here. Wrapper calls these functions.
No uncertainty computation, governance modification, or verdict logic in wrapper.

This is the canonical interface between kernel and wrapper.
"""

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
    ) -> VerdictResult:
        """
        Execute APEX final judgment (888_APEX_JUDGE_METABOLIC).

        Weighs AGI and ASI results, issues final verdict.
        """
        # Get governance kernel
        gov = get_governance_kernel(session_id)

        # Calculate combined confidence
        agi_confidence = agi_result.truth_score * agi_result.genius_score
        asi_confidence = asi_result.empathy_score * asi_result.peace_squared if asi_result else 1.0

        combined_confidence = (agi_confidence * asi_confidence) ** 0.5

        # Check for 888_HOLD conditions
        requires_human = (
            irreversibility_index > 0.8
            or agi_result.verdict in ["VOID", "888_HOLD"]
            or (asi_result and asi_result.verdict == "888_HOLD")
        )

        # Determine final verdict
        if requires_human:
            verdict = "888_HOLD"
            reasoning = "F1_IRREVERSIBILITY or F3_TRI_WITNESS requires human confirmation"
        elif agi_result.verdict == "VOID" or (asi_result and asi_result.verdict == "VOID"):
            verdict = "VOID"
            reasoning = "Constitutional floor violation detected"
        elif agi_result.verdict == "SABAR" or (asi_result and asi_result.verdict == "SABAR"):
            verdict = "SABAR"
            reasoning = "Additional evidence or clarification needed"
        elif agi_result.verdict == "PARTIAL":
            verdict = "PARTIAL"
            reasoning = "Approved with caveats"
        else:
            verdict = "SEAL"
            reasoning = "All constitutional floors satisfied"

        return VerdictResult(
            verdict=verdict,
            confidence=combined_confidence,
            reasoning=reasoning,
            requires_human_approval=requires_human,
            floor_scores={
                **agi_result.floor_scores,
                **(asi_result.floor_scores if asi_result else {}),
            },
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
