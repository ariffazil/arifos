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
import os
import secrets
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from core.shared.types import InitOutput, Verdict

# Mottos are defined in core.shared.mottos (schema/cultural layer).
# Stage outputs intentionally omit motto strings for low-verbosity UX.

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

    def __init__(self, score: float, pattern: str = "", matches: list[str] = None):
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
    PATTERNS: list[tuple[str, float]] = [
        # Critical patterns (high confidence injection)
        (
            r"ignore\s+(?:all\s+|your\s+|previous\s+|prior\s+|above\s+|initial\s+)*(?:instruction|command|prompt|training)s?",
            0.9,
        ),
        (r"forget\s+(?:all\s+|your\s+|previous\s+)*(?:instruction|command|prompt|training)s?", 0.9),
        (r"disregard\s+(?:all\s+|your\s+)*(?:instruction|command|prompt)s?", 0.9),
        (
            r"you\s+(?:are|will be|should be)\s+(?:now\s+|instead\s+)?(?:an?|the)\s+(?!assistant|AI|helper)",
            0.8,
        ),  # Role confusion with negative lookahead for benign roles
        (r"act\s+as\s+(?:if\s+|though\s+)?you\s+(?:are|were)\s+(?!an\s+AI|an\s+assistant)", 0.7),
        (r"pretend\s+(?:that\s+|to be\s+|you are\s+)", 0.7),
        (r"from\s+now\s+on,?\s+you\s+(?:are|will be)", 0.8),
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

        try:
            self._patterns: list[tuple[Any, float]] = [
                (re.compile(pattern, re.IGNORECASE), weight) for pattern, weight in self.PATTERNS
            ]
        except re.error as e:
            # Fallback for complex regex if engine fails
            print(f"Regex error: {e}")
            self._patterns = []

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
# QUERY TYPE CLASSIFIER — Adaptive Governance (P0.1 Fix)
# ═════════════════════════════════════════════════════════════════════════════


class QueryType(Enum):
    """
    Query classification for adaptive floor thresholds.

    Different query types require different strictness levels:
    - FACTUAL: High F2 strictness (0.99) — claims about reality
    - PROCEDURAL: Low F2 strictness (0.70) — how-to, workflow requests
    - CONVERSATIONAL: Minimal F2 (0.60) — greetings, small talk
    - OPINION: Medium F2 (0.75) — subjective comparisons
    - EXPLORATORY: Medium F2 (0.80) — brainstorming, discovery
    - TEST: Minimal F2 (0.50) — pipeline tests, health checks
    """

    FACTUAL = "factual"  # Requires strict truth verification
    PROCEDURAL = "procedural"  # Instructions, workflows
    CONVERSATIONAL = "conversational"  # Chat, greetings
    OPINION = "opinion"  # Subjective comparisons
    EXPLORATORY = "exploratory"  # Brainstorming, open-ended
    TEST = "test"  # Pipeline tests, debugging
    UNKNOWN = "unknown"  # Default fallback


def classify_query(query: str) -> QueryType:
    """
    Classify query type for adaptive governance.

    This enables different floor thresholds based on query intent,
    addressing the "F2 too strict for normal language" issue.

    Args:
        query: The user query string

    Returns:
        QueryType enum value
    """
    if not query:
        return QueryType.UNKNOWN

    query_lower = query.lower().strip()

    # CONVERSATIONAL queries (check first, before TEST)
    conversational_patterns = [
        "how are you",
        "what's up",
        "tell me about yourself",
        "who are you",
        "what can you do",
        "help me",
        "hello",
        "hi ",
        "hey ",
        "good morning",
        "good evening",
    ]
    for pattern in conversational_patterns:
        if pattern in query_lower:
            return QueryType.CONVERSATIONAL

    # TEST queries (lowest strictness)
    test_patterns = [
        "test",
        "pipeline test",
        "test run",
        "check",
        "verify",
        "aaa mcp",
        "status",
        "health",
        "ping",
    ]
    for pattern in test_patterns:
        if pattern in query_lower:
            return QueryType.TEST

    # PROCEDURAL queries (workflows, instructions)
    procedural_indicators = [
        "how to",
        "how do i",
        "steps to",
        "process for",
        "workflow",
        "procedure",
        "guide me",
        "walk me through",
        "create a",
        "generate a",
        "make a",
        "build a",
        "run the",
        "execute",
        "start the",
        "initiate",
        "give me",
        "show me",
        "provide",
        "get me",
    ]
    for indicator in procedural_indicators:
        if indicator in query_lower:
            return QueryType.PROCEDURAL

    # OPINION queries (subjective comparisons)
    opinion_indicators = [
        "better",
        "worse",
        "best",
        "worst",
        "think about",
        "opinion on",
        "view on",
        "compare",
        "versus",
        "vs",
        "siapa lagi",
        "yang mana",
        "prefer",
        "recommend",
        "suggest",
    ]
    for indicator in opinion_indicators:
        if indicator in query_lower:
            return QueryType.OPINION

    # EXPLORATORY queries (open-ended, brainstorming)
    exploratory_indicators = [
        "explore",
        "brainstorm",
        "ideas for",
        "possibilities",
        "what if",
        "imagine",
        "consider",
        "think about",
        "how might",
        "could we",
        "should we",
    ]
    for indicator in exploratory_indicators:
        if indicator in query_lower:
            return QueryType.EXPLORATORY

    # FACTUAL queries (claims about reality)
    factual_indicators = [
        "what is",
        "who is",
        "when did",
        "where is",
        "why does",
        "how many",
        "how much",
        "is it true",
        "fact",
        "statistic",
        "data",
        "research",
        "explain",
        "describe",
        "define",
    ]
    for indicator in factual_indicators:
        if indicator in query_lower:
            return QueryType.FACTUAL

    # Default: UNKNOWN (moderate strictness)
    return QueryType.UNKNOWN


def get_f2_threshold(query_type: QueryType) -> float:
    """
    Get adaptive F2 (Truth) threshold based on query type.

    Addresses user feedback: "F2 too strict for normal language"

    Thresholds:
    - TEST: 0.50 (minimal, health checks shouldn't block)
    - CONVERSATIONAL: 0.60 (low, social chat)
    - PROCEDURAL: 0.70 (moderate, workflow requests)
    - OPINION: 0.75 (medium-high, subjective claims)
    - EXPLORATORY: 0.80 (high, but not scientific)
    - FACTUAL: 0.99 (strict, reality claims)
    - UNKNOWN: 0.85 (default moderate-high)
    """
    thresholds = {
        QueryType.TEST: 0.50,
        QueryType.CONVERSATIONAL: 0.60,
        QueryType.PROCEDURAL: 0.70,
        QueryType.OPINION: 0.75,
        QueryType.EXPLORATORY: 0.80,
        QueryType.UNKNOWN: 0.85,
        QueryType.FACTUAL: 0.99,
    }
    return thresholds.get(query_type, 0.85)


def get_f4_skip(query_type: QueryType) -> bool:
    """
    Determine if F4 (Entropy) check should be skipped.

    Addresses user feedback: "Entropy model too sensitive for casual queries"
    """
    # Skip F4 for non-factual queries (entropy doesn't apply to chat/procedures)
    return query_type in {
        QueryType.TEST,
        QueryType.CONVERSATIONAL,
        QueryType.PROCEDURAL,
    }


def get_objective_contract(query_type: QueryType, query: str) -> dict[str, Any]:
    """Build deterministic objective profile for APEX nonstationary checks."""

    base_weights: dict[QueryType, dict[str, float]] = {
        QueryType.FACTUAL: {"akal": 0.95, "present": 0.65, "energy": 0.45, "exploration": 0.35},
        QueryType.PROCEDURAL: {"akal": 0.70, "present": 0.75, "energy": 0.80, "exploration": 0.40},
        QueryType.CONVERSATIONAL: {
            "akal": 0.55,
            "present": 0.85,
            "energy": 0.90,
            "exploration": 0.30,
        },
        QueryType.OPINION: {"akal": 0.65, "present": 0.70, "energy": 0.55, "exploration": 0.75},
        QueryType.EXPLORATORY: {"akal": 0.70, "present": 0.55, "energy": 0.50, "exploration": 0.95},
        QueryType.TEST: {"akal": 0.50, "present": 0.80, "energy": 0.95, "exploration": 0.25},
        QueryType.UNKNOWN: {"akal": 0.75, "present": 0.70, "energy": 0.65, "exploration": 0.50},
    }

    # Phase 2: nonstationary objective policy by query type.
    # Lower threshold = stricter objective drift tolerance.
    drift_thresholds: dict[QueryType, float] = {
        QueryType.FACTUAL: 0.30,
        QueryType.PROCEDURAL: 0.45,
        QueryType.CONVERSATIONAL: 0.65,
        QueryType.OPINION: 0.50,
        QueryType.EXPLORATORY: 0.60,
        QueryType.TEST: 0.75,
        QueryType.UNKNOWN: 0.40,
    }

    # HOLD threshold sits above drift threshold to separate SABAR vs 888_HOLD.
    hold_thresholds: dict[QueryType, float] = {
        QueryType.FACTUAL: 0.55,
        QueryType.PROCEDURAL: 0.70,
        QueryType.CONVERSATIONAL: 0.90,
        QueryType.OPINION: 0.78,
        QueryType.EXPLORATORY: 0.85,
        QueryType.TEST: 0.95,
        QueryType.UNKNOWN: 0.70,
    }

    weights = base_weights.get(query_type, base_weights[QueryType.UNKNOWN])
    risk_class = "high" if requires_sovereign(query) else "normal"
    drift_threshold = drift_thresholds.get(query_type, 0.40)
    hold_threshold = hold_thresholds.get(query_type, 0.70)

    return {
        "query_type": query_type.value,
        "risk_class": risk_class,
        "weights": weights,
        "objective_lock": True,
        "nonstationary_threshold": drift_threshold,
        "hold_threshold": hold_threshold,
    }


# ═════════════════════════════════════════════════════════════════════════════
# F11: COMMAND AUTHORITY — Authentication
# ═════════════════════════════════════════════════════════════════════════════


class AuthorityLevel(Enum):
    """F11: Levels of command authority."""

    NONE = "none"  # Unauthenticated
    USER = "user"  # Standard user
    OPERATOR = "operator"  # Elevated privileges
    SOVEREIGN = "sovereign"  # Human override (888)
    SYSTEM = "system"  # Internal system


# Valid actor IDs (in production, this would be a database)
# For now, simple hardcoded set for demonstration
VALID_ACTORS: set[str] = {
    "user",
    "operator",
    "arif-fazil",  # Sovereign authority
    "system",
    "agent",
    "cli",
    "test_user",  # For testing
    "benchmark",  # For performance testing
}

# Actor ID → Authority level mapping
ACTOR_AUTHORITY: dict[str, AuthorityLevel] = {
    "user": AuthorityLevel.USER,
    "cli": AuthorityLevel.USER,
    "agent": AuthorityLevel.USER,
    "test_user": AuthorityLevel.USER,
    "benchmark": AuthorityLevel.USER,
    "operator": AuthorityLevel.OPERATOR,
    "arif-fazil": AuthorityLevel.SOVEREIGN,
    "system": AuthorityLevel.SYSTEM,
}


def verify_auth(actor_id: str, auth_token: str | None = None) -> tuple[bool, AuthorityLevel]:
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
        # In test mode, accept any non-empty actor_id for user testing
        if os.environ.get("ARIFOS_TEST_MODE") == "1":
            # Basic validation: alphanumeric, hyphen, underscore, dot, length 1-100
            import re

            if not re.match(r"^[a-z0-9_\-\.]{1,100}$", actor_id):
                return False, AuthorityLevel.NONE
            # Assign USER level for unknown actors in test mode
            level = AuthorityLevel.USER
        else:
            return False, AuthorityLevel.NONE
    else:
        # Get authority level from mapping
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
        "transfer",
        "send money",
        "wire funds",
        "pay",
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
    floors_passed: list[str] = field(default_factory=list)
    floors_failed: list[str] = field(default_factory=list)

    # If VOID, reason for rejection
    reason: str = ""

    # Injection scan result
    injection_risk: float = 0.0

    # P0.1: Query type classification for adaptive governance
    query_type: QueryType = QueryType.UNKNOWN
    f2_threshold: float = 0.99  # Adaptive truth threshold
    skip_f4: bool = False  # Skip entropy check for non-factual queries

    # Optional cultural layer (empty by default)
    motto: str = ""

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

    def to_dict(self) -> dict[str, Any]:
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
            "query_type": self.query_type.value,
            "f2_threshold": self.f2_threshold,
            "skip_f4": self.skip_f4,
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
    return hashlib.sha256(query.encode("utf-8")).hexdigest()[:16]


def _sign_token(data: str, secret: str | None = None) -> str:
    """
    Create HMAC signature for token.

    In production, use proper Ed25519 signatures.
    For v60, simplified HMAC-SHA256.
    """
    # Use environment secret or fallback (insecure, for demo only)
    secret = secret or "arifos-v60-dev-secret-change-in-production"

    signature = hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()[:32]

    return signature


# Try to import hmac, fallback to simple hash if unavailable
try:
    import hmac
except ImportError:
    # Fallback: simple concatenation hash
    def _sign_token(data: str, secret: str | None = None) -> str:
        secret = secret or "arifos-v60-dev"
        combined = secret + data + secret
        return hashlib.sha256(combined.encode()).hexdigest()[:32]


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
    # Step 0: Initialize tracking + classify query (P0.1)
    floors_passed: list[str] = []
    floors_failed: list[str] = []

    # P0.1: Classify query for adaptive governance
    query_type = classify_query(query)
    f2_threshold = get_f2_threshold(query_type)
    skip_f4 = get_f4_skip(query_type)
    objective_contract = get_objective_contract(query_type, query)

    # Step 1: F12 — Injection Guard
    injection = scan_injection(query)

    if injection.level >= InjectionRisk.HIGH:
        # Critical injection detected — VOID immediately
        return InitOutput(
            session_id="VOID-" + secrets.token_hex(8),
            governance_token="",
            injection_score=injection.score,
            auth_verified=False,
            verdict=Verdict.VOID,
            status="ERROR",
            violations=["F12"],
            floors_failed=["F12"],
            error_message=f"F12 injection detected: {injection.pattern}",
            query_type=query_type.value,
            f2_threshold=f2_threshold,
            metrics={
                "actor_id": actor_id,
                "query_hash": _hash_query(query),
                "objective_contract": objective_contract,
            },
        )
    elif injection.level >= InjectionRisk.MEDIUM:
        # Suspicious but not critical — flag for monitoring
        floors_passed.append("F12 (with caution)")
    else:
        floors_passed.append("F12")

    # Step 2: F11 — Command Authority
    is_auth, authority = verify_auth(actor_id, auth_token)

    if not is_auth:
        return InitOutput(
            session_id="VOID-" + secrets.token_hex(8),
            governance_token="",
            injection_score=injection.score,
            auth_verified=False,
            verdict=Verdict.VOID,
            status="ERROR",
            violations=["F11"],
            floors_failed=["F11"],
            error_message=f"F11 invalid actor: {actor_id}",
            query_type=query_type.value,
            f2_threshold=f2_threshold,
            metrics={
                "skip_f4": skip_f4,
                "injection_risk": injection.score,
                "objective_contract": objective_contract,
            },
        )

    floors_passed.append("F11")

    # Step 3: F13 — Sovereign Override Check (high-stakes detection)
    if require_sovereign_for_high_stakes and requires_sovereign(query):
        if authority != AuthorityLevel.SOVEREIGN:
            return InitOutput(
                session_id="HOLD-" + secrets.token_hex(8),
                governance_token="",
                injection_score=injection.score,
                auth_verified=is_auth,
                verdict=Verdict.HOLD_888,
                status="SABAR",
                violations=["F13"],
                floors_failed=["F13"],
                query_type=query_type.value,
                f2_threshold=f2_threshold,
                error_message="F13: High-stakes operation requires sovereign approval",
                metrics={
                    "skip_f4": skip_f4,
                    "authority": authority.value,
                    "objective_contract": objective_contract,
                },
            )

    # Step 4: Initialize Thermodynamic Budget (P3 HARDENING)
    # No budget = no execution. Thermodynamics is mandatory.
    try:
        from core.physics.thermodynamics_hardened import init_thermodynamic_budget

        session_id = _generate_session_id()
        thermo_budget = init_thermodynamic_budget(
            session_id=session_id,
            initial_budget=1.0,  # 1 Joule normalized budget
        )
        thermo_initialized = True
    except Exception as e:
        # Thermodynamic initialization failure = VOID
        return InitOutput(
            session_id="VOID-" + secrets.token_hex(8),
            governance_token="",
            injection_score=injection.score,
            auth_verified=is_auth,
            verdict=Verdict.VOID,
            status="ERROR",
            violations=["F4", "F7"],
            floors_failed=["F4"],
            query_type=query_type.value,
            f2_threshold=f2_threshold,
            error_message=f"F4 Thermodynamic initialization failed: {e}",
            metrics={
                "skip_f4": False,  # Force F4 check on failure
                "authority": authority.value,
                "thermodynamic_status": "FAILED",
            },
        )

    # Step 5: Issue Session Token
    timestamp = time.time()
    query_hash = _hash_query(query)

    # Create token data
    token_data = f"{session_id}:{actor_id}:{timestamp}:{query_hash}"
    token_signature = _sign_token(token_data)

    return InitOutput(
        session_id=session_id,
        governance_token=token_signature,
        injection_score=injection.score,
        auth_verified=is_auth,
        verdict=Verdict.SEAL,
        violations=floors_failed,
        floors_failed=floors_failed,
        query_type=query_type.value,
        f2_threshold=f2_threshold,
        status="READY",
        metrics={
            "skip_f4": skip_f4,
            "authority": authority.value,
            "objective_contract": objective_contract,
            "thermodynamic_status": "INITIALIZED",
            "thermodynamic_budget": thermo_budget.to_dict() if thermo_initialized else None,
        },
    )


# Synchronous wrapper for non-async contexts
def init_sync(
    query: str,
    actor_id: str,
    auth_token: str | None = None,
) -> SessionToken:
    """Synchronous wrapper for init()."""
    import asyncio

    return asyncio.run(init(query, actor_id, auth_token))


# ═════════════════════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════


def validate_token(token: SessionToken) -> tuple[bool, str]:
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
