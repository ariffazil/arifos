#!/usr/bin/env python3
"""
aCLIp — arifOS Constitutional Layer Interface (CLI)
Exactly 9 commands for constitutional GitOps, agent governance, and CI.

The 9 Commands:
    1. aclip worktree add <agent> <feature>   Create F1 sandbox
    2. aclip worktree rm <branch>              Collapse → VOID
    3. aclip worktree list                     Show all worktrees
    4. aclip agent run [--stage]               Execute with F7 dry_run
    5. aclip f3 eval [--enforce]               Tri-Witness evaluation
    6. aclip manifest init                     Create arifos.yml from template
    7. aclip ingest local [path]               GitIngest local worktree
    8. aclip ingest remote <github-url>        GitIngest remote repo
    9. aclip ci status                         Check 888_JUDGE CI status

Exit codes:
    0 = Success (verdict executed)
    1 = Config error
    2 = Enforce violated (--enforce with low W₃)

Dependencies:
    - git
    - gitingest (for ingest commands)
    - Existing arifOS toolchain scripts
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

# Constants
ARIFOS_ROOT = Path("/mnt/arifOS")
TOOLCHAIN = ARIFOS_ROOT / "scripts" / "constitutional-gitops"
TEMPLATES = ARIFOS_ROOT / "templates"
VERSION = "2026.03.24"


def run_tool(script_name: str, args: list) -> int:
    """Execute a toolchain script"""
    script_path = TOOLCHAIN / script_name
    if not script_path.exists():
        print(f"❌ Error: {script_name} not found")
        return 1
    result = subprocess.run([str(script_path)] + args)
    return result.returncode


# ═══════════════════════════════════════════════════════════════════
# COMMAND 1-3: worktree (add, rm, list)
# ═══════════════════════════════════════════════════════════════════

def cmd_worktree_add(args):
    """1. aclip worktree add <agent> <feature> — Create F1 sandbox"""
    return run_tool("arifos-worktree-add.sh", [args.agent, args.feature])


def cmd_worktree_rm(args):
    """2. aclip worktree rm <branch> — Collapse universe → VOID"""
    return run_tool("arifos-worktree-remove.sh", [args.branch])


def cmd_worktree_list(args):
    """3. aclip worktree list — Show all constitutional worktrees"""
    result = subprocess.run(["git", "worktree", "list"])
    return result.returncode


# ═══════════════════════════════════════════════════════════════════
# COMMAND 4: agent run
# ═══════════════════════════════════════════════════════════════════

def cmd_agent_run(args):
    """4. aclip agent run [--stage] — Execute with F7 dry_run"""
    stage = args.stage or "dev"
    return run_tool("arifos-agent-run.sh", [stage])


# ═══════════════════════════════════════════════════════════════════
# COMMAND 5: f3 eval
# ═══════════════════════════════════════════════════════════════════

def cmd_f3_eval(args):
    """5. aclip f3 eval [--enforce] — Compute Tri-Witness (F3)"""
    cmd_args = []
    if args.worktree:
        cmd_args.extend(["--worktree", args.worktree])
    if args.mode:
        cmd_args.extend(["--mode", args.mode])
    if args.json:
        cmd_args.append("--json")
    if args.enforce:
        cmd_args.append("--enforce")
    return run_tool("arifos_f3_eval.py", cmd_args)


# ═══════════════════════════════════════════════════════════════════
# COMMAND 6: manifest init
# ═══════════════════════════════════════════════════════════════════

def cmd_manifest_init(args):
    """6. aclip manifest init — Create arifos.yml from template"""
    template_path = TEMPLATES / "arifos.yml.template"
    target_path = Path(args.path) / "arifos.yml"
    
    if not template_path.exists():
        print(f"❌ Template not found: {template_path}")
        return 1
    
    if target_path.exists() and not args.force:
        print(f"⚠️  arifos.yml already exists at {target_path}")
        print("   Use --force to overwrite")
        return 1
    
    try:
        with open(template_path) as f:
            content = f.read()
        
        # Basic template variable substitution
        content = content.replace("CHANGE-ME", f"arifos-{args.agent or 'agent'}-{args.feature or 'feature'}")
        content = content.replace("${AGENT_NAME}", args.agent or "unknown")
        content = content.replace("${FEATURE_NAME}", args.feature or "unknown")
        
        with open(target_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Manifest created: {target_path}")
        print(f"   Agent: {args.agent or 'unknown'}")
        print(f"   Feature: {args.feature or 'unknown'}")
        return 0
    except Exception as e:
        print(f"❌ Error creating manifest: {e}")
        return 1


# ═══════════════════════════════════════════════════════════════════
# COMMAND 7-8: ingest (local, remote)
# ═══════════════════════════════════════════════════════════════════

def cmd_ingest_local(args):
    """7. aclip ingest local [path] — GitIngest local worktree"""
    try:
        from gitingest import ingest
        
        path = args.path or "."
        print(f"🔥 Ingesting local worktree: {path}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        result = ingest(
            path_or_url=path,
            include_patterns=args.include,
            exclude_patterns=args.exclude,
            max_file_size=args.max_size * 1024 if args.max_size else None
        )
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(result)
            print(f"✅ Ingested to: {args.output}")
        else:
            print(result)
        
        return 0
    except ImportError:
        print("❌ gitingest not installed. Run: pip install gitingest")
        return 1
    except Exception as e:
        print(f"❌ Ingest failed: {e}")
        return 1


def cmd_ingest_remote(args):
    """8. aclip ingest remote <github-url> — GitIngest remote repo"""
    try:
        from gitingest import ingest
        
        print(f"🔥 Ingesting remote repo: {args.url}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        result = ingest(
            path_or_url=args.url,
            include_patterns=args.include,
            exclude_patterns=args.exclude,
            max_file_size=args.max_size * 1024 if args.max_size else None
        )
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(result)
            print(f"✅ Ingested to: {args.output}")
        else:
            print(result)
        
        return 0
    except ImportError:
        print("❌ gitingest not installed. Run: pip install gitingest")
        return 1
    except Exception as e:
        print(f"❌ Ingest failed: {e}")
        return 1


# ═══════════════════════════════════════════════════════════════════
# COMMAND 9: ci status
# ═══════════════════════════════════════════════════════════════════

def cmd_ci_status(args):
    """9. aclip ci status — Check 888_JUDGE CI status"""
    print("🔥 888_JUDGE CI Status")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("CI/CD: GitHub Actions")
    print("Workflow: .github/workflows/888-judge.yml")
    print("Status: Active on all PRs to main")
    print("")
    print("Verdicts: SEAL | PROVISIONAL | SABAR | HOLD | HOLD_888 | VOID")
    print("Thresholds: low=0.85 | medium=0.95 | high=0.99 | critical=1.0")
    print("")
    
    # Try to get current branch
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True
        )
        branch = result.stdout.strip()
        if branch:
            print(f"Current branch: {branch}")
            
            # Check if arifos.yml exists
            if Path("arifos.yml").exists():
                print("✅ arifos.yml found — constitutional metadata present")
            else:
                print("⚠️  No arifos.yml — run 'aclip manifest init'")
    except:
        pass
    
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    return 0


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        prog="aclip",
        description="aCLIp — arifOS Constitutional Layer Interface (9 Commands)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
The 9 Commands:
  1. worktree add <agent> <feature>    Create F1 sandbox
  2. worktree rm <branch>              Collapse → VOID
  3. worktree list                     Show worktrees
  4. agent run [--stage]               Execute with F7
  5. f3 eval [--enforce]               Tri-Witness evaluation
  6. manifest init                     Create arifos.yml
  7. ingest local [path]               GitIngest local
  8. ingest remote <url>               GitIngest remote
  9. ci status                         Check 888_JUDGE CI

Constitutional Floors: F1-F13
Tri-Witness: W₃ = (H × A × E)^(1/3)
Exit codes: 0=success, 1=config-error, 2=enforce-violated

Ditempa bukan diberi.
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # ═══════════════════════════════════════════════════════════════
    # 1-3: worktree
    # ═══════════════════════════════════════════════════════════════
    worktree_parser = subparsers.add_parser("worktree", help="Manage F1 sandboxes (1-3)")
    worktree_sub = worktree_parser.add_subparsers(dest="worktree_cmd")
    
    # 1. worktree add
    add_p = worktree_sub.add_parser("add", help="1. Create F1 sandbox")
    add_p.add_argument("agent", help="Agent name (claude, codex, etc.)")
    add_p.add_argument("feature", help="Feature slug")
    add_p.set_defaults(func=cmd_worktree_add)
    
    # 2. worktree rm
    rm_p = worktree_sub.add_parser("rm", help="2. Collapse → VOID")
    rm_p.add_argument("branch", help="Branch name (feature/xxx)")
    rm_p.set_defaults(func=cmd_worktree_rm)
    
    # 3. worktree list
    list_p = worktree_sub.add_parser("list", help="3. Show worktrees")
    list_p.set_defaults(func=cmd_worktree_list)
    
    # ═══════════════════════════════════════════════════════════════
    # 4: agent
    # ═══════════════════════════════════════════════════════════════
    agent_parser = subparsers.add_parser("agent", help="4. Run agent with F7")
    agent_parser.add_argument("--stage", default="dev", help="Stage (dev/prod)")
    agent_parser.set_defaults(func=cmd_agent_run)
    
    # ═══════════════════════════════════════════════════════════════
    # 5: f3
    # ═══════════════════════════════════════════════════════════════
    f3_parser = subparsers.add_parser("f3", help="5. Tri-Witness evaluation")
    f3_sub = f3_parser.add_subparsers(dest="f3_cmd")
    
    eval_p = f3_sub.add_parser("eval", help="Compute W₃ score")
    eval_p.add_argument("-w", "--worktree", default=".", help="Worktree path")
    eval_p.add_argument("-m", "--mode", choices=["pre-push", "pr-draft", "ci"],
                       default="pre-push", help="Mode")
    eval_p.add_argument("-j", "--json", action="store_true", help="JSON output")
    eval_p.add_argument("-e", "--enforce", action="store_true", help="Exit 2 if below threshold")
    eval_p.set_defaults(func=cmd_f3_eval)
    
    # ═══════════════════════════════════════════════════════════════
    # 6: manifest
    # ═══════════════════════════════════════════════════════════════
    manifest_parser = subparsers.add_parser("manifest", help="6. Manage arifos.yml")
    manifest_sub = manifest_parser.add_subparsers(dest="manifest_cmd")
    
    init_p = manifest_sub.add_parser("init", help="Create from template")
    init_p.add_argument("-p", "--path", default=".", help="Target path")
    init_p.add_argument("-a", "--agent", help="Agent name")
    init_p.add_argument("-f", "--feature", help="Feature name")
    init_p.add_argument("--force", action="store_true", help="Overwrite existing")
    init_p.set_defaults(func=cmd_manifest_init)
    
    # ═══════════════════════════════════════════════════════════════
    # 7-8: ingest
    # ═══════════════════════════════════════════════════════════════
    ingest_parser = subparsers.add_parser("ingest", help="7-8. GitIngest for LLMs")
    ingest_sub = ingest_parser.add_subparsers(dest="ingest_cmd")
    
    # 7. ingest local
    local_p = ingest_sub.add_parser("local", help="7. Ingest local worktree")
    local_p.add_argument("path", nargs="?", default=".", help="Path to ingest")
    local_p.add_argument("-i", "--include", action="append", help="Include patterns")
    local_p.add_argument("-e", "--exclude", action="append", help="Exclude patterns")
    local_p.add_argument("-s", "--max-size", type=int, help="Max file size (KB)")
    local_p.add_argument("-o", "--output", help="Output file")
    local_p.set_defaults(func=cmd_ingest_local)
    
    # 8. ingest remote
    remote_p = ingest_sub.add_parser("remote", help="8. Ingest remote repo")
    remote_p.add_argument("url", help="GitHub URL")
    remote_p.add_argument("-i", "--include", action="append", help="Include patterns")
    remote_p.add_argument("-e", "--exclude", action="append", help="Exclude patterns")
    remote_p.add_argument("-s", "--max-size", type=int, help="Max file size (KB)")
    remote_p.add_argument("-o", "--output", help="Output file")
    remote_p.set_defaults(func=cmd_ingest_remote)
    
    # ═══════════════════════════════════════════════════════════════
    # 9: ci
    # ═══════════════════════════════════════════════════════════════
    ci_parser = subparsers.add_parser("ci", help="9. Check 888_JUDGE CI status")
    ci_sub = ci_parser.add_subparsers(dest="ci_cmd")
    
    status_p = ci_sub.add_parser("status", help="Show CI status")
    status_p.set_defaults(func=cmd_ci_status)
    
    # Parse
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
