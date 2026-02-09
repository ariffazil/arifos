"""
shared/ — Constitutional Physics & Utilities

The 4 Shared Modules:
    physics.py  — W_3, delta_S, Omega_0, pi, Peace2, kappa_r, G
    atlas.py    — Lambda(), Theta(), Phi()
    types.py    — Pydantic contracts
    crypto.py   — Ed25519, SHA-256, Merkle
    guards.py   — F9/F10 guards
"""

from .physics import (
    # F3: Tri-Witness
    TrinityTensor,
    W_3,
    W_3_from_tensor,
    W_3_check,
    
    # Utilities
    geometric_mean,
    std_dev,
    
    # F4: Thermodynamic Clarity
    delta_S,
    is_cooling,
    clarity_ratio,
    
    # F7: Humility
    UncertaintyBand,
    Omega_0,
    
    # Precision
    pi,
    kalman_gain,
    
    # F5: Peace
    PeaceSquared,
    Peace2,
    
    # F6: Empathy
    Stakeholder,
    kappa_r,
    identify_stakeholders,
    DISTRESS_SIGNALS,
    
    # F8: Genius
    GeniusDial,
    G,
    G_from_dial,
    
    # Unified state
    ConstitutionalTensor,
)

from .atlas import (
    Lane,
    GPV,
    Lambda,
    Theta,
    Phi,
    ATLAS,
    classify,
    route,
)

# Import types if available (may not be fully implemented)
try:
    from .types import (
        Verdict,
        ThoughtNode,
        ThoughtChain,
        FloorScores,
        AgiMetrics,
        AsiMetrics,
        ApexMetrics,
    )
    TYPES_AVAILABLE = True
except ImportError:
    TYPES_AVAILABLE = False

# Import crypto if available
try:
    from .crypto import (
        generate_session_id,
        sha256_hash,
        sha256_hash_dict,
        ed25519_sign,
        ed25519_verify,
        merkle_root,
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
    "geometric_mean",
    "std_dev",
    "delta_S",
    "is_cooling",
    "clarity_ratio",
    "UncertaintyBand",
    "Omega_0",
    "pi",
    "kalman_gain",
    "PeaceSquared",
    "Peace2",
    "Stakeholder",
    "kappa_r",
    "identify_stakeholders",
    "DISTRESS_SIGNALS",
    "GeniusDial",
    "G",
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
]

# Add types to __all__ if available
if TYPES_AVAILABLE:
    __all__.extend([
        "Verdict",
        "ThoughtNode",
        "ThoughtChain",
        "FloorScores",
        "AgiMetrics",
        "AsiMetrics",
        "ApexMetrics",
    ])

# Add crypto to __all__ if available
if CRYPTO_AVAILABLE:
    __all__.extend([
        "generate_session_id",
        "sha256_hash",
        "sha256_hash_dict",
        "ed25519_sign",
        "ed25519_verify",
        "merkle_root",
    ])

# Add guards to __all__ if available
if GUARDS_AVAILABLE:
    __all__.extend([
        "detect_hantu",
        "validate_ontology",
    ])
