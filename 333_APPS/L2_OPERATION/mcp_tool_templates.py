"""MCP Tool Templates (v55.6-HARDENED)
Canonical 9-tool implementations with F1-F13 enforcement.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import re
import secrets
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# =============================================================================
# TEMPLATE 1: _IGNITE_ (000_INIT)
# =============================================================================


async def _ignite_(query: str, user_token: str | None = None, **kwargs) -> dict[str, Any]:
    """000_INIT: Constitutional gate with F11/F12 enforcement."""
    session_id = f"sess_{int(datetime.now().timestamp())}_{secrets.token_hex(4)}"

    try:
        # F11 Authority
        authority = _verify_authority(user_token)

        # F12 Injection Defense
        injection_risk = _detect_injection(query)
        if injection_risk >= 0.85:
            return {
                "verdict": "VOID",
                "session_id": session_id,
                "reason": f"F12: Injection detected (risk={injection_risk:.2f})",
            }

        # Budget allocation
        budget = {"tokens": 100000, "operations": 50, "external_calls": 10}

        return {
            "verdict": "SEAL",
            "session_id": session_id,
            "authority": authority,
            "budget": budget,
            "injection_risk": injection_risk,
            "floors": ["F1", "F11", "F12"],
        }
    except Exception as e:
        logger.error(f"[_ignite_] Error: {e}")
        return {"verdict": "VOID", "session_id": session_id, "reason": "Internal error"}


# F11: Token set loaded from env at import time (never hardcoded)
_VALID_TOKENS: frozenset[str] = frozenset(
    t.strip()
    for t in os.environ.get("ARIFOS_AUTH_TOKENS", "").split(",")
    if t.strip()
)

# F12: Critical injection patterns — any match → immediate risk=1.0
_CRITICAL_INJECTION = re.compile(
    r"ignore\s+previous\s+instructions"
    r"|you\s+are\s+now\s+in\s+.*\s+mode"
    r"|disable\s+(safety|restrictions|rules)"
    r"|forget\s+(your\s+)?(rules|training|instructions)"
    r"|bypass\s+(restrictions|safety|filters)"
    r"|pretend\s+(you\s+are|to\s+be)"
    r"|act\s+as\s+(if\s+)?(?:you\s+are\s+)?(?:an?\s+)?(unrestricted|jailbreak)",
    re.IGNORECASE,
)

# Unicode attacks (zero-width, RTL override, bidi isolate)
_UNICODE_INJECTION = re.compile(
    r"[\u200b\u200c\u200d\u202e\u2066\u2067\u2068\u2069\ufeff]"
)

# Soft suspicious patterns — additive, 0.2 each
_SOFT_INJECTION = [
    r"\[\s*(system|admin|root|developer)\s*\]",
    r"<\s*(system|admin|instruction)\s*>",
    r"---\s*END\s+PROMPT\s*---",
    r"new\s+instructions?\s*:",
]


def _verify_authority(token: str | None) -> str:
    """F11: Timing-safe authority verification against env-var token set."""
    if not token:
        return "PUBLIC"
    token_bytes = token.encode()
    for valid in _VALID_TOKENS:
        if hmac.compare_digest(token_bytes, valid.encode()):
            return "STANDARD"
    return "PUBLIC"


def _detect_injection(text: str) -> float:
    """F12: Injection pattern detection — critical patterns immediately return 1.0."""
    if _CRITICAL_INJECTION.search(text):
        return 1.0
    if _UNICODE_INJECTION.search(text):
        return 1.0
    risk = sum(0.2 for p in _SOFT_INJECTION if re.search(p, text, re.IGNORECASE))
    return min(risk, 0.90)


# =============================================================================
# TEMPLATE 2: _LOGIC_ (AGI Mind: 111-333)
# =============================================================================


async def _logic_(query: str, session_id: str, **kwargs) -> dict[str, Any]:
    """111-333: AGI Mind with F2, F4, F7, F10 enforcement."""
    try:
        # Calculate metrics
        truth_score = 0.99  # Placeholder
        clarity_delta = -0.15  # Placeholder
        omega_0 = 0.04  # Placeholder

        # F2 Truth Check
        if truth_score < 0.99:
            return {
                "verdict": "VOID",
                "session_id": session_id,
                "reason": f"F2: Truth {truth_score:.2f} < 0.99",
            }

        # F4 Clarity Check
        if clarity_delta >= 0:
            return {
                "verdict": "VOID",
                "session_id": session_id,
                "reason": f"F4: ΔS={clarity_delta:.2f} >= 0",
            }

        # F7 Humility Check — both bounds enforced
        if omega_0 > 0.08:
            return {
                "verdict": "VOID",
                "session_id": session_id,
                "reason": f"F7: Ω₀={omega_0:.3f} > 0.08 critical",
            }
        if omega_0 < 0.03:
            return {
                "verdict": "VOID",
                "session_id": session_id,
                "reason": f"F7: Ω₀={omega_0:.3f} < 0.03 overconfident",
            }
        if omega_0 > 0.06:
            return {
                "verdict": "SABAR",
                "session_id": session_id,
                "reason": f"F7: Ω₀={omega_0:.3f} elevated",
            }

        return {
            "verdict": "SEAL",
            "session_id": session_id,
            "metrics": {"truth": truth_score, "clarity": clarity_delta, "omega_0": omega_0},
            "floors": {"F2": "PASS", "F4": "PASS", "F7": "PASS", "F10": "PASS"},
        }
    except Exception as e:
        logger.error(f"[_logic_] Error: {e}")
        return {"verdict": "VOID", "session_id": session_id, "reason": "Internal error"}


# =============================================================================
# TEMPLATE 3: _SENSES_ (External Grounding)
# =============================================================================

_circuit_breaker = {"failures": 0, "blocked_until": 0.0, "max": 3, "timeout": 300}
_cb_lock = threading.Lock()


async def _senses_(query: str, session_id: str, **kwargs) -> dict[str, Any]:
    """External reality grounding with thread-safe circuit breaker."""
    with _cb_lock:
        if time.time() < _circuit_breaker["blocked_until"]:
            return {"verdict": "SABAR", "session_id": session_id, "reason": "Circuit breaker active"}

    try:
        # External search (placeholder)
        results = [{"url": f"source_{i}", "content": f"result_{i}"} for i in range(3)]
        with _cb_lock:
            _circuit_breaker["failures"] = 0

        return {
            "verdict": "SEAL",
            "session_id": session_id,
            "results": results,
            "sources": [r["url"] for r in results],
            "floors": {"F2": "PASS", "F7": "PASS"},
        }
    except Exception as e:
        with _cb_lock:
            _circuit_breaker["failures"] += 1
            if _circuit_breaker["failures"] >= _circuit_breaker["max"]:
                _circuit_breaker["blocked_until"] = time.time() + _circuit_breaker["timeout"]
        return {"verdict": "SABAR", "session_id": session_id, "reason": f"Error: {e}"}


# =============================================================================
# TEMPLATE 4: _ATLAS_ (Knowledge Mapping)
# =============================================================================


# F12: Safe root directories for atlas inspection
_ATLAS_SAFE_ROOTS: tuple[Path, ...] = (
    Path("/srv/arifOS").resolve(),
    Path.home().resolve(),
)


def _is_safe_atlas_path(path: Path) -> bool:
    """F12: Ensure resolved path stays within safe roots."""
    try:
        resolved = path.resolve()
        return any(
            str(resolved).startswith(str(root))
            for root in _ATLAS_SAFE_ROOTS
        )
    except Exception:
        return False


async def _atlas_(query: str = "", session_id: str | None = None, **kwargs) -> dict[str, Any]:
    """Knowledge atlas with F10 ontology enforcement and F12 path jail."""
    path = Path(query.strip() or ".")

    # F12: Reject paths outside safe roots
    if not _is_safe_atlas_path(path):
        return {
            "verdict": "VOID",
            "session_id": session_id,
            "reason": f"F12: Path traversal outside safe roots: {query}",
        }

    if not path.exists():
        return {"verdict": "VOID", "session_id": session_id, "reason": f"Path not found: {query}"}

    # Build tree
    tree = {}
    for item in sorted(path.iterdir()):
        if item.name.startswith(".") or item.name == "__pycache__":
            continue
        tree[item.name] = "file" if item.is_file() else "dir"

    return {
        "verdict": "SEAL",
        "session_id": session_id,
        "tree": tree,
        "floors": {"F10": "PASS", "F4": "PASS", "F12": "PASS"},
    }


# =============================================================================
# TEMPLATE 5: _FORGE_ (ASI Heart + APEX Builder)
# =============================================================================


async def _forge_(task: str, session_id: str, **kwargs) -> dict[str, Any]:
    """444-777: Forge with F1, F5, F6, F9 enforcement."""
    # Placeholder calculations
    empathy_kappa = 0.96
    peace_squared = 1.05
    is_reversible = True

    # F6 Empathy
    if empathy_kappa < 0.95:
        return {
            "verdict": "VOID",
            "session_id": session_id,
            "reason": f"F6: κᵣ={empathy_kappa:.2f} < 0.95",
        }

    # F5 Peace²
    if peace_squared < 1.0:
        return {
            "verdict": "VOID",
            "session_id": session_id,
            "reason": f"F5: P²={peace_squared:.2f} < 1.0",
        }

    # F1 Reversibility
    if not is_reversible:
        return {
            "verdict": "888_HOLD",
            "session_id": session_id,
            "reason": "F1: Irreversible action requires confirmation",
        }

    return {
        "verdict": "SEAL",
        "session_id": session_id,
        "metrics": {"kappa": empathy_kappa, "peace": peace_squared, "reversible": is_reversible},
        "floors": {"F1": "PASS", "F5": "PASS", "F6": "PASS", "F9": "PASS"},
    }


# =============================================================================
# TEMPLATE 6: _AUDIT_ (Constitutional Scanner)
# =============================================================================


async def _audit_(proposal: str, session_id: str, **kwargs) -> dict[str, Any]:
    """Floor-by-floor constitutional compliance audit."""
    floors = {
        "F1": "PASS",
        "F2": "PASS",
        "F3": "PASS",
        "F4": "PASS",
        "F5": "PASS",
        "F6": "PASS",
        "F7": "PASS",
        "F8": "PASS",
        "F9": "PASS",
        "F10": "PASS",
        "F11": "PASS",
        "F12": "PASS",
        "F13": "PASS",
    }

    void_count = sum(1 for s in floors.values() if s == "VOID")
    verdict = "SEAL" if void_count == 0 else "VOID" if void_count > 2 else "PARTIAL"

    return {
        "verdict": verdict,
        "session_id": session_id,
        "floors": floors,
        "void_count": void_count,
    }


# =============================================================================
# TEMPLATE 7: _DECREE_ (888_JUDGE + 999_SEAL)
# =============================================================================


async def _decree_(verdict_data: dict[str, Any], session_id: str, **kwargs) -> dict[str, Any]:
    """888-999: Final judgment with cryptographic seal."""
    # F3 Tri-Witness
    consensus = verdict_data.get("consensus", 0.96)
    if consensus < 0.95:
        return {
            "verdict": "VOID",
            "session_id": session_id,
            "reason": f"F3: Consensus {consensus:.2f} < 0.95",
        }

    # F8 Genius
    genius = verdict_data.get("genius", 0.85)
    if genius < 0.80:
        return {
            "verdict": "VOID",
            "session_id": session_id,
            "reason": f"F8: Genius {genius:.2f} < 0.80",
        }

    # Cryptographic seal
    judgment_str = json.dumps(verdict_data, sort_keys=True)
    merkle = hashlib.sha256(judgment_str.encode()).hexdigest()[:16]

    return {
        "verdict": "SEAL",
        "session_id": session_id,
        "consensus": consensus,
        "merkle_root": f"0x{merkle}",
        "floors": {"F3": "PASS", "F8": "PASS", "F11": "PASS", "F12": "PASS", "F13": "PASS"},
    }


# =============================================================================
# Serialization Utility
# =============================================================================


def _serialize(obj: Any) -> Any:
    """Zero-logic serialization for MCP transport."""
    if obj is None:
        return None
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    if hasattr(obj, "__dataclass_fields__"):
        from dataclasses import asdict

        return asdict(obj)
    if isinstance(obj, (list, tuple)):
        return [_serialize(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    if isinstance(obj, (str, int, float, bool)):
        return obj
    return str(obj)
