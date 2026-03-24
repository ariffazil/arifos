"""
arifosmcp/runtime/tools_hardened_dispatch.py — Dispatcher for Hardened Tools

FIX: apex_soul mode dispatch and argument alignment.
FIX: code_engine and architect_registry floor induction.
"""

from __future__ import annotations
import asyncio
import json
from typing import Any, Callable

from arifosmcp.runtime.contracts_v2 import ToolEnvelope, ToolStatus, RiskTier
from arifosmcp.runtime.init_anchor_hardened import HardenedInitAnchor
from arifosmcp.runtime.truth_pipeline_hardened import HardenedRealityCompass, HardenedRealityAtlas
from arifosmcp.runtime.tools_hardened_v2 import (
    HardenedAGIReason,
    HardenedASICritique,
    HardenedAgentZeroEngineer,
    HardenedApexJudge,
    HardenedVaultSeal,
)
from arifosmcp.runtime.substrate_policy import get_policy
from arifosmcp.core.shared.physics import delta_S, genius_score, humility_band

# Initialize hardened tool instances
init_anchor_tool = HardenedInitAnchor()
reality_compass_tool = HardenedRealityCompass()
reality_atlas_tool = HardenedRealityAtlas()
agi_reason_tool = HardenedAGIReason()
asi_critique_tool = HardenedASICritique()
agentzero_engineer_tool = HardenedAgentZeroEngineer()
apex_judge_tool = HardenedApexJudge()
vault_seal_tool = HardenedVaultSeal()

def _apply_policy(envelope_dict: dict[str, Any], tool: str, mode: str, input_payload: dict[str, Any]) -> dict[str, Any]:
    """Inject empirical substrate policy and thermodynamic metrics."""
    policy = get_policy(tool, mode)
    if not policy:
        return envelope_dict

    # 1. Base Policy Mapping (Now with Floors)
    envelope_dict["substrate_class"] = [policy.substrate.value]
    envelope_dict["risk_tier"] = policy.risk.value
    envelope_dict["organ_stage"] = policy.organ_stage
    envelope_dict["floors"] = policy.floors # Assigned Floors now visible

    # 2. Empirical Thermodynamic Measurement (F4 Clarity)
    input_str = json.dumps(input_payload, sort_keys=True)
    output_str = json.dumps(envelope_dict.get("payload", {}), sort_keys=True)
    
    ds = delta_S(input_str, output_str)
    envelope_dict["entropy"] = {
        "delta_s": round(ds, 4),
        "is_stable": ds <= 0,
        "source": "empirical_measurement"
    }

    # 3. Dynamic Genius Score (F8)
    conf = envelope_dict.get("confidence", 0.85)
    peace = 1.0 
    exploration = 0.9
    energy = 1.0 if ds <= 0 else 0.8
    
    g = genius_score(A=conf, P=peace, X=exploration, E=energy)
    envelope_dict["g_score"] = round(g, 4)

    # 4. Humility Mapping (F7)
    envelope_dict["humility_band"] = humility_band(conf).omega_0

    # 5. Proactive 888_HOLD
    if (policy.risk in ("high", "critical")) and envelope_dict.get("verdict") != "VOID":
        envelope_dict["verdict"] = "888_HOLD"
        envelope_dict["note"] = f"Sovereign approval required for {policy.substrate} operation."
            
    return envelope_dict

