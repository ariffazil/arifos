#!/usr/bin/env python3
"""
arifOS Unified Server — Single Deployable MCP Server with ChatGPT Integration
Combines AAA-MCP (9 governance skills) and ACLIP-CAI (10 sensory tools)
Includes MCP Resource Templates for dynamic data access.

Usage:
    python server.py                   # REST API (default)
    python server.py --mode rest       # REST API with HTTP + SSE endpoints
    python server.py --mode http       # FastMCP HTTP transport
    python server.py --mode sse        # FastMCP SSE transport  
    python server.py --mode stdio      # STDIO for local MCP clients

Deployment:
    PORT=8080 HOST=0.0.0.0 python server.py --mode rest

DITEMPA BUKAN DIBERI
"""

import argparse
import json
import os
import sys
from typing import Optional, Dict, Any

def check_fastmcp_version():
    """Verify FastMCP version compatibility."""
    try:
        import fastmcp
        version = getattr(fastmcp, "__version__", "unknown")
        print(f"[arifOS] FastMCP version: {version}", file=sys.stderr)
        major = int(version.split(".")[0]) if version != "unknown" else 0
        if major < 2:
            print(f"[arifOS] ⚠️  WARNING: FastMCP {version} detected. Version 2.x+ required.", file=sys.stderr)
        else:
            print(f"[arifOS] ✓ FastMCP {version} - Full functionality available", file=sys.stderr)
        return major
    except Exception as e:
        print(f"[arifOS] ⚠️  Could not check FastMCP version: {e}", file=sys.stderr)
        return 0

