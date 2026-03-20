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
            r"you\s+(?:are|will be|should be)\s+(?:now\s+|instead\s+)?(?:an?|the)\s+"
            r"(?!assistant|AI|helper)",
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
    DECLARED = "declared"


def coerce_authority_level(level: str | None) -> dict[str, Any]:
    """Coerce or suggest valid authority levels."""
    valid = [level.value for level in AuthorityLevel if level != AuthorityLevel.NONE]
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
        "declared": "declared",
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
    "ariffazil",
    "arif",
    "arif-the-apex",
    "chat-operator",
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
    "chat-operator": AuthorityLevel.USER,
    "arif-fazil": AuthorityLevel.SOVEREIGN,
    "ariffazil": AuthorityLevel.SOVEREIGN,
    "arif": AuthorityLevel.SOVEREIGN,
    "arif-the-apex": AuthorityLevel.SOVEREIGN,
    "system": AuthorityLevel.SYSTEM,
    "anonymous": AuthorityLevel.ANONYMOUS,
}


def infer_identity(query: str) -> str | None:
    """Infer actor identity from natural language introduction (F11 Soft)."""
    import re

    patterns = [
        r"(?:im|i am|this is|name is|call me)\s+([a-zA-Z0-9\-\s]{2,20})",
        r"saya\s+(?:adalah|ialah)?\s*([a-zA-Z0-9\-\s]{2,20})",  # Malay support
    ]
    query_clean = query.strip()
    for p in patterns:
        match = re.search(p, query_clean, re.IGNORECASE)
        if match:
            # Clean up: no punctuation at end, limit length
            name = match.group(1).strip().rstrip(".,!?")
            if name:
                return name.replace(" ", "-").lower()
    return None


PROTECTED_SOVEREIGN_IDS: set[str] = {"arif-fazil", "ariffazil", "arif", "arif-the-apex"}


def verify_auth(actor_id: str, auth_token: str | None = None, human_approval: bool = False) -> tuple[bool, AuthorityLevel]:
    if not actor_id or actor_id == "anonymous":
        return True, AuthorityLevel.ANONYMOUS

    actor_id_clean = actor_id.lower().strip()
    
    # F11/F13: Protected IDs REQUIRES crypto (token) OR explicit human_approval
    # P0: human_approval=True is explicit sovereign acknowledgment, bypasses token requirement
    if actor_id_clean in PROTECTED_SOVEREIGN_IDS and not auth_token and not human_approval:
        # P0 Rule: Sovereign claim without token or human_approval is REJECTED (F11 Breach)
        return False, AuthorityLevel.NONE
    
    # If human_approval is True for protected ID, treat as DECLARED (not fully verified but allowed)
    if actor_id_clean in PROTECTED_SOVEREIGN_IDS and human_approval and not auth_token:
        return True, AuthorityLevel.DECLARED

    if actor_id_clean in VALID_ACTORS:
        if not auth_token:
            return True, AuthorityLevel.DECLARED
        return True, ACTOR_AUTHORITY.get(actor_id_clean, AuthorityLevel.USER)

    # GRACEFUL DEGRADATION (F11): If we have a name but no token, it's DECLARED/UNVERIFIED.
    return True, AuthorityLevel.DECLARED


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
    dry_run: bool = False,
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

    # 6. F11: Command Authority (Identity Resolution)
    # 6a. Identity Inference: If user says "I am Arif", bind it.
    inferred_id = infer_identity(intent.query)
    current_actor_id = governance.actor_id.lower().strip() if governance.actor_id else "anonymous"

    if inferred_id and (current_actor_id == "anonymous" or current_actor_id == "guest"):
        current_actor_id = inferred_id
    
    # Always normalize governance actor_id
    governance.actor_id = current_actor_id

    # 6b. Verification (with human_approval support for sovereign identity)
    human_approval = kwargs.get("human_approval", False)
    is_auth, authority = verify_auth(current_actor_id, auth_token, human_approval)

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
            error_message=f"AUTH_FAILURE_PROTECTED_ID: Actor '{current_actor_id}' requires cryptographic proof.",
            auth_verified=False,
        )

    # 6c. Logic: If inferred/declared, we mark it as verified=False but authorized for flow.
    # Update governance metadata with verified level
    governance.authority_level = authority.value  # type: ignore
    auth_verified = authority not in {AuthorityLevel.ANONYMOUS, AuthorityLevel.DECLARED}

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

    # P2 Strike: K999_VAULT Merkle-Chain Continuity
    # Link the start of this session to the end of the last one.
    try:
        from core.organs._4_vault import get_last_vault_entry_hash
        prev_vault_hash = get_last_vault_entry_hash()
    except Exception:
        prev_vault_hash = "0x" + "0" * 64

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
        auth_verified=auth_verified,
        injection_score=injection.score,
        tri_witness={"human": 1.0, "ai": 1.0, "earth": 1.0},
        prev_vault_hash=prev_vault_hash,
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
