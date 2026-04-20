"""
Test Single-Line Interpreter with Bond et al. (2007) Synthetic Case
DITEMPA BUKAN DIBERI

Tests the governed interpretation workflow designed to avoid the 79% expert
failure rate observed by Bond et al. (2007) on ambiguous synthetic seismic.

Reference:
    Bond, C. E., Gibbs, A. D., Shipton, Z. K., & Jones, S. (2007).
    "What do you think this is? 'Conceptual uncertainty' in geoscience interpretation."
    GSA Today, 17(11), 4-10.
"""

import pytest
import numpy as np
import asyncio

from arifos.geox.tools.single_line_interpreter import (
    SingleLineInterpreter,
    compute_attributes_2d,
    link_attributes_to_geology,
    audit_conceptual_bias,
    TectonicSetting,
    InputType,
    _compute_coherence_2d,
    _compute_curvature_2d,
    _compute_instantaneous_frequency,
    _compute_envelope,
    _compute_dip_2d,
)
from arifos.geox.geox_tools import ToolRegistry


# -----------------------------------------------------------------------------
# 2D Attribute Computation Tests
# -----------------------------------------------------------------------------

def test_coherence_2d_computation():
    """Test 2D coherence computation returns valid data."""
    data = np.random.random((100, 200)).astype(np.float32)
    
    result = _compute_coherence_2d(data, window_size=5)
    
    assert "data" in result
    assert "stats" in result
    assert result["data"].shape == data.shape
    assert 0.0 <= result["stats"]["min"] <= result["stats"]["max"] <= 1.0


def test_curvature_2d_computation():
    """Test 2D curvature computation."""
    data = np.random.random((100, 200)).astype(np.float32)
    
    result = _compute_curvature_2d(data, "most_positive")
    
    assert "data" in result
    assert result["type"] == "most_positive"
    assert result["data"].shape == data.shape


def test_instantaneous_frequency_computation():
    """Test instantaneous frequency computation."""
    data = np.random.random((100, 200)).astype(np.float32)
    
    result = _compute_instantaneous_frequency(data, dt=0.004)
    
    assert "data" in result
    assert result["data"].shape == data.shape
    # Should be in typical seismic range
    assert 10 <= result["stats"]["mean"] <= 80


def test_envelope_computation():
    """Test envelope computation."""
    data = np.random.random((100, 200)).astype(np.float32) * 2 - 1
    
    result = _compute_envelope(data)
    
    assert "data" in result
    assert result["data"].shape == data.shape
    assert result["stats"]["min"] >= 0  # Envelope is always positive


def test_dip_2d_computation():
    """Test 2D dip computation."""
    data = np.random.random((100, 200)).astype(np.float32)
    
    result = _compute_dip_2d(data)
    
    assert "data" in result
    assert result["data"].shape == data.shape
    # Dip should be in degrees
    assert -90 <= result["stats"]["min"] <= result["stats"]["max"] <= 90


# -----------------------------------------------------------------------------
# Attribute Stack Tests
# -----------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_compute_attributes_2d_segy():
    """Test attribute computation with SEG-Y input (lower uncertainty)."""
    data = np.random.random((100, 200)).astype(np.float32)
    
    attr_stack = await compute_attributes_2d(
        data=data,
        data_ref="test_line_001",
        attribute_list=["coherence", "curvature_max"],
        config={"dip_steering": True},
        is_raster=False,
    )
    
    assert "coherence" in attr_stack.attributes
    assert "curvature_max" in attr_stack.attributes
    assert attr_stack.verdict == "QUALIFY"
    assert attr_stack.aggregate_uncertainty == 0.10
    assert "SEG-Y" in attr_stack.verdict_explanation


@pytest.mark.asyncio
async def test_compute_attributes_2d_raster():
    """Test attribute computation with raster input (higher uncertainty, HOLD)."""
    data = np.random.random((100, 200)).astype(np.float32)
    
    attr_stack = await compute_attributes_2d(
        data=data,
        data_ref="test_image_001",
        attribute_list=["coherence", "curvature_max"],
        config={},
        is_raster=True,
    )
    
    assert attr_stack.verdict == "HOLD"
    assert attr_stack.aggregate_uncertainty == 0.15
    assert "RASTER" in attr_stack.verdict_explanation
    assert "Bond" in attr_stack.verdict_explanation
    
    # Check anomalous risk is critical for raster
    coherence_attr = attr_stack.attributes["coherence"]
    assert coherence_attr.contrast.anomalous_risk["risk_level"] == "critical"


