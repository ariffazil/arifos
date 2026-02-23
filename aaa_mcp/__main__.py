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
    mode = (sys.argv[1] if len(sys.argv) > 1 else "sse").lower()

    if mode == "rest":
        from aaa_mcp.rest import main as rest_main

        rest_main()
        return

    if mode not in {"stdio", "sse", "http"}:
        raise SystemExit(2)

    # Kept for contract tests + runtime sanity checks.
    _ = check_fastmcp_version()

    from aaa_mcp.server import create_unified_mcp_server

    mcp = create_unified_mcp_server()
    mcp.run(transport=mode)


if __name__ == "__main__":
    main()
