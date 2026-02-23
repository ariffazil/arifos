"""
Unified arifOS server entrypoint (repo root).

This is the human-friendly wrapper around `python -m aaa_mcp`, matching docs:

    python server.py                  # default: sse
    python server.py --mode rest      # REST bridge (+ /mcp alias + /health)
    python server.py --mode sse       # FastMCP SSE transport
    python server.py --mode http      # FastMCP Streamable HTTP transport
    python server.py --mode stdio     # FastMCP stdio (local clients)
"""

from __future__ import annotations

import argparse
import os
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="arifOS Unified Server (root entrypoint)")
    parser.add_argument(
        "--mode",
        choices=["rest", "sse", "http", "stdio"],
        default=os.getenv("ARIFOS_MODE", "sse"),
        help="Server mode (default: sse)",
    )
    parser.add_argument(
        "--host",
        default=os.getenv("HOST", "0.0.0.0"),
        help="Bind host (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", "8080")),
        help="Bind port (default: 8080)",
    )
    args = parser.parse_args()

    mode = (args.mode or "sse").strip().lower()

    if mode == "rest":
        from aaa_mcp.rest import main as rest_main

        os.environ["HOST"] = args.host
        os.environ["PORT"] = str(args.port)
        print(f"[arifOS] REST bridge on {args.host}:{args.port}", file=sys.stderr)
        rest_main()
        return

    from aaa_mcp.server import create_unified_mcp_server

    mcp = create_unified_mcp_server()

    if mode == "stdio":
        print("[arifOS] FastMCP STDIO transport", file=sys.stderr)
        mcp.run(transport="stdio")
        return

    if mode == "sse":
        print(f"[arifOS] FastMCP SSE transport on {args.host}:{args.port}", file=sys.stderr)
        mcp.run(transport="sse", host=args.host, port=args.port)
        return

    if mode == "http":
        print(f"[arifOS] FastMCP HTTP transport on {args.host}:{args.port}", file=sys.stderr)
        mcp.run(transport="http", host=args.host, port=args.port)
        return

    raise SystemExit(2)


if __name__ == "__main__":
    main()
