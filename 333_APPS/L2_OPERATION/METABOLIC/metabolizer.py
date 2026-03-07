"""
metabolizer.py — Metabolic Membrane for 333_APPS (FORWARDING STUB)

This module enforces the EMD Stack (Encoder → Metabolizer → Decoder) on all
high-level applications in 333_APPS.

All architectural definitions have been moved to `core.pipeline` and `core.enforcement.aki_contract`
to centralize the L0-L3 taxonomy inside the core kernel.
"""

from core.observability.metrics import SystemAuditor

# ═══════════════════════════════════════════════════════════════════════════
# AUDIT FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════


def audit_333_apps_for_bypass() -> list[str]:
    """Scan 333_APPS for thermal leaks (direct LLM API calls)."""
    from pathlib import Path

    apps_dir = Path(__file__).parent
    return SystemAuditor.audit_apps_bypass(apps_dir)


if __name__ == "__main__":
    print("🔍 AUDIT: Scanning 333_APPS for thermal leaks...")
    violations = audit_333_apps_for_bypass()
    if violations:
        print("\n❌ THERMAL LEAKS DETECTED:")
        for v in violations:
            print(f"  - {v}")
        print("\nAll applications MUST route through L0 Kernel")
        exit(1)
    else:
        print("\n✅ No thermal leaks detected.")
        exit(0)
