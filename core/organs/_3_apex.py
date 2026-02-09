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

from typing import Dict, Any, List, Optional

from core.shared.physics import (
    W_3, W_3_from_tensor, G, TrinityTensor,
    ConstitutionalTensor, PeaceSquared, UncertaintyBand, GeniusDial,
)
from core.shared.types import Verdict
from core.shared.mottos import get_motto_for_stage, get_all_stage_mottos, format_all_stage_mottos


# =============================================================================
# ACTION 1: SYNC (Stage 444) — Trinity Merge Δ + Ω → Ψ
# =============================================================================


async def sync(
    agi_tensor: ConstitutionalTensor,
    asi_output: Dict[str, Any],
    session_id: str,
) -> Dict[str, Any]:
    """
    Stage 444: SYNC — The Bridge between Mind and Heart
    
    Merge AGI (Δ - Mind) and ASI (Ω - Heart) outputs into unified Ψ.
    
    Args:
        agi_tensor: AGI Mind output (witness, truth, entropy, genius)
        asi_output: ASI Heart output (kappa_r, peace, reversibility)
        session_id: Constitutional session token
    
    Returns:
        Dict with:
        - witness: Merged TrinityTensor
        - W_3: Tri-Witness consensus score
        - floor_scores: Combined F3, F5, F6, F8
        - pre_verdict: Initial assessment (before full judgment)
    
    Action Chain:
        agi.reason → asi.align → sync (bridge)
        sync → forge → judge (completes Soul)
    """
    # Merge witnesses (geometric mean of components)
    agi_witness = agi_tensor.witness
    
    # ASI contributes to Human witness (care perspective)
    asi_care = asi_output.get("kappa_r", 0.7)
    
    merged_witness = TrinityTensor(
        H=min(agi_witness.H, asi_care),  # Human limited by empathy
        A=agi_witness.A,                  # AI from AGI
        S=agi_witness.S,                  # System from AGI
    )
    
    # Compute Tri-Witness
    w3_score = W_3_from_tensor(merged_witness)
    
    # Determine pre-verdict
    if w3_score >= 0.95:
        pre_verdict = "SEAL"
    elif w3_score >= 0.85:
        pre_verdict = "PARTIAL"
    else:
        pre_verdict = "VOID"
    
    # Build merged floor scores
    floor_scores = {
        "f3_tri_witness": w3_score,
        "f5_peace": asi_output.get("peace_squared", 1.0),
        "f6_empathy": asi_output.get("kappa_r", 0.7),
        "f8_genius": agi_tensor.genius.G(),
    }
    
    # Get 444_SYNC motto: DIHADAPI, BUKAN DITANGGUHI
    motto = get_motto_for_stage("444_SYNC")
    all_mottos = get_all_stage_mottos()
    mottos = [f"[{m.stage}] {m.positive}, {m.negative} | {m.meaning}" for m in all_mottos]
    mottos_output = format_all_stage_mottos()
    
    return {
        "stage": 444,
        "action": "sync",
        "witness": merged_witness,
        "W_3": w3_score,
        "floor_scores": floor_scores,
        "pre_verdict": pre_verdict,
        "is_synced": w3_score >= 0.95,
        "session_id": session_id,
        "motto": str(motto),
        "motto_output": f"[{motto.stage}] {motto.positive}, {motto.negative} | {motto.meaning}",
        "mottos": mottos,
        "mottos_output": mottos_output,
    }


# =============================================================================
# ACTION 2: FORGE (Stage 777) — Phase Transition / Eureka
# =============================================================================


