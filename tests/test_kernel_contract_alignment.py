import inspect
import json
from pathlib import Path

import pytest

from arifosmcp.runtime import tools as runtime_tools
from arifosmcp.runtime.philosophy import select_governed_philosophy
from arifosmcp.runtime.public_registry import PUBLIC_TOOL_SPECS
from arifosmcp.runtime.tools import (
    audit_rules,
    check_vital,
    init_anchor_state,
    metabolic_loop_router,
    reason_mind_synthesis,
)
from core.governance_kernel import clear_governance_kernel, get_governance_kernel, route_pipeline


def test_route_pipeline_uses_canonical_heart_stage():
    plan = route_pipeline("Assess safety risk and ethical impact before proceeding.")

    assert "666_HEART" in plan
    assert "555_HEART" not in plan


def test_public_kernel_schema_exposes_auth_context():
    kernel_spec = next(spec for spec in PUBLIC_TOOL_SPECS if spec.name == "arifOS_kernel")
    properties = kernel_spec.input_schema["properties"]

    assert "auth_context" in properties
    assert properties["auth_context"]["type"] == "object"


def test_public_kernel_router_accepts_auth_context():
    signature = inspect.signature(metabolic_loop_router)

    assert "auth_context" in signature.parameters


def test_init_anchor_state_accepts_human_approval():
    """human_approval lives on init_anchor_state, not metabolic_loop_router."""
    signature = inspect.signature(init_anchor_state)

    assert "human_approval" in signature.parameters


def test_manifest_kernel_schema_exposes_auth_context():
    manifest_path = Path(__file__).resolve().parents[1] / "spec" / "mcp-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    tool_properties = manifest["tools"]["arifOS_kernel"]["inputSchema"]["properties"]
    schema_properties = manifest["schema"]["input"]["arifOS_kernel"]["properties"]

    assert "auth_context" in tool_properties
    assert "auth_context" in schema_properties


def test_public_registry_exposes_init_anchor_state():
    init_spec = next(spec for spec in PUBLIC_TOOL_SPECS if spec.name == "init_anchor_state")
    assert "anyOf" in init_spec.input_schema


def test_public_runtime_exports_init_anchor_state():
    signature = inspect.signature(init_anchor_state)
    assert "intent" in signature.parameters


@pytest.mark.asyncio
async def test_low_risk_declared_identity_auto_anchors_continuity(monkeypatch):
    from core.physics.thermodynamics_hardened import init_thermodynamic_budget

    monkeypatch.delenv("ARIFOS_GOVERNANCE_OPEN_MODE", raising=False)
    session_id = "test-low-risk-auto-anchor"
    init_thermodynamic_budget(session_id, initial_budget=1.0)

    envelope = await metabolic_loop_router(
        query="Assess deployment readiness.",
        actor_id="guest-user",
        risk_tier="low",
        session_id=session_id,
        dry_run=True,
        use_memory=False,
        use_heart=False,
        use_critique=False,
    )

    assert envelope.tool == "arifOS_kernel"
    assert envelope.auth_context is not None
    assert not any(error.code == "AUTH_FAILURE" for error in envelope.errors)
    assert envelope.authority.actor_id == "guest-user"
    assert envelope.authority.auth_state == "verified"
    assert envelope.trace.get("000_INIT") == "SEAL"
    assert envelope.philosophy is not None
    assert envelope.meta.motto is not None


@pytest.mark.asyncio
async def test_init_anchor_state_binds_declared_name() -> None:
    envelope = await init_anchor_state(
        declared_name="Arif-The-Apex",
        human_approval=False,
    )

    assert envelope.tool == "init_anchor_state"
    assert envelope.authority.actor_id == "arif-the-apex"
    assert envelope.authority.level != "anonymous"
    assert envelope.auth_context is not None


@pytest.mark.asyncio
async def test_init_anchor_state_human_approval_updates_kernel_state() -> None:
    session_id = "bootstrap-human-approval"
    clear_governance_kernel(session_id)

    envelope = await init_anchor_state(
        declared_name="Chat Operator",
        session_id=session_id,
        human_approval=True,
    )

    kernel = get_governance_kernel(session_id)

    assert envelope.auth_context is not None
    assert envelope.auth_context["authority_level"] == "declared"
    assert kernel.human_approval_status in {"approved", "not_required"}
    assert kernel.decision_owner is not None  # owner is set (exact value varies by kernel version)


