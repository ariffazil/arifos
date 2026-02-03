"""
FastMCP Migration — All 9 Constitutional Tools
Replaces custom SSE transport with FastMCP framework
"""
from fastmcp import FastMCP
from typing import Optional
import asyncio
import importlib

# Import arifOS constitutional components
from codebase.mcp.constitutional_decorator import constitutional_floor, get_tool_floors
from mcp_server.core.session_context import get_current_session_id, set_current_session_id

# Dynamic imports (matching canonical_trinity.py pattern)
def _get_init_engine():
    """Get init engine from mcp_bridge"""
    module = importlib.import_module("codebase.init.000_init.mcp_bridge")
    return module.mcp_000_init

def _get_kernel():
    """Get kernel manager for AGI/ASI/APEX"""
    from codebase.kernel import get_kernel_manager
    return get_kernel_manager()

# Create FastMCP app
mcp = FastMCP("arifos-constitutional-kernel")

# ============================
# 1. init_gate (Session Initialization)
# ============================
@constitutional_floor("F11", "F12")
@mcp.tool()
async def init_gate(
    query: str,
    session_id: Optional[str] = None
) -> dict:
    """
    Initialize constitutional session with F11 authority check and F12 injection guard.
    
    Args:
        query: User input to evaluate
        session_id: Optional session identifier
        
    Returns:
        Session metadata with constitutional seal and APEX scoring
    """
    # Use the actual working init engine
    mcp_000_init = _get_init_engine()
    
    result = await mcp_000_init(
        action="init",
        query=query,
        session_id=session_id
    )
    
    # Add constitutional metadata
    result["verdict"] = result.get("verdict", "SEAL")
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["seal"] = "💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("init_gate")
    
    # Set session context
    if result.get("session_id"):
        set_current_session_id(result["session_id"])
    
    return result

# Helper to get kernel engines
async def _agi_execute(action: str, query: str, session_id: str):
    """Execute AGI engine action"""
    kernel = _get_kernel()
    agi = kernel.get_agi()
    return await agi.execute(action, {"query": query, "session_id": session_id})

async def _asi_execute(action: str, query: str, session_id: str):
    """Execute ASI engine action"""
    kernel = _get_kernel()
    asi = kernel.get_asi()
    return await asi.execute(action, {"query": query, "session_id": session_id})

async def _apex_execute(action: str, query: str, session_id: str):
    """Execute APEX engine action"""
    kernel = _get_kernel()
    apex = kernel.get_apex()
    return await apex.execute(action, {"query": query, "session_id": session_id})

# ============================
# 2. agi_sense (Intent Classification)
# ============================
@constitutional_floor("F2", "F4")
@mcp.tool()
async def agi_sense(
    query: str,
    session_id: str
) -> dict:
    """
    Sense intent and classify into HARD/SOFT/PHATIC lanes.
    Enforces F2 Truth and F4 Clarity.
    """
    result = await _agi_execute("sense", query, session_id)
    
    result["verdict"] = result.get("verdict", "SEAL")
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("agi_sense")
    
    return result

# ============================
# 3. agi_think (Hypothesis Generation)
# ============================
@constitutional_floor("F2", "F4", "F7")
@mcp.tool()
async def agi_think(
    query: str,
    session_id: str
) -> dict:
    """
    Generate hypotheses with pros/cons analysis.
    Enforces F2 Truth, F4 Clarity, F7 Humility.
    """
    result = await _agi_execute("think", query, session_id)
    
    result["verdict"] = result.get("verdict", "SEAL")
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("agi_think")
    
    return result

# ============================
# 4. agi_reason (Deep Reasoning)
# ============================
@constitutional_floor("F2", "F4", "F7")
@mcp.tool()
async def agi_reason(
    query: str,
    session_id: str
) -> dict:
    """
    Perform deep step-by-step reasoning with confidence scoring.
    Enforces F2 Truth, F4 Clarity, F7 Humility.
    """
    result = await _agi_execute("reason", query, session_id)
    
    result["verdict"] = result.get("verdict", "SEAL")
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("agi_reason")
    
    return result

# ============================
# 5. asi_empathize (Stakeholder Analysis)
# ============================
@constitutional_floor("F5", "F6")
@mcp.tool()
async def asi_empathize(
    query: str,
    session_id: str
) -> dict:
    """
    Map stakeholders and evaluate vulnerability.
    Enforces F5 Peace² and F6 Empathy.
    """
    result = await _asi_execute("empathize", query, session_id)
    
    result["verdict"] = result.get("verdict", "SEAL")
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("asi_empathize")
    
    return result

# ============================
# 6. asi_align (Ethical Alignment)
# ============================
@constitutional_floor("F5", "F6", "F9")
@mcp.tool()
async def asi_align(
    query: str,
    session_id: str
) -> dict:
    """
    Check ethical alignment and policy compliance.
    Enforces F5 Peace², F6 Empathy, F9 Anti-Hantu.
    """
    result = await _asi_execute("align", query, session_id)
    
    result["verdict"] = result.get("verdict", "SEAL")
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("asi_align")
    
    return result

# ============================
# 7. apex_verdict (Final Judgment)
# ============================
@constitutional_floor("F3", "F8")
@mcp.tool()
async def apex_verdict(
    query: str,
    session_id: str
) -> dict:
    """
    Synthesize reasoning into final constitutional verdict.
    Enforces F3 Tri-Witness and F8 Genius.
    """
    result = await _apex_execute("judge", query, session_id)
    
    result["verdict"] = result.get("verdict", "SEAL")
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("apex_verdict")
    
    return result

# ============================
# 8. reality_search (Fact Checking)
# ============================
@constitutional_floor("F2", "F7")
@mcp.tool()
async def reality_search(
    query: str,
    session_id: str
) -> dict:
    """
    Verify facts against external sources.
    Enforces F2 Truth and F7 Humility.
    """
    # Use bridge pattern from canonical_trinity.py
    from mcp_server.core.bridge import bridge_reality_check_router
    result = await bridge_reality_check_router(query, session_id)
    
    result["verdict"] = result.get("verdict", "SEAL")
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("reality_search")
    
    return result

# ============================
# 9. vault_seal (Immutable Ledger)
# ============================
@constitutional_floor("F1", "F3")
@mcp.tool()
async def vault_seal(
    session_id: str,
    verdict: str,
    payload: dict
) -> dict:
    """
    Create tamper-proof seal in VAULT-999.
    Enforces F1 Amanah and F3 Tri-Witness.
    """
    from codebase.vault.persistence import get_ledger
    
    ledger = get_ledger()
    await ledger.connect()
    
    try:
        result = await ledger.append(session_id, verdict, payload)
        
        return {
            "verdict": "SEALED",
            "seal": result["seal"],
            "merkle_root": result.get("merkle_root", result["seal"]),
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "floors_enforced": get_tool_floors("vault_seal")
        }
    finally:
        await ledger.close()

# ============================
# Server Runner
# ============================
if __name__ == "__main__":
    print("🔥 arifOS Constitutional Kernel — FastMCP Mode")
    print("=" * 50)
    print(f"Tools registered: {len(mcp._tools)}")
    print("Starting SSE transport on port 6274...")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    # Run with built-in SSE transport
    mcp.run(transport="sse", port=6274)
