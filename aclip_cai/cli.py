"""
aclip_cai/cli.py
================

Command-line interface for ACLIP_CAI 9-Tool Nervous System.

Usage:
    python -m aclip_cai health
    python -m aclip_cai processes --filter python --limit 20
    python -m aclip_cai fs --path /root/arifOS --pattern "*.py"
    python -m aclip_cai logs --path /var/log/syslog --lines 100
    python -m aclip_cai net --ping google.com
    python -m aclip_cai config --path /root/arifOS/pyproject.toml
    python -m aclip_cai chroma --query "constitutional AI" --collection docs
    python -m aclip_cai cost --type llm --tokens 1000 --model gpt-4
    python -m aclip_cai guard --action deploy --target /app --risk medium
"""

import argparse
import asyncio
import json
import sys
from typing import Any

from .console_tools import (
    chroma_query,
    config_flags,
    cost_estimator,
    forge_guard,
    fs_inspect,
    log_tail,
    net_status,
    process_list,
    system_health,
)


def print_json(data: Any) -> None:
    """Print formatted JSON output."""
    print(json.dumps(data, indent=2, default=str))


async def cmd_health(args: argparse.Namespace) -> None:
    """System health command."""
    result = await system_health(
        include_swap=args.swap,
        include_io=args.io,
        include_temp=args.temp,
    )
    print_json(result.to_dict())


async def cmd_processes(args: argparse.Namespace) -> None:
    """Process list command."""
    result = await process_list(
        filter_name=args.filter,
        filter_user=args.user,
        min_cpu_percent=args.min_cpu,
        min_memory_mb=args.min_mem,
        limit=args.limit,
        include_threads=args.threads,
    )
    print_json(result.to_dict())


async def cmd_fs(args: argparse.Namespace) -> None:
    """Filesystem inspect command."""
    result = await fs_inspect(
        path=args.path,
        max_depth=args.depth,
        include_hidden=args.hidden,
        min_size_bytes=args.min_size,
        pattern=args.pattern,
        max_files=args.max_files,
    )
    print_json(result.to_dict())


async def cmd_logs(args: argparse.Namespace) -> None:
    """Log tail command."""
    result = await log_tail(
        log_path=args.path,
        lines=args.lines,
        grep_pattern=args.grep,
        since_minutes=args.since,
    )
    print_json(result.to_dict())


async def cmd_net(args: argparse.Namespace) -> None:
    """Network status command."""
    result = await net_status(
        check_interfaces=args.interfaces,
        check_connections=args.connections,
        check_routing=args.routing,
        target_host=args.ping,
    )
    print_json(result.to_dict())


async def cmd_config(args: argparse.Namespace) -> None:
    """Config flags command."""
    result = await config_flags(
        config_path=args.path,
        env_prefix=args.prefix,
        include_secrets=args.secrets,
    )
    print_json(result.to_dict())


async def cmd_chroma(args: argparse.Namespace) -> None:
    """ChromaDB query command."""
    result = await chroma_query(
        query_text=args.query,
        collection_name=args.collection,
        n_results=args.results,
        where_filter=json.loads(args.where) if args.where else None,
        include_embeddings=args.embeddings,
    )
    print_json(result.to_dict())


async def cmd_cost(args: argparse.Namespace) -> None:
    """Cost estimator command."""
    result = await cost_estimator(
        operation_type=args.type,
        token_count=args.tokens,
        compute_seconds=args.compute,
        storage_gb=args.storage,
        api_calls=args.calls,
        provider=args.provider,
        model=args.model,
    )
    print_json(result.to_dict())


