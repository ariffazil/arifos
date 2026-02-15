"""
Session Dependency — FastAPI/Starlette dependency injection for sessions.

Provides request-scoped session management.

DITEMPA BUKAN DIBERI
"""

from typing import Optional
from .session_ledger import SessionLedger, get_ledger


# Singleton ledger instance
_session_ledger: Optional[SessionLedger] = None


async def get_session_ledger() -> SessionLedger:
    """
    Dependency for getting the SessionLedger.
    
    Usage in FastAPI:
        @app.post("/seal")
        async def seal_entry(ledger: SessionLedger = Depends(get_session_ledger)):
            ...
    """
    global _session_ledger
    if _session_ledger is None:
        _session_ledger = await get_ledger()
    return _session_ledger


def reset_session_ledger():
    """Reset the session ledger (for testing)."""
    global _session_ledger
    _session_ledger = None