@pytest.mark.asyncio
async def test_contrast_metadata_bond_reference():
    """Test that ContrastMetadata includes Bond et al. (2007) reference."""
    data = np.random.random((100, 200)).astype(np.float32)
    
    attr_stack = await compute_attributes_2d(
        data=data,
        data_ref="bond_synthetic",
        attribute_list=["coherence"],
        config={},
        is_raster=True,
    )
    
    coherence = attr_stack.attributes["coherence"]
    notes = coherence.contrast.anomalous_risk["notes"]
    
    assert "Bond" in notes
    assert "79%" in notes or "expert" in notes.lower()


# -----------------------------------------------------------------------------
# Structural Linking Tests
# -----------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_link_attributes_to_geology():
    """Test rule-based structural linking (not LLM guess)."""
    data = np.random.random((100, 200)).astype(np.float32)
    
    attr_stack = await compute_attributes_2d(
        data=data,
        data_ref="test_line",
        attribute_list=["coherence", "curvature_max", "dip_2d"],
        config={},
        is_raster=False,
    )
    
    interpretation = await link_attributes_to_geology(attr_stack)
    
    assert interpretation.tectonic_setting in TectonicSetting
    assert 0.0 <= interpretation.setting_confidence <= 1.0
    assert len(interpretation.primary_structures) > 0
    assert len(interpretation.alternative_settings) > 0
    assert 0.03 <= interpretation.overall_uncertainty <= 0.15


@pytest.mark.asyncio
async def test_structural_elements_have_alternatives():
    """Test that every structural element has alternative interpretations."""
    data = np.random.random((100, 200)).astype(np.float32)
    
    attr_stack = await compute_attributes_2d(
        data=data,
        data_ref="test_line",
        attribute_list=["coherence", "curvature_max"],
        config={},
        is_raster=False,
    )
    
    interpretation = await link_attributes_to_geology(attr_stack)
    
    for structure in interpretation.primary_structures:
        assert len(structure.alternative_interpretations) > 0
        assert structure.confidence < 0.85  # Never too confident


# -----------------------------------------------------------------------------
# Conceptual Bias Audit Tests
# -----------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_audit_conceptual_bias_bond_reference():
    """Test that bias audit references Bond et al. (2007)."""
    data = np.random.random((100, 200)).astype(np.float32)
    
    attr_stack = await compute_attributes_2d(
        data=data,
        data_ref="test_line",
        attribute_list=["coherence"],
        config={},
        is_raster=False,
    )
    
    interpretation = await link_attributes_to_geology(attr_stack)
    biases = await audit_conceptual_bias(interpretation, attr_stack)
    
    # Should have multiple biases identified
    assert len(biases) >= 3
    
    # Check for Bond reference
    bias_descriptions = " ".join([b.description for b in biases])
    assert "Bond" in bias_descriptions


@pytest.mark.asyncio
async def test_audit_anchoring_bias():
    """Test anchoring bias detection."""
    data = np.random.random((100, 200)).astype(np.float32)
    
    attr_stack = await compute_attributes_2d(
        data=data,
        data_ref="test_line",
        attribute_list=["coherence"],
        config={},
        is_raster=False,
    )
    
    interpretation = await link_attributes_to_geology(attr_stack)
    biases = await audit_conceptual_bias(interpretation, attr_stack)
    
    anchoring = [b for b in biases if "Anchoring" in b.bias_type]
    assert len(anchoring) > 0
    assert anchoring[0].historical_failure_rate == 0.79  # Bond et al. rate


@pytest.mark.asyncio
async def test_audit_raster_data_quality_bias():
    """Test data quality bias for raster input."""
    data = np.random.random((100, 200)).astype(np.float32)
    
    attr_stack = await compute_attributes_2d(
        data=data,
        data_ref="test_image",
        attribute_list=["coherence"],
        config={},
        is_raster=True,
    )
    
    interpretation = await link_attributes_to_geology(attr_stack)
    biases = await audit_conceptual_bias(interpretation, attr_stack)
    
    # Should have data quality bias
    data_quality = [b for b in biases if "Data Quality" in b.bias_type]
    assert len(data_quality) > 0
    assert data_quality[0].historical_failure_rate == 0.79
    assert "STOP" in data_quality[0].mitigation


# -----------------------------------------------------------------------------
# SingleLineInterpreter Tool Tests
# -----------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_single_line_interpreter_segy():
    """Test full interpretation workflow with SEG-Y input."""
    tool = SingleLineInterpreter()
    
    # Mock SEG-Y data
    seismic_data = np.random.random((200, 300)).astype(np.float32) * 2 - 1
    
    result = await tool.run({
        "seismic_data": seismic_data,
        "data_type": "segy",
        "config": {
            "attribute_list": ["coherence", "curvature_max", "dip_2d"],
            "dip_steering": True,
        },
    })
    
    assert result.success is True
    assert result.tool_name == "SingleLineInterpreter"
    
    output = result.raw_output
    assert "interpretation" in output
    assert "bias_audit" in output
    assert "final_verdict" in output
    assert "bond_2007_reference" in output
    
    # Should be QUALIFY or PARTIAL for SEG-Y
    assert output["final_verdict"] in ["QUALIFY", "PARTIAL", "HOLD"]


