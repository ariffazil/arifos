"""
codebase/mcp/sessions/session_dependency.py - Session Store Stub (v55)

Minimal stub for session persistence.
Provides SessionStore for F1 (Amanah) session tracking.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class SessionStore:
    """
    Stores and retrieves session data for constitutional workflows.
    
    F1 Amanah: Ensures session state is preserved for audit and
    potential rollback operations.
    """
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path("./runtime/sessions")
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._sessions: Dict[str, Dict[str, Any]] = {}
    
    def get(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data by ID."""
        # Try memory first
        if session_id in self._sessions:
            return self._sessions[session_id]
        
        # Try disk
        session_file = self.storage_path / f"{session_id}.json"
        if session_file.exists():
            try:
                with open(session_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Failed to load session {session_id}: {e}")
        
        return None
    
    def set(self, session_id: str, data: Dict[str, Any]) -> bool:
        """Store session data."""
        self._sessions[session_id] = data
        
        # Persist to disk
        session_file = self.storage_path / f"{session_id}.json"
        try:
            with open(session_file, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except IOError as e:
            logger.error(f"Failed to save session {session_id}: {e}")
            return False
    
    def exists(self, session_id: str) -> bool:
        """Check if session exists."""
        return session_id in self._sessions or (self.storage_path / f"{session_id}.json").exists()
    
    def list_sessions(self) -> list:
        """List all active session IDs."""
        return list(self._sessions.keys())


def get_session_store() -> SessionStore:
    """Get global session store instance."""
    return SessionStore()