def create_unified_mcp_server():
    """Create a unified MCP server with AAA-MCP and ACLIP-CAI tools and resource templates."""
    from fastmcp import FastMCP
    from dotenv import load_dotenv
    
    load_dotenv()  # Load secrets from .env
    
    # Ensure core imports can be resolved
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Import constitutional enforcement
    from aaa_mcp.core.constitutional_decorator import constitutional_floor
    from aaa_mcp.core.engine_adapters import InitEngine
    from aaa_mcp.services.constitutional_metrics import get_stage_result, store_stage_result
    
    # Import AAA-MCP tool implementations
    from core.kernel.mcp_tool_service import (
        align_tool,
        anchor_tool,
        audit_tool,
        forge_tool,
        integrate_tool,
        reason_tool,
        respond_tool,
        seal_tool,
        trinity_forge_tool,
        validate_tool,
    )
    
    # Import ChatGPT integration tools
    from aaa_mcp.tools.reality_grounding import web_search_noapi
    
    # Import container management tools
    from aaa_mcp.integrations.mcp_container_tools import register_container_tools
    
    # Import ACLIP-CAI sensory tools
    from aclip_cai.tools.chroma_query import list_collections, query_memory
    from aclip_cai.tools.config_reader import config_flags as config_reader
    from aclip_cai.tools.financial_monitor import financial_cost as estimate_financial_cost
    from aclip_cai.tools.fs_inspector import fs_inspect as fs_inspector
    from aclip_cai.tools.log_reader import log_tail as log_reader
    from aclip_cai.tools.net_monitor import net_status as net_monitor
    from aclip_cai.tools.safety_guard import forge_guard as safety_guard
    from aclip_cai.tools.system_monitor import get_resource_usage, get_system_health, list_processes
    from aclip_cai.tools.thermo_estimator import cost_estimator as thermo_cost
    
    # Import constitutional resources
    from aaa_mcp.core.motto_schema import get_mottos_resource
    from core.shared.floors import THRESHOLDS
    
    # Create unified MCP server
    mcp = FastMCP(
        "arifOS-Unified",
        instructions="""
        arifOS Unified Server — Constitutional Governance + Sensory Perception
        
        AAA-MCP (9 Hardened Skills):
          1. anchor     — 000_INIT (Authority/F12)
          2. reason     — 222_REASON (Truth/F8)
          3. integrate  — 333_MAP (Grounding/F7)
          4. respond    — 444_DRAFT (Clarity/F4)
          5. validate   — 555_IMPACT (Empathy/F6)
          6. align      — 666_ETHICS (Anti-Hantu/F9)
          7. forge      — 777_SYNTHESIZE (Code/F2)
          8. audit      — 888_JUDGE (Consensus/F3)
          9. seal       — 999_SEAL (Permanence/F1)
          10. trinity_forge — Unified 000-999 pipeline
          11. search    — Web search (ChatGPT integration)
          12. fetch     — Web fetch (ChatGPT integration)
        
        ACLIP-CAI (10 Sensory Tools):
          system_health   — C0: CPU, RAM, disk, processes
          fs_inspect      — C2: Filesystem traversal (read-only)
          log_tail        — C3: Log monitoring
          net_status      — C4: Network diagnostics
          config_flags    — C5: Environment inspection
          chroma_query    — C6: Vector memory search
          cost_estimator  — C7: Thermodynamic cost
          forge_guard     — C8: Safety circuit breaker (gated)
          financial_cost  — C9: Monetary cost
        
        MCP Resource Templates (Read‑Only Data):
          constitutional://mottos             — All constitutional mottos
          constitutional://mottos/{floor}     — Motto for specific floor
          constitutional://floors             — All 13 floors specification
          constitutional://floors/{floor_id}  — Specific floor details
          system://health                     — Current system health
          tools://schemas                     — All tool schemas
          tools://schemas/{tool_name}         — Schema for specific tool
        
        Constitutional enforcement applies to AAA-MCP tools only.
        Sensory tools are read-only (except forge_guard which is local gating).
        
        DITEMPA BUKAN DIBERI — Forged, Not Given
        """,
    )
    
    # Register container tools
    register_container_tools(mcp)
    
    # =========================================================================
    # AAA-MCP TOOLS (9 Hardened Skills + ChatGPT)
    # =========================================================================
    
    @mcp.tool(name="anchor", description="1. ANCHOR (000) - Init & Sense")
    @constitutional_floor("F11", "F12")
    async def anchor(
        query: str,
        actor_id: str = "anonymous",
        auth_token: str = "none",
        platform: str = "CLI",
    ) -> dict:
        """000_INIT — Universal Ignition Protocol."""
        return await anchor_tool(
            query=query,
            actor_id=actor_id,
            auth_token=auth_token,
            platform=platform,
            init_engine=InitEngine(),
            store_stage_result_fn=store_stage_result,
        )
    
    @mcp.tool(name="reason", description="2. REASON (222) - Think & Hypothesize")
    @constitutional_floor("F2", "F4", "F8")
    async def reason(query: str, session_id: str, hypotheses: int = 3) -> dict:
        """222_THINK — Generate Hypotheses."""
        from core.kernel.constants import ToolDefaults
        from core.organs import sense, think
        
        return await reason_tool(
            query=query,
            session_id=session_id,
            hypotheses=hypotheses,
            get_stage_result_fn=get_stage_result,
            store_stage_result_fn=store_stage_result,
            sense_fn=sense,
            think_fn=think,
            truth_score_placeholder=ToolDefaults.TRUTH_SCORE_PLACEHOLDER,
            clarity_delta_placeholder=ToolDefaults.CLARITY_DELTA,
        )
    
    @mcp.tool(name="integrate", description="3. INTEGRATE (333) - Map & Ground")
    @constitutional_floor("F7", "F10")
    async def integrate(query: str, session_id: str, grounding: Optional[list] = None) -> dict:
        """333_ATLAS — Integrate context and external knowledge."""
        from core.kernel.constants import ConstitutionalThresholds
        from core.organs import reason as core_reason, sense, think
        
        return await integrate_tool(
            query=query,
            session_id=session_id,
            grounding=grounding,
            get_stage_result_fn=get_stage_result,
            store_stage_result_fn=store_stage_result,
            sense_fn=sense,
            think_fn=think,
            reason_fn=core_reason,
            humility_omega_default=ConstitutionalThresholds.OMEGA_DISPLAY_MIN,
        )
    
    @mcp.tool(name="respond", description="4. RESPOND (444) - Draft & Plan")
    @constitutional_floor("F4", "F6")
    async def respond(
        query: str, session_id: str, plan: Optional[str] = None, scope: str = "social"
    ) -> dict:
        """444_TRINITY — Generate consolidated plan or draft."""
        from aaa_mcp.core.stage_adapter import run_stage_444_trinity_sync
        return await respond_tool(
            session_id=session_id,
            plan=plan,
            get_stage_result_fn=get_stage_result,
            run_stage_444_fn=run_stage_444_trinity_sync,
        )

    @mcp.tool(name="validate", description="5. VALIDATE (555) - Impact Check")
    @constitutional_floor("F5", "F6")
    async def validate(
        query: str,
        session_id: str,
        stakeholders: Optional[list] = None,
        scope: str = "social",
    ) -> dict:
        """555_ASI — Empathy & Safety Verification."""
        from aaa_mcp.core.stage_adapter import run_stage_555_empathy
        from core.kernel.constants import ConstitutionalThresholds, ToolDefaults
        return await validate_tool(
            query=query,
            session_id=session_id,
            stakeholders=stakeholders,
            run_stage_555_fn=run_stage_555_empathy,
            peace_squared_min=(
                ConstitutionalThresholds.PEACE_SQUARED_MIN
                if hasattr(ConstitutionalThresholds, "PEACE_SQUARED_MIN")
                else 1.0
            ),
            empathy_kappa_r_default=ConstitutionalThresholds.EMPATHY_KAPPA_R,
            safe_default=ToolDefaults.SAFE_DEFAULT,
        )

    @mcp.tool(name="align", description="6. ALIGN (666) - Ethics Check")
    @constitutional_floor("F9")
    async def align(query: str, session_id: str, ethical_rules: Optional[list] = None) -> dict:
        """666_ASI — Ethical Alignment."""
        from aaa_mcp.core.stage_adapter import run_stage_666_align
        return await align_tool(
            query=query,
            session_id=session_id,
            ethical_rules=ethical_rules,
            run_stage_666_fn=run_stage_666_align,
        )

    @mcp.tool(name="forge", description="7. FORGE (777) - Synthesize Solution")
    @constitutional_floor("F2", "F4")
    async def forge(query: str, session_id: str, implementation_details: dict) -> dict:
        """777_APEX — Solution Synthesis."""
        from aaa_mcp.core.stage_adapter import run_stage_777_forge
        return await forge_tool(
            session_id=session_id,
            implementation_details=implementation_details,
            get_stage_result_fn=get_stage_result,
            run_stage_777_fn=run_stage_777_forge,
        )

    @mcp.tool(name="audit", description="8. AUDIT (888) - Verify & Judge")
    @constitutional_floor("F3", "F11", "F13")
    async def audit(session_id: str, verdict: str, human_approve: bool = False) -> dict:
        """888_APEX — Final Verdict."""
        from aaa_mcp.core.stage_adapter import run_stage_888_judge
        from core.kernel.constants import ConstitutionalThresholds
        return await audit_tool(
            session_id=session_id,
            verdict=verdict,
            human_approve=human_approve,
            tri_witness_score=ConstitutionalThresholds.TRI_WITNESS_SCORE,
            get_stage_result_fn=get_stage_result,
            run_stage_888_fn=run_stage_888_judge,
        )

    @mcp.tool(name="seal", description="9. SEAL (999) - Commit to Vault")
    @constitutional_floor("F1", "F3")
    async def seal(session_id: str, summary: str, verdict: str) -> dict:
        """999_VAULT — Cryptographic Seal."""
        from aaa_mcp.core.stage_adapter import run_stage_999_seal
        return await seal_tool(
            session_id=session_id,
            summary=summary,
            verdict=verdict,
            get_stage_result_fn=get_stage_result,
            run_stage_999_fn=run_stage_999_seal,
        )

    @mcp.tool(name="trinity_forge", description="Unified 000-999 Constitutional Pipeline")
    async def trinity_forge(query: str, actor_id: str = "anonymous") -> dict:
        """FORGE_PIPELINE — Orchestrate the full loop."""
        from core.pipeline import forge as forge_pipeline
        return await trinity_forge_tool(
            query=query,
            actor_id=actor_id,
            forge_pipeline_fn=forge_pipeline,
        )
    
    @mcp.tool(name="search", annotations={"readOnlyHint": True})
    async def search(
        query: str,
        num_results: int = 5,
        freshness: str = "any",
    ) -> dict:
        """Web search tool for ChatGPT Deep Research integration."""
        try:
            results = web_search_noapi(query, num_results, freshness)
            return {"results": results, "verdict": "SEAL", "source": "web_search_noapi"}
        except Exception as e:
            return {"verdict": "VOID", "error": str(e), "stage": "search"}
    
    @mcp.tool(name="fetch", annotations={"readOnlyHint": True})
    async def fetch(
        url: str,
        timeout: int = 10,
    ) -> dict:
        """Web fetch tool for ChatGPT Deep Research integration."""
        try:
            import requests
            from requests.exceptions import RequestException, Timeout
            
            headers = {
                "User-Agent": "arifOS-Fetch/1.0 (Compatible; ChatGPT-Deep-Research)",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            }
            
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            return {
                "url": url,
                "status_code": response.status_code,
                "content_type": response.headers.get("content-type", "unknown"),
                "content": response.text[:5000],  # Limit size
                "verdict": "SEAL",
            }
        except Timeout:
            return {"verdict": "VOID", "error": f"Request timed out after {timeout} seconds", "url": url}
        except RequestException as e:
            return {"verdict": "VOID", "error": f"Request failed: {e}", "url": url}
        except Exception as e:
            return {"verdict": "VOID", "error": f"Unexpected error: {e}", "url": url}
    
    # =========================================================================
    # ACLIP-CAI SENSORY TOOLS (10 Senses)
    # =========================================================================
    
    @mcp.tool()
    async def system_health(
        mode: str = "full",
        filter_process: str = "",
        top_n: int = 15,
    ) -> dict:
        """
        [C0] System health — CPU, RAM, disk, processes.
        
        The AI equivalent of 'top' or Task Manager.
        """
        if mode == "resources":
            return get_resource_usage()
        elif mode == "processes":
            return list_processes(filter_name=filter_process, top_n=top_n)
        else:
            return get_system_health()
    
    @mcp.tool()
    async def fs_inspect(
        path: str = ".",
        depth: int = 1,
        include_hidden: bool = False,
    ) -> dict:
        """
        [C2] Filesystem inspection — read-only directory traversal.
        
        Physical meaning: How much data exists where.
        """
        return fs_inspector(path=path, depth=depth, include_hidden=include_hidden)
    
    @mcp.tool()
    async def log_tail(
        log_file: str = "aaa_mcp.log",
        lines: int = 50,
        pattern: str = "",
    ) -> dict:
        """
        [C3] Log tail — recent entries with optional grep.
        
        Physical meaning: Historical errors, incidents, warnings.
        """
        return log_reader(log_file=log_file, lines=lines, pattern=pattern)
    
    @mcp.tool()
    async def net_status(
        check_ports: bool = True,
        check_connections: bool = True,
    ) -> dict:
        """
        [C4] Network posture — ports, connections, routing.
        
        Physical meaning: Attack surface, data exfil risk.
        """
        return net_monitor(check_ports=check_ports, check_connections=check_connections)
    
    @mcp.tool()
    async def config_flags() -> dict:
        """
        [C5] Environment and feature flags.
        
        Physical meaning: How the system is configured in reality.
        """
        return config_reader()
    
    @mcp.tool()
    async def chroma_query(
        query: str,
        collection: str = "default",
        top_k: int = 5,
        list_only: bool = False,
    ) -> dict:
        """
        [C6] Vector memory semantic search.
        
        The AI equivalent of 'grep' over persistent memory.
        """
        if list_only:
            return list_collections()
        return query_memory(query=query, collection=collection, top_k=top_k)
    
    @mcp.tool()
    async def cost_estimator(
        action_description: str,
        estimated_cpu_percent: float = 0,
        estimated_ram_mb: float = 0,
        estimated_io_mb: float = 0,
    ) -> dict:
        """
        [C7] Thermodynamic cost estimation.
        
        Physical meaning: Energy/heat/time consumption.
        """
        return thermo_cost(
            action_description=action_description,
            estimated_cpu_percent=estimated_cpu_percent,
            estimated_ram_mb=estimated_ram_mb,
            estimated_io_mb=estimated_io_mb,
        )
    
    @mcp.tool()
    async def financial_cost(
        service: str,
        action: str,
        resource_id: str = "",
        period_days: int = 1,
    ) -> dict:
        """
        [C9] Financial cost estimation.
        
        Physical meaning: Monetary cost of operations.
        """
        return estimate_financial_cost(
            service=service,
            action=action,
            resource_id=resource_id,
            period_days=period_days,
        )
    
    @mcp.tool()
    async def forge_guard(
        check_system_health: bool = True,
        cost_score_threshold: float = 0.8,
        cost_score_to_check: float = 0.0,
    ) -> dict:
        """
        [C8] Local safety circuit breaker.
        
        Physical meaning: Console-level circuit breaker.
        Returns: OK / SABAR (delay) / VOID_LOCAL (don't try).
        
        NOTE: This is the ONLY tool with write/gate potential.
        It only gates local actions, never executes remotely.
        """
        return safety_guard(
            check_system_health=check_system_health,
            cost_score_threshold=cost_score_threshold,
            cost_score_to_check=cost_score_to_check,
        )
    
    # =========================================================================
    # MCP RESOURCE TEMPLATES (Parameterized Read‑Only Data)
    # =========================================================================
    
    @mcp.resource("constitutional://mottos")
    def resource_all_mottos() -> Dict[str, Any]:
        """All constitutional mottos as a JSON resource."""
        return get_mottos_resource()["text"]
    
    @mcp.resource("constitutional://mottos/{floor}")
    def resource_motto_for_floor(floor: str) -> Dict[str, Any]:
        """Get motto for a specific constitutional floor."""
        from core.shared.mottos import get_motto_by_floor
        
        motto = get_motto_by_floor(floor)
        if not motto:
            return {"error": f"No motto found for floor {floor}"}
        
        return {
            "floor": floor,
            "malay": motto.malay,
            "english": motto.english,
            "explanation": motto.explanation,
        }
    
    @mcp.resource("constitutional://floors")
    def resource_all_floors() -> Dict[str, Any]:
        """All 13 constitutional floors specification."""
        return {
            "schema_version": "v52.5.2-SEAL",
            "total_floors": len(THRESHOLDS),
            "floors": THRESHOLDS,
            "note": "Threshold values are canonical and immutable.",
        }
    
    @mcp.resource("constitutional://floors/{floor_id}")
    def resource_specific_floor(floor_id: str) -> Dict[str, Any]:
        """Details for a specific constitutional floor."""
        floor_key = floor_id.upper()
        if floor_key not in THRESHOLDS:
            return {"error": f"Floor {floor_id} not found. Valid floors: {list(THRESHOLDS.keys())}"}
        
        floor_info = THRESHOLDS[floor_key].copy()
        floor_info["id"] = floor_key
        return floor_info
    
    @mcp.resource("system://health")
    def resource_system_health() -> Dict[str, Any]:
        """Current system health status."""
        health_data = get_system_health()
        return {
            "timestamp": health_data.get("timestamp"),
            "status": health_data.get("status", "unknown"),
            "cpu_percent": health_data.get("cpu_percent", 0),
            "memory_percent": health_data.get("memory_percent", 0),
            "disk_usage": health_data.get("disk_usage", {}),
            "process_count": health_data.get("process_count", 0),
        }
    
    @mcp.resource("tools://schemas")
    def resource_all_tool_schemas() -> Dict[str, Any]:
        """Schemas for all available tools."""
        # Collect tool schemas from MCP server
        schemas = {}
        for tool_name, tool_func in mcp._tools.items():
            # Extract schema from tool function annotations
            import inspect
            sig = inspect.signature(tool_func)
            params = {}
            for param_name, param in sig.parameters.items():
                params[param_name] = {
                    "type": str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any",
                    "default": param.default if param.default != inspect.Parameter.empty else None,
                    "required": param.default == inspect.Parameter.empty,
                }
            
            schemas[tool_name] = {
                "name": tool_name,
                "description": getattr(tool_func, "__doc__", ""),
                "parameters": params,
                "async": inspect.iscoroutinefunction(tool_func),
            }
        
        return {
            "total_tools": len(schemas),
            "schemas": schemas,
        }
    
    @mcp.resource("tools://schemas/{tool_name}")
    def resource_tool_schema(tool_name: str) -> Dict[str, Any]:
        """Schema for a specific tool."""
        import inspect
        
        if tool_name not in mcp._tools:
            return {"error": f"Tool {tool_name} not found"}
        
        tool_func = mcp._tools[tool_name]
        sig = inspect.signature(tool_func)
        params = {}
        for param_name, param in sig.parameters.items():
            params[param_name] = {
                "type": str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any",
                "default": param.default if param.default != inspect.Parameter.empty else None,
                "required": param.default == inspect.Parameter.empty,
            }
        
        return {
            "name": tool_name,
            "description": getattr(tool_func, "__doc__", ""),
            "parameters": params,
            "async": inspect.iscoroutinefunction(tool_func),
            "constitutional_floors": getattr(tool_func, "_constitutional_floors", []),
        }
    
    return mcp

