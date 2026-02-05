"""
arifOS MCP Server Integration Package
ASI (Arif's Sidekick Intelligence) Gateway

Provides constitutional governance layer for external MCP servers.
"""
from .asi_gateway import mcp, init_gate, agi_sense, agi_think, agi_reason
from .asi_gateway import asi_empathize, asi_align, apex_verdict, vault_seal
from .asi_gateway import mcp_call, get_audit_log, list_mcp_servers
from .mcp_integration import MCPIntegrationLayer, get_mcp_layer, mcp_call
from .mcp_config import MCP_SERVERS, get_server_config, TrinityComponent
from .constitutional_decorator import constitutional_floor, get_tool_floors

__version__ = "55.4.0"
__all__ = [
    # Gateway
    "mcp",
    "init_gate",
    "agi_sense",
    "agi_think", 
    "agi_reason",
    "asi_empathize",
    "asi_align",
    "apex_verdict",
    "vault_seal",
    "mcp_call",
    "get_audit_log",
    "list_mcp_servers",
    # Integration
    "MCPIntegrationLayer",
    "get_mcp_layer",
    # Config
    "MCP_SERVERS",
    "get_server_config",
    "TrinityComponent",
    # Decorators
    "constitutional_floor",
    "get_tool_floors",
]

def main():
    """Entry point for CLI"""
    import sys
    from .asi_gateway import mcp
    
    print("🔥 arifOS Constitutional Kernel — ASI Gateway")
    print(f"Version: {__version__}")
    print("Trinity: AGI(Δ)·ASI(Ω)·APEX(Ψ)")
    print("Motto: DITEMPA BUKAN DIBERI 💎🔥🧠")
    
    port = 6277
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    
    print(f"\nStarting SSE transport on port {port}...")
    mcp.run(transport="sse", port=port)

if __name__ == "__main__":
    main()