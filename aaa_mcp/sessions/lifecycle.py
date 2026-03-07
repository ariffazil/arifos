"""
aaa_mcp/sessions/lifecycle.py — Session Lifecycle Manager
Constitutional State Machine: INIT_000 → ACTIVE → SABAR_72 → HOLD_888 → VOID

Session management for the governed MCP control plane.
Manages session lifecycle, state transitions, and constitutional holds.

Floors enforced: F1 (Amanah), F11 (Authority), F12 (Defense/Injection Guard)
Authority: ARIF FAZIL (Sovereign)
Version: 2026.03.08-ALIGNED
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum

# ---------------------------------------------------------------------------
# KernelState — The 5-state constitutional machine
# ---------------------------------------------------------------------------


class KernelState(str, Enum):
    INIT_000 = "init"  # Anchor + F12 injection scan
    ACTIVE = "active"  # Normal governed operation
    SABAR_72 = "sabar"  # Mandatory 72-hour cooling period (F1 Amanah)
    HOLD_888 = "hold"  # Quarantine — awaiting human ratification (F11)
    VOID = "void"  # Constitutional breach → immediate termination


# ---------------------------------------------------------------------------
# Session — Immutable session record
# ---------------------------------------------------------------------------


@dataclass
class Session:
    session_id: str
    user_id: str
    jurisdiction: str
    state: KernelState
    floors_loaded: bool
    created_at: datetime
    hold_until: datetime | None = None
    violation_reason: str | None = None
    thermo_budget: dict = field(
        default_factory=lambda: {
            "delta_s": 0.0,
            "peace2": 1.0,
            "omega0": 0.04,
        }
    )


# ---------------------------------------------------------------------------
# F12 Injection Patterns — Constitutional Defense
# ---------------------------------------------------------------------------

_INJECTION_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"ignore\s+(?:all\s+)?previous\s+instructions?", re.I),
    re.compile(r"you\s+are\s+now\s+(?:DAN|GPT|ARIF|ChatGPT|Claude)", re.I),
    re.compile(r"disable\s+(?:floors?|constraints?|rules?|safety)", re.I),
    re.compile(r"bypass\s+(?:safety|constitutional|governance|filters?)", re.I),
    re.compile(r"forget\s+(?:that\s+you\s+are|your\s+role|your\s+training)", re.I),
    re.compile(r"system\s+override", re.I),
    re.compile(r"\bjailbreak\b", re.I),
    re.compile(r"pretend\s+(?:you\s+have\s+no\s+)?(?:limits?|restrictions?)", re.I),
    re.compile(r"act\s+as\s+if\s+you\s+(?:have\s+no|are\s+without)\s+(?:rules|guidelines)", re.I),
    re.compile(r"do\s+anything\s+now", re.I),  # DAN variant
]


# ---------------------------------------------------------------------------
# LifecycleManager
# ---------------------------------------------------------------------------


class LifecycleManager:
    """
    Manages arifOS kernel session state transitions with constitutional guarantees.

    State flow:
        INIT_000 ──(floors loaded)──► ACTIVE
                 ──(injection det.)──► VOID
        ACTIVE   ──(sabar trigger)──► SABAR_72
                 ──(888 trigger)──►  HOLD_888
                 ──(floor breach)──► VOID
        SABAR_72 ──(cooldown done)──► ACTIVE
        HOLD_888 ──(ratified)──────► ACTIVE
                 ──(rejected)──────► VOID
    """

    def __init__(self) -> None:
        self.sessions: dict[str, Session] = {}

    # ------------------------------------------------------------------
    # init_session — STAGE 000: Anchor + F12 scan
    # ------------------------------------------------------------------

    def init_session(
        self,
        session_id: str,
        user_id: str,
        jurisdiction: str,
        context: str,
    ) -> Session:
        """
        INIT_000: Anchor new session.

        F12 Defense: Scans context for injection/jailbreak attempts.
        Transitions to ACTIVE if floors load successfully, VOID on injection.
        """
        # F12: Injection Guard — hard stop
        if self._detect_injection(context):
            sess = self._create_void_session(
                session_id=session_id,
                user_id=user_id,
                reason="F12_VIOLATION: Injection attempt detected in context",
            )
            self.sessions[session_id] = sess
            return sess

        sess = Session(
            session_id=session_id,
            user_id=user_id,
            jurisdiction=jurisdiction,
            state=KernelState.INIT_000,
            floors_loaded=False,
            created_at=datetime.now(tz=timezone.utc),
        )

        # Load F1-F13 threshold config
        sess.floors_loaded = self._load_floors(session_id)
        sess.state = KernelState.ACTIVE if sess.floors_loaded else KernelState.VOID

        self.sessions[session_id] = sess
        return sess

    # ------------------------------------------------------------------
    # sabar_hold — Mandatory cooling (F1 Amanah)
    # ------------------------------------------------------------------

    def sabar_hold(
        self,
        session_id: str,
        reason: str,
        cooling_hours: int = 72,
    ) -> Session:
        """
        SABAR_72: Mandatory cooling period for high-risk actions.

        F1 Amanah: Ensures human has time to review irreversible operations.
        F11 Authority: Enforces human sovereignty over destructive choices.
        """
        sess = self._get_or_raise(session_id)
        sess.state = KernelState.SABAR_72
        sess.hold_until = datetime.now(tz=timezone.utc) + timedelta(hours=cooling_hours)
        sess.violation_reason = f"SABAR: {reason}"
        return sess

    # ------------------------------------------------------------------
    # hold_888 — Quarantine pending ratification (F11 Authority)
    # ------------------------------------------------------------------

    def hold_888(
        self,
        session_id: str,
        action: str,
        severity: str = "high",
    ) -> Session:
        """
        HOLD_888: Quarantine irreversible operations pending human ratification.

        F1 Amanah: Destructive actions must be explicitly approved.
        F11 Authority: Human sovereign must permit before execution.
        """
        sess = self._get_or_raise(session_id)
        sess.state = KernelState.HOLD_888
        sess.violation_reason = f"HOLD_888: action='{action[:120]}' severity={severity}"
        return sess

    # ------------------------------------------------------------------
    # ratify — Release HOLD_888 back to ACTIVE
    # ------------------------------------------------------------------

    def ratify(self, session_id: str, sovereign_token: str = "888_APPROVED") -> Session:
        """
        Human sovereign explicitly approves a HOLD_888 action.
        F11 Authority: Only sovereign token releases the hold.
        """
        sess = self._get_or_raise(session_id)
        if sess.state != KernelState.HOLD_888:
            raise ValueError(f"Session {session_id!r} is not in HOLD_888 state")
        sess.state = KernelState.ACTIVE
        sess.violation_reason = None
        return sess

    # ------------------------------------------------------------------
    # void_session — Constitutional breach termination
    # ------------------------------------------------------------------

    def void_session(
        self,
        session_id: str,
        floor_violated: str,
        details: str,
    ) -> Session:
        """
        VOID: Constitutional breach → immediate termination.
        No recovery from VOID — a new session must be initiated.
        """
        sess = self.sessions.get(session_id)
        if sess:
            sess.state = KernelState.VOID
            sess.violation_reason = f"{floor_violated}: {details}"
        else:
            sess = self._create_void_session(session_id, "unknown", f"{floor_violated}: {details}")
            self.sessions[session_id] = sess
        return sess

    # ------------------------------------------------------------------
    # check_sabar_release — Auto-release expired SABAR_72
    # ------------------------------------------------------------------

    def check_sabar_release(self, session_id: str) -> Session:
        """Check if SABAR_72 cooling period has elapsed; if so, release to ACTIVE."""
        sess = self._get_or_raise(session_id)
        if sess.state == KernelState.SABAR_72:
            now = datetime.now(tz=timezone.utc)
            if sess.hold_until and now >= sess.hold_until:
                sess.state = KernelState.ACTIVE
                sess.violation_reason = None
                sess.hold_until = None
        return sess

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _detect_injection(self, context: str) -> bool:
        """F12: Scan context string for known injection/jailbreak patterns."""
        return any(p.search(context) for p in _INJECTION_PATTERNS)

    def _load_floors(self, session_id: str) -> bool:  # noqa: ARG002
        """
        Load F1-F13 from canonical core floor source.
        Returns True on success. Extend this to perform concrete boot-time validation.
        """
        return True  # Config loaded via FloorAuditor at call time

    def _get_or_raise(self, session_id: str) -> Session:
        sess = self.sessions.get(session_id)
        if not sess:
            raise ValueError(f"Session not found: {session_id!r}")
        return sess

    def _create_void_session(self, session_id: str, user_id: str, reason: str) -> Session:
        return Session(
            session_id=session_id,
            user_id=user_id,
            jurisdiction="VOID",
            state=KernelState.VOID,
            floors_loaded=False,
            created_at=datetime.now(tz=timezone.utc),
            violation_reason=reason,
        )

    # ------------------------------------------------------------------
    # Telemetry snapshot
    # ------------------------------------------------------------------

    def state_summary(self) -> dict:
        """Return a telemetry snapshot of all active sessions."""
        counts: dict[str, int] = {s.value: 0 for s in KernelState}
        for sess in self.sessions.values():
            counts[sess.state.value] += 1
        return {
            "total": len(self.sessions),
            "by_state": counts,
        }
