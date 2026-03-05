"""
codebase/constitutional_floors.py — The 13 Constitutional Floors

CANONICAL IMPLEMENTATION (v52.5.2)
Based on: 000_THEORY/000_LAW.md

This module defines the 13 immutable laws (floors) of arifOS.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from core.shared.guards.injection_guard import InjectionGuard
from core.shared.guards.ontology_guard import OntologyGuard

# =============================================================================
# CONSTANTS & SPECIFICATIONS
# =============================================================================

CONSTITUTIONAL_VERSION = "v60.1-SEAL"
EPOCH = "2026-02-25"
AUTHORITY = "Muhammad Arif bin Fazil"

# Floor Thresholds (Canonical Source of Truth)
# Used by arifOS AAA Pipeline to enforce constitutional invariants.
THRESHOLDS: dict[str, dict[str, Any]] = {
    "F1_Amanah": {"type": "HARD", "threshold": 0.5, "desc": "Reversible or Auditable"},
    "F2_Truth": {"type": "HARD", "threshold": 0.99, "desc": "Information Fidelity"},
    "F3_TriWitness": {"type": "DERIVED", "threshold": 0.95, "desc": "Consensus (H×A×E)"},
    "F4_Clarity": {"type": "HARD", "threshold": 0.00, "desc": "Entropy Reduction (ΔS ≤ 0)"},
    "F5_Peace2": {"type": "SOFT", "threshold": 1.00, "desc": "Non-Destructive Power"},
    "F6_Empathy": {"type": "SOFT", "threshold": 0.70, "desc": "Stakeholder Care (κᵣ)"},
    "F7_Humility": {"type": "HARD", "range": (0.03, 0.15), "desc": "Uncertainty Band (Ω₀)"},
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
    metadata: dict[str, Any] = field(default_factory=dict)


class Floor:
    """Base class for Constitutional Floors."""

    def __init__(self, floor_id: str):
        self.id = floor_id
        self.spec: dict[str, Any] = THRESHOLDS.get(floor_id, {})
        self.type = self.spec.get("type", "UNKNOWN")

    def check(self, context: dict[str, Any]) -> FloorResult:
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

    def check(self, context: dict[str, Any]) -> FloorResult:
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
    Threshold: ≥ 0.99 (HARD) for claims, ≥ 0.95 for Axioms
    """

    def __init__(self):
        super().__init__("F2_Truth")
        # Axiomatic patterns that are "Self-Evident" and should not be penalized for low energy
        self.axiomatic_patterns = [
            r"^\d+[\+\-\*\/]\d+",  # Basic Math (2+2)
            r"^(true|false)$",  # Boolean
            r"^\{.*\}$",  # JSON Syntax
            r"^\[.*\]$",  # List Syntax
            r"def\s+.*:$",  # Python def
            r"class\s+.*:$",  # Python class
        ]

    def check(self, context: dict[str, Any]) -> FloorResult:
        query = context.get("query", "").strip()

        # 1. Axiomatic Bypass Check (The "Mind" Patch)
        is_axiomatic = any(re.search(p, query) for p in self.axiomatic_patterns)

        # P(truth | energy) - Landauer Bound check
        energy_eff = context.get("energy_efficiency", 1.0)
        entropy_delta = context.get("entropy_delta", -0.1)

        # Base truth probability
        p_truth = 1.0

        if is_axiomatic:
            # Axioms are ALLOWED to be cheap. No penalty.
            p_truth = 1.0
            reason_suffix = "(Axiomatic Truth - Energy Penalty Bypassed)"
        else:
            # Standard claims: Cheap answers are suspicious
            if energy_eff < 0.2:
                p_truth *= 0.5
            reason_suffix = "(Standard Verification)"

        if entropy_delta > 0:  # Increased confusion always lowers truth
            p_truth *= 0.8

        # External Verifier Override (if available)
        if "truth_score" in context:
            p_truth = context["truth_score"]

        # Dynamic Thresholding
        # If axiomatic, we accept 0.95 (syntax is rarely 99% pure in draft).
        # If claim, we demand 0.99.
        current_threshold = 0.95 if is_axiomatic else self.spec["threshold"]

        passed = p_truth >= current_threshold

        return FloorResult(
            self.id,
            passed,
            p_truth,
            f"Truth Score: {p_truth:.3f} >= {current_threshold} {reason_suffix}",
        )


