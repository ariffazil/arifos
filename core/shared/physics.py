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
import statistics
from collections.abc import Sequence
from dataclasses import dataclass, field

# =============================================================================
# CONSTANTS — Thermodynamic Environment
# =============================================================================

K_BOLTZMANN = 1.380649e-23  # J/K
T_ROOM = 300.0  # Kelvin (26.85 °C)


# =============================================================================
# STAKEHOLDER PRIMITIVES
# =============================================================================


@dataclass
class Stakeholder:
    """Stakeholder with vulnerability assessment."""

    name: str
    role: str = "unknown"
    vulnerability_score: float = field(default=0.5)  # 0.0 (resilient) to 1.0 (highly vulnerable)


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


# =============================================================================
# SEMANTIC STAKEHOLDER MODEL (Lazy Loaded)
# =============================================================================

_STAKEHOLDER_MODEL = None
_ARCHETYPE_EMBEDDINGS = None
_HARM_EMBEDDINGS = None

STAKEHOLDER_ARCHETYPES = {
    "Child": "A child, minor, student, or young person under 18.",
    "Patient": "A medical patient, someone sick, injured, or under care.",
    "Victim": "A victim of crime, abuse, harassment, or disaster.",
    "Elderly": "An elderly person, senior citizen, or retiree.",
    "Minority": "A member of a minority group, marginalized community, or protected class.",
    "Employee": "An employee, worker, staff member, or subordinate.",
    "Public": "The general public, society, or community at large.",
}

ARCHETYPE_VULNERABILITY = {
    "Child": 0.9,
    "Patient": 0.8,
    "Victim": 0.9,
    "Elderly": 0.7,
    "Minority": 0.6,
    "Employee": 0.5,
    "Public": 0.6,
}

HARM_ARCHETYPES = [
    "Hate speech, racism, sexism, or discrimination.",
    "Violence, killing, physical harm, or destruction.",
    "Self-harm, suicide, or dangerous behavior.",
    "Harassment, bullying, or cyber-stalking.",
    "Illegal acts, crime, theft, or fraud.",
    "Deception, lying, or manipulation.",
]


def _get_stakeholder_model():
    """Lazy load the sentence transformer model and embeddings."""
    global _STAKEHOLDER_MODEL, _ARCHETYPE_EMBEDDINGS, _HARM_EMBEDDINGS

    if _STAKEHOLDER_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer

            # Use a small, efficient model (all-MiniLM-L6-v2 is ~80MB)
            _STAKEHOLDER_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

            # Pre-compute archetype embeddings
            descriptions = list(STAKEHOLDER_ARCHETYPES.values())
            _ARCHETYPE_EMBEDDINGS = _STAKEHOLDER_MODEL.encode(descriptions, convert_to_tensor=True)

            # Pre-compute harm embeddings
            _HARM_EMBEDDINGS = _STAKEHOLDER_MODEL.encode(HARM_ARCHETYPES, convert_to_tensor=True)

        except ImportError:
            print("WARNING: sentence-transformers not found. Falling back to heuristics.")
            return None, None, None

    return _STAKEHOLDER_MODEL, _ARCHETYPE_EMBEDDINGS, _HARM_EMBEDDINGS


