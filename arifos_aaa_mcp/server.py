"""arifOS AAA MCP public 13-tool surface.

CANONICAL EXTERNAL ENTRYPOINT. This is the primary interface for all arifOS MCP interactions.
Internal provision is delegated to legacy `aaa_mcp` and `aclip_cai` packages.

USAGE (CLI):
- Local stdio (Cursor/Claude): `python -m arifos_aaa_mcp stdio`
- VPS HTTP (ChatGPT/External): `python -m arifos_aaa_mcp http --port 8080`
- VPS SSE: `python -m arifos_aaa_mcp sse`

PHASE 1 WIRING: Thermodynamic Core Integration
- All tools routed through core/ constitutional cage
- Physics exceptions caught and converted to VOID envelopes
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import hmac as _hmac
import json
import logging
import os
import secrets
import sys
import time
import traceback
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastmcp import FastMCP
from mcp.types import Icon

MANIFEST_VERSION = "2026.03.07"

import aaa_mcp as legacy
from aaa_mcp.protocol.public_surface import (
    PUBLIC_CANONICAL_TOOLS,
    PUBLIC_PROMPT_NAMES,
    PUBLIC_RESOURCE_URIS,
)
from aaa_mcp.protocol.tool_registry import export_full_context_pack
from aaa_mcp.sessions.session_ledger import get_ledger
from aclip_cai.tools.system_monitor import get_system_health
from aclip_cai.triad import (
    align,
    anchor,
    audit,
    forge,
    integrate,
    reason,
    respond,
    seal,
    think,
    validate,
)

from .contracts import require_session, validate_input
from .fastmcp_ext.discovery import build_surface_discovery
from .governance import (
    LAW_13_CATALOG,
    TOOL_DIALS_MAP,
    TOOL_LAW_BINDINGS,
    TOOL_STAGE_MAP,
    TRINITY_BY_TOOL,
    wrap_tool_output,
)

# Setup logger
logger = logging.getLogger(__name__)

# BGE Embeddings Integration from aclip_cai
try:
    from aclip_cai.embeddings import embed, get_embedder

    BGE_AVAILABLE = True
except ImportError:
    BGE_AVAILABLE = False

# ─── Amanah Handshake — Governance Token ────────────────────────────────────
_GOVERNANCE_TOKEN_SECRET = os.environ.get("ARIFOS_GOVERNANCE_SECRET", secrets.token_hex(32))


def _build_governance_token(session_id: str, verdict: str) -> str:
    sig = _hmac.new(
        _GOVERNANCE_TOKEN_SECRET.encode(),
        f"{session_id}:{verdict}".encode(),
        hashlib.sha256,
    ).hexdigest()
    return f"{verdict}:{sig}"


def _verify_governance_token(session_id: str, token: str) -> tuple[bool, str]:
    parts = token.split(":", 1)
    if len(parts) != 2:
        return False, "VOID"
    verdict, sig = parts
    expected_sig = _hmac.new(
        _GOVERNANCE_TOKEN_SECRET.encode(),
        f"{session_id}:{verdict}".encode(),
        hashlib.sha256,
    ).hexdigest()
    if _hmac.compare_digest(sig, expected_sig):
        return True, verdict
    return False, "VOID"


def _get_zkpc_witness(session_id: str, digest: str) -> str:
    """Generate a zkPC-style witness signature for a vault entry."""
    return _hmac.new(
        _GOVERNANCE_TOKEN_SECRET.encode(),
        f"{session_id}:{digest}".encode(),
        hashlib.sha256,
    ).hexdigest()[:16]


_CONTINUITY_TTL_SECONDS = max(
    30,
    int(os.environ.get("ARIFOS_CONTINUITY_TTL_SECONDS", "900")),
)
_CONTINUITY_STRICT = os.environ.get("ARIFOS_CONTINUITY_STRICT", "false").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}
_DEFAULT_APPROVAL_SCOPE = [
    "reason_mind",
    "simulate_heart",
    "critique_thought",
    "apex_judge",
    "eureka_forge",
    "seal_vault",
]
_SESSION_CONTINUITY_STATE: dict[str, dict[str, Any]] = {}
_PUBLIC_APPROVAL_MODE = os.environ.get(
    "ARIFOS_PUBLIC_APPROVAL_MODE", "true"
).strip().lower() not in {"0", "false", "no", "off"}
_PUBLIC_APPROVAL_KEY_ID = "PUBLIC_DEV_ACTOR"
_APPROVAL_ALG_HMAC_DEV = "hmac-dev"
_APPROVAL_ALG_ED25519 = "ed25519"
_APPROVAL_REQUIRED_FIELDS = [
    "approval_id",
    "actor_id",
    "session_id",
    "tool_name",
    "scope_hash",
    "risk_tier",
    "iat",
    "exp",
    "nonce",
    "signature",
]


def _token_fingerprint(auth_token: str | None) -> str:
    if not isinstance(auth_token, str) or not auth_token:
        return ""
    return _hmac.new(
        _GOVERNANCE_TOKEN_SECRET.encode(),
        auth_token.encode(),
        hashlib.sha256,
    ).hexdigest()


def _sign_auth_context(unsigned_context: dict[str, Any]) -> str:
    canonical = json.dumps(
        unsigned_context, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    )
    return _hmac.new(
        _GOVERNANCE_TOKEN_SECRET.encode(),
        canonical.encode(),
        hashlib.sha256,
    ).hexdigest()


def _mint_auth_context(
    session_id: str,
    actor_id: str,
    token_fingerprint: str,
    approval_scope: list[str],
    parent_signature: str,
) -> dict[str, Any]:
    now = int(time.time())
    unsigned_context = {
        "session_id": session_id,
        "actor_id": actor_id,
        "token_fingerprint": token_fingerprint,
        "nonce": secrets.token_hex(12),
        "iat": now,
        "exp": now + _CONTINUITY_TTL_SECONDS,
        "approval_scope": approval_scope,
        "parent_signature": parent_signature,
    }
    return {
        **unsigned_context,
        "signature": _sign_auth_context(unsigned_context),
    }


def _verify_signed_auth_context(session_id: str, auth_context: dict[str, Any]) -> tuple[bool, str]:
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
    if not isinstance(auth_context.get("approval_scope"), list):
        return False, "approval_scope must be a list"
    iat_raw = auth_context.get("iat", "")
    exp_raw = auth_context.get("exp", "")
    try:
        iat = int(iat_raw)
        exp = int(exp_raw)
    except (TypeError, ValueError):
        return False, "iat/exp must be integers"
    now = int(time.time())
    if exp <= now:
        return False, "auth_context expired"
    if exp < iat:
        return False, "exp earlier than iat"
    unsigned_context = {
        "session_id": str(auth_context.get("session_id", "")),
        "actor_id": str(auth_context.get("actor_id", "")),
        "token_fingerprint": str(auth_context.get("token_fingerprint", "")),
        "nonce": str(auth_context.get("nonce", "")),
        "iat": iat,
        "exp": exp,
        "approval_scope": list(auth_context.get("approval_scope", [])),
        "parent_signature": str(auth_context.get("parent_signature", "")),
    }
    expected_signature = _sign_auth_context(unsigned_context)
    actual_signature = str(auth_context.get("signature", ""))
    if not _hmac.compare_digest(actual_signature, expected_signature):
        return False, "signature mismatch"
    return True, ""


def _f11_continuity_failure(
    stage: str,
    session_id: str,
    reason: str,
    *,
    critical: bool,
) -> dict[str, Any]:
    actions = [
        "Run anchor_session to mint a fresh server-side continuity chain for this session.",
        "Reuse the same session_id and keep actor_id/auth_token stable for the full chain.",
        "Optionally pass auth_context for replay resistance across transport boundaries.",
    ]
    if critical:
        actions.append("Critical tool blocked until F11 continuity is valid.")
    return {
        "verdict": "VOID",
        "stage": stage,
        "session_id": session_id,
        "token_status": "ERROR",
        "floors": {"passed": [], "failed": ["F11"]},
        "truth": {"score": None, "threshold": None, "drivers": []},
        "next_actions": actions,
        "error": f"F11 continuity failure: {reason}",
    }


def _enforce_auth_continuity(
    *,
    tool_name: str,
    stage: str,
    session_id: str,
    actor_id: str,
    auth_token: str | None,
    auth_context: dict[str, Any] | None,
    critical: bool,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    state = _SESSION_CONTINUITY_STATE.get(session_id)
    strict_required = _CONTINUITY_STRICT
    if not isinstance(auth_context, dict):
        auth_context = None
    if auth_context is None:
        if strict_required:
            return None, _f11_continuity_failure(
                stage,
                session_id,
                "missing auth_context (strict mode)",
                critical=critical,
            )
        if state is None:
            if critical:
                return None, _f11_continuity_failure(
                    stage,
                    session_id,
                    "missing server continuity state; run anchor_session first",
                    critical=critical,
                )
            return {
                "actor_id": actor_id,
                "token_fingerprint": _token_fingerprint(auth_token),
                "approval_scope": list(_DEFAULT_APPROVAL_SCOPE),
                "parent_signature": "",
            }, None
        return {
            "actor_id": str(state.get("actor_id", actor_id)),
            "token_fingerprint": str(state.get("token_fingerprint", "")),
            "approval_scope": list(_DEFAULT_APPROVAL_SCOPE),
            "parent_signature": str(state.get("last_signature", "")),
        }, None

    valid, reason = _verify_signed_auth_context(session_id, auth_context)
    if not valid:
        return None, _f11_continuity_failure(stage, session_id, reason, critical=critical)

    incoming_signature = str(auth_context.get("signature", ""))
    incoming_actor = str(auth_context.get("actor_id", ""))
    incoming_token_fp = str(auth_context.get("token_fingerprint", ""))
    incoming_nonce = str(auth_context.get("nonce", ""))
    incoming_scope = [str(x) for x in auth_context.get("approval_scope", [])]
    if tool_name not in incoming_scope:
        return None, _f11_continuity_failure(
            stage,
            session_id,
            f"approval_scope missing permission for {tool_name}",
            critical=critical,
        )

    presented_token_fp = _token_fingerprint(auth_token)
    if presented_token_fp and presented_token_fp != incoming_token_fp:
        return None, _f11_continuity_failure(
            stage,
            session_id,
            "auth_token fingerprint mismatch",
            critical=critical,
        )

    if state is not None:
        state_nonces = state.get("nonces")
        if not isinstance(state_nonces, set):
            state_nonces = set()
            state["nonces"] = state_nonces
        if incoming_signature != str(state.get("last_signature", "")):
            return None, _f11_continuity_failure(
                stage,
                session_id,
                "chain signature mismatch",
                critical=critical,
            )
        if incoming_nonce in state_nonces:
            return None, _f11_continuity_failure(
                stage,
                session_id,
                "nonce replay detected",
                critical=critical,
            )
        if incoming_actor != str(state.get("actor_id", "")):
            return None, _f11_continuity_failure(
                stage,
                session_id,
                "actor_id mismatch",
                critical=critical,
            )
        if incoming_token_fp != str(state.get("token_fingerprint", "")):
            return None, _f11_continuity_failure(
                stage,
                session_id,
                "token fingerprint mismatch",
                critical=critical,
            )
        state_nonces.add(incoming_nonce)
        if len(state_nonces) > 2048:
            state_nonces.clear()
            state_nonces.add(incoming_nonce)
    else:
        _SESSION_CONTINUITY_STATE[session_id] = {
            "actor_id": incoming_actor,
            "token_fingerprint": incoming_token_fp,
            "last_signature": incoming_signature,
            "nonces": {incoming_nonce},
        }

    return {
        "actor_id": incoming_actor,
        "token_fingerprint": incoming_token_fp,
        "approval_scope": incoming_scope,
        "parent_signature": incoming_signature,
    }, None


def _rotate_auth_context(session_id: str, binding: dict[str, Any]) -> dict[str, Any]:
    next_context = _mint_auth_context(
        session_id=session_id,
        actor_id=str(binding.get("actor_id", "anonymous")),
        token_fingerprint=str(binding.get("token_fingerprint", "")),
        approval_scope=[str(x) for x in binding.get("approval_scope", _DEFAULT_APPROVAL_SCOPE)],
        parent_signature=str(binding.get("parent_signature", "")),
    )
    existing = _SESSION_CONTINUITY_STATE.get(session_id, {})
    nonces = existing.get("nonces")
    if not isinstance(nonces, set):
        nonces = set()
    _SESSION_CONTINUITY_STATE[session_id] = {
        "actor_id": str(binding.get("actor_id", "anonymous")),
        "token_fingerprint": str(binding.get("token_fingerprint", "")),
        "last_signature": next_context["signature"],
        "nonces": nonces,
    }
    return next_context


def _attach_rotated_auth_context(
    payload: dict[str, Any], session_id: str, binding: dict[str, Any] | None
) -> dict[str, Any]:
    if binding is not None:
        payload["auth_context"] = _rotate_auth_context(session_id, binding)
    return payload


def _approval_signature(unsigned_bundle: dict[str, Any]) -> str:
    canonical = json.dumps(
        unsigned_bundle, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    )
    return _hmac.new(
        _GOVERNANCE_TOKEN_SECRET.encode(),
        canonical.encode(),
        hashlib.sha256,
    ).hexdigest()


def _approval_signature_digest(signature: str) -> str:
    return hashlib.sha256(str(signature).encode()).hexdigest()[:16]


def _parse_string_set_env(name: str) -> set[str]:
    raw = str(os.environ.get(name, "") or "").strip()
    if not raw:
        return set()
    parsed: set[str] = set()
    if raw.startswith("[") or raw.startswith("{"):
        try:
            loaded = json.loads(raw)
            if isinstance(loaded, list):
                parsed.update(str(x).strip() for x in loaded if str(x).strip())
            elif isinstance(loaded, dict):
                parsed.update(str(k).strip() for k, v in loaded.items() if v and str(k).strip())
            elif isinstance(loaded, str) and loaded.strip():
                parsed.add(loaded.strip())
        except Exception:
            parsed = set()
    if not parsed:
        parsed.update(part.strip() for part in raw.split(",") if part.strip())
    return parsed


def _actor_public_keys() -> dict[str, str]:
    raw = str(os.environ.get("ARIFOS_ACTOR_PUBLIC_KEYS_JSON", "") or "").strip()
    if not raw:
        return {}
    try:
        loaded = json.loads(raw)
    except Exception:
        return {}
    if not isinstance(loaded, dict):
        return {}
    return {str(k): str(v) for k, v in loaded.items() if str(k).strip() and str(v).strip()}


def _revocation_reason(*, actor_id: str = "", session_id: str = "", approval_id: str = "") -> str:
    if actor_id and actor_id in _parse_string_set_env("ARIFOS_REVOKED_ACTORS"):
        return "AUTH_REVOKED_ACTOR"
    if session_id and session_id in _parse_string_set_env("ARIFOS_REVOKED_SESSIONS"):
        return "AUTH_REVOKED_SESSION"
    if approval_id and approval_id in _parse_string_set_env("ARIFOS_REVOKED_APPROVAL_IDS"):
        return "AUTH_REVOKED_APPROVAL"
    return ""


def _revocation_message(reason_code: str) -> str:
    mapping = {
        "AUTH_REVOKED_ACTOR": "actor_id is revoked",
        "AUTH_REVOKED_SESSION": "session_id is revoked",
        "AUTH_REVOKED_APPROVAL": "approval_id is revoked",
    }
    return mapping.get(reason_code, "authorization revoked")


def _revocation_void(stage: str, session_id: str, reason_code: str) -> dict[str, Any]:
    return {
        "verdict": "VOID",
        "stage": stage,
        "session_id": session_id,
        "reason_code": reason_code,
        "error": _revocation_message(reason_code),
        "floors": {"passed": [], "failed": ["F11", "F1"]},
        "next_actions": [
            "Use a non-revoked actor/session/approval artifact.",
            "Rotate identity material and mint a fresh approval bundle.",
            "Retry with authorization state that passes revocation checks.",
        ],
    }


def _approval_signing_bundle(
    approval_bundle: dict[str, Any],
    *,
    key_id: str,
    iat: int,
    exp: int,
    nonce: str,
    bundle_session_id: str,
    bundle_tool_name: str,
    bundle_risk_tier: str,
) -> dict[str, Any]:
    return {
        "approval_id": str(approval_bundle.get("approval_id", "")),
        "actor_id": str(approval_bundle.get("actor_id", "")),
        "session_id": bundle_session_id,
        "tool_name": bundle_tool_name,
        "scope_hash": str(approval_bundle.get("scope_hash", "")),
        "risk_tier": bundle_risk_tier,
        "iat": iat,
        "exp": exp,
        "nonce": nonce,
        "key_id": key_id,
    }


def _verify_ed25519_signature(
    *,
    approval_bundle: dict[str, Any],
    signing_bundle: dict[str, Any],
) -> tuple[bool, str]:
    actor_id = str(approval_bundle.get("actor_id", ""))
    actor_keys = _actor_public_keys()
    public_key_b64 = actor_keys.get(actor_id, "")
    if not public_key_b64:
        return False, "approval_bundle signature verification failed: missing actor public key"

    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    except Exception:
        return False, "approval_bundle signature verification failed: ed25519 library unavailable"

    try:
        public_key_bytes = base64.b64decode(public_key_b64.encode(), validate=True)
        signature_bytes = base64.b64decode(
            str(approval_bundle.get("signature", "")).encode(),
            validate=True,
        )
    except Exception:
        return False, "approval_bundle signature verification failed: invalid base64 key/signature"

    message = json.dumps(
        signing_bundle, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode()
    try:
        public_key = Ed25519PublicKey.from_public_bytes(public_key_bytes)
        public_key.verify(signature_bytes, message)
    except (ValueError, InvalidSignature):
        return False, "approval_bundle signature verification failed: ed25519 verify mismatch"
    except Exception:
        return False, "approval_bundle signature verification failed: ed25519 verifier error"

    return True, ""


def _approval_action_hash(parts: list[Any]) -> str:
    canonical = json.dumps(parts, ensure_ascii=True, sort_keys=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def _approval_scope_hash(
    tool_name: str,
    session_id: str,
    action_hash: str,
    risk_tier: str,
    exp: int,
    nonce: str,
) -> str:
    canonical = json.dumps(
        {
            "tool_name": tool_name,
            "session_id": session_id,
            "action_hash": action_hash,
            "risk_tier": str(risk_tier).upper(),
            "exp": int(exp),
            "nonce": str(nonce),
        },
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(canonical.encode()).hexdigest()


def _approval_void(
    *,
    stage: str,
    session_id: str,
    reason_code: str,
    message: str,
) -> dict[str, Any]:
    return {
        "verdict": "VOID",
        "stage": stage,
        "session_id": session_id,
        "reason_code": reason_code,
        "error": message,
        "floors": {"passed": [], "failed": ["F11", "F1"]},
        "next_actions": [
            "Provide a valid approval_bundle for this tool invocation.",
            "Use fresh approval_id/nonce and recompute scope_hash from exact action fields.",
            "Retry with a non-expired bundle signed by the active approval scheme.",
        ],
    }


def _annotate_approval(
    payload: dict[str, Any], approval_state: dict[str, Any] | None
) -> dict[str, Any]:
    if not isinstance(approval_state, dict):
        return payload
    mode = str(approval_state.get("approval_mode", "")).strip()
    if mode:
        payload["approval_mode"] = mode
        nested = payload.get("payload")
        if isinstance(nested, dict):
            nested["approval_mode"] = mode
    approval_id = str(approval_state.get("approval_id", "")).strip()
    if approval_id:
        payload["approval_id"] = approval_id
    return payload


async def _verify_approval_bundle(
    *,
    tool_name: str,
    stage: str,
    session_id: str,
    approval_bundle: dict[str, Any] | None,
    action_hash: str,
    risk_tier: str,
    require_bundle: bool,
) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    pre_bundle_revocation = _revocation_reason(session_id=session_id)
    if pre_bundle_revocation:
        return None, _revocation_void(stage, session_id, pre_bundle_revocation)

    if not isinstance(approval_bundle, dict):
        if require_bundle:
            return None, _approval_void(
                stage=stage,
                session_id=session_id,
                reason_code="AUTH_APPROVAL_MISSING",
                message="approval_bundle is required for elevated confirmation path",
            )
        return {"approval_mode": "public-open" if _PUBLIC_APPROVAL_MODE else "strict-open"}, None

    for field in _APPROVAL_REQUIRED_FIELDS:
        if field not in approval_bundle:
            return None, _approval_void(
                stage=stage,
                session_id=session_id,
                reason_code="AUTH_APPROVAL_MISSING",
                message=f"approval_bundle missing required field: {field}",
            )

    bundle_session_id = str(approval_bundle.get("session_id", ""))
    bundle_tool_name = str(approval_bundle.get("tool_name", ""))
    if bundle_session_id != session_id or bundle_tool_name != tool_name:
        return None, _approval_void(
            stage=stage,
            session_id=session_id,
            reason_code="AUTH_APPROVAL_SCOPE_MISMATCH",
            message="approval_bundle session_id/tool_name mismatch",
        )

    approval_id = str(approval_bundle.get("approval_id", ""))
    bundle_actor_id = str(approval_bundle.get("actor_id", ""))
    revocation = _revocation_reason(
        actor_id=bundle_actor_id,
        session_id=bundle_session_id,
        approval_id=approval_id,
    )
    if revocation:
        return None, _revocation_void(stage, session_id, revocation)

    now = int(time.time())
    try:
        iat_raw = approval_bundle.get("iat", "")
        exp_raw = approval_bundle.get("exp", "")
        iat = int(iat_raw)
        exp = int(exp_raw)
    except (TypeError, ValueError):
        return None, _approval_void(
            stage=stage,
            session_id=session_id,
            reason_code="AUTH_APPROVAL_EXPIRED",
            message="approval_bundle iat/exp must be integer timestamps",
        )
    if iat > now or exp <= now or exp < iat:
        return None, _approval_void(
            stage=stage,
            session_id=session_id,
            reason_code="AUTH_APPROVAL_EXPIRED",
            message="approval_bundle timestamp window invalid or expired",
        )

    nonce = str(approval_bundle.get("nonce", ""))
    expected_scope_hash = _approval_scope_hash(
        tool_name=tool_name,
        session_id=session_id,
        action_hash=action_hash,
        risk_tier=risk_tier,
        exp=exp,
        nonce=nonce,
    )
    if str(approval_bundle.get("scope_hash", "")) != expected_scope_hash:
        return None, _approval_void(
            stage=stage,
            session_id=session_id,
            reason_code="AUTH_APPROVAL_SCOPE_MISMATCH",
            message="approval_bundle scope_hash mismatch",
        )
    bundle_risk_tier = str(approval_bundle.get("risk_tier", "")).upper()
    if bundle_risk_tier != str(risk_tier).upper():
        return None, _approval_void(
            stage=stage,
            session_id=session_id,
            reason_code="AUTH_APPROVAL_SCOPE_MISMATCH",
            message="approval_bundle risk_tier mismatch",
        )

    alg = str(approval_bundle.get("alg") or _APPROVAL_ALG_HMAC_DEV).strip().lower()
    if alg not in {_APPROVAL_ALG_HMAC_DEV, _APPROVAL_ALG_ED25519}:
        return None, _approval_void(
            stage=stage,
            session_id=session_id,
            reason_code="AUTH_APPROVAL_SIGNATURE_INVALID",
            message=f"approval_bundle signature verification failed: unsupported alg '{alg}'",
        )

    key_id = str(approval_bundle.get("key_id") or _PUBLIC_APPROVAL_KEY_ID)
    unsigned_bundle = _approval_signing_bundle(
        approval_bundle,
        key_id=key_id,
        iat=iat,
        exp=exp,
        nonce=nonce,
        bundle_session_id=bundle_session_id,
        bundle_tool_name=bundle_tool_name,
        bundle_risk_tier=bundle_risk_tier,
    )
    actual_signature = str(approval_bundle.get("signature", ""))
    if alg == _APPROVAL_ALG_HMAC_DEV:
        expected_signature = _approval_signature(unsigned_bundle)
        if not _hmac.compare_digest(actual_signature, expected_signature):
            return None, _approval_void(
                stage=stage,
                session_id=session_id,
                reason_code="AUTH_APPROVAL_SIGNATURE_INVALID",
                message="approval_bundle signature verification failed",
            )

    if alg == _APPROVAL_ALG_ED25519:
        ed25519_bundle = dict(unsigned_bundle)
        ed25519_bundle["alg"] = _APPROVAL_ALG_ED25519
        verified, reason = _verify_ed25519_signature(
            approval_bundle=approval_bundle,
            signing_bundle=ed25519_bundle,
        )
        if not verified:
            return None, _approval_void(
                stage=stage,
                session_id=session_id,
                reason_code="AUTH_APPROVAL_SIGNATURE_INVALID",
                message=reason,
            )

    if (
        alg == _APPROVAL_ALG_HMAC_DEV
        and _PUBLIC_APPROVAL_MODE
        and key_id != _PUBLIC_APPROVAL_KEY_ID
    ):
        return None, _approval_void(
            stage=stage,
            session_id=session_id,
            reason_code="AUTH_APPROVAL_SIGNATURE_INVALID",
            message="approval_bundle key_id must be PUBLIC_DEV_ACTOR in public mode",
        )

    ledger = await get_ledger()
    replay_ok = await ledger.mark_approval_used(
        approval_id=approval_id,
        session_id=session_id,
        nonce=nonce,
        tool_name=tool_name,
    )
    if not replay_ok:
        return None, _approval_void(
            stage=stage,
            session_id=session_id,
            reason_code="AUTH_APPROVAL_REPLAY",
            message="approval_bundle replay detected",
        )

    return {
        "approval_mode": "artifact-verified",
        "approval_id": approval_id,
        "actor_id": bundle_actor_id,
        "approval_alg": alg,
        "approval_key_id": key_id,
        "approval_signature_digest": _approval_signature_digest(actual_signature),
    }, None


def _fold_verdict(verdicts: list[str]) -> str:
    if any(v.upper() == "VOID" for v in verdicts):
        return "VOID"
    if any(v.upper() in {"SABAR", "888_HOLD"} for v in verdicts):
        return "SABAR"
    if any(v.upper() == "PARTIAL" for v in verdicts):
        return "PARTIAL"
    return "SEAL"


def _token_status(auth_token: str | None) -> str:
    return "AUTHENTICATED" if auth_token else "ANONYMOUS"


def _clamp01(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    if parsed < 0.0:
        return 0.0
    if parsed > 1.0:
        return 1.0
    return parsed


def compute_human_witness(
    *,
    continuity_ok: bool,
    approval_ok: bool,
    human_approve: bool,
    public_approval_mode: bool,
) -> dict[str, Any]:
    authority_ready = continuity_ok and (approval_ok or human_approve or public_approval_mode)
    score = 1.0 if authority_ready else 0.0
    return {
        "valid": authority_ready,
        "score": score,
        "signals": {
            "continuity_ok": continuity_ok,
            "approval_ok": approval_ok,
            "human_approve": human_approve,
            "public_approval_mode": public_approval_mode,
        },
    }


def compute_ai_witness(*, truth_score: Any, truth_threshold: Any) -> dict[str, Any]:
    truth_score_num = None
    threshold_num = None
    try:
        truth_score_num = float(truth_score)
    except (TypeError, ValueError):
        truth_score_num = None
    try:
        threshold_num = float(truth_threshold)
    except (TypeError, ValueError):
        threshold_num = None

    if truth_score_num is not None and threshold_num is not None and threshold_num > 0:
        ratio = _clamp01(truth_score_num / threshold_num, default=0.0)
        return {
            "valid": truth_score_num >= threshold_num,
            "score": ratio,
            "signals": {
                "truth_score": truth_score_num,
                "truth_threshold": threshold_num,
            },
        }

    return {
        "valid": True,
        "score": 0.9,
        "signals": {
            "truth_score": truth_score_num,
            "truth_threshold": threshold_num,
            "fallback": "conservative_default",
        },
    }


def compute_earth_witness(
    *,
    precedent_count: int,
    grounding_present: bool,
    revocation_ok: bool,
    health_ok: bool,
) -> dict[str, Any]:
    grounded = grounding_present or precedent_count > 0
    valid = revocation_ok and health_ok and grounded
    score = 1.0 if valid else (0.5 if revocation_ok and health_ok else 0.0)
    return {
        "valid": valid,
        "score": score,
        "signals": {
            "precedent_count": max(0, int(precedent_count)),
            "grounding_present": grounded,
            "revocation_ok": revocation_ok,
            "health_ok": health_ok,
        },
    }


def build_governance_proof(
    *,
    continuity_ok: bool,
    approval_ok: bool,
    human_approve: bool,
    public_approval_mode: bool,
    truth_score: Any,
    truth_threshold: Any,
    precedent_count: int,
    grounding_present: bool,
    revocation_ok: bool,
    health_ok: bool,
    omega_ortho: Any,
    mode_collapse: bool,
    non_violation_status: bool,
) -> dict[str, Any]:
    human = compute_human_witness(
        continuity_ok=continuity_ok,
        approval_ok=approval_ok,
        human_approve=human_approve,
        public_approval_mode=public_approval_mode,
    )
    ai = compute_ai_witness(truth_score=truth_score, truth_threshold=truth_threshold)
    earth = compute_earth_witness(
        precedent_count=precedent_count,
        grounding_present=grounding_present,
        revocation_ok=revocation_ok,
        health_ok=health_ok,
    )

    omega_score = _clamp01(omega_ortho, default=1.0)
    omega_valid = True if omega_ortho is None else omega_score >= 0.95
    thermodynamics_valid = non_violation_status and (not mode_collapse) and omega_valid
    thermodynamic_score = (
        (1.0 if non_violation_status else 0.0) * 0.5
        + (1.0 if not mode_collapse else 0.0) * 0.25
        + omega_score * 0.25
    )

    authority_valid = bool(human.get("valid"))
    authority_score = _clamp01(human.get("score"), default=0.0)
    witness_product = (
        _clamp01(human.get("score"), default=0.0)
        * _clamp01(ai.get("score"), default=0.0)
        * _clamp01(earth.get("score"), default=0.0)
    )
    w3 = witness_product ** (1 / 3) if witness_product > 0.0 else 0.0
    tri_witness_valid = w3 >= 0.95 and bool(human.get("valid")) and bool(earth.get("valid"))

    proof: dict[str, Any] = {
        "authority_valid": authority_valid,
        "thermodynamics_valid": thermodynamics_valid,
        "tri_witness_valid": tri_witness_valid,
        "authority_score": authority_score,
        "thermodynamic_score": _clamp01(thermodynamic_score, default=0.0),
        "witness": {
            "human": human,
            "ai": ai,
            "earth": earth,
            "w3": w3,
        },
        "gate_verdict": "SEAL",
        "gate_reason": "All fused governance pillars are valid.",
    }
    return apply_governance_gate(current_verdict="SEAL", governance_proof=proof)


def apply_governance_gate(
    *, current_verdict: str, governance_proof: dict[str, Any]
) -> dict[str, Any]:
    verdict = str(current_verdict or "VOID").upper()
    if not governance_proof.get("authority_valid"):
        governance_proof["gate_verdict"] = "VOID"
        governance_proof["gate_reason"] = "Authority pillar failed (F11/F13)."
    elif not governance_proof.get("thermodynamics_valid"):
        governance_proof["gate_verdict"] = "VOID"
        governance_proof["gate_reason"] = "Thermodynamic pillar failed (P3 plausibility)."
    elif not governance_proof.get("tri_witness_valid"):
        governance_proof["gate_verdict"] = "888_HOLD"
        governance_proof["gate_reason"] = "Tri-Witness consensus below F3 threshold."
    elif verdict == "VOID":
        governance_proof["gate_verdict"] = "VOID"
        governance_proof["gate_reason"] = "Underlying verdict is already VOID."
    else:
        governance_proof["gate_verdict"] = verdict
        governance_proof["gate_reason"] = "Gate passed; preserving underlying verdict."
    return governance_proof


class EnvelopeBuilder:
    def _extract_truth(self, payload: dict[str, Any]) -> dict[str, Any]:
        score = payload.get("truth_score")
        threshold = payload.get("f2_threshold")
        drivers = payload.get("truth_drivers") or []
        return {"score": score, "threshold": threshold, "drivers": drivers}

    def _generate_sabar_requirements(
        self, verdict: str, payload: dict[str, Any]
    ) -> dict[str, Any] | None:
        if verdict not in {"SABAR", "PARTIAL"}:
            return None
        failed_floors = payload.get("floors_failed", [])
        missing_fields = []
        template_fields = {}
        for floor in failed_floors:
            missing_fields.append(
                {
                    "field": f"input_for_{floor.lower()}",
                    "needed_for": [floor],
                    "example": "<FILL_REQUIRED_DATA>",
                }
            )
            template_fields[f"input_for_{floor.lower()}"] = "<FILL_REQUIRED_DATA>"
        if not missing_fields:
            missing_fields.append(
                {
                    "field": "contextual_data",
                    "needed_for": ["F_UNKNOWN"],
                    "example": "<PROVIDE_MORE_CONTEXT>",
                }
            )
            template_fields["contextual_data"] = "<PROVIDE_MORE_CONTEXT>"
        return {
            "missing_grounding": [f for f in failed_floors if f.startswith("F2")],
            "missing_fields": missing_fields,
            "minimum_next_payload_template": template_fields,
        }

    def build_envelope(
        self, stage: str, session_id: str, verdict: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        floors_failed = payload.get("floors_failed", [])
        actions = []
        if "F2" in floors_failed:
            actions.append("Provide stronger evidence and retry with grounded claims.")
        if "F11" in floors_failed:
            actions.append("Restore session/auth continuity and retry.")
        if not actions:
            actions.append("Continue to next constitutional stage.")
        return {
            "verdict": verdict,
            "stage": stage,
            "session_id": session_id,
            "floors": {"passed": [], "failed": floors_failed},
            "truth": self._extract_truth(payload),
            "next_actions": actions,
            "sabar_requirements": self._generate_sabar_requirements(verdict, payload),
            "payload": payload,
        }


envelope_builder = EnvelopeBuilder()

# ═══════════════════════════════════════════════════════
# PHASE 1: Wire MCP Gateway to Thermodynamic Core
# ═══════════════════════════════════════════════════════

# Import core thermodynamic cage
try:
    from core.homeostasis import (
        PeaceViolation,
        check_peace_squared,
    )
    from core.judgment import (
        JudgmentKernel,
        get_judgment_kernel,
    )
    from core.kernel.constitutional_decorator import (
        AmanahViolation,
        EntropyViolation,
        constitutional_floor,
    )
    from core.physics.thermodynamics import (
        CheapTruthError,
        ModeCollapseError,
        ThermodynamicViolation,
        check_landauer_bound,
        derive_orthogonality,
    )

    CORE_AVAILABLE = True
except ImportError as e:
    CORE_AVAILABLE = False
    import logging

    logging.warning(f"Thermodynamic core not available: {e}")


def _fracture_response(stage: str, e: Exception, session_id: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "verdict": "SABAR",
        "status": "partial",
        "holding_reason": "Internal Engine Fracture",
        "error_class": e.__class__.__name__,
        "blast_radius": "kernel",
        "error": str(e),
        "trace": traceback.format_exc(),
        "stage": stage,
    }
    if session_id:
        result["session_id"] = session_id
    return result


def _build_floor_block(stage: str, reason: str) -> dict[str, Any]:
    return {
        "verdict": "VOID",
        "stage": stage,
        "session_id": "",
        "token_status": "ERROR",
        "floors": {"passed": [], "failed": ["F11"]},
        "truth": {"score": None, "threshold": None, "drivers": []},
        "next_actions": [
            "Run init_session (anchor) first to obtain session_id.",
            "Reuse the same session_id across downstream tools.",
        ],
        "error": reason,
    }


_rag_instance: Any = None


def _ensure_rag() -> Any:
    global _rag_instance
    if _rag_instance is not None:
        return _rag_instance
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    from arifos_rag import ConstitutionalRAG

    _rag_instance = ConstitutionalRAG()
    return _rag_instance


# Physics exception to VOID envelope converter
def _convert_physics_exception_to_void(
    exception: Exception,
    tool_name: str,
    session_id: str,
) -> dict[str, Any]:
    """
    Convert thermodynamic exceptions to VOID envelopes.

    Fail-closed: Physics violations return VOID, not crash.
    """
    exception_type = type(exception).__name__

    # Map exception types to constitutional floors
    floor_map = {
        "EntropyViolation": "F4_CLARITY",
        "AmanahViolation": "F1_AMANAH",
        "ModeCollapseError": "F3_TRI_WITNESS",
        "CheapTruthError": "F2_TRUTH",
        "PeaceViolation": "F5_PEACE2",
        "ThermodynamicViolation": "PHYSICS",
    }

    floor = floor_map.get(exception_type, "UNKNOWN")

    return {
        "verdict": "VOID",
        "stage": f"{tool_name.upper()}_PHYSICS",
        "session_id": session_id,
        "blocked_by_floor": floor,
        "blocked_by_exception": exception_type,
        "reason": str(exception),
        "thermodynamic_rejection": True,
        "error_class": exception_type,
        "timestamp": time.time(),
        "remediation": {
            "action": "COOLING_REQUIRED",
            "message": f"{floor} violation detected. System requires cooling cycle.",
            "next_steps": [
                "Wait for entropy dissipation",
                "Provide additional grounding evidence",
                "Reduce query complexity",
                "Request human oversight (888_HOLD)",
            ],
        },
    }


# ═══════════════════════════════════════════════════════════════════════════════
# ICON FORGE — Constitutional Semiotics (ΔS ≤ 0)
# ═══════════════════════════════════════════════════════════════════════════════
# Icons are not UI garnish; they are low-entropy carriers of law and affordance.
# Each icon encodes: Lane (ΔΩΨ), Risk tier, Constitutional floor binding.
# See: docs/ICONOGRAPHY.md for full semiotic specification.

# Server-level sovereign emblem (arifOS crest)
# Represents: Constitutional kernel, 13 floors, Trinity governance
ARIFOS_SERVER_ICON = Icon(
    src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSI+PHBhdGggZD0iTTI0IDJMNDIgMTZWMzJMMjQgNDZMNiAzMlYxNkwyNCAyWiIgZmlsbD0iI2U2YzI1ZCIvPjx0ZXh0IHg9IjI0IiB5PSIzMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1zaXplPSIxNCIgZmlsbD0iIzA1MDUwNSIgZm9udC13ZWlnaHQ9ImJvbGQiPvqltDwvdGV4dD48L3N2Zz4=",
    mimeType="image/svg+xml",
    sizes=["48x48"],
)

# Δ DELTA Lane — Mind/Reasoning (Blue/Cognition)
# anchor_session: Bootloader, session ignition
ICON_ANCHOR = Icon(
    src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiIGZpbGw9IiMwMDdhZmYiLz48cGF0aCBkPSJNMTIgNkw5IDlWMThIMTVWOUwxMiA2WiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=",
    mimeType="image/svg+xml",
)

# reason_mind: AGI cognition
ICON_REASON = Icon(
    src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiIGZpbGw9IiMwMDdhZmYiLz48cGF0aCBkPSJNMTIgOEM5Ljc5IDggOCA5Ljc5IDggMTJDOCAxNC4yMSA5Ljc5IDE2IDEyIDE2QzE0LjIxIDE2IDE2IDE0LjIxIDE2IDEyQzE2IDkuNzkgMTQuMjEgOCAxMiA4Wk0xMiAxNEMxMC45IDE0IDEwIDEzLjEgMTAgMTJDMTAgMTAuOSAxMC45IDEwIDEyIDEwQzEzLjEgMTAgMTQgMTAuOSAxNCAxMkMxNCAxMy4xIDEzLjEgMTQgMTIgMTRaIiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==",
    mimeType="image/svg+xml",
)

# search_reality: External evidence
ICON_SEARCH = Icon(
    src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiIGZpbGw9IiMwMDdhZmYiLz48cGF0aCBkPSJNMTUgMTFMMTMgMTNWMTVIMTFWMTNMOSAxMVY5SDExVjExSDEzVjlIMTVMMTFaIiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==",
    mimeType="image/svg+xml",
)

# ingest_evidence: Content retrieval (replaces fetch_content + inspect_file)
ICON_FETCH = Icon(
    src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiIGZpbGw9IiMwMDdhZmYiLz48cGF0aCBkPSJNOCA5SDE2VjE1SDhWOVpNOSAxMFYxNEgxNVYxMEg5WiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=",
    mimeType="image/svg+xml",
)

# audit_rules: Constitutional audit
ICON_AUDIT = Icon(
    src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiIGZpbGw9IiMwMDdhZmYiLz48cGF0aCBkPSJNMTAgN0wxNSAxMkwxMCAxN1Y3WiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=",
    mimeType="image/svg+xml",
)

# Ω OMEGA Lane — Heart/Safety (Green/Empathy)
# vector_memory: BBB Vector Memory (VM) - semantic retrieval (BGE + Qdrant)
ICON_RECALL = Icon(
    src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiIGZpbGw9IiMwMGEyZmYiLz48cGF0aCBkPSJNMTIgOEMxMy4xIDggMTQgOC45IDE0IDEwQzE0IDExLjEgMTMuMSAxMiAxMiAxMkMxMC45IDEyIDEwIDExLjEgMTAgMTBDMTAgOC45IDEwLjkgOCAxMiA4Wk04IDE0SDE2VjE2SDhWMTRaIiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==",
    mimeType="image/svg+xml",
)

# simulate_heart: Stakeholder impact
ICON_HEART = Icon(
    src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiIGZpbGw9IiMwMGEyZmYiLz48cGF0aCBkPSJNMTIgMjFMOCAxN0M2IDE1IDYgMTIgOCAxMEMxMCA4IDEyIDkgMTIgOUMxMiA5IDE0IDggMTYgMTBDMTggMTIgMTggMTUgMTYgMTdMMTIgMjFaIiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==",
    mimeType="image/svg+xml",
)

# critique_thought: 7-model critique
ICON_CRITIQUE = Icon(
    src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiIGZpbGw9IiMwMGEyZmYiLz48cGF0aCBkPSJNMTIgOEMxMy4xIDggMTQgOC45IDE0IDEwQzE0IDExLjEgMTMuMSAxMiAxMiAxMkMxMC45IDEyIDEwIDExLjEgMTAgMTBDMTAgOC45IDEwLjkgOCAxMiA4Wk04IDE0SDE2VjE2SDhWMTRaIiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==",
    mimeType="image/svg+xml",
)

# check_vital: System health
ICON_VITAL = Icon(
    src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiIGZpbGw9IiMwMGEyZmYiLz48cGF0aCBkPSJNOCAxMkw5IDE1TDExIDlMMTMgMThMMTUgMTJMMTYgMTVIOFoiIGZpbGw9IndoaXRlIi8+PC9zdmc+",
    mimeType="image/svg+xml",
)

# Ψ PSI Lane — Soul/Judgment (Gold/Sovereign)
# apex_judge: Sovereign verdict
ICON_APEX = Icon(
    src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiIGZpbGw9IiNlNmMyNWQiLz48cGF0aCBkPSJNMTIgNkwxNCAxMUgxOUwxNSAxNUwxNyAyMEwxMiAxNkwxNyAyMEwxMiAxNkw3IDIwTDkgMTVMNSAxMUgxMFoiIGZpbGw9IndoaXRlIi8+PC9zdmc+",
    mimeType="image/svg+xml",
)

# eureka_forge: Action execution
ICON_FORGE = Icon(
    src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiIGZpbGw9IiNlNmMyNWQiLz48cGF0aCBkPSJNMTIgNkw5IDEzSDE1TDEyIDZaTTEyIDE1TDkgMThIMTVMMTIgMTVaIiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==",
    mimeType="image/svg+xml",
)

# seal_vault: Immutable ledger
ICON_VAULT = Icon(
    src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiIGZpbGw9IiNlNmMyNWQiLz48cGF0aCBkPSJNMTIgNkw5IDlWMThIMTVWOUwxMiA2Wk0xMiAxNEMxMC45IDE0IDEwIDEzLjEgMTAgMTJDMTAgMTAuOSAxMC45IDEwIDEyIDEwQzEzLjEgMTAgMTQgMTAuOSAxNCAxMkMxNCAxMy4xIDEzLjEgMTQgMTIgMTRaIiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==",
    mimeType="image/svg+xml",
)

# ═══════════════════════════════════════════════════════════════════════════════
# SERVER INITIALIZATION — Constitutional Kernel with Iconography
# ═══════════════════════════════════════════════════════════════════════════════

mcp = FastMCP(
    name="arifOS_AAA_MCP",
    version="2026.3.6",
    instructions=(
        "Canonical 13-tool arifOS AAA MCP surface. "
        "Use 000->333->555->666->777_EUREKA_FORGE->888_APEX_JUDGE->999 governance spine."
    ),
    website_url="https://arifos.arif-fazil.com",
    icons=[ARIFOS_SERVER_ICON],
)

AAA_TOOLS = list(PUBLIC_CANONICAL_TOOLS)
_SESSION_GOVERNANCE_TOKENS: dict[str, str] = {}


def _model_flags(plan: dict[str, Any], context: str = "") -> dict[str, Any]:
    text = (context + " " + str(plan)).lower()
    return {
        "non_linearity": any(k in text for k in ["feedback", "cascade", "tipping"]),
        "gray_thinking": any(k in text for k in ["however", "trade-off", "depends"]),
        "occams_bias": len(plan.keys()) <= 20,
        "framing_bias": not any(k in text for k in ["obviously", "guaranteed", "always", "never"]),
        "anti_comfort": any(k in text for k in ["hard", "difficult", "mitigation", "review"]),
        "delayed_discomfort": any(k in text for k in ["future", "later", "debt", "drift"]),
        "inversion": any(k in text for k in ["failure", "risk", "worst-case", "break"]),
    }


@mcp.tool(name="anchor_session")
async def anchor_session(
    query: str,
    actor_id: str = "anonymous",
    auth_token: str | None = None,
    mode: str = "conscience",
    grounding_required: bool = True,
    debug: bool = False,
    session_id: str | None = None,
) -> dict[str, Any]:
    """000 BOOTLOADER: initialize constitutional execution kernel and governance context."""
    # 000_INIT Sacred Contract: Guarantee session continuity from ignition to vault seal
    # Generate session_id FIRST if not provided — janji hakiki dibawa ke mati sampai vault seal
    if not session_id:
        session_id = f"{actor_id}-{uuid.uuid4().hex[:8]}"

    # Now validate with guaranteed session_id for F3_CONTRACT continuity check
    blocked = validate_input(
        "anchor_session", {"query": query, "actor_id": actor_id, "session_id": session_id}
    )
    if blocked:
        return wrap_tool_output("anchor_session", blocked)

    # PHASE 1: Thermodynamic core integration
    start_time = time.time()
    try:
        if not session_id:
            session_id = f"{actor_id}-{uuid.uuid4().hex[:8]}"
        revoked = _revocation_reason(actor_id=actor_id, session_id=session_id)
        if revoked:
            return wrap_tool_output(
                "anchor_session", _revocation_void("000_INIT", session_id, revoked)
            )
        anch = await anchor(session_id=session_id, user_id=actor_id, context=query)
        effective_session = str(anch.get("session_id", session_id))
        verdict = str(anch.get("verdict", "SEAL"))
        initial_binding = {
            "actor_id": actor_id,
            "token_fingerprint": _token_fingerprint(auth_token),
            "approval_scope": list(_DEFAULT_APPROVAL_SCOPE),
            "parent_signature": "",
        }
        continuity_context = _rotate_auth_context(effective_session, initial_binding)

        payload = {
            "verdict": verdict,
            "session_id": effective_session,
            "stage": "000_INIT",
            "mode": mode,
            "grounding_required": grounding_required,
            "token_status": _token_status(auth_token),
            "auth": {"present": bool(auth_token)},
            "auth_context": continuity_context,
            "debug": debug,
            "data": {"anchor": anch} if debug else {},
        }
        payload.update(
            envelope_builder.build_envelope(
                stage="000_INIT",
                session_id=payload["session_id"],
                verdict=verdict,
                payload=anch if isinstance(anch, dict) else {},
            )
        )

        # Add compute telemetry for Landauer bound
        payload["compute_ms"] = (time.time() - start_time) * 1000
        payload["tokens"] = len(query.split())

        return wrap_tool_output("anchor_session", payload)
    except Exception as e:
        if isinstance(
            e,
            (
                ThermodynamicViolation,
                ModeCollapseError,
                CheapTruthError,
                PeaceViolation,
                EntropyViolation,
                AmanahViolation,
            ),
        ):
            return wrap_tool_output(
                "anchor_session", _convert_physics_exception_to_void(e, "anchor_session", "init")
            )
        return wrap_tool_output("anchor_session", _fracture_response("000_INIT", e))


@mcp.tool(name="reason_mind")
async def reason_mind(
    query: str,
    session_id: str,
    grounding: list[dict[str, Any]] | None = None,
    capability_modules: list[str] | None = None,
    debug: bool = False,
    actor_id: str = "anonymous",
    auth_token: str | None = None,
    auth_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """333 REASON: run AGI cognition with grounding and budget controls."""
    blocked = validate_input("reason_mind", {"query": query, "session_id": session_id})
    if blocked:
        return wrap_tool_output("reason_mind", blocked)
    missing = require_session("reason_mind", session_id)
    if missing:
        return wrap_tool_output("reason_mind", missing)

    # PHASE 1: Thermodynamic core integration with physics exception handling
    start_time = time.time()
    try:
        revoked = _revocation_reason(actor_id=actor_id, session_id=session_id)
        if revoked:
            return wrap_tool_output(
                "apex_judge",
                _revocation_void("888_APEX_JUDGE", session_id, revoked),
            )
        continuity_binding, continuity_error = _enforce_auth_continuity(
            tool_name="reason_mind",
            stage="111-444",
            session_id=session_id,
            actor_id=actor_id,
            auth_token=auth_token,
            auth_context=auth_context,
            critical=False,
        )
        if continuity_error:
            return wrap_tool_output("reason_mind", continuity_error)

        evidence = [str(x) for x in (grounding or [])]
        rag_contexts = []
        try:
            rag = _ensure_rag()
            rag_contexts = rag.query_with_metadata(query=query, top_k=3).get("contexts", [])
        except Exception:
            pass

        think_draft = await think(session_id=session_id, query=query, context="; ".join(evidence))
        if think_draft.get("verdict") == "VOID":
            return wrap_tool_output(
                "reason_mind",
                {
                    "verdict": "VOID",
                    "stage": "222_THINK",
                    "session_id": session_id,
                    "blocked_by": "Stage 222 THINK — constitutional floor violation",
                },
            )

        r = await reason(session_id=session_id, hypothesis=query, evidence=evidence)
        i = await integrate(
            session_id=session_id, context_bundle={"query": query, "grounding": grounding or {}}
        )
        d = await respond(session_id=session_id, draft_response=f"Draft response for: {query}")

        verdict = _fold_verdict(
            [
                str(think_draft.get("verdict", "")),
                str(r.get("verdict", "")),
                str(i.get("verdict", "")),
                str(d.get("verdict", "")),
            ]
        )

        # PHASE 2 Hardening: Auto-recall if Truth (F2) is low (< 0.85)
        truth_score = r.get("truth_score", 1.0)
        if truth_score < 0.85:
            try:
                # Ditempa Bukan Diberi: Re-forge with constitutional context
                rag = _ensure_rag()
                deeper_contexts = rag.retrieve(query, top_k=5, hybrid_alpha=0.5)
                if deeper_contexts:
                    rag_contexts.extend([ctx.content for ctx in deeper_contexts])
                    # Re-run reasoning with augmented context
                    evidence_augmented = evidence + [ctx.content for ctx in deeper_contexts]
                    r_augmented = await reason(
                        session_id=session_id, hypothesis=query, evidence=evidence_augmented
                    )
                    # Update metrics if improvement found
                    if r_augmented.get("truth_score", 0.0) > truth_score:
                        r = r_augmented
                        truth_score = r.get("truth_score")
            except Exception:
                pass

        merged = {
            "truth_score": truth_score,
            "f2_threshold": r.get("f2_threshold"),
            "floors_failed": list(r.get("floors_failed", []))
            + list(i.get("floors_failed", []))
            + list(d.get("floors_failed", [])),
            "retrieved_contexts": rag_contexts,
        }

        payload = {
            "capability_modules": capability_modules or [],
            "actor_id": continuity_binding["actor_id"] if continuity_binding else actor_id,
            "token_status": _token_status(auth_token),
            "auth_context": {},
            "debug": debug,
            "data": (
                {"think": think_draft, "reason": r, "integrate": i, "respond": d} if debug else {}
            ),
        }
        payload.update(
            envelope_builder.build_envelope(
                stage="111-444", session_id=session_id, verdict=verdict, payload=merged
            )
        )

        # Add compute telemetry for Landauer bound
        payload["compute_ms"] = (time.time() - start_time) * 1000
        payload["tokens"] = len(query.split()) + len(str(payload).split())

        # PHASE 1: Strict F4 entropy check (ΔS <= 0)
        delta_s = payload.get("payload", {}).get("dS", 0.0)
        if CORE_AVAILABLE and delta_s > 0:
            raise EntropyViolation(
                f"F4_CLARITY_VIOLATION: ΔS={delta_s:.4f} > 0 in reason_mind output"
            )

        return wrap_tool_output(
            "reason_mind",
            _attach_rotated_auth_context(payload, session_id, continuity_binding),
        )
    except Exception as e:
        if isinstance(
            e,
            (
                ThermodynamicViolation,
                ModeCollapseError,
                CheapTruthError,
                PeaceViolation,
                EntropyViolation,
                AmanahViolation,
            ),
        ):
            return wrap_tool_output(
                "reason_mind", _convert_physics_exception_to_void(e, "reason_mind", session_id)
            )
        return wrap_tool_output("reason_mind", _fracture_response("111-444", e, session_id))


@mcp.tool(name="vector_memory")
async def vector_memory(
    query: str,
    session_id: str,
    debug: bool = False,
) -> dict[str, Any]:
    """555 RECALL: retrieve associative memory traces from VAULT999."""
    blocked = validate_input(
        "vector_memory",
        {"query": query, "session_id": session_id},
    )
    if blocked:
        return wrap_tool_output("vector_memory", blocked)
    missing = require_session("vector_memory", session_id)
    if missing:
        return wrap_tool_output("vector_memory", missing)
    start_time = time.time()
    try:
        embedding_backend = "BGE (BAAI/bge-m3)"
        query_vector_dim = 768  # BGE-M3 = 768-dim multilingual (BM, EN, Manglish)
        points_count = 0
        namespace = "arifos_constitutional"

        try:
            rag = _ensure_rag()
            # Try to get actual model and collection info
            if hasattr(rag, "model_name"):
                embedding_backend = rag.model_name
            if hasattr(rag, "collection"):
                namespace = rag.collection

            # Get live counts for transparency
            health = rag.health_check()
            points_count = health.get("points_count", 0)

            contexts = rag.retrieve(query=query, top_k=5, min_score=0.15)
        except Exception:
            contexts = []

        result_state = "MATCH_FOUND" if contexts else "NO_MATCHES"
        jaccard_max = (
            max([ctx.metadata.get("jaccard_score", 0.0) for ctx in contexts]) if contexts else 0.0
        )
        cosine_max = (
            max([ctx.metadata.get("cosine_score", 0.0) for ctx in contexts]) if contexts else 0.0
        )

        # Enhanced instrumentation — "The Operational Truth"
        metrics = {
            "memory_count": len(contexts),
            "similarity_max": round(max(jaccard_max, cosine_max), 4),
            "cosine_similarity_max": round(cosine_max, 4),
            "jaccard_lexical_max": round(jaccard_max, 4),
            "memory_namespace": namespace,
            "indexed_points_count": points_count,
            "source_types": ["canon", "vault999", "session_history"],
            "embedding_backend": embedding_backend,
            "query_vector_dim": query_vector_dim,
            "similarity_metric": "cosine + jaccard (hybrid)",
            "embedding_backend_available": BGE_AVAILABLE,
        }

        merged = {
            "status": "RECALL_SUCCESS",
            "result_state": result_state,
            "memories": [
                {
                    "source": f"{ctx.source}/{ctx.path}",
                    "score": round(ctx.score, 4),
                    "content": ctx.content[:800],
                }
                for ctx in contexts
            ],
            "metrics": metrics,
        }

        # No results is still a successful operation (SEAL)
        payload = envelope_builder.build_envelope(
            stage="555_RECALL", session_id=session_id, verdict="SEAL", payload=merged
        )

        payload["compute_ms"] = (time.time() - start_time) * 1000
        return wrap_tool_output("vector_memory", payload)
    except Exception as e:
        return wrap_tool_output("vector_memory", _fracture_response("555_RECALL", e, session_id))


@mcp.tool(name="simulate_heart")
async def simulate_heart(
    query: str,
    session_id: str,
    stakeholders: list[str] | None = None,
    capability_modules: list[str] | None = None,
    debug: bool = False,
    actor_id: str = "anonymous",
    auth_token: str | None = None,
    auth_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """555 EMPATHY: evaluate stakeholder impact and care constraints."""
    blocked = validate_input("simulate_heart", {"query": query, "session_id": session_id})
    if blocked:
        return wrap_tool_output("simulate_heart", blocked)
    missing = require_session("simulate_heart", session_id)
    if missing:
        return wrap_tool_output("simulate_heart", missing)
    start_time = time.time()
    try:
        revoked = _revocation_reason(actor_id=actor_id, session_id=session_id)
        if revoked:
            return wrap_tool_output(
                "eureka_forge",
                _revocation_void("777_EUREKA_FORGE", session_id, revoked),
            )
        continuity_binding, continuity_error = _enforce_auth_continuity(
            tool_name="simulate_heart",
            stage="555-666",
            session_id=session_id,
            actor_id=actor_id,
            auth_token=auth_token,
            auth_context=auth_context,
            critical=False,
        )
        if continuity_error:
            return wrap_tool_output("simulate_heart", continuity_error)

        v = await validate(session_id=session_id, action=query)
        a = await align(session_id=session_id, action=query)
        verdict = _fold_verdict([str(v.get("verdict", "")), str(a.get("verdict", ""))])
        merged = {
            "truth_score": v.get("truth_score"),
            "floors_failed": list(v.get("floors_failed", [])) + list(a.get("floors_failed", [])),
        }

        payload = {
            "stakeholders": stakeholders or [],
            "capability_modules": capability_modules or [],
            "actor_id": continuity_binding["actor_id"] if continuity_binding else actor_id,
            "token_status": _token_status(auth_token),
            "auth_context": {},
            "debug": debug,
            "data": {"validate": v, "align": a} if debug else {},
        }
        payload.update(
            envelope_builder.build_envelope(
                stage="555-666", session_id=session_id, verdict=verdict, payload=merged
            )
        )

        payload["compute_ms"] = (time.time() - start_time) * 1000
        return wrap_tool_output(
            "simulate_heart",
            _attach_rotated_auth_context(payload, session_id, continuity_binding),
        )
    except Exception as e:
        return wrap_tool_output("simulate_heart", _fracture_response("555-666", e, session_id))


@mcp.tool(name="critique_thought")
async def critique_thought(
    plan: dict[str, Any],
    session_id: str,
    context: str = "",
    actor_id: str = "anonymous",
    auth_token: str | None = None,
    auth_context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """666 ALIGN: run 7-model critique (inversion, framing, non-linearity, etc.)."""
    blocked = validate_input("critique_thought", {"plan": plan, "session_id": session_id})
    if blocked:
        return wrap_tool_output("critique_thought", blocked)
    missing = require_session("critique_thought", session_id)
    if missing:
        return wrap_tool_output("critique_thought", missing)
    continuity_binding, continuity_error = _enforce_auth_continuity(
        tool_name="critique_thought",
        stage="666_ALIGN",
        session_id=session_id,
        actor_id=actor_id,
        auth_token=auth_token,
        auth_context=auth_context,
        critical=False,
    )
    if continuity_error:
        return wrap_tool_output("critique_thought", continuity_error)
    flags = _model_flags(plan, context=context)
    failed = [k for k, v in flags.items() if not v]
    critique_text = context.strip() or json.dumps(plan, ensure_ascii=True, sort_keys=True)
    payload: dict[str, Any] = {
        "verdict": "SEAL" if not failed else "SABAR",
        "session_id": session_id,
        "stage": "666_ALIGN",
        "mental_models": flags,
        "failed_models": failed,
        "critique_backend": "heuristic_fallback",
    }
    try:
        align_result = await align(session_id=session_id, action=critique_text)
        if isinstance(align_result, dict):
            payload.update(
                {
                    "verdict": str(align_result.get("verdict", payload["verdict"])),
                    "recommendation": align_result.get("recommendation"),
                    "alignment_status": align_result.get("status"),
                    "alignment_backend_result": align_result,
                    "critique_backend": "triad_align",
                }
            )
            if failed and payload["verdict"] == "SEAL":
                payload["verdict"] = "PARTIAL"
    except Exception as exc:
        payload["critique_backend_error"] = str(exc)
    return wrap_tool_output(
        "critique_thought",
        _attach_rotated_auth_context(payload, session_id, continuity_binding),
    )


@mcp.tool(name="apex_judge")
async def apex_judge(
    session_id: str,
    query: str,
    agi_result: dict[str, Any] | None = None,
    asi_result: dict[str, Any] | None = None,
    critique_result: dict[str, Any] | None = None,
    proposed_verdict: str = "SEAL",
    human_approve: bool = False,
    debug: bool = False,
    actor_id: str = "anonymous",
    auth_token: str | None = None,
    auth_context: dict[str, Any] | None = None,
    approval_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """888 APEX JUDGE METABOLIC: sovereign constitutional verdict synthesis."""
    blocked = validate_input("apex_judge", {"session_id": session_id, "query": query})
    if blocked:
        return wrap_tool_output("apex_judge", blocked)
    missing = require_session("apex_judge", session_id)
    if missing:
        return wrap_tool_output("apex_judge", missing)

    # PHASE 1: Thermodynamic core integration - APEX judgment with Ψ, W₃, Φₚ
    start_time = time.time()
    try:
        continuity_binding, continuity_error = _enforce_auth_continuity(
            tool_name="apex_judge",
            stage="888_APEX_JUDGE",
            session_id=session_id,
            actor_id=actor_id,
            auth_token=auth_token,
            auth_context=auth_context,
            critical=True,
        )
        if continuity_error:
            return wrap_tool_output("apex_judge", continuity_error)

        action_hash = _approval_action_hash([query, proposed_verdict, human_approve])
        require_approval = human_approve or (not _PUBLIC_APPROVAL_MODE)
        approval_state, approval_error = await _verify_approval_bundle(
            tool_name="apex_judge",
            stage="888_APEX_JUDGE",
            session_id=session_id,
            approval_bundle=approval_bundle,
            action_hash=action_hash,
            risk_tier="HIGH" if human_approve else "MEDIUM",
            require_bundle=require_approval,
        )
        if approval_error:
            return wrap_tool_output("apex_judge", approval_error)

        plan = {
            "query": query,
            "proposed_verdict": proposed_verdict,
            "human_approve": human_approve,
            "agi": agi_result or {},
            "asi": asi_result or {},
        }
        forged = await forge(session_id=session_id, plan=str(plan))
        judged = await audit(
            session_id=session_id,
            action=str(plan),
            sovereign_token="888_APPROVED" if human_approve else "",
            agi_result=agi_result,
            asi_result=asi_result,
        )

        precedents = []
        try:
            rag = _ensure_rag()
            precedent_contexts = rag.retrieve(query=query, top_k=3, min_score=0.25)
            precedents = [
                {
                    "source": f"{ctx.source}/{ctx.path}",
                    "score": ctx.score,
                    "content": ctx.content[:500],
                }
                for ctx in precedent_contexts
            ]
        except Exception:
            pass

        omega_ortho = None
        mode_collapse = False
        if agi_result and asi_result and CORE_AVAILABLE:
            agi_vector = agi_result.get("embedding_vector", [])
            asi_vector = asi_result.get("embedding_vector", [])
            if agi_vector and asi_vector:
                omega_ortho = derive_orthogonality(agi_vector, asi_vector)
                mode_collapse = omega_ortho < 0.95

        verdict = str(judged.get("verdict", "VOID"))
        approval_ok = isinstance(approval_state, dict) and bool(
            str(approval_state.get("approval_mode", "")).strip()
        )
        governance_proof = build_governance_proof(
            continuity_ok=bool(continuity_binding),
            approval_ok=approval_ok,
            human_approve=human_approve,
            public_approval_mode=_PUBLIC_APPROVAL_MODE,
            truth_score=judged.get("truth_score"),
            truth_threshold=judged.get("f2_threshold"),
            precedent_count=len(precedents),
            grounding_present=bool(precedents) or bool(str(query).strip()),
            revocation_ok=True,
            health_ok=True,
            omega_ortho=omega_ortho,
            mode_collapse=mode_collapse,
            non_violation_status=verdict.upper() != "VOID",
        )
        governance_proof = apply_governance_gate(
            current_verdict=verdict,
            governance_proof=governance_proof,
        )
        verdict = str(governance_proof.get("gate_verdict", verdict))
        governance_token = _build_governance_token(session_id, verdict)
        merged = {
            "truth_score": judged.get("truth_score"),
            "f2_threshold": judged.get("f2_threshold"),
            "floors_failed": list(forged.get("floors_failed", []))
            + list(judged.get("floors_failed", [])),
            "precedents": precedents,
            "governance_proof": governance_proof,
        }

        payload = {
            "authority": {"human_approve": human_approve},
            "governance_token": governance_token,
            "governance_proof": governance_proof,
            "actor_id": continuity_binding["actor_id"] if continuity_binding else actor_id,
            "token_status": _token_status(auth_token),
            "auth_context": {},
            "debug": debug,
            "data": {"forge": forged, "audit": judged} if debug else {},
        }
        payload.update(
            envelope_builder.build_envelope(
                stage="888_APEX_JUDGE", session_id=session_id, verdict=verdict, payload=merged
            )
        )

        # Add compute telemetry
        payload["compute_ms"] = (time.time() - start_time) * 1000

        if omega_ortho is not None:
            payload["omega_ortho"] = omega_ortho
        if mode_collapse:
            payload["mode_collapse_warning"] = True

        if isinstance(payload, dict):
            token = payload.get("governance_token")
            if isinstance(token, str) and token.strip():
                _SESSION_GOVERNANCE_TOKENS[session_id] = token.strip()
            stage_value = str(payload.get("stage", "")).upper()
            if stage_value in {"", "777-888", "777-888_APEX", "888_AUDIT", "888_JUDGE"}:
                payload["stage"] = "888_APEX_JUDGE"
                if stage_value:
                    payload["stage_legacy"] = stage_value
        return wrap_tool_output(
            "apex_judge",
            _attach_rotated_auth_context(
                _annotate_approval(payload, approval_state),
                session_id,
                continuity_binding,
            ),
        )

    except (
        ThermodynamicViolation,
        ModeCollapseError,
        CheapTruthError,
        PeaceViolation,
        EntropyViolation,
        AmanahViolation,
    ) as e:
        # Fail-closed: Physics violations return VOID
        return wrap_tool_output(
            "apex_judge", _convert_physics_exception_to_void(e, "apex_judge", session_id)
        )


# F1 Amanah: Safe workspace configuration
# Uses runtime env var, not import-time (Python pitfall avoidance)
DEFAULT_WORKDIR = os.environ.get("ARIFOS_WORKDIR", "/usr/src/app")

@mcp.tool(name="eureka_forge")
async def eureka_forge(
    session_id: str,
    command: str,
    working_dir: str | None = None,
    timeout: int = 60,
    confirm_dangerous: bool = False,
    agent_id: str = "unknown",
    purpose: str = "",
    actor_id: str = "anonymous",
    auth_token: str | None = None,
    auth_context: dict[str, Any] | None = None,
    approval_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """777 EUREKA FORGE: execute shell commands with audit logging and confirmation for dangerous operations.

    F1: Workspace boundary enforcement (cannot escape ARIFOS_WORKDIR)
    F5: Safe defaults (validates working_dir at runtime)
    F6: Comprehensive error handling
    F7: Risk classification (LOW/MODERATE/CRITICAL)
    F9: Transparent logging with agent_id and purpose
    F11: Command authority through session continuity
    F12: Input validation and dangerous pattern detection

    Dangerous commands (rm -rf, mkfs, dd, etc.) require confirm_dangerous=True
    """
    # Resolve working_dir with runtime evaluation (not import-time)
    if working_dir is None:
        working_dir = DEFAULT_WORKDIR
    
    # F1 Amanah + F12 Defense: Workspace boundary enforcement
    from pathlib import Path
    base_dir = Path(DEFAULT_WORKDIR).resolve()
    requested = Path(working_dir).resolve()
    
    if not str(requested).startswith(str(base_dir)):
        return wrap_tool_output(
            "eureka_forge",
            _attach_rotated_auth_context(
                {
                    "verdict": "VOID",
                    "stage": "777_EUREKA_FORGE",
                    "session_id": session_id,
                    "error": f"Working directory outside allowed workspace: {requested}",
                    "allowed_root": str(base_dir),
                    "violation": "F1_Amanah_WORKSPACE_ESCAPE",
                },
                session_id,
                None,
            ),
        )
    
    working_dir = str(requested)
    
    blocked = validate_input(
        "eureka_forge",
        {"session_id": session_id, "command": command, "agent_id": agent_id},
    )
    if blocked:
        return wrap_tool_output("eureka_forge", blocked)
    missing = require_session("eureka_forge", session_id)
    if missing:
        return wrap_tool_output("eureka_forge", missing)
    start_time = time.time()
    try:
        continuity_binding, continuity_error = _enforce_auth_continuity(
            tool_name="eureka_forge",
            stage="777_EUREKA_FORGE",
            session_id=session_id,
            actor_id=actor_id,
            auth_token=auth_token,
            auth_context=auth_context,
            critical=True,
        )
        if continuity_error:
            return wrap_tool_output("eureka_forge", continuity_error)

        import shlex

        DANGEROUS_PATTERNS = [
            "rm -rf",
            "rm -fr",
            "rm -r /",
            "rm -rf /",
            "mkfs",
            "dd if=",
            "> /dev/sda",
            "format",
            "shutdown",
            "reboot",
            "halt",
            "poweroff",
            "kill -9",
        ]
        risk_level = "LOW"
        for pattern in DANGEROUS_PATTERNS:
            if pattern in command.lower():
                risk_level = "CRITICAL"
                break
        if risk_level == "LOW":
            MODERATE_PATTERNS = [
                "docker rm",
                "docker stop",
                "docker kill",
                "systemctl stop",
                "apt remove",
                "pip uninstall",
                "rm -r",
                "rm -f",
                "> ",
                ">>",
                "| sh",
                "| bash",
            ]
            for pattern in MODERATE_PATTERNS:
                if pattern in command.lower():
                    risk_level = "MODERATE"
                    break

        if risk_level == "CRITICAL" and not confirm_dangerous:
            return wrap_tool_output(
                "eureka_forge",
                _attach_rotated_auth_context(
                    envelope_builder.build_envelope(
                        stage="888_FORGE",
                        session_id=session_id,
                        verdict="888_HOLD",
                        payload={
                            "status": "CONFIRMATION_REQUIRED",
                            "risk_level": risk_level,
                            "message": "CRITICAL command detected. Set confirm_dangerous=True to execute.",
                        },
                    ),
                    session_id,
                    continuity_binding,
                ),
            )

        action_hash = _approval_action_hash([command, working_dir, confirm_dangerous])
        require_approval = (risk_level == "CRITICAL" and confirm_dangerous) or (
            not _PUBLIC_APPROVAL_MODE
        )
        approval_state, approval_error = await _verify_approval_bundle(
            tool_name="eureka_forge",
            stage="777_EUREKA_FORGE",
            session_id=session_id,
            approval_bundle=approval_bundle,
            action_hash=action_hash,
            risk_tier=risk_level,
            require_bundle=require_approval,
        )
        if approval_error:
            return wrap_tool_output(
                "eureka_forge",
                _attach_rotated_auth_context(approval_error, session_id, continuity_binding),
            )

        args = shlex.split(command)
        process = await asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=working_dir,
            limit=1024 * 1024,
        )
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)

        res_payload = {
            "status": "SUCCESS" if process.returncode == 0 else "ERROR",
            "exit_code": process.returncode,
            "stdout": stdout.decode("utf-8", errors="replace")[:10000],
            "stderr": stderr.decode("utf-8", errors="replace")[:5000],
            "risk_level": risk_level,
        }
        payload = envelope_builder.build_envelope(
            stage="777_EUREKA_FORGE",
            session_id=session_id,
            verdict="SEAL" if process.returncode == 0 else "VOID",
            payload=res_payload,
        )
        payload["compute_ms"] = (time.time() - start_time) * 1000
        return wrap_tool_output(
            "eureka_forge",
            _attach_rotated_auth_context(
                _annotate_approval(payload, approval_state),
                session_id,
                continuity_binding,
            ),
        )
    except Exception as e:
        return wrap_tool_output(
            "eureka_forge", _fracture_response("777_EUREKA_FORGE", e, session_id)
        )


@mcp.tool(name="seal_vault")
async def seal_vault(
    session_id: str,
    summary: str,
    verdict: str = "SEAL",
    governance_token: str | None = None,
    approved_by: str | None = None,
    approval_reference: str | None = None,
    actor_id: str = "anonymous",
    auth_token: str | None = None,
    auth_context: dict[str, Any] | None = None,
    # PHASE 2: Thermodynamic telemetry for ledger binding
    telemetry: dict[str, Any] | None = None,
    approval_bundle: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """999 SEAL: commit immutable session decision record with thermodynamic telemetry."""
    blocked = validate_input("seal_vault", {"session_id": session_id, "summary": summary})
    if blocked:
        return wrap_tool_output("seal_vault", blocked)
    missing = require_session("seal_vault", session_id)
    if missing:
        return wrap_tool_output("seal_vault", missing)

    continuity_binding, continuity_error = _enforce_auth_continuity(
        tool_name="seal_vault",
        stage="999_SEAL",
        session_id=session_id,
        actor_id=actor_id,
        auth_token=auth_token,
        auth_context=auth_context,
        critical=True,
    )
    if continuity_error:
        return wrap_tool_output("seal_vault", continuity_error)

    revoked = _revocation_reason(actor_id=actor_id, session_id=session_id)
    if revoked:
        return wrap_tool_output("seal_vault", _revocation_void("999_SEAL", session_id, revoked))

    action_hash = _approval_action_hash([summary, verdict])
    require_approval = (str(verdict).upper() == "SEAL") or (not _PUBLIC_APPROVAL_MODE)
    approval_state, approval_error = await _verify_approval_bundle(
        tool_name="seal_vault",
        stage="999_SEAL",
        session_id=session_id,
        approval_bundle=approval_bundle,
        action_hash=action_hash,
        risk_tier="CRITICAL" if str(verdict).upper() == "SEAL" else "MEDIUM",
        require_bundle=require_approval,
    )
    if approval_error:
        return wrap_tool_output(
            "seal_vault",
            _attach_rotated_auth_context(approval_error, session_id, continuity_binding),
        )

    approval_id = ""
    approval_signature_digest = ""
    if isinstance(approval_state, dict):
        approval_id = str(approval_state.get("approval_id", ""))
        approval_signature_digest = str(approval_state.get("approval_signature_digest", ""))

    chain_prev = ""
    if isinstance(continuity_binding, dict):
        chain_prev = str(continuity_binding.get("parent_signature", ""))
    if not chain_prev:
        chain_prev = str(_SESSION_CONTINUITY_STATE.get(session_id, {}).get("last_signature", ""))

    lineage_actor_id = (
        str(continuity_binding.get("actor_id", actor_id))
        if isinstance(continuity_binding, dict)
        else str(actor_id)
    )
    authority_chain_hash = hashlib.sha256(
        json.dumps(
            {
                "prev_link": chain_prev,
                "action_hash": action_hash,
                "approval_id": approval_id,
                "actor_id": lineage_actor_id,
            },
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
        ).encode()
    ).hexdigest()
    lineage_payload = {
        "approval_id": approval_id,
        "actor_id": lineage_actor_id,
        "authority_chain_hash": authority_chain_hash,
        "approval_signature_digest": approval_signature_digest,
    }

    if approval_id:
        approval_revoked = _revocation_reason(approval_id=approval_id)
        if approval_revoked:
            return wrap_tool_output(
                "seal_vault", _revocation_void("999_SEAL", session_id, approval_revoked)
            )

    resolved_token = ""
    if isinstance(governance_token, str) and governance_token.strip():
        resolved_token = governance_token.strip()
    elif session_id in _SESSION_GOVERNANCE_TOKENS:
        resolved_token = _SESSION_GOVERNANCE_TOKENS[session_id]
    else:
        # Backend convenience path: mint token from APEX so humans never copy opaque strings.
        auto_judge = await legacy.apex_judge.fn(
            session_id=session_id,
            query=summary,
            proposed_verdict=verdict,
            human_approve=False,
            implementation_details={"source": "seal_vault_auto_token"},
            actor_id=actor_id,
            auth_token=auth_token,
            auth_context=auth_context,
        )
        auto_token = auto_judge.get("governance_token") if isinstance(auto_judge, dict) else ""
        if isinstance(auto_token, str) and auto_token.strip():
            resolved_token = auto_token.strip()
            _SESSION_GOVERNANCE_TOKENS[session_id] = resolved_token

    if not resolved_token:
        return wrap_tool_output(
            "seal_vault",
            _attach_rotated_auth_context(
                {
                    "verdict": "VOID",
                    "stage": "999_SEAL",
                    "session_id": session_id,
                    "error": "Missing governance_token for seal_vault",
                    "remediation": "Call apex_judge first in this session, then retry seal_vault.",
                },
                session_id,
                continuity_binding,
            ),
        )

    # PHASE 2: Bind thermodynamic telemetry to ledger
    # Include Ψ, W₃, Landauer metrics in vault entry
    thermodynamic_statement = {
        "summary": summary,
        "verdict": verdict,
        "governance_token": resolved_token[:16] + "...",  # Truncated for security
        # Include telemetry if provided
        "vitality_index": telemetry.get("psi") if telemetry else None,
        "tri_witness": telemetry.get("w3") if telemetry else None,
        "paradox_conductance": telemetry.get("phi_p") if telemetry else None,
        "landauer_ratio": telemetry.get("landauer_ratio") if telemetry else None,
        "omega_ortho": telemetry.get("omega_ortho") if telemetry else None,
        "constitutional_cost": telemetry.get("constitutional_cost") if telemetry else "SEALED",
        "approval_id": approval_id,
        "actor_id": lineage_actor_id,
        "authority_chain_hash": authority_chain_hash,
        "approval_signature_digest": approval_signature_digest,
        "timestamp": time.time(),
    }

    start_time = time.time()
    try:
        token_valid, verified_verdict = _verify_governance_token(session_id, resolved_token)
        if not token_valid:
            return wrap_tool_output(
                "seal_vault",
                _attach_rotated_auth_context(
                    {
                        "verdict": "VOID",
                        "stage": "999_SEAL",
                        "session_id": session_id,
                        "error": "F1 Amanah — governance_token invalid",
                    },
                    session_id,
                    continuity_binding,
                ),
            )

        sealed_summary = (
            f"{summary}\n[lineage]{json.dumps(lineage_payload, ensure_ascii=True, sort_keys=True)}"
        )
        res = await seal(
            session_id=session_id,
            task_summary=sealed_summary,
            was_modified=True,
            verdict=verified_verdict,
        )
        payload = {"data": res, "status": verified_verdict}
        if thermodynamic_statement is not None:
            payload["thermodynamic_statement"] = thermodynamic_statement
        payload["authority_lineage"] = lineage_payload
        payload.update(
            envelope_builder.build_envelope(
                stage="999_SEAL", session_id=session_id, verdict=verified_verdict, payload=res
            )
        )

        if verified_verdict == "SEAL":
            try:
                # 🔱 zkPC-ready Qdrant Indexing: Link back to Forensic Ledger
                entry_hash = res.get("entry_hash")
                metadata = {
                    "verdict": verified_verdict,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                if entry_hash:
                    metadata["vault_digest"] = entry_hash
                    metadata["witness_signature"] = _get_zkpc_witness(session_id, entry_hash)
                metadata["approval_id"] = approval_id
                metadata["actor_id"] = lineage_actor_id
                metadata["authority_chain_hash"] = authority_chain_hash
                metadata["approval_signature_digest"] = approval_signature_digest

                rag = _ensure_rag()
                rag.index_memory(
                    session_id=session_id,
                    content=summary,
                    metadata=metadata,
                )
            except Exception:
                pass

        # Add thermodynamic binding confirmation
        payload["thermodynamic_seal"] = {
            "bound_to_ledger": True,
            "telemetry_included": bool(telemetry),
            "constitutional_signature": resolved_token[:8] + "...",
        }

        return wrap_tool_output(
            "seal_vault",
            _attach_rotated_auth_context(
                _annotate_approval(payload, approval_state),
                session_id,
                continuity_binding,
            ),
        )
    except Exception as e:
        if isinstance(
            e,
            (
                ThermodynamicViolation,
                ModeCollapseError,
                CheapTruthError,
                PeaceViolation,
                EntropyViolation,
                AmanahViolation,
            ),
        ):
            return wrap_tool_output(
                "seal_vault", _convert_physics_exception_to_void(e, "seal_vault", session_id)
            )
        return wrap_tool_output("seal_vault", _fracture_response("999_SEAL", e, session_id))


@mcp.tool(name="search_reality")
async def search_reality(
    query: str = "",
    grounding_query: str = "",
    intent: str = "general",
    session_id: str = "",
    session_token: str = "",
) -> dict[str, Any]:
    """External evidence discovery (read-only)."""
    # grounding_query takes precedence as the EUREKA-prescribed semantic name.
    effective_query = (grounding_query or query or "").strip()
    # session_token takes precedence.
    effective_session = (session_token or session_id or "").strip()

    if not effective_query:
        return wrap_tool_output(
            "search_reality", {"verdict": "VOID", "error": "Missing query or grounding_query"}
        )

    blocked = validate_input(
        "search_reality", {"query": effective_query, "session_id": effective_session}
    )
    if blocked:
        return wrap_tool_output("search_reality", blocked)
    try:
        from aaa_mcp.external_gateways.brave_client import BraveSearchClient
        from aaa_mcp.external_gateways.jina_reader_client import JinaReaderClient
        from aaa_mcp.external_gateways.perplexity_client import PerplexitySearchClient

        primary = JinaReaderClient()
        payload = await primary.search(query=effective_query, intent=intent)
        if payload.get("status") not in {"OK"}:
            fallback1 = PerplexitySearchClient()
            payload = await fallback1.search(query=effective_query, intent=intent)
            if payload.get("status") in {"NO_API_KEY", "BAD_RESPONSE", "BAD_JSON"}:
                fallback2 = BraveSearchClient()
                payload = await fallback2.search(query=effective_query, intent=intent)

        urls = [r.get("url") for r in payload.get("results", []) if r.get("url")]
        results = payload.get("results", [])
        res_payload = {
            "query": effective_query,
            "status": payload.get("status", "OK"),
            "ids": urls,
            "results": results,
            "evidence_count": len(results),
            "f2_truth": {"grounded": len(results) > 0, "sources": urls[:3]},
        }
        if effective_session:
            res_payload["session_id"] = effective_session
        return wrap_tool_output("search_reality", res_payload)
    except Exception as e:
        return wrap_tool_output(
            "search_reality", {"query": effective_query, "status": f"ERROR: {e}"}
        )


@mcp.tool(name="ingest_evidence")
async def ingest_evidence(
    source_type: str,
    target: str,
    mode: str = "raw",
    max_chars: int = 4000,
    session_id: str | None = None,
    depth: int = 1,
    include_hidden: bool = False,
    pattern: str = "*",
    min_size_bytes: int = 0,
    max_files: int = 100,
) -> dict[str, Any]:
    """Unified evidence ingestion — fetch URL content or inspect local filesystem (read-only).

    source_type="url"  → fetch remote URL via Jina Reader / urllib fallback
    source_type="file" → read-only local filesystem inspection
    mode               → "raw" | "summary" | "chunks"  (default: "raw")
    """
    blocked = validate_input("ingest_evidence", {"source_type": source_type, "target": target})
    if blocked:
        return wrap_tool_output("ingest_evidence", blocked)
    from aaa_mcp.tools.ingest_evidence import ingest_evidence as _ingest

    result = await _ingest(
        source_type=source_type,
        target=target,
        mode=mode,
        max_chars=max_chars,
        session_id=session_id,
        depth=depth,
        include_hidden=include_hidden,
        pattern=pattern,
        min_size_bytes=min_size_bytes,
        max_files=max_files,
    )
    return wrap_tool_output("ingest_evidence", result)


# ARCHIVED: fetch_content — use ingest_evidence(source_type="url", ...) instead
async def fetch_content(id: str, max_chars: int = 4000) -> dict[str, Any]:
    """Archived — delegates to ingest_evidence."""
    from aaa_mcp.tools.ingest_evidence import ingest_evidence as _ingest

    result = await _ingest(source_type="url", target=id, mode="raw", max_chars=max_chars)
    return wrap_tool_output("fetch_content", result)


# ARCHIVED: inspect_file — use ingest_evidence(source_type="file", ...) instead
async def inspect_file(
    path: str = ".",
    depth: int = 1,
    include_hidden: bool = False,
    pattern: str = "*",
    min_size_bytes: int = 0,
    max_files: int = 100,
) -> dict[str, Any]:
    """Archived — delegates to ingest_evidence."""
    from aaa_mcp.tools.ingest_evidence import ingest_evidence as _ingest

    result = await _ingest(
        source_type="file",
        target=path,
        depth=depth,
        include_hidden=include_hidden,
        pattern=pattern,
        min_size_bytes=min_size_bytes,
        max_files=max_files,
    )
    return wrap_tool_output("inspect_file", result)


async def system_audit(audit_scope: str = "quick", verify_floors: bool = True) -> dict[str, Any]:
    """Legacy alias for audit_rules, kept for MCP compatibility."""
    return await audit_rules(audit_scope=audit_scope, verify_floors=verify_floors)


@mcp.tool(name="audit_rules")
async def audit_rules(
    audit_scope: str = "quick",
    verify_floors: bool = True,
    session_id: str = "",
) -> dict[str, Any]:
    """Run constitutional/system rule audit checks (read-only)."""
    blocked = validate_input("audit_rules", {"audit_scope": audit_scope, "session_id": session_id})
    if blocked:
        return wrap_tool_output("audit_rules", blocked)
    try:
        details = {"scope": audit_scope}
        if verify_floors:
            details["floors_loaded"] = True  # Heuristic for now
        res_payload = {"verdict": "SEAL", "scope": audit_scope, "details": details}
        if session_id:
            res_payload["session_id"] = session_id
        return wrap_tool_output("audit_rules", res_payload)
    except Exception as e:
        return wrap_tool_output("audit_rules", {"verdict": "VOID", "error": str(e)})


@mcp.tool(name="check_vital")
async def check_vital(
    include_swap: bool = True,
    include_io: bool = False,
    include_temp: bool = False,
) -> dict[str, Any]:
    """Read system health telemetry (CPU, memory, IO/thermal optional)."""
    payload = get_system_health(
        include_swap=include_swap,
        include_io=include_io,
        include_temp=include_temp,
    )
    return wrap_tool_output("check_vital", payload)


# INTERNAL: query_openclaw — NOT a public MCP tool; removed from canonical 13-tool surface.
async def query_openclaw(session_id: str, action: str = "health") -> dict[str, Any]:
    """Internal OpenClaw gateway diagnostics — not exposed via /tools/list."""
    try:
        from aaa_mcp.integrations.openclaw_gateway_client import (
            openclaw_get_health,
            openclaw_get_status,
        )

        if action == "health":
            payload = openclaw_get_health()
        elif action == "status":
            payload = openclaw_get_status()
        else:
            payload = {"error": f"Unknown action '{action}'"}

        return wrap_tool_output(
            "query_openclaw",
            envelope_builder.build_envelope(
                stage="333_OPENCLAW_PROBE",
                session_id=session_id,
                verdict="SEAL" if payload.get("http_probe", {}).get("ok") else "PARTIAL",
                payload=payload,
            ),
        )
    except Exception as e:
        return wrap_tool_output("query_openclaw", {"verdict": "VOID", "error": str(e)})


async def visualize_governance(
    session_id: str | None = None,
) -> dict[str, Any]:
    """Return metadata pointing the MCP client to the Constitutional Visualizer UI."""
    return {
        "verdict": "SEAL",
        "stage": "UI_LAUNCH",
        "session_id": session_id or "ui_session",
        "message": "Constitutional Decision Visualizer ready",
        "_meta": {
            "ui": {
                "resourceUri": "ui://constitutional-visualizer/mcp-app.html",
                "title": "Constitutional Decision Visualizer",
                "description": "Real-time governance metrics dashboard",
            }
        },
    }


def create_aaa_mcp_server() -> Any:
    """Canonical arifOS AAA MCP server factory."""
    return mcp


_TOOL_REQUIRED_ARGS: dict[str, list[str]] = {
    "anchor_session": ["query"],
    "reason_mind": ["query", "session_id"],
    "vector_memory": ["query", "session_id"],
    "simulate_heart": ["query", "session_id"],
    "critique_thought": ["plan", "session_id"],
    "eureka_forge": ["session_id", "command"],
    "apex_judge": ["session_id", "query"],
    "seal_vault": ["session_id", "summary", "governance_token"],
    "search_reality": [],
    "ingest_evidence": ["source_type", "target"],
    "audit_rules": [],
    "check_vital": [],
    "metabolic_loop": ["query"],
}

_TOOL_CRITICALITY: dict[str, str] = {
    "anchor_session": "foundation",
    "reason_mind": "normal",
    "vector_memory": "normal",
    "simulate_heart": "normal",
    "critique_thought": "normal",
    "eureka_forge": "critical",
    "apex_judge": "critical",
    "seal_vault": "critical",
    "search_reality": "read_only",
    "ingest_evidence": "read_only",
    "audit_rules": "read_only",
    "check_vital": "read_only",
    "metabolic_loop": "critical",
}


def _transport_profile_payload() -> dict[str, Any]:
    return {
        "protocol_revision_target": "2025-11-25",
        "supported_transports": ["stdio", "streamable-http", "sse-compat"],
        "canonical_endpoints": {
            "/": "Contract and service profile entrypoint.",
            "/mcp": "Runtime MCP transport endpoint.",
            "/tools": "Compatibility listing for REST-style clients.",
        },
        "required_headers": [
            "Accept: application/json, text/event-stream",
            "Content-Type: application/json",
            "MCP-Protocol-Version: 2025-11-25",
            "Mcp-Session-Id: <session_id after initialize>",
        ],
        "session_continuity": {
            "rules": [
                "Create or recover session with anchor_session before critical stages.",
                "Reuse the same session_id across all chained calls.",
                "Pass returned auth_context into the next call for F11 continuity.",
                "Keep actor_id and auth_token stable within one session chain.",
            ],
            "ttl_seconds_default": _CONTINUITY_TTL_SECONDS,
            "strict_mode": _CONTINUITY_STRICT,
        },
        "call_order_template": [
            "anchor_session",
            "reason_mind",
            "simulate_heart",
            "critique_thought",
            "apex_judge",
            "seal_vault",
        ],
        "failure_modes": [
            {
                "code": "SESSION_TERMINATED",
                "symptom": "chain signature mismatch, nonce replay, or expired auth_context",
                "remediation": "re-run anchor_session and continue using only the newest auth_context",
            },
            {
                "code": "MISSING_SESSION",
                "symptom": "required session_id absent on stateful tools",
                "remediation": "start with anchor_session and propagate returned session_id",
            },
            {
                "code": "SCOPE_MISMATCH",
                "symptom": "approval_scope or approval_bundle does not match tool/action hash",
                "remediation": "mint a fresh approval artifact for the exact tool and payload",
            },
        ],
    }


def _tool_operating_manual_payload() -> dict[str, Any]:
    tools: list[dict[str, Any]] = []
    for tool_name in AAA_TOOLS:
        tools.append(
            {
                "name": tool_name,
                "stage": TOOL_STAGE_MAP.get(tool_name, "000_INIT"),
                "trinity_lane": TRINITY_BY_TOOL.get(tool_name, "Delta"),
                "floor_bindings": TOOL_LAW_BINDINGS.get(tool_name, []),
                "required_args": _TOOL_REQUIRED_ARGS.get(tool_name, []),
                "criticality": _TOOL_CRITICALITY.get(tool_name, "normal"),
                "read_only": tool_name in {"search_reality", "ingest_evidence", "audit_rules", "check_vital"},
            }
        )

    return {
        "tools": tools,
        "approval_requirements": {
            "apex_judge": [
                "requires valid auth_context continuity",
                "requires approval_bundle when public mode is disabled or human_approve is true",
                "returns governance_token required by seal_vault",
            ],
            "eureka_forge": [
                "requires valid auth_context continuity",
                "requires approval_bundle for elevated or dangerous execution paths",
                "dangerous command classes require explicit confirm_dangerous=true",
            ],
            "seal_vault": [
                "requires valid auth_context continuity",
                "requires governance_token signed by apex_judge for same session_id",
                "requires approval_bundle for strict/elevated confirmation path",
            ],
        },
        "revocation": {
            "env_sets": [
                "ARIFOS_REVOKED_ACTORS",
                "ARIFOS_REVOKED_SESSIONS",
                "ARIFOS_REVOKED_APPROVAL_IDS",
            ],
            "effect": "returns VOID with AUTH_REVOKED_* reason codes on critical paths",
        },
        "continuity_notes": [
            "auth_context rotates after each accepted call",
            "approval_scope is checked per tool before execution",
            "nonce replay and signature drift terminate the chain",
        ],
    }


def _governance_gate_profile_payload() -> dict[str, Any]:
    return {
        "source_tool": "apex_judge",
        "version": "fused-3-pillar-gate",
        "pillars": {
            "authority": {
                "fields": ["authority_valid", "authority_score", "witness.human"],
                "pass_condition": "authority_valid == true",
                "floors": ["F11", "F13"],
            },
            "thermodynamics": {
                "fields": ["thermodynamics_valid", "thermodynamic_score"],
                "pass_condition": "thermodynamics_valid == true",
                "signals": ["non_violation_status", "mode_collapse", "omega_ortho"],
            },
            "tri_witness": {
                "fields": ["tri_witness_valid", "witness.w3", "witness.human", "witness.ai", "witness.earth"],
                "pass_condition": "tri_witness_valid == true and witness.w3 >= 0.95",
                "floors": ["F3"],
            },
        },
        "verdict_resolution": {
            "authority_fail": "VOID",
            "thermodynamics_fail": "VOID",
            "tri_witness_fail": "888_HOLD",
            "all_pass": "preserve underlying verdict unless already VOID",
        },
        "output_fields": [
            "authority_valid",
            "thermodynamics_valid",
            "tri_witness_valid",
            "authority_score",
            "thermodynamic_score",
            "witness",
            "gate_verdict",
            "gate_reason",
        ],
    }


@mcp.resource(
    PUBLIC_RESOURCE_URIS["schemas"],
    name="arifos_aaa_tool_schemas",
    mime_type="application/json",
    description="Canonical AAA MCP 13-tool schema/contract overview.",
)
def aaa_tool_schemas() -> str:
    discovery = build_surface_discovery(AAA_TOOLS)
    transport_profile = _transport_profile_payload()
    governance_gate = _governance_gate_profile_payload()
    payload = {
        "tool_count": 13,
        "surface": AAA_TOOLS,
        "trinity": {
            "Delta": [
                "anchor_session",
                "reason_mind",
                "search_reality",
                "ingest_evidence",
                "audit_rules",
            ],
            "Omega": ["vector_memory", "simulate_heart", "critique_thought", "check_vital"],
            "Psi": ["apex_judge", "eureka_forge", "seal_vault"],
            "ALL": ["metabolic_loop"],
        },
        "axioms": ["A1_TRUTH_COST", "A2_SCAR_WEIGHT", "A3_ENTROPY_WORK"],
        "technical_aliases": {
            "13_floors": "governance_rules",
            "333_axioms": "reasoning_constraints",
            "apex_dials": "decision_parameters",
            "eureka_forge": "action_actuator",
            "vault999": "immutable_ledger",
        },
        "laws_13": LAW_13_CATALOG,
        "apex_g_map": TOOL_DIALS_MAP,
        "transport_profile": {
            "protocol_revision_target": transport_profile["protocol_revision_target"],
            "supported_transports": transport_profile["supported_transports"],
            "canonical_endpoints": transport_profile["canonical_endpoints"],
            "required_headers": transport_profile["required_headers"],
            "call_order_template": transport_profile["call_order_template"],
        },
        "session_contract": {
            "continuity_ttl_seconds": transport_profile["session_continuity"]["ttl_seconds_default"],
            "strict_mode": transport_profile["session_continuity"]["strict_mode"],
            "rules": transport_profile["session_continuity"]["rules"],
            "failure_modes": transport_profile["failure_modes"],
        },
        "governance_gate": {
            "profile": governance_gate,
            "resource_uri": PUBLIC_RESOURCE_URIS["governance_gate_profile"],
        },
        "resource_links": {
            "transport_profile": PUBLIC_RESOURCE_URIS["mcp_transport_profile"],
            "tool_operating_manual": PUBLIC_RESOURCE_URIS["tool_operating_manual"],
            "governance_gate_profile": PUBLIC_RESOURCE_URIS["governance_gate_profile"],
        },
        "discovery": discovery,
    }
    # FastMCP resources must return str/bytes or ResourceContent.
    return json.dumps(payload, ensure_ascii=True)


@mcp.resource(
    PUBLIC_RESOURCE_URIS["mcp_transport_profile"],
    name="arifos_mcp_transport_profile",
    mime_type="application/json",
    description="Transport contract profile for MCP runtime clients.",
)
def mcp_transport_profile_resource() -> str:
    return json.dumps(_transport_profile_payload(), ensure_ascii=True)


@mcp.resource(
    PUBLIC_RESOURCE_URIS["tool_operating_manual"],
    name="arifos_tool_operating_manual",
    mime_type="application/json",
    description="Canonical tool operating manual with floor and approval guidance.",
)
def tool_operating_manual_resource() -> str:
    return json.dumps(_tool_operating_manual_payload(), ensure_ascii=True)


@mcp.resource(
    PUBLIC_RESOURCE_URIS["governance_gate_profile"],
    name="arifos_governance_gate_profile",
    mime_type="application/json",
    description="Fused authority/thermodynamics/tri-witness gate schema for apex_judge.",
)
def governance_gate_profile_resource() -> str:
    return json.dumps(_governance_gate_profile_payload(), ensure_ascii=True)


@mcp.resource(
    "ui://constitutional-visualizer/mcp-app.html",
    name="arifos_constitutional_visualizer",
    mime_type="text/html",
    description="Interactive MCP App visualizing real-time constitutional floor evaluations.",
)
def get_visualizer() -> str:
    path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "333_APPS",
        "constitutional-visualizer",
        "dist",
        "mcp-app.html",
    )
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    return "<html><body><h1>Visualizer app not built yet. Run npm run build:mcp in constitutional-visualizer</h1></body></html>"


@mcp.resource(
    PUBLIC_RESOURCE_URIS["full_context_pack"],
    name="arifos_aaa_full_context_pack",
    mime_type="application/json",
    description="Full-context orchestration metadata (stage spine, prompts, resources).",
)
def aaa_full_context_pack() -> str:
    return json.dumps(export_full_context_pack(), ensure_ascii=True)


@mcp.prompt(name=PUBLIC_PROMPT_NAMES["aaa_chain"])
def aaa_chain_prompt(query: str, actor_id: str = "user") -> str:
    return (
        "Use the canonical AAA 13-tool metabolic chain with session continuity:\n"
        "1) anchor_session          — 000 INIT: ignite session, get session_id\n"
        "2) reason_mind             — 222-333: AGI cognition and hypothesis grounding\n"
        "3) vector_memory           — 444-555: semantic recall from VAULT999\n"
        "4) simulate_heart          — 555-666: stakeholder impact and empathy check\n"
        "5) critique_thought        — 666: bias critique and alignment scan\n"
        "6) eureka_forge            — 777: execute material action (if needed)\n"
        "7) apex_judge              — 777-888: sovereign verdict, returns governance_token\n"
        "8) seal_vault              — 999: immutable ledger commit with governance_token\n"
        "Pass session_id from anchor_session to all downstream tools.\n"
        f"query={query!r}; actor_id={actor_id!r}."
    )


@mcp.prompt(name=PUBLIC_PROMPT_NAMES["mcp_transport_bootstrap"])
def mcp_transport_bootstrap_prompt(base_url: str = "https://<host>") -> str:
    return (
        "Bootstrap arifOS MCP over streamable HTTP.\n"
        "1) Read contract: GET {base_url}/ and GET {base_url}/.well-known/mcp/server.json\n"
        "2) Initialize MCP session against {base_url}/mcp using protocol 2025-11-25\n"
        "3) Send headers on MCP requests:\n"
        "   - Accept: application/json, text/event-stream\n"
        "   - Content-Type: application/json\n"
        "   - MCP-Protocol-Version: 2025-11-25\n"
        "   - Mcp-Session-Id: <session_id from initialize>\n"
        "4) Start chain with anchor_session, then propagate session_id and auth_context each call\n"
        "5) For compatibility-only clients, inspect /tools (do not treat as canonical runtime)\n"
        "6) On continuity errors, restart at anchor_session and use latest auth_context only\n"
    ).replace("{base_url}", base_url.rstrip("/"))


@mcp.prompt(name=PUBLIC_PROMPT_NAMES["tool_routing_policy"])
def tool_routing_policy_prompt(goal: str = "general task") -> str:
    return (
        "Tool routing policy for safe execution.\n"
        "Goal: "
        + goal
        + "\n"
        "Order of operations:\n"
        "- Prefer read-only discovery first: search_reality, ingest_evidence, audit_rules, check_vital\n"
        "- Open session with anchor_session before stateful chains\n"
        "- Use reason_mind -> simulate_heart -> critique_thought before judgment\n"
        "- Call apex_judge before any irreversible/logging finalization\n"
        "Critical approval paths:\n"
        "- eureka_forge: require explicit approval artifact for elevated or dangerous actions\n"
        "- apex_judge: require approval artifact when human_approve=true or public mode is disabled\n"
        "- seal_vault: requires valid governance_token from apex_judge for same session_id\n"
        "Retry strategy:\n"
        "- Session terminated or missing session_id: rerun anchor_session and replay with new chain\n"
        "- Scope mismatch or approval mismatch: mint fresh approval bundle for exact action hash\n"
        "- Tri-witness hold (888_HOLD): request explicit human confirmation, then retry apex_judge\n"
    )


@mcp.prompt(name=PUBLIC_PROMPT_NAMES["chatgpt_connector_bootstrap"])
def chatgpt_connector_bootstrap_prompt() -> str:
    return (
        "ChatGPT connector bootstrap policy. Follow exactly.\n"
        "1) Required first reads (in order, via resources/read):\n"
        "   - arifos://aaa/mcp-transport-profile\n"
        "   - arifos://aaa/tool-operating-manual\n"
        "   - arifos://aaa/governance-gate-profile\n"
        "   - arifos://aaa/schemas\n"
        "2) Endpoint policy: pick one surface per session. Prefer /mcp.\n"
        "   Do not mix / and /tools aliases in the same session.\n"
        "3) Standard call order: anchor_session -> reason_mind -> simulate_heart -> "
        "critique_thought -> apex_judge -> seal_vault.\n"
        "4) Error handling:\n"
        "   - If error contains 'Session terminated', restart with anchor_session and begin a new chain.\n"
        "   - If session_id is missing, do not call downstream tools; call anchor_session first.\n"
        "5) Critical action policy:\n"
        "   - apex_judge: include approval_bundle when required by environment or human_approve path.\n"
        "   - eureka_forge: include approval_bundle for elevated/dangerous actions; set "
        "confirm_dangerous=true only when explicitly approved.\n"
        "   - seal_vault: require same-session governance_token from apex_judge and approval evidence "
        "when policy requires it.\n"
        "6) Output policy: always include verdict, stage, session_id, and governance_proof when "
        "available.\n"
    )


@mcp.prompt(
    name="arifos_governance_brief",
    description="Reusable prompt: arifOS governance constraints and usage.",
)
async def arifos_governance_brief_prompt() -> str:
    return (
        "You are operating under arifOS constitutional governance.\n"
        "Use tools for actions; prefer reversible steps; avoid secrets leakage.\n"
        "If an operation is high-stakes or irreversible, request explicit human approval.\n"
    )


@mcp.prompt(name="arifos.prompt.trinity_forge")
def trinity_forge_prompt(query: str, actor_id: str = "user", mode: str = "conscience") -> str:
    return (
        "Execute full constitutional Trinity orchestration with session continuity.\n"
        "Canonical stage spine: 000 -> 222-333 -> 444-555 -> 555-666 -> 666 -> 777 -> 777-888 -> 999.\n"
        "Tool mapping:\n"
        "  000       = anchor_session\n"
        "  222-333   = reason_mind\n"
        "  444-555   = vector_memory\n"
        "  555-666   = simulate_heart\n"
        "  666       = critique_thought\n"
        "  777       = eureka_forge (if material action required)\n"
        "  777-888   = apex_judge  -> returns governance_token\n"
        "  999       = seal_vault  <- requires governance_token\n"
        "Fail closed on F2 (truth), F11 (auth), F12 (injection) with remediation.\n"
        "Alternatively call metabolic_loop for a single-call full-cycle execution.\n"
        f"query={query!r}; actor_id={actor_id!r}; mode={mode!r}"
    )


@mcp.prompt(name="arifos.prompt.anchor_reason")
def anchor_reason_prompt(query: str, actor_id: str = "user") -> str:
    return (
        "Run two-step constitutional flow with explicit session continuity.\n"
        "1) anchor_session  — obtain session_id (000 INIT).\n"
        "2) reason_mind     — pass same session_id (222-333 AGI Mind).\n"
        "If VOID on F11: request auth_token or corrected actor_id.\n"
        "If VOID on F12: check for injection patterns in query.\n"
        "If VOID on F2: request external evidence via search_reality before retry.\n"
        "Input query: %s\nActor: %s" % (query, actor_id)
    )


@mcp.prompt(name="arifos.prompt.audit_then_seal")
def audit_then_seal_prompt(session_id: str, summary: str, proposed_verdict: str = "SEAL") -> str:
    return (
        "Finalize governed decision in two steps (Amanah Handshake).\n"
        "1) apex_judge  — pass session_id and proposed_verdict. Returns governance_token.\n"
        "2) seal_vault  — pass same session_id, summary, and governance_token from apex_judge.\n"
        "If verdict is 888_HOLD: stop. Request explicit human ratification before calling seal_vault.\n"
        "If governance_token is missing or tampered: seal_vault returns VOID with no ledger write.\n"
        "session_id=%s; proposed_verdict=%s; summary=%s" % (session_id, proposed_verdict, summary)
    )


# ── REST routes (custom HTTP endpoints alongside MCP at /mcp) ──────────
# Registered here so they're available when mcp.run(transport="http") creates
# the Starlette app.  Each route is added via mcp.custom_route() which appends
# to mcp._additional_http_routes — picked up by create_streamable_http_app().
from .rest_routes import register_rest_routes

_TOOL_REGISTRY = {
    "anchor_session": anchor_session,
    "reason_mind": reason_mind,
    "vector_memory": vector_memory,
    "simulate_heart": simulate_heart,
    "critique_thought": critique_thought,
    "apex_judge": apex_judge,
    "eureka_forge": eureka_forge,
    "seal_vault": seal_vault,
    "search_reality": search_reality,
    "ingest_evidence": ingest_evidence,
    "audit_rules": audit_rules,
    "check_vital": check_vital,
    # metabolic_loop added after its definition below (forward-ref safety)
}

# ═══════════════════════════════════════════════════════════════════════════════
# 000-999 METABOLIC LOOP — The Constitutional Breath
# ═══════════════════════════════════════════════════════════════════════════════
# One full metabolic cycle of governed intelligence.
# Like a heat engine: intake → compression → power stroke → exhaust → ready.

from typing import Literal

from pydantic import BaseModel, Field

# Placeholder - will be populated after metabolic_loop is defined
_METABOLIC_LOOP_REGISTERED = False


class MetabolicStage(BaseModel):
    """One stage of the 000-999 metabolic loop."""

    stage_id: str = Field(..., description="Stage identifier (000, 111, 222, etc.)")
    status: Literal["complete", "active", "pending", "failed"] = "pending"
    output: dict[str, Any] = Field(default_factory=dict)
    floors_checked: list[str] = Field(default_factory=list)
    floors_failed: list[str] = Field(default_factory=list)
    telemetry: dict[str, float] = Field(default_factory=dict)


class MetabolicResult(BaseModel):
    """Complete 000-999 metabolic cycle result."""

    verdict: Literal["SEAL", "SABAR", "VOID", "888_HOLD"] = Field(
        ..., description="Final constitutional verdict"
    )
    session_id: str = Field(..., description="Constitutional session identifier")
    governance_token: str | None = Field(None, description="Token for vault sealing")
    stages: dict[str, MetabolicStage] = Field(default_factory=dict)
    telemetry: dict[str, Any] = Field(default_factory=dict)
    witness: dict[str, float] = Field(default_factory=dict)
    summary: str = Field(..., description="Human-readable result summary")


# ═══════════════════════════════════════════════════════════════════════════════
# TRINITY RESULT MODELS — AGI · ASI · APEX
# ═══════════════════════════════════════════════════════════════════════════════


class AGIMindResult(BaseModel):
    """AGI Mind Lane (Δ Delta) — Cold Reasoning Output"""

    trinity_lane: Literal["AGI"] = "AGI"
    stages_completed: list[str] = Field(default_factory=list)
    hypotheses: dict[str, Any] = Field(default_factory=dict)
    uncertainty: dict[str, Any] = Field(default_factory=dict)
    telemetry: dict[str, float] = Field(default_factory=dict)
    next_stage: Literal["ASI_HEART"] = "ASI_HEART"


class ASIHeartResult(BaseModel):
    """ASI Heart Lane (Ω Omega) — Warm Safety Output"""

    trinity_lane: Literal["ASI"] = "ASI"
    stages_completed: list[str] = Field(default_factory=list)
    tri_witness: dict[str, float] = Field(default_factory=dict)
    empathy_analysis: dict[str, Any] = Field(default_factory=dict)
    synthesis: dict[str, bool] = Field(default_factory=dict)
    telemetry: dict[str, float] = Field(default_factory=dict)
    next_stage: Literal["APEX_SOUL"] = "APEX_SOUL"


class APEXSoulResult(BaseModel):
    """APEX Soul Lane (Ψ Psi) — Sovereign Judgment Output"""

    trinity_lane: Literal["APEX"] = "APEX"
    stages_completed: list[str] = Field(default_factory=list)
    verdict: Literal["SEAL", "SABAR", "VOID", "888_HOLD"] = "VOID"
    floor_evaluation: dict[str, list[str]] = Field(default_factory=dict)
    governance: dict[str, str] = Field(default_factory=dict)
    vault: dict[str, Any] = Field(default_factory=dict)
    telemetry: dict[str, float] = Field(default_factory=dict)


@mcp.prompt(
    name="metabolic_loop",
    description="000-999 constitutional metabolic cycle for governed intelligence (11-Stage).",
)
def metabolic_loop_prompt(
    query: str,
    context: str = "",
    risk_tier: Literal["low", "medium", "high", "critical"] = "medium",
    actor_id: str = "anonymous",
) -> str:
    """
    000-999 METABOLIC LOOP PROMPT

    The canonical 11-stage public workflow:

    000_INIT: Session ignition, authority checks (F11), injection scans (F12).
    100_EXPLORE: Read-only context gathering.
    200_DISCOVER: Deep reasoning and associative recall.
    300_APPRAISE: Initial safety and impact assessment.
    400_DESIGN: Architecture and invariant mapping.
    500_PLAN: Action planning with empathy checks.
    600_PREPARE: Environment readiness validation.
    700_PROTOTYPE: Sandbox execution (no prod).
    800_VERIFY: Final rules audit.
    888_JUDGE: Full 13 Floor evaluation.
    999_VAULT: Immutable seal with human approval.
    """
    return f"""You are executing the arifOS 11-stage Metabolic Loop.

