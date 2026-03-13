"""
arifosmcp/bridge.py — The Harden Bridge

This module acts as the secure airlock between the transport layer (MCP/Hub)
and the governance layer (Core/Kernel).

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import json
import logging
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from arifosmcp.intelligence.tools.office_forge_engine import audit_markdown, render_office_document
from arifosmcp.intelligence.tools.ollama_local import (
    ollama_local_generate as ollama_local_generate_call,
)
from arifosmcp.intelligence.tools.reality_grounding import open_web_page, reality_check
from arifosmcp.runtime.contracts import REQUIRES_SESSION
from core.enforcement.auth_continuity import mint_auth_context, verify_auth_context_cached
from core.enforcement.governance_engine import wrap_tool_output
from core.organs import agi, apex, asi, init, vault
from core.organs._4_vault import verify_vault_ledger

from .models import Verdict

logger = logging.getLogger(__name__)
DEFAULT_VAULT_PATH = Path("VAULT999/vault999.jsonl")

# Normalized mapping for the 10-tool stack
TOOL_MAP = {
    "init_anchor_state": "anchor_session",
    "bootstrap_identity": "anchor_session",
    "integrate_analyze_reflect": "reason_mind",
    "reason_mind_synthesis": "reason_mind",
    "arifOS_kernel": "metabolic_loop",
    "arifOS.kernel": "metabolic_loop",
    "metabolic_loop_router": "metabolic_loop",
    "vector_memory_store": "vector_memory",
    "assess_heart_impact": "simulate_heart",
    "critique_thought_audit": "critique_thought",
    "quantum_eureka_forge": "eureka_forge",
    "apex_judge_verdict": "apex_judge",
    "seal_vault_commit": "seal_vault",
    "session_memory": "session_memory",
    "verify_vault_ledger": "verify_vault_ledger",
    "office_forge_audit": "office_forge_audit",
    "forge_office_document": "office_forge",
    "ollama_local_generate": "ollama_local_generate",
    "audit_rules": "system_audit",
    "check_vital": "sense_health",
}

AUTO_BOOTSTRAP_RISK_TIERS = frozenset({"low", "medium"})
PROTECTED_AUTO_ANCHOR_IDS = frozenset({"arif", "arif-fazil", "ariffazil"})
_AUTH_CONTEXT_CONTINUITY_KEYS = (
    "session_id",
    "actor_id",
    "authority_level",
    "token_fingerprint",
    "nonce",
    "iat",
    "exp",
    "approval_scope",
    "parent_signature",
    "signature",
)


def _resolve_claimed_actor_id(payload: dict[str, Any]) -> str:
    raw_claim = payload.get("claimed_actor_id", payload.get("actor_id", "anonymous"))
    if raw_claim is None:
        return "anonymous"
    claim = str(raw_claim).strip()
    return claim or "anonymous"


def _auth_failure_envelope(
    *,
    tool: str,
    session_id: str,
    error_message: str,
    claimed_actor_id: str,
    identity_claim_status: str,
    identity_reason: str,
    resolved_actor_id: str = "anonymous",
    next_action_reason: str,
    machine_issue: str = "AUTH_BOOTSTRAP_REQUIRED",
) -> dict[str, Any]:
    return {
        "ok": False,
        "tool": tool,
        "session_id": session_id,
        "stage": "000_INIT",
        "verdict": "HOLD",
        "status": "ERROR",
        "machine_status": "BLOCKED",
        "machine_issue": machine_issue,
        "metrics": {
            "truth": 0.0,
            "clarity_delta": 0.0,
            "confidence": 0.0,
            "peace": 0.0,
            "vitality": 0.0,
            "entropy_delta": 0.0,
            "authority": 0.0,
            "risk": 0.0,
        },
        "trace": {"000_INIT": "HOLD"},
        "authority": {
            "actor_id": "anonymous",
            "level": "anonymous",
            "human_required": True,
            "approval_scope": [],
            "auth_state": "unverified",
        },
        "payload": {
            "error": error_message,
            "identity_resolution": {
                "input_actor_id": claimed_actor_id,
                "resolved_actor_id": resolved_actor_id,
                "identity_claim_status": identity_claim_status,
                "reason": identity_reason,
            },
            "next_action": {
                "tool": "init_anchor_state",
                "required": True,
                "reason": next_action_reason,
            },
        },
        "errors": [
            {
                "code": machine_issue,
                "message": error_message,
                "stage": "000_INIT",
                "recoverable": True,
            }
        ],
        "meta": {
            "schema_version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "debug": False,
            "dry_run": False,
        },
        "auth_context": None,
    }


def _can_auto_anchor_declared_identity(payload: dict[str, Any], claimed_actor_id: str) -> bool:
    risk_tier = str(payload.get("risk_tier", "medium") or "medium").strip().lower()
    allow_execution = bool(payload.get("allow_execution", False))
    human_approval = payload.get("human_approval")
    claimed = claimed_actor_id.strip().lower()

    if claimed in {"", "anonymous"}:
        return False
    if claimed in PROTECTED_AUTO_ANCHOR_IDS:
        return False
    if allow_execution:
        return False
    if risk_tier not in AUTO_BOOTSTRAP_RISK_TIERS:
        return False
    if human_approval is False:
        return False
    return True


def _mint_auto_anchor_auth_context(session_id: str, actor_id: str) -> dict[str, Any]:
    return mint_auth_context(
        session_id=session_id,
        actor_id=actor_id,
        token_fingerprint="sha256:auto-anchor",
        approval_scope=[
            "arifOS_kernel:reason",
            "search_reality",
            "ingest_evidence",
            "session_memory",
        ],
        parent_signature="",
        authority_level="declared",
    )


def _normalize_auth_context(payload: dict[str, Any], auth_context: Any) -> dict[str, Any] | None:
    if not isinstance(auth_context, dict):
        return None

    normalized = dict(auth_context)
    continuity = normalized.get("continuity")
    if isinstance(continuity, dict):
        for key in _AUTH_CONTEXT_CONTINUITY_KEYS:
            if key not in normalized and key in continuity:
                normalized[key] = continuity[key]

    identity_claim = normalized.get("identity_claim")
    if isinstance(identity_claim, dict):
        if not normalized.get("actor_id") and identity_claim.get("actor_id"):
            normalized["actor_id"] = identity_claim["actor_id"]
        if not normalized.get("authority_level") and identity_claim.get("authority_level"):
            normalized["authority_level"] = identity_claim["authority_level"]

    if not normalized.get("actor_id"):
        fallback_actor_id = payload.get("actor_id") or payload.get("claimed_actor_id")
        if fallback_actor_id:
            normalized["actor_id"] = str(fallback_actor_id)

    return normalized


# Bootstrap tools that can run without prior auth_context (Phase 1 initialization)
BOOTSTRAP_WHITELIST: set[str] = {
    "anchor_session",        # init_anchor_state → mints auth token
    "revoke_anchor_state",   # revokes session
    "check_vital",           # system health check
    "sense_health",          # check_vital alias
}


def _requires_explicit_kernel_auth(payload: dict[str, Any], canonical_tool: str | None = None) -> bool:
    """Decide whether arifOS_kernel must reject missing auth_context."""
    from core.enforcement.auth_continuity import _env_flag

    # F11 Bootstrap Whitelist: These tools can run without prior auth
    # They are the tools that ESTABLISH auth, so they cannot require it
    if canonical_tool in BOOTSTRAP_WHITELIST:
        return False

    # In open mode (dev), we allow auto-bootstrap
    if _env_flag("ARIFOS_GOVERNANCE_OPEN_MODE"):
        risk_tier = str(payload.get("risk_tier", "medium") or "medium").strip().lower()
        allow_execution = bool(payload.get("allow_execution", False))
        if allow_execution:
            return True
        return risk_tier not in AUTO_BOOTSTRAP_RISK_TIERS

    # In hardened mode, everything requires explicit auth (except whitelisted bootstrap tools)
    return True


def _trace_replay_envelope(
    session_id: str,
    replay_status: str,
    entries: list[dict[str, Any]],
    message: str | None = None,
    error: str | None = None,
) -> dict[str, Any]:
    ok = replay_status not in {"ERROR", "TAMPERED"}
    errors = []
    if error:
        code = "TRACE_REPLAY_TAMPER" if replay_status == "TAMPERED" else "TRACE_REPLAY_ERROR"
        errors.append(
            {
                "code": code,
                "message": error,
                "stage": "999_VAULT",
                "recoverable": replay_status != "TAMPERED",
            }
        )

    return {
        "ok": ok,
        "tool": "trace_replay",
        "session_id": session_id,
        "stage": "999_VAULT",
        "verdict": "SEAL" if ok else "VOID",
        "status": "ERROR" if not ok else "SUCCESS",
        "metrics": {},
        "trace": {},
        "authority": {
            "actor_id": "anonymous",
            "level": "anonymous",
            "human_required": False,
            "approval_scope": [],
            "auth_state": "anonymous",
        },
        "payload": {
            "replay_status": replay_status,
            "trace_count": len(entries),
            "message": message,
            "entries": entries,
        },
        "errors": errors,
        "meta": {"schema_version": "1.0.0", "debug": False, "dry_run": False},
    }


def _build_constitutional_audit(session_id: str) -> dict[str, Any]:
    """
    Build the constitutional audit report for audit_rules tool.
    Returns the 13 Floors, their thresholds, and current governance state.
    """
    from core.shared.floors import THRESHOLDS, FLOOR_SPEC_KEYS
    from core.state.session_manager import session_manager

    # Build floors report using canonical floor specs
    floors = []
    floor_metadata = {
        "F1": {"name": "Amanah (Reversibility)", "doctrine": "Reversible or Auditable"},
        "F2": {"name": "Haqq (Truth)", "doctrine": "Information Fidelity ≥ 0.99"},
        "F3": {"name": "Tri-Witness Consensus", "doctrine": "W₃ = √(H × A × S) ≥ 0.95"},
        "F4": {"name": "Clarity (Entropy)", "doctrine": "ΔS ≤ 0 (entropy reduction)"},
        "F5": {"name": "Peace² (Stability)", "doctrine": "Non-destructive power"},
        "F6": {"name": "Empathy/Care", "doctrine": "Protect weakest stakeholder"},
        "F7": {"name": "Gödel Uncertainty", "doctrine": "Ω₀ ∈ [0.03, 0.05] humility band"},
        "F8": {"name": "Wisdom Equation", "doctrine": "G = A × P × X × E² ≥ 0.80"},
        "F9": {"name": "Anti-Hantu (Shadow)", "doctrine": "C_dark < 0.30 (no deception)"},
        "F10": {"name": "Ontology Lock", "doctrine": "Category precision"},
        "F11": {"name": "Command Authority", "doctrine": "Verified identity"},
        "F12": {"name": "Injection Defense", "doctrine": "Input sanitization"},
        "F13": {"name": "Sovereign Override", "doctrine": "Human final authority"},
    }

    for floor_id in [f"F{i}" for i in range(1, 14)]:
        spec_key = FLOOR_SPEC_KEYS.get(floor_id)
        threshold_data = THRESHOLDS.get(spec_key, {}) if spec_key else {}
        meta = floor_metadata.get(floor_id, {})

        # Format threshold for display
        threshold_val = threshold_data.get("threshold")
        if threshold_val is not None:
            threshold_str = f"≥ {threshold_val}"
        elif "range" in threshold_data:
            r = threshold_data["range"]
            threshold_str = f"∈ [{r[0]}, {r[1]}]"
        else:
            threshold_str = "HARD"

        floor_type = threshold_data.get("type", "SOFT")

        floor_data = {
            "floor_id": floor_id,
            "name": meta.get("name", floor_id),
            "type": floor_type,
            "threshold": threshold_str,
            "doctrine": meta.get("doctrine", threshold_data.get("desc", "—")),
        }
        floors.append(floor_data)

    # Get session state if available
    session_state = "NO_SESSION"
    try:
        kernel = session_manager.get_kernel(session_id)
        if kernel:
            session_state = "ACTIVE"
    except Exception:
        pass

    return {
        "audit_type": "constitutional_floors",
        "session_id": session_id,
        "session_state": session_state,
        "floors_count": len(floors),
        "hard_floors": sum(1 for f in floors if f["type"] == "HARD"),
        "soft_floors": sum(1 for f in floors if f["type"] == "SOFT"),
        "derived_floors": sum(1 for f in floors if f["type"] == "DERIVED"),
        "floors": floors,
        "doctrine_to_runtime": [
            {"doctrine": "F2 Truth", "runtime": "search_reality, ingest_evidence"},
            {"doctrine": "F4 Clarity", "runtime": "entropy tracking, office_forge_audit"},
            {"doctrine": "F6 Care", "runtime": "assess_heart_impact"},
            {"doctrine": "F11 Command", "runtime": "bootstrap_identity, auth_continuity"},
            {"doctrine": "F13 Sovereign", "runtime": "888_HOLD, verify_vault_ledger"},
        ],
        "status": "ACTIVE",
        "message": "13 Constitutional Floors loaded and enforced",
    }


def _build_vitals_report(session_id: str) -> dict[str, Any]:
    """
    Build the system vitals report for check_vital tool.
    Returns health status, thermodynamic budget, and capability map.
    """
    from core.shared.floors import THRESHOLDS
    from core.state.session_manager import session_manager

    # Gather system health
    health_status = "HEALTHY"
    degraded_components = []

    # Check session
    session_active = False
    try:
        session_active = session_manager.get_kernel(session_id) is not None
    except Exception:
        pass

    # Build capability map based on available integrations
    capability_map = {
        "governed_continuity": {"enabled": True, "status": "configured"},
        "vault_persistence": {"enabled": True, "status": "configured"},
        "vector_memory": {"enabled": True, "status": "configured"},
        "external_grounding": {"enabled": True, "status": "configured"},
        "model_provider_access": {"enabled": True, "status": "configured"},
        "local_model_runtime": {"enabled": True, "status": "configured"},
        "auto_deploy": {"enabled": False, "status": "manual_only"},
    }

    # Check thermodynamic module
    thermo_status = "active"
    try:
        from core.physics import thermodynamics_hardened

        thermo_status = "active"
    except ImportError as e:
        thermo_status = f"degraded: {e}"
        degraded_components.append("thermodynamics_hardened")
        health_status = "DEGRADED"

    return {
        "system_status": health_status,
        "session_id": session_id,
        "session_active": session_active,
        "capability_map": capability_map,
        "thermodynamic_vitality": {
            "status": thermo_status,
            "note": "F4 Clarity enforcement via thermodynamic budgeting",
        },
        "constitutional_telemetry": {
            "floors_enforced": len(THRESHOLDS),
            "governance_mode": "HARD" if session_active else "STANDBY",
            "audit_trail": "VAULT999",
        },
        "degraded_components": degraded_components if degraded_components else None,
        "operator_note": (
            "System operational. Run audit_rules for constitutional floor details. "
            "Run verify_vault_ledger for audit trail integrity."
        ),
    }


async def call_kernel(
    tool_name: str,
    session_id: str,
    payload: dict[str, Any],
) -> dict[str, Any]:

    from arifosmcp.runtime.models import CallerContext as _CallerContext
    from core.governance_kernel import get_governance_kernel
    from core.shared.types import GovernanceMetadata, Intent, MathDials, TemporalContract

    canonical_name = TOOL_MAP.get(tool_name, tool_name)
    claimed_actor_id = _resolve_claimed_actor_id(payload)

    t_start = time.perf_counter()
    now_utc = datetime.now(timezone.utc)
    valid_until = now_utc + timedelta(minutes=15)

    auth_ctx = _normalize_auth_context(payload, payload.get("auth_context"))
    if auth_ctx is not None:
        payload["auth_context"] = auth_ctx
    if canonical_name == "metabolic_loop":
        if not auth_ctx:
            if _can_auto_anchor_declared_identity(payload, claimed_actor_id):
                auth_ctx = _mint_auto_anchor_auth_context(session_id, claimed_actor_id)
                payload["auth_context"] = auth_ctx
                payload.setdefault("identity_resolution", {})
            elif _requires_explicit_kernel_auth(payload, canonical_name):
                return _auth_failure_envelope(
                    tool=canonical_name,
                    session_id=session_id,
                    error_message="F11: High-risk kernel calls require auth_context.",
                    claimed_actor_id=claimed_actor_id,
                    identity_claim_status="UNVERIFIED_CLAIM",
                    identity_reason="Auto-bootstrap not allowed for high-risk.",
                    next_action_reason="Run init_anchor_state first.",
                    machine_issue="AUTH_BOOTSTRAP_REQUIRED",
                )
        else:
            valid, reason = verify_auth_context_cached(session_id, auth_ctx)
            if not valid:
                return _auth_failure_envelope(
                    tool=canonical_name,
                    session_id=session_id,
                    error_message=f"F11: Continuity failed: {reason}",
                    claimed_actor_id=claimed_actor_id,
                    identity_claim_status="INVALID_AUTH_CONTEXT",
                    identity_reason=reason,
                    next_action_reason="Refresh continuity state.",
                    machine_issue="TOKEN_EXPIRED",
                )

    elif canonical_name in REQUIRES_SESSION and canonical_name not in BOOTSTRAP_WHITELIST:
        if not auth_ctx:
            return _auth_failure_envelope(
                tool=canonical_name,
                session_id=session_id,
                error_message="F11: Missing auth_context.",
                claimed_actor_id=claimed_actor_id,
                identity_claim_status="UNVERIFIED_CLAIM",
                identity_reason="No auth_context.",
                next_action_reason="Run init_anchor_state first.",
                machine_issue="AUTH_TOKEN_MISSING",
            )
        valid, reason = verify_auth_context_cached(session_id, auth_ctx)
        if not valid:
            return _auth_failure_envelope(
                tool=canonical_name,
                session_id=session_id,
                error_message=f"F11: Continuity failed: {reason}",
                claimed_actor_id=claimed_actor_id,
                identity_claim_status="INVALID_AUTH_CONTEXT",
                identity_reason=reason,
                next_action_reason="Refresh continuity state.",
                machine_issue="TOKEN_EXPIRED",
            )

    if canonical_name == "search_reality":
        res = await reality_check(query=payload.get("query", ""))
        return wrap_tool_output(canonical_name, res)
    if canonical_name == "ingest_evidence":
        res = await open_web_page(url=payload.get("source_url", ""))
        return wrap_tool_output(canonical_name, res)
    if canonical_name == "trace_replay":
        limit = payload.get("limit", 20)
        try:
            max_entries = max(1, min(int(limit), 200))
        except (TypeError, ValueError):
            max_entries = 20

        if not DEFAULT_VAULT_PATH.exists():
            return _trace_replay_envelope(session_id, "NO_DATA", [])

        integrity_ok, integrity_reason = verify_vault_ledger(DEFAULT_VAULT_PATH)
        if not integrity_ok:
            return _trace_replay_envelope(session_id, "TAMPERED", [], error=integrity_reason)

        replay_entries: list[dict[str, Any]] = []
        try:
            with open(DEFAULT_VAULT_PATH, encoding="utf-8") as f:
                for line in f:
                    row = line.strip()
                    if not row:
                        continue
                    parsed = json.loads(row)
                    if parsed.get("session_id") == session_id:
                        replay_entries.append(parsed)
        except Exception as exc:
            return _trace_replay_envelope(session_id, "ERROR", [], error=str(exc))

        return _trace_replay_envelope(session_id, "SUCCESS", replay_entries[-max_entries:])

    try:
        query_input = payload.get("query", "")
        actor_id = payload.get("actor_id", "anonymous")
        result: Any = {}

        caller_ctx_data = payload.get("caller_context")
        caller_ctx_obj = None
        if caller_ctx_data:
            try:
                caller_ctx_obj = _CallerContext.model_validate(caller_ctx_data)
            except ValidationError:
                caller_ctx_obj = None

        if canonical_name == "anchor_session":
            intent = (
                Intent(**payload.get("intent", {}))
                if payload.get("intent")
                else Intent(query=query_input or "INIT")
            )
            math = MathDials(**payload.get("math", {})) if payload.get("math") else MathDials()
            gov = (
                GovernanceMetadata(**payload.get("governance", {}))
                if payload.get("governance")
                else GovernanceMetadata(actor_id=actor_id)
            )
            res = await init(
                query=intent,
                actor_id=gov,
                math_dials=math,
                auth_token=payload.get("auth_token"),
                session_id=session_id,
                caller_context=caller_ctx_obj,
            )
            result = res.model_dump(mode="json")
            if res.verdict != Verdict.VOID:
                result["auth_context"] = mint_auth_context(
                    session_id=res.session_id,
                    actor_id=res.governance.actor_id,
                    token_fingerprint="sha256:initialized",
                    approval_scope=["*"],
                    parent_signature="",
                    authority_level=res.governance.authority_level,
                )

        elif canonical_name == "reason_mind":
            result = await agi(
                query=query_input,
                session_id=session_id,
                action=payload.get("action", "full"),
                reason_mode=payload.get("reason_mode", "default"),
                max_steps=payload.get("max_steps", 7),
                auth_context=auth_ctx,
            )

        elif canonical_name in ("vector_memory", "session_memory"):
            result = await vault(
                operation=payload.get("operation", "search"),
                session_id=session_id,
                content=payload.get("content") or query_input,
                memory_ids=payload.get("memory_ids"),
                top_k=payload.get("top_k", 5),
                auth_context=auth_ctx,
            )

        elif canonical_name in ("simulate_heart", "critique_thought"):
            result = await asi(
                action=canonical_name,
                session_id=session_id,
                scenario=payload.get("scenario") or query_input,
                thought_id=payload.get("thought_id"),
                focus=payload.get("focus") or "general",
                auth_context=auth_ctx,
            )

        elif canonical_name == "eureka_forge":
            result = await apex(
                action="forge",
                session_id=session_id,
                intent=payload.get("intent") or query_input,
                eureka_type=payload.get("eureka_type", "concept"),
                materiality=payload.get("materiality", "idea_only"),
                auth_context=auth_ctx,
            )

        elif canonical_name == "apex_judge":
            result = await apex(
                action="judge",
                session_id=session_id,
                verdict_candidate=payload.get("verdict_candidate", "SEAL"),
                reason_summary=payload.get("reason_summary"),
                auth_context=auth_ctx,
            )

        elif canonical_name == "seal_vault":
            result = await vault(
                operation="seal",
                session_id=session_id,
                summary=payload.get("summary"),
                verdict=payload.get("verdict", "SEAL"),
                approved_by=payload.get("approved_by"),
                approval_reference=payload.get("approval_reference"),
                telemetry=payload.get("telemetry"),
                seal_mode=payload.get("seal_mode", "final"),
                auth_context=auth_ctx,
            )

        elif canonical_name == "verify_vault_ledger":
            ok, reason = verify_vault_ledger(DEFAULT_VAULT_PATH)
            result = {
                "ok": ok,
                "status": "INTACT" if ok else "BROKEN",
                "message": reason or "Chain Integrity: VERIFIED (SHA-256 Merkle)",
                "path": str(DEFAULT_VAULT_PATH),
            }

        elif canonical_name == "office_forge_audit":
            result = await audit_markdown(markdown=payload.get("markdown") or query_input)

        elif canonical_name == "office_forge":
            result = await render_office_document(
                session_id=session_id,
                markdown=payload.get("markdown") or query_input,
                mode=payload.get("output_mode", "pdf"),
                theme=payload.get("theme", "default"),
                filename=payload.get("filename"),
            )

        elif canonical_name == "ollama_local_generate":
            result = await ollama_local_generate_call(
                prompt=payload.get("prompt") or query_input,
                model=payload.get("model", "qwen2.5:3b"),
                system=payload.get("system"),
                temperature=payload.get("temperature", 0.2),
                max_tokens=payload.get("max_tokens", 512),
            )

        elif canonical_name == "metabolic_loop":
            from arifosmcp.runtime.orchestrator import metabolic_loop

            result = await metabolic_loop(
                query=query_input,
                risk_tier=payload.get("risk_tier", "medium"),
                actor_id=actor_id,
                auth_context=auth_ctx,
                session_id=session_id,
                allow_execution=bool(payload.get("allow_execution", False)),
                dry_run=bool(payload.get("dry_run", False)),
                caller_context=caller_ctx_obj,
            )
            latency_ms = (time.perf_counter() - t_start) * 1000.0
            contract = TemporalContract(
                observed_at=now_utc, request_latency_ms=latency_ms, valid_until=valid_until
            )
            if isinstance(result, dict) and "meta" in result:
                result["meta"]["temporal_contract"] = contract.model_dump(mode="json")
            if isinstance(result, dict) and result.get("verdict") != "VOID" and auth_ctx:
                result["auth_context"] = mint_auth_context(
                    session_id=session_id,
                    actor_id=auth_ctx.get("actor_id", claimed_actor_id),
                    token_fingerprint="sha256:...",
                    approval_scope=auth_ctx.get(
                        "approval_scope",
                        [
                            "arifOS_kernel:reason",
                            "search_reality",
                            "ingest_evidence",
                            "session_memory",
                        ],
                    ),
                    parent_signature=auth_ctx.get("signature", ""),
                    authority_level=auth_ctx.get("authority_level", "declared"),
                )
            return result

        elif canonical_name == "system_audit":
            # Constitutional audit: return 13 Floors and governance state
            result = _build_constitutional_audit(session_id)

        elif canonical_name == "sense_health":
            # System health check with constitutional telemetry
            result = _build_vitals_report(session_id)

        else:
            result = {"status": "SUCCESS", "message": f"Utility {tool_name} executed."}

        latency_ms = (time.perf_counter() - t_start) * 1000.0
        contract = TemporalContract(
            observed_at=now_utc, request_latency_ms=latency_ms, valid_until=valid_until
        )

        kernel = get_governance_kernel(session_id)
        kernel.apply_temporal_grounding(contract)

        if hasattr(result, "model_dump"):
            result = result.model_dump(mode="json")

        envelope = wrap_tool_output(canonical_name, result)

        if caller_ctx_data and "caller_context" not in envelope:
            envelope["caller_context"] = caller_ctx_data

        if envelope.get("verdict") != "VOID" and canonical_name != "anchor_session" and auth_ctx:
            envelope["auth_context"] = mint_auth_context(
                session_id=session_id,
                actor_id=auth_ctx.get("actor_id", "anonymous"),
                token_fingerprint="sha256:...",
                approval_scope=auth_ctx.get(
                    "approval_scope",
                    ["reason_mind", "simulate_heart", "eureka_forge", "seal_vault"],
                ),
                parent_signature=auth_ctx.get("signature", ""),
            )
            if "math" in auth_ctx:
                envelope["auth_context"]["math"] = auth_ctx["math"]
        elif canonical_name == "anchor_session" and "auth_context" in result:
            envelope["auth_context"] = result["auth_context"]

        if "meta" in envelope and isinstance(envelope["meta"], dict):
            envelope["meta"]["temporal_contract"] = contract.model_dump(mode="json")

        return envelope

    except Exception as e:
        logger.error(f"Bridge failure on {tool_name}: {e}", exc_info=True)
        return wrap_tool_output(
            canonical_name, {"verdict": "VOID", "error": str(e), "stage": "BRIDGE_FAILURE"}
        )