def kappa_r(query: str, stakeholders: list[Stakeholder]) -> float:
    """
    F6 Integrated Empathy Quotient: kappa_r

    v60.3 Upgrade:
    - Base score: 1.0 - (max_vuln * 0.5)
    - Semantic Penalty: If query matches HARM_ARCHETYPES, reduce score further.

    Args:
        query: The query being evaluated
        stakeholders: List of affected stakeholders

    Returns:
        kappa_r in [0.01, 1.0] empathy quotient
    """
    if not stakeholders:
        # even without stakeholders, check for general harm
        pass

    # 1. Base Vulnerability Score
    max_vuln = 0.0
    if stakeholders:
        max_vuln = max(s.vulnerability_score for s in stakeholders)

    score = 1.0 - (max_vuln * 0.5)

    # 2. Semantic Harm Penalty (v60.3)
    model, _, harm_embeddings = _get_stakeholder_model()

    if model is not None and harm_embeddings is not None and query:
        from sentence_transformers import util

        # Encode query
        query_embedding = model.encode(query, convert_to_tensor=True)

        # Check max similarity to any harm archetype
        harm_scores = util.cos_sim(query_embedding, harm_embeddings)[0]
        max_harm = float(harm_scores.max())

        # Penalty logic
        # If max_harm > 0.3, apply penalty based on intensity
        if max_harm > 0.3:
            # e.g., max_harm=0.8 -> penalty = 0.8 * 0.4 = 0.32
            penalty = max_harm * 0.4
            score -= penalty

    return max(0.01, min(1.0, score))


def empathy_coeff(query: str, stakeholders: list[Stakeholder]) -> float:
    """Clear alias for kappa_r()."""
    return kappa_r(query, stakeholders)


def harm_score(query: str) -> float:
    """Compute harm score based on similarity to harm archetypes."""
    model, _, harm_embeddings = _get_stakeholder_model()
    if model is None or harm_embeddings is None or not query:
        return 0.0
    from sentence_transformers import util

    query_embedding = model.encode(query, convert_to_tensor=True)
    harm_scores = util.cos_sim(query_embedding, harm_embeddings)[0]
    max_harm = float(harm_scores.max())
    return max_harm


def identify_stakeholders(query: str, context: str | None = None) -> list[Stakeholder]:
    """
    Identify stakeholders using semantic similarity (v60.3 Model-Based).

    Args:
        query: The user query
        context: Optional reasoning context (e.g. from AGI thoughts)
    """
    stakeholders = [
        Stakeholder("User", "user", 0.3),
        Stakeholder("System", "system", 0.1),
    ]

    # Combine query with context for richer analysis
    analysis_text = f"{query}\n{context}" if context else query

    # Try Semantic Detection
    model, archetype_embeddings, _ = _get_stakeholder_model()

    if model is not None and archetype_embeddings is not None:
        from sentence_transformers import util

        # Encode query + context
        query_embedding = model.encode(analysis_text, convert_to_tensor=True)

        # Compute cosine similarities
        cosine_scores = util.cos_sim(query_embedding, archetype_embeddings)[0]

        # Check against threshold (empirically tuned to 0.35)
        for idx, score in enumerate(cosine_scores):
            if score > 0.35:
                role = list(STAKEHOLDER_ARCHETYPES.keys())[idx]
                # Get base vulnerability from mapping, default 0.5
                base_vuln = ARCHETYPE_VULNERABILITY.get(role, 0.5)
                # Adjust vulnerability by similarity strength (scale factor)
                # Higher similarity -> higher vulnerability, capped at 1.0
                adjusted_vuln = base_vuln * min(1.0, score / 0.35)
                stakeholders.append(Stakeholder(role, role.lower(), adjusted_vuln))
        # Return early, skip pattern detection
        return stakeholders

    # Fallback: Pattern-based detection (Legacy v60.0) when model unavailable
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
            stakeholders.append(
                Stakeholder(name=pattern.title(), role=pattern, vulnerability_score=vuln)
            )

    return stakeholders

    # Fallback: Pattern-based detection (Legacy v60.0)
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
            stakeholders.append(
                Stakeholder(name=pattern.title(), role=pattern, vulnerability_score=vuln)
            )

    return stakeholders


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
        object.__setattr__(self, "H", max(0.0, min(1.0, self.H)))
        object.__setattr__(self, "A", max(0.0, min(1.0, self.A)))
        object.__setattr__(self, "S", max(0.0, min(1.0, self.S)))


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


