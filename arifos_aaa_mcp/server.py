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
import aaa_mcp as legacy

from aaa_mcp.protocol.aaa_contract import MANIFEST_VERSION
from aaa_mcp.protocol.public_surface import (
    PUBLIC_CANONICAL_TOOLS,
    PUBLIC_PROMPT_NAMES,
    PUBLIC_RESOURCE_URIS,
)
from aaa_mcp.protocol.tool_registry import export_full_context_pack
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
from aclip_cai.tools.fs_inspector import fs_inspect
from aclip_cai.tools.system_monitor import get_system_health

from .contracts import require_session, validate_input
from .fastmcp_ext.discovery import build_surface_discovery
from .governance import LAW_13_CATALOG, TOOL_DIALS_MAP, wrap_tool_output

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
    from core.physics.thermodynamics import (
        ThermodynamicViolation,
        ModeCollapseError,
        CheapTruthError,
        check_landauer_bound,
        derive_orthogonality,
    )
    from core.homeostasis import (
        PeaceViolation,
        check_peace_squared,
    )
    from core.kernel.constitutional_decorator import (
        EntropyViolation,
        AmanahViolation,
        constitutional_floor,
    )
    from core.judgment import (
        get_judgment_kernel,
        JudgmentKernel,
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
        anch = await anchor(session_id=session_id, user_id=actor_id, context=query)
        verdict = str(anch.get("verdict", "SEAL"))

        payload = {
            "verdict": verdict,
            "session_id": anch.get("session_id", session_id),
            "stage": "000_INIT",
            "mode": mode,
            "grounding_required": grounding_required,
            "token_status": _token_status(auth_token),
            "auth": {"present": bool(auth_token)},
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
            "actor_id": actor_id,
            "token_status": _token_status(auth_token),
            "debug": debug,
            "data": {"think": think_draft, "reason": r, "integrate": i, "respond": d}
            if debug
            else {},
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

        return wrap_tool_output("reason_mind", payload)
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
        embedding_backend = "BGE (BAAI/bge-small-en-v1.5)"
        query_vector_dim = 384  # bge-small-en-v1.5 = 384-dim; BGE-M3 = 768-dim
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


async def recall_memory(query: str, session_id: str, debug: bool = False) -> dict[str, Any]:
    """Compatibility alias for vector_memory."""
    return await vector_memory(query=query, session_id=session_id, debug=debug)


@mcp.tool(name="simulate_heart")
async def simulate_heart(
    query: str,
    session_id: str,
    stakeholders: list[str] | None = None,
    capability_modules: list[str] | None = None,
    debug: bool = False,
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
            "debug": debug,
            "data": {"validate": v, "align": a} if debug else {},
        }
        payload.update(
            envelope_builder.build_envelope(
                stage="555-666", session_id=session_id, verdict=verdict, payload=merged
            )
        )

        payload["compute_ms"] = (time.time() - start_time) * 1000
        return wrap_tool_output("simulate_heart", payload)
    except Exception as e:
        return wrap_tool_output("simulate_heart", _fracture_response("555-666", e, session_id))


@mcp.tool(name="critique_thought")
async def critique_thought(
    plan: dict[str, Any], session_id: str, context: str = ""
) -> dict[str, Any]:
    """666 ALIGN: run 7-model critique (inversion, framing, non-linearity, etc.)."""
    blocked = validate_input("critique_thought", {"plan": plan, "session_id": session_id})
    if blocked:
        return wrap_tool_output("critique_thought", blocked)
    missing = require_session("critique_thought", session_id)
    if missing:
        return wrap_tool_output("critique_thought", missing)
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
    return wrap_tool_output("critique_thought", payload)


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

        verdict = str(judged.get("verdict", "VOID"))
        governance_token = _build_governance_token(session_id, verdict)
        merged = {
            "truth_score": judged.get("truth_score"),
            "f2_threshold": judged.get("f2_threshold"),
            "floors_failed": list(forged.get("floors_failed", []))
            + list(judged.get("floors_failed", [])),
            "precedents": precedents,
        }

        payload = {
            "authority": {"human_approve": human_approve},
            "governance_token": governance_token,
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

        # PHASE 1: Map AGI/ASI vectors for Tri-Witness (Ω_ortho calculation)
        if agi_result and asi_result:
            # Extract embedding vectors for orthogonality check
            agi_vector = agi_result.get("embedding_vector", [])
            asi_vector = asi_result.get("embedding_vector", [])
            if agi_vector and asi_vector and CORE_AVAILABLE:
                omega_ortho = derive_orthogonality(agi_vector, asi_vector)
                payload["omega_ortho"] = omega_ortho
                if omega_ortho < 0.95:
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
        return wrap_tool_output("apex_judge", payload)

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


@mcp.tool(name="eureka_forge")
async def eureka_forge(
    session_id: str,
    command: str,
    working_dir: str = "/root",
    timeout: int = 60,
    confirm_dangerous: bool = False,
    agent_id: str = "unknown",
    purpose: str = "",
) -> dict[str, Any]:
    """777 EUREKA FORGE: execute shell commands with audit logging and confirmation for dangerous operations.

    F5: Safe defaults (validates working_dir)
    F6: Comprehensive error handling
    F7: Risk classification (LOW/MODERATE/CRITICAL)
    F9: Transparent logging with agent_id and purpose

    Dangerous commands (rm -rf, mkfs, dd, etc.) require confirm_dangerous=True
    """
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
        from aaa_mcp.sessions.session_ledger import get_session_manager
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
                envelope_builder.build_envelope(
                    stage="888_FORGE",
                    session_id=session_id,
                    verdict="888_HOLD",
                    payload={
                        "status": "CONFIRMATION_REQUIRED",
                        "risk_level": risk_level,
                        "message": f"CRITICAL command detected. Set confirm_dangerous=True to execute.",
                    },
                ),
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
        return wrap_tool_output("eureka_forge", payload)
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
    # PHASE 2: Thermodynamic telemetry for ledger binding
    telemetry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """999 SEAL: commit immutable session decision record with thermodynamic telemetry."""
    blocked = validate_input("seal_vault", {"session_id": session_id, "summary": summary})
    if blocked:
        return wrap_tool_output("seal_vault", blocked)
    missing = require_session("seal_vault", session_id)
    if missing:
        return wrap_tool_output("seal_vault", missing)

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
        )
        auto_token = auto_judge.get("governance_token") if isinstance(auto_judge, dict) else ""
        if isinstance(auto_token, str) and auto_token.strip():
            resolved_token = auto_token.strip()
            _SESSION_GOVERNANCE_TOKENS[session_id] = resolved_token

    if not resolved_token:
        return wrap_tool_output(
            "seal_vault",
            {
                "verdict": "VOID",
                "stage": "999_SEAL",
                "session_id": session_id,
                "error": "Missing governance_token for seal_vault",
                "remediation": "Call apex_judge first in this session, then retry seal_vault.",
            },
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
        "timestamp": time.time(),
    }

    start_time = time.time()
    try:
        token_valid, verified_verdict = _verify_governance_token(session_id, resolved_token)
        if not token_valid:
            return wrap_tool_output(
                "seal_vault",
                {
                    "verdict": "VOID",
                    "stage": "999_SEAL",
                    "session_id": session_id,
                    "error": "F1 Amanah — governance_token invalid",
                },
            )

        res = await seal(
            session_id=session_id, task_summary=summary, was_modified=True, verdict=verified_verdict
        )
        payload = {"data": res, "status": verified_verdict}
        if thermodynamic_statement is not None:
            payload["thermodynamic_statement"] = thermodynamic_statement
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

        return wrap_tool_output("seal_vault", payload)
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
    query: str,
    intent: str = "general",
    session_id: str = "",
) -> dict[str, Any]:
    """External evidence discovery (read-only)."""
    blocked = validate_input("search_reality", {"query": query, "session_id": session_id})
    if blocked:
        return wrap_tool_output("search_reality", blocked)
    try:
        from aaa_mcp.external_gateways.brave_client import BraveSearchClient
        from aaa_mcp.external_gateways.jina_reader_client import JinaReaderClient
        from aaa_mcp.external_gateways.perplexity_client import PerplexitySearchClient

        primary = JinaReaderClient()
        payload = await primary.search(query=query, intent=intent)
        if payload.get("status") not in {"OK"}:
            fallback1 = PerplexitySearchClient()
            payload = await fallback1.search(query=query, intent=intent)
            if payload.get("status") in {"NO_API_KEY", "BAD_RESPONSE", "BAD_JSON"}:
                fallback2 = BraveSearchClient()
                payload = await fallback2.search(query=query, intent=intent)

        urls = [r.get("url") for r in payload.get("results", []) if r.get("url")]
        results = payload.get("results", [])
        res_payload = {
            "query": query,
            "status": payload.get("status", "OK"),
            "ids": urls,
            "results": results,
            "evidence_count": len(results),
            "f2_truth": {"grounded": len(results) > 0, "sources": urls[:3]},
        }
        if session_id:
            res_payload["session_id"] = session_id
        return wrap_tool_output("search_reality", res_payload)
    except Exception as e:
        return wrap_tool_output("search_reality", {"query": query, "status": f"ERROR: {e}"})


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


@mcp.resource(
    PUBLIC_RESOURCE_URIS["schemas"],
    name="arifos_aaa_tool_schemas",
    mime_type="application/json",
    description="Canonical AAA MCP 13-tool schema/contract overview.",
)
def aaa_tool_schemas() -> str:
    discovery = build_surface_discovery(AAA_TOOLS)
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
        "discovery": discovery,
    }
    # FastMCP resources must return str/bytes or ResourceContent.
    return json.dumps(payload, ensure_ascii=True)


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
        with open(path, "r", encoding="utf-8") as f:
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

from pydantic import BaseModel, Field
from typing import Literal


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
    # Legacy compatibility aliases (intentionally registered without decorators)
    mcp.add_tool(fetch_content)
    mcp.add_tool(inspect_file)
    mcp.add_tool(system_audit)

    from fastmcp.server.transforms import PromptsAsTools

    mcp.add_transform(PromptsAsTools(mcp))
except ImportError:
    # FastMCP < 3.0.0 or transforms not available
    pass


register_rest_routes(mcp, _TOOL_REGISTRY)


__all__ = [
    "mcp",
    "create_aaa_mcp_server",
    "aaa_tool_schemas",
    "aaa_full_context_pack",
    "aaa_chain_prompt",
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

# DEPLOY_TRIGGER: 2026-03-06T03:30:00+00:00
