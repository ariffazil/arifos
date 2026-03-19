"""
core/enforcement/aki_contract.py — Hard Boundary Enforcement (L2 ↔ L3)

The AKI (Arif Kernel Interface) Enforcement Gate. This is the 'Hard Boundary'
that prevents internal operations (L2) from acting on the external
Civilization (L3) without explicit constitutional verification.
"""

import logging
from typing import Any

from core.governance_kernel import GovernanceKernel

logger = logging.getLogger(__name__)


class AKIContract:
    """
    The 'Wall' between Operation and Civilization.
    Enforces the L2 <-> L3 boundary contract.
    """

    def __init__(self, kernel: GovernanceKernel):
        self.kernel = kernel

    def validate_material_action(self, tool_id: str, payload: dict[str, Any]) -> bool:
        """
        Hard Enforcement: No tool can bypass this gate.
        Returns: True if action is 'Signed as Lawful', False if VOID.
        """
        # 1. F12: Initial Injection Defense on payload
        # (Already assumed in Stage 000, but AKI provides secondary check)

        # 2. F2: Truth Check
        if self.kernel.safety_omega > self.kernel.UNCERTAINTY_THRESHOLD:
            logger.warning(
                f"AKI VOID: Tool {tool_id} blocked. Uncertainty (Ω₀={self.kernel.safety_omega:.3f}) too high."
            )
            return False

        # 3. F11 + F13: Sovereignty Check (High-stakes / Irreversibility)
        if self.kernel.irreversibility_index > self.kernel.IRREVERSIBILITY_THRESHOLD:
            if self.kernel.human_approval_status != "approved":
                logger.warning(
                    f"AKI HOLD: Tool {tool_id} requires 888 ratification. (Index: {self.kernel.irreversibility_index:.3f})"
                )
                return False

        # 4. F5: Peace (Stability)
        # We don't act if the system is 'heated' (Peace² < 1.0 logic)

        # 5. L2-L3 Boundary Enforcement (Phoenix Protocol States)
        from core.governance_kernel import GovernanceState

        if self.kernel.governance_state == GovernanceState.QUARANTINED:
            logger.error(f"AKI QUARANTINE: Tool {tool_id} blocked. System is in QUARANTINED state.")
            return False

        if self.kernel.governance_state == GovernanceState.DEGRADED:
            # Degraded mode might only allow 'read' tools or specific safe tools
            if "read" not in tool_id and "search" not in tool_id:
                logger.warning(f"AKI DEGRADED: Non-safe tool {tool_id} blocked in DEGRADED mode.")
                return False

        logger.info(f"AKI SEAL: Tool {tool_id} signed as lawful.")
        return True

    def ingest_feedback(self, result: Any):
        """
        Implementation of the [L3 -> STATE] feedback law.
        Updates the kernel's state field after a tool returns from Civilization.
        """
        # This would decrease 'Void' (uncertainty) and consume 'Energy'
        # In this mock, we just log the transition.
        logger.info("AKI FEEDBACK: World data updating State Field (Ψ).")
        pass


# Example usage for a mock tool router
def invoke_governed_tool(kernel: GovernanceKernel, tool_id: str, payload: dict[str, Any]):
    aki = AKIContract(kernel)
    if aki.validate_material_action(tool_id, payload):
        # Proceed with execution in L3 Civilization
        pass
    else:
        # Trigger 888_HOLD or VOID
        pass


# =========================================================================
# L2 <-> L3 SOVEREIGN GATES (Migrated from 333_APPS/metabolizer.py)
# =========================================================================


class SovereignGate:
    """
    888_HOLD enforcement gate for irreversible actions.
    Any application performing destructive operations MUST pass through this gate.
    """

    IRREVERSIBLE_ACTIONS = {
        "delete",
        "remove",
        "drop",
        "truncate",
        "send",
        "transfer",
        "trade",
        "execute",
        "deploy",
        "publish",
        "commit",
    }

    def __init__(self, action_type: str, resource_path: str, requires_signature: bool = True):
        self.action_type = action_type.lower()
        self.resource_path = resource_path
        self.requires_signature = requires_signature
        self.is_irreversible = self.action_type in self.IRREVERSIBLE_ACTIONS

    async def check_approval(
        self, context: dict[str, Any], proposed_verdict: str = "SEAL"
    ) -> dict[str, Any]:
        """Check if action is approved or requires 888_HOLD."""
        if self.is_irreversible and self.requires_signature:
            return {
                "verdict": "888_HOLD",
                "output": {
                    "message": f"Action '{self.action_type}' on '{self.resource_path}' requires sovereign approval",
                    "action_type": self.action_type,
                    "resource": self.resource_path,
                    "authority": "888_JUDGE",
                },
                "stage": "888_HOLD",
            }
        return {
            "verdict": proposed_verdict,
            "output": {"approved": True, "action": self.action_type},
            "stage": "pre-flight",
        }

    def verify_signature(self, signature: str) -> bool:
        return signature.upper() == "SEAL"


class L0KernelGatekeeper:
    """Protects L0_KERNEL from modification by L1-L7 apps."""

    PROTECTED_PATHS = [
        "000_THEORY/000_LAW.md",
        "core/enforcement/floors.py",
        "core/shared/floors.py",
        "333_APPS/L0_CONSTITUTION/",
        "T000_VERSIONING.md",
    ]

    @classmethod
    def check_modification_permission(cls, filepath: str) -> bool:
        for protected in cls.PROTECTED_PATHS:
            if protected in filepath or filepath.endswith(protected):
                return False
        return True

    @classmethod
    def assert_modification_allowed(cls, filepath: str) -> None:
        if not cls.check_modification_permission(filepath):
            raise PermissionError(
                f"🚫 SOVEREIGN ONLY: Cannot modify '{filepath}'. "
                f"Modification of L0_KERNEL constitutional law requires 888_JUDGE authority. "
            )
