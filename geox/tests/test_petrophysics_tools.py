"""
test_petrophysics_tools.py — Tests for GEOX Petrophysics Phase B Tools
═══════════════════════════════════════════════════════════════════════════════
DITEMPA BUKAN DIBERI

Tests for 4 MCP petrophysics tools:
- geox_select_sw_model
- geox_compute_petrophysics
- geox_validate_cutoffs
- geox_petrophysical_hold_check

36 tests total: 9 per tool (4 tools × 9 = 36)
"""

from __future__ import annotations

import pytest
import asyncio
from typing import Any

# Import the server module
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from geox_mcp_server import (
    geox_select_sw_model,
    geox_compute_petrophysics,
    geox_validate_cutoffs,
    geox_petrophysical_hold_check,
    IS_FASTMCP_3,
)


# ═══════════════════════════════════════════════════════════════════════════════
# Helper to extract structured content from result
# ═══════════════════════════════════════════════════════════════════════════════

def get_structured_content(result):
    """Extract structured_content from ToolResult or dict."""
    if hasattr(result, 'structured_content'):
        # FastMCP 3.x - ToolResult object
        return result.structured_content
    else:
        # FastMCP 2.x - dict
        return result.get('structured_content', result)


def get_content(result):
    """Extract content string from ToolResult or dict."""
    if hasattr(result, 'content'):
        # FastMCP 3.x - ToolResult object
        if isinstance(result.content, list) and len(result.content) > 0:
            # TextContent object
            return result.content[0].text
        return str(result.content)
    else:
        # FastMCP 2.x - dict
        return result.get('content', '')


# ═══════════════════════════════════════════════════════════════════════════════
# Test Fixtures
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def sample_interval_uri() -> str:
    return "geox://well/WELL-001/interval/1500.0-1600.0/rock-state"


@pytest.fixture
def uncalibrated_interval_uri() -> str:
    return "geox://well/WELL-uncalibrated/interval/1500.0-1600.0/rock-state-uncalibrated"


# ═══════════════════════════════════════════════════════════════════════════════
# geox_select_sw_model Tests (9 tests)
# ═══════════════════════════════════════════════════════════════════════════════

