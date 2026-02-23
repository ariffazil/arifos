"""CLI entrypoint for arifOS AAA MCP."""

from __future__ import annotations

import os
import sys

from .fastmcp_ext.transports import run_server


def main() -> None:
    mode = (sys.argv[1] if len(sys.argv) > 1 else os.getenv("AAA_MCP_TRANSPORT", "sse")).lower()
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))

    from .server import create_aaa_mcp_server

    mcp = create_aaa_mcp_server()

    try:
        run_server(mcp, mode=mode, host=host, port=port)
    except ValueError as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
