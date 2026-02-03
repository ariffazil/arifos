"""
FastMCP Migration — All 9 Constitutional Tools
Replaces custom SSE transport with FastMCP framework
"""
from fastmcp import FastMCP
from typing import Optional
import asyncio

# Import arifOS constitutional components
from codebase.init import InitEngine
from codebase.agi.engine import AGIEngine
from codebase.asi.engine import ASIEngine
from codebase.apex.engine import APEXEngine
from codebase.reality.engine import RealityEngine
from codebase.vault.engine import VaultEngine
from codebase.guards.injection_guard import InjectionGuard
from codebase.mcp.constitutional_decorator import constitutional_floor, get_tool_floors

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
    # F12: Injection Guard
    guard = InjectionGuard()
    injection_score = await guard.scan(query)
    
    if injection_score > 0.85:
        return {
            "verdict": "VOID",
            "reason": "F12 Hardening violation",
            "injection_score": injection_score,
            "safe": False,
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "seal": "💎🔥🧠"
        }
    
    # Initialize session
    engine = InitEngine()
    result = await engine.ignite(query, session_id)
    
    # Add constitutional metadata
    result["verdict"] = "SEAL"
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["seal"] = "💎🔥🧠"
    result["safe"] = True
    result["floors_enforced"] = get_tool_floors("init_gate")
    
    return result

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
    engine = AGIEngine()
    result = await engine.sense(query, session_id)
    
    result["verdict"] = "SEAL"
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
    engine = AGIEngine()
    result = await engine.think(query, session_id)
    
    result["verdict"] = "SEAL"
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
    engine = AGIEngine()
    result = await engine.reason(query, session_id)
    
    result["verdict"] = "SEAL"
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
    engine = ASIEngine()
    result = await engine.empathize(query, session_id)
    
    result["verdict"] = "SEAL"
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
    engine = ASIEngine()
    result = await engine.align(query, session_id)
    
    result["verdict"] = "SEAL"
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
    engine = APEXEngine()
    result = await engine.judge(query, session_id)
    
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
    engine = RealityEngine()
    result = await engine.search(query, session_id)
    
    result["verdict"] = "SEAL"
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
    engine = VaultEngine()
    result = await engine.seal(session_id, verdict, payload)
    
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("vault_seal")
    
    return result

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