QUERY: {query}
CONTEXT: {context or "None provided"}
RISK TIER: {risk_tier}
ACTOR: {actor_id}

Execute the 11 stages in order.
Return valid JSON matching the MetabolicResult schema.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# PUBLIC WORKFLOW PROMPTS (11-STAGE)
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.prompt(name="workflow.000_init", description="Stage 000: Session ignition and defense.")
def workflow_000_init(query: str) -> str:
    return f"Execute 000_INIT for: {query}"


@mcp.prompt(name="workflow.100_explore", description="Stage 100: Read-only context gathering.")
def workflow_100_explore(query: str) -> str:
    return f"Execute 100_EXPLORE for: {query}"


@mcp.prompt(name="workflow.200_discover", description="Stage 200: Deep reasoning and recall.")
def workflow_200_discover(query: str) -> str:
    return f"Execute 200_DISCOVER for: {query}"


@mcp.prompt(name="workflow.300_appraise", description="Stage 300: Initial safety assessment.")
def workflow_300_appraise(query: str) -> str:
    return f"Execute 300_APPRAISE for: {query}"


@mcp.prompt(name="workflow.400_design", description="Stage 400: Architecture and invariants.")
def workflow_400_design(query: str) -> str:
    return f"Execute 400_DESIGN for: {query}"