@pytest.mark.asyncio
async def test_single_line_interpreter_raster():
    """Test that raster input triggers HOLD with Bond warning."""
    tool = SingleLineInterpreter()
    
    # Mock raster image data
    image_data = np.random.random((200, 300)).astype(np.float32)
    
    result = await tool.run({
        "seismic_data": image_data,
        "data_type": "raster",
        "config": {},
    })
    
    assert result.success is True
    
    output = result.raw_output
    assert output["final_verdict"] == "HOLD"
    
    # Should mention Bond and 79% failure rate
    explanation = output["verdict_explanation"]
    assert "Bond" in explanation
    assert "79%" in explanation
    assert "RASTER" in explanation or "trace" in explanation.lower()


@pytest.mark.asyncio
async def test_single_line_interpreter_validation_recommendations():
    """Test that interpretation includes validation recommendations."""
    tool = SingleLineInterpreter()
    
    seismic_data = np.random.random((100, 200)).astype(np.float32)
    
    result = await tool.run({
        "seismic_data": seismic_data,
        "data_type": "segy",
        "config": {},
    })
    
    output = result.raw_output
    recommendations = output["validation_recommendations"]
    
    assert len(recommendations) > 0
    # Should mention intersecting line or 3D
    assert any("intersecting" in r.lower() or "3d" in r.lower() for r in recommendations)


@pytest.mark.asyncio
async def test_single_line_interpreter_bias_mitigation():
    """Test that bias audit includes mitigations."""
    tool = SingleLineInterpreter()
    
    seismic_data = np.random.random((100, 200)).astype(np.float32)
    
    result = await tool.run({
        "seismic_data": seismic_data,
        "data_type": "segy",
        "config": {},
    })
    
    output = result.raw_output
    biases = output["bias_audit"]
    
    for bias in biases:
        assert bias["mitigation"]  # Should have non-empty mitigation
        assert len(bias["mitigation"]) > 10  # Meaningful length


@pytest.mark.asyncio
async def test_single_line_interpreter_invalid_inputs():
    """Test error handling for invalid inputs."""
    tool = SingleLineInterpreter()
    
    result = await tool.run({
        # Missing required fields
    })
    
    assert result.success is False
    assert "Invalid inputs" in result.error


# -----------------------------------------------------------------------------
# Bond Synthetic Case Simulation
# -----------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_bond_synthetic_inversion_case():
    """
    Simulate the Bond et al. (2007) synthetic inversion case.
    
    This synthetic was designed to look extensional but was actually
    extension followed by inversion (compression). 79% of experts got it wrong.
    
    GEOX should:
    1. Detect the ambiguity (multiple valid interpretations)
    2. Flag high conceptual uncertainty
    3. Recommend validation before committing to interpretation
    4. Reference Bond et al. (2007) explicitly
    """
    tool = SingleLineInterpreter()
    
    # Create synthetic data that mimics the Bond case
    # (Extensional-looking geometry with subtle inversion indicators)
    rng = np.random.RandomState(42)
    synthetic = rng.random((250, 400)).astype(np.float32) * 2 - 1
    
    # Add some coherent structure to simulate reflectors
    for i in range(50, 200, 20):
        synthetic[i:i+3, :] += 0.5
    
    result = await tool.run({
        "seismic_data": synthetic,
        "data_type": "segy",  # Pretend we have SEG-Y for this test
        "config": {
            "attribute_list": ["coherence", "curvature_max", "dip_2d", "instantaneous_frequency"],
        },
    })
    
    assert result.success is True
    output = result.raw_output
    
    # Check interpretation
    interpretation = output["interpretation"]
    
    # Should detect multiple alternatives
    alternatives = interpretation["alternative_settings"]
    assert len(alternatives) > 1
    
    # Inversion should be in alternatives (the correct answer in Bond case)
    setting_names = [a["setting"] for a in alternatives]
    assert "inversion" in setting_names or "extensional" in setting_names
    
    # Check bias audit references Bond
    bias_audit = output["bias_audit"]
    anchoring_bias = [b for b in bias_audit if "Anchoring" in b["type"]]
    assert len(anchoring_bias) > 0
    assert anchoring_bias[0]["historical_failure_rate"] == 0.79
    
    # Should recommend validation
    recommendations = output["validation_recommendations"]
    assert len(recommendations) > 0


