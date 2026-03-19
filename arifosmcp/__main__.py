"""arifosmcp - The Holy 9 MCP CLI entrypoint.

This is the canonical entrypoint for the unified arifOS MCP server.
It exposes the 9 Holy Tools through stdio, sse, or http transports.
"""

from __future__ import annotations
import argparse
from arifosmcp.server import mcp

def main() -> None:
    parser = argparse.ArgumentParser(description="arifosmcp server")
    parser.add_argument("mode", nargs="?", default="stdio", choices=["stdio", "sse", "http"])
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind (for sse/http)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind (for sse/http)")

    args, _ = parser.parse_known_args()
    
    run_kwargs = {"transport": args.mode}
    if args.mode in ["sse", "http"]:
        run_kwargs["host"] = args.host
        run_kwargs["port"] = args.port

    mcp.run(**run_kwargs)

if __name__ == "__main__":
    main()
