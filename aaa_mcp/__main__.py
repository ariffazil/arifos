"""
aaa_mcp CLI Entry Point — Triple Transport Support

Usage:
    python -m aaa_mcp                # stdio (default — Local Agents)
    python -m aaa_mcp sse            # sse (Remote — Railway/Network)
    python -m aaa_mcp http           # http (Streamable HTTP at /mcp)

DITEMPA BUKAN DIBERI
"""

import os
import sys


def main():
    mode = (sys.argv[1] if len(sys.argv) > 1 else "stdio").strip().lower()

    from .server import mcp

    if mode in ("", "stdio"):
        # Default to stdio for local agents
        mcp.run(transport="stdio")
        return

    if mode == "sse":
        port = int(os.getenv("PORT", 8080))
        host = os.getenv("HOST", "0.0.0.0")
        mcp.run(transport="sse", host=host, port=port)
        return

    if mode in ("http", "streamable-http"):
        port = int(os.getenv("PORT", 8080))
        host = os.getenv("HOST", "0.0.0.0")
        mcp.run(transport="http", host=host, port=port)
        return

    print(f"Unknown mode '{mode}'. Use one of: stdio, sse, http", file=sys.stderr)
    raise SystemExit(2)


if __name__ == "__main__":
    main()
