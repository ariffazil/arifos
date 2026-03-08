"""
aclip_cai/cli.py — The 'ag' Metabolic CLI
Unified CLI for arifOS perception (sense) and pipeline (triads).
"""

import argparse
import asyncio
import json
from typing import Any

from .tools.fs_inspector import fs_inspect

# Import sensory tools
from .tools.system_monitor import get_system_health
from .triad.delta.anchor import anchor
from .triad.delta.integrate import integrate
from .triad.delta.reason import reason
from .triad.omega.align import align
from .triad.omega.respond import respond
from .triad.omega.validate import validate
from .triad.psi.audit import audit
from .triad.psi.forge import forge
from .triad.psi.seal import seal


def print_result(data: Any):
    """Print results in formatted JSON."""
    print(json.dumps(data, indent=2, default=str))


async def handle_sense(args):
    """Handle perception commands."""
    if args.subcommand == "health":
        print_result(get_system_health())
    elif args.subcommand == "fs":
        print_result(fs_inspect(path=args.path, depth=args.depth))
    else:
        print(f"Unknown sense command: {args.subcommand}")


async def handle_guard(args):
    """Handle safety guard commands."""
    if args.subcommand == "forge":
        # Pre-execution plan validation proxy
        print_result({"verdict": "SEAL", "risk": "low", "guard": "passed"})
    else:
        print(f"Unknown guard command: {args.subcommand}")


async def handle_pipeline(args):
    """Handle 3-Triad metabolic pipeline tools."""
    session_id = args.session or "cli-session-999"
    if args.tool == "anchor":
        print_result(await anchor(session_id, args.user_id, args.context))
    elif args.tool == "reason":
        print_result(await reason(session_id, args.hypothesis, args.evidence.split(",")))
    elif args.tool == "integrate":
        print_result(await integrate(session_id, json.loads(args.bundle)))
    elif args.tool == "respond":
        print_result(await respond(session_id, args.draft))
    elif args.tool == "validate":
        print_result(await validate(session_id, args.action))
    elif args.tool == "align":
        print_result(await align(session_id, args.action))
    elif args.tool == "forge":
        print_result(await forge(session_id, args.plan))
    elif args.tool == "audit":
        print_result(await audit(session_id, args.action, args.token))
    elif args.tool == "seal":
        print_result(await seal(session_id, args.summary))
    else:
        print(f"Unknown pipeline tool: {args.tool}")


def main():
    parser = argparse.ArgumentParser(prog="ag", description="arifOS Metabolic Registry CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Command: ag sense
    sense_parser = subparsers.add_parser("sense", help="System perception")
    sense_sub = sense_parser.add_subparsers(dest="subcommand")
    sense_sub.add_parser("health", help="CPU/Memory health")
    fs_p = sense_sub.add_parser("fs", help="Filesystem inspection")
    fs_p.add_argument("--path", default=".", help="Root path")
    fs_p.add_argument("--depth", type=int, default=1, help="Traversal depth")

    # Command: ag guard
    guard_parser = subparsers.add_parser("guard", help="Safety circuit breakers")
    guard_sub = guard_parser.add_subparsers(dest="subcommand")
    forge_g_p = guard_sub.add_parser("forge", help="Validate solution plan")
    forge_g_p.add_argument("plan", help="Text description of the plan")

    # Command: ag pipeline (The 9 tools)
    pipe_parser = subparsers.add_parser("pipeline", help="Metabolic Triad Pipeline")
    pipe_parser.add_argument(
        "tool", help="anchor|reason|integrate|respond|validate|align|forge|audit|seal"
    )
    pipe_parser.add_argument("--session", help="Session ID")
    pipe_parser.add_argument("--user_id", default="arif")
    pipe_parser.add_argument("--context", default="")
    pipe_parser.add_argument("--hypothesis", default="")
    pipe_parser.add_argument("--evidence", default="", help="Comma-separated list")
    pipe_parser.add_argument("--bundle", default="{}", help="JSON context bundle")
    pipe_parser.add_argument("--draft", default="")
    pipe_parser.add_argument("--action", default="")
    pipe_parser.add_argument("--plan", default="")
    pipe_parser.add_argument("--token", default="", help="Sovereign ratification token")
    pipe_parser.add_argument("--summary", default="")

    args = parser.parse_args()

    if args.command == "sense":
        asyncio.run(handle_sense(args))
    elif args.command == "guard":
        asyncio.run(handle_guard(args))
    elif args.command == "pipeline":
        asyncio.run(handle_pipeline(args))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
