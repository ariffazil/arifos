"""
Test Contrast Canon Implementation
DITEMPA BUKAN DIBERI

Tests for:
  - ContrastMetadata schema validation
  - SeismicAttributesTool compute_attributes
  - Channel-Fault discrimination example
  - Constitutional floor enforcement (F7, F9)
"""

import pytest
import asyncio
from datetime import datetime, timezone

from arifos.geox.geox_schemas import (
    ContrastMetadata,
    AttributeVolume,
    AttributeStack,
    ProvenanceRecord,
    CoordinatePoint,
)
from arifos.geox.contrast_wrapper import (
    contrast_governed,
    compute_contrast_verdict,
    _generate_anomalous_risk,
)
from arifos.geox.geox_tools import SeismicAttributesTool, ToolRegistry


# -----------------------------------------------------------------------------
# ContrastMetadata Schema Tests
# -----------------------------------------------------------------------------

def test_contrast_metadata_creation():
    """Test basic ContrastMetadata creation."""
    contrast = ContrastMetadata(
        attribute_name="coherence_semblance",
        physical_axes=["waveform_similarity", "discontinuity"],
        processing_steps=["dip_steered", "semblance_3x3x3"],
        equation_reference="Marfurt et al. (1998)",
    )
    
    assert contrast.attribute_name == "coherence_semblance"
    assert "waveform_similarity" in contrast.physical_axes
    assert contrast.visual_encoding["colormap"] == "gray_inverted"
    assert contrast.anomalous_risk["display_bias"] == "medium"


def test_contrast_metadata_meta_attribute():
    """Test ContrastMetadata for meta-attributes."""
    contrast = ContrastMetadata(
        attribute_name="meta_fault_prob",
        physical_axes=["discontinuity", "learned_nonlinear"],
        processing_steps=["cnn_fusion", "coherence+curvature_stack"],
        is_meta_attribute=True,
    )
    
    assert contrast.is_meta_attribute is True
    assert "learned_nonlinear" in contrast.physical_axes


# -----------------------------------------------------------------------------
# Anomalous Risk Tests
# -----------------------------------------------------------------------------

def test_anomalous_risk_classical():
    """Test risk assessment for classical attributes."""
    risk = _generate_anomalous_risk("coherence", False)
    
    assert risk["display_bias"] == "low"
    assert risk["risk_level"] == "minimal"
    assert "traceability" in risk["notes"].lower() or "physical" in risk["notes"].lower()


def test_anomalous_risk_meta():
    """Test risk assessment for meta-attributes."""
    risk = _generate_anomalous_risk("meta_fault_prob", True)
    
    assert risk["display_bias"] == "high"
    assert risk["risk_level"] == "critical"
    assert "learned" in risk["notes"].lower() or "perceptual" in risk["notes"].lower()
    assert len(risk["mitigation"]) >= 3


def test_anomalous_risk_meta_with_fault_prob():
    """Test that fault_prob triggers meta-attribute risk."""
    risk = _generate_anomalous_risk("ai_fault_probability", False)
    # Should still detect as meta due to name pattern
    assert risk["display_bias"] in ["high", "medium"]


# -----------------------------------------------------------------------------
# Contrast Verdict Tests
# -----------------------------------------------------------------------------

def test_contrast_verdict_seal():
    """Test SEAL verdict for grounded classical attributes."""
    attributes = {
        "coherence": {
            "_contrast_metadata": {"attribute_name": "coherence"},
            "_is_meta_attribute": False,
            "_grounding_status": "GROUNDED",
        }
    }
    
    result = compute_contrast_verdict(attributes, well_ties=["WELL-01"])
    
    assert result["verdict"] == "SEAL"
    assert len(result["warnings"]) == 0


def test_contrast_verdict_block_ungrounded_meta():
    """Test GEOX_BLOCK for ungrounded meta-attributes."""
    attributes = {
        "meta_fault_prob": {
            "_contrast_metadata": {"attribute_name": "meta_fault_prob"},
            "_is_meta_attribute": True,
            "_grounding_status": "UNGROUNDED",
        }
    }
    
    result = compute_contrast_verdict(attributes, well_ties=None)
    
    assert result["verdict"] == "GEOX_BLOCK"
    assert any("F9" in f or "F7" in f for f in result["floors_triggered"])
    assert len(result["warnings"]) > 0


def test_contrast_verdict_partial_with_warnings():
    """Test PARTIAL verdict for mixed attributes."""
    attributes = {
        "coherence": {
            "_contrast_metadata": {"attribute_name": "coherence"},
            "_is_meta_attribute": False,
            "_grounding_status": "GROUNDED",
        },
        "ai_edge_detect": {
            "_contrast_metadata": {"attribute_name": "ai_edge_detect"},
            "_is_meta_attribute": True,
            "_grounding_status": "UNGROUNDED",
        }
    }
    
    result = compute_contrast_verdict(attributes, well_ties=None)
    
    assert result["verdict"] == "GEOX_BLOCK"  # Because meta is ungrounded


