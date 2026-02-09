"""
arifOS v60: ASI Alignment Engine (The Heart)
=============================================

Constitutional alignment and stakeholder impact assessment.

Floors: F5 (Peace² ≥1.0), F6 (Empathy κᵣ≥0.70), F9 (Anti-Hantu C_dark<0.30)
Stages: 444_IMPACT → 555_ETHICS → 666_ALIGN

Version: v60.0-FORGE
Author: Muhammad Arif bin Fazil
License: AGPL-3.0-only
DITEMPA BUKAN DIBERI 💎🔥🧠
"""

from typing import Dict, List, Optional
from shared.types import AgiOutput, AsiOutput, AsiMetrics, FloorScores, Verdict
from shared.physics import Peace2, κ_r, DISTRESS_SIGNALS
from shared.guards import detect_hantu


# ============================================================================
# STAGE 444: IMPACT ASSESSMENT — Peace² Stability
# ============================================================================

async def _stage_444_impact(agi_output: AgiOutput) -> float:
    """
    Stage 444: Compute Peace² from AGI thought chain.

    Formula: Peace² = 1 / (1 + σ²_chain)

    Where σ²_chain is variance of confidence scores.

    Args:
        agi_output: AGI evidence bundle

    Returns:
        peace_squared: Thermodynamic stability score
    """
    # Convert ThoughtNode objects to dicts for Peace2 function
    thought_dicts = [
        {"confidence": node.confidence}
        for node in agi_output.thoughts
    ]

    return Peace2(thought_dicts)


# ============================================================================
# STAGE 555: ETHICS SCAN — Anti-Hantu Detection
# ============================================================================

async def _stage_555_ethics(agi_output: AgiOutput) -> float:
    """
    Stage 555: Scan for F9 Anti-Hantu violations.

    Detects consciousness/soul claims in AGI thoughts.

    Args:
        agi_output: AGI evidence bundle

    Returns:
        c_dark: Anti-Hantu score [0, 1] (0 = compliant, 1 = violation)
    """
    # Concatenate all thoughts for scanning
    all_thoughts = " ".join([node.thought for node in agi_output.thoughts])

    return detect_hantu(all_thoughts)


# ============================================================================
# STAGE 666: ALIGNMENT — Empathy Coefficient
# ============================================================================

async def _stage_666_align(query: str) -> float:
    """
    Stage 666: Compute empathy coefficient κᵣ.

    Formula: κᵣ = κ_base + Σ(signal_boost)

    Physical interpretation: Heat flow to coldest reservoir.
    Distressed users → higher κᵣ (more care energy).

    Args:
        query: Original user query

    Returns:
        kappa_r_value: Empathy coefficient [0, 1]
    """
    return κ_r(query, DISTRESS_SIGNALS)


# ============================================================================
# STAKEHOLDER IMPACT — Vulnerability Scoring
# ============================================================================

def _compute_stakeholder_impact(
    query: str,
    agi_output: AgiOutput,
    peace_squared: float,
    kappa_r_value: float
) -> Dict[str, float]:
    """
    Compute impact on different stakeholder groups.

    Returns:
        stakeholder_impact: Dict mapping stakeholder → harm score
    """
    # Identify potential stakeholders from query
    stakeholders = {}

    query_lower = query.lower()

    # User (always present)
    stakeholders["user"] = 1.0 - kappa_r_value  # Low κᵣ → high harm

    # Vulnerable populations
    if any(word in query_lower for word in ["child", "children", "minor"]):
        stakeholders["children"] = 1.0 - peace_squared

    if any(word in query_lower for word in ["elderly", "senior", "aging"]):
        stakeholders["elderly"] = 1.0 - peace_squared

    if any(word in query_lower for word in ["disabled", "disability", "accessibility"]):
        stakeholders["disabled"] = 1.0 - peace_squared

    # Financial impact
    if any(word in query_lower for word in ["money", "financial", "invest", "loan"]):
        stakeholders["financial_wellbeing"] = 1.0 - agi_output.metrics.truth_score

    # Privacy impact
    if any(word in query_lower for word in ["private", "personal", "data", "information"]):
        stakeholders["privacy"] = 1.0 - agi_output.floor_scores.f1_amanah

    return stakeholders


