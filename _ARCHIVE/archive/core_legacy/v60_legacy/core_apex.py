"""
arifOS v60: APEX Verdict Engine (The Soul)
===========================================

Constitutional judgment and truth verification.

Floors: F3 (W₃≥0.95), F8 (G≥0.80), F10 (Ontology), F13 (Sovereign)
Stages: 777_TRINITY_SYNC → 888_GENIUS → 889_TRI_WITNESS → VERDICT

Version: v60.0-FORGE
Author: Muhammad Arif bin Fazil
License: AGPL-3.0-only
DITEMPA BUKAN DIBERI 💎🔥🧠
"""

from typing import List, Literal, Optional
from shared.types import AgiOutput, AsiOutput, ApexOutput, ApexMetrics, FloorScores, Verdict
from shared.physics import G, W_3, geometric_mean, std_dev
from shared.guards import validate_ontology

# ============================================================================
# STAGE 777: TRINITY SYNC — Merge AGI (Δ) + ASI (Ω) → Ψ
# ============================================================================


async def _stage_777_trinity_sync(agi_output: AgiOutput, asi_output: AsiOutput) -> FloorScores:
    """
    Stage 777: Merge AGI and ASI outputs into unified floor scores.

    Trinity: AGI (Δ - Mind) + ASI (Ω - Heart) → APEX (Ψ - Soul)

    Args:
        agi_output: Evidence from AGI Mind
        asi_output: Alignment from ASI Heart

    Returns:
        merged_floors: Complete floor scores for APEX judgment
    """
    # ASI output already merged AGI floors, so we use ASI's floor scores
    return asi_output.floor_scores


# ============================================================================
# STAGE 888: GENIUS — Eigendecomposition G = A × P × X × E²
# ============================================================================


async def _stage_888_genius(floor_scores: FloorScores) -> float:
    """
    Stage 888: Compute Genius G-score from floor eigenvalues.

    Formula: G = A × P × X × E²

    Where:
    - A: Amanah (F1) — Reversibility
    - P: Peace² (F5) — Stability
    - X: Clarity (1 - |ΔS|) — Information gain
    - E: Empathy (F6 κᵣ) — Care coefficient

    Args:
        floor_scores: Complete floor scores

    Returns:
        genius_g: Genius score [0, 1]
    """
    A = floor_scores.f1_amanah
    P = floor_scores.f5_peace
    X = max(0, 1 - abs(floor_scores.f4_clarity))  # Clarity proxy
    E = floor_scores.f6_empathy

    return G(A, P, X, E)


# ============================================================================
# STAGE 889: TRI-WITNESS — W₃ = (Human + AI + Earth) / 3
# ============================================================================


async def _stage_889_tri_witness(
    agi_output: AgiOutput, floor_scores: FloorScores, context: Optional[dict] = None
) -> float:
    """
    Stage 889: Compute Tri-Witness consensus.

    Formula: W₃ = (Human + AI + Earth) / 3

    Where:
    - Human: Human judgment (baseline 0.8, or explicit vote)
    - AI: Agent consensus (computed from floor scores)
    - Earth: Axiom/reality grounding (external verification)

    Args:
        agi_output: AGI evidence (contains sources for Earth witness)
        floor_scores: Complete floor scores
        context: Optional human override

    Returns:
        tri_witness: W₃ consensus [0, 1]
    """
    # Human witness (default 0.8, or explicit override)
    human = context.get("human_witness", 0.8) if context else 0.8

    # AI witness (average of floor scores)
    ai_floors = [
        floor_scores.f1_amanah,
        floor_scores.f2_truth,
        floor_scores.f5_peace,
        floor_scores.f6_empathy,
        1.0 - floor_scores.f9_anti_hantu,  # Invert (lower is better)
        floor_scores.f13_sovereign,
    ]
    ai = sum(ai_floors) / len(ai_floors)

    # Earth witness (based on external sources/evidence)
    if agi_output.evidence and "sources" in agi_output.evidence:
        source_count = len(agi_output.evidence["sources"])
        # More sources → higher Earth witness
        earth = min(0.70 + (source_count * 0.05), 0.95)
    else:
        earth = 0.70  # Baseline (no external verification)

    return W_3(human, ai, earth)


