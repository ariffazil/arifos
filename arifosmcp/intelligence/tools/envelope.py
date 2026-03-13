"""
Unified Tool Output Envelope — MGI (Machine, Governance, Intelligence)

This module enforces the 3-layer GovernedResponse envelope on all tools.
Ensures F3 Quad-Witness compliance by structuring output through:
- Machine Layer: Status, issue labels, physical state
- Governance Layer: Verdict, authority, trace
- Intelligence Layer: Metrics, exploration/entropy/eureka state
"""

from __future__ import annotations

import functools
from collections.abc import Callable

from arifosmcp.runtime.models import (
    CallerContext,
    CanonicalAuthority,
    CanonicalError,
    CanonicalMetrics,
    MachineIssueLabel,
    MachineState,
    RuntimeEnvelope,
    RuntimeStatus,
    Verdict,
)


def unified_tool_output(
    tool_name: str | None = None,
    stage: str = "444_ROUTER",
    default_verdict: Verdict = Verdict.SEAL,
) -> Callable:
    """
    Decorator that forces tool output into RuntimeEnvelope (MGI structure).

    Args:
        tool_name: Name of the tool (auto-detected from function name if None)
        stage: Metabolic stage identifier (default: 444_ROUTER for tools)
        default_verdict: Default verdict for successful execution

    Returns:
        Decorated function that always returns RuntimeEnvelope
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> RuntimeEnvelope:
            # Auto-detect tool name from function
            detected_name = tool_name or func.__name__

            # Extract caller_context from kwargs if present
            caller_ctx = kwargs.get("caller_context")
            auth_ctx = kwargs.get("auth_context", {})
            session_id = kwargs.get("session_id")

            try:
                # Execute the actual tool function
                raw_result = func(*args, **kwargs)

                # If already a RuntimeEnvelope, return as-is
                if isinstance(raw_result, RuntimeEnvelope):
                    return raw_result

                # If dict with envelope-like structure, unwrap and re-wrap properly
                if isinstance(raw_result, dict):
                    # Extract verdict if provided by tool
                    verdict_str = raw_result.get("verdict", default_verdict.value)
                    verdict = (
                        Verdict(verdict_str) if isinstance(verdict_str, str) else default_verdict
                    )

                    # Map ok/status to machine state
                    ok = raw_result.get("ok", True)
                    status_str = raw_result.get("status", "SUCCESS" if ok else "ERROR")
                    status = (
                        RuntimeStatus(status_str)
                        if isinstance(status_str, str)
                        else (RuntimeStatus.SUCCESS if ok else RuntimeStatus.ERROR)
                    )

                    # Determine machine state
                    if status == RuntimeStatus.SUCCESS:
                        machine_state = MachineState.READY
                    elif status == RuntimeStatus.TIMEOUT:
                        machine_state = MachineState.DEGRADED
                    else:
                        machine_state = MachineState.FAILED if not ok else MachineState.READY

                    # Extract issue label if present
                    issue_label = raw_result.get("issue")
                    machine_issue = MachineIssueLabel(issue_label) if issue_label else None

                    # Build errors list if error present
                    errors = []
                    if "error" in raw_result and raw_result["error"]:
                        error_msg = str(raw_result["error"])
                        error_code = raw_result.get("issue", "TOOL_ERROR")
                        errors.append(
                            CanonicalError(
                                code=error_code,
                                message=error_msg,
                                stage=stage,
                                recoverable=verdict not in (Verdict.VOID, Verdict.HOLD_888),
                            )
                        )

                    # Extract payload (everything that's not metadata)
                    payload_keys = {"ok", "verdict", "status", "error", "issue", "trace"}
                    payload = {k: v for k, v in raw_result.items() if k not in payload_keys}

                    # Build the RuntimeEnvelope
                    return RuntimeEnvelope(
                        ok=ok,
                        tool=detected_name,
                        session_id=session_id,
                        stage=stage,
                        verdict=verdict,
                        status=status,
                        machine_status=machine_state,
                        machine_issue=machine_issue,
                        metrics=CanonicalMetrics(
                            confidence=1.0 if ok else 0.0,
                            vitality=1.0 if machine_state == MachineState.READY else 0.5,
                            risk=0.0 if ok else 0.7,
                        ),
                        payload=payload,
                        errors=errors,
                        authority=CanonicalAuthority(
                            actor_id=auth_ctx.get("actor_id", "anonymous"),
                            level=auth_ctx.get("authority_level", "anonymous"),
                            human_required=verdict in (Verdict.HOLD, Verdict.HOLD_888),
                        ),
                        caller_context=caller_ctx
                        if isinstance(caller_ctx, CallerContext)
                        else None,
                        auth_context=auth_ctx if auth_ctx else None,
                    )

                # For any other return type, wrap as payload
                return RuntimeEnvelope(
                    ok=True,
                    tool=detected_name,
                    session_id=session_id,
                    stage=stage,
                    verdict=default_verdict,
                    status=RuntimeStatus.SUCCESS,
                    machine_status=MachineState.READY,
                    payload={"result": raw_result},
                    caller_context=caller_ctx if isinstance(caller_ctx, CallerContext) else None,
                    auth_context=auth_ctx if auth_ctx else None,
                )

            except Exception as e:
                # Even exceptions get wrapped in RuntimeEnvelope — never escape naked
                return RuntimeEnvelope(
                    ok=False,
                    tool=detected_name,
                    session_id=session_id,
                    stage=stage,
                    verdict=Verdict.HOLD,  # Never VOID for mechanical failures
                    status=RuntimeStatus.ERROR,
                    machine_status=MachineState.FAILED,
                    machine_issue=MachineIssueLabel.INTERNAL_RUNTIME_ERROR,
                    metrics=CanonicalMetrics(
                        confidence=0.0,
                        vitality=0.0,
                        risk=0.9,
                    ),
                    errors=[
                        CanonicalError(
                            code="TOOL_EXCEPTION",
                            message=str(e),
                            stage=stage,
                            recoverable=False,
                        )
                    ],
                    authority=CanonicalAuthority(
                        actor_id=auth_ctx.get("actor_id", "anonymous") if auth_ctx else "anonymous",
                        level="anonymous",
                        human_required=True,  # Exception requires human review
                    ),
                    caller_context=caller_ctx if isinstance(caller_ctx, CallerContext) else None,
                    auth_context=auth_ctx if auth_ctx else None,
                )

        return wrapper

    return decorator


# Convenience partials for common tool patterns
seal_tool = functools.partial(unified_tool_output, default_verdict=Verdict.SEAL)
sabar_tool = functools.partial(unified_tool_output, default_verdict=Verdict.SABAR)
hold_tool = functools.partial(unified_tool_output, default_verdict=Verdict.HOLD)