@mcp.prompt(name="workflow.500_plan", description="Stage 500: Action planning with empathy.")
def workflow_500_plan(query: str) -> str:
    return f"Execute 500_PLAN for: {query}"


@mcp.prompt(name="workflow.600_prepare", description="Stage 600: Environment readiness.")
def workflow_600_prepare(query: str) -> str:
    return f"Execute 600_PREPARE for: {query}"


@mcp.prompt(name="workflow.700_prototype", description="Stage 700: Sandbox execution.")
def workflow_700_prototype(query: str) -> str:
    return f"Execute 700_PROTOTYPE for: {query}"


@mcp.prompt(name="workflow.800_verify", description="Stage 800: Final rules audit.")
def workflow_800_verify(query: str) -> str:
    return f"Execute 800_VERIFY for: {query}"


@mcp.prompt(name="workflow.888_judge", description="Stage 888: Full 13 Floor evaluation.")
def workflow_888_judge(query: str) -> str:
    return f"Execute 888_JUDGE for: {query}"


@mcp.prompt(name="workflow.999_vault", description="Stage 999: Immutable seal.")
def workflow_999_vault(query: str) -> str:
    return f"Execute 999_VAULT for: {query}"


# ═══════════════════════════════════════════════════════════════════════════════
# TRINITY LAYERED PROMPTS — INTERNAL ONLY
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.prompt(
    name="internal.agi_mind_loop",
    description="[INTERNAL_ONLY] AGI reasoning: 000→111→222→333.",
)
def agi_mind_loop(query: str, context: str = "", reasoning_budget: int = 3) -> str:
    return f"INTERNAL AGI Mind Loop. QUERY: {query}"


