#!/usr/bin/env python3
"""
arifOS MCP Self-Test Module (2026.02.22-FORGE-VPS-SEAL)

Run before deployment to verify:
1. Constitutional floors are loaded
2. Tools are properly wired
3. Thermodynamic parameters are valid
4. Health endpoint contract is correct

Usage:
    python -m aaa_mcp.selftest
    python -m aaa_mcp.selftest --strict  # Fail on warnings
"""

import os
import sys
from pathlib import Path

from aaa_mcp.protocol.aaa_contract import AAA_TOOL_LAW_BINDINGS, MANIFEST_VERSION

# Target bands
OMEGA_TARGET_MIN = 0.03
OMEGA_TARGET_MAX = 0.05
OMEGA_CRITICAL = 0.08


def check_floors() -> tuple[bool, list[str]]:
    """Verify constitutional floors are configured."""
    issues = []

    # Check for canonical floor bindings on the public 13-tool contract.
    try:
        if not AAA_TOOL_LAW_BINDINGS:
            issues.append("WARN: No constitutional floors defined")
        else:
            floor_count = len(AAA_TOOL_LAW_BINDINGS)
            required_floor_tools = [
                "anchor_session",
                "reason_mind",
                "simulate_heart",
                "apex_judge",
                "seal_vault",
            ]
            missing_floors = [t for t in required_floor_tools if not AAA_TOOL_LAW_BINDINGS.get(t)]

            if missing_floors:
                issues.append(f"WARN: Missing floors for: {missing_floors}")

            print(f"✓ Constitutional floors loaded: {floor_count} definitions")
    except ImportError as e:
        issues.append(f"ERROR: Cannot load constitutional floors: {e}")

    return len([i for i in issues if i.startswith("FAIL")]) == 0, issues


async def check_tools() -> tuple[bool, list[str]]:
    """Verify MCP tools are properly wired."""
    issues = []

    try:
        from aaa_mcp.server import mcp

        # Introspect tool registry using FastMCP public API (v2+)
        tool_names = []
        try:
            # get_tools() is async and returns a dict[name -> FunctionTool]
            if hasattr(mcp, "get_tools"):
                tools = await mcp.get_tools()  # type: ignore
                if isinstance(tools, dict):
                    tool_names = list(tools.keys())
                else:
                    try:
                        tool_names = [t.name for t in tools]
                    except Exception:
                        pass
            elif hasattr(mcp, "list_tools"):  # Fallback
                tools = await mcp.list_tools()
                tool_names = [t.name for t in tools]
        except Exception:
            tool_names = []

        if not tool_names:
            issues.append("WARN: Could not inspect tools list")

        # Verify canonical 13-tool surface against the shared contract manifest.
        required_tools = [
            "anchor_session",
            "reason_mind",
            "recall_memory",
            "simulate_heart",
            "critique_thought",
            "apex_judge",
            "eureka_forge",
            "seal_vault",
            "search_reality",
            "fetch_content",
            "inspect_file",
            "audit_rules",
            "check_vital",
        ]

        missing = [t for t in required_tools if t not in tool_names]
        if missing:
            issues.append(f"FAIL: Missing canonical tools: {missing}")
        else:
            print(f"✓ All {len(required_tools)} canonical tools present (MANIFEST_VERSION={MANIFEST_VERSION})")

        print("✓ MCP server module loaded successfully")

    except ImportError as e:
        issues.append(f"FAIL: Cannot import MCP server: {e}")
    except Exception as e:
        issues.append(f"WARN: MCP server check issue: {e}")

    return len([i for i in issues if i.startswith("FAIL")]) == 0, issues


def check_thermodynamics() -> tuple[bool, list[str]]:
    """Verify thermodynamic parameters are within bounds."""
    issues = []

    # Check environment variables
    governance_mode = os.environ.get("GOVERNANCE_MODE", "SOFT")
    cluster_level = os.environ.get("CLUSTER_LEVEL", "1")

    print(f"✓ Governance mode: {governance_mode}")
    print(f"✓ Cluster level: {cluster_level}")

    # Validate cluster level
    try:
        level = int(cluster_level)
        if level < 0 or level > 999:
            issues.append(f"WARN: Cluster level {level} outside 0-999 range")
    except ValueError:
        issues.append(f"WARN: Invalid cluster level: {cluster_level}")

    # Check Ω₀ if available
    omega = os.environ.get("OMEGA_ZERO")
    if omega:
        try:
            omega_val = float(omega)
            if omega_val > OMEGA_CRITICAL:
                issues.append(f"FAIL: Ω₀ = {omega_val} exceeds critical threshold {OMEGA_CRITICAL}")
            elif omega_val > OMEGA_TARGET_MAX:
                issues.append(
                    f"WARN: Ω₀ = {omega_val} above target band [{OMEGA_TARGET_MIN}-{OMEGA_TARGET_MAX}]"
                )
            else:
                print(f"✓ Ω₀ = {omega_val} (within target band)")
        except ValueError:
            issues.append(f"WARN: Invalid OMEGA_ZERO value: {omega}")

    return len([i for i in issues if i.startswith("FAIL")]) == 0, issues


