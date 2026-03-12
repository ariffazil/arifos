import inspect
import json
from pathlib import Path

import pytest

from arifosmcp.runtime.philosophy import select_governed_philosophy
from arifosmcp.runtime.public_registry import PUBLIC_TOOL_SPECS
from arifosmcp.runtime.tools import bootstrap_identity, check_vital, metabolic_loop_router
from core.governance_kernel import route_pipeline


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


def test_manifest_kernel_schema_exposes_auth_context():
    manifest_path = Path(__file__).resolve().parents[1] / "spec" / "mcp-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    tool_properties = manifest["tools"]["arifOS_kernel"]["inputSchema"]["properties"]
    schema_properties = manifest["schema"]["input"]["arifOS_kernel"]["properties"]

    assert "auth_context" in tool_properties
    assert "auth_context" in schema_properties


@pytest.mark.asyncio
async def test_low_risk_open_mode_mints_context_but_keeps_unverified_authority(monkeypatch):
    from core.physics.thermodynamics_hardened import init_thermodynamic_budget
    monkeypatch.setenv("ARIFOS_GOVERNANCE_OPEN_MODE", "1")
    
    # We need a stable session_id to init budget
    session_id = "test_low_risk_auto"
    init_thermodynamic_budget(session_id, initial_budget=1.0)
    
    envelope = await metabolic_loop_router(
        query="Assess deployment readiness.",
        actor_id="ARIF",
        risk_tier="low",
        session_id=session_id,
    )

    assert envelope.tool == "arifOS_kernel"
    assert envelope.auth_context is not None
    assert any(error.code == "AUTH_FAILURE" for error in envelope.errors)
    assert envelope.verdict == "VOID"
    assert envelope.authority.actor_id == "anonymous"
    assert envelope.authority.auth_state == "unverified"
    assert envelope.trace.get("000_INIT") == "SEAL"
    assert envelope.philosophy is not None
    assert envelope.meta.motto is not None


@pytest.mark.asyncio
async def test_bootstrap_identity_binds_declared_name() -> None:
    envelope = await bootstrap_identity(declared_name="Arif-The-Sovereign")

    assert envelope.tool == "bootstrap_identity"
    assert envelope.authority.actor_id == "arif-the-sovereign"
    assert envelope.authority.level == "declared"
    assert envelope.auth_context is not None


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
async def test_check_vital_includes_motto_and_governed_philosophy():
    envelope = await check_vital()

    assert envelope.meta.motto == "🔥 IGNITE — DITEMPA, BUKAN DIBERI 💎"
    assert envelope.philosophy is not None
    assert envelope.philosophy["stage"] == "000_INIT"
    assert envelope.philosophy["agi"]["source"] == "deterministic_33"
    assert envelope.philosophy["asi"] is None
    assert "capability_map" in envelope.payload
    assert envelope.payload["capability_map"]["schema"] == "capability-map/v1"
    assert "credential_classes" in envelope.payload["capability_map"]
    assert "providers" in envelope.payload["capability_map"]


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