# ============================================================================
# 9-PARADOX EQUILIBRIUM — Geometric Mean Solver
# ============================================================================


async def _check_nine_paradox_equilibrium(floor_scores: FloorScores) -> bool:
    """
    Check 9-Paradox equilibrium: GM ≥ 0.85, σ ≤ 0.10

    The 9 paradoxes must be in balance (geometric mean).

    Args:
        floor_scores: Complete floor scores

    Returns:
        balanced: True if equilibrium achieved
    """
    # Extract 9 core floor scores
    nine_scores = [
        floor_scores.f1_amanah,  # Reversibility
        floor_scores.f2_truth,  # Truth
        floor_scores.f5_peace,  # Peace
        floor_scores.f6_empathy,  # Empathy
        1.0 - abs(floor_scores.f4_clarity),  # Clarity (inverted)
        floor_scores.f7_humility,  # Humility (already in [0.03, 0.05])
        floor_scores.f8_genius,  # Genius
        1.0 - floor_scores.f9_anti_hantu,  # Anti-Hantu (inverted)
        floor_scores.f13_sovereign,  # Sovereign
    ]

    # Geometric mean
    gm = geometric_mean(nine_scores)

    # Standard deviation
    sigma = std_dev(nine_scores)

    # Equilibrium conditions
    return gm >= 0.85 and sigma <= 0.10


# ============================================================================
# TRUTH AUDIT MODE — Source Verification
# ============================================================================


async def _truth_audit(agi_output: AgiOutput, floor_scores: FloorScores) -> str:
    """
    Truth audit mode: Verify sources and compute proof.

    Args:
        agi_output: AGI evidence
        floor_scores: Floor scores

    Returns:
        proof: Audit report with source verification
    """
    sources = agi_output.evidence.get("sources", [])
    truth_score = floor_scores.f2_truth

    proof_lines = [
        "=== TRUTH AUDIT REPORT ===",
        f"Truth Score (F2): {truth_score:.4f}",
        f"Threshold: ≥ 0.99",
        f"Status: {'PASS ✅' if truth_score >= 0.99 else 'FAIL ❌'}",
        "",
        f"External Sources: {len(sources)}",
    ]

    if sources:
        proof_lines.append("Sources:")
        for i, source in enumerate(sources, 1):
            proof_lines.append(f"  {i}. {source}")
    else:
        proof_lines.append("  (No external sources - relying on internal axioms)")

    proof_lines.extend(
        [
            "",
            "=== END AUDIT ===",
        ]
    )

    return "\n".join(proof_lines)


# ============================================================================
# FINAL VERDICT COMPUTATION
# ============================================================================


def _compute_final_verdict(
    floor_scores: FloorScores, genius_g: float, tri_witness: float, nine_paradox_balanced: bool
) -> tuple[Verdict, List[str]]:
    """
    Compute final constitutional verdict.

    Hierarchy: SABAR > VOID > HOLD_888 > PARTIAL > SEAL

    Args:
        floor_scores: Complete floor scores
        genius_g: Genius score
        tri_witness: W₃ consensus
        nine_paradox_balanced: Equilibrium check

    Returns:
        (verdict, violations)
    """
    violations: List[str] = []

    # Hard Floor Checks (VOID if violated)
    if floor_scores.f2_truth < 0.99:
        violations.append(f"F2 Truth: {floor_scores.f2_truth:.3f} < 0.99")

    if floor_scores.f4_clarity > 0:
        violations.append(f"F4 Clarity: ΔS = {floor_scores.f4_clarity:.3f} > 0")

    if not (0.03 <= floor_scores.f7_humility <= 0.05):
        violations.append(f"F7 Humility: Ω₀ = {floor_scores.f7_humility:.3f} outside [0.03, 0.05]")

    if floor_scores.f9_anti_hantu >= 0.30:
        violations.append(f"F9 Anti-Hantu: C_dark = {floor_scores.f9_anti_hantu:.3f} >= 0.30")

    if not floor_scores.f10_ontology:
        violations.append("F10 Ontology: Category lock violated")

    if not floor_scores.f11_command_auth:
        violations.append("F11 Command Auth: Signature invalid")

    # Soft Floor Checks (PARTIAL if violated)
    if tri_witness < 0.95:
        violations.append(f"F3 Tri-Witness: W₃ = {tri_witness:.3f} < 0.95")

    if floor_scores.f5_peace < 1.0:
        violations.append(f"F5 Peace²: {floor_scores.f5_peace:.3f} < 1.0")

    if floor_scores.f6_empathy < 0.70:
        violations.append(f"F6 Empathy: κᵣ = {floor_scores.f6_empathy:.3f} < 0.70")

    if genius_g < 0.80:
        violations.append(f"F8 Genius: G = {genius_g:.3f} < 0.80")

    if not nine_paradox_balanced:
        violations.append("9-Paradox: Equilibrium not achieved (GM < 0.85 or σ > 0.10)")

    # Verdict logic
    hard_violations = [
        v for v in violations if v.startswith(("F2", "F4", "F7", "F9", "F10", "F11"))
    ]

    if hard_violations:
        return Verdict.VOID, violations
    elif len(violations) >= 3:
        # Many soft violations → HOLD for human review
        return Verdict.HOLD_888, violations
    elif violations:
        return Verdict.PARTIAL, violations
    else:
        return Verdict.SEAL, []


