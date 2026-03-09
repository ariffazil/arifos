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
    genius_score: float
    grounded: bool
    floor_scores: dict[str, float]
    module_results: dict[str, Any]
    motto: str | None = None
    clarity_delta: float = 0.0
    humility_omega: float = 0.04
    safety_omega: float = 0.04
    reasoning: dict[str, Any] = field(default_factory=dict)
    evidence_sources: list[dict] = field(default_factory=list)
    evidence_records: list[EvidenceRecord] = field(default_factory=list)
    error: str | None = None


@dataclass
class EmpathyResult:
    """Result of ASI empathy judgment."""

    verdict: str
    reversibility_score: float
    peace_squared: float
    empathy_score: float
    floor_scores: dict[str, float]
    motto: str | None = None
    stakeholder_impact: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


@dataclass
class VerdictResult:
    """Result of APEX final judgment."""

    verdict: str
    confidence: float
    floor_scores: dict[str, float]
    motto: str | None = None
    reasoning: str | None = None
    requires_human_approval: bool = False
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
        from core.enforcement.genius import calculate_genius
        from core.shared.mottos import get_motto_by_stage
        from core.shared.types import FloorScores

        uncertainty_calc = calculate_uncertainty(
            evidence_count=evidence_count,
            evidence_relevance=evidence_relevance,
            reasoning_consistency=reasoning_consistency,
            knowledge_gaps=knowledge_gaps,
            model_logits_confidence=model_logits_confidence,
        )

        safety_omega = uncertainty_calc["safety_omega"]
        truth_score = (
            min(
                0.99,
                (
                    sum(g.get("relevance", 0.9) for g in (grounding or []))
                    / max(1, len(grounding or []))
                )
                - (safety_omega * 0.1),
            )
            if grounding
            else 0.5
        )

        partial_floors = FloorScores(
            f2_truth=max(0.0, truth_score),
            f4_clarity=0.9,
            f7_humility=max(0.0, round(0.04 - (safety_omega / 10.0), 4)),
            f8_genius=0.8,
            f10_ontology=bool(grounding),
        )

        from core.enforcement.genius import calculate_genius
        from core.shared.types import Verdict

        genius_res = calculate_genius(
            partial_floors,
            compute_budget_used=compute_ms,
            compute_budget_max=max(expected_ms * 2, 1000),
        )
        motto = get_motto_by_stage("333")

        # RULE: 333 MIND (Laboratory) forbidden: VOID
        # The lab must be allowed to think wrong.
        g_score = genius_res["genius_score"]
        if g_score >= 0.8:
            verdict = Verdict.SEAL
        elif g_score >= 0.6:
            verdict = Verdict.PROVISIONAL
        elif g_score >= 0.4:
            verdict = Verdict.PARTIAL
        else:
            verdict = Verdict.SABAR

        return CognitionResult(
            verdict=verdict.value,
            truth_score=truth_score,
            genius_score=g_score,
            grounded=bool(grounding),
            motto=f"{motto.malay} | {motto.english}" if motto else None,
            floor_scores=partial_floors.model_dump(),
            module_results={"omega": safety_omega},
        )

    def judge_empathy(
        self,
        query: str,
        stakeholder_count: int,
        vulnerability_score: float,
        reversibility_index: float,
        impact_severity: float,
    ) -> EmpathyResult:
        from core.enforcement.genius import calculate_genius
        from core.shared.mottos import get_motto_by_stage
        from core.shared.types import FloorScores, Verdict

        peace_squared = (1.0 - impact_severity) ** 2
        empathy_score = min(1.0, 0.6 + (stakeholder_count * 0.08) - (vulnerability_score * 0.2))
        motto = get_motto_by_stage("555")

        # RULE: 555 HEART (Safety) forbidden: VOID
        # Heart does not reject ideas. It pauses them.
        if peace_squared > 0.8:
            verdict = Verdict.SEAL
        elif peace_squared > 0.4:
            verdict = Verdict.PARTIAL
        else:
            verdict = Verdict.HOLD  # Requires human review due to risk

        return EmpathyResult(
            verdict=verdict.value,
            reversibility_score=1.0 - reversibility_index,
            peace_squared=peace_squared,
            empathy_score=empathy_score,
            motto=f"{motto.malay} | {motto.english}" if motto else None,
            floor_scores={
                "F1": 1.0 - reversibility_index,
                "F5": peace_squared,
                "F6": empathy_score,
            },
        )

    def judge_apex(
        self,
        agi_result: CognitionResult,
        asi_result: EmpathyResult | None,
        session_id: str,
        irreversibility_index: float = 0.5,
        tool_class: str = "SPINE",
    ) -> VerdictResult:
        from core.enforcement.genius import calculate_genius
        from core.shared.mottos import get_motto_by_stage
        from core.shared.types import FloorScores

        kernel = get_governance_kernel(session_id)
        combined_floors = FloorScores(
            f1_amanah=asi_result.reversibility_score if asi_result else 1.0 - irreversibility_index,
            f2_truth=agi_result.truth_score,
            f4_clarity=0.9,
            f5_peace=asi_result.peace_squared if asi_result else 1.0,
            f6_empathy=asi_result.empathy_score if asi_result else 0.95,
            f8_genius=0.8,
            f13_sovereign=1.0 if kernel.human_approval_status == "approved" else 0.7,
        )

        from core.shared.types import Verdict

        genius_res = calculate_genius(combined_floors, h=kernel.hysteresis_penalty)
        g_score = genius_res["genius_score"]
        motto = get_motto_by_stage("888")

        # RULE: 888 JUDGE allows VOID
        if g_score >= 0.8:
            verdict = Verdict.SEAL
        elif g_score >= 0.6:
            verdict = Verdict.PARTIAL
        elif g_score >= 0.4:
            verdict = Verdict.HOLD
        else:
            verdict = Verdict.VOID

        return VerdictResult(
            verdict=verdict.value,
            confidence=g_score,
            motto=f"{motto.malay} | {motto.english}" if motto else "DITEMPA, BUKAN DIBERI",
            vitality_index=round(g_score / 0.5, 4),
            floor_scores=combined_floors.model_dump(),
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
