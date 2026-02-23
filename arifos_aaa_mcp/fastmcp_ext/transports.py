"""Transport helpers for AAA MCP runtime."""

from __future__ import annotations

from typing import Any


def run_server(mcp: Any, mode: str, host: str, port: int) -> None:
    """Run FastMCP server by transport mode."""
    normalized = (mode or "sse").strip().lower()
    if normalized in ("", "stdio"):
        mcp.run(transport="stdio")
        return
    if normalized == "sse":
        mcp.run(transport="sse", host=host, port=port)
        return
    if normalized in ("http", "streamable-http"):
        mcp.run(transport="http", host=host, port=port)
        return
    raise ValueError(f"Unknown mode '{mode}'. Use stdio|sse|http")
