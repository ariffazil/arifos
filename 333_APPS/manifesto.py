"""
manifesto.py — Constitutional Manifesto for 333_APPS

Every application in 333_APPS must provide a manifesto declaring:
1. Which floors it enforces (Hard vs Soft)
2. Its metabolic contract with L0 Kernel
3. Telemetry requirements
4. Sovereign gate requirements (for irreversible actions)

This is the DECLARATIVE counterpart to metabolizer.py (IMPERATIVE).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AppLayer(Enum):
    """Application layer in the 8-layer stack."""

    L1_PROMPT = "L1"
    L2_SKILLS = "L2"
    L3_WORKFLOW = "L3"
    L4_TOOLS = "L4"
    L5_AGENTS = "L5"
    L6_INSTITUTION = "L6"
    L7_AGI = "L7"


class FloorClassification(Enum):
    """How a floor is classified for this app."""

    HARD = "hard"  # Existential: VOID on failure
    SOFT = "soft"  # Performance: SABAR on failure
    N_A = "n/a"  # Not applicable to this app


@dataclass
class FloorManifesto:
    """Manifesto entry for a single floor."""

    floor_id: str
    classification: FloorClassification
    custom_threshold: Any | None = None
    rationale: str = ""


@dataclass
class AppManifesto:
    """
    Constitutional manifesto for a 333_APPS application.

    Every app must instantiate this and register with the AppRegistry.

    Example:
        manifesto = AppManifesto(
            app_name="DocumentAnalyzer",
            layer=AppLayer.L4_TOOLS,
            description="Analyzes documents with constitutional oversight",
            floors=[
                FloorManifesto("F1", FloorClassification.HARD, None, "File operations must be reversible"),
                FloorManifesto("F2", FloorClassification.HARD, 0.99, "Analysis must be grounded"),
                FloorManifesto("F4", FloorClassification.SOFT, 0.0, "Reduce analysis entropy"),
            ],
            requires_sovereign_gate=True,
            irreversible_actions=["delete", "overwrite"],
        )
    """

    app_name: str
    layer: AppLayer
    description: str
    version: str = "1.0.0"

    # Constitutional contract
    floors: list[FloorManifesto] = field(default_factory=list)

    # Sovereign gate requirements
    requires_sovereign_gate: bool = False
    irreversible_actions: list[str] = field(default_factory=list)

    # L0 Kernel routing
    l0_organs_used: list[str] = field(default_factory=lambda: ["agi_cognition"])

    # Metadata
    author: str = ""
    dependencies: list[str] = field(default_factory=list)

    def validate(self) -> bool:
        """Validate that manifesto is complete."""
        if not self.floors:
            raise ValueError(f"App '{self.app_name}' must declare at least one floor")

        # Check for required floors
        floor_ids = {f.floor_id for f in self.floors}
        required = {"F1", "F2", "F7"}  # Amanah, Truth, Humility
        missing = required - floor_ids

        if missing:
            raise ValueError(f"App '{self.app_name}' missing required floors: {missing}")

        return True

    def to_dict(self) -> dict[str, Any]:
        """Convert manifesto to dictionary."""
        return {
            "app_name": self.app_name,
            "layer": self.layer.value,
            "version": self.version,
            "description": self.description,
            "floors": [
                {
                    "floor_id": f.floor_id,
                    "classification": f.classification.value,
                    "threshold": f.custom_threshold,
                    "rationale": f.rationale,
                }
                for f in self.floors
            ],
            "requires_sovereign_gate": self.requires_sovereign_gate,
            "irreversible_actions": self.irreversible_actions,
            "l0_organs_used": self.l0_organs_used,
        }


class AppRegistry:
    """
    Registry of all constitutional applications in 333_APPS.

    This is the authoritative directory of what apps exist and their
    constitutional contracts.
    """

    _apps: dict[str, AppManifesto] = {}

    @classmethod
    def register(cls, manifesto: AppManifesto) -> None:
        """Register an app manifesto."""
        manifesto.validate()
        cls._apps[manifesto.app_name] = manifesto

    @classmethod
    def get(cls, app_name: str) -> AppManifesto | None:
        """Get manifesto by app name."""
        return cls._apps.get(app_name)

    @classmethod
    def list_all(cls) -> list[str]:
        """List all registered app names."""
        return list(cls._apps.keys())

    @classmethod
    def audit(cls) -> dict[str, Any]:
        """
        Audit all registered apps for constitutional compliance.

        Returns:
            Audit report with statistics
        """
        total = len(cls._apps)
        by_layer = {}
        sovereign_gates = 0

        for app in cls._apps.values():
            layer = app.layer.value
            by_layer[layer] = by_layer.get(layer, 0) + 1
            if app.requires_sovereign_gate:
                sovereign_gates += 1

        return {
            "total_apps": total,
            "by_layer": by_layer,
            "sovereign_gates_required": sovereign_gates,
            "apps": {name: m.to_dict() for name, m in cls._apps.items()},
        }


# ═══════════════════════════════════════════════════════════════════════════
# EXAMPLE MANIFESTOS (Template for new apps)
# ═══════════════════════════════════════════════════════════════════════════


def create_example_manifestos():
    """Create example manifestos for reference."""

    # Example: L4 Tool that analyzes documents
    doc_analyzer = AppManifesto(
        app_name="DocumentAnalyzer",
        layer=AppLayer.L4_TOOLS,
        description="Constitutional document analysis with grounded citations",
        floors=[
            FloorManifesto(
                "F1", FloorClassification.HARD, None, "Analysis must not corrupt source"
            ),
            FloorManifesto("F2", FloorClassification.HARD, 0.99, "Citations must be verifiable"),
            FloorManifesto("F4", FloorClassification.SOFT, 0.0, "Reduce cognitive entropy"),
            FloorManifesto("F7", FloorClassification.HARD, 0.05, "Declare uncertainty bounds"),
        ],
        requires_sovereign_gate=False,
        l0_organs_used=["agi_cognition", "asi_empathy"],
    )

    # Example: L5 Agent that executes tasks
    task_executor = AppManifesto(
        app_name="TaskExecutor",
        layer=AppLayer.L5_AGENTS,
        description="Multi-step task execution with reversibility guarantees",
        floors=[
            FloorManifesto("F1", FloorClassification.HARD, None, "All actions reversible"),
            FloorManifesto("F2", FloorClassification.HARD, 0.99, "Ground all decisions"),
            FloorManifesto("F6", FloorClassification.HARD, None, "Protect vulnerable stakeholders"),
            FloorManifesto(
                "F11", FloorClassification.HARD, None, "Human authority over irreversible"
            ),
        ],
        requires_sovereign_gate=True,
        irreversible_actions=["delete", "execute", "deploy"],
        l0_organs_used=["agi_cognition", "asi_empathy", "apex_verdict"],
    )

    return [doc_analyzer, task_executor]


if __name__ == "__main__":
    # Register example manifestos and print audit
    for manifesto in create_example_manifestos():
        AppRegistry.register(manifesto)

    print("📋 CONSTITUTIONAL APP REGISTRY")
    print("=" * 60)
    audit = AppRegistry.audit()
    print(f"\nTotal Apps: {audit['total_apps']}")
    print(f"By Layer: {audit['by_layer']}")
    print(f"Sovereign Gates: {audit['sovereign_gates_required']}")
    print("\nRegistered Apps:")
    for name in AppRegistry.list_all():
        print(f"  - {name}")
