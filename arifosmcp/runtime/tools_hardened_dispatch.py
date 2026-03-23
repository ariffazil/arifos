"""
arifosmcp/runtime/tools_hardened_dispatch.py — Dispatcher for Hardened Tools

This module acts as the integration layer between the main FastMCP server
and the hardened tool implementations, now governed by the Substrate Policy.
"""

from __future__ import annotations
import asyncio
from typing import Any, Callable
from fastmcp.dependencies import CurrentContext

from arifosmcp.runtime.contracts_v2 import ToolEnvelope, ToolStatus, RiskTier
from arifosmcp.runtime.init_anchor_hardened import HardenedInitAnchor, SessionClass
from arifosmcp.runtime.truth_pipeline_hardened import HardenedRealityCompass, HardenedRealityAtlas
from arifosmcp.runtime.tools_hardened_v2 import (
    HardenedAGIReason,
    HardenedASICritique,
    HardenedAgentZeroEngineer,
    HardenedApexJudge,
    HardenedVaultSeal,
)
from arifosmcp.runtime.substrate_policy import get_policy

# Initialize hardened tool instances
init_anchor_tool = HardenedInitAnchor()
reality_compass_tool = HardenedRealityCompass()
reality_atlas_tool = HardenedRealityAtlas()
agi_reason_tool = HardenedAGIReason()
asi_critique_tool = HardenedASICritique()
agentzero_engineer_tool = HardenedAgentZeroEngineer()
apex_judge_tool = HardenedApexJudge()
vault_seal_tool = HardenedVaultSeal()

def _apply_policy(envelope_dict: dict[str, Any], tool: str, mode: str) -> dict[str, Any]:
    """Inject substrate policy metadata into the tool response."""
    policy = get_policy(tool, mode)
    if policy:
        envelope_dict["substrate_class"] = policy.substrate
        envelope_dict["risk_tier"] = policy.risk
        envelope_dict["organ_stage"] = policy.organ_stage
        
        # Automatic 888_HOLD injection for high-risk substrate classes
        if policy.risk == "high" and envelope_dict.get("verdict") != "VOID":
            envelope_dict["verdict"] = "888_HOLD"
            envelope_dict["note"] = f"Sovereign approval required for {policy.substrate} operation."
            
    return envelope_dict