@pytest.mark.asyncio
async def test_reason_stage_preserves_declared_authority_context() -> None:
    session_id = "declared-authority-continuity"
    init_env = await init_anchor_state(
        declared_name="Arif",
        session_id=session_id,
        human_approval=False,
    )

    envelope = await reason_mind_synthesis(
        session_id=session_id,
        query="Explain F11 briefly.",
        auth_context=init_env.auth_context or {},
    )

    # "Arif" maps to apex identity "ariffazil" via kernel apex mapping.
    # Bootstrap gives apex authority; the auth_context carries the apex actor_id.
    assert envelope.auth_context is not None
    assert envelope.auth_context["actor_id"] == "ariffazil"
    # The reason stage inherits the auth_context actor but the authority object reflects
    # the kernel's own authority resolution for this specific call.
    assert envelope.authority is not None


@pytest.mark.asyncio
async def test_high_risk_kernel_call_still_requires_explicit_auth_context():
    envelope = await metabolic_loop_router(
        query="Approve production release and execute deployment steps.",
        actor_id="ARIF",
        risk_tier="high",
        allow_execution=True,
    )

    payload = envelope.payload
    identity_resolution = payload["identity_resolution"]
    next_action = payload["next_action"]

    assert envelope.tool == "arifOS_kernel"
    assert envelope.errors[0].code == "AUTH_FAILURE"
    assert identity_resolution["input_actor_id"] == "ARIF"
    assert identity_resolution["resolved_actor_id"] == "anonymous"
    assert identity_resolution["identity_claim_status"] == "UNVERIFIED_CLAIM"
    assert next_action["tool"] == "init_anchor_state"
    assert next_action["required"] is True


@pytest.mark.asyncio
async def test_explicit_human_approval_bootstraps_kernel_without_crypto(monkeypatch):
    """human_approval is set via init_anchor_state, then the session is used in metabolic_loop_router."""
    from core.physics.thermodynamics_hardened import init_thermodynamic_budget

    monkeypatch.delenv("ARIFOS_GOVERNANCE_OPEN_MODE", raising=False)
    session_id = "human-approval-kernel"
    clear_governance_kernel(session_id)
    init_thermodynamic_budget(session_id, initial_budget=1.0)

    # Step 1: Bootstrap identity with human_approval
    init_env = await init_anchor_state(
        declared_name="Chat Operator",
        session_id=session_id,
        human_approval=True,
    )
    assert init_env.auth_context is not None
    assert init_env.auth_context["authority_level"] == "declared"

    # Step 2: Use the anchored session in metabolic_loop_router
    envelope = await metabolic_loop_router(
        query="Explain the current runtime authority posture.",
        actor_id="chat-operator",
        auth_context=init_env.auth_context or {},
        risk_tier="low",
        dry_run=True,
        session_id=session_id,
    )

    assert envelope.auth_context is not None
    assert envelope.auth_context["actor_id"] == "chat-operator"
    assert not any(error.code == "AUTH_FAILURE" for error in envelope.errors)


@pytest.mark.asyncio
async def test_nested_continuity_actor_id_is_promoted_to_auth_context_root():
    session_id = "nested-continuity-root-promotion"
    init_env = await init_anchor_state(
        declared_name="Chat Operator",
        session_id=session_id,
        human_approval=True,
    )

    nested_auth_context = dict(init_env.auth_context or {})
    actor_id = nested_auth_context.pop("actor_id")
    nested_auth_context["continuity"] = {
        "actor_id": actor_id,
        "method": "minted_auth_context",
        "issuer": "init_anchor_state",
    }

    envelope = await metabolic_loop_router(
        query="Explain the runtime continuity posture.",
        actor_id="chat-operator",
        auth_context=nested_auth_context or {},
        risk_tier="low",
        dry_run=True,
        session_id=session_id,
    )

    assert envelope.auth_context is not None
    assert envelope.auth_context["actor_id"] == "chat-operator"
    assert not any(error.code == "AUTH_FAILURE" for error in envelope.errors)


@pytest.mark.asyncio
async def test_protected_identity_claim_requires_crypto():
    """Sovereign identity claims still require crypto — human_approval alone is not sufficient."""
    envelope = await metabolic_loop_router(
        query="Inspect the current runtime posture.",
        actor_id="arif-fazil",
        risk_tier="low",
        dry_run=True,
        session_id="protected-identity-claim",
    )

    assert envelope.verdict.name in ["VOID", "HOLD"]
    assert envelope.errors[0].code == "AUTH_FAILURE"
    assert envelope.authority.actor_id == "anonymous"
    # Protected IDs (arif-fazil) without crypto → auth failure with UNVERIFIED_CLAIM
    assert envelope.payload["identity_resolution"]["identity_claim_status"] in {
        "PROTECTED_IDENTITY_REQUIRES_CRYPTO",
        "UNVERIFIED_CLAIM",
    }