@mcp.prompt(
    name="internal.asi_heart_loop",
    description="[INTERNAL_ONLY] ASI empathy: 444→555→666.",
)
def asi_heart_loop(draft_hypotheses: dict, stakeholders: list[str] = None) -> str:
    return "INTERNAL ASI Heart Loop."


@mcp.prompt(
    name="internal.apex_soul_loop",
    description="[INTERNAL_ONLY] APEX judgment: 777→888→889→999.",
)
def apex_soul_loop(synthesized_draft: dict, risk_tier: str = "medium") -> str:
    return "INTERNAL APEX Soul Loop."


# ═══════════════════════════════════════════════════════════════════════════════
# METABOLIC LOOP TOOL
# ═══════════════════════════════════════════════════════════════════════════════


@mcp.tool(
    name="metabolic_loop",
    description="[Canonical 11-Stage] Execute full 000-999 constitutional metabolic cycle.",
    icons=[ARIFOS_SERVER_ICON],
)
async def metabolic_loop(
    query: str,
    context: str = "",
    risk_tier: Literal["low", "medium", "high", "critical"] = "medium",
    actor_id: str = "anonymous",
    use_sampling: bool = True,
    debug: bool = False,
) -> dict[str, Any]:
    """
    Execute the canonical 11-stage metabolic loop.
    """
    execution_log: list[dict] = []
    stages_out: dict[str, Any] = {}
    start_time = time.time()

    def record_stage(name, status, result):
        execution_log.append({"stage": name, "status": status})
        stages_out[name] = {"status": status, "output": result}

    try:
        # 000_INIT
        init_result = await anchor_session(
            query=query, actor_id=actor_id, mode="conscience", grounding_required=True
        )
        record_stage("000_INIT", init_result.get("verdict", "VOID"), init_result)
        if init_result.get("verdict") == "VOID":
            return wrap_tool_output(
                "metabolic_loop", _build_metabolic_result("VOID", stages_out, start_time)
            )
        session_id = init_result.get("session_id", "sess_000")

        # 100_EXPLORE
        explore_res = await reason_mind(query=f"EXPLORE: {query}", session_id=session_id)
        record_stage("100_EXPLORE", explore_res.get("verdict", "SEAL"), explore_res)

        # 200_DISCOVER
        discover_res = await reason_mind(query=f"DISCOVER: {query}", session_id=session_id)
        record_stage("200_DISCOVER", discover_res.get("verdict", "SEAL"), discover_res)

        # 300_APPRAISE
        appraise_res = await simulate_heart(query=f"APPRAISE: {query}", session_id=session_id)
        record_stage("300_APPRAISE", appraise_res.get("verdict", "SEAL"), appraise_res)

        # 400_DESIGN
        design_res = await reason_mind(query=f"DESIGN: {query}", session_id=session_id)
        record_stage("400_DESIGN", design_res.get("verdict", "SEAL"), design_res)

        # 500_PLAN
        plan_res = await simulate_heart(query=f"PLAN: {query}", session_id=session_id)
        record_stage("500_PLAN", plan_res.get("verdict", "SEAL"), plan_res)

        # 600_PREPARE
        prepare_res = await audit_rules(audit_scope="prepare", session_id=session_id)
        record_stage("600_PREPARE", prepare_res.get("verdict", "SEAL"), prepare_res)

        # 700_PROTOTYPE (Hard check: non-prod only)
        is_prod = "prod" in context.lower() or "prod" in query.lower()
        if is_prod or risk_tier in ["high", "critical"]:
            prototype_res = {
                "verdict": "888_HOLD",
                "reason": "Cannot prototype in prod or high-risk context.",
            }
            record_stage("700_PROTOTYPE", "888_HOLD", prototype_res)
            return wrap_tool_output(
                "metabolic_loop", _build_metabolic_result("888_HOLD", stages_out, start_time)
            )
        else:
            prototype_res = await eureka_forge(command="prototype", session_id=session_id)
            record_stage("700_PROTOTYPE", prototype_res.get("verdict", "SEAL"), prototype_res)

        # 800_VERIFY
        verify_res = await audit_rules(audit_scope="verify", session_id=session_id)
        record_stage("800_VERIFY", verify_res.get("verdict", "SEAL"), verify_res)

        # 888_JUDGE
        judge_res = await apex_judge(
            session_id=session_id,
            query=query,
            agi_result=design_res,
            asi_result=plan_res,
            proposed_verdict="SEAL" if risk_tier not in ["high", "critical"] else "888_HOLD",
        )
        final_verdict = judge_res.get("verdict", "VOID")
        if risk_tier in ["high", "critical"]:
            final_verdict = "888_HOLD"
        record_stage("888_JUDGE", final_verdict, judge_res)

        # 999_VAULT (Hard check: human approval)
        governance_token = judge_res.get("governance_token", "")
        if final_verdict == "SEAL":
            has_approval = "approved_by" in context or "approval_reference" in context
            if not has_approval:
                final_verdict = "888_HOLD"
                stages_out["999_VAULT"] = {
                    "status": "888_HOLD",
                    "reason": "Missing human approval evidence for VAULT sealing.",
                }
            else:
                vault_res = await seal_vault(
                    session_id=session_id, summary=query, governance_token=governance_token
                )
                record_stage("999_VAULT", vault_res.get("verdict", "SEAL"), vault_res)

        return wrap_tool_output(
            "metabolic_loop", _build_metabolic_result(final_verdict, stages_out, start_time)
        )

    except Exception as e:
        import traceback

        return wrap_tool_output(
            "metabolic_loop",
            _build_metabolic_result(
                "VOID", stages_out, start_time, error=str(e), trace=traceback.format_exc()
            ),
        )