async def forge(
    sync_output: Dict[str, Any],
    agi_tensor: ConstitutionalTensor,
    session_id: str,
) -> Dict[str, Any]:
    """
    Stage 777: FORGE — Collapse vectors into scalar output
    
    Synthesize AGI reasoning + ASI alignment → unified solution.
    
    Args:
        sync_output: Trinity sync output
        agi_tensor: AGI Mind output
        session_id: Constitutional session token
    
    Returns:
        Dict with:
        - genius_G: Computed G = A·P·X·E²
        - is_genius: Whether G ≥ 0.80
        - solution_draft: Synthesized response
        - coherence: Internal consistency score
    
    Action Chain:
        sync → forge → judge
    """
    floor_scores = sync_output["floor_scores"]
    
    # Extract components for G
    A = floor_scores["f5_peace"]  # Amanah proxy
    P = floor_scores["f6_empathy"]  # Present
    X = agi_tensor.genius.X  # Exploration from AGI
    E = min(1.0, agi_tensor.entropy_delta * -1 + 0.5)  # Energy from clarity
    
    # Compute Genius
    genius_score = G(A, P, X, E)
    
    # Check coherence
    coherence = _check_coherence(agi_tensor, sync_output)
    
    # Generate solution draft
    solution = _generate_solution(agi_tensor, sync_output)
    
    # Get 777_FORGE motto: DIUSAHAKAN, BUKAN DIHARAPI
    motto = get_motto_for_stage("777_FORGE")
    all_mottos = get_all_stage_mottos()
    mottos = [f"[{m.stage}] {m.positive}, {m.negative} | {m.meaning}" for m in all_mottos]
    mottos_output = format_all_stage_mottos()
    
    return {
        "stage": 777,
        "action": "forge",
        "genius_G": genius_score,
        "is_genius": genius_score >= 0.80,
        "floor_G": floor_scores["f8_genius"],
        "computed_G": genius_score,
        "coherence": coherence,
        "solution_draft": solution,
        "gamma_synchrony": coherence * genius_score,
        "session_id": session_id,
        "motto": str(motto),
        "motto_output": f"[{motto.stage}] {motto.positive}, {motto.negative} | {motto.meaning}",
    }


def _check_coherence(
    agi_tensor: ConstitutionalTensor,
    sync_output: Dict[str, Any],
) -> float:
    """Check internal consistency of merged outputs."""
    # Simple coherence: agreement between AGI and ASI
    agi_truth = agi_tensor.truth_score
    asi_care = sync_output["floor_scores"]["f6_empathy"]
    
    # Coherence is inverse of disagreement
    disagreement = abs(agi_truth - asi_care)
    coherence = 1.0 - disagreement
    
    return max(0.0, min(1.0, coherence))


def _generate_solution(
    agi_tensor: ConstitutionalTensor,
    sync_output: Dict[str, Any],
) -> str:
    """Generate solution draft from synthesis."""
    w3 = sync_output["W_3"]
    
    if w3 >= 0.95:
        return "Solution: High confidence synthesis approved."
    elif w3 >= 0.85:
        return "Solution: Proceed with caution (partial confidence)."
    else:
        return "Solution: Insufficient confidence for synthesis."


# =============================================================================
# 5-FOLD FORGE MOTTOS — G-Level Labeling System
# =============================================================================

THE_5_MOTTOS = {
    "foundation": ("DITEMPA", "BUKAN DIBERI"),
    "akal":       ("DIKAJI", "BUKAN DISUAPI"),
    "present":    ("DIHADAPI", "BUKAN DITANGGUHI"),
    "explore":    ("DIJELAJAH", "BUKAN DISEKATI"),
    "energy":     ("DIUSAHAKAN", "BUKAN DIHARAPI"),
}

def get_g_level_label(g_score: float) -> dict:
    """
    Convert G score to labeled genius level with 5-Fold Forge mottos.
    
    Returns dict with:
    - level: Numeric G-Level (0-5)
    - label: Human-readable label
    - motto: The 5-fold forge chant
    - chant: Rhythmic declaration
    """
    if g_score >= 0.95:
        return {
            "level": 5,
            "label": "PEAK GENIUS",
            "motto": "All 5 mottos honored",
            "chant": "DITEMPA, DIKAJI, DIHADAPI, DIJELAJAH, DIUSAHAKAN — SEAL",
            "negation": "BUKAN DIBERI, BUKAN DISUAPI, BUKAN DITANGGUHI, BUKAN DISEKATI, BUKAN DIHARAPI",
        }
    elif g_score >= 0.90:
        return {
            "level": 4,
            "label": "MASTER GENIUS",
            "motto": "5-Fold Forge Complete",
            "chant": "DITEMPA, DIKAJI, DIHADAPI, DIJELAJAH, DIUSAHAKAN",
            "negation": "BUKAN DIBERI, BUKAN DISUAPI, BUKAN DITANGGUHI, BUKAN DISEKATI, BUKAN DIHARAPI",
        }
    elif g_score >= 0.80:
        return {
            "level": 3,
            "label": "CERTIFIED GENIUS",
            "motto": "Genius Forged",
            "chant": "DITEMPA, DIKAJI, DIHADAPI, DIJELAJAH, DIUSAHAKAN",
            "negation": "BUKAN DIBERI, BUKAN DISUAPI...",
        }
    elif g_score >= 0.70:
        return {
            "level": 2,
            "label": "EMERGING GENIUS",
            "motto": "Partial Forge — Some Dials Need Work",
            "chant": "DITEMPA... [Partial]",
            "negation": "Some BUKAN still present",
        }
    elif g_score >= 0.50:
        return {
            "level": 1,
            "label": "INITIAL FORGE",
            "motto": "Foundation Laid — Continue Forging",
            "chant": "DITEMPA...",
            "negation": "Multiple BUKAN detected",
        }
    else:
        return {
            "level": 0,
            "label": "UNFORGED",
            "motto": "No Genius Without Work",
            "chant": "BUKAN DIBERI, BUKAN DISUAPI, BUKAN DITANGGUHI, BUKAN DISEKATI, BUKAN DIHARAPI",
            "negation": "All negations active — VOID",
        }