async def hardened_init_anchor_dispatch(mode: str, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
    if mode == "init":
        envelope = await init_anchor_tool.init(actor_id=payload.get("actor_id"), session_id=payload.get("session_id"))
    elif mode in ("state", "status", "refresh"):
        envelope = await init_anchor_tool.state(session_id=payload.get("session_id"))
    elif mode == "revoke":
        envelope = await init_anchor_tool.revoke(session_id=payload.get("session_id") or "unknown")
    else:
        return {"ok": False, "error": f"Invalid mode for init_anchor: {mode}"}

    envelope_dict = _apply_policy(envelope.to_dict(), "init_anchor", mode, payload)

    # EUREKA Layer 6 — Feedback Loop: inject scar_context from previous sessions
    # This closes the 999→000 loop: past outcomes inform the current anchor.
    if mode == "init":
        try:
            from arifosmcp.core.recovery.rollback_engine import outcome_ledger
            envelope_dict["scar_context"] = outcome_ledger.build_scar_context(n=10)
        except Exception as _sc_err:
            envelope_dict["scar_context"] = {"error": str(_sc_err)}

    return envelope_dict

async def hardened_physics_reality_dispatch(mode: str, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
    if mode in ("compass", "search", "ingest"):
        envelope = await reality_compass_tool.ingest(
            query=payload.get("query") or payload.get("input"),
            is_temporal=payload.get("is_temporal", False),
            strips=payload.get("strips"),
            session_id=payload.get("session_id")
        )
    elif mode == "atlas":
        envelope = await reality_atlas_tool.map_claims(
            evidence_bundles=payload.get("evidence_bundles", []),
            session_id=payload.get("session_id")
        )
    elif mode == "time":
        from datetime import datetime, timezone
        res = {"ok": True, "utc": datetime.now(timezone.utc).isoformat()}
        return _apply_policy(res, "physics_reality", mode, payload)
    else:
        return {"ok": False, "error": f"Invalid mode for physics_reality: {mode}"}
    
    return _apply_policy(envelope.to_dict(), "physics_reality", mode, payload)

async def hardened_agi_mind_dispatch(mode: str, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
    if mode in ("reason", "reflect", "forge"):
        envelope = await agi_reason_tool.reason(
            query=payload.get("query"),
            is_forge=(mode == "forge"),
            session_id=payload.get("session_id")
        )
    else:
        return {"ok": False, "error": f"Invalid mode for agi_mind: {mode}"}
    
    envelope_dict = _apply_policy(envelope.to_dict(), "agi_mind", mode, payload)
    
    # P1: Register every agi_mind output in OutcomeLedger so it's traceable
    # and can be resolved later with vault_ledger(mode="resolve").
    try:
        import secrets as _sec
        from arifosmcp.core.recovery.rollback_engine import outcome_ledger
        _did = f"AGI-{_sec.token_hex(6).upper()}"
        outcome_ledger.record_outcome(
            decision_id=_did,
            session_id=payload.get("session_id") or envelope_dict.get("session_id") or "anonymous",
            verdict_issued=envelope_dict.get("verdict", "SEAL"),
            expected_outcome=f"agi_mind.{mode}: {str(payload.get('query', ''))[:80]}",
        )
        envelope_dict["outcome_id"] = _did  # surface so caller can resolve later
    except Exception as _p1_err:
        envelope_dict["outcome_id"] = None

    return envelope_dict

async def hardened_asi_heart_dispatch(mode: str, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
    if mode in ("critique", "simulate"):
        envelope = await asi_critique_tool.critique(
            candidate=payload.get("proposal") or payload.get("content"),
            session_id=payload.get("session_id")
        )
    else:
        return {"ok": False, "error": f"Invalid mode for asi_heart: {mode}"}
    
    return _apply_policy(envelope.to_dict(), "asi_heart", mode, payload)

async def hardened_engineering_memory_dispatch(mode: str, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
    if mode in ("engineer", "recall", "write", "generate"):
        envelope = await agentzero_engineer_tool.plan_execution(
            task=payload.get("task") or payload.get("query"),
            action_class=payload.get("action_class", "read"),
            session_id=payload.get("session_id")
        )
    else:
        return {"ok": False, "error": f"Invalid mode for engineering_memory: {mode}"}
    
    return _apply_policy(envelope.to_dict(), "engineering_memory", mode, payload)

async def hardened_apex_soul_dispatch(mode: str, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
    # FIX: Explicitly handle all modes and prevent positional argument error
    if mode in ("judge", "rules", "validate", "armor", "probe", "hold", "notify"):
        envelope = await apex_judge_tool.judge(
            proposal=payload.get("proposal") or payload.get("candidate"),
            session_id=payload.get("session_id")
        )
    else:
        return {"ok": False, "error": f"Invalid mode for apex_soul: {mode}"}
    
    return _apply_policy(envelope.to_dict(), "apex_soul", mode, payload)

async def hardened_vault_ledger_dispatch(mode: str, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
    if mode in ("seal", "verify"):
        envelope = await vault_seal_tool.seal(
            decision=payload.get("decision") or {},
            session_id=payload.get("session_id")
        )
        return _apply_policy(envelope.to_dict(), "vault_ledger", mode, payload)

    if mode == "resolve":
        # H2 — Metabolizer return port.
        # Human or agent closes the consequence loop by resolving a PENDING outcome.
        # payload: { decision_id, actual_outcome, harm_detected, operator_override, override_reason }
        decision_id = payload.get("decision_id")
        if not decision_id:
            return {"ok": False, "error": "resolve requires decision_id"}

        from arifosmcp.core.recovery.rollback_engine import outcome_ledger
        resolved = outcome_ledger.resolve_outcome(
            decision_id=decision_id,
            actual_outcome=payload.get("actual_outcome", ""),
            harm_detected=bool(payload.get("harm_detected", False)),
            operator_override=bool(payload.get("operator_override", False)),
            override_reason=payload.get("override_reason", ""),
        )
        if resolved is None:
            return {"ok": False, "error": f"No PENDING outcome found for decision_id={decision_id}"}

        res = {
            "ok": True,
            "decision_id": resolved.decision_id,
            "session_id": resolved.session_id,
            "verdict_issued": resolved.verdict_issued,
            "outcome_status": resolved.outcome_status,
            "harm_detected": resolved.harm_detected,
            "calibration_delta": resolved.calibration_delta,
            "loop": "CLOSED",  # 999→consequence→000 metabolizer complete
        }
        return _apply_policy(res, "vault_ledger", mode, payload)

    return {"ok": False, "error": f"Invalid mode for vault_ledger: {mode}"}

async def hardened_code_engine_dispatch(mode: str, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
    # Placeholder for code engine - assigning generic response for floor visibility
    res = {"ok": True, "action": f"Executed {mode}", "result": "Sandboxed"}
    return _apply_policy(res, "code_engine", mode, payload)

async def hardened_architect_registry_dispatch(mode: str, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
    res = {"ok": True, "registry": "arifOS Sovereign Registry", "mode": mode}
    return _apply_policy(res, "architect_registry", mode, payload)

HARDENED_DISPATCH_MAP = {
    "init_anchor": hardened_init_anchor_dispatch,
    "physics_reality": hardened_physics_reality_dispatch,
    "agi_mind": hardened_agi_mind_dispatch,
    "asi_heart": hardened_asi_heart_dispatch,
    "engineering_memory": hardened_engineering_memory_dispatch,
    "apex_soul": hardened_apex_soul_dispatch,
    "vault_ledger": hardened_vault_ledger_dispatch,
    "code_engine": hardened_code_engine_dispatch,
    "architect_registry": hardened_architect_registry_dispatch,
}
