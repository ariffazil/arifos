"""
shared/ — Constitutional Physics & Utilities

The 4 Shared Modules:
    physics.py  — W_3, delta_S, Omega_0, pi, Peace2, kappa_r, G
    atlas.py    — Lambda(), Theta(), Phi()
    types.py    — Pydantic contracts
    crypto.py   — Ed25519, SHA-256, Merkle
    guards.py   — F9/F10 guards
"""

from .atlas import (
    ATLAS,
    GPV,
    Lambda,
    Lane,
    Phi,
    Theta,
    classify,
    classify_query,
    route,
    route_query,
)
from .physics import (
    DISTRESS_SIGNALS,
    W_3,
    # Unified state
    ConstitutionalTensor,
    G,
    G_from_dial,
    # F8: Genius
    GeniusDial,
    Omega_0,
    Peace2,
    # F5: Peace
    PeaceSquared,
    # F6: Empathy
    Stakeholder,
    # F3: Tri-Witness
    TrinityTensor,
    # F7: Humility
    UncertaintyBand,
    W_3_check,
    W_3_from_tensor,
    clarity_ratio,
    # F4: Thermodynamic Clarity
    delta_S,
    empathy_coeff,
    entropy_delta,
    genius_score,
    # Utilities
    geometric_mean,
    humility_band,
    identify_stakeholders,
    is_cooling,
    kalman_gain,
    kappa_r,
    peace_squared,
    # Precision
    pi,
    std_dev,
    tri_witness,
)

# Import types if available (may not be fully implemented)
try:
    from .types import (
        AgiMetrics,
        ApexMetrics,
        AsiMetrics,
        FloorScores,
        ThoughtChain,
        ThoughtNode,
        Verdict,
    )

    TYPES_AVAILABLE = True
except ImportError:
    TYPES_AVAILABLE = False

# Import crypto if available
try:
    from .crypto import (
        ed25519_sign,
        ed25519_verify,
        generate_session_id,
        merkle_root,
        sha256_hash,
        sha256_hash_dict,
    )

    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

# Import guards if available
try:
    from .guards import (
        detect_hantu,
        validate_ontology,
    )

    GUARDS_AVAILABLE = True
except ImportError:
    GUARDS_AVAILABLE = False

__all__ = [
    # Physics
    "TrinityTensor",
    "W_3",
    "W_3_from_tensor",
    "W_3_check",
    "tri_witness",
    "geometric_mean",
    "std_dev",
    "delta_S",
    "entropy_delta",
    "is_cooling",
    "clarity_ratio",
    "UncertaintyBand",
    "Omega_0",
    "humility_band",
    "pi",
    "kalman_gain",
    "PeaceSquared",
    "Peace2",
    "peace_squared",
    "Stakeholder",
    "kappa_r",
    "empathy_coeff",
    "identify_stakeholders",
    "DISTRESS_SIGNALS",
    "GeniusDial",
    "G",
    "genius_score",
    "G_from_dial",
    "ConstitutionalTensor",
    # ATLAS
    "Lane",
    "GPV",
    "Lambda",
    "Theta",
    "Phi",
    "ATLAS",
    "classify",
    "route",
    "classify_query",
    "route_query",
]

# Add types to __all__ if available
if TYPES_AVAILABLE:
    __all__.extend(
        [
            "Verdict",
            "ThoughtNode",
            "ThoughtChain",
            "FloorScores",
            "AgiMetrics",
            "AsiMetrics",
            "ApexMetrics",
        ]
    )

# Add crypto to __all__ if available
if CRYPTO_AVAILABLE:
    __all__.extend(
        [
            "generate_session_id",
            "sha256_hash",
            "sha256_hash_dict",
            "ed25519_sign",
            "ed25519_verify",
            "merkle_root",
        ]
    )

# Add guards to __all__ if available
if GUARDS_AVAILABLE:
    __all__.extend(
        [
            "detect_hantu",
            "validate_ontology",
        ]
    )