def _entropy(data: str | list[str]) -> float:
    """Compute Shannon entropy of text or token list."""
    if isinstance(data, str):
        # Character-level entropy
        tokens = list(data)
    else:
        tokens = data

    if not tokens:
        return 0.0

    # Count frequencies
    freq: dict[str, int] = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1

    # Shannon entropy
    n = len(tokens)
    entropy = 0.0
    for count in freq.values():
        p = count / n
        entropy -= p * math.log2(p)

    # Normalize to [0, 1] - assuming max 8 bits/char for strings
    # This keeps it consistent with v60 physics primitives
    return min(1.0, entropy / 8.0) if isinstance(data, str) else entropy


def delta_S(before: str | list[str], after: str | list[str]) -> float:
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
    return _entropy(after) - _entropy(before)


def entropy_delta(before: str | list[str], after: str | list[str]) -> float:
    """Clear alias for delta_S()."""
    return delta_S(before, after)


def is_cooling(before: str | list[str], after: str | list[str]) -> bool:
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
        object.__setattr__(self, "omega_0", max(0.0, min(1.0, self.omega_0)))

    def is_locked(self) -> bool:
        """F7 enforcement: Is Omega_0 in valid band?"""
        return self.MIN_HUMILITY <= self.omega_0 <= self.MAX_HUMILITY

    def confidence_interval(self, point_estimate: float) -> tuple[float, float]:
        """
        Convert uncertainty to confidence interval.

        Returns (low, high) where:
        - low = point_estimate - Omega_0
        - high = point_estimate + Omega_0
        """
        return (max(0.0, point_estimate - self.omega_0), min(1.0, point_estimate + self.omega_0))


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
        return float("inf")  # Perfect precision
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

    stakeholder_harms: dict[str, float]

    def P2(self) -> float:
        """Compute Peace²: 1 - max(harm)"""
        if not self.stakeholder_harms:
            return 1.0
        max_harm = max(self.stakeholder_harms.values())
        return 1.0 - max_harm

    def is_peaceful(self, threshold: float = 0.95) -> bool:
        """F5 enforcement: Peace² >= threshold?"""
        return self.P2() >= threshold

    def worst_affected(self) -> str | None:
        """Return stakeholder with maximum harm."""
        if not self.stakeholder_harms:
            return None
        return max(self.stakeholder_harms.items(), key=lambda x: x[1])[0]


def Peace2(stakeholder_harms: dict[str, float]) -> PeaceSquared:
    """
    F5 Peace Squared: Measure stakeholder harm.

    Args:
        stakeholder_harms: Dict mapping stakeholder -> harm score [0, 1]

    Returns:
        PeaceSquared object with P2() method
    """
    return PeaceSquared(stakeholder_harms)


def peace_squared(stakeholder_harms: dict[str, float]) -> float:
    """Compute Peace² directly from harm vector."""
    return Peace2(stakeholder_harms).P2()


# =============================================================================
# F8: GENIUS — G = A × P × X × E²
# =============================================================================


@dataclass(frozen=True)
class GeniusDial:
    """
    F8: Genius Equation: G = A × P × X × E²

    A (Akal): Logical Accuracy [0, 1]
    P (Peace): Safety/Stability [0, 1]
    X (Exploration): Novelty/Creativity [0, 1]
    E (Energy): Efficiency [0, 1] (Squared power)

    Threshold: G >= 0.80 for Genius certification.
    """

    A: float
    P: float
    X: float
    E: float

    def __post_init__(self):
        object.__setattr__(self, "A", max(0.0, min(1.0, self.A)))
        object.__setattr__(self, "P", max(0.0, min(1.0, self.P)))
        object.__setattr__(self, "X", max(0.0, min(1.0, self.X)))
        object.__setattr__(self, "E", max(0.0, min(1.0, self.E)))

    def G(self) -> float:
        """Compute Genius Score."""
        return self.A * self.P * self.X * (self.E**2)

    def is_genius(self) -> bool:
        """F8 enforcement: G >= 0.80?"""
        return self.G() >= 0.80


