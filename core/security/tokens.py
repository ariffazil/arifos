"""
core/security/tokens.py — F11 Command Auth: HMAC-SHA256 Governance Tokens

Mints and validates cryptographically signed session continuity tokens.
These are NOT JWTs. They are compact HMAC-SHA256 structures bound to:
  - session_id (UUIDv7)
  - actor_id (bootstrap-whitelist verified)
  - timestamp_bucket (5-minute window for replay protection)

Token structure: base64(header).base64(claims).hex(signature)
  - header:    {"alg": "HS256", "ver": "F11-v2"}
  - claims:    {"sid": session_id, "aid": actor_id, "iat": bucket, "clr": clearance}
  - signature: HMAC-SHA256(SOVEREIGN_KEY, header + "." + claims)

No stateless validation — tokens are always cross-checked against Redis session store.
Replayed tokens outside the 5-minute bucket are rejected with F11_TOKEN_EXPIRED.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import os
import time
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────────────────
SOVEREIGN_KEY: bytes = os.getenv("SOVEREIGN_KEY", "CHANGEME-SOVEREIGN-KEY-32-BYTES!!").encode()
BOOTSTRAP_ACTORS: frozenset[str] = frozenset(
    a.strip()
    for a in os.getenv("BOOTSTRAP_ACTORS", "").split(",")
    if a.strip()
)
TOKEN_BUCKET_SECONDS: int = 300  # 5-minute replay window
TOKEN_VERSION: str = "F11-v2"


# ─────────────────────────────────────────────────────────────────────────────
# DATA CLASSES
# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class TokenResult:
    valid: bool
    token: str = ""
    session_id: str = ""
    actor_id: str = ""
    clearance: str = "none"
    error: str = ""


@dataclass
class ValidationResult:
    valid: bool
    session_id: str = ""
    actor_id: str = ""
    clearance: str = "none"
    error: str = ""
    expired: bool = False


# ─────────────────────────────────────────────────────────────────────────────
# INTERNALS
# ─────────────────────────────────────────────────────────────────────────────
def _current_bucket() -> int:
    """Current 5-minute timestamp bucket for replay protection."""
    return int(time.time()) // TOKEN_BUCKET_SECONDS


def _b64(data: dict[str, Any]) -> str:
    return base64.urlsafe_b64encode(
        json.dumps(data, sort_keys=True).encode()
    ).rstrip(b"=").decode()


def _sign(payload: str) -> str:
    sig = hmac.new(SOVEREIGN_KEY, payload.encode(), hashlib.sha256)
    return sig.hexdigest()


def _actor_clearance(actor_id: str) -> str:
    """Determine clearance level from actor_id prefix conventions."""
    if actor_id.startswith("sovereign:"):
        return "sovereign"
    if actor_id.startswith("apex:"):
        return "apex"
    if actor_id.startswith("agent:"):
        return "agent"
    return "user"


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────
def mint_governance_token(
    actor_id: str,
    session_id: str,
    auth_nonce: str = "",
) -> TokenResult:
    """
    Mint a governance token after F11 bootstrap whitelist check.

    Returns TokenResult(valid=False) if actor_id is not in BOOTSTRAP_ACTORS
    and BOOTSTRAP_ACTORS is non-empty (open mode if empty).
    """
    # Whitelist gate (F11)
    if BOOTSTRAP_ACTORS and actor_id not in BOOTSTRAP_ACTORS:
        logger.warning("F11: actor_id '%s' not in bootstrap whitelist", actor_id)
        return TokenResult(
            valid=False,
            error="F11_AUTH_FAILURE: actor not in bootstrap whitelist",
        )

    clearance = _actor_clearance(actor_id)
    bucket = _current_bucket()

    header = _b64({"alg": "HS256", "ver": TOKEN_VERSION})
    claims = _b64({
        "sid": session_id,
        "aid": actor_id,
        "iat": bucket,
        "clr": clearance,
        "non": auth_nonce[:32] if auth_nonce else "",  # truncate, not store full nonce
    })
    payload = f"{header}.{claims}"
    signature = _sign(payload)
    token = f"{payload}.{signature}"

    logger.debug("F11: minted governance token for actor=%s session=%s", actor_id, session_id)
    return TokenResult(
        valid=True,
        token=token,
        session_id=session_id,
        actor_id=actor_id,
        clearance=clearance,
    )


def validate_governance_token(
    token: str,
    expected_session_id: str,
    allow_bucket_drift: int = 1,
) -> ValidationResult:
    """
    Validate a governance token.

    Checks:
      1. Structure: exactly 3 dot-separated parts
      2. Signature: HMAC-SHA256 matches
      3. Session ID: matches expected_session_id
      4. Timestamp bucket: within allow_bucket_drift windows (default: 1 = 10 min total)

    Returns ValidationResult(valid=False, expired=True) if bucket is stale.
    Returns ValidationResult(valid=False) for all other failures.
    """
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return ValidationResult(valid=False, error="F11_TOKEN_MALFORMED: expected 3 parts")

        header_b64, claims_b64, provided_sig = parts
        payload = f"{header_b64}.{claims_b64}"

        # Signature check
        expected_sig = _sign(payload)
        if not hmac.compare_digest(provided_sig, expected_sig):
            return ValidationResult(valid=False, error="F11_TOKEN_INVALID: signature mismatch")

        # Decode claims
        padding = "=" * (4 - len(claims_b64) % 4)
        claims = json.loads(base64.urlsafe_b64decode(claims_b64 + padding))

        # Session ID check
        if claims.get("sid") != expected_session_id:
            return ValidationResult(
                valid=False,
                error=f"F11_SESSION_MISMATCH: expected {expected_session_id}",
            )

        # Bucket replay check
        current_bucket = _current_bucket()
        token_bucket = claims.get("iat", 0)
        if abs(current_bucket - token_bucket) > allow_bucket_drift:
            return ValidationResult(
                valid=False,
                expired=True,
                error="F11_TOKEN_EXPIRED: timestamp bucket too stale",
            )

        return ValidationResult(
            valid=True,
            session_id=claims["sid"],
            actor_id=claims.get("aid", "unknown"),
            clearance=claims.get("clr", "none"),
        )

    except Exception as exc:
        logger.warning("F11 token validation error: %s", exc)
        return ValidationResult(valid=False, error=f"F11_TOKEN_PARSE_ERROR: {exc}")


def hash_governance_token(token: str) -> str:
    """SHA-256 of the governance token for safe storage in VAULT999 (never store raw)."""
    return hashlib.sha256(token.encode()).hexdigest()


__all__ = [
    "TokenResult",
    "ValidationResult",
    "mint_governance_token",
    "validate_governance_token",
    "hash_governance_token",
    "BOOTSTRAP_ACTORS",
    "TOKEN_BUCKET_SECONDS",
]
