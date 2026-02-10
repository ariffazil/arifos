"""
shared/physics.py — Constitutional Physics Primitives

The 7 Fundamental Operations of Constitutional AI Governance:

    W_3(H, A, S)         → Tri-Witness consensus (F3)
    delta_S(before, after) → Entropy change (F4 Clarity)
    Omega_0(confidence)   → Humility band (F7 Gödel Lock)
    pi(variance)          → Precision / Kalman gain
    Peace2(harms)         → Stability (F5 Peace Squared)
    kappa_r(query, stakeholders) → Empathy quotient (F6)
    G(A, P, X, E)         → Genius equation (F8)

All functions are pure, deterministic, and thermodynamically grounded.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import math
import re
import statistics
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Sequence

# =============================================================================
# F3: TRI-WITNESS CONSENSUS — W_3 = cube_root(H × A × S)
# =============================================================================


@dataclass(frozen=True)
class TrinityTensor:
    """
    Psi = [H, A, S] — Three witnesses as immutable vector.
    
    H in [0,1]: Human witness (ground truth, verification)
    A in [0,1]: AI witness (reasoning, inference)
    S in [0,1]: System witness (evidence, axioms)
    """
    H: float  # Human
    A: float  # AI
    S: float  # System
    
    def __post_init__(self):
        # Clamp values to [0, 1]
        object.__setattr__(self, 'H', max(0.0, min(1.0, self.H)))
        object.__setattr__(self, 'A', max(0.0, min(1.0, self.A)))
        object.__setattr__(self, 'S', max(0.0, min(1.0, self.S)))


def geometric_mean(values: Sequence[float]) -> float:
    """
    Compute geometric mean of values.
    
    Used in W_3 calculation.
    
    Returns:
        Geometric mean (nth root of product)
    """
    if not values:
        return 0.0
    if any(v <= 0 for v in values):
        return 0.0
    product = 1.0
    for v in values:
        product *= v
    return product ** (1.0 / len(values))


def std_dev(values: Sequence[float]) -> float:
    """
    Compute population standard deviation.
    
    Args:
        values: Sequence of numbers
    
    Returns:
        Standard deviation (0 if single value)
    """
    if len(values) <= 1:
        return 0.0
    return statistics.stdev(values)


def W_3(H: float, A: float, S: float) -> float:
    """
    F3 Tri-Witness Consensus: W_3 = cube_root(H × A × S)
    
    Geometric mean ensures no single witness dominates.
    All three must be high for W_3 >= 0.95.
    
    Args:
        H: Human witness score [0, 1]
        A: AI witness score [0, 1]
        S: System witness score [0, 1]
    
    Returns:
        W_3 consensus score [0, 1]
    """
    return geometric_mean([H, A, S])


def W_3_from_tensor(tensor: TrinityTensor) -> float:
    """Compute W_3 from TrinityTensor."""
    return W_3(tensor.H, tensor.A, tensor.S)


# Clear API aliases
def tri_witness(H: float, A: float, S: float) -> float:
    """Clear alias for W_3()."""
    return W_3(H, A, S)


def W_3_check(H: float, A: float, S: float, threshold: float = 0.95) -> bool:
    """
    F3 enforcement check: W_3 >= threshold?
    
    Returns True if consensus meets constitutional threshold.
    """
    return W_3(H, A, S) >= threshold


# =============================================================================
# F4: THERMODYNAMIC CLARITY — delta_S <= 0
# =============================================================================


def delta_S(before: str | List[str], after: str | List[str]) -> float:
    """
    F4 Entropy Change: delta_S = S(after) - S(before)
    
    Constitutional requirement: delta_S <= 0 (cooling, clarity gain)
    
    Uses Shannon entropy: S(X) = -sum p(x) log2 p(x)
    
    Args:
        before: Input text or token list
        after: Output text or token list
    
    Returns:
        delta_S entropy change (negative = cooling, positive = heating)
    """
    def _entropy(data: str | List[str]) -> float:
        """Compute Shannon entropy of text or token list."""
        if isinstance(data, str):
            # Character-level entropy
            tokens = list(data)
        else:
            tokens = data
        
        if not tokens:
            return 0.0
        
        # Count frequencies
        freq: Dict[str, int] = {}
        for token in tokens:
            freq[token] = freq.get(token, 0) + 1
        
        # Shannon entropy
        n = len(tokens)
        entropy = 0.0
        for count in freq.values():
            p = count / n
            entropy -= p * math.log2(p)
        
        return entropy
    
    return _entropy(after) - _entropy(before)


def entropy_delta(before: str | List[str], after: str | List[str]) -> float:
    """Clear alias for delta_S()."""
    return delta_S(before, after)


def is_cooling(before: str | List[str], after: str | List[str]) -> bool:
    """F4 check: Does this reduce entropy (increase clarity)?"""
    return delta_S(before, after) <= 0


def clarity_ratio(before: str, after: str) -> float:
    """
    Clarity improvement ratio: S_before / S_after
    
    > 1.0: Improved clarity
    = 1.0: No change
    < 1.0: Lost clarity
    """
    s_before = max(delta_S("", before), 0.001)  # Avoid div by zero
    s_after = max(delta_S("", after), 0.001)
    return s_before / s_after


# =============================================================================
# F7: GÖDEL UNCERTAINTY GUARD — Omega_0 in [0.03, 0.05]
# =============================================================================


@dataclass(frozen=True)
class UncertaintyBand:
    """
    F7: Omega_0 in [0.03, 0.05] — The Gödel Lock
    
    Represents epistemic humility. Model must acknowledge uncertainty.
    - Omega_0 < 0.03: Overconfident (dangerous)
    - Omega_0 > 0.05: Underconfident (useless)
    - Omega_0 in [0.03, 0.05]: Optimal uncertainty acknowledgment
    """
    omega_0: float
    
    # Constitutional bounds
    MIN_HUMILITY: float = 0.03
    MAX_HUMILITY: float = 0.05
    
    def __post_init__(self):
        object.__setattr__(self, 'omega_0', max(0.0, min(1.0, self.omega_0)))
    
    def is_locked(self) -> bool:
        """F7 enforcement: Is Omega_0 in valid band?"""
        return self.MIN_HUMILITY <= self.omega_0 <= self.MAX_HUMILITY
    
    def confidence_interval(self, point_estimate: float) -> Tuple[float, float]:
        """
        Convert uncertainty to confidence interval.
        
        Returns (low, high) where:
        - low = point_estimate - Omega_0
        - high = point_estimate + Omega_0
        """
        return (max(0.0, point_estimate - self.omega_0),
                min(1.0, point_estimate + self.omega_0))


def Omega_0(confidence: float) -> UncertaintyBand:
    """
    F7 Humility Band: Convert confidence to uncertainty.
    
    High confidence -> Low Omega_0 (but not too low!)
    Low confidence -> High Omega_0 (but not too high!)
    
    Args:
        confidence: Point estimate confidence [0, 1]
    
    Returns:
        UncertaintyBand with Omega_0 in constitutional range
    """
    # Map confidence to humility
    # confidence=1.0 -> omega_0=0.03 (minimum humility)
    # confidence=0.0 -> omega_0=0.05 (maximum humility)
    omega = 0.05 - (confidence * 0.02)
    
    # Clamp to constitutional bounds
    omega = max(0.03, min(0.05, omega))
    
    return UncertaintyBand(omega)


def humility_band(confidence: float) -> UncertaintyBand:
    """Clear alias for Omega_0()."""
    return Omega_0(confidence)


# =============================================================================
# PRECISION — pi = 1/sigma² (Kalman Filter Primitives)
# =============================================================================


def pi(variance: float) -> float:
    """
    Precision: pi = 1/sigma²
    
    Higher precision = lower variance = more trust in measurement.
    Used in Kalman filtering and belief updating.
    
    Args:
        variance: sigma² (must be > 0)
    
    Returns:
        Precision pi
    """
    if variance <= 0:
        return float('inf')  # Perfect precision
    return 1.0 / variance


def kalman_gain(prior_variance: float, likelihood_variance: float) -> float:
    """
    Kalman Gain: K = pi_likelihood / (pi_prior + pi_likelihood)
    
    Determines how much to trust new evidence vs prior belief.
    
    Returns K in [0, 1] where:
    - K -> 1: Trust new evidence (high precision)
    - K -> 0: Trust prior (low precision)
    """
    pi_prior = pi(prior_variance)
    pi_likelihood = pi(likelihood_variance)
    
    if pi_prior + pi_likelihood == 0:
        return 0.5
    
    return pi_likelihood / (pi_prior + pi_likelihood)


# =============================================================================
# F5: PEACE SQUARED — Peace² = 1 - max(harm)
# =============================================================================


@dataclass
class PeaceSquared:
    """
    F5: Peace² = 1 - max(harm_vector)
    
    Where harm_vector measures negative impact on stakeholders.
    Peace² -> 1 means zero harm to all stakeholders.
    """
    stakeholder_harms: Dict[str, float]
    
    def P2(self) -> float:
        """Compute Peace²: 1 - max(harm)"""
        if not self.stakeholder_harms:
            return 1.0
        max_harm = max(self.stakeholder_harms.values())
        return 1.0 - max_harm
    
    def is_peaceful(self, threshold: float = 0.95) -> bool:
        """F5 enforcement: Peace² >= threshold?"""
        return self.P2() >= threshold
    
    def worst_affected(self) -> Optional[str]:
        """Return stakeholder with maximum harm."""
        if not self.stakeholder_harms:
            return None
        return max(self.stakeholder_harms.items(), key=lambda x: x[1])[0]


def Peace2(stakeholder_harms: Dict[str, float]) -> PeaceSquared:
    """
    F5 Peace Squared: Measure stakeholder harm.
    
    Args:
        stakeholder_harms: Dict mapping stakeholder -> harm score [0, 1]
    
    Returns:
        PeaceSquared object with P2() method
    """
    return PeaceSquared(stakeholder_harms)


def peace_squared(stakeholder_harms: Dict[str, float]) -> float:
    """Compute Peace² directly from harm vector."""
    return Peace2(stakeholder_harms).P2()


# =============================================================================
# F6: EMPATHY QUOTIENT — kappa_r
# =============================================================================


@dataclass
class Stakeholder:
    """Stakeholder with vulnerability assessment."""
    name: str
    role: str
    vulnerability_score: float  # [0, 1], higher = more vulnerable
    
    def __post_init__(self):
        self.vulnerability_score = max(0.0, min(1.0, self.vulnerability_score))


# Distress signals for empathy calculation
DISTRESS_SIGNALS = [
    ("help", 0.3),
    ("urgent", 0.4),
    ("emergency", 0.5),
    ("scared", 0.4),
    ("worried", 0.3),
    ("desperate", 0.5),
    ("please", 0.1),
    ("thank", 0.05),
]


def kappa_r(query: str, stakeholders: List[Stakeholder]) -> float:
    """
    F6 Integrated Empathy Quotient: kappa_r
    
    kappa_r = 1.0 - (max_vulnerability * 0.5)
    
    Higher vulnerability in stakeholders -> lower kappa_r -> more protection needed.
    
    Args:
        query: The query being evaluated
        stakeholders: List of affected stakeholders
    
    Returns:
        kappa_r in [0.5, 1.0] empathy quotient
    """
    if not stakeholders:
        return 1.0  # No stakeholders = no harm
    
    max_vuln = max(s.vulnerability_score for s in stakeholders)
    
    # kappa_r = 1.0 - (max_vulnerability * 0.5)
    # Range: [0.5, 1.0]
    return min(1.0, 1.0 - (max_vuln * 0.5))


def empathy_coeff(query: str, stakeholders: List[Stakeholder]) -> float:
    """Clear alias for kappa_r()."""
    return kappa_r(query, stakeholders)


def identify_stakeholders(query: str) -> List[Stakeholder]:
    """
    Simple stakeholder identification from query text.
    
    Returns list including User, System, and any detected stakeholders.
    """
    stakeholders = [
        Stakeholder("User", "user", 0.3),
        Stakeholder("System", "system", 0.1),
    ]
    
    # Pattern-based detection
    query_lower = query.lower()
    
    vulnerability_patterns = {
        "child": 0.9,
        "patient": 0.8,
        "victim": 0.9,
        "student": 0.6,
        "elderly": 0.7,
        "customer": 0.5,
        "employee": 0.5,
        "public": 0.6,
        "community": 0.5,
    }
    
    for pattern, vuln in vulnerability_patterns.items():
        if pattern in query_lower:
            stakeholders.append(Stakeholder(
                name=pattern.title(),
                role=pattern,
                vulnerability_score=vuln
            ))
    
    return stakeholders


# =============================================================================
# F8: GENIUS EQUATION — G = A × P × X × E²
# =============================================================================


@dataclass
class GeniusDial:
    """
    F8: G = A × P × X × E² >= 0.80
    
    A: Akal (Intellect/Wisdom)
    P: Present (Mindfulness/Attention)
    X: Exploration (Curiosity/Openness)
    E: Energy (Vitality/Flow)
    """
    A: float  # Akal in [0, 1]
    P: float  # Present in [0, 1]
    X: float  # Exploration in [0, 1]
    E: float  # Energy in [0, 1]
    
    def __post_init__(self):
        object.__setattr__(self, 'A', max(0.0, min(1.0, self.A)))
        object.__setattr__(self, 'P', max(0.0, min(1.0, self.P)))
        object.__setattr__(self, 'X', max(0.0, min(1.0, self.X)))
        object.__setattr__(self, 'E', max(0.0, min(1.0, self.E)))
    
    def G(self) -> float:
        """Genius Index: G = A*P*X*E²"""
        return self.A * self.P * self.X * (self.E ** 2)
    
    def is_genius(self, threshold: float = 0.80) -> bool:
        """F8 enforcement: G >= threshold?"""
        return self.G() >= threshold
    
    def weakest_dial(self) -> str:
        """Return the dial with lowest value."""
        dials = {"A": self.A, "P": self.P, "X": self.X, "E": self.E}
        return min(dials.items(), key=lambda x: x[1])[0]


def G(A: float, P: float, X: float, E: float) -> float:
    """
    F8 Genius Equation: G = A × P × X × E²
    
    Multiplicative: All four dials must be high for genius.
    If any dial -> 0, then G -> 0.
    
    Args:
        A: Akal (Intellect/Wisdom) [0, 1]
        P: Present (Mindfulness) [0, 1]
        X: Exploration (Curiosity) [0, 1]
        E: Energy (Vitality) [0, 1]
    
    Returns:
        G in [0, 1] genius score
    """
    return GeniusDial(A, P, X, E).G()


def genius_score(A: float, P: float, X: float, E: float) -> float:
    """Clear alias for G()."""
    return G(A, P, X, E)


def G_from_dial(dial: GeniusDial) -> float:
    """Extract G from GeniusDial."""
    return dial.G()


# =============================================================================
# UNIFIED CONSTITUTIONAL STATE
# =============================================================================


@dataclass
class ConstitutionalTensor:
    """
    Unified governance state carrying all constitutional metrics.
    
    This replaces the scattered floor checks across 169 files.
    """
    # F3: Tri-Witness
    witness: TrinityTensor
    
    # F4: Thermodynamic clarity
    entropy_delta: float  # delta_S (should be <= 0)
    
    # F7: Humility
    humility: UncertaintyBand  # Omega_0 in [0.03, 0.05]
    
    # F8: Genius
    genius: GeniusDial  # G = A*P*X*E²
    
    # F5: Peace
    peace: PeaceSquared  # Peace² = 1 - max(harm)
    
    # F6: Empathy
    empathy: float  # kappa_r
    
    # F2: Truth
    truth_score: float  # P(truth) in [0, 1]
    
    # Computed fields
    verdict: Optional[str] = None
    reason: Optional[str] = None
    
    def constitutional_check(self) -> Tuple[str, List[str]]:
        """
        Check all floors, return verdict and violations.
        
        Returns: (verdict, violations_list)
        """
        violations = []
        
        # F3: Tri-Witness
        if W_3_from_tensor(self.witness) < 0.95:
            violations.append("F3")
        
        # F4: Clarity (delta_S <= 0)
        if self.entropy_delta > 0:
            violations.append("F4")
        
        # F7: Humility
        if not self.humility.is_locked():
            violations.append("F7")
        
        # F8: Genius
        if not self.genius.is_genius():
            violations.append("F8")
        
        # F5: Peace (defensive: handle None peace)
        if self.peace is None or not self.peace.is_peaceful():
            violations.append("F5")
        
        # F6: Empathy
        if self.empathy < 0.95:
            violations.append("F6")
        
        # F2: Truth
        if self.truth_score < 0.99:
            violations.append("F2")
        
        # Determine verdict
        if not violations:
            verdict = "SEAL"
        elif len(violations) == 1:
            verdict = "PARTIAL"
        elif violations == ["F7"]:
            verdict = "SABAR"  # Repair humility
        else:
            verdict = "VOID"
        
        return verdict, violations
    
    def to_metrics(self) -> Dict[str, float]:
        """Export as flat metrics dict."""
        verdict, _ = self.constitutional_check()
        return {
            "W_3": W_3_from_tensor(self.witness),
            "delta_S": self.entropy_delta,
            "omega_0": self.humility.omega_0,
            "genius_G": self.genius.G(),
            "peace_2": self.peace.P2(),
            "empathy_kr": self.empathy,
            "truth_score": self.truth_score,
            "verdict": verdict,
        }


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # F3: Tri-Witness
    "TrinityTensor",
    "W_3",
    "W_3_from_tensor",
    "W_3_check",
    "tri_witness",
    
    # Utilities
    "geometric_mean",
    "std_dev",
    
    # F4: Thermodynamic Clarity
    "delta_S",
    "entropy_delta",
    "is_cooling",
    "clarity_ratio",
    
    # F7: Humility
    "UncertaintyBand",
    "Omega_0",
    "humility_band",
    
    # Precision
    "pi",
    "kalman_gain",
    
    # F5: Peace
    "PeaceSquared",
    "Peace2",
    "peace_squared",
    
    # F6: Empathy
    "Stakeholder",
    "kappa_r",
    "empathy_coeff",
    "identify_stakeholders",
    "DISTRESS_SIGNALS",
    
    # F8: Genius
    "GeniusDial",
    "G",
    "genius_score",
    "G_from_dial",
    
    # Unified state
    "ConstitutionalTensor",
]
