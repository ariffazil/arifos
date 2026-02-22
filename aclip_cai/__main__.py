"""
aclip_cai CLI Entry Point — Triple Transport Support

Usage:
    python -m aclip_cai                # stdio (default — MCP server)
    python -m aclip_cai stdio          # stdio (explicit)
    python -m aclip_cai sse            # SSE (Remote — Railway/Network)
    python -m aclip_cai http           # HTTP (Streamable HTTP at /mcp)
    python -m aclip_cai health         # CLI subcommand (legacy)

DITEMPA BUKAN DIBERI
"""

import os
import sys

TRANSPORT_MODES = {"stdio", "sse", "http", "streamable-http"}


def main():
    mode = (sys.argv[1] if len(sys.argv) > 1 else "stdio").strip().lower()

    # Route to FastMCP server for transport modes
    if mode in TRANSPORT_MODES or mode == "":
        from .server import mcp

        if mode in ("", "stdio"):
            mcp.run(transport="stdio")
            return

        if mode == "sse":
            port = int(os.getenv("PORT", 8081))
            host = os.getenv("HOST", "0.0.0.0")
            mcp.run(transport="sse", host=host, port=port)
            return

        if mode in ("http", "streamable-http"):
            port = int(os.getenv("PORT", 8081))
            host = os.getenv("HOST", "0.0.0.0")
            mcp.run(transport="http", host=host, port=port)
            return

    # Fall through to CLI for subcommands (health, processes, fs, etc.)
    from .cli import main as cli_main

    cli_main()


if __name__ == "__main__":
    main()