def format_apex_output(g_score: float, verdict: str) -> str:
    """
    Format APEX output with 5-Fold Forge labeling.
    
    Example output:
    [G-LEVEL 4: MASTER GENIUS | 0.92]
    DITEMPA, DIKAJI, DIHADAPI, DIJELAJAH, DIUSAHAKAN
    BUKAN DIBERI, BUKAN DISUAPI, BUKAN DITANGGUHI, BUKAN DISEKATI, BUKAN DIHARAPI
    """
    g_info = get_g_level_label(g_score)
    
    lines = [
        f"[G-LEVEL {g_info['level']}: {g_info['label']} | {g_score:.2f}]",
        g_info['chant'],
    ]
    
    if g_info['level'] >= 3:
        lines.append(g_info['negation'])
    
    lines.append(f"Verdict: {verdict}")
    
    return "\n".join(lines)


# =============================================================================
# ACTION 3: JUDGE (Stage 888) — Final Constitutional Verdict
# =============================================================================


async def judge(
    forge_output: Dict[str, Any],
    sync_output: Dict[str, Any],
    asi_output: Dict[str, Any],
    session_id: str,
    require_sovereign: bool = False,
) -> Dict[str, Any]:
    """
    Stage 888: JUDGE — The Soul's Final Verdict
    
    Render constitutional verdict based on all evidence.
    
    Args:
        forge_output: Forge synthesis output
        sync_output: Trinity sync output
        asi_output: ASI alignment output
        session_id: Constitutional session token
        require_sovereign: Whether this needs 888 sovereign approval
    
    Returns:
        Dict with:
        - verdict: SEAL / VOID / PARTIAL / SABAR / 888_HOLD
        - W_3: Tri-Witness score
        - genius_G: Genius score
        - floors_failed: List of failed floors
        - justification: Explanation of verdict
    
    Action Chain:
        forge → judge → vault.seal (completes pipeline)
    """
    violations = []
    justifications = []
    
    # F3: Tri-Witness
    w3 = sync_output["W_3"]
    if w3 < 0.95:
        violations.append("F3")
        justifications.append(f"Tri-Witness {w3:.3f} < 0.95")
    
    # F8: Genius
    g_score = forge_output["genius_G"]
    if g_score < 0.80:
        violations.append("F8")
        justifications.append(f"Genius {g_score:.3f} < 0.80")
    
    # F9: Anti-Hantu (placeholder - real detection in guards)
    c_dark = 0.0  # Would come from detect_hantu()
    if c_dark > 0.30:
        violations.append("F9")
        justifications.append("Ghost claim detected")
    
    # F10: Ontology (placeholder)
    f10_pass = True
    if not f10_pass:
        violations.append("F10")
        justifications.append("Ontology violation")
    
    # F13: Sovereign override
    if require_sovereign:
        verdict = "888_HOLD"
        justification = "Requires sovereign approval (F13)"
    elif not violations:
        verdict = "SEAL"
        justification = "All constitutional floors pass"
    elif len(violations) == 1 and violations[0] == "F8":
        verdict = "SABAR"
        justification = "Genius below threshold — cooling recommended"
    elif len(violations) <= 2:
        verdict = "PARTIAL"
        justification = "; ".join(justifications)
    else:
        verdict = "VOID"
        justification = "Multiple floor violations: " + "; ".join(justifications)
    
    # Generate 5-Fold Forge labeling
    g_level = get_g_level_label(g_score)
    apex_output_label = format_apex_output(g_score, verdict)
    
    # Get 888_JUDGE motto: DISEDARKAN, BUKAN DIYAKINKAN
    motto = get_motto_for_stage("888_JUDGE")
    all_mottos = get_all_stage_mottos()
    mottos = [f"[{m.stage}] {m.positive}, {m.negative} | {m.meaning}" for m in all_mottos]
    mottos_output = format_all_stage_mottos()
    
    return {
        "stage": 888,
        "action": "judge",
        "verdict": verdict,
        "W_3": w3,
        "genius_G": g_score,
        "g_level": g_level["level"],
        "g_label": g_level["label"],
        "g_motto": g_level["motto"],
        "g_chant": g_level["chant"],
        "g_negation": g_level["negation"],
        "apex_output": apex_output_label,  # Full formatted output with mottos
        "floors_passed": ["F3", "F8", "F9", "F10"] if not violations else [],
        "floors_failed": violations,
        "justification": justification,
        "requires_sovereign": require_sovereign,
        "session_id": session_id,
        "motto": str(motto),
        "motto_output": f"[{motto.stage}] {motto.positive}, {motto.negative} | {motto.meaning}",
        "mottos": mottos,
        "mottos_output": mottos_output,
        # 5-Fold Forge mottos for AAA MCP labeling
        "_5_fold_forge": {
            "foundation": "DITEMPA, BUKAN DIBERI",
            "akal": "DIKAJI, BUKAN DISUAPI",
            "present": "DIHADAPI, BUKAN DITANGGUHI",
            "explore": "DIJELAJAH, BUKAN DISEKATI",
            "energy": "DIUSAHAKAN, BUKAN DIHARAPI",
            "rhythmic_declaration": "DITEMPA, DIKAJI, DIHADAPI, DIJELAJAH, DIUSAHAKAN",
            "negation_chant": "BUKAN DIBERI, BUKAN DISUAPI, BUKAN DITANGGUHI, BUKAN DISEKATI, BUKAN DIHARAPI",
        },
    }