class TestSelectSwModel:
    """Tests for geox_select_sw_model tool."""
    
    async def _call(self, **kwargs) -> dict:
        """Helper to call the tool."""
        return await geox_select_sw_model(**kwargs)
    
    @pytest.mark.asyncio
    async def test_basic_call(self, sample_interval_uri: str):
        """Test basic successful call with defaults."""
        result = await self._call(interval_uri=sample_interval_uri)
        structured = get_structured_content(result)
        assert "admissible_models" in structured
    
    @pytest.mark.asyncio
    async def test_with_candidate_models(self, sample_interval_uri: str):
        """Test with explicit candidate models."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            candidate_models=["archie", "simandoux"]
        )
        structured = get_structured_content(result)
        assert "admissible_models" in structured
    
    @pytest.mark.asyncio
    async def test_returns_admissible_models(self, sample_interval_uri: str):
        """Test that admissible models are returned."""
        result = await self._call(interval_uri=sample_interval_uri)
        structured = get_structured_content(result)
        admissible = structured["admissible_models"]
        assert isinstance(admissible, list)
        if admissible:
            assert "model" in admissible[0]
            assert "confidence" in admissible[0]
    
    @pytest.mark.asyncio
    async def test_returns_rejected_models(self, sample_interval_uri: str):
        """Test that rejected models are returned with reasons."""
        result = await self._call(interval_uri=sample_interval_uri)
        structured = get_structured_content(result)
        rejected = structured["rejected_models"]
        assert isinstance(rejected, list)
    
    @pytest.mark.asyncio
    async def test_recommended_model_present(self, sample_interval_uri: str):
        """Test that recommended model is present."""
        result = await self._call(interval_uri=sample_interval_uri)
        structured = get_structured_content(result)
        recommended = structured["recommended_model"]
        # Can be a model name or None
        assert recommended is None or isinstance(recommended, str)
    
    @pytest.mark.asyncio
    async def test_floor_check_f4_clarity(self, sample_interval_uri: str):
        """Test F4 Clarity floor check is present."""
        result = await self._call(interval_uri=sample_interval_uri)
        structured = get_structured_content(result)
        floor_check = structured["floor_check"]
        assert floor_check["F4_clarity"] is True
    
    @pytest.mark.asyncio
    async def test_floor_check_f7_humility(self, sample_interval_uri: str):
        """Test F7 Humility floor check is present."""
        result = await self._call(interval_uri=sample_interval_uri)
        structured = get_structured_content(result)
        floor_check = structured["floor_check"]
        assert "F7_humility" in floor_check
    
    @pytest.mark.asyncio
    async def test_timestamp_present(self, sample_interval_uri: str):
        """Test timestamp is included in response."""
        result = await self._call(interval_uri=sample_interval_uri)
        structured = get_structured_content(result)
        assert "timestamp" in structured
    
    @pytest.mark.asyncio
    async def test_content_is_string(self, sample_interval_uri: str):
        """Test content field is a string."""
        result = await self._call(interval_uri=sample_interval_uri)
        content = get_content(result)
        assert isinstance(content, str)
        assert len(content) > 0


# ═══════════════════════════════════════════════════════════════════════════════
# geox_compute_petrophysics Tests (9 tests)
# ═══════════════════════════════════════════════════════════════════════════════

class TestComputePetrophysics:
    """Tests for geox_compute_petrophysics tool."""
    
    async def _call(self, **kwargs) -> dict:
        """Helper to call the tool."""
        return await geox_compute_petrophysics(**kwargs)
    
    @pytest.mark.asyncio
    async def test_basic_computation(self, sample_interval_uri: str):
        """Test basic computation with required params."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            model_id="archie"
        )
        structured = get_structured_content(result)
        assert structured["verdict"] == "COMPUTED"
    
    @pytest.mark.asyncio
    async def test_with_model_params(self, sample_interval_uri: str):
        """Test computation with custom model parameters."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            model_id="archie",
            model_params={"a": 0.62, "m": 2.15, "n": 2.0, "rw": 0.15}
        )
        structured = get_structured_content(result)
        assert structured["verdict"] == "COMPUTED"
    
    @pytest.mark.asyncio
    async def test_uncertainty_enabled(self, sample_interval_uri: str):
        """Test computation with uncertainty enabled."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            model_id="archie",
            compute_uncertainty=True
        )
        structured = get_structured_content(result)
        assert structured["compute_uncertainty"] is True
    
    @pytest.mark.asyncio
    async def test_uncertainty_disabled(self, sample_interval_uri: str):
        """Test computation with uncertainty disabled."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            model_id="archie",
            compute_uncertainty=False
        )
        structured = get_structured_content(result)
        assert structured["compute_uncertainty"] is False
    
    @pytest.mark.asyncio
    async def test_results_structure(self, sample_interval_uri: str):
        """Test that results have expected structure."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            model_id="archie"
        )
        structured = get_structured_content(result)
        results = structured["results"]
        expected_keys = ["vsh_range", "phi_t_range", "phi_e_range", "sw_range", "bvw_range"]
        for key in expected_keys:
            assert key in results
    
    @pytest.mark.asyncio
    async def test_floor_check_f4_clarity(self, sample_interval_uri: str):
        """Test F4 Clarity floor check."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            model_id="archie"
        )
        structured = get_structured_content(result)
        floor_check = structured["floor_check"]
        assert floor_check["F4_clarity"] is True
    
    @pytest.mark.asyncio
    async def test_floor_check_f7_humility_with_uncertainty(self, sample_interval_uri: str):
        """Test F7 Humility when uncertainty is enabled."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            model_id="archie",
            compute_uncertainty=True
        )
        structured = get_structured_content(result)
        floor_check = structured["floor_check"]
        assert floor_check["F7_humility"] is True
    
    @pytest.mark.asyncio
    async def test_model_id_recorded(self, sample_interval_uri: str):
        """Test that model_id is recorded in response."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            model_id="simandoux"
        )
        structured = get_structured_content(result)
        assert structured["model_used"] == "simandoux"
    
    @pytest.mark.asyncio
    async def test_content_is_string(self, sample_interval_uri: str):
        """Test content field is a string."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            model_id="archie"
        )
        content = get_content(result)
        assert isinstance(content, str)