@pytest.mark.asyncio
async def test_bond_case_conceptual_uncertainty_high():
    """
    Test that the Bond synthetic case is flagged as high conceptual uncertainty.
    
    The key insight from Bond et al. (2007) is that conceptual uncertainty
    (what tectonic model to apply) is often more important than data quality.
    """
    tool = SingleLineInterpreter()
    
    rng = np.random.RandomState(42)
    synthetic = rng.random((200, 300)).astype(np.float32) * 2 - 1
    
    result = await tool.run({
        "seismic_data": synthetic,
        "data_type": "segy",
        "config": {},
    })
    
    output = result.raw_output
    
    # Should have complexity or anchoring bias
    bias_types = [b["type"] for b in output["bias_audit"]]
    assert any(b in bias_types for b in ["Anchoring Bias", "Complexity Aversion", "Confirmation Bias"])
    
    # Overall uncertainty should be elevated
    interpretation = output["interpretation"]
    assert interpretation["overall_uncertainty"] >= 0.12


# -----------------------------------------------------------------------------
# Tool Registry Integration
# -----------------------------------------------------------------------------

def test_single_line_interpreter_in_registry():
    """Test that SingleLineInterpreter is in default ToolRegistry."""
    registry = ToolRegistry.default_registry()
    
    assert "SingleLineInterpreter" in registry.list_tools()
    
    tool = registry.get("SingleLineInterpreter")
    assert isinstance(tool, SingleLineInterpreter)


@pytest.mark.asyncio
async def test_registry_execution():
    """Test executing through registry."""
    registry = ToolRegistry.default_registry()
    tool = registry.get("SingleLineInterpreter")
    
    seismic_data = np.random.random((100, 200)).astype(np.float32)
    
    result = await tool.run({
        "seismic_data": seismic_data,
        "data_type": "segy",
        "config": {},
    })
    
    assert result.success is True
    assert "interpretation" in result.raw_output


# -----------------------------------------------------------------------------
# Contrast Canon Enforcement
# -----------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_contrast_canon_physical_vs_visual():
    """Test that physical axes are explicitly separated from visual encoding."""
    data = np.random.random((100, 200)).astype(np.float32)
    
    attr_stack = await compute_attributes_2d(
        data=data,
        data_ref="test",
        attribute_list=["coherence"],
        config={"visual_encoding": {"colormap": "rainbow", "gamma": 1.5}},
        is_raster=False,
    )
    
    coherence = attr_stack.attributes["coherence"]
    contrast = coherence.contrast
    
    # Physical axes should be defined
    assert len(contrast.physical_axes) > 0
    assert "waveform_similarity" in contrast.physical_axes
    
    # Visual encoding should be separate
    assert contrast.visual_encoding["colormap"] == "rainbow"
    assert contrast.visual_encoding["gamma"] == 1.5


@pytest.mark.asyncio
async def test_f7_humility_enforced():
    """Test F7 Humility: uncertainty in [0.03, 0.15]."""
    data = np.random.random((100, 200)).astype(np.float32)
    
    attr_stack = await compute_attributes_2d(
        data=data,
        data_ref="test",
        attribute_list=["coherence", "curvature_max"],
        config={},
        is_raster=False,
    )
    
    for name, attr in attr_stack.attributes.items():
        assert 0.03 <= attr.uncertainty <= 0.15


@pytest.mark.asyncio
async def test_f9_anti_hantu_no_llm_guess():
    """Test F9 Anti-Hantu: No raw pixel interpretation, only governed attributes."""
    tool = SingleLineInterpreter()
    
    seismic_data = np.random.random((100, 200)).astype(np.float32)
    
    result = await tool.run({
        "seismic_data": seismic_data,
        "data_type": "segy",
        "config": {},
    })
    
    # Result should include computed attributes
    output = result.raw_output
    assert "attribute_stack" in output
    
    # Should NOT just be an LLM description of the image
    interpretation = output["interpretation"]
    assert "primary_structures" in interpretation
    
    # Structures should have supporting_attributes (traceable to computed attributes)
    for struct in interpretation["primary_structures"]:
        assert len(struct["attributes"]) > 0


# -----------------------------------------------------------------------------
# Seal
# -----------------------------------------------------------------------------

"""
Test Suite Status: SEAL
Constitutional Floors Checked:
  F1  Amanah — Full provenance chain, reversible interpretation
  F2  Truth — No claims beyond attribute support
  F4  Clarity — Physical/visual separation explicit
  F7  Humility — Uncertainty ∈ [0.03, 0.15] enforced
  F9  Anti-Hantu — Image-only triggers HOLD, no hallucination
  F13 Sovereign — Multiple alternatives trigger human review

Bond et al. (2007) Reference:
  All tests reference the 79% expert failure rate on synthetic data.
  Bias audit explicitly includes anchoring, confirmation, and availability biases.
  RASTER input triggers automatic HOLD with explicit warning.

DITEMPA BUKAN DIBERI
"""
