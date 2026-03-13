"""arifOS Runtime — The Sovereign FastMCP Instance.

Provides the primary Model Context Protocol (MCP) server for the arifOS ecosystem.
"""

from __future__ import annotations


def __getattr__(name: str):
    # Lazy import to avoid circular dependency:
    # core.enforcement.governance_engine → arifosmcp.runtime.contracts
    # → arifosmcp.runtime.__init__ → server → phase2_tools → bridge
    # → core.enforcement.governance_engine (cycle)
    if name in ("mcp", "create_aaa_mcp_server"):
        from .server import create_aaa_mcp_server
        from .server import mcp as _mcp

        globals()["mcp"] = _mcp
        globals()["create_aaa_mcp_server"] = create_aaa_mcp_server
        return globals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["mcp", "create_aaa_mcp_server"]
