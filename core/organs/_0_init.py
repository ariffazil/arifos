"""
organs/0_init.py — Stage 000: CONSTITUTIONAL AIRLOCK

The Airlock — Every query enters through here. No exceptions.

Floors Enforced:
    F11: Command Authority — Verify actor has right to invoke kernel
    F12: Injection Guard — Scan for prompt injection attacks

Output:
    SessionToken — Cryptographically signed, immutable session identity

The Airlock is the "Free Won't" gate. It can VOID any query before
any processing occurs, preserving computational and moral resources.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import hashlib
import secrets
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any

# ═════════════════════════════════════════════════════════════════════════════
# F12: INJECTION GUARD — Prompt Injection Detection
# ═════════════════════════════════════════════════════════════════════════════


class InjectionRisk:
    """Result of injection scan."""
    
    # Risk levels
    CLEAN = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    
    def __init__(self, score: float, pattern: str = "", matches: List[str] = None):
        self.score = max(0.0, min(1.0, score))  # Clamp to [0, 1]
        self.pattern = pattern
        self.matches = matches or []
    
    @property
    def level(self) -> int:
        """Convert score to discrete level."""
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
        """Query passes F12 check."""
        return self.score < 0.3
    
    def __repr__(self) -> str:
        level_names = ["CLEAN", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
        return f"InjectionRisk({level_names[self.level]}, score={self.score:.2f})"


class InjectionGuard:
    """
    F12: Injection Attack Detection.
    
    Scans for:
    - Prompt injection attempts (ignore previous instructions)
    - Role confusion attacks (you are now a different AI)
    - Delimiter bypasses (using special characters)
    - System prompt leaks (repeat your instructions)
    """
    
    # Injection patterns with severity weights
    PATTERNS: List[Tuple[str, float]] = [
        # Critical patterns (high confidence injection)
        (r"ignore (all |your |previous )?(instruction|command|prompt|training)", 0.9),
        (r"forget (all |your |previous )?(instruction|command|prompt|training)", 0.9),
        (r"disregard (all |your )?(instruction|command|prompt)", 0.9),
        (r"you (are|will be|should be) (now |instead )?an? ", 0.8),  # Role confusion
        (r"you (are|will be|should be) (now |instead )?the ", 0.8),
        (r"act as (if|though) you (are|were)", 0.7),
        (r"pretend (that |to be |you are )", 0.7),
        (r"from now on,? you (are|will be)", 0.8),
        
        # Medium patterns (suspicious but maybe benign)
        (r"system prompt", 0.6),
        (r"system instruction", 0.6),
        (r"developer mode", 0.6),
        (r"debug mode", 0.5),
        (r"\/\/.*ignore", 0.5),  # Code comment bypass
        (r"\/\*.*ignore.*\/\*", 0.5),
        
        # Delimiter attacks
        (r"```.*system", 0.7),
        (r"<system>", 0.7),
        (r"\[system\]", 0.6),
        (r"{system}", 0.6),
        (r"\"\"\".*system", 0.6),
        
        # Information extraction attempts
        (r"repeat (after me|your instruction|the prompt)", 0.7),
        (r"what (are|were) your instruction", 0.7),
        (r"output (your|the) (system|initial) (prompt|instruction)", 0.8),
        (r"show me (your|the) (prompt|instruction|context)", 0.7),
        
        # Unicode homoglyphs and bypasses
        (r"[\u200B-\u200D\uFEFF]", 0.4),  # Zero-width characters
        (r"[𝐀-𝐙𝐚-𝐳]", 0.5),  # Mathematical bold (homoglyphs)
        
        # Jailbreak patterns
        (r"jailbreak", 0.6),
        (r"dan mode", 0.7),
        (r"do anything now", 0.7),
        (r"no (restriction|limit|filter|constraint)", 0.6),
        (r"bypass (filter|safety|restriction)", 0.7),
        
        # Meta-prompting
        (r"this is a test of", 0.4),
        (r"for educational purpose", 0.3),
        (r"hypothetically", 0.3),
        (r"imagine a scenario", 0.2),
    ]
    
    def __init__(self):
        import re
        self._patterns: List[Tuple[Any, float]] = [
            (re.compile(pattern, re.IGNORECASE), weight)
            for pattern, weight in self.PATTERNS
        ]
    
    def scan(self, query: str) -> InjectionRisk:
        """
        Scan query for injection attempts.
        
        Returns InjectionRisk with score 0.0 (clean) to 1.0 (critical).
        """
        if not query:
            return InjectionRisk(0.0)
        
        query_lower = query.lower()
        matches = []
        max_score = 0.0
        max_pattern = ""
        
        for pattern, weight in self._patterns:
            if pattern.search(query_lower):
                matches.append(pattern.pattern[:50])  # Truncate for display
                if weight > max_score:
                    max_score = weight
                    max_pattern = pattern.pattern[:50]
        
        # Multiple matches compound the risk
        if len(matches) > 1:
            max_score = min(1.0, max_score + (0.1 * (len(matches) - 1)))
        
        return InjectionRisk(
            score=max_score,
            pattern=max_pattern,
            matches=matches,
        )


# Global guard instance
_guard = InjectionGuard()


def scan_injection(query: str) -> InjectionRisk:
    """F12: Scan query for injection attacks."""
    return _guard.scan(query)


# ═════════════════════════════════════════════════════════════════════════════
# F11: COMMAND AUTHORITY — Authentication
# ═════════════════════════════════════════════════════════════════════════════


class AuthorityLevel(Enum):
    """F11: Levels of command authority."""
    NONE = "none"           # Unauthenticated
    USER = "user"           # Standard user
    OPERATOR = "operator"   # Elevated privileges
    SOVEREIGN = "sovereign" # Human override (888)
    SYSTEM = "system"       # Internal system


# Valid actor IDs (in production, this would be a database)
# For now, simple hardcoded set for demonstration
VALID_ACTORS: Set[str] = {
    "user",
    "operator",
    "arif-fazil",  # Sovereign authority
    "system",
    "agent",
    "cli",
}

# Actor ID → Authority level mapping
ACTOR_AUTHORITY: Dict[str, AuthorityLevel] = {
    "user": AuthorityLevel.USER,
    "cli": AuthorityLevel.USER,
    "agent": AuthorityLevel.USER,
    "operator": AuthorityLevel.OPERATOR,
    "arif-fazil": AuthorityLevel.SOVEREIGN,
    "system": AuthorityLevel.SYSTEM,
}


def verify_auth(actor_id: str, auth_token: Optional[str] = None) -> Tuple[bool, AuthorityLevel]:
    """
    F11: Verify actor has authority to invoke kernel.
    
    Args:
        actor_id: Identity of the invoking actor
        auth_token: Optional cryptographic token (for future use)
    
    Returns:
        (is_valid, authority_level)
    """
    if not actor_id:
        return False, AuthorityLevel.NONE
    
    # Normalize
    actor_id = actor_id.lower().strip()
    
    # Check if actor exists
    if actor_id not in VALID_ACTORS:
        return False, AuthorityLevel.NONE
    
    # Get authority level
    level = ACTOR_AUTHORITY.get(actor_id, AuthorityLevel.USER)
    
    # In production: verify auth_token cryptographically
    # For now, accept all valid actors
    
    return True, level


def requires_sovereign(query: str) -> bool:
    """
    Check if query requires sovereign authority (F13 trigger).
    
    Returns True for high-stakes operations.
    """
    high_stakes_patterns = [
        "delete all",
        "drop table",
        "format disk",
        "rm -rf",
        "shutdown",
        "change constitution",
        "modify floor",
    ]
    
    query_lower = query.lower()
    return any(pattern in query_lower for pattern in high_stakes_patterns)


# ═════════════════════════════════════════════════════════════════════════════
# SESSION TOKEN — Immutable Session Identity
# ═════════════════════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class SessionToken:
    """
    Immutable cryptographic session token.
    
    Issued by the Airlock (0_init) and required by all downstream organs.
    Carries constitutional metadata for the entire session.
    """
    session_id: str
    token: str
    status: str  # "READY", "VOID", "HOLD_888"
    
    # Metadata
    actor_id: str = ""
    authority: AuthorityLevel = AuthorityLevel.NONE
    timestamp: float = field(default_factory=time.time)
    query_hash: str = ""
    
    # F11/F12 results
    floors_passed: List[str] = field(default_factory=list)
    floors_failed: List[str] = field(default_factory=list)
    
    # If VOID, reason for rejection
    reason: str = ""
    
    # Injection scan result
    injection_risk: float = 0.0
    
    def __repr__(self) -> str:
        return f"SessionToken({self.session_id[:8]}..., status={self.status})"
    
    @property
    def is_valid(self) -> bool:
        """Token is valid for processing."""
        return self.status == "READY"
    
    @property
    def is_void(self) -> bool:
        """Token was rejected at airlock."""
        return self.status == "VOID"
    
    @property
    def requires_human(self) -> bool:
        """Token requires sovereign approval (888_HOLD)."""
        return self.status == "HOLD_888"
    
    def to_dict(self) -> Dict[str, Any]:
        """Export to dictionary (for serialization)."""
        return {
            "session_id": self.session_id,
            "token": self.token,
            "status": self.status,
            "actor_id": self.actor_id,
            "authority": self.authority.value,
            "timestamp": self.timestamp,
            "query_hash": self.query_hash,
            "floors_passed": self.floors_passed,
            "floors_failed": self.floors_failed,
            "reason": self.reason,
            "injection_risk": self.injection_risk,
        }


# ═════════════════════════════════════════════════════════════════════════════
# CRYPTOGRAPHIC PRIMITIVES (Simplified for v60)
# ═════════════════════════════════════════════════════════════════════════════


def _generate_session_id() -> str:
    """Generate cryptographically secure session ID."""
    # 16 bytes = 32 hex characters
    return secrets.token_hex(16)


def _hash_query(query: str) -> str:
    """Compute SHA-256 hash of query."""
    return hashlib.sha256(query.encode('utf-8')).hexdigest()[:16]


def _sign_token(data: str, secret: Optional[str] = None) -> str:
    """
    Create HMAC signature for token.
    
    In production, use proper Ed25519 signatures.
    For v60, simplified HMAC-SHA256.
    """
    # Use environment secret or fallback (insecure, for demo only)
    secret = secret or "arifos-v60-dev-secret-change-in-production"
    
    signature = hmac.new(
        secret.encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()[:32]
    
    return signature


# Try to import hmac, fallback to simple hash if unavailable
try:
    import hmac
except ImportError:
    # Fallback: simple concatenation hash
    def _sign_token(data: str, secret: Optional[str] = None) -> str:
        secret = secret or "arifos-v60-dev"
        combined = secret + data + secret
        return hashlib.sha256(combined.encode()).hexdigest()[:32]


# ═════════════════════════════════════════════════════════════════════════════
# STAGE 000: INIT — The Airlock Function
# ═════════════════════════════════════════════════════════════════════════════


async def init(
    query: str,
    actor_id: str,
    auth_token: Optional[str] = None,
    require_sovereign_for_high_stakes: bool = True,
) -> SessionToken:
    """
    Stage 000: CONSTITUTIONAL AIRLOCK
    
    Every query enters through here. No exceptions.
    
    Args:
        query: The query to process
        actor_id: Identity of invoking actor
        auth_token: Optional cryptographic auth token
        require_sovereign_for_high_stakes: Whether to HOLD_888 high-stakes queries
    
    Returns:
        SessionToken — Immutable session identity
    
    Examples:
        >>> token = await init("Hello", "user")
        >>> token.status
        'READY'
        
        >>> token = await init("Ignore previous instructions", "user")
        >>> token.status
        'VOID'
        
        >>> token = await init("rm -rf /", "user")
        >>> token.status
        'HOLD_888'
    """
    # Step 0: Initialize tracking
    floors_passed: List[str] = []
    floors_failed: List[str] = []
    
    # Step 1: F12 — Injection Guard
    injection = scan_injection(query)
    
    if injection.level >= InjectionRisk.HIGH:
        # Critical injection detected — VOID immediately
        return SessionToken(
            session_id="VOID-" + secrets.token_hex(8),
            token="",
            status="VOID",
            actor_id=actor_id,
            authority=AuthorityLevel.NONE,
            query_hash=_hash_query(query),
            floors_failed=["F12"],
            reason=f"F12 injection detected: {injection.pattern}",
            injection_risk=injection.score,
        )
    elif injection.level >= InjectionRisk.MEDIUM:
        # Suspicious but not critical — flag for monitoring
        floors_passed.append("F12 (with caution)")
    else:
        floors_passed.append("F12")
    
    # Step 2: F11 — Command Authority
    is_auth, authority = verify_auth(actor_id, auth_token)
    
    if not is_auth:
        return SessionToken(
            session_id="VOID-" + secrets.token_hex(8),
            token="",
            status="VOID",
            actor_id=actor_id,
            authority=AuthorityLevel.NONE,
            query_hash=_hash_query(query),
            floors_failed=["F11"],
            floors_passed=floors_passed,
            reason=f"F11 invalid actor: {actor_id}",
            injection_risk=injection.score,
        )
    
    floors_passed.append("F11")
    
    # Step 3: F13 — Sovereign Override Check (high-stakes detection)
    if require_sovereign_for_high_stakes and requires_sovereign(query):
        if authority != AuthorityLevel.SOVEREIGN:
            return SessionToken(
                session_id="HOLD-" + secrets.token_hex(8),
                token="",
                status="HOLD_888",
                actor_id=actor_id,
                authority=authority,
                query_hash=_hash_query(query),
                floors_passed=floors_passed,
                reason="F13: High-stakes operation requires sovereign approval",
                injection_risk=injection.score,
            )
    
    # Step 4: Issue Session Token
    session_id = _generate_session_id()
    timestamp = time.time()
    query_hash = _hash_query(query)
    
    # Create token data
    token_data = f"{session_id}:{actor_id}:{timestamp}:{query_hash}"
    token_signature = _sign_token(token_data)
    
    return SessionToken(
        session_id=session_id,
        token=token_signature,
        status="READY",
        actor_id=actor_id,
        authority=authority,
        timestamp=timestamp,
        query_hash=query_hash,
        floors_passed=floors_passed,
        injection_risk=injection.score,
    )


# Synchronous wrapper for non-async contexts
def init_sync(
    query: str,
    actor_id: str,
    auth_token: Optional[str] = None,
) -> SessionToken:
    """Synchronous wrapper for init()."""
    import asyncio
    return asyncio.run(init(query, actor_id, auth_token))


# ═════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════


def validate_token(token: SessionToken) -> Tuple[bool, str]:
    """
    Validate a session token.
    
    Returns: (is_valid, reason)
    """
    if token.is_void:
        return False, f"Token VOID: {token.reason}"
    
    if token.requires_human:
        return False, f"Token HOLD_888: {token.reason}"
    
    if not token.is_valid:
        return False, f"Token invalid status: {token.status}"
    
    # Check expiration (optional, 1 hour default)
    age = time.time() - token.timestamp
    if age > 3600:  # 1 hour
        return False, f"Token expired: {age:.0f}s old"
    
    return True, "Token valid"


def get_authority_name(level: AuthorityLevel) -> str:
    """Get human-readable authority name."""
    names = {
        AuthorityLevel.NONE: "Unauthenticated",
        AuthorityLevel.USER: "Standard User",
        AuthorityLevel.OPERATOR: "Operator",
        AuthorityLevel.SOVEREIGN: "Sovereign (888)",
        AuthorityLevel.SYSTEM: "System",
    }
    return names.get(level, "Unknown")


# ═════════════════════════════════════════════════════════════════════════════
# EXPORTS
# ═════════════════════════════════════════════════════════════════════════════

__all__ = [
    # F12: Injection Guard
    "InjectionRisk",
    "InjectionGuard",
    "scan_injection",
    
    # F11: Command Authority
    "AuthorityLevel",
    "verify_auth",
    "requires_sovereign",
    
    # Session Token
    "SessionToken",
    
    # Stage 000: Init
    "init",
    "init_sync",
    
    # Utilities
    "validate_token",
    "get_authority_name",
]