async def cmd_guard(args: argparse.Namespace) -> None:
    """Forge guard command."""
    result = await forge_guard(
        action=args.action,
        target=args.target,
        session_id=args.session or f"cli-{id(args)}",
        risk_level=args.risk,
        justification=args.justify,
        dry_run=not args.execute,
        require_approval=args.approve,
    )
    print_json(result.to_dict())


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="aclip_cai",
        description="ACLIP_CAI — arifOS Console Intelligence & Perception Console",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s health                    # Full system health check
  %(prog)s processes --filter python # List Python processes
  %(prog)s fs --path /root/arifOS    # Inspect filesystem
  %(prog)s logs --path /var/log/syslog --grep "error" --lines 20
  %(prog)s net --ping 8.8.8.8        # Network diagnostics
  %(prog)s config --path .env        # Inspect config
  %(prog)s chroma --query "AI safety" # Vector search
  %(prog)s cost --type llm --tokens 1000  # Cost estimate
  %(prog)s guard --action deploy --target /app --risk medium
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Health command
    health_p = subparsers.add_parser("health", help="System health metrics")
    health_p.add_argument("--swap", action="store_true", default=True, help="Include swap info")
    health_p.add_argument("--io", action="store_true", help="Include I/O stats")
    health_p.add_argument("--temp", action="store_true", help="Include thermal readings")

    # Processes command
    proc_p = subparsers.add_parser("processes", help="List system processes")
    proc_p.add_argument("--filter", "-f", help="Filter by process name")
    proc_p.add_argument("--user", "-u", help="Filter by username")
    proc_p.add_argument("--min-cpu", type=float, default=0.0, help="Min CPU %")
    proc_p.add_argument("--min-mem", type=float, default=0.0, help="Min memory MB")
    proc_p.add_argument("--limit", "-n", type=int, default=50, help="Max results")
    proc_p.add_argument("--threads", action="store_true", help="Include thread count")

    # Filesystem command
    fs_p = subparsers.add_parser("fs", help="Inspect filesystem")
    fs_p.add_argument("--path", "-p", default="/root/arifOS", help="Root path")
    fs_p.add_argument("--depth", "-d", type=int, default=2, help="Max depth")
    fs_p.add_argument("--hidden", action="store_true", help="Include hidden files")
    fs_p.add_argument("--min-size", type=int, default=0, help="Min file size bytes")
    fs_p.add_argument("--pattern", help="Glob pattern (e.g., *.py)")
    fs_p.add_argument("--max-files", type=int, default=100, help="Max files")

    # Logs command
    logs_p = subparsers.add_parser("logs", help="Tail and search logs")
    logs_p.add_argument("--path", "-p", required=True, help="Log file path")
    logs_p.add_argument("--lines", "-n", type=int, default=50, help="Number of lines")
    logs_p.add_argument("--grep", "-g", help="Filter pattern (regex)")
    logs_p.add_argument("--since", type=int, help="Minutes since now")

    # Network command
    net_p = subparsers.add_parser("net", help="Network diagnostics")
    net_p.add_argument("--interfaces", action="store_true", default=True, help="Show interfaces")
    net_p.add_argument("--connections", action="store_true", default=True, help="Show connections")
    net_p.add_argument("--routing", action="store_true", default=True, help="Show routing")
    net_p.add_argument("--ping", help="Ping target host")

    # Config command
    cfg_p = subparsers.add_parser("config", help="Inspect configuration")
    cfg_p.add_argument("--path", "-p", help="Config file path")
    cfg_p.add_argument("--prefix", default="ARIFOS", help="Env var prefix")
    cfg_p.add_argument("--secrets", action="store_true", help="Show secrets (caution)")

    # Chroma command
    chroma_p = subparsers.add_parser("chroma", help="Query ChromaDB")
    chroma_p.add_argument("--query", "-q", required=True, help="Search text")
    chroma_p.add_argument("--collection", "-c", default="default", help="Collection name")
    chroma_p.add_argument("--results", "-n", type=int, default=5, help="Result count")
    chroma_p.add_argument("--where", "-w", help="JSON metadata filter")
    chroma_p.add_argument("--embeddings", action="store_true", help="Include embeddings")

    # Cost command
    cost_p = subparsers.add_parser("cost", help="Cost estimation")
    cost_p.add_argument(
        "--type",
        "-t",
        required=True,
        choices=["llm", "embedding", "storage", "compute"],
        help="Operation type",
    )
    cost_p.add_argument("--tokens", type=int, help="Token count")
    cost_p.add_argument("--compute", type=float, help="Compute seconds")
    cost_p.add_argument("--storage", type=float, help="Storage GB")
    cost_p.add_argument("--calls", type=int, help="API call count")
    cost_p.add_argument("--provider", default="openai", help="LLM provider")
    cost_p.add_argument("--model", "-m", default="gpt-4", help="Model name")

    # Guard command
    guard_p = subparsers.add_parser("guard", help="Forge guard gating")
    guard_p.add_argument("--action", "-a", required=True, help="Action to evaluate")
    guard_p.add_argument("--target", "-t", required=True, help="Target resource")
    guard_p.add_argument("--session", "-s", help="Session ID")
    guard_p.add_argument(
        "--risk",
        "-r",
        default="low",
        choices=["low", "medium", "high", "critical"],
        help="Risk level",
    )
    guard_p.add_argument("--justify", "-j", default="", help="Justification")
    guard_p.add_argument("--execute", action="store_true", help="Actually execute (not dry-run)")
    guard_p.add_argument("--approve", action="store_true", help="Require approval")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Dispatch to handler
    handlers = {
        "health": cmd_health,
        "processes": cmd_processes,
        "fs": cmd_fs,
        "logs": cmd_logs,
        "net": cmd_net,
        "config": cmd_config,
        "chroma": cmd_chroma,
        "cost": cmd_cost,
        "guard": cmd_guard,
    }

    handler = handlers.get(args.command)
    if handler:
        asyncio.run(handler(args))
        return 0
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
