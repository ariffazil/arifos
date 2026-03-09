#!/usr/bin/env python3
"""
OpenClaw Doctor & Troubleshooter Skill for AGI-OpenCode

This tool provides comprehensive OpenClaw diagnostics, troubleshooting,
and automated fixes for the OpenClaw gateway running in Docker.

Usage:
    python openclaw_doctor.py [command] [options]

Commands:
    health      - Quick health check
    diagnose    - Full diagnostic run
    fix         - Auto-fix common issues
    logs        - Tail logs
    telegram    - Check/fix Telegram channel
    security    - Run security audit
    reset       - Reset sessions/config
    status      - Full status report
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass

CONTAINER_NAME = "openclaw_gateway"


@dataclass
class HealthStatus:
    """Health check results."""

    healthy: bool
    gateway_running: bool
    telegram_configured: bool
    telegram_connected: bool
    errors: list[str]
    warnings: list[str]


def run_docker_command(cmd: list[str], capture: bool = True) -> tuple[int, str, str]:
    """Run a docker exec command inside OpenClaw container."""

    full_cmd = ["docker", "exec", CONTAINER_NAME] + cmd
    try:
        result = subprocess.run(
            full_cmd,
            capture_output=capture,
            text=True,
            timeout=30,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"
    except Exception as e:
        return 1, "", str(e)


def check_container_running() -> bool:
    """Check if OpenClaw container is running."""

    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", f"name={CONTAINER_NAME}", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return CONTAINER_NAME in result.stdout
    except Exception:
        return False


def health_check() -> HealthStatus:
    """Perform comprehensive health check."""

    errors = []
    warnings = []

    # Check container
    if not check_container_running():
        errors.append(f"❌ Container {CONTAINER_NAME} is not running")
        return HealthStatus(
            healthy=False,
            gateway_running=False,
            telegram_configured=False,
            telegram_connected=False,
            errors=errors,
            warnings=warnings,
        )

    # Check gateway health endpoint
    code, stdout, stderr = run_docker_command(["curl", "-fsS", "http://localhost:18789/healthz"])
    gateway_running = code == 0 and '"ok":true' in stdout

    if not gateway_running:
        errors.append("❌ Gateway health check failed")

    # Check Telegram config
    code, stdout, stderr = run_docker_command(["openclaw", "config", "get", "channels"])
    try:
        config = json.loads(stdout) if stdout else {}
        telegram_configured = "telegram" in config
        if not telegram_configured:
            errors.append("❌ Telegram not configured")
    except json.JSONDecodeError:
        telegram_configured = False
        errors.append("❌ Could not parse channel config")

    # Check Telegram connection
    code, stdout, stderr = run_docker_command(["openclaw", "channels", "status", "--probe"])
    telegram_connected = "Telegram" in stdout and "running" in stdout

    if telegram_configured and not telegram_connected:
        warnings.append("⚠️ Telegram configured but not connected")

    healthy = gateway_running and telegram_configured and telegram_connected

    return HealthStatus(
        healthy=healthy,
        gateway_running=gateway_running,
        telegram_configured=telegram_configured,
        telegram_connected=telegram_connected,
        errors=errors,
        warnings=warnings,
    )


def print_health_report(status: HealthStatus) -> None:
    """Print formatted health report."""

    print("\n" + "=" * 60)
    print("🩺 OPENCLAW HEALTH REPORT")
    print("=" * 60)

    if status.healthy:
        print("\n✅ OVERALL STATUS: HEALTHY")
    else:
        print("\n❌ OVERALL STATUS: UNHEALTHY")

    print(f"\nGateway Running: {'✅' if status.gateway_running else '❌'}")
    print(f"Telegram Configured: {'✅' if status.telegram_configured else '❌'}")
    print(f"Telegram Connected: {'✅' if status.telegram_connected else '❌'}")

    if status.errors:
        print("\n❌ ERRORS:")
        for error in status.errors:
            print(f"   {error}")

    if status.warnings:
        print("\n⚠️ WARNINGS:")
        for warning in status.warnings:
            print(f"   {warning}")

    print("\n" + "=" * 60)


def cmd_health() -> int:
    """Quick health check command."""

    status = health_check()
    print_health_report(status)
    return 0 if status.healthy else 1


def cmd_diagnose() -> int:
    """Full diagnostic run."""

    print("\n🔍 Running full diagnostics...\n")

    # Container check
    print("1. Container Status:")
    if check_container_running():
        print("   ✅ Container is running")
    else:
        print("   ❌ Container is NOT running")
        print("\n💡 Fix: docker-compose up -d openclaw")
        return 1

    # Gateway status
    print("\n2. Gateway Status:")
    code, stdout, stderr = run_docker_command(["openclaw", "gateway", "status"])
    if code == 0:
        print("   ✅ Gateway status retrieved")
        # Extract key info
        if "RPC probe: ok" in stdout:
            print("   ✅ RPC probe: OK")
        elif "RPC probe: failed" in stdout:
            print("   ❌ RPC probe: FAILED")
    else:
        print(f"   ❌ Failed to get gateway status: {stderr}")

    # Doctor check
    print("\n3. Doctor Diagnostics:")
    code, stdout, stderr = run_docker_command(["openclaw", "doctor"])
    if code == 0:
        print("   ✅ Doctor check passed")
        if "Telegram: ok" in stdout:
            print("   ✅ Telegram: OK")
        elif "Telegram:" in stdout:
            print("   ⚠️ Telegram status needs attention")
    else:
        print(f"   ❌ Doctor check failed: {stderr}")

    # Channel status
    print("\n4. Channel Status:")
    code, stdout, stderr = run_docker_command(["openclaw", "channels", "status", "--probe"])
    if code == 0:
        if "Telegram" in stdout:
            print("   ✅ Telegram channel found")
            if "running" in stdout:
                print("   ✅ Telegram is running")
            else:
                print("   ⚠️ Telegram not running")
        else:
            print("   ❌ No Telegram channel configured")
    else:
        print(f"   ❌ Failed to check channels: {stderr}")

    print("\n" + "=" * 60)
    print("Diagnosis complete!")
    print("=" * 60)

    return 0


def cmd_logs(follow: bool = False, limit: int = 100) -> int:
    """View OpenClaw logs."""

    print(f"\n📊 OpenClaw Logs {'(following...)' if follow else ''}\n")

    if follow:
        # For follow mode, we need to stream directly
        cmd = ["docker", "logs", "-f", CONTAINER_NAME]
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            print("\n\nStopped following logs.")
    else:
        cmd = ["openclaw", "logs", "--limit", str(limit)]
        code, stdout, stderr = run_docker_command(cmd)
        if code == 0:
            print(stdout)
        else:
            print(f"❌ Failed to get logs: {stderr}")
            return 1

    return 0


def cmd_fix() -> int:
    """Auto-fix common issues."""

    print("\n🔧 Running auto-fix...\n")

    fixes_applied = []

    # 1. Check and fix config permissions
    print("1. Checking config permissions...")
    code, stdout, stderr = run_docker_command(["stat", "-c", "%a", "/root/.openclaw/openclaw.json"])
    if code == 0 and stdout.strip() != "600":
        print("   Fixing config permissions...")
        run_docker_command(["chmod", "600", "/root/.openclaw/openclaw.json"])
        fixes_applied.append("Config permissions fixed (600)")
    else:
        print("   ✅ Config permissions OK")

    # 2. Check Telegram config
    print("\n2. Checking Telegram configuration...")
    code, stdout, stderr = run_docker_command(["openclaw", "config", "get", "channels"])
    try:
        config = json.loads(stdout) if stdout else {}
        if "telegram" not in config:
            print("   ❌ Telegram not configured")
            print("\n💡 To fix Telegram, restore from backup:")
            print(
                "   docker exec openclaw_gateway cp /root/.openclaw/openclaw.json.backup /root/.openclaw/openclaw.json"
            )
            print("   docker restart openclaw_gateway")
        else:
            print("   ✅ Telegram configured")
    except json.JSONDecodeError:
        print("   ❌ Could not parse config")

    # 3. Run doctor with --fix
    print("\n3. Running doctor with auto-fix...")
    code, stdout, stderr = run_docker_command(["openclaw", "doctor", "--fix"])
    if code == 0:
        print("   ✅ Doctor fixes applied")
        fixes_applied.append("Doctor auto-fixes applied")
    else:
        print(f"   ⚠️ Doctor had issues: {stderr}")

    print("\n" + "=" * 60)
    if fixes_applied:
        print("✅ Fixes Applied:")
        for fix in fixes_applied:
            print(f"   • {fix}")
    else:
        print("ℹ️ No fixes needed - all checks passed")
    print("=" * 60)

    return 0


def cmd_security() -> int:
    """Run security audit."""

    print("\n🔐 Running Security Audit...\n")

    code, stdout, stderr = run_docker_command(["openclaw", "security", "audit", "--deep"])
    if code == 0:
        print(stdout)
    else:
        print(f"❌ Security audit failed: {stderr}")
        return 1

    print("\n💡 To fix security issues:")
    print("   docker exec openclaw_gateway openclaw security audit --fix")

    return 0


def cmd_telegram() -> int:
    """Check and fix Telegram channel."""

    print("\n📱 Telegram Channel Check\n")

    # Check current status
    code, stdout, stderr = run_docker_command(["openclaw", "channels", "status", "--probe"])

    if "Telegram" in stdout and "running" in stdout:
        print("✅ Telegram is configured and running")
        print(f"\n{stdout}")
        return 0

    print("❌ Telegram issue detected")

    # Check if configured
    code, stdout, stderr = run_docker_command(["openclaw", "config", "get", "channels"])
    try:
        config = json.loads(stdout) if stdout else {}
        if "telegram" not in config:
            print("\n📝 Telegram not configured in openclaw.json")
            print("\n💡 Fix Options:")
            print("   1. Restore from backup:")
            print(
                "      docker exec openclaw_gateway cp /root/.openclaw/openclaw.json.backup /root/.openclaw/openclaw.json"
            )
            print(
                "   2. Manual configuration via openclaw channels add --channel telegram --token $TOKEN"
            )
            print("\n   Then restart: docker restart openclaw_gateway")
        else:
            print("\n✅ Telegram configured but not connected")
            print("   Check bot token is valid and bot is not blocked")
    except json.JSONDecodeError:
        print("❌ Could not parse channel config")

    return 1


def cmd_reset(scope: str = "sessions") -> int:
    """Reset OpenClaw state."""

    print(f"\n🔄 Resetting OpenClaw ({scope})...\n")

    valid_scopes = ["sessions", "config", "full"]
    if scope not in valid_scopes:
        print(f"❌ Invalid scope: {scope}")
        print(f"   Valid scopes: {', '.join(valid_scopes)}")
        return 1

    code, stdout, stderr = run_docker_command(["openclaw", "reset", "--scope", scope])
    if code == 0:
        print(f"✅ Reset {scope} complete")
        print("\n📝 Restarting OpenClaw gateway...")
        subprocess.run(["docker", "restart", CONTAINER_NAME])
        print("✅ OpenClaw restarted")
    else:
        print(f"❌ Reset failed: {stderr}")
        return 1

    return 0


def cmd_status() -> int:
    """Full status report."""

    print("\n📊 OPENCLAW FULL STATUS REPORT\n")

    # Container
    print("Container:")
    subprocess.run(
        [
            "docker",
            "ps",
            "--filter",
            f"name={CONTAINER_NAME}",
            "--format",
            "table {{.Names}}\t{{.Status}}\t{{.Ports}}",
        ]
    )

    # Health check
    print("\nHealth Status:")
    status = health_check()
    print(f"   Gateway: {'✅' if status.gateway_running else '❌'}")
    print(f"   Telegram Config: {'✅' if status.telegram_configured else '❌'}")
    print(f"   Telegram Connected: {'✅' if status.telegram_connected else '❌'}")

    # OpenClaw status
    print("\nOpenClaw Status:")
    code, stdout, stderr = run_docker_command(["openclaw", "status"])
    if code == 0:
        # Parse and display key info
        lines = stdout.split("\n")
        for line in lines:
            if any(x in line for x in ["Gateway", "Agents", "Heartbeat", "Sessions"]):
                print(f"   {line.strip()}")

    print("\n" + "=" * 60)
    return 0


def main() -> int:
    """Main entry point."""

    parser = argparse.ArgumentParser(
        description="OpenClaw Doctor & Troubleshooter for AGI-OpenCode",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s health              # Quick health check
    %(prog)s diagnose            # Full diagnostics
    %(prog)s fix                 # Auto-fix issues
    %(prog)s logs --follow       # Follow logs
    %(prog)s telegram            # Check Telegram
    %(prog)s security            # Security audit
    %(prog)s reset --scope full  # Full reset
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Health command
    subparsers.add_parser("health", help="Quick health check")

    # Diagnose command
    subparsers.add_parser("diagnose", help="Full diagnostic run")

    # Fix command
    subparsers.add_parser("fix", help="Auto-fix common issues")

    # Logs command
    logs_parser = subparsers.add_parser("logs", help="View logs")
    logs_parser.add_argument("-f", "--follow", action="store_true", help="Follow logs")
    logs_parser.add_argument("-n", "--limit", type=int, default=100, help="Number of lines")

    # Telegram command
    subparsers.add_parser("telegram", help="Check/fix Telegram channel")

    # Security command
    subparsers.add_parser("security", help="Run security audit")

    # Reset command
    reset_parser = subparsers.add_parser("reset", help="Reset OpenClaw state")
    reset_parser.add_argument(
        "--scope",
        choices=["sessions", "config", "full"],
        default="sessions",
        help="Reset scope (default: sessions)",
    )

    # Status command
    subparsers.add_parser("status", help="Full status report")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Check container exists
    if not check_container_running() and args.command not in ["logs"]:
        print(f"\n❌ Container '{CONTAINER_NAME}' is not running!")
        print("\n💡 Start OpenClaw with:")
        print("   docker-compose up -d openclaw")
        return 1

    # Route to command handler
    commands = {
        "health": cmd_health,
        "diagnose": cmd_diagnose,
        "fix": cmd_fix,
        "logs": lambda: cmd_logs(args.follow, args.limit),
        "telegram": cmd_telegram,
        "security": cmd_security,
        "reset": lambda: cmd_reset(args.scope),
        "status": cmd_status,
    }

    handler = commands.get(args.command)
    if handler:
        return handler()
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