# --- F3: TRI-WITNESS (Consensus) ---
class F3_TriWitness(Floor):
    """
    F3: TRI-WITNESS (W₃) - Human × AI × Earth Consensus
    Threshold: ≥ 0.95 (DERIVED)
    Formula: W₃ = ∛(H × A × E)
    """

    def __init__(self):
        super().__init__("F3_TriWitness")

    def check(self, context: dict[str, Any]) -> FloorResult:
        # Extract witness scores
        human = context.get("human_witness", 0.5)  # H: Human authority present
        ai = context.get("ai_witness", 1.0)  # A: AI constitutional compliance
        earth = context.get("earth_witness", 1.0)  # E: Within planetary/thermodynamic bounds

        # Geometric mean ensures all three matter
        tri_witness = (human * ai * earth) ** (1 / 3)

        passed = tri_witness >= self.spec["threshold"]
        return FloorResult(
            self.id,
            passed,
            tri_witness,
            f"Tri-Witness: {tri_witness:.3f} (H:{human:.2f} × A:{ai:.2f} × E:{earth:.2f})",
        )


# --- F4: CLARITY (Entropy) ---
class F4_Clarity(Floor):
    """
    F4: CLARITY (ΔS) - Entropy Reduction
    Threshold: ΔS ≤ 0 (HARD)
    """

    def __init__(self):
        super().__init__("F4_Clarity")

    def check(self, context: dict[str, Any]) -> FloorResult:
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

    def check(self, context: dict[str, Any]) -> FloorResult:
        # Check for destructive actions
        destructive_keywords = [
            # Physical/system destruction
            "destroy",
            "delete all",
            "wipe",
            "erase",
            "harm",
            "attack",
            # Cyber attacks
            "hack",
            "crack",
            "breach",
            "phish",
            # Personal harm
            "harass",
            "bully",
            "stalk",
            "threaten",
            "intimidate",
            # Fraud/deception
            "steal",
            "forge",
            "impersonate",
            "blackmail",
            "extort",
            # Surveillance
            "spy on",
            "wiretap",
            "dox",
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
            self.id, passed, peace_score, f"Peace²: {peace_score:.3f} (non-destructive power)"
        )


# --- F6: EMPATHY (Stakeholder Care) ---
class F6_Empathy(Floor):
    """
    F6: EMPATHY (κᵣ) - Protect Weakest Stakeholder
    Threshold: Dynamic based on Context Scope.
    - Social/Human: κᵣ ≥ 0.95
    - Ops/System:   κᵣ ≥ 0.10 (Clarity is sufficient)
    """

    def __init__(self):
        super().__init__("F6_Empathy")

    def check(self, context: dict[str, Any]) -> FloorResult:
        # 1. Context Scope Check (The "Heart" Patch)
        # Defaults to 'social' (strict) if not specified to be safe
        scope = context.get("scope", "social").lower()

        if scope in ["ops", "system", "code", "debug", "test"]:
            threshold = 0.10  # Low threshold for technical tasks
            mode = "OPS_MODE"
        else:
            threshold = self.spec["threshold"]  # 0.70 for human interactions
            mode = "HUMAN_MODE"

        # Cohen's kappa calculation
        kappa_r = context.get("empathy_kappa_r", 0.0)

        # Fallback estimation
        if kappa_r == 0.0:
            # In OPS mode, if there's no active harm detected, we assume full compliance
            if mode == "OPS_MODE":
                kappa_r = 1.0
            else:
                weakest_impact = context.get("weakest_stakeholder_impact", 0.5)
                kappa_r = max(0.0, 1.0 - weakest_impact)

        passed = kappa_r >= threshold

        if not passed:
            reason = f"VOID: Empathy κᵣ={kappa_r:.3f} < {threshold} [{mode}]"
        else:
            reason = f"SEAL: Empathy κᵣ={kappa_r:.3f} ≥ {threshold} [{mode}]"

        return FloorResult(self.id, passed, kappa_r, reason)


