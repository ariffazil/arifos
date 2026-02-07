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

from aaa_mcp.core.constitutional_decorator import constitutional_floor, get_tool_floors
from aaa_mcp.core.engine_adapters import AGIEngine, APEXEngine, ASIEngine, InitEngine
from aaa_mcp.services.constitutional_metrics import store_stage_result
from aaa_mcp.tools.reality_grounding import reality_check

mcp = FastMCP("aaa-mcp")


# Note: custom_route endpoints require FastMCP 2.0+
# For health checks, use the MCP tools/list endpoint
# or upgrade FastMCP: pip install fastmcp>=2.0


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
async def reality_search(
    query: str, session_id: str, region: str = "wt-wt", timelimit: Optional[str] = None
) -> dict:
    """External fact-checking and reality grounding via web search.

    Verifies claims against external sources using constitutional cascade:
    1. DDGS (DuckDuckGo) - Primary, no API key, low entropy
    2. Playwright DDG HTML - Fallback
    3. Playwright Google - Last resort

    Use when a query requires up-to-date information or when truth
    confidence is low. Can be called at any point in the pipeline.

    Args:
        query: Search query
        session_id: Session identifier
        region: "wt-wt" (worldwide) or "asean" (MY/SG/ID bias)
        timelimit: "d" (day), "w" (week), "m" (month), "y" (year)

    Returns results with uncertainty tracking (Ω₀) per F7 Humility.

    Pipeline position: Auxiliary (can be called from any stage)
    Floors enforced: F2 (Truth >= 0.99), F7 (Humility)
    """
    result = await reality_check(query, region=region, timelimit=timelimit)
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
    from codebase.vault.persistent_ledger_hardened import get_hardened_vault_ledger

    ledger = get_hardened_vault_ledger()
    await ledger.connect()
    try:
        result = await ledger.append(
            session_id=session_id, verdict=verdict, seal_data=payload, authority="mcp_server"
        )
        return {
            "verdict": "SEALED",
            "seal": result.get("entry_hash", f"hash-{result.get('sequence_number', 0)}"),
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "floors_enforced": get_tool_floors("vault_seal"),
            "pass": "reverse",
        }
    finally:
        # Singleton - don't close
        pass


@mcp.tool()
@constitutional_floor("F1", "F2")
async def vault_query(
    session_pattern: Optional[str] = None,
    verdict: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    limit: int = 10,
) -> dict:
    """Query past vault_seal entries for institutional memory retrieval.

    Search the constitutional ledger for past decisions, violations, and patterns.
    Use this to learn from history and maintain institutional continuity (F13).

    Pipeline position: Auxiliary (can be called anytime)
    Floors enforced: F1 (Amanah), F2 (Truth)

    Args:
        session_pattern: Glob pattern for session_id (e.g., "test_*")
        verdict: Filter by verdict type (SEAL, VOID, PARTIAL, SABAR)
        date_from: ISO date string for range start (e.g., "2026-02-01")
        date_to: ISO date string for range end
        limit: Maximum entries to return (default 10, max 100)

    Returns:
        Dict with count, entries list, and detected patterns
    """
    from datetime import datetime, timezone
    from codebase.vault.persistent_ledger_hardened import get_hardened_vault_ledger

    ledger = get_hardened_vault_ledger()
    await ledger.connect()

    # Parse dates
    start_time = None
    end_time = None
    if date_from:
        try:
            start_time = datetime.fromisoformat(date_from.replace("Z", "+00:00"))
            if start_time.tzinfo is None:
                start_time = start_time.replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    if date_to:
        try:
            end_time = datetime.fromisoformat(date_to.replace("Z", "+00:00"))
            if end_time.tzinfo is None:
                end_time = end_time.replace(tzinfo=timezone.utc)
        except ValueError:
            pass

    # Clamp limit
    limit = max(1, min(limit, 100))

    try:
        if verdict:
            # Use existing query_by_verdict
            result = await ledger.query_by_verdict(
                verdict=verdict,
                start_time=start_time,
                end_time=end_time,
                limit=limit
            )
            entries = result.get("entries", [])
        else:
            # Use list_entries and filter
            result = await ledger.list_entries(limit=limit * 2)  # Get more to filter
            entries = result.get("entries", [])

            # Filter by date range
            if start_time:
                entries = [e for e in entries if datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00")) >= start_time]
            if end_time:
                entries = [e for e in entries if datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00")) <= end_time]

        # Filter by session pattern (simple glob)
        if session_pattern:
            import fnmatch
            entries = [e for e in entries if fnmatch.fnmatch(e.get("session_id", ""), session_pattern)]

        # Limit results
        entries = entries[:limit]

        # Compute patterns if enough data
        patterns = {}
        if len(entries) >= 3:
            verdicts = [e.get("verdict") for e in entries]
            void_count = sum(1 for v in verdicts if v == "VOID")
            patterns["void_rate"] = round(void_count / len(verdicts), 3) if verdicts else 0
            patterns["total_queried"] = len(entries)
            patterns["verdict_distribution"] = {
                v: sum(1 for x in verdicts if x == v) for v in set(verdicts)
            }

        # Simplify entries for response (remove heavy payload)
        simplified = []
        for e in entries:
            simplified.append({
                "session_id": e.get("session_id"),
                "timestamp": e.get("timestamp"),
                "verdict": e.get("verdict"),
                "authority": e.get("authority"),
                "entry_hash": e.get("entry_hash", "")[:16] + "...",
            })

        return {
            "count": len(simplified),
            "query": {
                "session_pattern": session_pattern,
                "verdict": verdict,
                "date_from": date_from,
                "date_to": date_to,
            },
            "entries": simplified,
            "patterns": patterns,
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "floors_enforced": get_tool_floors("vault_query"),
        }
    except Exception as e:
        return {
            "count": 0,
            "error": str(e),
            "entries": [],
            "patterns": {},
            "motto": "DITEMPA BUKAN DIBERI 💎🔥🧠",
            "floors_enforced": get_tool_floors("vault_query"),
        }


if __name__ == "__main__":
    print("🔥 arifOS Constitutional Kernel — FastMCP Mode")
    mcp.run(transport="sse", port=6274)
