"""core/intelligence - 333_MIND: AGI reasoning and Tri-Witness metrics.

This module provides the ATLAS stage (333) implementations:
- Delta bundle assembly (AGI output packaging)
- Paradox detection (F7 contradiction scanning)
- Entropy calculation (F4 clarity measurement)
- Humility scoring (F7 Ω₀ calculation)
- Tri-Witness evaluation (F3 consensus)
- Genius scoring (F8 wisdom)
- Scar tracking (unresolved contradictions)
- Clarity optimization (F4 entropy reduction)
"""

from .delta_bundle import assemble_delta_bundle
from .paradox import scan_for_paradoxes
from .entropy import measure_entropy
from .humility import calculate_omega_zero
from .tri_witness import compute_w3

__all__ = [
    # Delta Bundle (AGI output packaging)
    "assemble_delta_bundle",
    # Paradox Detection (F7)
    "scan_for_paradoxes",
    # Entropy (F4 Clarity)
    "measure_entropy",
    # Humility (F7)
    "calculate_omega_zero",
    # Tri-Witness (F3)
    "compute_w3",
]