async def hardened_init_anchor_dispatch(mode: str, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
    if mode == "init":
        raw_input = (
            payload.get("raw_input")
            or payload.get("query")
            or (payload.get("intent", {}).get("query") if isinstance(payload.get("intent"), dict) else None)
        )
        envelope = await init_anchor_tool.init(
            declared_name=payload.get("declared_name") or payload.get("actor_id"),
            actor_id=payload.get("actor_id"),
            intent=payload.get("intent"),
            query=payload.get("query"),
            raw_input=raw_input,
            auth_context=payload.get("auth_context"),
            human_approval=payload.get("human_approval", False),
            proof=payload.get("proof"),
            requested_scope=payload.get("requested_scope"),
            risk_tier=payload.get("risk_tier", "low"),
            session_class=payload.get("session_class", "execute"),
            session_id=payload.get("session_id"),
            caller_context=payload.get("caller_context"),
            pns_shield=payload.get("pns_shield"),
        )
    elif mode in ("state", "status", "refresh"):
        envelope = await init_anchor_tool.state(session_id=payload.get("session_id"))
    elif mode == "revoke":
        envelope = await init_anchor_tool.revoke(
            session_id=payload.get("session_id") or "unknown",
            reason=payload.get("reason", "User requested revocation"),
        )
    else:
        return {"ok": False, "error": f"Invalid mode for init_anchor: {mode}"}
    
    return _apply_policy(envelope.to_dict(), "init_anchor", mode)

async def hardened_physics_reality_dispatch(mode: str, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
    if mode in ("compass", "search", "query"):
        envelope = await reality_compass_tool.ingest(
            query=payload.get("query") or payload.get("input") or payload.get("url"),
            session_id=payload.get("session_id")
        )
    elif mode in ("atlas", "ingest", "map"):
        envelope = await reality_atlas_tool.map_claims(
            session_id=payload.get("session_id"),
            evidence_bundles=payload.get("evidence_bundles", [])
        )
    elif mode == "time":
        from datetime import datetime, timezone, timedelta
        now_utc = datetime.now(timezone.utc)
        kl_offset = timezone(timedelta(hours=8))
        now_kl = now_utc.astimezone(kl_offset)
        res = {
            "ok": True,
            "tool": "physics_reality",
            "stage": "111_SENSE",
            "temporal": {
                "utc_iso": now_utc.isoformat(),
                "kl_iso": now_kl.isoformat(),
                "kl_timezone": "Asia/Kuala_Lumpur (UTC+08:00)",
                "day_of_week": now_utc.strftime("%A"),
            },
            "sovereignty_epoch": "888",
        }
        return _apply_policy(res, "physics_reality", mode)
    else:
        return {"ok": False, "error": f"Invalid mode for physics_reality: {mode}"}
    
    return _apply_policy(envelope.to_dict(), "physics_reality", mode)

async def hardened_agi_mind_dispatch(mode: str, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
    if mode in ("reason", "reflect", "forge"):
        envelope = await agi_reason_tool.reason(
            query=payload.get("query") or payload.get("prompt"),
            session_id=payload.get("session_id")
        )
    else:
        return {"ok": False, "error": f"Invalid mode for agi_mind: {mode}"}
    
    return _apply_policy(envelope.to_dict(), "agi_mind", mode)

async def hardened_asi_heart_dispatch(mode: str, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
    if mode in ("critique", "simulate", "align"):
        envelope = await asi_critique_tool.critique(
            proposal=payload.get("proposal") or payload.get("content") or payload.get("draft_output"),
            session_id=payload.get("session_id")
        )
    else:
        return {"ok": False, "error": f"Invalid mode for asi_heart: {mode}"}
    
    return _apply_policy(envelope.to_dict(), "asi_heart", mode)

async def hardened_engineering_memory_dispatch(mode: str, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
    if mode in ("engineer", "query", "generate"):
        envelope = await agentzero_engineer_tool.plan_execution(
            task=payload.get("task") or payload.get("query"),
            action_class=payload.get("action_class", "read"),
            session_id=payload.get("session_id")
        )
    elif mode in ("vector_query", "vector_store"):
        envelope = await agentzero_engineer_tool.plan_execution(
            task=payload.get("query") or payload.get("content"),
            action_class="read" if "query" in mode else "write",
            session_id=payload.get("session_id")
        )
    else:
        return {"ok": False, "error": f"Invalid mode for engineering_memory: {mode}"}
    
    return _apply_policy(envelope.to_dict(), "engineering_memory", mode)

async def hardened_apex_soul_dispatch(mode: str, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
    if mode in ("judge", "validate", "hold", "armor", "rules"):
        envelope = await apex_judge_tool.judge(
            proposal=payload.get("proposal") or payload.get("candidate") or payload.get("input_to_validate"),
            execution_plan=payload.get("execution_plan"),
            session_id=payload.get("session_id")
        )
    else:
        return {"ok": False, "error": f"Invalid mode for apex_soul: {mode}"}
    
    return _apply_policy(envelope.to_dict(), "apex_soul", mode)

async def hardened_vault_ledger_dispatch(mode: str, payload: dict[str, Any], **kwargs) -> dict[str, Any]:
    if mode in ("seal", "verify"):
        envelope = await vault_seal_tool.seal(
            decision=payload.get("decision") or {"verdict": payload.get("verdict"), "evidence": payload.get("evidence")},
            session_id=payload.get("session_id"),
            seal_class=payload.get("seal_class", "operational")
        )
    else:
        return {"ok": False, "error": f"Invalid mode for vault_ledger: {mode}"}
    
    return _apply_policy(envelope.to_dict(), "vault_ledger", mode)

HARDENED_DISPATCH_MAP = {
    "init_anchor": hardened_init_anchor_dispatch,
    "physics_reality": hardened_physics_reality_dispatch,
    "agi_mind": hardened_agi_mind_dispatch,
    "asi_heart": hardened_asi_heart_dispatch,
    "engineering_memory": hardened_engineering_memory_dispatch,
    "apex_soul": hardened_apex_soul_dispatch,
    "vault_ledger": hardened_vault_ledger_dispatch,
}
