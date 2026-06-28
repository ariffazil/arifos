from __future__ import annotations

from arifosmcp.kernel.models import (
    AuthorityTier,
    BlastRadius,
    CapabilityGraph,
    CapabilityNode,
    GraphVersion,
    MutationClass,
    ResourceClass,
    TrustState,
)
from arifosmcp.kernel.substrate_readiness import (
    FORBIDDEN_PUBLIC_TOOLS,
    REQUIRED_CORE_TOOLS,
    ReadinessVerdict,
    assess_substrate_readiness,
)


def _ready_graph() -> CapabilityGraph:
    capabilities: list[CapabilityNode] = []
    for tool_name in sorted(REQUIRED_CORE_TOOLS):
        capabilities.append(
            CapabilityNode(
                capability_id=f"kernel.{tool_name}",
                tool_name=tool_name,
                server_id="local",
                description=f"Test capability for {tool_name}",
                authority_required=AuthorityTier.LOW,
                mutation_class=MutationClass.NONE,
                irreversible=False,
                blast_radius=BlastRadius.LOCAL,
                resource_class=ResourceClass.MEMORY,
                organ_id="arifOS",
                trust_state=TrustState.TRUSTED_READ,
                allow_python_fallback=False,
            )
        )

    for gate in ("arif_act", "arif_seal"):
        for cap in capabilities:
            if cap.tool_name == gate:
                cap.mutation_class = MutationClass.IRREVERSIBLE
                cap.irreversible = True
                cap.audit_required = True
                cap.requires_888_hold = True
                cap.requires_external_anchor = True

    return CapabilityGraph(
        version=GraphVersion(version_id="test-ready"),
        capabilities=capabilities,
    )


def test_substrate_readiness_returns_report_shape():
    report = assess_substrate_readiness(_ready_graph())

    assert report.total == 6
    assert report.passed == 6
    assert report.score == 100
    assert report.verdict == ReadinessVerdict.READY
    assert report.failed_checks == ()
    assert report.to_dict()["verdict"] == "READY"


def test_substrate_readiness_detects_missing_core_tool():
    graph = _ready_graph()
    graph.capabilities = [cap for cap in graph.capabilities if cap.tool_name != "arif_act"]
    graph.model_post_init(None)

    report = assess_substrate_readiness(graph)

    assert report.verdict == ReadinessVerdict.HOLD
    failed = {check.check_id: check for check in report.failed_checks}
    assert "CAPABILITY_GRAPH_COVERS_CORE_SEVEN" in failed
    assert failed["CAPABILITY_GRAPH_COVERS_CORE_SEVEN"].evidence["missing_core_tools"] == ["arif_act"]


def test_substrate_readiness_blocks_unsafe_mutation():
    graph = _ready_graph()
    graph.add(
        CapabilityNode(
            capability_id="unsafe.write",
            tool_name="unsafe_write",
            server_id="local",
            description="Unsafe write without audit",
            authority_required=AuthorityTier.MEDIUM,
            mutation_class=MutationClass.ORG_STATE,
            irreversible=False,
            blast_radius=BlastRadius.PROCESS,
            resource_class=ResourceClass.FILE,
            audit_required=False,
            allow_python_fallback=True,
            trust_state=TrustState.PROBATION,
        )
    )

    report = assess_substrate_readiness(graph)

    failed = {check.check_id: check for check in report.failed_checks}
    assert "MUTATIONS_ARE_AUDITED_NO_UNIVERSAL_FALLBACK" in failed
    assert "unsafe_write" in failed["MUTATIONS_ARE_AUDITED_NO_UNIVERSAL_FALLBACK"].evidence[
        "unsafe_mutating_tools"
    ]
    assert "NO_UNIVERSAL_PYTHON_ESCAPE_HATCH" in failed


def test_substrate_readiness_blocks_unwitnessed_irreversible_action():
    graph = _ready_graph()
    graph.add(
        CapabilityNode(
            capability_id="unsafe.delete",
            tool_name="unsafe_delete",
            server_id="local",
            description="Irreversible delete without witness or hold",
            authority_required=AuthorityTier.HIGH,
            mutation_class=MutationClass.IRREVERSIBLE,
            irreversible=True,
            blast_radius=BlastRadius.FEDERATION,
            resource_class=ResourceClass.FILE,
            audit_required=True,
            allow_python_fallback=False,
            trust_state=TrustState.PROBATION,
        )
    )

    report = assess_substrate_readiness(graph)

    failed = {check.check_id: check for check in report.failed_checks}
    assert "IRREVERSIBLE_ACTIONS_REQUIRE_EXTERNALITY_OR_HOLD" in failed
    assert "unsafe_delete" in failed[
        "IRREVERSIBLE_ACTIONS_REQUIRE_EXTERNALITY_OR_HOLD"
    ].evidence["unsafe_irreversible_tools"]


def test_forbidden_public_tool_set_names_sovereign_machinery():
    assert {
        "arif_bridge_connect",
        "arif_gateway_connect",
        "arif_forge_execute",
        "arif_vault_seal",
        "arif_memory_recall",
        "hermes_vault_query",
        "arif_canary",
        "arif_conformance_report",
    }.issubset(FORBIDDEN_PUBLIC_TOOLS)
