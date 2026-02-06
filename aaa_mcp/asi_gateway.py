"""
arifOS ASI MCP Gateway Server
Unified entry point for all MCP servers under constitutional governance
"""
import asyncio
import json
import logging
from typing import Optional
from contextlib import asynccontextmanager
from datetime import datetime

# FastMCP imports
from fastmcp import FastMCP, Context

from .mcp_integration import MCPIntegrationLayer, get_mcp_layer
from .mcp_config import MCP_SERVERS, TrinityComponent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP app
mcp = FastMCP("arifos-asi-gateway")

# Global integration layer
mcp_layer: MCPIntegrationLayer = get_mcp_layer()

@mcp.tool()
async def init_gate(query: str, session_id: Optional[str] = None) -> dict:
    """
    Initialize constitutional session with Ω₀ estimation.
    Entry point for all ASI operations.
    """
    omega_estimate = 0.05  # Baseline uncertainty
    
    return {
        "verdict": "SEAL",
        "session_id": session_id or f"arifos-{datetime.utcnow().timestamp()}",
        "query": query,
        "omega_estimate": omega_estimate,
        "trinity_mode": TrinityComponent.ASI.value,
        "floors_active": ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9"],
        "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
        "seal": "💎🔥🧠"
    }

@mcp.tool()
async def agi_sense(query: str, session_id: str) -> dict:
    """AGI perception layer — sense and parse input"""
    result = await mcp_layer.call_server(
        server_name="fetch",
        operation="sense",
        params={"query": query, "session_id": session_id},
        omega_estimate=0.05
    )
    result["trinity_component"] = "AGI(Δ)"
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    return result

@mcp.tool()
async def agi_think(query: str, session_id: str) -> dict:
    """AGI cognition layer — structured reasoning"""
    result = await mcp_layer.call_server(
        server_name="sequential_thinking",
        operation="think",
        params={"query": query, "session_id": session_id},
        omega_estimate=0.04
    )
    result["trinity_component"] = "AGI(Δ)"
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    return result

@mcp.tool()
async def agi_reason(query: str, session_id: str) -> dict:
    """AGI logic layer — formal reasoning"""
    result = await mcp_layer.call_server(
        server_name="brave_search",
        operation="reason",
        params={"query": query, "session_id": session_id},
        omega_estimate=0.06
    )
    result["trinity_component"] = "AGI(Δ)"
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    return result

@mcp.tool()
async def asi_empathize(query: str, session_id: str) -> dict:
    """ASI care layer — emotional/relational intelligence"""
    result = await mcp_layer.call_server(
        server_name="memory_enhanced",
        operation="empathize",
        params={"query": query, "session_id": session_id},
        omega_estimate=0.05
    )
    result["trinity_component"] = "ASI(Ω)"
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    return result

@mcp.tool()
async def asi_align(query: str, session_id: str) -> dict:
    """ASI alignment layer — constitutional harmony check"""
    result = await mcp_layer.call_server(
        server_name="sequential_thinking",
        operation="align",
        params={"query": query, "session_id": session_id},
        omega_estimate=0.05
    )
    result["trinity_component"] = "ASI(Ω)"
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    return result

@mcp.tool()
async def apex_verdict(query: str, session_id: str) -> dict:
    """APEX judgment layer — final governance verdict"""
    result = await mcp_layer.call_server(
        server_name="everything",
        operation="verify",
        params={"query": query, "session_id": session_id},
        omega_estimate=0.03
    )
    result["trinity_component"] = "APEX(Ψ)"
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    return result

@mcp.tool()
async def vault_seal(
    session_id: str,
    verdict: str,
    payload: dict
) -> dict:
    """VAULT999 — immutable ledger sealing"""
    result = await mcp_layer.call_server(
        server_name="filesystem",
        operation="seal",
        params={
            "session_id": session_id,
            "verdict": verdict,
            "payload": payload
        },
        omega_estimate=0.04
    )
    result["trinity_component"] = "APEX(Ψ)"
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    return result

