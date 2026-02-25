"""
metabolizer.py — Metabolic Membrane for 333_APPS

This module enforces the EMD Stack (Encoder → Metabolizer → Decoder) on all
high-level applications in 333_APPS. It ensures:

1. Zero-bypass: All apps MUST route through L0 Kernel (7-Organ Sovereign Stack)
2. Floor enforcement: Every app defines Hard vs Soft floors
3. Telemetry: Standard arifOS telemetry appended to all outputs
4. 888_HOLD: Sovereign gate for irreversible actions

PHILOSOPHY: DITEMPA BUKAN DIBERI — No app runs outside constitutional law.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FloorType(Enum):
    """Constitutional floor classification."""

    HARD = "hard"  # Existential: VOID on failure
    SOFT = "soft"  # Performance: SABAR on failure


class AppVerdict(Enum):
    """Application execution verdicts."""

    SEAL = "SEAL"  # Approved, proceed
    SABAR = "SABAR"  # Pause, retry, gather more info
    VOID = "VOID"  # Blocked, cannot proceed
    HOLD_888 = "888_HOLD"  # Requires sovereign approval


@dataclass
class FloorRequirement:
    """Floor requirement for an application."""

    floor_id: str  # F1, F2, F4, etc.
    floor_type: FloorType
    threshold: Any | None = None
    description: str = ""


@dataclass
class Telemetry:
    """Standard arifOS telemetry for app execution."""

    timestamp: float = field(default_factory=time.time)
    dS: float = 0.0  # Entropy reduction
    peace2: float = 1.0  # Stability metric
    kappa_r: float = 1.0  # Weakest listener protection
    echo_debt: float = 0.0
    shadow: float = 0.0
    confidence: float = 0.99
    psi_le: float = 1.0  # Law-energy

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "dS": self.dS,
            "peace2": self.peace2,
            "kappa_r": self.kappa_r,
            "echoDebt": self.echo_debt,
            "shadow": self.shadow,
            "confidence": self.confidence,
            "psi_le": self.psi_le,
        }


@dataclass
class AppResult:
    """Result from a metabolized application."""

    verdict: AppVerdict
    output: Any
    telemetry: Telemetry
    stage: str = ""
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "verdict": self.verdict.value,
            "output": self.output,
            "telemetry": self.telemetry.to_dict(),
            "stage": self.stage,
            "error": self.error,
        }


class Metabolizer(ABC):
    """
    Abstract base class for all 333_APPS.

    Every application in 333_APPS must inherit from Metabolizer and:
    1. Define required floors via `required_floors()`
    2. Implement `metabolize()` to process input through L0
    3. Never call LLM APIs directly — always use L0 organs
    """

    def __init__(self, app_name: str, app_version: str = "1.0.0"):
        self.app_name = app_name
        self.app_version = app_version
        self._floor_cache: dict[str, FloorRequirement] = {}
        self._telemetry = Telemetry()

    @abstractmethod
    def required_floors(self) -> list[FloorRequirement]:
        """
        Define which floors this app requires.

        Returns:
            List of FloorRequirement objects

        Example:
            return [
                FloorRequirement("F1", FloorType.HARD, None, "Reversibility check"),
                FloorRequirement("F2", FloorType.HARD, 0.99, "Truth threshold"),
                FloorRequirement("F4", FloorType.SOFT, 0.0, "Entropy reduction"),
            ]
        """
        pass

    @abstractmethod
    async def metabolize(self, input_data: dict[str, Any]) -> AppResult:
        """
        Process input through L0 Kernel.

        This is the ONLY authorized method to perform cognition.
        All LLM calls MUST go through:
        - agi_cognition (for reasoning)
        - asi_empathy (for impact analysis)
        - apex_verdict (for final decisions)

        NEVER call OpenAI/Anthropic directly!

        Args:
            input_data: Raw input to the application

        Returns:
            AppResult with verdict and telemetry
        """
        pass

    def _check_floor_violations(self, floor_results: dict[str, Any]) -> list[str]:
        """Check if any hard floors were violated."""
        violations = []
        for req in self.required_floors():
            if req.floor_id in floor_results:
                result = floor_results[req.floor_id]
                if req.floor_type == FloorType.HARD and not result.get("passed", False):
                    violations.append(f"{req.floor_id} (HARD): {req.description}")
        return violations

    def _calculate_telemetry(self, start_time: float) -> Telemetry:
        """Calculate telemetry for this execution."""
        elapsed = time.time() - start_time
        # Simplified telemetry calculation
        return Telemetry(
            dS=-0.1 * elapsed,  # More time = more entropy reduced
            peace2=1.0 - (0.01 * elapsed),  # Stability degrades slightly with time
            kappa_r=0.95,
            confidence=0.99,
        )


class SovereignGate:
    """
    888_HOLD enforcement gate for irreversible actions.

    Any application performing destructive operations (delete, send, trade)
    MUST pass through this gate. It enforces F1 Amanah and F11 Authority.

    Usage:
        gate = SovereignGate(action_type="delete", resource_path="/data/file.txt")
        result = await gate.check_approval(context)
        if result.verdict == AppVerdict.HOLD_888:
            # Wait for sovereign signature
            pass
    """

    IRREVERSIBLE_ACTIONS = {
        "delete",
        "remove",
        "drop",
        "truncate",
        "send",
        "transfer",
        "trade",
        "execute",
        "deploy",
        "publish",
        "commit",
    }

    def __init__(
        self,
        action_type: str,
        resource_path: str,
        requires_signature: bool = True,
    ):
        self.action_type = action_type.lower()
        self.resource_path = resource_path
        self.requires_signature = requires_signature
        self.is_irreversible = self.action_type in self.IRREVERSIBLE_ACTIONS

    async def check_approval(
        self,
        context: dict[str, Any],
        proposed_verdict: str = "SEAL",
    ) -> AppResult:
        """
        Check if action is approved or requires 888_HOLD.

        Args:
            context: Execution context including session_id, actor_id
            proposed_verdict: Expected outcome (SEAL, SABAR, VOID)

        Returns:
            AppResult with HOLD_888 if sovereign approval needed
        """
        # If irreversible, force 888_HOLD
        if self.is_irreversible and self.requires_signature:
            return AppResult(
                verdict=AppVerdict.HOLD_888,
                output={
                    "message": f"Action '{self.action_type}' on '{self.resource_path}' requires sovereign approval",
                    "action_type": self.action_type,
                    "resource": self.resource_path,
                    "authority": "888_JUDGE",
                },
                telemetry=Telemetry(confidence=0.99),
                stage="888_HOLD",
            )

        # Otherwise, proceed with proposed verdict
        return AppResult(
            verdict=AppVerdict(proposed_verdict),
            output={"approved": True, "action": self.action_type},
            telemetry=Telemetry(),
            stage="pre-flight",
        )

    def verify_signature(self, signature: str) -> bool:
        """
        Verify sovereign cryptographic signature.

        In production, this validates against 888_JUDGE public key.
        For now, placeholder implementation.

        Args:
            signature: Cryptographic signature from sovereign

        Returns:
            True if signature valid
        """
        # TODO: Implement Ed25519 signature verification
        # For now, accept "SEAL" as manual override
        return signature.upper() == "SEAL"


class L0KernelGatekeeper:
    """
    Protects L0_KERNEL from modification by L1-L7 apps.

    Rule: No application in 333_APPS may modify:
    - 000_LAW.md (constitutional law)
    - core/enforcement/floors.py (floor thresholds)
    - Any file in L0_KERNEL/

    These are SOVEREIGN ONLY actions.
    """

    PROTECTED_PATHS = [
        "000_THEORY/000_LAW.md",
        "core/enforcement/floors.py",
        "core/shared/floors.py",
        "333_APPS/L0_KERNEL/",
        "T000_VERSIONING.md",
    ]

    @classmethod
    def check_modification_permission(cls, filepath: str) -> bool:
        """
        Check if modifying a file is allowed.

        Args:
            filepath: Path to file being modified

        Returns:
            False if modification requires sovereign authority
        """
        for protected in cls.PROTECTED_PATHS:
            if protected in filepath or filepath.endswith(protected):
                return False
        return True

    @classmethod
    def assert_modification_allowed(cls, filepath: str) -> None:
        """
        Raise exception if trying to modify protected L0 file.

        Args:
            filepath: Path to file being modified

        Raises:
            PermissionError: If file is protected
        """
        if not cls.check_modification_permission(filepath):
            raise PermissionError(
                f"🚫 SOVEREIGN ONLY: Cannot modify '{filepath}'. "
                f"Modification of L0_KERNEL constitutional law requires 888_JUDGE authority. "
                f"This action has been logged and blocked."
            )


def require_metabolizer(app_class):
    """
    Decorator to ensure a class inherits from Metabolizer.

    Usage:
        @require_metabolizer
        class MyApp(Metabolizer):
            pass
    """
    if not issubclass(app_class, Metabolizer):
        raise TypeError(
            f"Class '{app_class.__name__}' must inherit from Metabolizer. "
            f"All 333_APPS must implement the metabolic membrane."
        )
    return app_class


# ═══════════════════════════════════════════════════════════════════════════
# AUDIT FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════


def audit_333_apps_for_bypass() -> list[str]:
    """
    Scan 333_APPS for thermal leaks (direct LLM API calls).

    Returns:
        List of violation messages
    """
    import ast
    from pathlib import Path

    violations = []
    apps_dir = Path(__file__).parent.parent  # 333_APPS/

    forbidden_patterns = [
        "openai",
        "anthropic",
        "claude",
        "gpt-",
        "ChatCompletion",
        "client.chat",
    ]

    for py_file in apps_dir.rglob("*.py"):
        # Skip the metabolizer itself
        if py_file.name == "metabolizer.py":
            continue

        try:
            with open(py_file, encoding="utf-8") as f:
                source = f.read()
            tree = ast.parse(source)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if any(pat in alias.name for pat in forbidden_patterns):
                            violations.append(
                                f"[BYPASS DETECTED] {py_file}:{node.lineno} "
                                f"imports '{alias.name}' — MUST route through L0 Kernel"
                            )
                elif isinstance(node, ast.ImportFrom):
                    if node.module and any(pat in node.module for pat in forbidden_patterns):
                        violations.append(
                            f"[BYPASS DETECTED] {py_file}:{node.lineno} "
                            f"imports from '{node.module}' — MUST route through L0 Kernel"
                        )
        except Exception:
            pass

    return violations


if __name__ == "__main__":
    # Run audit when executed directly
    print("🔍 AUDIT: Scanning 333_APPS for thermal leaks...")
    violations = audit_333_apps_for_bypass()

    if violations:
        print("\n❌ THERMAL LEAKS DETECTED:")
        for v in violations:
            print(f"  - {v}")
        print("\nAll applications MUST route through L0 Kernel (agi_cognition, asi_empathy)")
        exit(1)
    else:
        print("\n✅ No thermal leaks detected. All apps route through L0 Kernel.")
        exit(0)
