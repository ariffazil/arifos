"""
core/enforcement/auth_continuity.py — F11 Amanah Handshake

Strict session continuity through cryptographic chaining.
Ensures that a session cannot be hijacked or forged between tool calls.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import hashlib
import hmac
import json
import secrets
import time
from typing import Any

# HMAC signs the actor's context so the kernel can verify it across calls
# without keeping a large in-memory state for every hop.
_GOVERNANCE_TOKEN_SECRET = secrets.token_hex(32)


def sign_auth_context(unsigned_context: dict[str, Any]) -> str:
    canonical = json.dumps(
        unsigned_context, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    )
    return hmac.new(
        _GOVERNANCE_TOKEN_SECRET.encode(),
        canonical.encode(),
        hashlib.sha256,
    ).hexdigest()


def mint_auth_context(
    session_id: str,
    actor_id: str,
    token_fingerprint: str,
    approval_scope: list[str],
    parent_signature: str,
    ttl: int = 900,
) -> dict[str, Any]:
    now = int(time.time())
    unsigned_context = {
        "session_id": session_id,
        "actor_id": actor_id,
        "token_fingerprint": token_fingerprint,
        "nonce": secrets.token_hex(12),
        "iat": now,
        "exp": now + ttl,
        "approval_scope": approval_scope,
        "parent_signature": parent_signature,
    }
    return {
        **unsigned_context,
        "signature": sign_auth_context(unsigned_context),
    }


def verify_auth_context(session_id: str, auth_context: dict[str, Any]) -> tuple[bool, str]:
    required_fields = [
        "session_id",
        "actor_id",
        "token_fingerprint",
        "nonce",
        "iat",
        "exp",
        "approval_scope",
        "parent_signature",
        "signature",
    ]
    for field in required_fields:
        if field not in auth_context:
            return False, f"missing field: {field}"

    if str(auth_context.get("session_id", "")) != session_id:
        return False, "session_id mismatch"

    exp = int(auth_context.get("exp", 0))
    if exp <= int(time.time()):
        return False, "auth_context expired"

    unsigned_context = {field: auth_context[field] for field in required_fields if field != "signature"}
    expected_sig = sign_auth_context(unsigned_context)
    if not hmac.compare_digest(auth_context.get("signature", ""), expected_sig):
        return False, "signature mismatch"

    return True, ""