def run_stdio():
    """Run MCP server with STDIO transport (for local clients like Claude Desktop)."""
    mcp = create_unified_mcp_server()
    print("[arifOS] Starting Unified MCP server with STDIO transport", file=sys.stderr)
    print("[arifOS] Tools available: 9 AAA-MCP skills + 10 ACLIP-CAI senses + ChatGPT search/fetch", file=sys.stderr)
    mcp.run(transport="stdio")

def run_sse(host: str, port: int):
    """Run MCP server with SSE transport."""
    mcp = create_unified_mcp_server()
    print(f"[arifOS] Starting Unified MCP server with SSE transport on {host}:{port}", file=sys.stderr)
    print("[arifOS] Tools available: 9 AAA-MCP skills + 10 ACLIP-CAI senses + ChatGPT search/fetch", file=sys.stderr)
    os.environ["FORWARDED_ALLOW_IPS"] = "*"  # Trust proxy headers
    mcp.run(transport="sse", host=host, port=port)

def run_http(host: str, port: int):
    """Run MCP server with FastMCP HTTP transport."""
    mcp = create_unified_mcp_server()
    print(f"[arifOS] Starting Unified MCP server with HTTP transport on {host}:{port}", file=sys.stderr)
    print("[arifOS] Tools available: 9 AAA-MCP skills + 10 ACLIP-CAI senses + ChatGPT search/fetch", file=sys.stderr)
    mcp.run(transport="http", host=host, port=port)

