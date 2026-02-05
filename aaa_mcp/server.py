"""
FastMCP Migration — Clean Implementation
Uses engine adapters to bridge to existing codebase
"""

from typing import Optional

from fastmcp import FastMCP

from aaa_mcp.constitutional_decorator import constitutional_floor, get_tool_floors
from aaa_mcp.engine_adapters import AGIEngine, APEXEngine, ASIEngine, InitEngine
from aaa_mcp.services.constitutional_metrics import store_stage_result
from aaa_mcp.tools.reality_grounding import reality_check

mcp = FastMCP("aaa-mcp")


# Tool implementations using adapters
@constitutional_floor("F11", "F12")
@mcp.tool()
async def init_gate(query: str, session_id: Optional[str] = None) -> dict:
    """Initialize constitutional session"""
    engine = InitEngine()
    result = await engine.ignite(query, session_id)
    store_stage_result(result.get("session_id", session_id or "unknown"), "init", result)
    result["verdict"] = result.get("verdict", "SEAL")
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["seal"] = result.get("seal", "💎🔥🧠")
    result["floors_enforced"] = get_tool_floors("init_gate")
    result["pass"] = "forward"
    return result


@constitutional_floor("F2", "F4")
@mcp.tool()
async def agi_sense(query: str, session_id: str) -> dict:
    engine = AGIEngine()
    result = await engine.sense(query, session_id)
    store_stage_result(session_id, "agi", result)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("agi_sense")
    result["pass"] = "forward"
    return result


@constitutional_floor("F2", "F4", "F7")
@mcp.tool()
async def agi_think(query: str, session_id: str) -> dict:
    engine = AGIEngine()
    result = await engine.think(query, session_id)
    store_stage_result(session_id, "agi", result)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("agi_think")
    result["pass"] = "forward"
    return result


@constitutional_floor("F2", "F4", "F7")
@mcp.tool()
async def agi_reason(query: str, session_id: str) -> dict:
    engine = AGIEngine()
    result = await engine.reason(query, session_id)
    store_stage_result(session_id, "agi", result)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("agi_reason")
    result["pass"] = "forward"
    return result


@constitutional_floor("F5", "F6")
@mcp.tool()
async def asi_empathize(query: str, session_id: str) -> dict:
    engine = ASIEngine()
    result = await engine.empathize(query, session_id)
    store_stage_result(session_id, "asi", result)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("asi_empathize")
    result["pass"] = "forward"
    return result


@constitutional_floor("F5", "F6", "F9")
@mcp.tool()
async def asi_align(query: str, session_id: str) -> dict:
    engine = ASIEngine()
    result = await engine.align(query, session_id)
    store_stage_result(session_id, "asi", result)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("asi_align")
    result["pass"] = "forward"
    return result


@constitutional_floor("F3", "F8")
@mcp.tool()
async def apex_verdict(query: str, session_id: str) -> dict:
    engine = APEXEngine()
    result = await engine.judge(query, session_id)
    store_stage_result(session_id, "apex", result)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("apex_verdict")
    result["pass"] = "reverse"
    return result


@constitutional_floor("F2", "F7")
@mcp.tool()
async def reality_search(query: str, session_id: str) -> dict:
    # Reality search using external fact verification
    result = await reality_check(query)
    result["session_id"] = session_id
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("reality_search")
    result["pass"] = "reverse"
    return result


@constitutional_floor("F1", "F3")
@mcp.tool()
async def vault_seal(session_id: str, verdict: str, payload: dict) -> dict:
    from codebase.vault.persistence import get_ledger

    ledger = get_ledger()
    await ledger.connect()
    try:
        result = await ledger.append(session_id, verdict, payload)
        return {
            "verdict": "SEALED",
            "seal": result["seal"],
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "floors_enforced": get_tool_floors("vault_seal"),
            "pass": "reverse",
        }
    finally:
        await ledger.close()


if __name__ == "__main__":
    print("🔥 arifOS Constitutional Kernel — FastMCP Mode")
    mcp.run(transport="sse", port=6274)
