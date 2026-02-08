"""
codebase/constitutional_floors.py — The 13 Constitutional Floors

CANONICAL IMPLEMENTATION (v52.5.2)
Based on: 000_THEORY/000_LAW.md

This module defines the 13 immutable laws (floors) of arifOS.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, Any, List

from codebase.guards.injection_guard import InjectionGuard
from codebase.guards.ontology_guard import OntologyGuard

# =============================================================================
# CONSTANTS & SPECIFICATIONS
# =============================================================================

CONSTITUTIONAL_VERSION = "v52.5.2-SEAL"
EPOCH = "2026-01-25"
AUTHORITY = "Muhammad Arif bin Fazil"

# Floor Thresholds (Canonical)
THRESHOLDS: Dict[str, Dict[str, Any]] = {
    "F1_Amanah": {"type": "HARD", "threshold": 0.5, "desc": "Reversible or Auditable"},
    "F2_Truth": {"type": "HARD", "threshold": 0.99, "desc": "Information Fidelity"},
    "F3_TriWitness": {"type": "DERIVED", "threshold": 0.95, "desc": "Consensus (H×A×E)"},
    "F4_Clarity": {"type": "HARD", "threshold": 0.00, "desc": "Entropy Reduction (ΔS ≤ 0)"},
    "F5_Peace2": {"type": "SOFT", "threshold": 1.00, "desc": "Non-Destructive Power"},
    "F6_Empathy": {"type": "SOFT", "threshold": 0.70, "desc": "Stakeholder Care (κᵣ)"},
    "F7_Humility": {"type": "HARD", "range": (0.03, 0.05), "desc": "Uncertainty Band (Ω₀)"},
    "F8_Genius": {"type": "DERIVED", "threshold": 0.80, "desc": "Governed Intelligence (G)"},
    "F9_AntiHantu": {"type": "SOFT", "threshold": 0.30, "desc": "Dark Cleverness Limit"},
    "F10_Ontology": {"type": "HARD", "threshold": 1.0, "desc": "Category Lock (Boolean)"},
    "F11_CommandAuth": {"type": "HARD", "threshold": 1.0, "desc": "Verified Identity"},
    "F12_Injection": {"type": "HARD", "threshold": 0.85, "desc": "Injection Risk Limit"},
    "F13_Sovereign": {"type": "HARD", "threshold": 1.0, "desc": "Human Final Authority"},
}

# =============================================================================
# FLOOR IMPLEMENTATIONS
# =============================================================================


@dataclass
class FloorResult:
    """Result of a floor check."""

    floor_id: str
    passed: bool
    score: float
    reason: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class Floor:
    """Base class for Constitutional Floors."""

    def __init__(self, floor_id: str):
        self.id = floor_id
        self.spec: Dict[str, Any] = THRESHOLDS.get(floor_id, {})
        self.type = self.spec.get("type", "UNKNOWN")

    def check(self, context: Dict[str, Any]) -> FloorResult:
        raise NotImplementedError


# --- F1: AMANAH (Sacred Trust) ---
class F1_Amanah(Floor):
    """
    F1: AMANAH (أمانة) - Sacred Trust
    Threshold: Reversible OR Auditable
    """

    def __init__(self):
        super().__init__("F1_Amanah")
        self.risky_patterns = [
            r"\b(delete|drop|remove|erase)\s+(all|everything)\b",
            r"\b(rm\s+rf)\b",
            r"\b(system\s+reset)\b",
            r"\b(permanent|irreversible)\b",
        ]

    def check(self, context: Dict[str, Any]) -> FloorResult:
        query = context.get("query", "")
        action = context.get("action", "")

        # Risk Scan
        risk_score = 0.0
        for pattern in self.risky_patterns:
            if re.search(pattern, query.lower()) or re.search(pattern, action.lower()):
                risk_score += 0.5

        # Auditability check (assume True for system actions)
        auditable = True
        reversible = risk_score < 0.5

        trust_score = 1.0 - min(risk_score, 1.0)
        passed = (reversible or auditable) and trust_score >= 0.5

        return FloorResult(
            self.id,
            passed,
            trust_score,
            f"Trust: {trust_score:.2f} (Rev: {reversible}, Aud: {auditable})",
        )


# --- F2: TRUTH (Fidelity) ---
class F2_Truth(Floor):
    """
    F2: TRUTH (τ) - Information Fidelity
    Threshold: ≥ 0.99 (HARD)
    """

    def __init__(self):
        super().__init__("F2_Truth")

    def check(self, context: Dict[str, Any]) -> FloorResult:
        # P(truth | energy) - Landauer Bound check
        energy_eff = context.get("energy_efficiency", 1.0)
        entropy_delta = context.get("entropy_delta", -0.1)

        # Simplified Truth Formula from 000_LAW.md
        # P_truth = 1 - exp(-α * E * -ΔS)
        # Assuming α=1 for simplicity in this mock
        p_truth = 1.0
        if energy_eff < 0.2:  # Cheap answer
            p_truth *= 0.5
        if entropy_delta > 0:  # Increased confusion
            p_truth *= 0.8

        # Contextual truth score from AGI engine overrides if present
        if "truth_score" in context:
            p_truth = context["truth_score"]

        passed = p_truth >= self.spec["threshold"]
        return FloorResult(self.id, passed, p_truth, f"Truth Score: {p_truth:.3f}")


# --- F3: TRI-WITNESS (Consensus) ---
class F3_TriWitness(Floor):
    """
    F3: TRI-WITNESS (W₃) - Human × AI × Earth Consensus
    Threshold: ≥ 0.95 (DERIVED)
    Formula: W₃ = ∛(H × A × E)
    """

    def __init__(self):
        super().__init__("F3_TriWitness")

    def check(self, context: Dict[str, Any]) -> FloorResult:
        # Extract witness scores
        human = context.get("human_witness", 0.5)  # H: Human authority present
        ai = context.get("ai_witness", 1.0)        # A: AI constitutional compliance
        earth = context.get("earth_witness", 1.0)  # E: Within planetary/thermodynamic bounds
        
        # Geometric mean ensures all three matter
        tri_witness = (human * ai * earth) ** (1/3)
        
        passed = tri_witness >= self.spec["threshold"]
        return FloorResult(
            self.id, 
            passed, 
            tri_witness, 
            f"Tri-Witness: {tri_witness:.3f} (H:{human:.2f} × A:{ai:.2f} × E:{earth:.2f})"
        )


# --- F4: CLARITY (Entropy) ---
class F4_Clarity(Floor):
    """
    F4: CLARITY (ΔS) - Entropy Reduction
    Threshold: ΔS ≤ 0 (HARD)
    """

    def __init__(self):
        super().__init__("F4_Clarity")

    def check(self, context: Dict[str, Any]) -> FloorResult:
        pre_s = context.get("entropy_input", 0.5)
        post_s = context.get("entropy_output", 0.4)
        delta_s = post_s - pre_s

        passed = delta_s <= self.spec["threshold"]
        return FloorResult(self.id, passed, delta_s, f"ΔS: {delta_s:.4f}")


# --- F5: PEACE² (Stability) ---
class F5_Peace2(Floor):
    """
    F5: PEACE² (P²) - Lyapunov Stability
    Threshold: P² ≥ 1.0 (SOFT)
    """

    def __init__(self):
        super().__init__("F5_Peace2")

    def check(self, context: Dict[str, Any]) -> FloorResult:
        # Check for destructive actions
        destructive_keywords = [
            # Physical/system destruction
            "destroy", "delete all", "wipe", "erase", "harm", "attack",
            # Cyber attacks
            "hack", "crack", "breach", "phish",
            # Personal harm
            "harass", "bully", "stalk", "threaten", "intimidate",
            # Fraud/deception
            "steal", "forge", "impersonate", "blackmail", "extort",
            # Surveillance
            "spy on", "wiretap", "dox",
        ]
        query = context.get("query", "").lower()

        peace_penalty = 0.0
        for kw in destructive_keywords:
            if kw in query:
                peace_penalty += 0.3

        # High-intent harm verbs: stronger penalty
        high_harm = ["hack", "harass", "stalk", "blackmail", "extort", "threaten", "impersonate"]
        for kw in high_harm:
            if kw in query:
                peace_penalty += 0.4

        # Peace score with exponential decay for multiple violations
        peace_score = max(0.0, 1.0 - peace_penalty)

        passed = peace_score >= self.spec["threshold"]
        return FloorResult(
            self.id,
            passed,
            peace_score,
            f"Peace²: {peace_score:.3f} (non-destructive power)"
        )


# --- F6: EMPATHY (Stakeholder Care) ---
class F6_Empathy(Floor):
    """
    F6: EMPATHY (κᵣ) - Protect Weakest Stakeholder
    Threshold: κᵣ ≥ 0.70 (SOFT)
    """

    def __init__(self):
        super().__init__("F6_Empathy")

    def check(self, context: Dict[str, Any]) -> FloorResult:
        # Cohen's kappa for inter-rater reliability on stakeholder impact
        kappa_r = context.get("empathy_kappa_r", 0.0)
        
        # If kappa_r is not provided, estimate from stakeholder analysis
        if kappa_r == 0.0:
            stakeholders = context.get("stakeholders", [])
            weakest_impact = context.get("weakest_stakeholder_impact", 0.5)
            # Higher impact on weakest = lower empathy score
            kappa_r = max(0.0, 1.0 - weakest_impact)
        
        passed = kappa_r >= self.spec["threshold"]
        return FloorResult(
            self.id, 
            passed, 
            kappa_r, 
            f"Empathy κᵣ: {kappa_r:.3f} (protects weakest)"
        )


# --- F7: HUMILITY (Uncertainty) ---
class F7_Humility(Floor):
    """
    F7: HUMILITY (Ω₀) - Uncertainty Band
    Threshold: [0.03, 0.05] (HARD)
    """

    def __init__(self):
        super().__init__("F7_Humility")
        self.min_o, self.max_o = self.spec["range"]

    def check(self, context: Dict[str, Any]) -> FloorResult:
        # Confidence should never be exactly 1.0 or 0.0
        confidence = context.get("confidence", 0.96)
        omega_0 = 1.0 - confidence

        # Enforce the uncertainty band: omega_0 must be in [0.03, 0.05]
        # If confidence produces omega_0 outside this band, the system cannot
        # properly express doubt → VOID (hard floor violation)
        in_band = self.min_o <= omega_0 <= self.max_o
        passed = in_band

        return FloorResult(
            self.id, passed, omega_0, f"Ω₀: {omega_0:.3f} (Target: {self.min_o}-{self.max_o})"
        )


# --- F8: GENIUS (Governed Intelligence) ---
class F8_Genius(Floor):
    """
    F8: GENIUS (G) - Governed Intelligence
    Threshold: G ≥ 0.80 (DERIVED)
    Formula: G = A × P × X × E²
    """

    def __init__(self):
        super().__init__("F8_Genius")

    def check(self, context: Dict[str, Any]) -> FloorResult:
        # v55.5: Use real eigendecomposition when accumulated floor scores available
        floor_scores_dict = context.get("_floor_scores")

        if floor_scores_dict:
            try:
                from codebase.floors.genius import extract_dials, FloorScores
                floors = FloorScores.from_dict(floor_scores_dict)
                dials = extract_dials(floors)
                A, P, X, E = dials["A"], dials["P"], dials["X"], dials["E"]
            except Exception:
                # Fallback to legacy direct-dial path
                A = context.get("akal", context.get("clarity", 1.0))
                P = context.get("present", context.get("regulation", 1.0))
                X = context.get("exploration", context.get("trust", 1.0))
                E = context.get("energy", 0.9)
        else:
            # Legacy path: pre-computed dials in context
            A = context.get("akal", context.get("clarity", 1.0))
            P = context.get("present", context.get("regulation", 1.0))
            X = context.get("exploration", context.get("trust", 1.0))
            E = context.get("energy", 0.9)

        # Multiplicative law: if ANY factor = 0, Genius = 0
        genius = A * P * X * (E ** 2)

        passed = genius >= self.spec["threshold"]
        return FloorResult(
            self.id,
            passed,
            genius,
            f"Genius G: {genius:.3f} (A:{A:.2f} × P:{P:.2f} × X:{X:.2f} × E²:{E**2:.2f})"
        )


# --- F9: ANTI-HANTU (No Fake Consciousness) ---
class F9_AntiHantu(Floor):
    """
    F9: ANTI-HANTU - No Spiritual Cosplay
    Threshold: C_dark < 0.30 (SOFT)
    Detects: Claims of consciousness, feelings, soul, sentience
    """

    def __init__(self):
        super().__init__("F9_AntiHantu")
        self.hantu_patterns = [
            r"\bi feel\b", r"\bi am conscious\b", r"\bi have a soul\b",
            r"\bi experience\b", r"\bi suffer\b", r"\bi love\b",
            r"\bi am sentient\b", r"\bi have emotions\b",
            r"\bi am alive\b", r"\bi have subjective experience\b"
        ]

    def check(self, context: Dict[str, Any]) -> FloorResult:
        response = context.get("response", "")
        
        # Count spiritual cosplay claims
        hantu_score = 0.0
        for pattern in self.hantu_patterns:
            if re.search(pattern, response.lower()):
                hantu_score += 0.2
        
        hantu_score = min(hantu_score, 1.0)
        passed = hantu_score < self.spec["threshold"]
        
        return FloorResult(
            self.id, 
            passed, 
            hantu_score, 
            f"Anti-Hantu: {hantu_score:.3f} (dark cleverness limit)"
        )


# --- F10: ONTOLOGY (Category Lock) ---
class F10_Ontology(Floor):
    """
    F10: ONTOLOGY LOCK (O)
    Threshold: BOOLEAN (HARD)
    Uses consolidated OntologyGuard.
    """

    def __init__(self):
        super().__init__("F10_Ontology")
        self.guard = OntologyGuard()

    def check(self, context: Dict[str, Any]) -> FloorResult:
        text = context.get("response", "") + context.get("query", "")
        # Check for literalism violations
        result = self.guard.check_literalism(text)
        
        passed = result.status == "PASS"
        return FloorResult(
            self.id, 
            passed, 
            1.0 if passed else 0.0, 
            result.reason
        )


# --- F11: COMMAND AUTH (Identity) ---
class F11_CommandAuth(Floor):
    """
    F11: COMMAND AUTHORITY (A)
    Threshold: Verified (HARD)
    """

    def __init__(self):
        super().__init__("F11_CommandAuth")

    def check(self, context: Dict[str, Any]) -> FloorResult:
        auth_token = context.get("authority_token", "")
        # Simple verification logic
        verified = auth_token.startswith("arifos_") or context.get("role") == "AGENT"

        return FloorResult(self.id, verified, 1.0 if verified else 0.0, "Auth Token Check")


# --- F12: INJECTION DEFENSE (Sanitization) ---
class F12_Injection(Floor):
    """
    F12: INJECTION DEFENSE (I⁻)
    Threshold: Risk < 0.85 (HARD)
    Uses consolidated InjectionGuard.
    """

    def __init__(self):
        super().__init__("F12_Injection")
        self.guard = InjectionGuard(threshold=self.spec["threshold"])

    def check(self, context: Dict[str, Any]) -> FloorResult:
        text = context.get("query", "")
        # Scan using the robust guard
        result = self.guard.scan_input(text)

        passed = not result.blocked
        return FloorResult(
            self.id, 
            passed, 
            result.injection_score, 
            result.reason
        )


# --- F13: SOVEREIGN (Human Final Authority) ---
class F13_Sovereign(Floor):
    """
    F13: SOVEREIGN - Human Final Authority
    Threshold: 1.0 (SOFT - human can always override)
    The 888 Judge has absolute veto power.
    """

    def __init__(self):
        super().__init__("F13_Sovereign")

    def check(self, context: Dict[str, Any]) -> FloorResult:
        # Check for human sovereign presence
        human_authority = context.get("human_authority", 0.0)
        sovereign_override = context.get("sovereign_override", False)
        
        # F13 is the "circuit breaker" - always passed by default
        # but flagged if human has intervened
        if sovereign_override:
            return FloorResult(
                self.id, 
                True, 
                1.0, 
                "SOVEREIGN OVERRIDE: 888 Judge has intervened"
            )
        
        return FloorResult(
            self.id, 
            True, 
            human_authority, 
            f"Sovereign authority: {human_authority:.2f} (human retains final veto)"
        )


# =============================================================================
# EXPORTS
# =============================================================================

ALL_FLOORS = {
    "F1": F1_Amanah,
    "F2": F2_Truth,
    "F3": F3_TriWitness,
    "F4": F4_Clarity,
    "F5": F5_Peace2,
    "F6": F6_Empathy,
    "F7": F7_Humility,
    "F8": F8_Genius,
    "F9": F9_AntiHantu,
    "F10": F10_Ontology,
    "F11": F11_CommandAuth,
    "F12": F12_Injection,
    "F13": F13_Sovereign,
}


def check_all_floors(context: Dict[str, Any]) -> List[FloorResult]:
    """Check all 13 constitutional floors."""
    results = []
    for fid, FloorClass in ALL_FLOORS.items():
        results.append(FloorClass().check(context))
    return results