# ═══════════════════════════════════════════════════════════════════════════════
# geox_validate_cutoffs Tests (9 tests)
# ═══════════════════════════════════════════════════════════════════════════════

class TestValidateCutoffs:
    """Tests for geox_validate_cutoffs tool."""
    
    async def _call(self, **kwargs) -> dict:
        """Helper to call the tool."""
        return await geox_validate_cutoffs(**kwargs)
    
    @pytest.mark.asyncio
    async def test_basic_validation(self, sample_interval_uri: str):
        """Test basic cutoff validation."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            cutoff_policy_id="POLICY-001"
        )
        structured = get_structured_content(result)
        assert structured["status"] == "VALIDATED"
    
    @pytest.mark.asyncio
    async def test_interval_uri_recorded(self, sample_interval_uri: str):
        """Test interval_uri is recorded."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            cutoff_policy_id="POLICY-001"
        )
        structured = get_structured_content(result)
        assert structured["interval_uri"] == sample_interval_uri
    
    @pytest.mark.asyncio
    async def test_policy_id_recorded(self, sample_interval_uri: str):
        """Test policy_id is recorded."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            cutoff_policy_id="POLICY-SPECIAL"
        )
        structured = get_structured_content(result)
        assert structured["policy_id"] == "POLICY-SPECIAL"
    
    @pytest.mark.asyncio
    async def test_net_pay_flags_present(self, sample_interval_uri: str):
        """Test net/pay flags are present."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            cutoff_policy_id="POLICY-001"
        )
        structured = get_structured_content(result)
        flags = structured["net_pay_flags"]
        assert "net_thickness_m" in flags
        assert "pay_thickness_m" in flags
        assert "net_to_gross" in flags
    
    @pytest.mark.asyncio
    async def test_cutoffs_applied_present(self, sample_interval_uri: str):
        """Test applied cutoffs are present."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            cutoff_policy_id="POLICY-001"
        )
        structured = get_structured_content(result)
        cutoffs = structured["cutoffs_applied"]
        assert "vsh_max" in cutoffs
        assert "phi_min" in cutoffs
        assert "sw_max" in cutoffs
    
    @pytest.mark.asyncio
    async def test_floor_check_f4_clarity(self, sample_interval_uri: str):
        """Test F4 Clarity floor check."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            cutoff_policy_id="POLICY-001"
        )
        structured = get_structured_content(result)
        floor_check = structured["floor_check"]
        assert floor_check["F4_clarity"] is True
    
    @pytest.mark.asyncio
    async def test_floor_check_f11_authority(self, sample_interval_uri: str):
        """Test F11 Authority floor check."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            cutoff_policy_id="POLICY-001"
        )
        structured = get_structured_content(result)
        floor_check = structured["floor_check"]
        assert floor_check["F11_authority"] is True
    
    @pytest.mark.asyncio
    async def test_timestamp_present(self, sample_interval_uri: str):
        """Test timestamp is included."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            cutoff_policy_id="POLICY-001"
        )
        structured = get_structured_content(result)
        assert "timestamp" in structured
    
    @pytest.mark.asyncio
    async def test_content_is_string(self, sample_interval_uri: str):
        """Test content field is a string."""
        result = await self._call(
            interval_uri=sample_interval_uri,
            cutoff_policy_id="POLICY-001"
        )
        content = get_content(result)
        assert isinstance(content, str)


# ═══════════════════════════════════════════════════════════════════════════════
# geox_petrophysical_hold_check Tests (9 tests)
# ═══════════════════════════════════════════════════════════════════════════════