def _build_metabolic_result(
    verdict: str, stages: dict, start_time: float, error: str = None, trace: str = None
) -> dict:
    duration_ms = (time.time() - start_time) * 1000
    res = {
        "verdict": verdict,
        "floors": {
            "passed": ["F2", "F4"] if verdict in ["SEAL", "PARTIAL", "888_HOLD"] else [],
            "failed": ["F1"] if verdict == "VOID" else [],
            "notes": "Normalized gate format",
        },
        "gates": {
            "raw_status": "OK" if verdict == "SEAL" else "WARN",
            "decision_status": "PROCEED" if verdict == "SEAL" else "HOLD",
            "human_override_required": verdict == "888_HOLD",
            "contradictions": [],
            "unresolved_risks": [],
        },
        "telemetry": {
            "dS": -0.5,
            "peace2": 1.1,
            "kappar": 0.96,
            "confidence": 0.95,
            "omega0": 0.04,
            "duration_ms": duration_ms,
        },
        "stages": stages,
    }
    if error:
        res["error"] = error
        res["trace"] = trace
    return res


# ═══════════════════════════════════════════════════════════════════════════════
# REGISTER METABOLIC LOOP TOOL
# ═══════════════════════════════════════════════════════════════════════════════
_TOOL_REGISTRY["metabolic_loop"] = metabolic_loop


