"""
core/philosophy/ — APEX-G 6D Quote Manifold

Provides geometric wisdom selection in constitutional space (τ, ΔS, P², G, Ψ, κᵣ).
Includes word-power theory: neural_simulation, symbolic_compression, coordination,
attention_steering, and resonance_density (ρ).
"""

from .coordinates import (
    ALL_MECHANISMS,
    CATEGORY_AGI_DOCTRINE,
    CATEGORY_CENTROIDS,
    CATEGORY_FLOOR_AFFINITIES,
    CATEGORY_POWER_MECHANISMS,
    CATEGORY_RESONANCE_DENSITY,
    DIM,
    LAYER_DESCRIPTIONS,
    APEXGCoordinate,
    WisdomLayer,
    WordPowerMechanism,
    session_state_to_coordinate,
    stage_to_tau,
)
from .manifold import (
    DEFAULT_K_NEIGHBOURS,
    FLOOR_AFFINITY_BONUS,
    RESONANCE_BONUS_WEIGHT,
    QuoteManifold,
    QuoteSelection,
    get_manifold,
    select_wisdom,
)

__all__ = [
    # coordinates
    "APEXGCoordinate",
    "CATEGORY_AGI_DOCTRINE",
    "CATEGORY_CENTROIDS",
    "CATEGORY_FLOOR_AFFINITIES",
    "CATEGORY_POWER_MECHANISMS",
    "CATEGORY_RESONANCE_DENSITY",
    "DIM",
    "LAYER_DESCRIPTIONS",
    "WordPowerMechanism",
    "WisdomLayer",
    "ALL_MECHANISMS",
    "session_state_to_coordinate",
    "stage_to_tau",
    # manifold
    "QuoteManifold",
    "QuoteSelection",
    "DEFAULT_K_NEIGHBOURS",
    "FLOOR_AFFINITY_BONUS",
    "RESONANCE_BONUS_WEIGHT",
    "get_manifold",
    "select_wisdom",
]
