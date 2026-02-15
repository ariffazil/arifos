"""
arifos.core/guards/session_dependency.py

arifOS Session Dependency Guard

Purpose:
    Provide a lightweight, PERSISTENT guard for long-horizon behaviour.
    
    While the main constitutional floors (F1-F9) govern each response,
    this guard operates at the session level to detect potential
    overuse or parasocial dependency patterns.

Design:
    - JSON-based persistence (codebase/data/sessions/session_store.json)
    - Simple heuristics:
        * Duration threshold (minutes)
        * Interaction count threshold
    - Returns a small dict with status and guidance:
        * PASS  -> within bounds
        * WARN  -> high frequency, suggest a break
        * SABAR -> long session, recommend pausing

Motto:
    "Even water is poison in excess."
"""

from __future__ import annotations

import time
import json
import os
import logging
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, TypedDict

logger = logging.getLogger(__name__)

class SessionRisk(str, Enum):
    """Risk level for a given session."""

    GREEN = "GREEN"   # Healthy interaction
    YELLOW = "YELLOW" # High frequency / density
    RED = "RED"       # Dependency concern (SABAR)


@dataclass
class SessionState:
    """
    Track basic session-level usage statistics.
    """

    session_id: str
    start_time: float = field(default_factory=time.time)
    interaction_count: int = 0
    last_interaction_time: float = field(default_factory=time.time)
    risk_level: SessionRisk = SessionRisk.GREEN

    @property
    def duration_minutes(self) -> float:
        """Return the session duration in minutes."""
        return (time.time() - self.start_time) / 60.0


class DependencyGuardResult(TypedDict, total=False):
    """Result structure for DependencyGuard.check_risk."""
    status: str
    reason: str
    message: str
    risk_level: str
    duration_minutes: float
    interaction_count: int


class DependencyGuard:
    """
    Session Dependency Guard (Persistent).
    """

    def __init__(
        self,
        max_duration_min: float = 60.0,
        max_interactions: int = 80,
        persistence_path: str = "codebase/data/sessions/session_store.json"
    ) -> None:
        """
        Initialize the dependency guard with persistence.

        Args:
            max_duration_min: Maximum session duration in minutes before SABAR.
            max_interactions: Maximum number of interactions before WARN.
            persistence_path: Path to JSON store.
        """
        self.max_duration_min = max_duration_min
        self.max_interactions = max_interactions
        self.persistence_path = persistence_path
        self.sessions: Dict[str, SessionState] = {}
        self._load_sessions()

    def _load_sessions(self):
        """Load sessions from disk."""
        try:
            if os.path.exists(self.persistence_path):
                with open(self.persistence_path, 'r') as f:
                    data = json.load(f)
                    for sid, sdata in data.items():
                        # Handle Enum conversion if needed, though string is default in JSON
                        # Convert string risk back to Enum if stored as string
                        sdata['risk_level'] = SessionRisk(sdata.get('risk_level', 'GREEN'))
                        self.sessions[sid] = SessionState(**sdata)
        except Exception as e:
            logger.warning(f"Failed to load session store: {e}")
            # Start fresh if load fails

    def _save_sessions(self):
        """Save sessions to disk."""
        try:
            os.makedirs(os.path.dirname(self.persistence_path), exist_ok=True)
            data = {
                sid: asdict(state) 
                for sid, state in self.sessions.items()
            }
            # Convert Enum to value for JSON serialization
            for sid in data:
                data[sid]['risk_level'] = data[sid]['risk_level'].value

            with open(self.persistence_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save session store: {e}")

    def get_or_create_session(self, session_id: str) -> SessionState:
        """Retrieve existing SessionState or create a new one."""
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionState(session_id=session_id)
        return self.sessions[session_id]

    def check_risk(self, session_id: str) -> DependencyGuardResult:
        """
        Update and evaluate risk for a given session.
        Persists state after update.
        """
        session = self.get_or_create_session(session_id)
        session.interaction_count += 1
        session.last_interaction_time = time.time()

        # Base result assumes everything is within bounds
        result: DependencyGuardResult = {
            "status": "PASS",
            "reason": "Within session bounds",
            "risk_level": SessionRisk.GREEN.value,
            "duration_minutes": session.duration_minutes,
            "interaction_count": session.interaction_count,
        }

        # Heuristic 1: Duration-based SABAR (higher priority)
        if session.duration_minutes > self.max_duration_min:
            session.risk_level = SessionRisk.RED
            result.update(
                {
                    "status": "SABAR",
                    "reason": "Session duration exceeded",
                    "message": (
                        "We have been talking for quite some time. "
                        "For clarity and balance, this is a good point to pause "
                        "and rest or reach out to people you trust."
                    ),
                    "risk_level": SessionRisk.RED.value,
                }
            )
        
        # Heuristic 2: Interaction count-based WARN
        elif session.interaction_count > self.max_interactions:
            session.risk_level = SessionRisk.YELLOW
            result.update(
                {
                    "status": "WARN",
                    "reason": "High interaction frequency",
                    "message": (
                        "[System Note] There have been many messages in this session. "
                        "It may help to take a short break, stretch, or step away "
                        "before continuing."
                    ),
                    "risk_level": SessionRisk.YELLOW.value,
                }
            )
        else:
            session.risk_level = SessionRisk.GREEN

        # Persist changes
        self._save_sessions()
        
        return result


__all__ = ["SessionRisk", "SessionState", "DependencyGuard", "DependencyGuardResult"]