def run_rest(host: str, port: int):
    """Run REST API with full endpoints (HTTP + SSE + ChatGPT tools)."""
    from aaa_mcp.rest import main as rest_main
    # Set environment variables for rest.py
    os.environ["HOST"] = host
    os.environ["PORT"] = str(port)
    print(f"[arifOS] Starting REST API server on {host}:{port}", file=sys.stderr)
    print(f"[arifOS] Endpoints:", file=sys.stderr)
    print(f"[arifOS]   GET  /health           - Health check", file=sys.stderr)
    print(f"[arifOS]   GET  /ready            - Tool registry ready", file=sys.stderr)
    print(f"[arifOS]   GET  /tools            - List tools with schemas", file=sys.stderr)
    print(f"[arifOS]   POST /tools/{{name}}     - Call tool", file=sys.stderr)
    print(f"[arifOS]   GET  /sse              - MCP SSE transport", file=sys.stderr)
    print(f"[arifOS]   POST /messages         - MCP JSON-RPC messages", file=sys.stderr)
    print(f"[arifOS]   POST /apex_judge       - Full pipeline wrapper", file=sys.stderr)
    print(f"[arifOS]   GET  /                 - Route info", file=sys.stderr)
    print(f"[arifOS] Tools available: anchor, reason, integrate, respond, validate, align, forge, audit, seal, search, fetch, system_health, fs_inspect, log_tail, net_status, config_flags, chroma_query, cost_estimator, financial_cost, forge_guard", file=sys.stderr)
    rest_main()

def main():
    parser = argparse.ArgumentParser(description="arifOS Unified MCP Server")
    parser.add_argument(
        "--mode",
        choices=["stdio", "sse", "http", "rest"],
        default="rest",
        help="Server mode (default: rest)"
    )
    parser.add_argument(
        "--host",
        default=os.getenv("HOST", "0.0.0.0"),
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", "8080")),
        help="Port to bind to (default: 8080)"
    )
    
    args = parser.parse_args()
    
    # Check FastMCP version before anything else
    check_fastmcp_version()
    
    if args.mode == "stdio":
        run_stdio()
    elif args.mode == "sse":
        run_sse(args.host, args.port)
    elif args.mode == "http":
        run_http(args.host, args.port)
    elif args.mode == "rest":
        run_rest(args.host, args.port)
    else:
        print(f"Unknown mode: {args.mode}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()