class TestPetrophysicalHoldCheck:
    """Tests for geox_petrophysical_hold_check tool."""
    
    async def _call(self, **kwargs) -> dict:
        """Helper to call the tool."""
        return await geox_petrophysical_hold_check(**kwargs)
    
    @pytest.mark.asyncio
    async def test_basic_check(self, sample_interval_uri: str):
        """Test basic hold check."""
        result = await self._call(interval_uri=sample_interval_uri)
        structured = get_structured_content(result)
        assert structured["status"] == "SUCCESS"
        assert "verdict" in structured
    
    @pytest.mark.asyncio
    async def test_verdict_is_string(self, sample_interval_uri: str):
        """Test verdict is a string value."""
        result = await self._call(interval_uri=sample_interval_uri)
        structured = get_structured_content(result)
        verdict = structured["verdict"]
        assert isinstance(verdict, str)
        assert verdict in ["SEAL", "QUALIFY", "888_HOLD"]
    
    @pytest.mark.asyncio
    async def test_triggers_is_list(self, sample_interval_uri: str):
        """Test triggers is a list."""
        result = await self._call(interval_uri=sample_interval_uri)
        structured = get_structured_content(result)
        triggers = structured["triggers"]
        assert isinstance(triggers, list)
    
    @pytest.mark.asyncio
    async def test_required_actions_is_list(self, sample_interval_uri: str):
        """Test required_actions is a list."""
        result = await self._call(interval_uri=sample_interval_uri)
        structured = get_structured_content(result)
        actions = structured["required_actions"]
        assert isinstance(actions, list)
    
    @pytest.mark.asyncio
    async def test_can_override_boolean(self, sample_interval_uri: str):
        """Test can_override is a boolean."""
        result = await self._call(interval_uri=sample_interval_uri)
        structured = get_structured_content(result)
        can_override = structured["can_override"]
        assert isinstance(can_override, bool)
    
    @pytest.mark.asyncio
    async def test_uncalibrated_triggers_hold(self, uncalibrated_interval_uri: str):
        """Test that uncalibrated data triggers 888_HOLD."""
        result = await self._call(interval_uri=uncalibrated_interval_uri)
        structured = get_structured_content(result)
        assert structured["verdict"] == "888_HOLD"
        assert "Rw_uncalibrated" in structured["triggers"]
    
    @pytest.mark.asyncio
    async def test_override_authority_for_hold(self, uncalibrated_interval_uri: str):
        """Test override authority is set when on hold."""
        result = await self._call(interval_uri=uncalibrated_interval_uri)
        structured = get_structured_content(result)
        if structured["verdict"] == "888_HOLD":
            assert structured["override_authority"] == "F13_SOVEREIGN"
    
    @pytest.mark.asyncio
    async def test_floor_check_f1_amanah(self, sample_interval_uri: str):
        """Test F1 Amanah floor check."""
        result = await self._call(interval_uri=sample_interval_uri)
        structured = get_structured_content(result)
        floor_check = structured["floor_check"]
        assert floor_check["F1_amanah"] is True
    
    @pytest.mark.asyncio
    async def test_content_is_string(self, sample_interval_uri: str):
        """Test content field is a string."""
        result = await self._call(interval_uri=sample_interval_uri)
        content = get_content(result)
        assert isinstance(content, str)


# ═══════════════════════════════════════════════════════════════════════════════
# Integration Tests (Optional)
# ═══════════════════════════════════════════════════════════════════════════════

class TestPetrophysicsWorkflow:
    """Integration tests for petrophysics workflow."""
    
    @pytest.mark.asyncio
    async def test_full_workflow(self, sample_interval_uri: str):
        """Test the full petrophysics workflow."""
        # Step 1: Select saturation model
        sw_result = await geox_select_sw_model(interval_uri=sample_interval_uri)
        sw_structured = get_structured_content(sw_result)
        assert "admissible_models" in sw_structured
        recommended_model = sw_structured["recommended_model"]
        
        # Step 2: Compute petrophysics with recommended model
        if recommended_model:
            comp_result = await geox_compute_petrophysics(
                interval_uri=sample_interval_uri,
                model_id=recommended_model
            )
            comp_structured = get_structured_content(comp_result)
            assert comp_structured["verdict"] == "COMPUTED"
        
        # Step 3: Validate cutoffs
        cutoff_result = await geox_validate_cutoffs(
            interval_uri=sample_interval_uri,
            cutoff_policy_id="POLICY-001"
        )
        cutoff_structured = get_structured_content(cutoff_result)
        assert cutoff_structured["status"] == "VALIDATED"
        
        # Step 4: Hold check
        hold_result = await geox_petrophysical_hold_check(interval_uri=sample_interval_uri)
        hold_structured = get_structured_content(hold_result)
        assert hold_structured["status"] == "SUCCESS"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
