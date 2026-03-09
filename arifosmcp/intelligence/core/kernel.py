"""
arifosmcp.intelligence/core/kernel.py — Unified Constitutional Kernel Singleton
The single source of truth for arifOS governance.
"""

from .amendment import AmendmentChain
from .eval.suite import ConstitutionalEvalSuite as EvalSuite
from .federation import FederationCoordinator
from .floor_audit import FloorAuditor
from .lifecycle import LifecycleManager
from .thermo_budget import ThermoBudget
from .vault_logger import VaultLogger


class ConstitutionalKernel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Initialize all constitutional singletons
            cls._instance.lifecycle = LifecycleManager()
            cls._instance.auditor = FloorAuditor()
            cls._instance.thermo = ThermoBudget()
            cls._instance.vault = VaultLogger()
            cls._instance.amendment = AmendmentChain()
            cls._instance.federation = FederationCoordinator()
            cls._instance.eval_suite = EvalSuite()
        return cls._instance

    def audit(self, action: str, context: str | dict = "", severity: str = "medium"):
        """Centralized audit gate for all triad tools."""
        return self.auditor.check_floors(action, context=context, severity=severity)


# Export the singleton
kernel = ConstitutionalKernel()


async def get_kernel() -> ConstitutionalKernel:
    """Provides async-friendly access to the kernel singleton."""
    return kernel
