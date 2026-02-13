"""
aclip_cai/__main__.py — ACLIP Console for AI entry point

Usage:
    python -m aclip_cai           # stdio (default, for Claude Code / Desktop)
    python -m aclip_cai stdio
    python -m aclip_cai sse       # port 6275
    python -m aclip_cai http      # port 6276
"""

import sys


def main() -> None:
    from aclip_cai.server import mcp

    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"

    if transport == "sse":
        mcp.run(transport="sse", port=6275)
    elif transport == "http":
        mcp.run(transport="streamable-http", port=6276)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
