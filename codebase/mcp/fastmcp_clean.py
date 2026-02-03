"""
FastMCP Migration — Clean Implementation
Uses engine adapters to bridge to existing codebase
"""
from fastmcp import FastMCP
from typing import Optional

from codebase.mcp.constitutional_decorator import constitutional_floor, get_tool_floors
from codebase.mcp.engine_adapters import (
    InitEngine, AGIEngine, ASIEngine, APEXEngine
)

mcp = FastMCP("arifos-constitutional-kernel")

# Tool implementations using adapters
@constitutional_floor("F11", "F12")
@mcp.tool()
async def init_gate(query: str, session_id: Optional[str] = None) -> dict:
    """Initialize constitutional session"""
    engine = InitEngine()
    result = await engine.ignite(query, session_id)
    result["verdict"] = result.get("verdict", "SEAL")
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["seal"] = result.get("seal", "💎🔥🧠")
    result["floors_enforced"] = get_tool_floors("init_gate")
    return result

@constitutional_floor("F2", "F4")
@mcp.tool()
async def agi_sense(query: str, session_id: str) -> dict:
    engine = AGIEngine()
    result = await engine.sense(query, session_id)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("agi_sense")
    return result

@constitutional_floor("F2", "F4", "F7")
@mcp.tool()
async def agi_think(query: str, session_id: str) -> dict:
    engine = AGIEngine()
    result = await engine.think(query, session_id)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("agi_think")
    return result

@constitutional_floor("F2", "F4", "F7")
@mcp.tool()
async def agi_reason(query: str, session_id: str) -> dict:
    engine = AGIEngine()
    result = await engine.reason(query, session_id)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("agi_reason")
    return result

@constitutional_floor("F5", "F6")
@mcp.tool()
async def asi_empathize(query: str, session_id: str) -> dict:
    engine = ASIEngine()
    result = await engine.empathize(query, session_id)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("asi_empathize")
    return result

@constitutional_floor("F5", "F6", "F9")
@mcp.tool()
async def asi_align(query: str, session_id: str) -> dict:
    engine = ASIEngine()
    result = await engine.align(query, session_id)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("asi_align")
    return result

@constitutional_floor("F3", "F8")
@mcp.tool()
async def apex_verdict(query: str, session_id: str) -> dict:
    engine = APEXEngine()
    result = await engine.judge(query, session_id)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("apex_verdict")
    return result

@constitutional_floor("F2", "F7")
@mcp.tool()
async def reality_search(query: str, session_id: str) -> dict:
    from mcp_server.core.bridge import bridge_reality_check_router
    result = await bridge_reality_check_router(query, session_id)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("reality_search")
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
            "floors_enforced": get_tool_floors("vault_seal")
        }
    finally:
        await ledger.close()

if __name__ == "__main__":
    print("🔥 arifOS Constitutional Kernel — FastMCP Mode")
    mcp.run(transport="sse", port=6274)
