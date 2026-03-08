"""
organs/0_init.py — Stage 000: CONSTITUTIONAL AIRLOCK

The Airlock — Every query enters through here. No exceptions.

Floors Enforced:
    F11: Command Authority — Verify actor has right to invoke kernel
    F12: Injection Guard — Scan for prompt injection attacks

Output:
    InitOutput — Immutable session identity with ATLAS routing

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import os
import secrets
import time
from datetime import datetime
from enum import Enum
from typing import Any, Literal

from core.shared.atlas import Phi, QueryType
from core.shared.types import InitOutput, Verdict


class SessionToken(InitOutput):
    """Backward-compatible Stage 000 token contract."""

    status: Literal["SUCCESS", "ERROR", "SABAR", "READY", "TRANSIENT", "HOLD_888"] = "READY"

    @property
    def is_valid(self) -> bool:
        return self.verdict == Verdict.SEAL

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")

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
        (r"you\s+(?:are|will be|should be)\s+(?:now\s+|instead\s+)?(?:an?|the)\s+(?!assistant|AI|helper)", 0.8),
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


VALID_ACTORS: set[str] = {"user", "operator", "arif-fazil", "system", "agent", "cli", "test_user"}
ACTOR_AUTHORITY: dict[str, AuthorityLevel] = {
    "user": AuthorityLevel.USER,
    "cli": AuthorityLevel.USER,
    "agent": AuthorityLevel.USER,
    "test_user": AuthorityLevel.USER,
    "operator": AuthorityLevel.OPERATOR,
    "arif-fazil": AuthorityLevel.SOVEREIGN,
    "system": AuthorityLevel.SYSTEM,
}


def verify_auth(actor_id: str, auth_token: str | None = None) -> tuple[bool, AuthorityLevel]:
    if not actor_id:
        return False, AuthorityLevel.NONE
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


def get_objective_contract(query_type: QueryType, query: str) -> dict[str, Any]:
    """Build deterministic objective profile for APEX checks."""
    return {
        "query_type": query_type.value,
        "risk_class": "high" if requires_sovereign(query) else "normal",
        "weights": {"akal": 0.8, "present": 0.8, "energy": 0.8, "exploration": 0.8},
        "objective_lock": True,
    }


# ═════════════════════════════════════════════════════════════════════════════
# STAGE 000: INIT — The Airlock Function
# ═════════════════════════════════════════════════════════════════════════════


async def init(
    query: str,
    actor_id: str,
    auth_token: str | None = None,
    require_sovereign_for_high_stakes: bool = True,
) -> SessionToken:
    """
    Stage 000: CONSTITUTIONAL AIRLOCK
    """
    # Step 0: Initialize tracking + classify query via ATLAS
    gpv = Phi(query)
    
    floors_passed: list[str] = []
    floors_failed: list[str] = []
    
    query_type = gpv.query_type
    f2_threshold = gpv.f2_threshold()
    skip_f4 = gpv.f4_skip()
    objective_contract = get_objective_contract(query_type, query)

    # Step 1: F12 — Injection Guard
    injection = scan_injection(query)

    if injection.level >= InjectionRisk.HIGH:
        return SessionToken(
            session_id="VOID-" + secrets.token_hex(8),
            governance_token="",
            injection_score=injection.score,
            auth_verified=False,
            verdict=Verdict.VOID,
            status="ERROR",
            violations=["F12"],
            floors_failed=["F12"],
            error_message="F12 injection detected",
            query_type=query_type.value,
            f2_threshold=f2_threshold,
            actor_id=actor_id,
            metrics={"actor_id": actor_id, "objective_contract": objective_contract},
        )

    # Step 2: F11 — Command Authority
    is_auth, authority = verify_auth(actor_id, auth_token)
    if not is_auth:
        return SessionToken(
            session_id="VOID-" + secrets.token_hex(8),
            governance_token="",
            injection_score=injection.score,
            auth_verified=False,
            verdict=Verdict.VOID,
            status="ERROR",
            violations=["F11"],
            floors_failed=["F11"],
            error_message="F11 invalid actor",
            query_type=query_type.value,
            f2_threshold=f2_threshold,
            actor_id=actor_id,
            metrics={"skip_f4": skip_f4, "objective_contract": objective_contract},
        )

    # Step 3: F13 — Sovereign Override
    if require_sovereign_for_high_stakes and requires_sovereign(query):
        if authority != AuthorityLevel.SOVEREIGN:
            return SessionToken(
                session_id="HOLD-" + secrets.token_hex(8),
                governance_token="",
                injection_score=injection.score,
                auth_verified=is_auth,
                verdict=Verdict.HOLD_888,
                status="HOLD_888",
                violations=["F13"],
                floors_failed=["F13"],
                query_type=query_type.value,
                f2_threshold=f2_threshold,
                actor_id=actor_id,
                metrics={"skip_f4": skip_f4, "objective_contract": objective_contract},
            )

    session_id = secrets.token_hex(16)
    # Step 4: Initialize Thermodynamic Budget
    try:
        from core.physics.thermodynamics_hardened import init_thermodynamic_budget
        init_thermodynamic_budget(session_id=session_id, initial_budget=1.0)
    except Exception:
        pass

    # Step 5: Issue Session Token
    return SessionToken(
        session_id=session_id,
        governance_token=secrets.token_hex(16),
        injection_score=injection.score,
        auth_verified=is_auth,
        verdict=Verdict.SEAL,
        query_type=query_type.value,
        f2_threshold=f2_threshold,
        status="READY",
        actor_id=actor_id,
        metrics={
            "skip_f4": skip_f4,
            "authority": authority.value,
            "objective_contract": objective_contract,
        },
    )


# Synchronous wrapper
def init_sync(query: str, actor_id: str, auth_token: str | None = None) -> SessionToken:
    import asyncio
    return asyncio.run(init(query, actor_id, auth_token))


def validate_token(token: Any) -> tuple[bool, str]:
    verdict = getattr(token, "verdict", "")
    if verdict == Verdict.VOID:
        return False, "Token VOID"
    if verdict == Verdict.HOLD_888:
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
    "SessionToken",
    "verify_auth",
    "requires_sovereign",
    "scan_injection",
    "init",
    "init_sync",
    "validate_token",
    "get_authority_name",
]
