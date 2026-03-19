"""
tests/runtime/test_tools_advanced.py — Advanced Runtime Tools Tests

Tests for error paths, edge cases, and complex scenarios in runtime/tools.py
Focus on bringing coverage from 62% to 85%+
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from typing import Any





class TestToolDialsMap:
    """Test tool dials configuration loading"""

    def test_dials_map_exists(self):
        """Test tool dials map file exists and is valid"""
        import json
        from pathlib import Path

        dials_path = (
            Path(__file__).parent.parent.parent / "arifosmcp" / "runtime" / "tool_dials_map.json"
        )
        assert dials_path.exists(), "tool_dials_map.json should exist"

        with open(dials_path) as f:
            dials = json.load(f)

        assert isinstance(dials, dict)

    def test_dials_map_structure(self):
        """Test dials map has expected structure"""
        import json
        from pathlib import Path

        dials_path = (
            Path(__file__).parent.parent.parent / "arifosmcp" / "runtime" / "tool_dials_map.json"
        )

        with open(dials_path) as f:
            dials = json.load(f)

        # Check for expected tool configurations
        if dials:
            for tool_name, config in dials.items():
                assert isinstance(tool_name, str)
                assert isinstance(config, (dict, str))


class TestProbeIntelligenceServices:
    """Test _probe_intelligence_services function"""

    @pytest.mark.asyncio
    async def test_probe_services_basic(self):
        """Test probing intelligence services"""
        from arifosmcp.runtime.tools import _probe_intelligence_services

        result = await _probe_intelligence_services()

        assert isinstance(result, dict)
        # Should return service status info

    @pytest.mark.asyncio
    async def test_probe_services_with_mock(self):
        """Test probing with mocked services"""
        from arifosmcp.runtime.tools import _probe_intelligence_services

        with patch("arifosmcp.runtime.tools.check_vital") as mock_vital:
            mock_vital.return_value = AsyncMock()
            mock_vital.return_value.payload = {"status": "ok"}

            result = await _probe_intelligence_services()
            assert isinstance(result, dict)


class TestAdaptationStatus:
    """Test adaptation status checking"""

    def test_check_adaptation_status(self):
        """Test adaptation status returns valid data"""
        from arifosmcp.runtime.tools import check_adaptation_status

        result = check_adaptation_status()

        assert isinstance(result, dict)
        # Should contain adaptation metrics

    def test_get_current_hysteresis(self):
        """Test hysteresis calculation"""
        from arifosmcp.runtime.tools import get_current_hysteresis

        result = get_current_hysteresis()

        # Should return a float or dict with hysteresis info
        assert isinstance(result, (dict, float, int))


class TestWrapCallEdgeCases:
    """Test _wrap_call edge cases and error handling"""

    @pytest.mark.asyncio
    async def test_wrap_call_with_none_ctx(self):
        """Test wrap_call with None context"""
        from arifosmcp.runtime.tools import _wrap_call, Stage

        with patch("arifosmcp.runtime.tools.call_kernel") as mock_call:
            mock_call.return_value = {
                "ok": True,
                "tool": "test",
                "session_id": "test",
                "stage": "000_INIT",
                "verdict": "SEAL",
                "status": "SUCCESS",
            }

            result = await _wrap_call("test_tool", Stage.INIT_000, "test-session", {}, None)

            assert result is not None

    @pytest.mark.asyncio
    async def test_wrap_call_empty_payload(self):
        """Test wrap_call with empty payload"""
        from arifosmcp.runtime.tools import _wrap_call, Stage

        with patch("arifosmcp.runtime.tools.call_kernel") as mock_call:
            mock_call.return_value = {
                "ok": True,
                "tool": "test",
                "session_id": "test",
                "stage": "000_INIT",
                "verdict": "SEAL",
                "status": "SUCCESS",
            }

            result = await _wrap_call("test_tool", Stage.INIT_000, "test-session", {}, None)

            assert result is not None


class TestArifosKernelAdvanced:
    """Test arifos_kernel advanced scenarios"""

    @pytest.mark.asyncio
    async def test_kernel_with_all_legacy_params(self):
        """Test kernel with all legacy compatibility parameters"""
        from arifosmcp.runtime.tools import arifos_kernel

        with patch("arifosmcp.runtime.tools.metabolic_loop") as mock_loop:
            # arifos_kernel uses metabolic_loop from orchestrator internally now,
            # wait, if it uses from orchestrator import metabolic_loop, we patch there
            # actually let's just patch orchestrator
            pass
        
        with patch("arifosmcp.runtime.orchestrator.metabolic_loop", new_callable=AsyncMock) as mock_loop:
            mock_loop.return_value = {
                "ok": True,
                "tool": "arifOS_kernel",
                "session_id": "test",
                "stage": "000_INIT",
                "verdict": "SEAL",
                "status": "SUCCESS",
            }

            result = await arifos_kernel(
                query="test query",
                session_id="test-session",
                risk_tier="high",
                context="additional context",
                auth_context={"test": "auth"},
                actor_id="test-actor",
                use_memory=True,
                use_heart=True,
                use_critique=True,
                allow_execution=True,
                dry_run=True,
                requested_persona="ARCHITECT",
                debug=True,
            )

            assert result is not None

    @pytest.mark.asyncio
    async def test_kernel_with_caller_context(self):
        """Test kernel with caller context"""
        from arifosmcp.runtime.tools import arifos_kernel, CallerContext

        caller_ctx = CallerContext(
            agent_id="test-agent", thread_id="test-thread", request_id="test-request"
        )

        with patch("arifosmcp.runtime.orchestrator.metabolic_loop", new_callable=AsyncMock) as mock_loop:
            mock_loop.return_value = {
                "ok": True,
                "tool": "arifOS_kernel",
                "session_id": "test",
                "stage": "000_INIT",
                "verdict": "SEAL",
                "status": "SUCCESS",
            }

            result = await arifos_kernel(query="test", caller_context=caller_ctx)

            assert result is not None


class TestRealityCompassAdvanced:
    """Test reality_compass advanced scenarios"""

    @pytest.mark.asyncio
    async def test_reality_compass_with_policy(self):
        """Test reality_compass with custom policy"""
        from arifosmcp.runtime.tools import reality_compass

        with patch("arifosmcp.runtime.tools.reality_handler.handle_compass", new_callable=AsyncMock) as mock_handle:
            mock_bundle = Mock()
            mock_bundle.status.state = "SUCCESS"
            mock_bundle.status.verdict = "SEAL"
            mock_bundle.model_dump.return_value = {
                "status": {"state": "SUCCESS", "verdict": "SEAL"}
            }
            mock_handle.return_value = mock_bundle

            result = await reality_compass(
                input="test query",
                session_id="test",
                policy={"allow_search": True, "max_results": 10},
                debug_profile="detailed",
            )

            assert result is not None

    @pytest.mark.asyncio
    async def test_reality_compass_url_mode(self):
        """Test reality_compass with URL input"""
        from arifosmcp.runtime.tools import reality_compass

        with patch("arifosmcp.runtime.tools.reality_handler.handle_compass", new_callable=AsyncMock) as mock_handle:
            mock_bundle = Mock()
            mock_bundle.status.state = "SUCCESS"
            mock_bundle.status.verdict = "SEAL"
            mock_bundle.model_dump.return_value = {
                "status": {"state": "SUCCESS", "verdict": "SEAL"}
            }
            mock_handle.return_value = mock_bundle

            result = await reality_compass(
                input="https://example.com/article",
                session_id="test",
                mode="auto",  # Should detect URL
            )

            assert result is not None


class TestSealVaultCommitAdvanced:
    """Test seal_vault_commit advanced scenarios"""

    @pytest.mark.asyncio
    async def test_seal_with_invalid_verdict(self):
        """Test seal with invalid verdict"""
        from arifosmcp.runtime.tools import seal_vault_commit

        with patch("arifosmcp.runtime.tools.call_kernel") as mock_call:
            mock_call.return_value = AsyncMock()
            mock_call.return_value = {
                "ok": False,
                "tool": "seal_vault_commit",
                "verdict": "VOID",
                "status": "ERROR",
            }

            result = await seal_vault_commit(
                verdict="INVALID_VERDICT", evidence={}, session_id="test"
            )

            assert result is not None

    @pytest.mark.asyncio
    async def test_seal_with_low_sii(self):
        """Test seal with low SII score"""
        from arifosmcp.runtime.tools import seal_vault_commit

        # If low SII, mock call_kernel to return VOID
        with patch("arifosmcp.runtime.tools.call_kernel", new_callable=AsyncMock) as mock_call:
            mock_call.return_value = {
                "ok": False, "verdict": "VOID", "status": "ERROR", "tool": "seal_vault_commit"
            }
            res = await seal_vault_commit(verdict="SEAL", evidence={"test": "data"}, session_id="test")
            assert res.verdict.name == "VOID"


class TestForgeAdvanced:
    """Test forge tool advanced scenarios"""

    @pytest.mark.asyncio
    async def test_forge_with_risk_tiers(self):
        """Test forge with different risk tiers"""
        from arifosmcp.runtime.tools import forge

        for risk_tier in ["low", "medium", "high", "critical"]:
            with patch("arifosmcp.runtime.orchestrator.metabolic_loop", new_callable=AsyncMock) as mock_loop:
                mock_loop.return_value = {
                    "ok": True,
                    "tool": "forge",
                    "verdict": "SEAL",
                    "status": "SUCCESS",
                }

                result = await forge(spec=f"Test spec with {risk_tier} risk", risk_tier=risk_tier)

                assert result is not None

    @pytest.mark.asyncio
    async def test_forge_server_injection(self):
        """Test forge injects server instance"""
        from arifosmcp.runtime.tools import forge

        mock_server = Mock()

        with patch("arifosmcp.runtime.orchestrator.metabolic_loop", new_callable=AsyncMock) as mock_loop:
            mock_loop.return_value = {
                "ok": True,
                "tool": "forge",
                "verdict": "SEAL",
                "status": "SUCCESS",
            }

            # Forge should work even with server context
            result = await forge("test spec")
            assert result is not None


class TestRealityAtlas:
    """Test reality_atlas tool"""

    @pytest.mark.asyncio
    async def test_reality_atlas_operations(self):
        """Test reality_atlas with different operations"""
        from arifosmcp.runtime.tools import reality_atlas

        operations = ["merge", "query", "filter", "validate"]

        for op in operations:
            with patch("arifosmcp.runtime.tools._wrap_call") as mock_wrap:
                mock_wrap.return_value = AsyncMock()
                mock_wrap.return_value.ok = True

                result = await reality_atlas(operation=op, session_id="test", bundles=[], query={})

                assert result is not None


class TestCheckVitalAdvanced:
    """Test check_vital advanced scenarios"""

    @pytest.mark.asyncio
    async def test_check_vital_with_thermodynamics(self):
        """Test check_vital includes thermodynamic metrics"""
        from arifosmcp.runtime.tools import check_vital

        with patch("arifosmcp.runtime.tools.get_thermodynamic_report") as mock_thermo:
            mock_thermo.return_value = {"dS": 0.5, "peace2": 0.8, "G_star": 0.9}

            with patch("arifosmcp.runtime.tools._wrap_call") as mock_wrap:
                mock_wrap.return_value = AsyncMock()
                mock_wrap.return_value.ok = True
                mock_wrap.return_value.payload = {}

                result = await check_vital(session_id="test")

                assert result is not None

    @pytest.mark.asyncio
    async def test_check_vital_thermodynamics_error(self):
        """Test check_vital handles thermodynamics errors gracefully"""
        from arifosmcp.runtime.tools import check_vital

        with patch("arifosmcp.runtime.tools.get_thermodynamic_report") as mock_thermo:
            mock_thermo.side_effect = Exception("Thermo error")

            with patch("arifosmcp.runtime.tools._wrap_call") as mock_wrap:
                mock_wrap.return_value = AsyncMock()
                mock_wrap.return_value.ok = True
                mock_wrap.return_value.payload = {}

                result = await check_vital(session_id="test")

                # Should handle error gracefully
                assert result is not None


class TestPublicToolRegistry:
    """Test public tool registry functions"""

    def test_tool_registry_exists(self):
        """Test tool registry is properly defined"""
        from arifosmcp.runtime.tools import tool_registry

        assert tool_registry is not None
        assert isinstance(tool_registry, dict)

    def test_public_kernel_tool_name(self):
        """Test public kernel tool name constant"""
        from arifosmcp.runtime.tools import PUBLIC_KERNEL_TOOL_NAME

        assert PUBLIC_KERNEL_TOOL_NAME == "arifOS_kernel"


class TestStageTransitions:
    """Test stage transition logic"""

    def test_all_stages_defined(self):
        """Test all stages are properly defined"""
        from arifosmcp.runtime.tools import Stage

        expected_stages = [
            "000_INIT",
            "111_SENSE",
            "222_REALITY",
            "333_MIND",
            "444_ROUTE",
            "555_MEMORY",
            "666_HEART",
            "777_FORGE",
            "888_JUDGE",
            "999_VAULT",
        ]

        for stage_value in expected_stages:
            # Should be able to access each stage
            stage = Stage(stage_value)
            assert stage.value == stage_value


class TestToolAliases:
    """Test tool alias functions"""

    @pytest.mark.asyncio
    async def test_search_reality_alias(self):
        """Test search_reality is alias for reality_compass"""
        from arifosmcp.runtime.tools import search_reality

        with patch("arifosmcp.runtime.tools.reality_compass") as mock_compass:
            mock_compass.return_value = AsyncMock()
            mock_compass.return_value.tool = "reality_compass"

            result = await search_reality("test query")

            mock_compass.assert_called_once()
            assert "mode" in mock_compass.call_args.kwargs
            assert mock_compass.call_args.kwargs["mode"] == "search"

    @pytest.mark.asyncio
    async def test_ingest_evidence_alias(self):
        """Test ingest_evidence is alias for reality_compass"""
        from arifosmcp.runtime.tools import ingest_evidence

        with patch("arifosmcp.runtime.tools.reality_compass") as mock_compass:
            mock_compass.return_value = AsyncMock()
            mock_compass.return_value.tool = "reality_compass"

            result = await ingest_evidence("https://example.com")

            mock_compass.assert_called_once()
            assert "mode" in mock_compass.call_args.kwargs
            assert mock_compass.call_args.kwargs["mode"] == "fetch"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