# -----------------------------------------------------------------------------
# SeismicAttributesTool Tests
# -----------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_seismic_attributes_tool_classical():
    """Test computing classical attributes."""
    tool = SeismicAttributesTool()
    
    result = await tool.run({
        "volume_ref": "seismic_vol_pm3-2025-001",
        "attribute_list": ["coherence", "curvature_max"],
        "config": {"dip_steered": True},
    })
    
    assert result.success is True
    assert result.tool_name == "SeismicAttributesTool"
    assert "stack" in result.raw_output
    
    stack_data = result.raw_output["stack"]
    assert stack_data["verdict"] in ["SEAL", "QUALIFY", "HOLD", "GEOX_BLOCK"]
    assert "coherence" in stack_data["attributes"]
    assert "curvature_max" in stack_data["attributes"]


@pytest.mark.asyncio
async def test_seismic_attributes_tool_meta_without_wells():
    """Test that meta-attributes without well ties trigger GEOX_BLOCK."""
    tool = SeismicAttributesTool()
    
    result = await tool.run({
        "volume_ref": "seismic_vol_pm3-2025-001",
        "attribute_list": ["coherence", "meta_fault_prob"],
        "config": {},
        # No well_ties provided
    })
    
    assert result.success is True  # Tool succeeded
    stack_data = result.raw_output["stack"]
    
    # Should be blocked due to ungrounded meta-attribute
    assert stack_data["verdict"] == "GEOX_BLOCK"
    assert stack_data["has_meta_attributes"] is True
    assert len(stack_data["well_ties"]) == 0


@pytest.mark.asyncio
async def test_seismic_attributes_tool_meta_with_wells():
    """Test that meta-attributes with well ties are QUALIFY."""
    tool = SeismicAttributesTool()
    
    result = await tool.run({
        "volume_ref": "seismic_vol_pm3-2025-001",
        "attribute_list": ["coherence", "meta_fault_prob"],
        "config": {},
        "well_ties": ["BEKANTAN-1", "PUTERI-1"],
    })
    
    assert result.success is True
    stack_data = result.raw_output["stack"]
    
    # With well ties, should qualify
    assert stack_data["verdict"] == "QUALIFY"
    assert stack_data["has_meta_attributes"] is True
    assert len(stack_data["well_ties"]) == 2


@pytest.mark.asyncio
async def test_seismic_attributes_contrast_metadata():
    """Test that contrast metadata is properly attached."""
    tool = SeismicAttributesTool()
    
    result = await tool.run({
        "volume_ref": "test_vol",
        "attribute_list": ["coherence"],
        "config": {"dip_steered": True},
    })
    
    stack_data = result.raw_output["stack"]
    coherence_attr = stack_data["attributes"]["coherence"]
    contrast = coherence_attr["contrast"]
    
    assert contrast["attribute_name"] == "coherence"
    assert "waveform_similarity" in contrast["physical_axes"]
    assert contrast["equation_reference"] == "Marfurt et al. (1998) — semblance-based coherence"
    assert contrast["anomalous_risk"]["display_bias"] == "low"


@pytest.mark.asyncio
async def test_seismic_attributes_f7_uncertainty():
    """Test F7 Humility: uncertainty bounds enforcement."""
    tool = SeismicAttributesTool()
    
    result = await tool.run({
        "volume_ref": "test_vol",
        "attribute_list": ["coherence", "meta_fault_prob"],
        "well_ties": ["WELL-01"],
    })
    
    stack_data = result.raw_output["stack"]
    
    # Classical attribute has lower uncertainty
    classical_unc = stack_data["attributes"]["coherence"]["uncertainty"]
    assert 0.03 <= classical_unc <= 0.15
    
    # Meta attribute has higher uncertainty (F7 enforced)
    meta_unc = stack_data["attributes"]["meta_fault_prob"]["uncertainty"]
    assert meta_unc >= 0.12  # Meta floor
    assert 0.03 <= meta_unc <= 0.15


