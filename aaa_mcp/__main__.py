"""
aaa_mcp CLI Entry Point — Triple Transport Support

Usage:
    python -m aaa_mcp                # stdio (default — Local Agents)
    python -m aaa_mcp sse            # sse (Remote — Railway/Network)

DITEMPA BUKAN DIBERI
"""

import sys


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "stdio"

    from .server import mcp

    if mode == "sse":
        mcp.run(transport="sse")
    else:
        # Default to stdio for local agents
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
