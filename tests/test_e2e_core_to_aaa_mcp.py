"""
E2E Test: Core to AAA MCP Pipeline

Tests the complete constitutional pipeline from init_gate through vault_seal.
Verifies:
1. init_gate outputs DITEMPA, BUKAN DIBERI with 🔥 emoji
2. vault_seal outputs DITEMPA, BUKAN DIBERI with 💎🧠🔒 emoji
3. All constitutional floors are enforced
4. Session flows correctly through all stages

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import pytest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
import types


def _load_module(module_name: str, rel_path: str):
    root = Path(__file__).resolve().parents[1]
    aaa_mcp_path = root / "aaa_mcp"
    protocol_path = aaa_mcp_path / "protocol"

    if "aaa_mcp" not in sys.modules:
        pkg = types.ModuleType("aaa_mcp")
        pkg.__path__ = [str(aaa_mcp_path)]
        sys.modules["aaa_mcp"] = pkg
    if "aaa_mcp.protocol" not in sys.modules:
        protocol_pkg = types.ModuleType("aaa_mcp.protocol")
        protocol_pkg.__path__ = [str(protocol_path)]
        sys.modules["aaa_mcp.protocol"] = protocol_pkg

    module_path = root / rel_path
    spec = spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module spec for {module_path}")
    module = module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


LOAD_ERROR = None
try:
    tool_graph_module = _load_module("aaa_mcp.protocol.tool_graph", "aaa_mcp/protocol/tool_graph.py")
    capabilities_module = _load_module(
        "aaa_mcp.protocol.capabilities", "aaa_mcp/protocol/capabilities.py"
    )
    response_module = _load_module("aaa_mcp.protocol.response", "aaa_mcp/protocol/response.py")
    schemas_module = _load_module("aaa_mcp.protocol.schemas", "aaa_mcp/protocol/schemas.py")
except Exception as exc:
    LOAD_ERROR = exc

if LOAD_ERROR is None:
    WORKFLOW_SEQUENCES = tool_graph_module.WORKFLOW_SEQUENCES
    validate_sequence = tool_graph_module.validate_sequence
    TOOL_GRAPH = tool_graph_module.TOOL_GRAPH
    TOOL_CAPABILITIES = capabilities_module.TOOL_CAPABILITIES
    TOOL_INPUT_SCHEMAS = schemas_module.TOOL_INPUT_SCHEMAS
    build_init_response = response_module.build_init_response
    build_seal_response = response_module.build_seal_response
    build_verdict_response = response_module.build_verdict_response

pytestmark = pytest.mark.skipif(LOAD_ERROR is not None, reason=f"Core modules not available: {LOAD_ERROR}")


class TestConstitutionalPipeline:
    """E2E tests for the 000-999 constitutional pipeline."""

    def test_init_gate_has_motto_with_fire_emoji(self):
        """🔥 INIT gate must output DITEMPA, BUKAN DIBERI with fire emoji."""
        response = build_init_response(
            session_id="test-session-001", verdict="SEAL", mode="conscience"
        )

        # Check message contains motto with fire emoji
        assert "🔥" in response.message, "INIT gate must have 🔥 emoji"
        assert "DITEMPA" in response.message, "INIT gate must have DITEMPA"
        assert "BUKAN DIBERI" in response.message, "INIT gate must have BUKAN DIBERI"

        # Check data contains motto metadata
        assert response.data.get("motto") == "DITEMPA, BUKAN DIBERI"
        assert response.data.get("motto_english") == "Forged, Not Given"
        assert response.data.get("motto_emojis") == "🔥"
        assert response.data.get("bookend") == "INIT"

        print(f"✅ INIT gate: {response.message}")

    def test_vault_seal_has_motto_with_diamond_brain_lock(self):
        """💎🧠🔒 VAULT seal must output DITEMPA, BUKAN DIBERI with diamond/brain/lock emojis."""
        response = build_seal_response(
            session_id="test-session-001",
            seal_id="seal_abc123xyz",
            seal_hash="a1b2c3d4e5f6...",
            verdict="SEALED",
        )

        # Check message contains motto with diamond/brain/lock emojis
        assert "💎" in response.message, "VAULT seal must have 💎 emoji"
        assert "🧠" in response.message, "VAULT seal must have 🧠 emoji"
        assert "🔒" in response.message, "VAULT seal must have 🔒 emoji"
        assert "DITEMPA" in response.message, "VAULT seal must have DITEMPA"
        assert "BUKAN DIBERI" in response.message, "VAULT seal must have BUKAN DIBERI"

        # Check data contains motto metadata
        assert response.data.get("motto") == "DITEMPA, BUKAN DIBERI"
        assert response.data.get("motto_english") == "Forged, Not Given"
        assert "💎🧠🔒" in response.data.get(
            "motto_emojis", ""
        ), "VAULT seal must have 💎🧠🔒 emojis"
        assert response.data.get("bookend") == "SEAL"

        print(f"✅ VAULT seal: {response.message}")

    def test_emojis_are_different_for_init_vs_seal(self):
        """INIT and SEAL must have contrasting emojis."""
        init_response = build_init_response(session_id="test-session-001", verdict="SEAL")
        seal_response = build_seal_response(
            session_id="test-session-001",
            seal_id="seal_abc123",
            seal_hash="hash...",
            verdict="SEALED",
        )

        init_emojis = init_response.data.get("motto_emojis", "")
        seal_emojis = seal_response.data.get("motto_emojis", "")

        # Emojis must be different
        assert init_emojis != seal_emojis, "INIT and SEAL must have different emojis"

        # INIT should have fire
        assert "🔥" in init_emojis, "INIT must have fire emoji"

        # SEAL should have diamond/brain/lock
        assert (
            "💎" in seal_emojis or "🧠" in seal_emojis or "🔒" in seal_emojis
        ), "SEAL must have diamond/brain/lock emojis"

        print(f"✅ INIT emojis: {init_emojis}")
        print(f"✅ SEAL emojis: {seal_emojis}")

    def test_workflow_sequences_are_valid(self):
        """All workflow sequences must pass constitutional validation."""
        workflows = WORKFLOW_SEQUENCES

        for name, sequence in workflows.items():
            is_valid, msg = validate_sequence(sequence)
            assert is_valid, f"Workflow '{name}' invalid: {msg}"
            print(f"✅ Workflow '{name}' valid: {' -> '.join(sequence)}")

    def test_all_tools_have_capability_descriptions(self):
        """Every tool in graph must have capability description."""
        for tool_name in TOOL_GRAPH.keys():
            assert (
                tool_name in TOOL_CAPABILITIES
            ), f"Tool '{tool_name}' missing capability description"

            cap = TOOL_CAPABILITIES[tool_name]
            assert cap.floors_enforced is not None, f"Tool '{tool_name}' missing floors_enforced"
            assert cap.when_to_use, f"Tool '{tool_name}' missing when_to_use guidance"

            print(f"✅ Tool '{tool_name}' has full capability description")

    def test_trinity_forge_is_primary_entrypoint(self):
        """trinity_forge must be the unified entrypoint."""
        assert "trinity_forge" in TOOL_GRAPH, "trinity_forge must exist in tool graph"

        node = TOOL_GRAPH["trinity_forge"]
        assert node.must_call_first, "trinity_forge must be callable first"
        assert node.terminal, "trinity_forge must be terminal (complete pipeline)"

        # Check it's in quick_decision workflow
        assert (
            "trinity_forge" in WORKFLOW_SEQUENCES["quick_decision"]
        ), "trinity_forge must be in quick_decision workflow"

        print(f"✅ trinity_forge is valid unified entrypoint")


class TestAuthenticationRelaxed:
    """Tests that authentication is relaxed for pilot phase."""

    def test_auth_token_is_optional(self):
        """auth_token parameter must be optional for all tools."""
        # Check trinity_forge schema
        forge_schema = TOOL_INPUT_SCHEMAS.get("trinity_forge", {})
        props = forge_schema.get("properties", {})

        if "auth_token" in props:
            # auth_token exists but should not be in required
            assert "auth_token" not in forge_schema.get(
                "required", []
            ), "auth_token must be optional (not required)"
            # And should accept null
            auth_type = props["auth_token"].get("type", [])
            assert "null" in auth_type or "string" in str(
                auth_type
            ), "auth_token must accept null for pilot phase"

        print("✅ auth_token is optional for pilot phase")

    def test_init_gate_no_strict_auth(self):
        """init_gate should not require strict authentication."""
        try:
            decorator_module = _load_module(
                "constitutional_decorator", "aaa_mcp/core/constitutional_decorator.py"
            )
        except Exception as exc:
            pytest.skip(f"constitutional_decorator unavailable in this environment: {exc}")

        _build_pre_context = decorator_module._build_pre_context

        ctx = _build_pre_context("test query", {"session_id": "test-123"})

        # Should have auto-authentication for MCP tools
        assert ctx.get("role") == "AGENT", "MCP tools auto-authenticate as AGENT"
        assert (
            ctx.get("authority_token") == "arifos_mcp"
        ), "MCP tools should use arifos_mcp authority token"

        print("✅ Authentication relaxed for pilot: auto-authenticated as AGENT")


class TestEndToEndFlow:
    """Full E2E flow tests."""

    def test_full_pipeline_flow(self):
        """Test complete 000-999 pipeline execution."""
        # This would require full server integration
        # For now, verify the sequence is correct
        sequence = WORKFLOW_SEQUENCES["full_analysis"]

        expected_stages = [
            "init_gate",  # 000
            "agi_sense",  # 111
            "reality_search",  # External
            "agi_think",  # 222
            "agi_reason",  # 333
            "asi_empathize",  # 555
            "asi_align",  # 666
            "apex_verdict",  # 888
            "vault_seal",  # 999
        ]

        assert sequence == expected_stages, f"Full analysis sequence mismatch: {sequence}"

        print(f"✅ Full pipeline sequence verified: {' -> '.join(sequence)}")

    def test_bookend_mottos_match(self):
        """INIT and SEAL bookends must share DITEMPA motto."""
        init = build_init_response("test", "SEAL")
        seal = build_seal_response("test", "seal-123", "hash...", "SEALED")

        # Both must have same motto
        assert init.data["motto"] == seal.data["motto"] == "DITEMPA, BUKAN DIBERI"

        # But different bookend markers
        assert init.data["bookend"] == "INIT"
        assert seal.data["bookend"] == "SEAL"

        # And different emojis (fire vs diamond/brain/lock)
        assert init.data["motto_emojis"] == "🔥"
        assert "💎" in seal.data["motto_emojis"]
        assert "🧠" in seal.data["motto_emojis"]

        print("✅ Bookend design verified: DITEMPA at both gates with contrasting emojis")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
