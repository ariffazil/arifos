"""
aaa_mcp CLI Entry Point — Triple Transport Support

Usage:
    python -m aaa_mcp                # stdio (default — Claude Code, Claude Desktop)
    python -m aaa_mcp stdio          # stdio (explicit)
    python -m aaa_mcp sse            # SSE (legacy remote — Railway, cloud)
    python -m aaa_mcp http           # Streamable HTTP (ChatGPT, OpenAI Codex, modern remote)

DITEMPA BUKAN DIBERI
"""

import sys


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "stdio"

    from .server import mcp

    if mode == "http":
        mcp.run(transport="streamable-http")
    elif mode == "sse":
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