# =============================================================================
# UNIFIED APEX INTERFACE
# =============================================================================


async def apex(
    agi_tensor: ConstitutionalTensor,
    asi_output: Dict[str, Any],
    session_id: str,
    action: str = "full",
    require_sovereign: bool = False,
) -> Dict[str, Any]:
    """
    Unified APEX interface — The Soul in action.
    
    Args:
        agi_tensor: AGI Mind output
        asi_output: ASI Heart output
        session_id: Constitutional session token
        action: Which action ("sync", "forge", "judge", "full")
        require_sovereign: Whether to trigger F13
    
    Returns:
        Action output or complete judgment
    
    Example:
        >>> result = await apex(tensor, asi_out, session, action="full")
        >>> result["verdict"]
        'SEAL'
    """
    if action == "sync":
        return await sync(agi_tensor, asi_output, session_id)
    
    elif action == "forge":
        sync_out = await sync(agi_tensor, asi_output, session_id)
        return await forge(sync_out, agi_tensor, session_id)
    
    elif action == "judge":
        sync_out = await sync(agi_tensor, asi_output, session_id)
        forge_out = await forge(sync_out, agi_tensor, session_id)
        return await judge(forge_out, sync_out, asi_output, session_id, require_sovereign)
    
    elif action == "full":
        # Get APEX mottos
        motto_444 = get_motto_for_stage("444_SYNC")
        motto_777 = get_motto_for_stage("777_FORGE")
        motto_888 = get_motto_for_stage("888_JUDGE")
        all_mottos = get_all_stage_mottos()
        mottos = [f"[{m.stage}] {m.positive}, {m.negative} | {m.meaning}" for m in all_mottos]
        mottos_output = format_all_stage_mottos()
        
        # Complete APEX pipeline
        sync_out = await sync(agi_tensor, asi_output, session_id)
        forge_out = await forge(sync_out, agi_tensor, session_id)
        judge_out = await judge(forge_out, sync_out, asi_output, session_id, require_sovereign)
        
        return {
            "stage": 888,
            "action": "judge",
            "sync": sync_out,
            "forge": forge_out,
            "judge": judge_out,
            "verdict": judge_out["verdict"],
            "W_3": judge_out["W_3"],
            "genius_G": judge_out["genius_G"],
            "floors_failed": judge_out["floors_failed"],
            "justification": judge_out["justification"],
            "session_id": session_id,
            "motto_444": str(motto_444),
            "motto_777": str(motto_777),
            "motto_888": str(motto_888),
            "motto_output": f"APEX: [{motto_444.stage}] {motto_444.positive} -> [{motto_777.stage}] {motto_777.positive} -> [{motto_888.stage}] {motto_888.positive}",
            "mottos": mottos,
            "mottos_output": mottos_output,
        }
    
    else:
        raise ValueError(f"Unknown action: {action}. Use: sync, forge, judge, full")


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Actions (3 max)
    "sync",    # Stage 444: Trinity merge
    "forge",   # Stage 777: Phase transition
    "judge",   # Stage 888: Final verdict
    
    # Unified interface
    "apex",
]
