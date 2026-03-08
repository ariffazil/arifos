"""
L0 Constitution — 13-Floor Kernel Re-exports.

This sub-package re-exports the constitutional governance modules that
live directly in ``core/``.  Import from here or from ``core.*``
directly — both paths work.

Example::

    from core.l0_constitution import GovernanceKernel, THRESHOLDS
    # equivalent to:
    from core.governance_kernel import GovernanceKernel
    from core.shared.floors import THRESHOLDS
"""

from __future__ import annotations

# Governance kernel
from core.governance_kernel import GovernanceKernel, get_governance_kernel  # noqa: F401

# Constitutional floors
from core.shared.floors import THRESHOLDS  # noqa: F401

# Physics engine
try:
    from core.physics.thermodynamics_hardened import (  # noqa: F401
        ThermodynamicEngine,
    )
except ImportError:
    pass

# Judgment
from core.judgment import JudgmentKernel as JudgmentEngine  # noqa: F401

__all__ = [
    "GovernanceKernel",
    "get_governance_kernel",
    "THRESHOLDS",
    "JudgmentEngine",
]
