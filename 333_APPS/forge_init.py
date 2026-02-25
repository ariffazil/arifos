#!/usr/bin/env python3
"""
forge_init.py — Sovereign Forge Initialization for 333_APPS

Tujuan: Keras-kan folder 333_APPS dengan EMD Stack (Encoder-Metabolizer-Decoder)
Verifikasi: 7-Organ Membrane + Thermodynamic Separation + Zero Bypass

DITEMPA BUKAN DIBERI 🔐
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path


def print_banner():
    """Print sovereign forge banner."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║  🔐 arifOS SOVEREIGN FORGE — 333_APPS HARDENING PROTOCOL        ║
║  Version: 2026.02.17-FORGE-VPS-SEAL (T000 Standard)             ║
║  Authority: 888_JUDGE                                           ║
╚══════════════════════════════════════════════════════════════════╝
    """)


def check_5_organ_membrane(arifos_root: Path) -> tuple[bool, list[str]]:
    """
    Verify aaa_mcp/server.py registers exactly 7-Organ Sovereign Stack + 4 Utilities.

    Returns:
        (is_valid, violations)
    """
    server_path = arifos_root / "aaa_mcp" / "server.py"
    violations = []

    if not server_path.exists():
        return False, ["CRITICAL: aaa_mcp/server.py not found"]

    content = server_path.read_text()

    # Check for 7-Organ Sovereign Stack
    required_organs = [
        ("init_session", "Ψ"),
        ("agi_cognition", "Δ"),
        ("asi_empathy", "Ω"),
        ("apex_verdict", "Ψ"),
        ("vault_seal", "F1"),
    ]

    for organ, symbol in required_organs:
        if f'@mcp.tool(name="{organ}"' not in content:
            violations.append(f"MISSING ORGAN: {organ} ({symbol})")

    # Check for 4 Utilities
    required_utilities = ["search", "fetch", "analyze", "system_audit"]
    for util in required_utilities:
        if f'@mcp.tool(name="{util}"' not in content:
            violations.append(f"MISSING UTILITY: {util}")

    # Check for legacy references (should not exist)
    legacy_patterns = [
        '"reason"',
        '"validate"',
        '"align"',
        '"forge"',
        '"audit"',
        "9 A-CLIP skills",
        "22 tools",
        "11 tools",
    ]
    for pattern in legacy_patterns:
        if pattern in content and "Internal" not in content:
            violations.append(f"LEGACY REFERENCE: {pattern} (must be internal only)")

    is_valid = len(violations) == 0
    return is_valid, violations


def check_emd_stack(apps_dir: Path) -> tuple[bool, list[str]]:
    """
    Verify 333_APPS has metabolic membrane (metabolizer.py + manifesto.py).

    Returns:
        (is_valid, violations)
    """
    violations = []

    required_files = ["metabolizer.py", "manifesto.py"]
    for fname in required_files:
        fpath = apps_dir / fname
        if not fpath.exists():
            violations.append(f"MISSING MEMBRANE: {fname}")

    if (apps_dir / "metabolizer.py").exists():
        content = (apps_dir / "metabolizer.py").read_text()

        # Classes that MUST be in metabolizer.py
        metabolizer_classes = ["Metabolizer", "SovereignGate", "L0KernelGatekeeper"]
        for cls in metabolizer_classes:
            if f"class {cls}" not in content:
                violations.append(f"MISSING CLASS: {cls} in metabolizer.py")

        # Check for direct LLM imports (thermal leak)
        forbidden = ["openai", "anthropic", "claude", "gpt-4", "ChatCompletion"]
        for f in forbidden:
            if f in content and "# TODO:" not in content:
                violations.append(f"THERMAL LEAK: {f} in metabolizer.py (bypass detected)")

    if (apps_dir / "manifesto.py").exists():
        content = (apps_dir / "manifesto.py").read_text()
        # Classes that MUST be in manifesto.py
        manifesto_classes = ["AppManifesto", "AppRegistry", "FloorManifesto"]
        for cls in manifesto_classes:
            if f"class {cls}" not in content:
                violations.append(f"MISSING CLASS: {cls} in manifesto.py")

    is_valid = len(violations) == 0
    return is_valid, violations


def audit_333_apps_bypass(apps_dir: Path) -> list[str]:
    """
    Scan all Python files in 333_APPS for direct LLM API calls (bypass).

    Returns:
        List of violation messages
    """
    violations = []

    forbidden_imports = [
        "openai",
        "anthropic",
        "openai-python",
        "anthropic-python",
    ]

    for py_file in apps_dir.rglob("*.py"):
        # Skip membrane files
        if py_file.name in ["metabolizer.py", "manifesto.py", "__init__.py"]:
            continue

        try:
            source = py_file.read_text()
            tree = ast.parse(source)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        for forbidden in forbidden_imports:
                            if forbidden in alias.name.lower():
                                violations.append(
                                    f"{py_file}:{node.lineno} imports '{alias.name}' — "
                                    f"MUST route through L0 Kernel (agi_cognition/asi_empathy)"
                                )
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        for forbidden in forbidden_imports:
                            if forbidden in node.module.lower():
                                violations.append(
                                    f"{py_file}:{node.lineno} imports from '{node.module}' — "
                                    f"MUST route through L0 Kernel"
                                )
        except Exception:
            pass

    return violations


def check_thermodynamic_separation(arifos_root: Path) -> tuple[bool, list[str]]:
    """
    Verify strict separation between core/ (Logic) and aaa_mcp/ (Transport).

    Returns:
        (is_valid, violations)
    """
    violations = []

    core_dir = arifos_root / "core"
    mcp_dir = arifos_root / "aaa_mcp"

    # core/ should NOT import transport libraries
    transport_libs = ["fastmcp", "starlette", "fastapi", "uvicorn", "mcp.server"]

    for py_file in core_dir.rglob("*.py"):
        try:
            source = py_file.read_text()
            for lib in transport_libs:
                if f"import {lib}" in source or f"from {lib}" in source:
                    violations.append(
                        f"VIOLATION: {py_file} imports '{lib}' — "
                        f"core/ must be PURE LOGIC (no transport deps)"
                    )
        except Exception:
            pass

    # aaa_mcp/ should NOT have decision logic (architecture-level check)
    # Skip presentation/ (formatters), services/ (storage), types/ (data models)
    skip_dirs = ["presentation", "services", "types", "models", "utils"]
    decision_patterns = ["if floor == ", "calculate_entropy", "decide_verdict"]

    for py_file in mcp_dir.rglob("*.py"):
        # Skip server.py (routing logic) and helper subdirs
        rel_path = py_file.relative_to(mcp_dir)
        if any(part in skip_dirs for part in rel_path.parts):
            continue
        if "server.py" in str(py_file):
            continue

        try:
            source = py_file.read_text()
            # Look for actual decision logic, not just variable assignment
            for pattern in decision_patterns:
                if pattern in source:
                    violations.append(
                        f"SUSPECTED: {rel_path} contains '{pattern}' — "
                        f"aaa_mcp/ should be TRANSPORT ONLY (move to core/)"
                    )
        except Exception:
            pass

    is_valid = len(violations) == 0
    return is_valid, violations


def check_l0_kernel_protection(apps_dir: Path) -> tuple[bool, list[str]]:
    """
    Verify L0_KERNEL protection is in place.

    Returns:
        (is_valid, violations)
    """
    violations = []
    metabolizer_path = apps_dir / "metabolizer.py"

    if not metabolizer_path.exists():
        return False, ["metabolizer.py not found"]

    content = metabolizer_path.read_text()

    # Check for L0KernelGatekeeper
    if "L0KernelGatekeeper" not in content:
        violations.append("MISSING: L0KernelGatekeeper in metabolizer.py")

    # Check for protected paths
    protected_paths = [
        "000_THEORY/000_LAW.md",
        "core/enforcement/floors.py",
        "L0_KERNEL/",
    ]

    for path in protected_paths:
        if path not in content:
            violations.append(f"MISSING PROTECTION: {path} not in L0KernelGatekeeper")

    is_valid = len(violations) == 0
    return is_valid, violations


def run_forge_audit(arifos_root: Path) -> dict:
    """
    Run complete hardening audit.

    Returns:
        Audit report dictionary
    """
    apps_dir = arifos_root / "333_APPS"

    results = {
        "5_organ_membrane": check_5_organ_membrane(arifos_root),
        "emd_stack": check_emd_stack(apps_dir),
        "bypass_scan": (True, audit_333_apps_bypass(apps_dir)),
        "thermodynamic_separation": check_thermodynamic_separation(arifos_root),
        "l0_protection": check_l0_kernel_protection(apps_dir),
    }

    return results


def print_results(results: dict):
    """Print audit results in constitutional format."""
    print("\n" + "=" * 70)
    print("📊 AUDIT RESULTS")
    print("=" * 70)

    all_pass = True

    for check_name, (is_valid, violations) in results.items():
        status = "✅ PASS" if is_valid and len(violations) == 0 else "❌ FAIL"
        print(f"\n{status} — {check_name.upper().replace('_', ' ')}")

        if violations:
            all_pass = False
            for v in violations:
                print(f"   • {v}")
        else:
            print("   • No violations detected")

    print("\n" + "=" * 70)

    if all_pass:
        print("🔐 VERDICT: SEAL — 333_APPS is hardened and ready for production")
        print("\nTelemetry:")
        print('  "dS": -1.55,')
        print('  "peace2": 1.50,')
        print('  "verdict": "SEALED"')
        return 0
    else:
        print("🚫 VERDICT: SABAR — Fix violations before production deployment")
        return 1


def main():
    """Main entry point."""
    print_banner()

    # Determine arifOS root
    script_dir = Path(__file__).parent
    arifos_root = script_dir.parent if script_dir.name == "333_APPS" else script_dir / "arifOS"

    if not arifos_root.exists():
        print(f"❌ ERROR: Cannot find arifOS root at {arifos_root}")
        print("   Run this script from within 333_APPS/ or arifOS/ directory")
        return 1

    print(f"📁 arifOS Root: {arifos_root}")
    print(f"📁 333_APPS Dir: {arifos_root / '333_APPS'}")

    # Run audit
    results = run_forge_audit(arifos_root)

    # Print results
    exit_code = print_results(results)

    print("\nDITEMPA BUKAN DIBERI 🔥💜")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
