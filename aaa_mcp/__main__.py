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


def check_fastmcp_version():
    """Verify FastMCP version compatibility."""
    try:
        import fastmcp
        version = getattr(fastmcp, '__version__', 'unknown')
        print(f"[arifOS] FastMCP version: {version}", file=sys.stderr)
        
        # Parse major version
        major = int(version.split('.')[0]) if version != 'unknown' else 0
        if major < 2:
            print(f"[arifOS] ⚠️  WARNING: FastMCP {version} detected. Version 2.x+ required for full functionality.", file=sys.stderr)
            print(f"[arifOS] Some features (like /health endpoint) may not work correctly.", file=sys.stderr)
        else:
            print(f"[arifOS] ✓ FastMCP {version} - Full functionality available", file=sys.stderr)
        return major
    except Exception as e:
        print(f"[arifOS] ⚠️  Could not check FastMCP version: {e}", file=sys.stderr)
        return 0


def main():
    # Check version before importing server
    fastmcp_major = check_fastmcp_version()
    
    mode = (sys.argv[1] if len(sys.argv) > 1 else "stdio").strip().lower()

    from .server import mcp

    if mode in ("", "stdio"):
        # Default to stdio for local agents
        mcp.run(transport="stdio")
        return

    if mode == "sse":
        port = int(os.getenv("PORT", 8080))
        host = os.getenv("HOST", "0.0.0.0")
        print(f"[arifOS] Starting MCP server with SSE transport on {host}:{port}", file=sys.stderr)

        # Railway terminates TLS at proxy and sets X-Forwarded-Proto.
        # We need uvicorn to trust these headers so SSE endpoint
        # advertises https:// URLs, not http://.
        import uvicorn
        from fastmcp.server.http import create_sse_app

        app = create_sse_app(mcp, message_path="/messages", sse_path="/sse")
        uvicorn.run(
            app,
            host=host,
            port=port,
            proxy_headers=True,
            forwarded_allow_ips="*",
        )
        return

    if mode in ("http", "streamable-http"):
        port = int(os.getenv("PORT", 8080))
        host = os.getenv("HOST", "0.0.0.0")
        print(f"[arifOS] Starting MCP server with HTTP transport on {host}:{port}", file=sys.stderr)
        mcp.run(transport="http", host=host, port=port)
        return

    print(f"Unknown mode '{mode}'. Use one of: stdio, sse, http", file=sys.stderr)
    raise SystemExit(2)


if __name__ == "__main__":
    main()
