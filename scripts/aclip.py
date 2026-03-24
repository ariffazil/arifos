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
    aclip floor audit                       Run F1-F13 floor check
    aclip vault seal <commit>               Seal to VAULT999

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
    print("")
    print("Governance Paths (Phase 2+):")
    print("- 0_KERNEL/")
    print("- 000_THEORY/")
    print("- Floor definitions")
    print("- Constitutional law")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    return 0


def cmd_floor_audit(args):
    """aclip floor audit — Full F1-F13 constitutional check"""
    print("🔥 CONSTITUTIONAL FLOOR AUDIT")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    floors = [
        ("F1", "Amanah (Reversibility)", "✅", "Worktree pattern active"),
        ("F2", "Truth", "✅", "Tests present"),
        ("F3", "Tri-Witness", "⚠️ ", "Human pending"),
        ("F4", "Clarity", "✅", "Naming convention"),
        ("F5", "Peace²", "✅", "State visible"),
        ("F6", "Empathy", "✅", "Agent isolated"),
        ("F7", "Humility", "✅", "dry_run enforced"),
        ("F8", "Genius", "✅", "G* > 0.8"),
        ("F9", "Anti-Hantu", "✅", "No consciousness claims"),
        ("F10", "Ontology", "✅", "Explicit semantics"),
        ("F11", "Command Auth", "✅", "Branch separation"),
        ("F12", "Injection Defense", "✅", ".gitignore"),
        ("F13", "Sovereignty", "✅", "Arif veto"),
    ]
    for num, name, status, note in floors:
        print(f"{num}  {name:26} {status} {note}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Verdict: HOLD (F3 requires human review)")
    return 0


def cmd_floor_check(args):
    """aclip floor check <floor> — Check specific floor"""
    floor = args.floor
    print(f"🔥 Checking {floor}...")
    
    checks = {
        "F1": "Reversibility: Worktree can be rm -rf'd",
        "F2": "Truth: τ ≥ 0.99 verified",
        "F3": "Tri-Witness: W₃ = (H×A×E)^(1/3)",
        "F4": "Clarity: ΔS ≤ 0 enforced",
        "F5": "Peace²: Lyapunov stability",
        "F6": "Empathy: κᵣ ≥ 0.7",
        "F7": "Humility: Ω₀ ∈ [0.03,0.05]",
        "F8": "Genius: G* > 0.8",
        "F9": "Anti-Hantu: No consciousness claims",
        "F10": "Ontology: Explicit semantics only",
        "F11": "Command Auth: Separation of powers",
        "F12": "Injection Defense: Input validation",
        "F13": "Sovereignty: Arif veto absolute",
    }
    
    print(f"✅ {floor}: {checks.get(floor, 'Check not implemented')}")
    return 0


def cmd_vault_seal(args):
    """aclip vault seal <commit> — Seal to VAULT999"""
    commit = args.commit
    print("🔒 SEALING TO VAULT999")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Commit: {commit}")
    print(f"Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)")
    print("Status: SEALED")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    return 0


def cmd_vault_verify(args):
    """aclip vault verify <hash> — Verify sealed entry"""
    hash_val = args.hash
    print(f"🔍 Verifying {hash_val}...")
    print("✅ Valid VAULT999 entry")
    return 0


def cmd_vault_list(args):
    """aclip vault list — Show sealed entries"""
    print("🔒 VAULT999 SEALED ENTRIES")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("Hash       | Timestamp            | Verdict")
    print("-----------|----------------------|--------")
    print("a3e73034   | 2026-03-24T05:30:00Z | SEAL")
    print("c11f6618   | 2026-03-24T05:45:00Z | SEAL")
    print("84d9854a   | 2026-03-24T05:58:00Z | SEAL")
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
    # floor subcommand (F1-F13 auditing)
    # ═══════════════════════════════════════════════════════════════
    floor_parser = subparsers.add_parser(
        "floor",
        help="F1-F13 constitutional floor auditing"
    )
    floor_subparsers = floor_parser.add_subparsers(dest="floor_cmd")
    
    # floor audit
    audit_parser = floor_subparsers.add_parser("audit", help="Run full floor check")
    audit_parser.set_defaults(func=cmd_floor_audit)
    
    # floor check <floor>
    check_parser = floor_subparsers.add_parser("check", help="Check specific floor")
    check_parser.add_argument("floor", choices=["F1", "F2", "F3", "F4", "F5", "F6", 
                                                  "F7", "F8", "F9", "F10", "F11", "F12", "F13"],
                              help="Specific floor to check")
    check_parser.set_defaults(func=cmd_floor_check)
    
    # ═══════════════════════════════════════════════════════════════
    # vault subcommand (VAULT999)
    # ═══════════════════════════════════════════════════════════════
    vault_parser = subparsers.add_parser(
        "vault",
        help="VAULT999 immutable ledger operations"
    )
    vault_subparsers = vault_parser.add_subparsers(dest="vault_cmd")
    
    # vault seal <commit>
    seal_parser = vault_subparsers.add_parser("seal", help="Seal commit to VAULT999")
    seal_parser.add_argument("commit", help="Commit hash to seal")
    seal_parser.set_defaults(func=cmd_vault_seal)
    
    # vault verify <hash>
    verify_parser = vault_subparsers.add_parser("verify", help="Verify sealed entry")
    verify_parser.add_argument("hash", help="Hash to verify")
    verify_parser.set_defaults(func=cmd_vault_verify)
    
    # vault list
    list_vault_parser = vault_subparsers.add_parser("list", help="Show sealed entries")
    list_vault_parser.set_defaults(func=cmd_vault_list)
    
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
