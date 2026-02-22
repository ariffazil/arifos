"""
arifOS Human-AI Interface SDK for Python

Constitutional governance SDK for AI agents and human operators.
Provides Human-in-the-Loop (HITL) integration with 13-floor enforcement.

Basic Usage:
    import arifos_sdk as arifos

    # Initialize session with human identity
    session = arifos.Session(
        actor_id="arif@arif-fazil.com",
        actor_type="human",
        groups=["platform-engineers"],
    )

    # Check action constitutionally
    result = await session.check_action(
        tool="k8s_apply",
        payload={"manifest": "...", "namespace": "prod"},
    )

    # Handle 888_HOLD
    if result.verdict == "888_HOLD":
        # Wait for human approval (blocking)
        final = await session.await_human_approval(result.hold_id)
        if final.verdict == "SEAL":
            # Proceed with operation
            pass

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from .client import ArifOSClient, Session
from .decorators import constitutional_infra_write, constitutional_read_only, requires_f13
from .exceptions import (
    ArifOSError,
    FloorViolationError,
    GatewayConnectionError,
    HumanApprovalTimeoutError,
)
from .types import (
    BlastRadius,
    FloorResult,
    GatewayDecision,
    HumanApprovalRequest,
    HumanApprovalResponse,
    Verdict,
)

__version__ = "60.2.0"
__all__ = [
    # Client
    "ArifOSClient",
    "Session",
    # Decorators
    "requires_f13",
    "constitutional_infra_write",
    "constitutional_read_only",
    # Types
    "Verdict",
    "FloorResult",
    "GatewayDecision",
    "HumanApprovalRequest",
    "HumanApprovalResponse",
    "BlastRadius",
    # Exceptions
    "ArifOSError",
    "FloorViolationError",
    "HumanApprovalTimeoutError",
    "GatewayConnectionError",
]
