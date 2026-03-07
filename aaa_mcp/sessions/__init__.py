"""
aaa_mcp.sessions — Session Management & VAULT999 Persistence

This module provides:
- LifecycleManager: Constitutional session state machine (INIT → ACTIVE → VOID)
- KernelState: Session state enum (INIT_000, ACTIVE, SABAR_72, HOLD_888, VOID)
- SessionLedger: Postgres-backed VAULT999 ledger
- SessionDependency: Session dependency injection for FastAPI/Starlette

Aligned with spec: Session management belongs in aaa_mcp (governed transport),
not in aclip_cai (sensory infrastructure).

DITEMPA BUKAN DIBERI
"""

from .lifecycle import KernelState, LifecycleManager, Session
from .session_dependency import get_session_ledger
from .session_ledger import SessionLedger

__all__ = [
    # Session Lifecycle (moved from aclip_cai per spec)
    "KernelState",
    "LifecycleManager",
    "Session",
    # VAULT999 Persistence
    "SessionLedger",
    "get_session_ledger",
]
