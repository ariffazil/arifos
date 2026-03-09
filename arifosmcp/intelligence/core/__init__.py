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

from .amendment import AmendmentChain, AmendmentRecord
from .eval.suite import ConstitutionalEvalSuite as EvalSuite
from .federation import FederationCoordinator
from .floor_audit import AuditResult, FloorAuditor, FloorResult, Verdict
from .lifecycle import KernelState, LifecycleManager, Session
from .thermo_budget import ThermoBudget, ThermoSnapshot
from .vault_logger import VaultLogger, WitnessRecord

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