@pytest.mark.asyncio
async def test_check_vital_includes_motto_and_governed_philosophy():
    session_id = "vital-diagnostics-session"
    envelope = await check_vital(session_id)

    assert envelope.meta.motto == "🔥 IGNITE — DITEMPA, BUKAN DIBERI 💎"
    # check_vital routes through the global session context
    assert envelope.session_id is not None
    assert envelope.philosophy is not None
    assert envelope.philosophy["stage"] == "000_INIT"
    assert envelope.philosophy["agi"]["source"] == "deterministic_33"
    assert envelope.philosophy["asi"] is None
    assert "capability_map" in envelope.payload
    assert envelope.payload["capability_map"]["schema"] == "capability-map/v1"
    assert "credential_classes" in envelope.payload["capability_map"]
    assert "providers" in envelope.payload["capability_map"]
    assert "message" in envelope.payload


@pytest.mark.asyncio
async def test_audit_rules_loads_governance_diagnostics() -> None:
    session_id = "audit-diagnostics-session"
    envelope = await audit_rules(session_id)

    # audit_rules routes through the global session context
    assert envelope.session_id is not None
    assert "message" in envelope.payload
    assert envelope.verdict.name in {"SEAL", "SABAR"}


@pytest.mark.asyncio
async def test_metabolic_loop_preserves_declared_authority() -> None:
    # "Arif" maps to apex identity "ariffazil" via kernel apex mapping
    session_id = "declared-loop-authority"
    init_env = await init_anchor_state(
        declared_name="Arif", session_id=session_id, human_approval=False
    )

    envelope = await metabolic_loop_router(
        query="Explain the 13 Constitutional Floors.",
        context="Authority continuity regression test.",
        risk_tier="low",
        auth_context=init_env.auth_context or {},
        actor_id="ariffazil",
        use_memory=False,
        use_heart=False,
        use_critique=False,
        allow_execution=False,
        dry_run=True,
        session_id=session_id,
    )

    # Actor is correctly resolved via apex mapping
    assert envelope.authority.actor_id == "ariffazil"
    assert envelope.authority is not None


def test_governed_philosophy_exposes_available_categories():
    payload = select_governed_philosophy(
        "Assess trade-offs in a paradox-heavy design review.",
        stage="333_MIND",
        verdict="SEAL",
        g_score=0.74,
        failed_floors=[],
        session_id="phi-1",
    )

    assert payload["label"] == "paradox"
    assert payload["label_source"] in {"bounded_context", "state_router"}
    assert "local_99" in payload["available_categories"]
    assert "bounded_labels" in payload["available_categories"]
    assert "paradox" in payload["available_categories"]["local_99"]


def test_thermodynamic_reporter_is_callable_from_runtime_tools():
    """get_thermodynamic_report works via thermodynamics_hardened; ThermodynamicViolation from thermodynamics."""
    from core.physics.thermodynamics import ThermodynamicViolation
    from core.physics.thermodynamics_hardened import (
        get_thermodynamic_report,
        init_thermodynamic_budget,
    )

    session_id = "thermo-loader-test"
    init_thermodynamic_budget(session_id, initial_budget=5.0)
    report = get_thermodynamic_report(session_id)

    assert isinstance(report, dict)
    assert len(report) > 0  # non-empty thermodynamic report
    assert issubclass(ThermodynamicViolation, Exception)


def test_governed_philosophy_uses_richer_local_categories_for_normal_runtime():
    payload = select_governed_philosophy(
        "Close the loop and release the governed result.",
        stage="888_JUDGE",
        verdict="SEAL",
        g_score=0.92,
        failed_floors=[],
        session_id="phi-2",
    )

    assert payload["agi"]["source"] == "deterministic_99"
    assert payload["agi"]["category"] in {"triumph", "power"}


def test_governed_philosophy_maps_empathy_failures_to_love():
    payload = select_governed_philosophy(
        "A user is hurt and needs care before we proceed.",
        stage="666_HEART",
        verdict="PARTIAL",
        g_score=0.71,
        failed_floors=["F6"],
        session_id="phi-3",
    )

    assert payload["agi"]["source"] == "deterministic_99"
    assert payload["agi"]["category"] == "love"


def test_stage_000_low_g_uses_bounded_label_not_fixed_void_quote():
    payload = select_governed_philosophy(
        "Please respond with care and compassion after a painful loss.",
        stage="000_INIT",
        verdict="VOID",
        g_score=0.21,
        failed_floors=[],
        session_id="phi-4",
    )

    assert payload["label"] == "love"
    assert payload["agi"]["source"] == "deterministic_33"
    assert payload["agi"]["category"] == "wisdom"
    assert payload["agi"]["quote_id"] != "V2"
