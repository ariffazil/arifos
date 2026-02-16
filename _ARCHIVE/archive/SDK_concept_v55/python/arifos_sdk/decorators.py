"""
Decorators for arifOS SDK.

Provides convenient decorators for constitutional enforcement.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import functools
import inspect
from typing import Any, Callable, Optional, TypeVar

from .client import ArifOSClient, Session
from .exceptions import FloorViolationError, HumanApprovalRequiredError
from .types import GatewayDecision, Verdict

F = TypeVar("F", bound=Callable[..., Any])


def requires_f13(
    timeout: Optional[float] = 3600.0,
    notify_channels: Optional[list] = None,
):
    """
    Decorator: Require F13 Sovereign (human approval) for function.

    Usage:
        @requires_f13(timeout=7200)
        async def deploy_to_production(manifest: str):
            # This will trigger 888_HOLD if not pre-approved
            pass

    Args:
        timeout: Seconds to wait for human approval
        notify_channels: Where to send approval notifications

    Raises:
        HumanApprovalRequiredError: If approval needed but not awaited
        HumanApprovalTimeoutError: If timeout waiting for approval
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Extract session from args or kwargs
            session = _extract_session(args, kwargs)
            if not session:
                raise ValueError(
                    f"@requires_f13 requires a Session argument. "
                    f"Use: async def func(session: Session, ...)"
                )

            # The function itself should call check_action
            # We wrap to ensure 888_HOLD handling
            try:
                result = await func(*args, **kwargs)

                # If result is GatewayDecision with 888_HOLD, wait for approval
                if isinstance(result, GatewayDecision) and result.requires_human_approval:
                    approval_req = await session.request_approval(
                        result,
                        notify=notify_channels,
                    )

                    # Wait for human
                    final = await session.await_approval(approval_req.hold_id, timeout)

                    if not final.is_approved:
                        raise FloorViolationError(
                            f"F13 Sovereign: Human rejected the operation. "
                            f"Reason: {final.rejection_reason}"
                        )

                    # Return final decision
                    return final

                return result

            except Exception:
                raise

        # Handle sync functions
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:

            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                raise RuntimeError("@requires_f13 only works with async functions")

            return sync_wrapper

    return decorator


def constitutional_infra_write(
    auto_approve_staging: bool = True,
    require_attestation_for_prod: bool = True,
):
    """
    Decorator: Mark function as infrastructure write operation.

    Automatically:
    - Classifies tool as "infra_write"
    - Triggers F1, F2, F6, F10, F11, F12 floors
    - 888_HOLD for production if not auto-approved

    Usage:
        @constitutional_infra_write()
        async def update_config(session: Session, config: dict):
            return await session.check_action("k8s_apply", config)
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Add metadata to function
            func._arifos_tool_class = "infra_write"
            func._arifos_auto_approve_staging = auto_approve_staging
            func._arifos_require_attestation = require_attestation_for_prod

            return await func(*args, **kwargs)

        return wrapper

    return decorator


def constitutional_read_only():
    """
    Decorator: Mark function as read-only operation.

    Only enforces F11 (Authority) and F12 (Defense).
    Never triggers 888_HOLD.

    Usage:
        @constitutional_read_only()
        async def get_status(session: Session):
            return await session.check_action("k8s_get", {...})
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            func._arifos_tool_class = "read_only"
            return await func(*args, **kwargs)

        return wrapper

    return decorator


def human_as_tool(
    contact_method: str = "slack",
    contact_id: Optional[str] = None,
):
    """
    Decorator: Treat human as a tool in the workflow.

    Similar to HumanLayer's `human_as_tool` pattern.

    Usage:
        @human_as_tool(contact_method="email", contact_id="oncall@company.com")
        async def ask_oncall(session: Session, question: str):
            # This will send question to oncall and wait for response
            pass

    This creates an 888_HOLD that expects human input as the "return value".
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            session = _extract_session(args, kwargs)
            if not session:
                raise ValueError("@human_as_tool requires a Session argument")

            # Create human-as-tool request
            # This is a special 888_HOLD that expects human input
            hold_payload = {
                "type": "human_as_tool",
                "contact_method": contact_method,
                "contact_id": contact_id,
                "question": kwargs.get("question", "Human input required"),
            }

            # Request would be sent to human, response returned
            # Placeholder: actual implementation would integrate with
            # Slack/email/whatever
            raise NotImplementedError("human_as_tool integration pending")

        return wrapper

    return decorator


def _extract_session(args: tuple, kwargs: dict) -> Optional[Session]:
    """Extract Session from function arguments."""
    # Check kwargs first
    if "session" in kwargs:
        session = kwargs["session"]
        if isinstance(session, Session):
            return session

    # Check args
    for arg in args:
        if isinstance(arg, Session):
            return arg

    return None


# Convenience re-exports for common patterns
__all__ = [
    "requires_f13",
    "constitutional_infra_write",
    "constitutional_read_only",
    "human_as_tool",
]
