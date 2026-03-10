import json
import inspect
from pathlib import Path

import pytest

from arifosmcp.runtime.bridge import call_kernel
from arifosmcp.runtime.tools import metabolic_loop_router
from arifosmcp.runtime.public_registry import PUBLIC_TOOL_SPECS
from core.governance_kernel import route_pipeline


def test_route_pipeline_uses_canonical_heart_stage():
    plan = route_pipeline("Assess safety risk and ethical impact before proceeding.")

    assert "666_HEART" in plan
    assert "555_HEART" not in plan


def test_public_kernel_schema_exposes_auth_context():
    kernel_spec = next(spec for spec in PUBLIC_TOOL_SPECS if spec.name == "arifOS.kernel")
    properties = kernel_spec.input_schema["properties"]

    assert "auth_context" in properties
    assert properties["auth_context"]["type"] == "object"


def test_public_kernel_router_accepts_auth_context():
    signature = inspect.signature(metabolic_loop_router)

    assert "auth_context" in signature.parameters


def test_manifest_kernel_schema_exposes_auth_context():
    manifest_path = Path(__file__).resolve().parents[1] / "spec" / "mcp-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    tool_properties = manifest["tools"]["arifOS.kernel"]["inputSchema"]["properties"]
    schema_properties = manifest["schema"]["input"]["arifOS.kernel"]["properties"]

    assert "auth_context" in tool_properties
    assert "auth_context" in schema_properties


@pytest.mark.asyncio
async def test_auth_failure_payload_includes_identity_resolution_and_next_action():
    envelope = await call_kernel(
        "arifOS.kernel",
        "session-auth-fail",
        {"query": "Assess deployment readiness.", "actor_id": "ARIF"},
    )

    payload = envelope["payload"]
    identity_resolution = payload["identity_resolution"]
    next_action = payload["next_action"]

    assert envelope["errors"][0]["code"] == "AUTH_FAILURE"
    assert "input_actor_id" in identity_resolution
    assert identity_resolution["resolved_actor_id"] == "anonymous"
    assert identity_resolution["identity_claim_status"] == "UNVERIFIED_CLAIM"
    assert next_action["tool"] == "init_anchor_state"
    assert next_action["required"] is True
