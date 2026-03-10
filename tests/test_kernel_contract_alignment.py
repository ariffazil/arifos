import inspect
import json
from pathlib import Path

import pytest

from arifosmcp.runtime.philosophy import select_governed_philosophy
from arifosmcp.runtime.public_registry import PUBLIC_TOOL_SPECS
from arifosmcp.runtime.tools import check_vital, metabolic_loop_router
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
async def test_auth_failure_payload_includes_identity_resolution_and_next_action():
    envelope = await metabolic_loop_router(
        query="Assess deployment readiness.",
        actor_id="ARIF",
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
    assert envelope.meta.motto == "🔥 IGNITE — DITEMPA, BUKAN DIBERI 💎"
    assert envelope.philosophy is not None
    assert envelope.philosophy["apex_mode"] == "deterministic_33"
    assert envelope.philosophy["agi"]["source"] == "deterministic_33"


@pytest.mark.asyncio
async def test_check_vital_includes_motto_and_governed_philosophy():
    envelope = await check_vital()

    assert envelope.meta.motto == "🔥 IGNITE — DITEMPA, BUKAN DIBERI 💎"
    assert envelope.philosophy is not None
    assert envelope.philosophy["stage"] == "000_INIT"
    assert envelope.philosophy["agi"]["source"] == "deterministic_33"
    assert envelope.philosophy["asi"] is None


def test_governed_philosophy_exposes_available_categories():
    payload = select_governed_philosophy(
        "Assess trade-offs in a paradox-heavy design review.",
        stage="333_MIND",
        verdict="SEAL",
        g_score=0.74,
        failed_floors=[],
        session_id="phi-1",
    )

    assert "local_99" in payload["available_categories"]
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
