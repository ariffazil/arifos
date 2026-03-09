"""
DEPRECATED: This legacy transport module is deprecated.

arifosmcp/runtime/server.py and FastMCP are the canonical deployment paths
for modern, agnostic MCP clients.
"""
"""arifosmcp.transport CLI entrypoint.

This module is intentionally small and stable because multiple clients and test
suites rely on its transport dispatch behavior.

Canonical external surface may live in `arifosmcp.runtime`, but `arifosmcp.transport` remains a
supported compatibility shim.
"""

from __future__ import annotations

from arifosmcp.transport.env_bootstrap import bootstrap_environment


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

    bootstrap_environment()

    parser = argparse.ArgumentParser(description="arifOS MCP server")
    parser.add_argument("mode", nargs="?", default="sse", choices=["stdio", "sse", "http", "rest"])
    parser.add_argument("--host", default=None, help="Host to bind (for sse/http)")
    parser.add_argument("--port", type=int, default=None, help="Port to bind (for sse/http)")

    args, _ = parser.parse_known_args()
    mode = args.mode.lower()

    if mode == "rest":
        from arifosmcp.transport.rest import main as rest_main

        rest_main()
        return

    # Kept for contract tests + runtime sanity checks.
    _ = check_fastmcp_version()

    import arifosmcp.runtime.server as _pub_server

    mcp = _pub_server.create_aaa_mcp_server()

    run_kwargs = {"transport": mode}
    if args.host is not None:
        run_kwargs["host"] = args.host
    if args.port is not None:
        run_kwargs["port"] = args.port

    mcp.run(**run_kwargs)


if __name__ == "__main__":
    main()