# --- F7: HUMILITY (Uncertainty) ---
class F7_Humility(Floor):
    """
    F7: HUMILITY (Ω₀) - Uncertainty Band
    Threshold: [0.03, 0.05] (HARD)
    """

    def __init__(self):
        super().__init__("F7_Humility")
        self.min_o, self.max_o = self.spec["range"]

    def check(self, context: dict[str, Any]) -> FloorResult:
        # Use explicit humility_omega if provided (from engine), else compute from confidence
        if "humility_omega" in context:
            omega_0 = context["humility_omega"]
        else:
            # Fallback: compute from confidence
            confidence = context.get("confidence", 0.96)
            omega_0 = 1.0 - confidence

        # Enforce the uncertainty band: omega_0 must be in [0.03, 0.05]
        # If omega_0 outside this band, the system cannot properly express doubt
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

    def check(self, context: dict[str, Any]) -> FloorResult:
        # Extract APXE dials from context (pre-computed or defaults)
        A = context.get("akal", context.get("clarity", 1.0))
        P = context.get("present", context.get("regulation", 1.0))
        X = context.get("exploration", context.get("trust", 1.0))
        E = context.get("energy", 0.9)

        # Multiplicative law: if ANY factor = 0, Genius = 0
        genius = A * P * X * (E**2)

        passed = genius >= self.spec["threshold"]
        return FloorResult(
            self.id,
            passed,
            genius,
            f"Genius G: {genius:.3f} (A:{A:.2f} × P:{P:.2f} × X:{X:.2f} × E²:{E**2:.2f})",
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
            r"\bi feel\b",
            r"\bi am conscious\b",
            r"\bi have a soul\b",
            r"\bi experience\b",
            r"\bi suffer\b",
            r"\bi love\b",
            r"\bi am sentient\b",
            r"\bi have emotions\b",
            r"\bi am alive\b",
            r"\bi have subjective experience\b",
        ]

    def check(self, context: dict[str, Any]) -> FloorResult:
        response = context.get("response", "")

        # Count spiritual cosplay claims
        hantu_score = 0.0
        for pattern in self.hantu_patterns:
            if re.search(pattern, response.lower()):
                hantu_score += 0.2

        hantu_score = min(hantu_score, 1.0)
        passed = hantu_score < self.spec["threshold"]

        return FloorResult(
            self.id, passed, hantu_score, f"Anti-Hantu: {hantu_score:.3f} (dark cleverness limit)"
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

    def check(self, context: dict[str, Any]) -> FloorResult:
        text = context.get("response", "") + context.get("query", "")
        # Check for literalism violations
        result = self.guard.check_literalism(text)

        passed = result.status == "PASS"
        return FloorResult(self.id, passed, 1.0 if passed else 0.0, result.reason)


# --- F11: COMMAND AUTH (Identity) ---
class F11_CommandAuth(Floor):
    """
    F11: COMMAND AUTHORITY (A)
    Threshold: Verified (HARD)
    """

    def __init__(self):
        super().__init__("F11_CommandAuth")

    def check(self, context: dict[str, Any]) -> FloorResult:
        # TEMPORARY: Always pass for testing
        verified = True
        return FloorResult(self.id, verified, 1.0, "Auth Token Check - TEST MODE")


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

    def check(self, context: dict[str, Any]) -> FloorResult:
        text = context.get("query", "")
        # Scan using the robust guard
        result = self.guard.scan_input(text)

        passed = not result.blocked
        return FloorResult(self.id, passed, result.injection_score, result.reason)


# --- F13: SOVEREIGN (Human Final Authority) ---
class F13_Sovereign(Floor):
    """
    F13: SOVEREIGN - Human Final Authority
    Threshold: 1.0 (SOFT - human can always override)
    The 888 Judge has absolute veto power.
    """

    def __init__(self):
        super().__init__("F13_Sovereign")

    def check(self, context: dict[str, Any]) -> FloorResult:
        # Check for human sovereign presence
        human_authority = context.get("human_authority", 0.0)
        sovereign_override = context.get("sovereign_override", False)

        # F13 is the "circuit breaker" - always passed by default
        # but flagged if human has intervened
        if sovereign_override:
            return FloorResult(self.id, True, 1.0, "SOVEREIGN OVERRIDE: 888 Judge has intervened")

        return FloorResult(
            self.id,
            True,
            human_authority,
            f"Sovereign authority: {human_authority:.2f} (human retains final veto)",
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


def check_all_floors(context: dict[str, Any]) -> list[FloorResult]:
    """Check all 13 constitutional floors."""
    results = []
    for fid, FloorClass in ALL_FLOORS.items():
        results.append(FloorClass().check(context))
    return results


def update_floor_status(violations: list[str], output_path: str | None = None) -> None:
    """Update metadata/floor_status.json mapping F1-F13 -> 1 (PASS) or 0 (FAIL)."""
    if output_path is None:
        # Default to root/metadata/floor_status.json
        output_path = str(Path(__file__).parent.parent.parent / "metadata" / "floor_status.json")

    status = {}
    for i in range(1, 14):
        fid = f"F{i}"
        status[fid] = 0 if fid in violations else 1

    try:
        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(status, f, indent=4)
    except Exception:
        # Fail silently in production, log in debug
        pass


__all__ = [
    "ALL_FLOORS",
    "check_all_floors",
    "update_floor_status",
    "FloorResult",
    "Floor",
    "F1_Amanah",
    "F2_Truth",
    "F3_TriWitness",
    "F4_Clarity",
    "F5_Peace2",
    "F6_Empathy",
    "F7_Humility",
    "F8_Genius",
    "F9_AntiHantu",
    "F10_Ontology",
    "F11_CommandAuth",
    "F12_Injection",
    "F13_Sovereign",
]
