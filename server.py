"""
Unified arifOS server entrypoint (repo root).

This is the human-friendly wrapper around `python -m aaa_mcp`, matching docs:

    python server.py                  # default: sse
    python server.py --mode rest      # REST bridge (+ /mcp alias + /health)
    python server.py --mode sse       # FastMCP SSE transport
    python server.py --mode http      # FastMCP Streamable HTTP transport
    python server.py --mode stdio     # FastMCP stdio (local clients)

Capabilities exposed by unified server:
- 20 registered MCP tools
- 2 MCP resources (`arifos://templates/full-context`, `arifos://schemas/tooling`)
- 3 MCP prompts for constitutional orchestration
"""

from __future__ import annotations

import argparse
import os
import sys

VALID_MODES = {"rest", "sse", "http", "stdio"}
DEFAULT_MODE = "sse"
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8080


def _normalize_mode(mode: str | None) -> str:
    normalized = (mode or DEFAULT_MODE).strip().lower()
    if normalized not in VALID_MODES:
        print(
            f"[arifOS] invalid ARIFOS_MODE '{mode}', falling back to '{DEFAULT_MODE}'",
            file=sys.stderr,
        )
        return DEFAULT_MODE
    return normalized


def _safe_env_port() -> int:
    raw_port = os.getenv("PORT", str(DEFAULT_PORT)).strip()
    try:
        port = int(raw_port)
    except ValueError:
        print(
            f"[arifOS] invalid PORT '{raw_port}', falling back to {DEFAULT_PORT}",
            file=sys.stderr,
        )
        return DEFAULT_PORT
    return port


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="arifOS Unified Server (root entrypoint)")
    parser.add_argument(
        "--mode",
        choices=sorted(VALID_MODES),
        default=_normalize_mode(os.getenv("ARIFOS_MODE", DEFAULT_MODE)),
        help="Server mode (default: sse)",
    )
    parser.add_argument(
        "--host",
        default=os.getenv("HOST", DEFAULT_HOST),
        help="Bind host (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=_safe_env_port(),
        help="Bind port (default: 8080)",
    )
    return parser


def _validate_network_args(mode: str, host: str, port: int) -> None:
    if mode == "stdio":
        return
    if not host.strip():
        raise SystemExit("[arifOS] host cannot be empty for network transports")
    if port < 1 or port > 65535:
        raise SystemExit(f"[arifOS] invalid port {port}, expected 1-65535")


def main(argv: list[str] | None = None) -> None:
    parser = _build_parser()
    args = parser.parse_args(argv)

    mode = _normalize_mode(args.mode)
    host = args.host.strip() or DEFAULT_HOST
    port = args.port
    _validate_network_args(mode, host, port)

    if mode == "rest":
        from aaa_mcp.rest import main as rest_main

        os.environ["HOST"] = host
        os.environ["PORT"] = str(port)
        print(f"[arifOS] REST bridge on {host}:{port}", file=sys.stderr)
        rest_main()
        return

    from arifos_aaa_mcp.server import create_aaa_mcp_server

    mcp = create_aaa_mcp_server()

    if mode == "stdio":
        print("[arifOS] FastMCP STDIO transport", file=sys.stderr)
        mcp.run(transport="stdio")
        return

    if mode == "sse":
        print(f"[arifOS] FastMCP SSE transport on {host}:{port}", file=sys.stderr)
        mcp.run(transport="sse", host=host, port=port)
        return

    if mode == "http":
        print(f"[arifOS] FastMCP HTTP transport on {host}:{port}", file=sys.stderr)
        mcp.run(transport="http", host=host, port=port)
        return

    raise SystemExit(2)


if __name__ == "__main__":
    main()
