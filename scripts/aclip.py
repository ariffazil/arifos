#!/usr/bin/env python3
"""
aclip — arifOS Constitutional Layer Interface (CLI)
Unified CLI for constitutional GitOps, agent management, and governance.

Usage:
    aclip worktree add <agent> <feature>    Create F1 sandbox
    aclip worktree rm <branch>              Collapse → VOID
    aclip agent run [stage]                 Execute with F7 dry_run
    aclip f3 eval [--worktree .]            Tri-Witness evaluation
    aclip judge status                      Check 888_JUDGE CI status

Exit codes:
    0 = Success (verdict executed)
    1 = Config error
    2 = Enforce violated (--enforce with low W₃)
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Constants
ARIFOS_ROOT = Path("/mnt/arifOS")
TOOLCHAIN = ARIFOS_ROOT / "scripts" / "constitutional-gitops"
VERSION = "2026.03.24"


def run_script(script_name: str, args: list) -> int:
    """Execute a toolchain script with arguments"""
    script_path = TOOLCHAIN / script_name
    if not script_path.exists():
        print(f"❌ Error: {script_name} not found at {script_path}")
        return 1
    
    cmd = [str(script_path)] + args
    result = subprocess.run(cmd)
    return result.returncode


# ═══════════════════════════════════════════════════════════════════
# SUBCOMMANDS
# ═══════════════════════════════════════════════════════════════════

def cmd_worktree_add(args):
    """aclip worktree add <agent> <feature>"""
    return run_script("arifos-worktree-add.sh", [args.agent, args.feature])


def cmd_worktree_rm(args):
    """aclip worktree rm <branch>"""
    return run_script("arifos-worktree-remove.sh", [args.branch])


def cmd_worktree_list(args):
    """aclip worktree list"""
    result = subprocess.run(["git", "worktree", "list"])
    return result.returncode


def cmd_agent_run(args):
    """aclip agent run [stage]"""
    stage = args.stage or "dev"
    return run_script("arifos-agent-run.sh", [stage])


def cmd_f3_eval(args):
    """aclip f3 eval [--worktree PATH] [--mode MODE] [--json] [--enforce]"""
    cmd_args = []
    if args.worktree:
        cmd_args.extend(["--worktree", args.worktree])
    if args.mode:
        cmd_args.extend(["--mode", args.mode])
    if args.json:
        cmd_args.append("--json")
    if args.enforce:
        cmd_args.append("--enforce")
    if args.update_manifest:
        cmd_args.append("--update-manifest")
    
    return run_script("arifos_f3_eval.py", cmd_args)


def cmd_judge_status(args):
    """aclip judge status — Check CI/CD governance status"""
    print("🔥 888_JUDGE Status")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("CI/CD: GitHub Actions")
    print("Workflow: .github/workflows/888-judge.yml")
    print("Status: Active on all PRs to main")
    print("")
    print("Verdicts: SEAL | PROVISIONAL | SABAR | HOLD | HOLD_888 | VOID")
    print("Thresholds: low=0.85 | medium=0.95 | high=0.99 | critical=1.0")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    return 0


def cmd_version(args):
    """aclip version"""
    print(f"aclip (arifOS Constitutional Layer Interface) {VERSION}")
    print(f"Location: {ARIFOS_ROOT}")
    print(f"Toolchain: {TOOLCHAIN}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="aclip",
        description="arifOS Constitutional Layer Interface (CLI) — GitOps for AI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  aclip worktree add claude api-refactor    # Create F1 sandbox
  aclip worktree rm feature/claude-api      # Collapse → VOID
  aclip f3 eval --enforce                   # Evaluate with blocking
  aclip agent run --stage prod              # Run agent with F7

Constitutional Floors: F1-F13
Tri-Witness: W₃ = (H × A × E)^(1/3)
Exit codes: 0=success, 1=config-error, 2=enforce-violated

Ditempa bukan diberi.
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # ═══════════════════════════════════════════════════════════════
    # worktree subcommand
    # ═══════════════════════════════════════════════════════════════
    worktree_parser = subparsers.add_parser(
        "worktree", 
        help="Manage constitutional sandboxes (F1)"
    )
    worktree_subparsers = worktree_parser.add_subparsers(dest="worktree_cmd")
    
    # worktree add
    add_parser = worktree_subparsers.add_parser("add", help="Create F1 sandbox")
    add_parser.add_argument("agent", help="Agent name (e.g., claude, codex)")
    add_parser.add_argument("feature", help="Feature slug (e.g., api-refactor)")
    add_parser.set_defaults(func=cmd_worktree_add)
    
    # worktree rm
    rm_parser = worktree_subparsers.add_parser("rm", help="Collapse universe → VOID")
    rm_parser.add_argument("branch", help="Branch name (e.g., feature/claude-api)")
    rm_parser.set_defaults(func=cmd_worktree_rm)
    
    # worktree list
    list_parser = worktree_subparsers.add_parser("list", help="List all worktrees")
    list_parser.set_defaults(func=cmd_worktree_list)
    
    # ═══════════════════════════════════════════════════════════════
    # agent subcommand
    # ═══════════════════════════════════════════════════════════════
    agent_parser = subparsers.add_parser(
        "agent",
        help="Run agents under F7 (Humility)"
    )
    agent_parser.add_argument(
        "stage",
        nargs="?",
        default="dev",
        help="Execution stage (dev/prod) [default: dev]"
    )
    agent_parser.set_defaults(func=cmd_agent_run)
    
    # ═══════════════════════════════════════════════════════════════
    # f3 subcommand (Tri-Witness)
    # ═══════════════════════════════════════════════════════════════
    f3_parser = subparsers.add_parser(
        "f3",
        help="Tri-Witness evaluation (F3)"
    )
    f3_subparsers = f3_parser.add_subparsers(dest="f3_cmd")
    
    # f3 eval
    eval_parser = f3_subparsers.add_parser("eval", help="Compute W₃ score")
    eval_parser.add_argument("-w", "--worktree", default=".", help="Worktree path")
    eval_parser.add_argument("-m", "--mode", choices=["pre-push", "pr-draft", "ci"],
                            default="pre-push", help="Evaluation mode")
    eval_parser.add_argument("-j", "--json", action="store_true", help="JSON output")
    eval_parser.add_argument("-e", "--enforce", action="store_true",
                            help="Exit 2 if W₃ below threshold")
    eval_parser.add_argument("-u", "--update-manifest", action="store_true",
                            help="Write results to arifos.yml")
    eval_parser.set_defaults(func=cmd_f3_eval)
    
    # ═══════════════════════════════════════════════════════════════
    # judge subcommand (888_JUDGE)
    # ═══════════════════════════════════════════════════════════════
    judge_parser = subparsers.add_parser(
        "judge",
        help="888_JUDGE CI/CD governance"
    )
    judge_subparsers = judge_parser.add_subparsers(dest="judge_cmd")
    
    # judge status
    status_parser = judge_subparsers.add_parser("status", help="Check CI status")
    status_parser.set_defaults(func=cmd_judge_status)
    
    # ═══════════════════════════════════════════════════════════════
    # version subcommand
    # ═══════════════════════════════════════════════════════════════
    version_parser = subparsers.add_parser("version", help="Show version")
    version_parser.set_defaults(func=cmd_version)
    
    # Parse and execute
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    if hasattr(args, "func"):
        return args.func(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
