"""
AGI (Mind/Δ) — v53.5.0 WIRED

Live Engine: engine_hardened.py (AGIEngineHardened)
Stages: 111 SENSE → 222 THINK → 333 FORGE

Modules:
    precision.py            - Kalman-style precision weighting (P1)
    hierarchy.py            - 5-level cortical encoding (P2)
    action.py               - EFE minimization action selection (P3)
    trinity_sync.py         - 333 AGI↔ASI 6-paradox convergence
    trinity_sync_hardened.py - Hardened sync with geometric synthesis
    engine_hardened.py      - Full hardened pipeline (LIVE)

DITEMPA BUKAN DIBERI - Forged, Not Given
"""

import logging as _logging

_agi_init_logger = _logging.getLogger("codebase.agi")

# v55.5: Consolidated engine (engine_hardened merged into engine.py)
from .engine import AGIEngineHardened, execute_agi_hardened

AGIEngine = AGIEngineHardened
execute_agi = execute_agi_hardened

from .action import (
    ActionPolicy,
    ActionType,
    BeliefState,
    ExpectedFreeEnergyCalculator,
    MotorOutput,
    compute_action_policy,
    execute_action,
)
from .hierarchy import (
    HierarchicalBelief,
    HierarchicalEncoder,
    HierarchyLevel,
    encode_hierarchically,
    get_cumulative_delta_s,
)

# v53.4.0: Gap modules (wired into engine_hardened pipeline)
from .precision import (
    PrecisionEstimate,
    PrecisionWeighter,
    cosine_similarity,
    estimate_precision,
    update_belief_with_precision,
)

# v53.4.0: Trinity Sync (333 convergence)
from .trinity_sync import PARADOXES, ConvergenceResult, TrinitySync, trinity_sync
from .trinity_sync_hardened import TrinitySyncHardened, compute_trinity_score, synthesize_paradox

# Legacy engine + kernel (safe import — may depend on archived modules)
# [REMOVED] Legacy imports archived in v55.5

# Backward compat alias
AGIKernel = None

__version__ = "v53.5.0-WIRED"

__all__ = [
    # Live engine
    "AGIEngineHardened",
    "execute_agi_hardened",
    # Legacy compatibility aliases
    "AGIEngine",
    "execute_agi",
    # Precision (P1)
    "PrecisionEstimate",
    "PrecisionWeighter",
    "estimate_precision",
    "update_belief_with_precision",
    "cosine_similarity",
    # Hierarchy (P2)
    "HierarchyLevel",
    "HierarchicalBelief",
    "HierarchicalEncoder",
    "encode_hierarchically",
    "get_cumulative_delta_s",
    # Active Inference (P3)
    "ActionType",
    "ActionPolicy",
    "BeliefState",
    "ExpectedFreeEnergyCalculator",
    "MotorOutput",
    "compute_action_policy",
    "execute_action",
    # Trinity Sync
    "TrinitySync",
    "ConvergenceResult",
    "trinity_sync",
    "PARADOXES",
    "TrinitySyncHardened",
    "synthesize_paradox",
    "compute_trinity_score",
    "__version__",
]
__all__ = [
    # Live engine
    "AGIEngineHardened",
    "execute_agi_hardened",
    # Legacy compatibility aliases
    "AGIEngine",
    "execute_agi",
    # Precision (P1)
    "PrecisionEstimate",
    "PrecisionWeighter",
    "estimate_precision",
    "update_belief_with_precision",
    "cosine_similarity",
    # Hierarchy (P2)
    "HierarchyLevel",
    "HierarchicalBelief",
    "HierarchicalEncoder",
    "encode_hierarchically",
    "get_cumulative_delta_s",
    # Active Inference (P3)
    "ActionType",
    "ActionPolicy",
    "BeliefState",
    "ExpectedFreeEnergyCalculator",
    "MotorOutput",
    "compute_action_policy",
    "execute_action",
    # Trinity Sync
    "TrinitySync",
    "ConvergenceResult",
    "trinity_sync",
    "PARADOXES",
    "TrinitySyncHardened",
    "synthesize_paradox",
    "compute_trinity_score",
    "__version__",
]