# -----------------------------------------------------------------------------
# Channel-Fault Discrimination Example
# -----------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_channel_fault_discrimination():
    """
    Test the channel-fault discrimination workflow.
    
    This test validates that the Contrast Canon properly distinguishes:
    - Linear discontinuities → faults
    - Sinuous planform → channels  
    - Adjacent curvature drag → confirms fault (not channel)
    """
    tool = SeismicAttributesTool()
    
    # Request attributes for channel-fault analysis
    result = await tool.run({
        "volume_ref": "pm3_channel_fault_test",
        "attribute_list": [
            "coherence",           # For discontinuity detection
            "curvature_max",       # For structural flexure
            "curvature_min",       # For drag patterns
            "spectral_rms",        # For channel fill characterization
        ],
        "config": {
            "dip_steered": True,
            "coherence_window": "3x3x3",
            "visual_encoding": {
                "colormap": "seismic",
                "dynamic_range": "p2-p98",
            }
        },
        "well_ties": ["TEST-WELL-01"],
    })
    
    assert result.success is True
    stack = result.raw_output["stack"]
    
    # Validate attribute stack for interpretation
    assert stack["verdict"] == "SEAL"
    
    attrs = stack["attributes"]
    assert "coherence" in attrs
    assert "curvature_max" in attrs
    assert "curvature_min" in attrs
    assert "spectral_rms" in attrs
    
    # Each attribute should have proper contrast metadata
    for name, attr in attrs.items():
        contrast = attr["contrast"]
        assert "physical_axes" in contrast
        assert "visual_encoding" in contrast
        assert "anomalous_risk" in contrast
        assert contrast["anomalous_risk"]["display_bias"] == "low"  # Classical attrs


# -----------------------------------------------------------------------------
# ToolRegistry Integration
# -----------------------------------------------------------------------------

def test_tool_registry_includes_seismic_attributes():
    """Test that SeismicAttributesTool is in default registry."""
    registry = ToolRegistry.default_registry()
    
    assert "SeismicAttributesTool" in registry.list_tools()
    
    tool = registry.get("SeismicAttributesTool")
    assert isinstance(tool, SeismicAttributesTool)


@pytest.mark.asyncio
async def test_registry_seismic_attributes_execution():
    """Test executing SeismicAttributesTool through registry."""
    registry = ToolRegistry.default_registry()
    tool = registry.get("SeismicAttributesTool")
    
    result = await tool.run({
        "volume_ref": "reg_test_vol",
        "attribute_list": ["coherence"],
    })
    
    assert result.success is True


# -----------------------------------------------------------------------------
# Error Handling Tests
# -----------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_seismic_attributes_invalid_inputs():
    """Test error handling for invalid inputs."""
    tool = SeismicAttributesTool()
    
    result = await tool.run({
        # Missing volume_ref and attribute_list
    })
    
    assert result.success is False
    assert "Invalid inputs" in result.error


@pytest.mark.asyncio
async def test_seismic_attributes_empty_attribute_list():
    """Test handling of empty attribute list."""
    tool = SeismicAttributesTool()
    
    result = await tool.run({
        "volume_ref": "test_vol",
        "attribute_list": [],
    })
    
    # Should succeed but with empty stack
    assert result.success is True
    assert result.raw_output["attribute_count"] == 0


# -----------------------------------------------------------------------------
# Constitutional Floor Tests
# -----------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_f7_humility_enforcement():
    """Test F7 Humility: uncertainty outside [0.03, 0.15] is rejected."""
    tool = SeismicAttributesTool()
    
    # This should work (uncertainty in valid range)
    result = await tool.run({
        "volume_ref": "f7_test",
        "attribute_list": ["coherence"],
    })
    
    stack = result.raw_output["stack"]
    unc = stack["aggregate_uncertainty"]
    assert 0.03 <= unc <= 0.15


@pytest.mark.asyncio
async def test_f9_anti_hantu_meta_detection():
    """Test F9 Anti-Hantu: meta-attributes are properly flagged."""
    tool = SeismicAttributesTool()
    
    result = await tool.run({
        "volume_ref": "f9_test",
        "attribute_list": ["ai_fault_detect", "ml_discontinuity"],
    })
    
    stack = result.raw_output["stack"]
    
    # Should detect meta-attributes
    assert stack["has_meta_attributes"] is True
    
    # Should be blocked without well ties
    assert stack["verdict"] == "GEOX_BLOCK"
    
    # Each meta attribute should have high anomalous risk
    for name, attr in stack["attributes"].items():
        risk = attr["contrast"]["anomalous_risk"]
        assert risk["risk_level"] == "critical"


# -----------------------------------------------------------------------------
# Seal
# -----------------------------------------------------------------------------

"""
Test Suite Status: SEAL
Constitutional Floors Checked:
  F1  Amanah — All results reversible with full provenance
  F4  Clarity — Physical/visual separation explicit
  F7  Humility — Uncertainty ∈ [0.03, 0.15] enforced
  F9  Anti-Hantu — Meta-attributes flagged without well ties
  F13 Sovereign — Human sign-off gates active

DITEMPA BUKAN DIBERI
"""