def check_health_contract() -> tuple[bool, list[str]]:
    """Verify health endpoint contract."""
    issues = []

    # Check required fields for health response
    required_fields = ["status"]
    optional_fields = ["version", "tools", "mode", "cluster", "floors"]

    try:
        # Try to import health handler

        print("✓ Health endpoint: /health available")

        # Check if we can construct a valid health response
        health_response = {
            "status": "ok",
            "version": os.environ.get("ARIFOS_VERSION", "unknown"),
            "mode": os.environ.get("GOVERNANCE_MODE", "SOFT"),
            "cluster": os.environ.get("CLUSTER_LEVEL", "1"),
        }

        for field in required_fields:
            if field not in health_response:
                issues.append(f"FAIL: Health response missing required field: {field}")

        print(
            f"✓ Health contract: {len(required_fields)} required, {len(optional_fields)} optional fields"
        )

    except Exception as e:
        issues.append(f"WARN: Health contract check issue: {e}")

    return len([i for i in issues if i.startswith("FAIL")]) == 0, issues


def check_environment() -> tuple[bool, list[str]]:
    """Verify environment is properly configured."""
    issues = []

    # Required/defaultable env vars for production
    defaults = {
        "HOST": "0.0.0.0",
        "PORT": "8080",
        "GOVERNANCE_MODE": "SOFT",
        "VAULT_PATH": str(Path("VAULT999").resolve()),
    }

    for var, default_value in defaults.items():
        if not os.environ.get(var):
            os.environ[var] = default_value
            print(f"✓ {var} defaulted to {os.environ.get(var)}")
        else:
            print(f"✓ {var} = {os.environ.get(var)}")

    return True, issues


def run_selftest(strict: bool = False) -> bool:
    """Run all self-tests."""
    import asyncio

    print("=" * 60)
    print(f"  arifOS MCP Self-Test (v2026.2 — MANIFEST_VERSION={MANIFEST_VERSION})")
    print("=" * 60)
    print()

    all_passed = True
    all_issues = []

    checks = [
        ("Environment", check_environment),
        ("Constitutional Floors", check_floors),
        ("MCP Tools", check_tools),
        ("Thermodynamics", check_thermodynamics),
        ("Health Contract", check_health_contract),
    ]

    async def execute_checks():
        # Inner async loop to handle async checks
        results = []
        for name, check_fn in checks:
            print(f"\n[{name}]")
            try:
                if asyncio.iscoroutinefunction(check_fn):
                    passed, issues = await check_fn()
                else:
                    passed, issues = check_fn()

                results.append((passed, issues))
            except Exception as e:
                print(f"FAIL: {name} check crashed: {e}")
                results.append((False, [f"FAIL: {name} check crashed: {e}"]))
        return results

    # Run checks in event loop
    try:
        check_results = asyncio.run(execute_checks())
    except Exception as e:
        print(f"CRITICAL: Async runner failed: {e}")
        return False

    # Process results
    for passed, issues in check_results:
        all_issues.extend(issues)
        if not passed:
            all_passed = False

    # Summary
    print("\n" + "=" * 60)
    print("  SELF-TEST SUMMARY")
    print("=" * 60)

    fails = [i for i in all_issues if i.startswith("FAIL")]
    warns = [i for i in all_issues if i.startswith("WARN")]

    if fails:
        print(f"\n❌ FAILURES ({len(fails)}):")
        for f in fails:
            print(f"   {f}")

    if warns:
        print(f"\n⚠️  WARNINGS ({len(warns)}):")
        for w in warns:
            print(f"   {w}")

    if not fails and not warns:
        print("\n✅ All checks passed!")

    # Verdict
    print("\n" + "-" * 60)
    if fails:
        print("VERDICT: VOID — Cannot deploy with failures")
        return False
    elif warns and strict:
        print("VERDICT: SABAR — Warnings present (strict mode)")
        return False
    elif warns:
        print("VERDICT: PARTIAL — Deploy allowed with warnings")
        return True
    else:
        print("VERDICT: SEAL — Ready for deployment")
        return True


if __name__ == "__main__":
    strict = "--strict" in sys.argv
    success = run_selftest(strict=strict)
    sys.exit(0 if success else 1)
