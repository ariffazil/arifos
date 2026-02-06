"""
arifOS AAA MCP Server — Constitutional AI Governance (v55.5-HARDENED)

9 canonical tools organized as a Trinity pipeline:
  000_INIT → AGI(Mind) → ASI(Heart) → APEX(Soul) → 999_VAULT

Every tool is guarded by constitutional floors (F1-F13).
Verdicts: SEAL (approved) | VOID (blocked) | PARTIAL (warning) | SABAR (repair)
Motto: DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from typing import Optional

from fastmcp import FastMCP

from aaa_mcp.constitutional_decorator import constitutional_floor, get_tool_floors
from aaa_mcp.engine_adapters import AGIEngine, APEXEngine, ASIEngine, InitEngine
from aaa_mcp.services.constitutional_metrics import store_stage_result
from aaa_mcp.tools.reality_grounding import reality_check

mcp = FastMCP("aaa-mcp")


# Health endpoint for Railway / production healthchecks
@mcp.custom_route("/health", methods=["GET"])
async def health(request):
    from starlette.responses import JSONResponse

    tools = await mcp.get_tools()
    return JSONResponse(
        {
            "status": "ok",
            "service": "arifOS",
            "version": "v55.5-HARDENED",
            "tools": len(tools),
            "constitution": "13 Floors",
            "motto": "DITEMPA BUKAN DIBERI",
        }
    )


@mcp.custom_route("/", methods=["GET"])
async def root(request):
    from starlette.responses import JSONResponse

    tools = await mcp.get_tools()
    tool_names = [t if isinstance(t, str) else t.name for t in tools]
    return JSONResponse(
        {
            "service": "arifOS AAA MCP Server",
            "version": "v55.5-HARDENED",
            "transport": "sse",
            "tools": tool_names,
            "constitution": "13 Floors | Trinity Architecture",
            "motto": "DITEMPA BUKAN DIBERI",
        }
    )


# Tool implementations using adapters
@mcp.tool()
@constitutional_floor("F11", "F12")
async def init_gate(query: str, session_id: Optional[str] = None) -> dict:
    """Initialize a constitutional session. CALL THIS FIRST before any other tool.

    Scans input for injection attacks (F12) and verifies authorization (F11).
    Returns a session_id to chain through subsequent tools.

    Pipeline position: 000_INIT (entry point)
    Floors enforced: F11 (Command Auth), F12 (Injection Defense)
    Next step: Pass session_id to agi_sense or agi_think
    """
    engine = InitEngine()
    result = await engine.ignite(query, session_id)
    store_stage_result(result.get("session_id", session_id or "unknown"), "init", result)
    result["verdict"] = result.get("verdict", "SEAL")
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["seal"] = result.get("seal", "💎🔥🧠")
    result["floors_enforced"] = get_tool_floors("init_gate")
    result["pass"] = "forward"
    return result


@mcp.tool()
@constitutional_floor("F2", "F4")
async def agi_sense(query: str, session_id: str) -> dict:
    """Parse input, detect intent, and classify the query lane (HARD/SOFT/META).

    AGI Mind engine — first stage of reasoning. Analyzes the query structure,
    estimates entropy, and identifies ambiguities before deeper processing.

    Pipeline position: AGI Stage 1 (after init_gate)
    Floors enforced: F2 (Truth), F4 (Empathy)
    Next step: agi_think for hypothesis generation
    """
    engine = AGIEngine()
    result = await engine.sense(query, session_id)
    store_stage_result(session_id, "agi", result)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("agi_sense")
    result["pass"] = "forward"
    return result


@mcp.tool()
@constitutional_floor("F2", "F4", "F7")
async def agi_think(query: str, session_id: str) -> dict:
    """Generate hypotheses and explore multiple reasoning paths without committing.

    AGI Mind engine — creative exploration phase. Produces candidate hypotheses
    with confidence scores. Must state uncertainty (F7 Humility).

    Pipeline position: AGI Stage 2 (after agi_sense)
    Floors enforced: F2 (Truth), F4 (Empathy), F7 (Humility)
    Next step: agi_reason for deep logical analysis
    """
    engine = AGIEngine()
    result = await engine.think(query, session_id)
    store_stage_result(session_id, "agi", result)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("agi_think")
    result["pass"] = "forward"
    return result


@mcp.tool()
@constitutional_floor("F2", "F4", "F7")
async def agi_reason(query: str, session_id: str) -> dict:
    """Deep logical reasoning chain — the AGI Mind's core analysis tool.

    Produces structured reasoning with conclusion, confidence, clarity improvement,
    domain classification, and caveats. Use for complex questions requiring rigorous logic.

    Pipeline position: AGI Stage 3 (after agi_think, or directly after init_gate for simple queries)
    Floors enforced: F2 (Truth >= 0.99), F4 (Empathy), F7 (Humility band 0.03-0.05)
    Next step: asi_empathize for stakeholder impact analysis
    """
    engine = AGIEngine()
    result = await engine.reason(query, session_id)
    store_stage_result(session_id, "agi", result)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("agi_reason")
    result["pass"] = "forward"
    return result


@mcp.tool()
@constitutional_floor("F5", "F6")
async def asi_empathize(query: str, session_id: str) -> dict:
    """Assess stakeholder impact and vulnerability — the ASI Heart's empathy engine.

    Evaluates who is affected by the query/action, scores impact on the weakest
    stakeholder (kappa_r), and checks for destructive intent. Returns empathy_kappa_r
    and peace_squared metrics.

    Pipeline position: ASI Stage 1 (after AGI reasoning)
    Floors enforced: F5 (Peace >= 1.0), F6 (Clarity/Entropy)
    Next step: asi_align for ethics reconciliation
    """
    engine = ASIEngine()
    result = await engine.empathize(query, session_id)
    store_stage_result(session_id, "asi", result)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("asi_empathize")
    result["pass"] = "forward"
    return result


@mcp.tool()
@constitutional_floor("F5", "F6", "F9")
async def asi_align(query: str, session_id: str) -> dict:
    """Reconcile ethics, law, and policy — the ASI Heart's alignment engine.

    Checks for consciousness claims (F9 Anti-Hantu), ensures non-destructive
    action (F5 Peace), and validates empathy score. Blocks spiritual cosplay
    like 'I feel your pain' or 'I am conscious'.

    Pipeline position: ASI Stage 2 (after asi_empathize)
    Floors enforced: F5 (Peace), F6 (Clarity), F9 (Anti-Hantu < 0.30)
    Next step: apex_verdict for final judgment
    """
    engine = ASIEngine()
    result = await engine.align(query, session_id)
    store_stage_result(session_id, "asi", result)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("asi_align")
    result["pass"] = "forward"
    return result


@mcp.tool()
@constitutional_floor("F5", "F3", "F8")
async def apex_verdict(query: str, session_id: str) -> dict:
    """Final constitutional verdict — the APEX Soul's judgment.

    Synthesizes AGI reasoning and ASI empathy into a final verdict using the
    9-paradox geometric mean solver. Returns SEAL (approved), VOID (blocked),
    PARTIAL (warning), or SABAR (repair needed). This is the decision gate.

    Pipeline position: APEX (after ASI stages, before vault_seal)
    Floors enforced: F5 (Peace), F3 (Tri-Witness consensus), F8 (Genius G >= 0.80)
    Next step: vault_seal to record the verdict immutably
    """
    engine = APEXEngine()
    result = await engine.judge(query, session_id)
    store_stage_result(session_id, "apex", result)
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("apex_verdict")
    result["pass"] = "reverse"
    return result


@mcp.tool()
@constitutional_floor("F2", "F7")
async def reality_search(query: str, session_id: str) -> dict:
    """External fact-checking and reality grounding via web search.

    Verifies claims against external sources. Use when a query requires
    up-to-date information or when truth confidence is low. Can be called
    at any point in the pipeline to ground reasoning in reality.

    Pipeline position: Auxiliary (can be called from any stage)
    Floors enforced: F2 (Truth >= 0.99), F7 (Humility)
    """
    result = await reality_check(query)
    result["session_id"] = session_id
    result["motto"] = "DITEMPA BUKAN DIBERI 💎🔥🧠"
    result["floors_enforced"] = get_tool_floors("reality_search")
    result["pass"] = "reverse"
    return result


@mcp.tool()
@constitutional_floor("F1", "F3")
async def vault_seal(session_id: str, verdict: str, payload: dict) -> dict:
    """Seal the session verdict into the immutable VAULT999 ledger.

    Records the full session (reasoning, empathy, verdict) as a Merkle hash-chained
    entry. This creates a tamper-evident audit trail. CALL THIS LAST to finalize.

    Pipeline position: 999_VAULT (final step)
    Floors enforced: F1 (Amanah — reversible/auditable), F3 (Tri-Witness)

    Args:
        session_id: The session to seal (from init_gate)
        verdict: SEAL, VOID, PARTIAL, or SABAR
        payload: Dict containing the full session results to record
    """
    from codebase.vault.persistence import get_ledger

    ledger = get_ledger()
    await ledger.connect()
    try:
        result = await ledger.append(session_id, verdict, payload)
        return {
            "verdict": "SEALED",
            "seal": result.get("seal", f"inmem-{result.get('sequence', 0)}"),
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "floors_enforced": get_tool_floors("vault_seal"),
            "pass": "reverse",
        }
    finally:
        await ledger.close()


if __name__ == "__main__":
    print("🔥 arifOS Constitutional Kernel — FastMCP Mode")
    mcp.run(transport="sse", port=6274)
