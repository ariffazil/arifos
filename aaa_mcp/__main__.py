"""aaa_mcp CLI entrypoint.

This module is intentionally small and stable because multiple clients and test
suites rely on its transport dispatch behavior.

Canonical external surface may live in `arifos_aaa_mcp`, but `aaa_mcp` remains a
supported compatibility shim.
"""

from __future__ import annotations

import sys


def check_fastmcp_version() -> int:
    """Return the major FastMCP version (best-effort)."""

    try:
        import fastmcp  # type: ignore

        ver = getattr(fastmcp, "__version__", "0")
        major = int(str(ver).split(".", 1)[0])
        return major
    except Exception:
        return 0


def main() -> None:
    import argparse
    
    parser = argparse.ArgumentParser(description="arifOS MCP server")
    parser.add_argument("mode", nargs="?", default="sse", choices=["stdio", "sse", "http", "rest"])
    parser.add_argument("--host", default=None, help="Host to bind (for sse/http)")
    parser.add_argument("--port", type=int, default=None, help="Port to bind (for sse/http)")
    
    args, _ = parser.parse_known_args()
    mode = args.mode.lower()

    if mode == "rest":
        from aaa_mcp.rest import main as rest_main

        rest_main()
        return

    # Kept for contract tests + runtime sanity checks.
    _ = check_fastmcp_version()

    from arifos_aaa_mcp.server import create_aaa_mcp_server

    mcp = create_aaa_mcp_server()

    run_kwargs = {"transport": mode}
    if args.host is not None:
        run_kwargs["host"] = args.host
    if args.port is not None:
        run_kwargs["port"] = args.port

    mcp.run(**run_kwargs)


if __name__ == "__main__":
    main()
