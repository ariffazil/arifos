"""
aaa_mcp CLI Entry Point — Triple Transport Support

Usage:
    python -m aaa_mcp                # stdio (default — Local Agents)
    python -m aaa_mcp sse            # sse (Remote — VPS/Network)
    python -m aaa_mcp http           # http (Streamable HTTP at /mcp)

DITEMPA BUKAN DIBERI
"""

import os
import sys


def check_fastmcp_version():
    """Verify FastMCP version compatibility."""
    try:
        import fastmcp

        version = getattr(fastmcp, "__version__", "unknown")
        print(f"[arifOS] FastMCP version: {version}", file=sys.stderr)

        # Parse major version
        major = int(version.split(".")[0]) if version != "unknown" else 0
        if major < 2:
            print(
                f"[arifOS] ⚠️  WARNING: FastMCP {version} detected. Version 2.x+ required for full functionality.",
                file=sys.stderr,
            )
            print(
                "[arifOS] Some features (like /health endpoint) may not work correctly.",
                file=sys.stderr,
            )
        else:
            print(f"[arifOS] ✓ FastMCP {version} - Full functionality available", file=sys.stderr)
        return major
    except Exception as e:
        print(f"[arifOS] ⚠️  Could not check FastMCP version: {e}", file=sys.stderr)
        return 0


def main():
    # Check version before importing server modules
    check_fastmcp_version()

    mode = (sys.argv[1] if len(sys.argv) > 1 else "stdio").strip().lower()

    # Unified server combines AAA-MCP and ACLIP-CAI tools
    from aaa_mcp.server import create_unified_mcp_server

    mcp = create_unified_mcp_server()

    if mode in ("", "stdio"):
        # Default to stdio for local agents
        mcp.run(transport="stdio")
        return

    if mode == "sse":
        port = int(os.getenv("PORT", 8080))
        host = os.getenv("HOST", "0.0.0.0")
        print(f"[arifOS] Starting MCP server with SSE transport on {host}:{port}", file=sys.stderr)

        # Reverse proxy terminates TLS and sets X-Forwarded-Proto.
        # We need uvicorn to trust these headers so SSE endpoint
        # advertises https:// URLs, not http://.
        os.environ["FORWARDED_ALLOW_IPS"] = "*"
        mcp.run(transport="sse", host=host, port=port)
        return

    if mode in ("http", "streamable-http"):
        port = int(os.getenv("PORT", 8080))
        host = os.getenv("HOST", "0.0.0.0")
        print(f"[arifOS] Starting MCP server with HTTP transport on {host}:{port}", file=sys.stderr)
        mcp.run(transport="http", host=host, port=port)
        return

    if mode == "rest":
        from aaa_mcp.rest import main as rest_main

        print("[arifOS] Starting REST bridge (Starlette + Uvicorn)", file=sys.stderr)
        rest_main()
        return

    print(f"Unknown mode '{mode}'. Use one of: stdio, sse, http, rest", file=sys.stderr)
    raise SystemExit(2)


if __name__ == "__main__":
    main()