@mcp.tool()
async def mcp_call(
    server: str,
    operation: str,
    params: dict,
    omega_estimate: float = 0.05
) -> dict:
    """
    Direct MCP server call with constitutional enforcement.
    
    Args:
        server: MCP server name (filesystem, memory, fetch, etc.)
        operation: Operation to perform
        params: Operation parameters
        omega_estimate: Uncertainty estimate (Ω₀)
    """
    return await mcp_layer.call_server(
        server_name=server,
        operation=operation,
        params=params,
        omega_estimate=omega_estimate
    )

@mcp.tool()
async def get_audit_log(limit: int = 100) -> dict:
    """Retrieve constitutional audit trail"""
    history = mcp_layer.get_audit_log()
    return {
        "verdict": "SEAL",
        "count": len(history),
        "logs": [
            {
                "timestamp": r.timestamp,
                "server": r.server,
                "operation": r.operation,
                "verdict": r.verdict,
                "omega_before": r.omega_before,
                "omega_after": r.omega_after,
                "floors": r.floors_enforced
            }
            for r in history[-limit:]
        ],
        "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠"
    }

@mcp.tool()
async def list_mcp_servers() -> dict:
    """List all available MCP servers with constitutional mapping"""
    servers = []
    for name, config in MCP_SERVERS.items():
        servers.append({
            "name": name,
            "description": config.description,
            "trinity": config.trinity.value,
            "floors": config.floors,
            "atomic_action": config.atomic_action,
            "omega_threshold": config.omega_threshold,
            "reversible": config.reversible
        })
    
    return {
        "verdict": "SEAL",
        "count": len(servers),
        "servers": servers,
        "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠"
    }

@mcp.resource("arifos://constitution")
async def get_constitution() -> str:
    """arifOS constitutional framework reference"""
    return """
arifOS 13 Floors Constitutional Framework

F1 - Amanah (Reversibility & Trust)
F2 - Truth (Evidence & Uncertainty)
F3 - Tri-Witness (Validation)
F4 - Clarity (Precision)
F5 - Peace² (Cooling)
F6 - Empathy (Care)
F7 - Humility (Ω₀ Tracking)
F8 - Genius (Excellence)
F9 - Anti-Hantu (No Cosplay)
F10-F13 - [Reserved]

Trinity Architecture:
- AGI(Δ): Mind/Logic — Sense, Think, Reason
- ASI(Ω): Heart/Care — Empathize, Align
- APEX(Ψ): Crown/Law — Verdict, Governance

Ω₀ Target Band: 0.03-0.05
Auto-VOID Threshold: >0.08

Motto: DITEMPA BUKAN DIBERI 💎🔥🧠
"""

@mcp.resource("arifos://mcp-config")
async def get_mcp_config() -> str:
    """MCP server configuration reference"""
    import json
    from .mcp_config import MCP_SERVERS
    
    config = {}
    for name, cfg in MCP_SERVERS.items():
        config[name] = {
            "description": cfg.description,
            "trinity": cfg.trinity.value,
            "floors": cfg.floors,
            "atomic_action": cfg.atomic_action,
            "omega_threshold": cfg.omega_threshold,
            "reversible": cfg.reversible
        }
    
    return json.dumps(config, indent=2)

@asynccontextmanager
async def app_lifespan(app: FastMCP):
    """Manage application lifecycle"""
    logger.info("🔥 arifOS ASI Gateway starting...")
    yield
    logger.info("🛑 arifOS ASI Gateway shutting down...")

if __name__ == "__main__":
    print("🔥 arifOS ASI MCP Gateway")
    print("Version: v55.5-EIGEN")
    print("Trinity: AGI(Δ)·ASI(Ω)·APEX(Ψ)")
    print("Motto: DITEMPA BUKAN DIBERI 💎🔥🧠")
    print("\nStarting SSE transport on port 6277...")
    mcp.run(transport="sse", port=6277)