"""
arifosmcp.intelligence/core — Constitutional Intelligence Kernel
Constitutional Metabolizer: arifOS v60.0-FORGE
Authority: ARIF FAZIL (Sovereign)
Motto: Ditempa Bukan Diberi

Exports the 8 kernel modules:
  lifecycle     — KernelState machine (INIT→ACTIVE→SABAR→HOLD→VOID)
  floor_audit   — F1-F13 runtime constitutional auditor
  vault_logger  — Tri-Witness + VAULT999 immutable ledger
  thermo_budget — Thermodynamic session budget (ΔS, Peace², Ω₀)
  federation    — Multi-agent health coordination
  eval_suite    — Programmatic regression test runner
  amendment     — Phoenix-72 cooldown protocol
"""

from .lifecycle import KernelState, LifecycleManager, Session

__all__ = [
    "LifecycleManager",
    "KernelState",
    "Session",
    "FloorAuditor",
    "FloorResult",
    "AuditResult",
    "Verdict",
    "ThermoBudget",
    "ThermoSnapshot",
    "VaultLogger",
    "WitnessRecord",
    "FederationCoordinator",
    "EvalSuite",
    "AmendmentChain",
    "AmendmentRecord",
]


def __getattr__(name: str):
    """Keep lifecycle imports light; load the rest of core on demand."""
    if name in {"FloorAuditor", "FloorResult", "AuditResult", "Verdict"}:
        from .floor_audit import AuditResult, FloorAuditor, FloorResult, Verdict

        return {
            "FloorAuditor": FloorAuditor,
            "FloorResult": FloorResult,
            "AuditResult": AuditResult,
            "Verdict": Verdict,
        }[name]
    if name in {"ThermoBudget", "ThermoSnapshot"}:
        from .thermo_budget import ThermoBudget, ThermoSnapshot

        return {"ThermoBudget": ThermoBudget, "ThermoSnapshot": ThermoSnapshot}[name]
    if name in {"VaultLogger", "WitnessRecord"}:
        from .vault_logger import VaultLogger, WitnessRecord

        return {"VaultLogger": VaultLogger, "WitnessRecord": WitnessRecord}[name]
    if name == "FederationCoordinator":
        from .federation import FederationCoordinator

        return FederationCoordinator
    if name == "EvalSuite":
        from .eval_suite import EvalSuite

        return EvalSuite
    if name in {"AmendmentChain", "AmendmentRecord"}:
        from .amendment import AmendmentChain, AmendmentRecord

        return {"AmendmentChain": AmendmentChain, "AmendmentRecord": AmendmentRecord}[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
