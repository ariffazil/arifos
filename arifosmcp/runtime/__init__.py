"""arifOS Runtime — The Sovereign FastMCP Instance.

Provides the primary Model Context Protocol (MCP) server for the arifOS ecosystem.
"""

from __future__ import annotations


def __getattr__(name: str):
    # Lazy import to avoid circular dependency
    if name in (
        "mcp",
        "create_aaa_mcp_server",
        "tools",
        "tools_internal",
        "phase2_tools",
        "bridge",
    ):
        if name in ("mcp", "create_aaa_mcp_server"):
            from .server import create_aaa_mcp_server
            from .server import mcp as _mcp

            globals()["mcp"] = _mcp
            globals()["create_aaa_mcp_server"] = create_aaa_mcp_server
        elif name == "tools":
            from . import tools as _tools

            globals()["tools"] = _tools
        elif name == "tools_internal":
            import importlib

            _tools_internal = importlib.import_module(".tools_internal", __package__)
            globals()["tools_internal"] = _tools_internal
        elif name == "phase2_tools":
            from . import phase2_tools as _p2tools

            globals()["phase2_tools"] = _p2tools
        elif name == "bridge":
            from . import bridge as _bridge

            globals()["bridge"] = _bridge

        return globals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["mcp", "create_aaa_mcp_server", "tools", "tools_internal", "phase2_tools", "bridge"]
