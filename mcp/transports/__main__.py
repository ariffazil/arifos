"""
AAA MCP Glocal Entry Point — Global + Local Transport Unification (v55.3)

Usage:
    python -m mcp.transports [stdio|sse|auto]
    
Modes:
    stdio    → Local stdio for Claude Desktop, Cursor (BBB Bridge mode)
    sse      → Streamable HTTP for production/cloud (AAA Authority mode)
    auto     → Detect from environment (default)
    
Auto-Detection Logic:
    - If STDIN is TTY + no PORT env → stdio (local development)
    - If PORT env set or STDIN not TTY → sse (production/cloud)
    
DITEMPA BUKAN DIBERI
"""

import asyncio
import os
import sys
from typing import Literal

from ..core.tool_registry import ToolRegistry


def detect_transport_mode() -> Literal["stdio", "sse"]:
    """
    Auto-detect transport mode from environment.
    
    Glocal Logic:
        - Development (local): TTY stdin, no PORT set → stdio
        - Production (cloud): PORT set or non-TTY → sse
    """
    # Explicit override takes precedence
    explicit = os.environ.get("AAA_MCP_TRANSPORT", "").lower()
    if explicit in ("stdio", "sse"):
        return explicit
    
    # Production signals
    if os.environ.get("PORT") or os.environ.get("RAILWAY_ENVIRONMENT"):
        return "sse"
    
    # Check if stdin is a TTY (interactive terminal = local dev)
    try:
        if sys.stdin.isatty():
            return "stdio"
    except AttributeError:
        pass  # Non-TTY (pipe, file, etc.) → sse
    
    # Default to sse for non-interactive environments
    return "sse"


async def main():
    """Main entry point for AAA MCP Glocal transport."""
    # Parse command line
    mode = sys.argv[1] if len(sys.argv) > 1 else "auto"
    
    if mode == "auto":
        mode = detect_transport_mode()
        print(f"[AAA-MCP] Auto-detected mode: {mode}", file=sys.stderr)
    else:
        print(f"[AAA-MCP] Explicit mode: {mode}", file=sys.stderr)
    
    # Initialize constitutional tool registry
    registry = ToolRegistry()
    print(f"[AAA-MCP] Tool registry initialized: {len(registry._tools)} tools", file=sys.stderr)
    
    # Start appropriate transport
    if mode == "stdio":
        from .stdio import StdioTransport
        transport = StdioTransport(registry)
        print("[AAA-MCP] Starting stdio transport (BBB Bridge mode)", file=sys.stderr)
    else:  # sse
        from .sse import SSETransport
        transport = SSETransport(registry)
        host = os.getenv("HOST", "127.0.0.1")
        port = os.getenv("PORT", "8080")
        print(f"[AAA-MCP] Starting SSE transport (AAA Authority mode) on {host}:{port}", file=sys.stderr)
    
    # Run transport
    await transport.start()


# Entry point aliases for pyproject.toml
def main_stdio():
    """Explicit stdio entry point."""
    sys.argv = [sys.argv[0], "stdio"]
    asyncio.run(main())


def main_sse():
    """Explicit SSE entry point."""
    sys.argv = [sys.argv[0], "sse"]
    asyncio.run(main())


def main_auto():
    """Auto-detect entry point (default)."""
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())