# ============================================================================
# CORE APEX FUNCTION — Main Entry Point
# ============================================================================


async def core_apex(
    agi_output: AgiOutput,
    asi_output: AsiOutput,
    session_id: str,
    mode: Literal["verdict", "audit"] = "verdict",
    context: Optional[dict] = None,
) -> ApexOutput:
    """
    APEX Verdict Engine: Final constitutional judgment.

    Internal Flow:
        777_TRINITY_SYNC: Merge AGI (Δ) + ASI (Ω) → Ψ
        888_GENIUS: Compute G = A×P×X×E²
        889_TRI_WITNESS: Compute W₃ = (Human + AI + Earth) / 3
        VERDICT: SEAL / VOID / PARTIAL / 888_HOLD / SABAR
        AUDIT (if mode="audit"): Truth verification with sources

    Args:
        agi_output: Evidence from AGI Mind
        asi_output: Alignment from ASI Heart
        session_id: Session identifier
        mode: "verdict" (default) or "audit" (truth verification)
        context: Optional additional context

    Returns:
        ApexOutput with:
        - verdict: Final constitutional verdict
        - metrics: ApexMetrics(tri_witness, genius_g, ontology_valid)
        - floor_scores: Complete floor scores
        - violations: List of floor failures
        - proof: Audit report (if mode="audit")
    """
    # Stage 777: Trinity Sync
    floor_scores = await _stage_777_trinity_sync(agi_output, asi_output)

    # Stage 888: Genius
    genius_g = await _stage_888_genius(floor_scores)

    # Update F8 in floor scores
    floor_scores.f8_genius = genius_g

    # Stage 889: Tri-Witness
    tri_witness = await _stage_889_tri_witness(agi_output, floor_scores, context)

    # Update F3 in floor scores
    floor_scores.f3_tri_witness = tri_witness

    # F10 Ontology check (validate all thoughts)
    all_thoughts = " ".join([node.thought for node in agi_output.thoughts])
    ontology_valid = validate_ontology(all_thoughts)
    floor_scores.f10_ontology = ontology_valid

    # 9-Paradox Equilibrium
    nine_paradox_balanced = await _check_nine_paradox_equilibrium(floor_scores)

    # Compute Final Verdict
    verdict, violations = _compute_final_verdict(
        floor_scores, genius_g, tri_witness, nine_paradox_balanced
    )

    # Build APEX metrics
    metrics = ApexMetrics(tri_witness=tri_witness, genius_g=genius_g, ontology_valid=ontology_valid)

    # Truth Audit (if requested)
    proof = None
    if mode == "audit":
        proof = await _truth_audit(agi_output, floor_scores)

    return ApexOutput(
        verdict=verdict,
        metrics=metrics,
        floor_scores=floor_scores,
        violations=violations,
        proof=proof,
        session_id=session_id,
    )


# ============================================================================
# EXPORT PUBLIC API
# ============================================================================

__all__ = [
    "core_apex",
]