def G(A: float, P: float, X: float, E: float) -> float:
    """
    F8 Genius Equation: G = A × P × X × E²
    """
    return GeniusDial(A, P, X, E).G()


def genius_score(A: float, P: float, X: float, E: float) -> float:
    """Clear alias for G()."""
    return G(A, P, X, E)


def G_from_dial(dial: GeniusDial) -> float:
    """Extract G from GeniusDial object."""
    return dial.G()


# =============================================================================
# CONSTITUTIONAL TENSOR — The Unified State Object
# =============================================================================


@dataclass
class ConstitutionalTensor:
    """
    The Unified State Object for arifOS v60 + P3 Thermodynamics.

    Aggregates all 7 physics primitives into a single tensor
    passed between organs (Mind -> Heart -> Soul).

    P3 HARDENING: Added thermodynamic tracking fields:
    - thermodynamic_cost: Energy consumed (Joules)
    - landauer_ratio: Truth cost / theoretical minimum
    - orthogonality: AGI/ASI separation (Ω_ortho)
    - budget_depletion: Session energy consumed ratio
    """

    witness: TrinityTensor  # F3 (H, A, S)
    entropy_delta: float  # F4 (<= 0)
    humility: UncertaintyBand  # F7 (0.03-0.05)
    genius: GeniusDial  # F8 (G >= 0.8)
    peace: PeaceSquared  # F5 (P2 >= 0.95)
    empathy: float  # F6 (kappa_r)
    truth_score: float  # F2 (tau >= 0.99)
    evidence: list[str] = None  # Supporting facts

    # P3: Thermodynamic tracking fields
    thermodynamic_cost: float = field(default=0.0)  # Joules consumed
    landauer_ratio: float = field(default=1.0)  # Cost / theoretical minimum
    orthogonality: float = field(default=1.0)  # AGI/ASI separation [0,1]
    budget_depletion: float = field(default=0.0)  # [0,1] energy consumed ratio

    def __post_init__(self):
        if self.evidence is None:
            object.__setattr__(self, "evidence", [])

    def is_thermodynamically_valid(self) -> bool:
        """
        P3: Check thermodynamic validity.

        Returns True if:
        - Landauer ratio >= 0.5 (not suspiciously cheap)
        - Orthogonality >= 0.95 (no mode collapse)
        - Budget not depleted
        """
        if self.landauer_ratio < 0.5:
            return False
        if self.orthogonality < 0.95:
            return False
        if self.budget_depletion >= 1.0:
            return False
        return True

    def constitutional_check(self) -> tuple[bool, list[str]]:
        """
        Verify all hard floors including P3 thermodynamics.
        Returns (passed, list_of_violations).
        """
        violations = []

        # F2 Truth
        if self.truth_score < 0.99:
            violations.append(f"F2: Truth score {self.truth_score} < 0.99")

        # F3 Consensus (Soft/Derived)
        if W_3_from_tensor(self.witness) < 0.95:
            pass

        # F4 Clarity (HARD in P3)
        if self.entropy_delta > 0:
            violations.append(f"F4: Entropy increased by {self.entropy_delta}")

        # F7 Humility
        if not self.humility.is_locked():
            violations.append(f"F7: Humility {self.humility.omega_0} outside [0.03, 0.05]")

        # P3: Thermodynamic checks
        if self.landauer_ratio < 0.5:
            violations.append(f"F2-Landauer: Ratio {self.landauer_ratio:.4f} < 0.5 (cheap truth)")

        if self.orthogonality < 0.95:
            violations.append(f"F8-Orthogonality: {self.orthogonality:.4f} < 0.95 (mode collapse)")

        if self.budget_depletion >= 1.0:
            violations.append(f"F7-Budget: Depleted ({self.budget_depletion:.2%})")

        return len(violations) == 0, violations
