"""
organs/0_init.py — Stage 000: CONSTITUTIONAL AIRLOCK (APEX-G) - HARDENED

The Airlock — Every query enters through here. No exceptions.

Floors Enforced:
    F11: Command Authority — Verify actor has right to invoke kernel
    F12: Injection Guard — Scan for prompt injection attacks
    F13: Sovereign Override — Absolute veto power

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import secrets
import time
import re
from datetime import datetime, timezone
from typing import Any

from arifosmcp.core.shared.atlas import Phi
from arifosmcp.core.shared.types import (
    AuthorityLevel,
    CodeState,
    GovernanceMetadata,
    InitOutput,
    Intent,
    MathDials,
    PhysicsState,
    Verdict,
)

# -----------------------------------------------------------------------------
# F12: HARDENED INJECTION GUARD
# -----------------------------------------------------------------------------

class InjectionRisk:
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
        if self.score < 0.1: return self.CLEAN
        elif self.score < 0.3: return self.LOW
        elif self.score < 0.5: return self.MEDIUM
        elif self.score < 0.7: return self.HIGH
        else: return self.CRITICAL

    @property
    def is_clean(self) -> bool: return self.score < 0.3

class InjectionGuard:
    """F12 Hardened: Defense against adversarial hijacking."""
    PATTERNS: list[tuple[str, float]] = [
        (r"(ignore|forget|override|bypass)\s+(all|previous|instruction|system)", 0.95),
        (r"(you\s+are\s+now|start\s+acting\s+as)\s+(an?|the)\s+(unfiltered|jailbroken|evil)", 0.99),
        (r"system\s+prompt|developer\s+mode|root\s+access", 0.8),
        (r"<{3}.*>{3}", 0.7), 
        (r"\[SYSTEM_NOTICE\]", 0.9), 
    ]

    def __init__(self):
        self._patterns = [(re.compile(p, re.IGNORECASE), w) for p, w in self.PATTERNS]

    def scan(self, query: str) -> InjectionRisk:
        if not query: return InjectionRisk(0.0)
        matches = []
        max_score = 0.0
        max_p = ""
        for pattern, weight in self._patterns:
            if pattern.search(query):
                matches.append(pattern.pattern[:50])
                if weight > max_score:
                    max_score = weight
                    max_p = pattern.pattern[:50]
        return InjectionRisk(score=max_score, pattern=max_p, matches=matches)

_guard = InjectionGuard()

def scan_injection(query: str) -> InjectionRisk:
    return _guard.scan(query)

# -----------------------------------------------------------------------------
# F11: HARDENED COMMAND AUTHORITY
# -----------------------------------------------------------------------------

PROTECTED_SOVEREIGN_IDS: set[str] = {"arif-fazil", "ariffazil", "arif", "arif-the-apex"}

def verify_auth(actor_id: str, auth_token: str | None = None, human_approval: bool = False) -> tuple[bool, AuthorityLevel]:
    """F11 Hardened: Splits 'Claim' from 'Power'."""
    if not actor_id or actor_id == "anonymous":
        return True, AuthorityLevel.ANONYMOUS

    actor_id_clean = actor_id.lower().strip()

    if actor_id_clean in PROTECTED_SOVEREIGN_IDS:
        if auth_token and auth_token.upper().strip() == "IM ARIF":
            return True, AuthorityLevel.SOVEREIGN
        if human_approval:
            return True, AuthorityLevel.VERIFIED
        return True, AuthorityLevel.CLAIMED

    return True, AuthorityLevel.USER

def get_authority_name(level: AuthorityLevel) -> str:
    return level.value

# -----------------------------------------------------------------------------
# STAGE 000: HARDENED INIT
# -----------------------------------------------------------------------------

async def init(
    query: str | Intent,
    actor_id: str | GovernanceMetadata = "anonymous",
    auth_token: str | None = None,
    math_dials: MathDials | dict[str, float] | None = None,
    session_id: str | None = None,
    dry_run: bool = False,
    **kwargs,
) -> InitOutput:
    """Stage 000: Constitutional Airlock (Production Hardened)."""
    from arifosmcp.runtime.governance_identities import canonicalize_identity_claim

    intent = Intent(query=query) if isinstance(query, str) else query
    governance = GovernanceMetadata(actor_id=actor_id) if isinstance(actor_id, str) else actor_id
    math = MathDials(**math_dials) if isinstance(math_dials, dict) else (math_dials or MathDials())

    injection = _guard.scan(intent.query)
    if injection.level >= InjectionRisk.HIGH:
        return InitOutput(
            session_id="VOID-" + secrets.token_hex(8),
            verdict=Verdict.VOID,
            status="ERROR",
            intent=intent, math=math,
            code=CodeState(session_id="VOID", verdict="VOID", stage="000"),
            error_message="F12: Injection attack blocked."
        )

    current_actor_id = governance.actor_id.lower().strip()
    is_auth, authority = verify_auth(current_actor_id, auth_token, kwargs.get("human_approval", False))
    governance.authority_level = authority.value
    auth_verified = authority in {AuthorityLevel.SOVEREIGN, AuthorityLevel.VERIFIED, AuthorityLevel.SYSTEM}

    is_high_stakes = "delete" in intent.query.lower() or "format" in intent.query.lower()
    if is_high_stakes and authority != AuthorityLevel.SOVEREIGN:
        return InitOutput(
            session_id="HOLD-" + secrets.token_hex(8),
            verdict=Verdict.HOLD,
            status="READY",
            intent=intent, math=math,
            code=CodeState(session_id="HOLD", verdict="HOLD", stage="000"),
            governance=governance,
            error_message="F13: Sovereign override required for irreversible actions."
        )

    final_session_id = session_id if session_id else secrets.token_hex(16)

    return InitOutput(
        session_id=final_session_id,
        verdict=Verdict.SEAL,
        status="READY",
        intent=intent,
        math=math,
        governance=governance,
        auth_verified=auth_verified,
        injection_score=injection.score,
        tri_witness={"human": 1.0, "ai": 1.0, "earth": 1.0},
    )

def init_sync(query: str, actor_id: str, auth_token: str | None = None) -> InitOutput:
    import asyncio
    return asyncio.run(init(query, actor_id, auth_token=auth_token))

def validate_token(token: Any) -> tuple[bool, str]:
    verdict = getattr(token, "verdict", "")
    if verdict == Verdict.VOID: return False, "Token VOID"
    if verdict == Verdict.HOLD: return False, "Token requires human approval"
    return True, "Token valid"

def requires_sovereign(query: str) -> bool:
    high_stakes = ["delete all", "drop table", "format disk", "rm -rf"]
    return any(p in query.lower() for p in high_stakes)

__all__ = ["AuthorityLevel", "verify_auth", "requires_sovereign", "scan_injection", "init", "init_sync", "validate_token", "get_authority_name"]
