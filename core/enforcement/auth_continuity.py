"""
core/enforcement/auth_continuity.py — F11 Amanah Handshake

Strict session continuity through cryptographic chaining.
Ensures that a session cannot be hijacked or forged between tool calls.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import hashlib
import hmac
import json
import os
import secrets
import time
import warnings
from typing import Any

# HMAC signs the actor's context so the kernel can verify it across calls
# without keeping a large in-memory state for every hop.


def _env_flag(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def _load_governance_token_secret() -> str:
    if _env_flag("ARIFOS_GOVERNANCE_OPEN_MODE"):
        return "arifos-open-governance-dev-mode"

    for env_name in ("ARIFOS_GOVERNANCE_SECRET", "ARIFOS_GOVERNANCE_TOKEN_SECRET"):
        secret = os.getenv(env_name, "").strip()
        if secret:
            return secret

    warnings.warn(
        (
            "ARIFOS_GOVERNANCE_SECRET is not set; using a process-local ephemeral secret. "
            "Set a stable secret in deployment so auth_context signatures remain valid "
            "across restarts and replicas."
        ),
        RuntimeWarning,
        stacklevel=2,
    )
    return secrets.token_hex(32)


_GOVERNANCE_TOKEN_SECRET = _load_governance_token_secret()
_AUTH_VERIFY_CACHE_TTL_SECONDS = 60
_auth_verify_cache: dict[str, tuple[bool, str, float, str]] = {}


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

    unsigned_context = {
        field: auth_context[field] for field in required_fields if field != "signature"
    }
    expected_sig = sign_auth_context(unsigned_context)
    if not hmac.compare_digest(auth_context.get("signature", ""), expected_sig):
        return False, "signature mismatch"

    return True, ""


def _auth_cache_key(session_id: str, auth_context: dict[str, Any]) -> str:
    signature = str(auth_context.get("signature", ""))
    expires_at = str(auth_context.get("exp", ""))
    fingerprint = str(auth_context.get("token_fingerprint", ""))
    payload = f"{session_id}:{signature}:{expires_at}:{fingerprint}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def verify_auth_context_cached(session_id: str, auth_context: dict[str, Any]) -> tuple[bool, str]:
    now = time.time()
    cache_key = _auth_cache_key(session_id, auth_context)
    cached = _auth_verify_cache.get(cache_key)
    if cached and (now - cached[2]) <= _AUTH_VERIFY_CACHE_TTL_SECONDS:
        return cached[0], cached[1]

    result = verify_auth_context(session_id, auth_context)
    _auth_verify_cache[cache_key] = (result[0], result[1], now, session_id)

    if len(_auth_verify_cache) > 2048:
        stale_keys = [
            key
            for key, (_, _, ts, _) in _auth_verify_cache.items()
            if (now - ts) > _AUTH_VERIFY_CACHE_TTL_SECONDS
        ]
        for key in stale_keys:
            _auth_verify_cache.pop(key, None)

    return result


def clear_auth_context_cache(session_id: str | None = None) -> None:
    if session_id is None:
        _auth_verify_cache.clear()
        return

    keys_to_remove = [
        key for key, (_, _, _, sid) in _auth_verify_cache.items() if sid == session_id
    ]
    for key in keys_to_remove:
        _auth_verify_cache.pop(key, None)
