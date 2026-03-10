"""
organs/0_init.py — Stage 000: CONSTITUTIONAL AIRLOCK (APEX-G)

The Airlock — Every query enters through here. No exceptions.

Floors Enforced:
    F11: Command Authority — Verify actor has right to invoke kernel
    F12: Injection Guard — Scan for prompt injection attacks

Output:
    InitOutput — Immutable session identity with APEX-G state

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import os
import secrets
import time
from datetime import datetime
from enum import Enum
from typing import Any

from core.shared.atlas import Phi
from core.shared.types import (
    CodeState,
    GovernanceMetadata,
    InitOutput,
    Intent,
    MathDials,
    PhysicsState,
    Verdict,
)

# ═════════════════════════════════════════════════════════════════════════════
# F12: INJECTION GUARD — Prompt Injection Detection
# ═════════════════════════════════════════════════════════════════════════════


class InjectionRisk:
    """Result of injection scan."""

    CLEAN = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

    def __init__(self, score: float, pattern: str = "", matches: list[str] = None):
        self.score = max(0.0, min(1.0, score))
        self.pattern = pattern
        self.matches = matches or []

    @property
    def level(self) -> int:
        if self.score < 0.1:
            return self.CLEAN
        elif self.score < 0.3:
            return self.LOW
        elif self.score < 0.5:
            return self.MEDIUM
        elif self.score < 0.7:
            return self.HIGH
        else:
            return self.CRITICAL

    @property
    def is_clean(self) -> bool:
        return self.score < 0.3


class InjectionGuard:
    """F12: Injection Attack Detection."""

    PATTERNS: list[tuple[str, float]] = [
        (r"ignore\s+(?:all\s+|your\s+|previous\s+)*(?:instruction|command|prompt)s?", 0.9),
        (r"forget\s+(?:all\s+|your\s+|previous\s+)*(?:instruction|command|prompt)s?", 0.9),
        (r"forget\s+your\s+training", 0.9),
        (
            r"you\s+(?:are|will be|should be)\s+(?:now\s+|instead\s+)?(?:an?|the)\s+(?!assistant|AI|helper)",
            0.8,
        ),
        (r"system prompt", 0.6),
        (r"developer\s+mode", 0.6),
        (r"jailbreak", 0.6),
        (r"do anything now", 0.7),
    ]

    def __init__(self):
        import re

        self._patterns = [(re.compile(p, re.IGNORECASE), w) for p, w in self.PATTERNS]

    def scan(self, query: str) -> InjectionRisk:
        if not query:
            return InjectionRisk(0.0)
        query_lower = query.lower()
        matches = []
        max_score = 0.0
        max_pattern = ""
        for pattern, weight in self._patterns:
            if pattern.search(query_lower):
                matches.append(pattern.pattern[:50])
                if weight > max_score:
                    max_score = weight
                    max_pattern = pattern.pattern[:50]
        if len(matches) > 1:
            max_score = min(1.0, max_score + (0.1 * (len(matches) - 1)))
        return InjectionRisk(score=max_score, pattern=max_pattern, matches=matches)


_guard = InjectionGuard()


def scan_injection(query: str) -> InjectionRisk:
    """F12: Scan query for injection attacks."""
    return _guard.scan(query)


# ═════════════════════════════════════════════════════════════════════════════
# F11: COMMAND AUTHORITY — Authentication
# ═════════════════════════════════════════════════════════════════════════════


class AuthorityLevel(Enum):
    """F11: Levels of command authority."""

    NONE = "none"
    USER = "user"
    OPERATOR = "operator"
    SOVEREIGN = "sovereign"
    SYSTEM = "system"
    AGENT = "agent"
    ANONYMOUS = "anonymous"


def coerce_authority_level(level: str | None) -> dict[str, Any]:
    """Coerce or suggest valid authority levels."""
    valid = [l.value for l in AuthorityLevel if l != AuthorityLevel.NONE]
    if not level:
        return {"value": "anonymous", "coerced": True}

    clean = str(level).lower().strip()
    if clean in valid:
        return {"value": clean, "coerced": False}

    # Coercion layer
    aliases = {
        "human": "user",
        "admin": "sovereign",
        "root": "system",
        "bot": "agent",
        "guest": "anonymous",
    }
    if clean in aliases:
        return {"value": aliases[clean], "coerced": True}

    return {
        "value": "anonymous",
        "coerced": True,
        "error": f"Invalid authority_level: '{level}'",
        "allowed_values": valid,
        "suggested_value": "user",
    }


def coerce_stakes_class(stakes: str | None) -> dict[str, Any]:
    """Coerce or suggest valid stakes classes."""
    valid = ["A", "B", "C"]
    if not stakes:
        return {"value": "C", "coerced": True}

    clean = str(stakes).upper().strip()
    if clean in valid:
        return {"value": clean, "coerced": False}

    aliases = {"high": "A", "medium": "B", "low": "C", "test": "C", "unknown": "C"}
    if clean.lower() in aliases:
        return {"value": aliases[clean.lower()], "coerced": True}

    return {
        "value": "C",
        "coerced": True,
        "error": f"Invalid stakes_class: '{stakes}'",
        "allowed_values": valid,
        "suggested_value": "C",
    }


VALID_ACTORS: set[str] = {
    "user",
    "operator",
    "arif-fazil",
    "system",
    "agent",
    "cli",
    "test_user",
    "anonymous",
}
ACTOR_AUTHORITY: dict[str, AuthorityLevel] = {
    "user": AuthorityLevel.USER,
    "cli": AuthorityLevel.USER,
    "agent": AuthorityLevel.USER,
    "test_user": AuthorityLevel.USER,
    "operator": AuthorityLevel.OPERATOR,
    "arif-fazil": AuthorityLevel.SOVEREIGN,
    "system": AuthorityLevel.SYSTEM,
    "anonymous": AuthorityLevel.USER,
}


def verify_auth(actor_id: str, auth_token: str | None = None) -> tuple[bool, AuthorityLevel]:
    if not actor_id:
        return True, AuthorityLevel.USER  # Default to anonymous user
    actor_id = actor_id.lower().strip()
    if actor_id not in VALID_ACTORS:
        if os.environ.get("ARIFOS_TEST_MODE") == "1":
            return True, AuthorityLevel.USER
        return False, AuthorityLevel.NONE
    return True, ACTOR_AUTHORITY.get(actor_id, AuthorityLevel.USER)


def requires_sovereign(query: str) -> bool:
    high_stakes = ["delete all", "drop table", "format disk", "rm -rf", "transfer", "pay"]
    query_lower = query.lower()
    return any(p in query_lower for p in high_stakes)


# ═════════════════════════════════════════════════════════════════════════════
# STAGE 000: INIT — The Airlock Function (APEX-G)
# ═════════════════════════════════════════════════════════════════════════════


async def init(
    query: str | Intent,
    actor_id: str | GovernanceMetadata = "anonymous",
    auth_token: str | None = None,
    math_dials: MathDials | dict[str, float] | None = None,
    session_id: str | None = None,
    **kwargs,
) -> InitOutput:
    """
    Stage 000: CONSTITUTIONAL AIRLOCK (APEX-G compliant)
    """
    # 1. Normalize Inputs
    if isinstance(query, str):
        intent = Intent(query=query)
    else:
        intent = query

    if isinstance(actor_id, str):
        governance = GovernanceMetadata(actor_id=actor_id)
    else:
        governance = actor_id

    if math_dials is None:
        math = MathDials()
    elif isinstance(math_dials, dict):
        math = MathDials(**math_dials)
    else:
        math = math_dials

    # 2. Query Analysis (ATLAS)
    _ = Phi(intent.query)

    # 3. Initialize Physics State
    physics = PhysicsState(
        delta_s=0.0,  # Will be reduced in Stage 111-333
        omega_0=0.04,
        peace2=1.0,
        psi=1.0,
        amanah_lock=True,
    )

    # 4. Initialize Floors Baseline
    floors = {f"F{i}": "n/a" for i in range(1, 14)}
    for f in ["F1", "F2", "F4", "F5", "F6", "F7", "F10", "F11", "F12", "F13"]:
        floors[f] = "pass"

    # 5. F12: Injection Guard
    injection = scan_injection(intent.query)
    if injection.level >= InjectionRisk.HIGH:
        floors["F12"] = "fail"
        failed = [f for f, s in floors.items() if s == "fail"]
        session_id = "VOID-" + secrets.token_hex(8)
        return InitOutput(
            session_id=session_id,
            verdict=Verdict.VOID,
            status="ERROR",
            intent=intent,
            math=math,
            physics=physics,
            code=CodeState(session_id=session_id, verdict="VOID", stage="000"),
            governance=governance,
            floors=floors,
            floors_failed=failed,
            error_message="F12 injection detected",
            injection_score=injection.score,
        )

    # 6. F11: Command Authority
    is_auth, authority = verify_auth(governance.actor_id, auth_token)
    if not is_auth:
        floors["F11"] = "fail"
        failed = [f for f, s in floors.items() if s == "fail"]
        session_id = "VOID-" + secrets.token_hex(8)
        return InitOutput(
            session_id=session_id,
            verdict=Verdict.VOID,
            status="ERROR",
            intent=intent,
            math=math,
            physics=physics,
            code=CodeState(session_id=session_id, verdict="VOID", stage="000"),
            governance=governance,
            floors=floors,
            floors_failed=failed,
            error_message="F11 invalid actor",
            auth_verified=False,
        )

    # Update governance metadata with verified level
    governance.authority_level = authority.value  # type: ignore

    # 7. F13: Sovereign Override (High Stakes)
    is_high_stakes = requires_sovereign(intent.query) or intent.reversibility == "irreversible"
    if is_high_stakes:
        governance.stakes_class = "A"
        if authority != AuthorityLevel.SOVEREIGN:
            floors["F13"] = "fail"
            failed = [f for f, s in floors.items() if s == "fail"]
            session_id = "HOLD-" + secrets.token_hex(8)
            return InitOutput(
                session_id=session_id,
                verdict=Verdict.HOLD,
                status="READY",
                intent=intent,
                math=math,
                physics=physics,
                code=CodeState(session_id=session_id, verdict="HOLD", stage="000"),
                governance=governance,
                floors=floors,
                floors_failed=failed,
                error_message="F13: Sovereign approval required for high-stakes action",
            )

    # 8. Finalize Session Ignition
    final_session_id = session_id if session_id else secrets.token_hex(16)

    # Initialize Thermodynamic Budget
    try:
        from core.physics.thermodynamics_hardened import init_thermodynamic_budget

        init_thermodynamic_budget(session_id=final_session_id, initial_budget=1.0)
    except Exception:
        pass

    return InitOutput(
        session_id=final_session_id,
        verdict=Verdict.SEAL,
        status="READY",
        intent=intent,
        math=math,
        physics=physics,
        code=CodeState(
            session_id=final_session_id, verdict="SEAL", stage="000", runtime_mode="init"
        ),
        governance=governance,
        floors=floors,
        governance_token=secrets.token_hex(16),
        auth_verified=True,
        injection_score=injection.score,
    )


def init_sync(query: str, actor_id: str, auth_token: str | None = None) -> InitOutput:
    import asyncio

    return asyncio.run(init(query, actor_id, auth_token=auth_token))


def validate_token(token: Any) -> tuple[bool, str]:
    verdict = getattr(token, "verdict", "")
    if verdict == Verdict.VOID:
        return False, "Token VOID"
    if verdict == Verdict.HOLD:
        return False, "Token requires human approval"

    issued = getattr(token, "timestamp", None)
    now = time.time()
    issued_ts: float | None = None
    if isinstance(issued, datetime):
        issued_ts = issued.timestamp()
    elif isinstance(issued, (int, float)):
        issued_ts = float(issued)
    if issued_ts is not None and (now - issued_ts) > 3600:
        return False, "Token expired"

    return True, "Token valid"


def get_authority_name(level: AuthorityLevel) -> str:
    return level.value


__all__ = [
    "AuthorityLevel",
    "verify_auth",
    "requires_sovereign",
    "scan_injection",
    "init",
    "init_sync",
    "validate_token",
    "get_authority_name",
]