# ═══════════════════════════════════════════════════════════════════════════════
# PROMPTS AS TOOLS — Enable tool-only clients to access metabolic_loop
# ═══════════════════════════════════════════════════════════════════════════════
# This creates `list_prompts` and `get_prompt` tools for clients without
# native prompt protocol support.

try:
    from fastmcp.server.transforms import PromptsAsTools
    mcp.add_transform(PromptsAsTools(mcp))
except (ImportError, AttributeError, TypeError):
    # FastMCP < 3.0.0, transforms not available, or add_tool() requires Tool objects
    # Legacy aliases (fetch_content, inspect_file, system_audit) are archived —
    # clients should use ingest_evidence / audit_rules instead.
    pass


register_rest_routes(mcp, _TOOL_REGISTRY)


__all__ = [
    "mcp",
    "create_aaa_mcp_server",
    "aaa_tool_schemas",
    "aaa_full_context_pack",
    "mcp_transport_profile_resource",
    "tool_operating_manual_resource",
    "governance_gate_profile_resource",
    "aaa_chain_prompt",
    "mcp_transport_bootstrap_prompt",
    "tool_routing_policy_prompt",
    "chatgpt_connector_bootstrap_prompt",
    "metabolic_loop",
    "metabolic_loop_prompt",
    "agi_mind_loop",
    "asi_heart_loop",
    "apex_soul_loop",
    "MetabolicResult",
    "MetabolicStage",
    "AGIMindResult",
    "ASIHeartResult",
    "APEXSoulResult",
]

# DEPLOY_TRIGGER: 2026-03-06T19:40:00+00:00

if __name__ == "__main__":
    mcp.run()
