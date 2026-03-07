#!/usr/bin/env python3
"""
forge_init.py — Sovereign Forge Initialization for 333_APPS (FORWARDING STUB)

All verification logic has been migrated to `core.observability.metrics.SystemAuditor`.
"""

from __future__ import annotations
import sys
from pathlib import Path

from core.observability.metrics import SystemAuditor

def print_banner():
    print(
        """
╔══════════════════════════════════════════════════════════════════╗
║  🔐 arifOS SOVEREIGN FORGE — 333_APPS HARDENING PROTOCOL        ║
║  Version: 2026.03.07-ARCH-SEAL (T000 Standard)                       ║
║  Authority: 888_JUDGE                                           ║
╚══════════════════════════════════════════════════════════════════╝
    """
    )

def main():
    print_banner()
    # Path is now 333_APPS/L2_OPERATION/METABOLIC/forge_init.py
    arifos_root = Path(__file__).resolve().parent.parent.parent.parent
    apps_dir = arifos_root / "333_APPS"

    print("1. Checking 5-Organ Sovereign Membrane... ", end="")
    is_valid, violations = SystemAuditor.check_5_organ_membrane(arifos_root)
    if is_valid:
        print("✅ SEALED")
    else:
        print("❌ VOID")
        for v in violations:
            print(f"  -> {v}")

    # Skipping check_emd_stack as its logic is distributed now, or you could add it to SystemAuditor

    print("2. Scanning for Thermal Leaks (LLM Bypass)... ", end="")
    violations = SystemAuditor.audit_apps_bypass(apps_dir)
    if not violations:
        print("✅ SEALED")
    else:
        print("❌ VOID")
        for v in violations:
            print(f"  -> {v}")

    print("3. Checking Thermodynamic Separation (core vs aaa_mcp)... ", end="")
    is_valid, violations = SystemAuditor.check_thermodynamic_separation(arifos_root)
    if is_valid:
        print("✅ SEALED")
    else:
        print("❌ VOID")
        for v in violations:
            print(f"  -> {v}")

if __name__ == "__main__":
    main()