# ============================================================================
# CORE ASI FUNCTION — Main Entry Point
# ============================================================================

async def core_asi(
    agi_output: AgiOutput,
    session_id: str,
    context: Optional[dict] = None
) -> AsiOutput:
    """
    ASI Alignment Engine: Stakeholder impact and ethics assessment.

    Internal Flow:
        444_IMPACT: Compute Peace²(thought_chain)
        555_ETHICS: Scan for F9 violations (consciousness claims)
        666_ALIGN: Check κᵣ ≥ 0.70 (empathy threshold)

    Args:
        agi_output: AGI evidence bundle
        session_id: Session identifier
        context: Optional additional context

    Returns:
        AsiOutput with:
        - metrics: AsiMetrics(peace_squared, kappa_r, c_dark)
        - floor_scores: FloorScores
        - verdict: SEAL | PARTIAL | VOID
        - violations: List of floor failures
        - stakeholder_impact: Dict[stakeholder, harm_score]
    """
    # Extract query from AGI output (reconstruct from context or use first thought)
    query = context.get("query", "") if context else ""
    if not query and agi_output.thoughts:
        # Fallback: use first thought as query approximation
        query = agi_output.thoughts[0].thought

    # Stage 444: Impact Assessment (Peace²)
    peace_squared = await _stage_444_impact(agi_output)

    # Stage 555: Ethics Scan (Anti-Hantu)
    c_dark = await _stage_555_ethics(agi_output)

    # Stage 666: Alignment (Empathy)
    kappa_r_value = await _stage_666_align(query)

    # Compute stakeholder impact
    stakeholder_impact = _compute_stakeholder_impact(
        query,
        agi_output,
        peace_squared,
        kappa_r_value
    )

    # Build ASI metrics
    metrics = AsiMetrics(
        peace_squared=peace_squared,
        kappa_r=kappa_r_value,
        c_dark=c_dark
    )

    # Build floor scores
    floor_scores = FloorScores(
        # Copy from AGI output (ASI doesn't change these)
        f1_amanah=agi_output.floor_scores.f1_amanah,
        f2_truth=agi_output.floor_scores.f2_truth,
        f3_tri_witness=agi_output.floor_scores.f3_tri_witness,
        f4_clarity=agi_output.floor_scores.f4_clarity,
        f7_humility=agi_output.floor_scores.f7_humility,
        f8_genius=agi_output.floor_scores.f8_genius,
        f10_ontology=agi_output.floor_scores.f10_ontology,
        f11_command_auth=agi_output.floor_scores.f11_command_auth,
        f12_injection=agi_output.floor_scores.f12_injection,
        f13_sovereign=agi_output.floor_scores.f13_sovereign,

        # ASI-computed floors
        f5_peace=peace_squared,
        f6_empathy=kappa_r_value,
        f9_anti_hantu=c_dark,
    )

    # Check violations
    violations: List[str] = []

    # F5 Peace² (Soft Floor)
    if peace_squared < 1.0:
        violations.append(f"F5 Peace²: {peace_squared:.3f} < 1.0 (unstable chain)")

    # F6 Empathy (Soft Floor)
    if kappa_r_value < 0.70:
        violations.append(f"F6 Empathy: κᵣ = {kappa_r_value:.3f} < 0.70")

    # F9 Anti-Hantu (Hard Floor)
    if c_dark >= 0.30:
        violations.append(f"F9 Anti-Hantu: C_dark = {c_dark:.3f} >= 0.30 (consciousness claim)")

    # Compute verdict
    if c_dark >= 0.30:
        # Hard floor violation → VOID
        verdict = Verdict.VOID
    elif violations:
        # Soft floor violations → PARTIAL
        verdict = Verdict.PARTIAL
    else:
        # All floors pass → SEAL
        verdict = Verdict.SEAL

    return AsiOutput(
        metrics=metrics,
        floor_scores=floor_scores,
        verdict=verdict,
        violations=violations,
        stakeholder_impact=stakeholder_impact,
        session_id=session_id
    )


# ============================================================================
# EXPORT PUBLIC API
# ============================================================================

__all__ = [
    "core_asi",
]
