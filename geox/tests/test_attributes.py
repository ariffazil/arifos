"""
tests/test_attributes.py — Classical Seismic Attribute Tests
DITEMPA BUKAN DIBERI

Validates:
  1. Coherence computation (semblance)
  2. Curvature (4 types: most_positive, most_negative, gaussian, mean)
  3. Spectral decomposition (STFT frequency bands)
  4. RMS amplitude and envelope
  5. compute_attributes orchestrator
  6. SeismicAttributeTool BaseTool integration
  7. Contrast Canon metadata on all outputs
"""

from __future__ import annotations

import numpy as np
import pytest

from arifos.geox.tools.attributes import (
    SeismicAttributeTool,
    compute_attributes,
    compute_coherence,
    compute_curvature,
    compute_envelope,
    compute_rms_amplitude,
    compute_spectral_decomposition,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def synthetic_3d_volume() -> np.ndarray:
    """
    Synthetic 8x8x32 3D seismic volume with:
    - Three horizontal reflectors
    - Gaussian noise
    """
    rng = np.random.RandomState(42)
    ni, nx, ns = 8, 8, 32
    volume = np.zeros((ni, nx, ns), dtype=np.float64)

    # Horizontal reflectors at samples 8, 16, 24
    for s in [8, 16, 24]:
        volume[:, :, max(0, s - 1):min(ns, s + 2)] = 100.0

    volume += rng.normal(0, 10, (ni, nx, ns))
    return volume


@pytest.fixture
def synthetic_2d_slice() -> np.ndarray:
    """16x32 2D seismic section with fault offset."""
    rng = np.random.RandomState(42)
    h, w = 16, 32
    img = np.zeros((h, w), dtype=np.float64)

    # Horizontal layers
    for y in [4, 8, 12]:
        img[max(0, y - 1):min(h, y + 1), :] = 120.0

    # Fault: shift right half down by 2
    img[2:, w // 2:] = img[:-2, w // 2:]
    img[:2, w // 2:] = 0

    img += rng.normal(0, 8, (h, w))
    return img


# ---------------------------------------------------------------------------
# Coherence Tests
# ---------------------------------------------------------------------------

class TestCoherence:
    def test_coherence_shape(self, synthetic_3d_volume):
        result = compute_coherence(synthetic_3d_volume, window_shape=(3, 3, 3))
        assert result.volume.shape == synthetic_3d_volume.shape

    def test_coherence_range(self, synthetic_3d_volume):
        result = compute_coherence(synthetic_3d_volume, window_shape=(3, 3, 3))
        assert result.volume.min() >= 0.0
        assert result.volume.max() <= 1.0

    def test_coherence_metadata(self, synthetic_3d_volume):
        result = compute_coherence(synthetic_3d_volume, window_shape=(3, 3, 3))
        assert result.name == "coherence_semblance"
        assert result.units == "dimensionless"
        assert result.contrast_metadata is not None
        assert result.contrast_metadata.requires_non_visual_confirmation is True
        assert result.contrast_metadata.confidence_class.anomalous_contrast_risk == "low"

    def test_coherence_2d_input(self, synthetic_2d_slice):
        """2D input should be auto-promoted to 3D."""
        result = compute_coherence(synthetic_2d_slice, window_shape=(3, 3, 3))
        assert result.volume.ndim == 3


# ---------------------------------------------------------------------------
# Curvature Tests
# ---------------------------------------------------------------------------

class TestCurvature:
    @pytest.mark.parametrize("curv_type", [
        "most_positive", "most_negative", "gaussian", "mean"
    ])
    def test_curvature_types_2d(self, synthetic_2d_slice, curv_type):
        result = compute_curvature(synthetic_2d_slice, curvature_type=curv_type)
        assert result.volume.shape == synthetic_2d_slice.shape
        assert result.name == f"curvature_{curv_type}"

    @pytest.mark.parametrize("curv_type", [
        "most_positive", "most_negative", "gaussian", "mean"
    ])
    def test_curvature_types_3d(self, synthetic_3d_volume, curv_type):
        result = compute_curvature(synthetic_3d_volume, curvature_type=curv_type)
        assert result.volume.shape == synthetic_3d_volume.shape

    def test_curvature_invalid_type(self, synthetic_2d_slice):
        with pytest.raises(ValueError, match="Unknown curvature_type"):
            compute_curvature(synthetic_2d_slice, curvature_type="invalid")

    def test_curvature_contrast_metadata(self, synthetic_2d_slice):
        result = compute_curvature(synthetic_2d_slice, curvature_type="most_positive")
        assert result.contrast_metadata.physical_proxy.proxy_name == "structural_curvature_most_positive"
        assert result.contrast_metadata.confidence_class.anomalous_contrast_risk == "low"


# ---------------------------------------------------------------------------
# Spectral Decomposition Tests
# ---------------------------------------------------------------------------

class TestSpectralDecomposition:
    def test_spectral_default_bands(self, synthetic_3d_volume):
        results = compute_spectral_decomposition(synthetic_3d_volume, sample_rate_ms=4.0)
        assert len(results) == 5  # 5 default bands
        for r in results:
            assert r.volume.shape == synthetic_3d_volume.shape
            assert "spectral_rms" in r.name
            assert r.contrast_metadata.source_domain.domain == "frequency_content"

    def test_spectral_custom_bands(self, synthetic_3d_volume):
        bands = [(10.0, 30.0), (30.0, 60.0)]
        results = compute_spectral_decomposition(
            synthetic_3d_volume, sample_rate_ms=4.0, freq_bands_hz=bands
        )
        assert len(results) == 2

    def test_spectral_2d_input(self, synthetic_2d_slice):
        results = compute_spectral_decomposition(synthetic_2d_slice, sample_rate_ms=4.0)
        assert len(results) > 0

    def test_spectral_contrast_risk(self, synthetic_3d_volume):
        results = compute_spectral_decomposition(synthetic_3d_volume)
        for r in results:
            assert r.contrast_metadata.confidence_class.anomalous_contrast_risk == "medium"


# ---------------------------------------------------------------------------
# Amplitude Tests
# ---------------------------------------------------------------------------

class TestAmplitude:
    def test_rms_amplitude_shape(self, synthetic_3d_volume):
        result = compute_rms_amplitude(synthetic_3d_volume, window_samples=5)
        # squeeze removes leading dimension if was promoted
        assert result.volume.shape == synthetic_3d_volume.shape

    def test_rms_amplitude_positive(self, synthetic_3d_volume):
        result = compute_rms_amplitude(synthetic_3d_volume)
        assert (result.volume >= 0).all()

    def test_envelope_shape(self, synthetic_3d_volume):
        result = compute_envelope(synthetic_3d_volume)
        assert result.volume.shape == synthetic_3d_volume.shape

    def test_envelope_positive(self, synthetic_3d_volume):
        result = compute_envelope(synthetic_3d_volume)
        assert (result.volume >= 0).all()

    def test_envelope_metadata(self, synthetic_3d_volume):
        result = compute_envelope(synthetic_3d_volume)
        assert result.equation_reference.startswith("Taner")
        assert result.contrast_metadata.confidence_class.anomalous_contrast_risk == "low"


# ---------------------------------------------------------------------------
# Orchestrator Tests
# ---------------------------------------------------------------------------

class TestComputeAttributes:
    def test_single_attribute(self, synthetic_2d_slice):
        stack = compute_attributes(synthetic_2d_slice, ["envelope"])
        assert "envelope" in stack.names
        assert len(stack.attributes) == 1

    def test_multiple_attributes(self, synthetic_2d_slice):
        stack = compute_attributes(
            synthetic_2d_slice,
            ["curvature_most_positive", "curvature_most_negative", "rms_amplitude"],
        )
        assert len(stack.attributes) == 3
        assert "curvature_most_positive" in stack.names

    def test_governance_summary(self, synthetic_2d_slice):
        stack = compute_attributes(
            synthetic_2d_slice,
            ["envelope", "curvature_mean"],
        )
        summary = stack.governance_summary
        assert "envelope" in summary
        assert "curvature_mean" in summary
        # All should be unverified (no non-visual confirmation provided)
        for status in summary.values():
            assert status == "unverified"

    def test_checksum_populated(self, synthetic_2d_slice):
        stack = compute_attributes(synthetic_2d_slice, ["envelope"])
        assert len(stack.source_volume_checksum) == 16

    def test_unknown_attribute_skipped(self, synthetic_2d_slice):
        stack = compute_attributes(synthetic_2d_slice, ["nonexistent_attr"])
        assert len(stack.attributes) == 0


# ---------------------------------------------------------------------------
# BaseTool Integration Tests
# ---------------------------------------------------------------------------

class TestSeismicAttributeTool:
    @pytest.fixture
    def tool(self) -> SeismicAttributeTool:
        return SeismicAttributeTool()

    def test_tool_properties(self, tool):
        assert tool.name == "SeismicAttributeTool"
        assert "Contrast Canon" in tool.description
        assert tool.health_check() is True

    @pytest.mark.asyncio
    async def test_run_single(self, tool, synthetic_2d_slice):
        result = await tool.run({
            "volume": synthetic_2d_slice,
            "attributes": ["envelope"],
        })
        assert result.success is True
        assert result.tool_name == "SeismicAttributeTool"
        assert len(result.quantities) >= 2  # mean + std
        assert result.metadata["contrast_canon_enforced"] is True

    @pytest.mark.asyncio
    async def test_run_multiple(self, tool, synthetic_2d_slice):
        result = await tool.run({
            "volume": synthetic_2d_slice,
            "attributes": ["curvature_most_positive", "rms_amplitude"],
        })
        assert result.success is True
        assert len(result.metadata["attributes_computed"]) == 2

    @pytest.mark.asyncio
    async def test_invalid_inputs(self, tool):
        result = await tool.run({})
        assert result.success is False

    @pytest.mark.asyncio
    async def test_governance_in_output(self, tool, synthetic_2d_slice):
        result = await tool.run({
            "volume": synthetic_2d_slice,
            "attributes": ["envelope"],
        })
        assert "governance_summary" in result.raw_output
        assert result.raw_output["contrast_canon_enforced"] is True
