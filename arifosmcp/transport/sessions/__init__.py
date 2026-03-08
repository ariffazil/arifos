"""
arifosmcp.transport.sessions — Session Management & VAULT999 Persistence

This module provides:
- LifecycleManager: Constitutional session state machine (INIT → ACTIVE → VOID)
- KernelState: Session state enum (INIT_000, ACTIVE, SABAR_72, HOLD_888, VOID)
- SessionLedger: Postgres-backed VAULT999 ledger
- SessionDependency: Session dependency injection for FastAPI/Starlette

Aligned with spec: Session management belongs in arifosmcp.transport (governed transport),
not in arifosmcp.intelligence (sensory infrastructure).

DITEMPA BUKAN DIBERI
"""

from .lifecycle import KernelState, LifecycleManager, Session

__all__ = [
    # Session Lifecycle (moved from arifosmcp.intelligence per spec)
    "KernelState",
    "LifecycleManager",
    "Session",
    # VAULT999 Persistence
    "SessionLedger",
    "get_session_ledger",
]


def __getattr__(name: str):
    """Avoid importing ledger backends unless callers actually need them."""
    if name == "SessionLedger":
        from .session_ledger import SessionLedger

        return SessionLedger
    if name == "get_session_ledger":
        from .session_dependency import get_session_ledger

        return get_session_ledger
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
