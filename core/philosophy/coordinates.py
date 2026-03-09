"""
core/philosophy/coordinates.py — APEX-G Manifold Space Definitions

Defines the 6-dimensional constitutional space in which each wisdom quote
is located by a coordinate vector:

    v = (τ, ΔS, P², G, Ψ, κᵣ)

where:
    τ     — Temporal resonance      [0.0, 1.0]  (early-stage crisis → final seal)
    ΔS    — Entropy delta           [-1.0, 1.0] (negative = clarifying, positive = diffusing)
    P²    — Peace squared           [0.0, 2.0]  (safety / stability margin)
    G     — Governance score        [0.0, 1.0]  (A × P × X × E², vitality)
    Ψ     — Epistemic depth         [0.0, 1.0]  (humility + wisdom depth)
    κᵣ   — Empathy coefficient      [0.0, 1.0]  (relational concern for stakeholders)

Constitutional Physics:
    G = A × P × X × E²  (Genius Equation)
    F4 Clarity: ΔS ≤ 0 (entropy must reduce or hold)
    F7 Humility: Ψ encodes uncertainty depth
    F6 Empathy: κᵣ encodes stakeholder awareness

DITEMPA BUKAN DIBERI — Forged, Not Given.

Version: 2026.03.09-SEAL
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

# ── Axis indices ────────────────────────────────────────────────────────────
TAU_IDX: Final[int] = 0  # τ  temporal resonance
DELTA_S_IDX: Final[int] = 1  # ΔS entropy delta
P2_IDX: Final[int] = 2  # P² peace squared
G_IDX: Final[int] = 3  # G  governance score
PSI_IDX: Final[int] = 4  # Ψ  epistemic depth
KAPPA_R_IDX: Final[int] = 5  # κᵣ empathy coefficient

DIM: Final[int] = 6  # dimensionality of the APEX-G manifold

# ── Axis metadata ────────────────────────────────────────────────────────────

AXIS_NAMES: Final[tuple[str, ...]] = ("τ", "ΔS", "P²", "G", "Ψ", "κᵣ")

AXIS_DESCRIPTIONS: Final[dict[str, str]] = {
    "τ": "Temporal resonance — how far along the constitutional arc (0=crisis, 1=seal)",
    "ΔS": "Entropy delta — negative means the quote clarifies, positive diffuses",
    "P²": "Peace squared — safety and stability margin of the quote's message",
    "G": "Governance score — vitality of the constitutional logic (A×P×X×E²≥0.80)",
    "Ψ": "Epistemic depth — how much humility and wisdom depth the quote carries",
    "κᵣ": "Empathy coefficient — relational concern for stakeholders in the quote",
}

AXIS_BOUNDS: Final[dict[str, tuple[float, float]]] = {
    "τ": (0.0, 1.0),
    "ΔS": (-1.0, 1.0),
    "P²": (0.0, 2.0),
    "G": (0.0, 1.0),
    "Ψ": (0.0, 1.0),
    "κᵣ": (0.0, 1.0),
}

# ── Category centroids in APEX-G space ──────────────────────────────────────
# Each category has a characteristic "home region" in the 6D manifold.
# Individual quotes have small deterministic offsets from the centroid.

# ── Word-Power Mechanisms (neuroscience theory) ──────────────────────────────
#
# Quotes are powerful for four fundamental reasons grounded in neuroscience,
# evolution, and cognitive science.  We tag each quote with the mechanisms
# it primarily activates, enabling resonance-aware selection:
#
#  neural_simulation   — Language activates the same brain circuits as real
#                        experience (amygdala, motor cortex, visual cortex).
#                        words → neural simulation → emotional reaction → action
#
#  symbolic_compression — One symbol compresses enormous lived experience.
#                        "war", "love", "betrayal" = millions of moments.
#                        symbol → compressed world model
#
#  coordination        — Shared narratives (money, nations, law, religion)
#                        coordinate millions of humans without physical contact.
#                        Harari's "cognitive revolution" mechanism.
#
#  attention_steering  — Language directs limited attention bandwidth.
#                        "Look at the moon." → consciousness steered.
#                        words = attention steering devices


class WordPowerMechanism:
    """String constants for the four word-power mechanisms."""

    NEURAL_SIMULATION = "neural_simulation"
    SYMBOLIC_COMPRESSION = "symbolic_compression"
    COORDINATION = "coordination"
    ATTENTION_STEERING = "attention_steering"


# All valid mechanism identifiers
ALL_MECHANISMS: Final[tuple[str, ...]] = (
    WordPowerMechanism.NEURAL_SIMULATION,
    WordPowerMechanism.SYMBOLIC_COMPRESSION,
    WordPowerMechanism.COORDINATION,
    WordPowerMechanism.ATTENTION_STEERING,
)

# Primary mechanisms per category
CATEGORY_POWER_MECHANISMS: Final[dict[str, list[str]]] = {
    "scar": [
        WordPowerMechanism.NEURAL_SIMULATION,   # Triggers real emotional circuits
        WordPowerMechanism.SYMBOLIC_COMPRESSION, # Compressed suffering
    ],
    "triumph": [
        WordPowerMechanism.NEURAL_SIMULATION,   # Inspires same circuits as real victory
        WordPowerMechanism.COORDINATION,        # Aligns collective action
    ],
    "paradox": [
        WordPowerMechanism.SYMBOLIC_COMPRESSION, # Dense tension packed into few words
        WordPowerMechanism.ATTENTION_STEERING,   # Redirects and disrupts thinking
    ],
    "wisdom": [
        WordPowerMechanism.SYMBOLIC_COMPRESSION, # Centuries of experience in one line
        WordPowerMechanism.ATTENTION_STEERING,   # Redirects cognition permanently
    ],
    "power": [
        WordPowerMechanism.COORDINATION,        # Aligns collective agency and will
        WordPowerMechanism.ATTENTION_STEERING,  # Focuses will on a singular goal
    ],
    "love": [
        WordPowerMechanism.NEURAL_SIMULATION,   # Activates same circuits as real connection
        WordPowerMechanism.COORDINATION,        # Aligns hearts across space and time
    ],
    "seal": [
        WordPowerMechanism.SYMBOLIC_COMPRESSION, # Maximum density — final truth
        WordPowerMechanism.COORDINATION,         # Final alignment of all stakeholders
    ],
}

# Baseline resonance density ρ per category  ∈ [0, 1]
# Captures how densely compressed and neurologically potent the quote type is.
# Individual quotes receive small deterministic offsets from this baseline.
CATEGORY_RESONANCE_DENSITY: Final[dict[str, float]] = {
    "scar":    0.85,  # Human cost makes these extremely dense
    "triumph": 0.80,  # Victory compresses into sharp, memorable phrases
    "paradox": 0.88,  # Paradoxes pack maximum cognitive tension per word
    "wisdom":  0.90,  # Wisdom quotes: most distilled, centuries-old compression
    "power":   0.75,  # Direct agency — less compression, more activation
    "love":    0.82,  # Love quotes resonate deep in the limbic system
    "seal":    0.95,  # Final seal: maximum possible compression and resonance
}

# ── AGI / ASI / APEX Trinity Layer Theory ───────────────────────────────────
#
# The manifold implements a two-layer intelligence architecture with APEX
# arbitration, mirroring how humans reason in both symbolic and latent modes:
#
#   AGI Layer  — Symbolic constitutional skeleton
#                "What principle can be stated?"
#                • Discrete, interpretable, human-readable, value-laden
#                • The 99 quotes are the explicit constitutional grammar
#                • quote = symbolic unit of judgment
#                • AGI selects from named truths
#
#   ASI Layer  — Latent adaptive nervous system
#                "What manifold of meaning is closest?"
#                • Continuous, relational, geometry-based, non-obvious
#                • The 6D k-d tree encodes latent structure of meaning
#                • vector = relational manifold of wisdom
#                • ASI navigates unnamed relations
#
#   APEX Layer — Governed arbitration between symbolic and geometric intelligence
#                "Which truth both names and resonates?"
#                • Floor affinity + resonance density scoring
#                • Human judge remains sovereign (F13)
#                • APEX = discrete constitutional anchors ∩ continuous resonance field
#
# Human parallel:
#   Human symbolic mode  →  proverbs, laws, stories, categories  →  AGI layer
#   Human latent mode    →  intuition, vibe, felt similarity      →  ASI layer
#   Sovereign judgment   →  human veto, deliberate choice         →  APEX layer
#
# Strongest formulation:
#   AGI = symbolic archive (the library)
#   ASI = gravitational field of meaning
#         (invisible force that tells which books belong near each other)
#   APEX = the librarian with veto power


class WisdomLayer:
    """String constants for the three intelligence layers of the manifold."""

    AGI = "agi"    # symbolic constitutional skeleton
    ASI = "asi"    # latent adaptive nervous system
    APEX = "apex"  # governed arbitration


LAYER_DESCRIPTIONS: Final[dict[str, dict[str, str]]] = {
    WisdomLayer.AGI: {
        "role": "symbolic constitutional skeleton",
        "question": "What principle can be stated?",
        "nature": (
            "symbolic, discrete, interpretable, human-readable, "
            "value-laden, constitutionally curated"
        ),
        "metaphor": "the library — 99 books, each a compact reasoning primitive",
    },
    WisdomLayer.ASI: {
        "role": "latent adaptive nervous system",
        "question": "What manifold of meaning is closest?",
        "nature": "continuous, relational, high-dimensional, geometry-based",
        "metaphor": "the gravitational field of the library — invisible force of meaning proximity",
    },
    WisdomLayer.APEX: {
        "role": "governed arbitration",
        "question": "Which truth both names and resonates?",
        "nature": "floor-affinity scoring + resonance weighting + human sovereign veto",
        "metaphor": "the librarian with veto power — selects, scores, and explains",
    },
}

# Constitutional doctrine per category — the explicit AGI-layer statement each category makes
CATEGORY_AGI_DOCTRINE: Final[dict[str, str]] = {
    "scar": (
        "Constitutional truth forged through lived suffering; "
        "the last freedom is the choice of attitude."
    ),
    "triumph": (
        "Governing principle that victory is not absence of obstacle "
        "but the capacity forged by overcoming it."
    ),
    "paradox": (
        "Explicit tension holding two truths simultaneously; "
        "the contradiction is the insight."
    ),
    "wisdom": (
        "Epistemic doctrine distilled across centuries: "
        "know the limits of knowing."
    ),
    "power": (
        "Governance principle: collective will made legible "
        "through shared explicit intention."
    ),
    "love": (
        "Constitutional empathy: the relational obligation "
        "to the other as irreducibly real."
    ),
    "seal": (
        "Final constitutional doctrine: the sovereign closure "
        "that makes all prior stages meaningful."
    ),
}

# ── Category centroids in APEX-G space ──────────────────────────────────────
# Each category has a characteristic "home region" in the 6D manifold.
# Individual quotes have small deterministic offsets from the centroid.

CATEGORY_CENTROIDS: Final[dict[str, tuple[float, ...]]] = {
    # (τ,    ΔS,   P²,   G,    Ψ,    κᵣ)
    "scar": (0.80, -0.30, 1.10, 0.78, 0.85, 0.72),
    "triumph": (0.90, -0.60, 1.70, 0.92, 0.75, 0.82),
    "paradox": (0.50, 0.10, 1.20, 0.82, 0.92, 0.60),
    "wisdom": (0.40, -0.40, 1.40, 0.88, 0.97, 0.68),
    "power": (0.60, -0.20, 1.50, 0.90, 0.65, 0.55),
    "love": (0.82, -0.50, 1.85, 0.93, 0.82, 0.95),
    "seal": (0.98, -0.80, 1.95, 0.97, 0.98, 0.90),
}

# ── Floor affinities per category ───────────────────────────────────────────
# A quote's floor affinity boosts its selection score when the corresponding
# constitutional floor is active or relevant in the current session state.

CATEGORY_FLOOR_AFFINITIES: Final[dict[str, list[str]]] = {
    "scar": ["F6", "F7", "F1"],  # Empathy, Humility, Truth
    "triumph": ["F5", "F8", "F3"],  # Craft, Tri-Witness, Stability
    "paradox": ["F4", "F8", "F7"],  # Clarity, Tri-Witness, Humility
    "wisdom": ["F1", "F2", "F7", "F4"],  # Truth, Clarity, Humility, Entropy
    "power": ["F3", "F5", "F11"],  # Stability, Craft, Command Auth
    "love": ["F6", "F13", "F3"],  # Empathy, Sovereign, Stability
    "seal": ["F13", "F11", "F9", "F1"],  # Sovereign, Command, Anti-Hantu, Truth
}

# ── Stage-to-τ mapping ────────────────────────────────────────────────────
# Maps canonical AClip stage numbers to a τ (temporal resonance) value.

STAGE_TAU: Final[dict[int, float]] = {
    0: 0.00,  # 000 INIT
    111: 0.15,  # 111 MIND
    222: 0.25,  # 222 INTEGRATE
    333: 0.35,  # 333 REASON
    444: 0.45,  # 444 FORGE
    555: 0.55,  # 555 HEART
    666: 0.65,  # 666 EMPATHY
    777: 0.75,  # 777 EUREKA
    888: 0.85,  # 888 JUDGE
    999: 0.98,  # 999 SEAL
}


def stage_to_tau(stage: str | int) -> float:
    """
    Convert a stage identifier to its τ (temporal resonance) value.

    Accepts numeric stage (e.g., 666), string stage (e.g., "666_HEART"),
    or any string containing digits.
    """
    try:
        stage_num = int("".join(filter(str.isdigit, str(stage))) or "0")
    except (TypeError, ValueError):
        stage_num = 0

    # Direct match
    if stage_num in STAGE_TAU:
        return STAGE_TAU[stage_num]

    # Interpolate between known checkpoints
    checkpoints = sorted(STAGE_TAU.keys())
    for i in range(len(checkpoints) - 1):
        lo, hi = checkpoints[i], checkpoints[i + 1]
        if lo <= stage_num <= hi:
            frac = (stage_num - lo) / (hi - lo)
            return STAGE_TAU[lo] + frac * (STAGE_TAU[hi] - STAGE_TAU[lo])

    return 0.5


@dataclass
class APEXGCoordinate:
    """
    A point in the 6D APEX-G constitutional manifold.

    Immutable after construction; coordinates are validated on init.
    """

    tau: float  # τ ∈ [0, 1]
    delta_s: float  # ΔS ∈ [-1, 1]
    p2: float  # P² ∈ [0, 2]
    g: float  # G ∈ [0, 1]
    psi: float  # Ψ ∈ [0, 1]
    kappa_r: float  # κᵣ ∈ [0, 1]
    floor_affinities: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        _check("τ", self.tau, 0.0, 1.0)
        _check("ΔS", self.delta_s, -1.0, 1.0)
        _check("P²", self.p2, 0.0, 2.0)
        _check("G", self.g, 0.0, 1.0)
        _check("Ψ", self.psi, 0.0, 1.0)
        _check("κᵣ", self.kappa_r, 0.0, 1.0)

    def as_vector(self) -> tuple[float, ...]:
        """Return the raw 6-float vector for distance calculations."""
        return (self.tau, self.delta_s, self.p2, self.g, self.psi, self.kappa_r)

    def to_dict(self) -> dict[str, float | list[str]]:
        return {
            "tau": self.tau,
            "delta_s": self.delta_s,
            "p2": self.p2,
            "g": self.g,
            "psi": self.psi,
            "kappa_r": self.kappa_r,
            "floor_affinities": self.floor_affinities,
        }

    @classmethod
    def from_dict(cls, d: dict) -> APEXGCoordinate:
        return cls(
            tau=float(d["tau"]),
            delta_s=float(d["delta_s"]),
            p2=float(d["p2"]),
            g=float(d["g"]),
            psi=float(d["psi"]),
            kappa_r=float(d["kappa_r"]),
            floor_affinities=list(d.get("floor_affinities", [])),
        )


def session_state_to_coordinate(
    *,
    stage: str | int = "444",
    delta_s: float = 0.0,
    p2: float = 1.0,
    g_score: float = 0.85,
    psi: float = 0.5,
    kappa_r: float = 0.5,
    active_floors: list[str] | None = None,
) -> APEXGCoordinate:
    """
    Convert runtime session state into an APEX-G coordinate for manifold lookup.

    Args:
        stage:       Current AClip stage (e.g., "666_HEART" or 666).
        delta_s:     Current entropy delta from thermodynamic module.
        p2:          Current peace-squared safety margin.
        g_score:     Current G = A×P×X×E² governance score.
        psi:         Current epistemic depth / uncertainty estimate (Ω₀ proxy).
        kappa_r:     Current empathy coefficient for active session.
        active_floors: Floors currently active/triggered (for floor affinity).

    Returns:
        APEXGCoordinate ready for k-d tree query.
    """
    tau = stage_to_tau(stage)
    return APEXGCoordinate(
        tau=_clamp(tau, 0.0, 1.0),
        delta_s=_clamp(delta_s, -1.0, 1.0),
        p2=_clamp(p2, 0.0, 2.0),
        g=_clamp(g_score, 0.0, 1.0),
        psi=_clamp(psi, 0.0, 1.0),
        kappa_r=_clamp(kappa_r, 0.0, 1.0),
        floor_affinities=list(active_floors or []),
    )


# ── Helpers ──────────────────────────────────────────────────────────────────


def _check(name: str, value: float, lo: float, hi: float) -> None:
    if not lo <= value <= hi:
        raise ValueError(f"APEX-G coordinate {name}={value:.4f} is outside [{lo}, {hi}]")


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


__all__ = [
    "DIM",
    "TAU_IDX",
    "DELTA_S_IDX",
    "P2_IDX",
    "G_IDX",
    "PSI_IDX",
    "KAPPA_R_IDX",
    "AXIS_NAMES",
    "AXIS_DESCRIPTIONS",
    "AXIS_BOUNDS",
    "CATEGORY_CENTROIDS",
    "CATEGORY_FLOOR_AFFINITIES",
    "CATEGORY_POWER_MECHANISMS",
    "CATEGORY_RESONANCE_DENSITY",
    "CATEGORY_AGI_DOCTRINE",
    "LAYER_DESCRIPTIONS",
    "STAGE_TAU",
    "WordPowerMechanism",
    "WisdomLayer",
    "ALL_MECHANISMS",
    "APEXGCoordinate",
    "stage_to_tau",
    "session_state_to_coordinate",
]
