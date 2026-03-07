"""
manifesto.py — Constitutional Manifesto for 333_APPS (FORWARDING STUB)

This file now acts as a forward-compatibility stub. 
All architectural definitions have been moved to `core.governance_kernel` 
to centralize the L0-L3 taxonomy inside the core kernel.
"""

from core.governance_kernel import (
    AppLayer,
    FloorClassification,
    FloorManifesto,
    AppManifesto,
    AppRegistry,
)

# ═══════════════════════════════════════════════════════════════════════════
# EXAMPLE MANIFESTOS (Template for new apps)
# ═══════════════════════════════════════════════════════════════════════════

def create_example_manifestos():
    """Create example manifestos for reference."""

    # Example: L4 Tool that analyzes documents
    doc_analyzer = AppManifesto(
        app_name="DocumentAnalyzer",
        layer=AppLayer.L3_CIVILIZATION,
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
        layer=AppLayer.L2_OPERATION,
        description="Executes L2 operational skills",
        floors=[
            FloorManifesto("F11", FloorClassification.HARD, None, "Must verify authority token"),
            FloorManifesto("F13", FloorClassification.HARD, None, "Cannot execute irreversible without gate"),
        ],
        requires_sovereign_gate=True,
        irreversible_actions=["delete", "modify_system"],
        l0_organs_used=["init_session", "apex_verdict", "vault_seal"],
    )

    return [doc_analyzer, task_executor]


if __name__ == "__main__":
    # Register examples
    examples = create_example_manifestos()
    for ex in examples:
        AppRegistry.register(ex)

    print("📋 CONSTITUTIONAL APP REGISTRY")
    print("======================")
    audit = AppRegistry.audit()
    print(f"Total Apps: {audit['total_apps']}")
    print(f"By Layer: {audit['by_layer']}")
    print(f"Sovereign Gates: {audit['sovereign_gates_required']}")
    print("Registered Apps:")
    for app_name in audit['apps'].keys():
        print(f"  - {app_name}")
