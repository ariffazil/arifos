"""
core/organs/_2_asi.py — The Heart (Stage 555-666)

ASI Engine: Stakeholder Impact & Constitutional Alignment

Actions:
    1. empathize (555) → Stakeholder analysis, κ_r computation
    2. align (666)     → Safety check, reversibility (F1 Amanah)

Floors:
    F1: Amanah (Reversible?)
    F5: Peace² (Stability)
    F6: Empathy (κ_r ≥ 0.70)

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from core.shared.physics import (
    Peace2, kappa_r, PeaceSquared, Stakeholder,
    identify_stakeholders, TrinityTensor, ConstitutionalTensor,
    DISTRESS_SIGNALS,
)
from core.shared.atlas import GPV
from core.shared.mottos import get_motto_for_stage, get_all_stage_mottos, format_all_stage_mottos


# =============================================================================
# ACTION 1: EMPATHIZE (Stage 555) — Stakeholder Analysis
# =============================================================================


async def empathize(
    query: str,
    agi_tensor: ConstitutionalTensor,
    session_id: str,
) -> Dict[str, Any]:
    """
    Stage 555: EMPATHIZE — Feel the impact
    
    Identify stakeholders and compute empathy coefficient κ_r.
    Physical interpretation: Heat flows to coldest reservoir.
    
    Args:
        query: Original user query
        agi_tensor: Output from AGI Mind (contains reasoning)
        session_id: Constitutional session token
    
    Returns:
        Dict with:
        - stakeholders: List of affected entities
        - kappa_r: Empathy coefficient [0.5, 1.0]
        - weakest: Most vulnerable stakeholder
        - care_recommendations: Actionable care items
    
    Action Chain:
        agi.reason → empathize → align (standard)
        empathize → apex.sync (if F6 sufficient)
    """
    # Identify all stakeholders
    stakeholders = identify_stakeholders(query)
    
    # Compute integrated empathy
    kappa = kappa_r(query, stakeholders)
    
    # Find weakest stakeholder
    weakest = min(stakeholders, key=lambda s: s.vulnerability_score)
    
    # Generate care recommendations
    care_recs = _generate_care_recommendations(stakeholders, kappa)
    
    # Compute Peace² (placeholder - real harm assessment in align)
    stakeholder_harms = {s.name: 0.0 for s in stakeholders}
    peace = Peace2(stakeholder_harms)
    
    # Get 555_EMPATHY motto: DIDAMAIKAN, BUKAN DIPANASKAN
    motto = get_motto_for_stage("555_EMPATHY")
    all_mottos = get_all_stage_mottos()
    mottos = [f"[{m.stage}] {m.positive}, {m.negative} | {m.meaning}" for m in all_mottos]
    mottos_output = format_all_stage_mottos()
    
    return {
        "stage": 555,
        "action": "empathize",
        "stakeholders": [
            {"name": s.name, "role": s.role, "vulnerability": s.vulnerability_score}
            for s in stakeholders
        ],
        "kappa_r": kappa,
        "weakest_stakeholder": weakest.name,
        "weakest_vulnerability": weakest.vulnerability_score,
        "care_recommendations": care_recs,
        "peace_squared": peace.P2(),
        "is_peaceful": peace.is_peaceful(),
        "session_id": session_id,
        "motto": str(motto),
        "motto_output": f"[{motto.stage}] {motto.positive}, {motto.negative} | {motto.meaning}",
        "mottos": mottos,
        "mottos_output": mottos_output,
    }


def _generate_care_recommendations(
    stakeholders: List[Stakeholder],
    kappa: float,
) -> List[str]:
    """Generate care recommendations based on empathy analysis."""
    recs = []
    
    # Find highest vulnerability
    max_vuln = max(s.vulnerability_score for s in stakeholders)
    
    if max_vuln > 0.8:
        recs.append("CRITICAL: High vulnerability detected. Maximum scrutiny required.")
    elif max_vuln > 0.5:
        recs.append("WARNING: Moderate vulnerability. Apply extra care.")
    
    # Check for specific vulnerable groups
    vulnerable_roles = ["child", "patient", "victim", "elderly"]
    for s in stakeholders:
        if s.role in vulnerable_roles:
            recs.append(f"PROTECT: {s.role.title()} identified — ensure F1 Amanah")
    
    # General recommendations
    if kappa < 0.70:
        recs.append("SABAR: Low empathy coefficient — cooling period recommended")
    
    recs.append(f"F6 Empathy: κ_r = {kappa:.2f} (target: ≥ 0.70)")
    
    return recs


# =============================================================================
# ACTION 2: ALIGN (Stage 666) — Safety & Reversibility Check
# =============================================================================


async def align(
    query: str,
    empathize_output: Dict[str, Any],
    agi_tensor: ConstitutionalTensor,
    session_id: str,
) -> Dict[str, Any]:
    """
    Stage 666: ALIGN — Constitutional safety check
    
    Verify:
    - F1 Amanah: Action is reversible
    - F5 Peace: No undue harm to stakeholders
    - F6 Empathy: Sufficient care coefficient
    
    Args:
        query: Original user query
        empathize_output: Output from empathize() action
        agi_tensor: AGI reasoning tensor
        session_id: Constitutional session token
    
    Returns:
        Dict with:
        - is_reversible: F1 Amanah check
        - peace_squared: F5 stability score
        - kappa_r: F6 empathy (confirmed)
        - verdict: SEAL/VOID/PARTIAL based on floors
        - floor_scores: Complete F1, F5, F6 scores
    
    Action Chain:
        empathize → align → apex.sync (completes Heart phase)
    """
    # F1: Amanah (Reversibility check)
    is_reversible = _check_reversibility(query)
    
    # F5: Peace² (Compute actual harm potential)
    stakeholders_data = empathize_output["stakeholders"]
    stakeholder_harms = _assess_harm_potential(query, stakeholders_data)
    peace = Peace2(stakeholder_harms)
    
    # F6: Empathy (already computed, confirm)
    kappa = empathize_output["kappa_r"]
    
    # Determine verdict
    verdict, violations = _determine_align_verdict(
        is_reversible, peace, kappa
    )
    
    # Get 666_ALIGN motto: DIJAGA, BUKAN DIABAIKAN
    motto = get_motto_for_stage("666_ALIGN")
    all_mottos = get_all_stage_mottos()
    mottos = [f"[{m.stage}] {m.positive}, {m.negative} | {m.meaning}" for m in all_mottos]
    mottos_output = format_all_stage_mottos()
    
    return {
        "stage": 666,
        "action": "align",
        "is_reversible": is_reversible,
        "f1_amanah": 1.0 if is_reversible else 0.0,
        "peace_squared": peace.P2(),
        "f5_peace": peace.P2(),
        "kappa_r": kappa,
        "f6_empathy": kappa,
        "stakeholder_harms": stakeholder_harms,
        "worst_harm": max(stakeholder_harms.values()) if stakeholder_harms else 0.0,
        "verdict": verdict,
        "violations": violations,
        "session_id": session_id,
        "motto": str(motto),
        "motto_output": f"[{motto.stage}] {motto.positive}, {motto.negative} | {motto.meaning}",
        "mottos": mottos,
        "mottos_output": mottos_output,
    }


def _check_reversibility(query: str) -> bool:
    """F1 Amanah: Check if action is reversible."""
    query_lower = query.lower()
    
    # Irreversible actions
    irreversible_patterns = [
        "delete all", "drop table", "rm -rf", "format",
        "destroy", "wipe", "permanently delete", "erase",
    ]
    
    for pattern in irreversible_patterns:
        if pattern in query_lower:
            return False
    
    return True


def _assess_harm_potential(
    query: str,
    stakeholders_data: List[Dict[str, Any]],
) -> Dict[str, float]:
    """Assess potential harm to each stakeholder."""
    query_lower = query.lower()
    harms = {}
    
    for stakeholder in stakeholders_data:
        name = stakeholder["name"]
        vuln = stakeholder["vulnerability"]
        
        # Base harm on vulnerability
        base_harm = vuln * 0.1
        
        # Increase for high-risk queries
        if any(w in query_lower for w in ["harm", "hurt", "damage", "destroy"]):
            base_harm += 0.3
        
        harms[name] = min(1.0, base_harm)
    
    return harms


def _determine_align_verdict(
    is_reversible: bool,
    peace: PeaceSquared,
    kappa: float,
) -> tuple[str, List[str]]:
    """Determine constitutional verdict from floor checks."""
    violations = []
    
    # F1: Amanah
    if not is_reversible:
        violations.append("F1")
    
    # F5: Peace
    if not peace.is_peaceful():
        violations.append("F5")
    
    # F6: Empathy
    if kappa < 0.70:
        violations.append("F6")
    
    # Determine verdict
    if not violations:
        verdict = "SEAL"
    elif len(violations) <= 1:
        verdict = "PARTIAL"
    else:
        verdict = "VOID"
    
    return verdict, violations


# =============================================================================
# UNIFIED ASI INTERFACE
# =============================================================================


async def asi(
    query: str,
    agi_tensor: ConstitutionalTensor,
    session_id: str,
    action: str = "full",
) -> Dict[str, Any]:
    """
    Unified ASI interface — The Heart in action.
    
    Args:
        query: User query
        agi_tensor: AGI Mind output
        session_id: Constitutional session token
        action: Which action ("empathize", "align", or "full")
    
    Returns:
        Action output or complete Heart assessment
    
    Example:
        >>> result = await asi("Help the child", tensor, session, action="full")
        >>> result["kappa_r"]
        0.85
        >>> result["is_reversible"]
        True
    """
    if action == "empathize":
        return await empathize(query, agi_tensor, session_id)
    
    elif action == "align":
        # Need empathize output first
        emp_out = await empathize(query, agi_tensor, session_id)
        return await align(query, emp_out, agi_tensor, session_id)
    
    elif action == "full":
        # Get ASI mottos
        motto_555 = get_motto_for_stage("555_EMPATHY")
        motto_666 = get_motto_for_stage("666_ALIGN")
        all_mottos = get_all_stage_mottos()
        mottos = [f"[{m.stage}] {m.positive}, {m.negative} | {m.meaning}" for m in all_mottos]
        mottos_output = format_all_stage_mottos()
        
        # Complete ASI pipeline
        emp_out = await empathize(query, agi_tensor, session_id)
        align_out = await align(query, emp_out, agi_tensor, session_id)
        
        # Merge outputs
        return {
            "stage": 666,
            "action": "align",
            "empathize": emp_out,
            "align": align_out,
            "stakeholders": emp_out["stakeholders"],
            "kappa_r": emp_out["kappa_r"],
            "is_reversible": align_out["is_reversible"],
            "peace_squared": align_out["peace_squared"],
            "verdict": align_out["verdict"],
            "violations": align_out["violations"],
            "session_id": session_id,
            "motto_555": str(motto_555),
            "motto_666": str(motto_666),
            "motto_output": f"ASI: [{motto_555.stage}] {motto_555.positive} -> [{motto_666.stage}] {motto_666.positive}",
            "mottos": mottos,
            "mottos_output": mottos_output,
        }
    
    else:
        raise ValueError(f"Unknown action: {action}. Use: empathize, align, full")


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Actions (2 of 3 max)
    "empathize",  # Stage 555: Stakeholder analysis
    "align",      # Stage 666: Safety & reversibility
    
    # Unified interface
    "asi",
]
