"""
core/recovery/rollback_engine.py — Governance State Restoration

Provides the ability to repair or rollback the GovernanceKernel (Ψ)
to a known healthy state if a session reaches 'Homeostatic Collapse'.
"""

import copy
import logging

from core.governance_kernel import GovernanceKernel

logger = logging.getLogger(__name__)


class RollbackEngine:
    """
    Constitutional State Repair.
    Ensures that truth remains immutable even if reasoning fails.
    """

    def __init__(self):
        self._checkpoints: dict[str, list[GovernanceKernel]] = {}
        self._max_history = 5

    def create_checkpoint(self, session_id: str, kernel: GovernanceKernel):
        """Save a snapshot of the current governance state."""
        if session_id not in self._checkpoints:
            self._checkpoints[session_id] = []

        # Perform deep copy to ensure isolation
        snapshot = copy.deepcopy(kernel)
        self._checkpoints[session_id].append(snapshot)

        # Keep only the last N checkpoints
        if len(self._checkpoints[session_id]) > self._max_history:
            self._checkpoints[session_id].pop(0)

    def rollback(self, session_id: str) -> GovernanceKernel | None:
        """
        Restore the kernel to the previous healthy checkpoint.
        Use this when HomeostaticCollapse exception is raised.
        """
        if session_id not in self._checkpoints or not self._checkpoints[session_id]:
            logger.error(f"No checkpoints found for session {session_id}. Rollback failed.")
            return None

        # The last checkpoint is the current failing state, so take the one before it
        if len(self._checkpoints[session_id]) >= 2:
            self._checkpoints[session_id].pop()  # Remove current bad state
            healthy_state = self._checkpoints[session_id][-1]
            logger.info(f"Session {session_id} rolled back to previous checkpoint.")
            return copy.deepcopy(healthy_state)

        return None


# Global singleton
rollback_engine = RollbackEngine()
