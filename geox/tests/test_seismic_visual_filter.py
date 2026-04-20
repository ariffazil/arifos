"""
tests/test_seismic_visual_filter.py — SeismicVisualFilterTool Test Suite
DITEMPA BUKAN DIBERI

Validates:
  1. All five filter families execute without error
  2. Filter stack generation and comparison ranking
  3. Visual hypothesis emission with perception bridge disclaimers
  4. SeismicVisualFilterTool BaseTool integration (single + all modes)
  5. Constitutional compliance: F7 uncertainty ≥ 0.15, Contract 2 active
  6. Input validation and error handling
"""

from __future__ import annotations

import numpy as np
import pytest

from arifos.geox.geox_schemas import CoordinatePoint
from arifos.geox.tools.seismic_visual_filter import (
    FilterResult,
    SeismicVisualFilterTool,
    _compute_contrast,
    _compute_edge_density,
    _image_checksum,
    apply_filter,
    compare_filter_response,
    emit_visual_hypothesis,
    generate_filter_stack,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def synthetic_seismic_slice() -> np.ndarray:
    """
    Create a synthetic 64x64 seismic slice with:
    - Horizontal reflectors (sine waves at different depths)
    - A diagonal fault (offset discontinuity)
    - Random noise
    """
    h, w = 64, 64
    image = np.zeros((h, w), dtype=np.float64)

    # Horizontal reflectors
    for y in range(h):
        image[y, :] += 80 * np.sin(2 * np.pi * y / 16)
        image[y, :] += 40 * np.sin(2 * np.pi * y / 8)

    # Diagonal fault: shift right half down by 5 pixels
    fault_x = w // 2
    shifted = image.copy()
    shifted[5:, fault_x:] = image[:-5, fault_x:]
    shifted[:5, fault_x:] = 0
    image = shifted

    # Add noise
    rng = np.random.RandomState(42)
    image += rng.normal(0, 15, (h, w))

    # Normalize to [0, 255]
    image = ((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8)
    return image


@pytest.fixture
def small_slice() -> np.ndarray:
    """Tiny 8x8 test image for fast filter tests."""
    rng = np.random.RandomState(99)
    return rng.randint(0, 256, (8, 8), dtype=np.uint8)


# ---------------------------------------------------------------------------
# Unit Tests: Filter Functions
# ---------------------------------------------------------------------------

class TestFilterFunctions:
    """Test individual filter implementations."""

    def test_gaussian_filter(self, synthetic_seismic_slice: np.ndarray):
        result = apply_filter(synthetic_seismic_slice, "gaussian")
        assert isinstance(result, FilterResult)
        assert result.filter_type == "gaussian"
        assert result.output_array.shape == synthetic_seismic_slice.shape
        assert result.metric_contrast > 0
        assert result.processing_time_ms > 0

    def test_mean_filter(self, synthetic_seismic_slice: np.ndarray):
        result = apply_filter(synthetic_seismic_slice, "mean")
        assert result.filter_type == "mean"
        assert result.output_array.shape == synthetic_seismic_slice.shape

    def test_kuwahara_filter(self, small_slice: np.ndarray):
        """Kuwahara on small image (expensive on large)."""
        result = apply_filter(small_slice, "kuwahara")
        assert result.filter_type == "kuwahara"
        assert result.output_array.shape == small_slice.shape
        assert "edge-preserving" in result.notes.lower()

    def test_sobel_filter(self, synthetic_seismic_slice: np.ndarray):
        result = apply_filter(synthetic_seismic_slice, "sobel")
        assert result.filter_type == "sobel"
        assert result.output_array.shape == synthetic_seismic_slice.shape
        assert result.metric_edge_density >= 0.0

    def test_canny_filter(self, small_slice: np.ndarray):
        """Canny on small image for speed."""
        result = apply_filter(small_slice, "canny")
        assert result.filter_type == "canny"
        assert result.output_array.shape == small_slice.shape
        # Canny output should be binary-ish (0 or 255)
        unique_vals = np.unique(result.output_array)
        assert all(v in [0, 255] for v in unique_vals)

    def test_clahe_filter(self, synthetic_seismic_slice: np.ndarray):
        result = apply_filter(synthetic_seismic_slice, "clahe")
        assert result.filter_type == "clahe"
        assert result.output_array.shape == synthetic_seismic_slice.shape

    def test_invalid_filter_type(self, synthetic_seismic_slice: np.ndarray):
        with pytest.raises(ValueError):
            apply_filter(synthetic_seismic_slice, "invalid_filter")

    def test_gaussian_custom_params(self, small_slice: np.ndarray):
        result = apply_filter(small_slice, "gaussian", {"kernel_size": 3, "sigma": 0.8})
        assert result.params["kernel_size"] == 3
        assert result.params["sigma"] == 0.8


# ---------------------------------------------------------------------------
# Unit Tests: Stack & Comparison
# ---------------------------------------------------------------------------

class TestFilterStack:
    """Test filter stack generation and comparison."""

    def test_generate_filter_stack(self, small_slice: np.ndarray):
        stack = generate_filter_stack(small_slice)
        # Should have all 6 filter types
        assert len(stack) == 6
        filter_types = {r.filter_type for r in stack}
        assert filter_types == {"gaussian", "mean", "kuwahara", "sobel", "canny", "clahe"}

    def test_compare_filter_response(self, small_slice: np.ndarray):
        stack = generate_filter_stack(small_slice)
        comparison = compare_filter_response(stack)

        assert "ranking" in comparison
        assert "best_filter" in comparison
        assert "best_score" in comparison
        assert "disclaimer" in comparison
        assert len(comparison["ranking"]) == 6

        # Best score should be highest composite
        scores = [r["composite_score"] for r in comparison["ranking"]]
        assert scores == sorted(scores, reverse=True)

    def test_compare_empty_stack(self):
        comparison = compare_filter_response([])
        assert "error" in comparison

    def test_disclaimer_present(self, small_slice: np.ndarray):
        stack = generate_filter_stack(small_slice)
        comparison = compare_filter_response(stack)
        assert "VISUAL ENHANCEMENT ONLY" in comparison["disclaimer"]
        assert "RGB ≠ truth" in comparison["disclaimer"]


# ---------------------------------------------------------------------------
# Unit Tests: Visual Hypothesis
# ---------------------------------------------------------------------------

class TestVisualHypothesis:
    """Test hypothesis emission with Contract 2 compliance."""

    def test_emit_hypothesis(self, small_slice: np.ndarray):
        stack = generate_filter_stack(small_slice)
        comparison = compare_filter_response(stack)
        hypothesis = emit_visual_hypothesis(comparison, "/data/seismic_001.npy")

        # Contract 2: Must carry perception bridge warning
        assert hypothesis["uncertainty"] >= 0.15
        assert hypothesis["status"] == "unverified"
        assert "CONTRACT 2 ACTIVE" in hypothesis["perception_bridge_warning"]
        assert hypothesis["pipeline_stage"] == "222_REFLECT"
        assert hypothesis["seal"] == "DITEMPA BUKAN DIBERI"

    def test_hypothesis_requires_confirmation(self, small_slice: np.ndarray):
        stack = generate_filter_stack(small_slice)
        comparison = compare_filter_response(stack)
        hypothesis = emit_visual_hypothesis(comparison)

        assert len(hypothesis["requires_confirmation_by"]) > 0
        assert "EarthModelTool" in hypothesis["requires_confirmation_by"]


# ---------------------------------------------------------------------------
# Unit Tests: Utility Functions
# ---------------------------------------------------------------------------

class TestUtilities:
    """Test metric and utility functions."""

    def test_compute_contrast(self):
        # Uniform image → 0 contrast
        uniform = np.ones((10, 10), dtype=np.float64) * 128
        assert _compute_contrast(uniform) == 0.0

        # High-contrast image → positive contrast
        checkerboard = np.zeros((10, 10), dtype=np.float64)
        checkerboard[::2, ::2] = 255
        checkerboard[1::2, 1::2] = 255
        assert _compute_contrast(checkerboard) > 0.0

    def test_compute_edge_density(self):
        # Zero image → 0 edge density
        zeros = np.zeros((10, 10), dtype=np.float64)
        assert _compute_edge_density(zeros) == 0.0

    def test_image_checksum_deterministic(self):
        img = np.array([[1, 2], [3, 4]], dtype=np.uint8)
        c1 = _image_checksum(img)
        c2 = _image_checksum(img)
        assert c1 == c2
        assert len(c1) == 16  # 16-char hex prefix


# ---------------------------------------------------------------------------
# Integration Tests: SeismicVisualFilterTool (BaseTool)
# ---------------------------------------------------------------------------

class TestSeismicVisualFilterTool:
    """Full BaseTool integration tests."""

    @pytest.fixture
    def tool(self) -> SeismicVisualFilterTool:
        return SeismicVisualFilterTool()

    def test_tool_properties(self, tool: SeismicVisualFilterTool):
        assert tool.name == "SeismicVisualFilterTool"
        assert "Plane 2" in tool.description
        assert "RGB ≠ truth" in tool.description
        assert tool.health_check() is True

    @pytest.mark.asyncio
    async def test_single_filter(self, tool: SeismicVisualFilterTool, small_slice: np.ndarray):
        """Test single filter execution through BaseTool interface."""
        result = await tool.run({
            "image_array": small_slice,
            "image_path": "<test>",
            "filter_type": "gaussian",
        })

        assert result.success is True
        assert result.tool_name == "SeismicVisualFilterTool"
        assert len(result.quantities) > 0
        assert result.latency_ms > 0

        # F7 Perception Bridge: all uncertainties must be ≥ 0.15
        for q in result.quantities:
            assert q.uncertainty >= 0.15, f"F7 violation: {q.quantity_type} uncertainty={q.uncertainty}"

        # Contract 2: perception_only must be flagged
        assert result.metadata["perception_only"] is True
        assert result.metadata["contract_2_active"] is True
        assert "perception_bridge_warning" in result.raw_output

    @pytest.mark.asyncio
    async def test_all_filters(self, tool: SeismicVisualFilterTool, small_slice: np.ndarray):
        """Test 'all' mode — applies all filter families."""
        result = await tool.run({
            "image_array": small_slice,
            "image_path": "<test>",
            "filter_type": "all",
        })

        assert result.success is True
        # 6 filters × 2 metrics (contrast + edge_density) + 1 composite = 13
        assert len(result.quantities) >= 13

        # Hypothesis should be in raw_output
        assert "hypothesis" in result.raw_output
        assert result.raw_output["hypothesis"]["status"] == "unverified"

        # All filters applied
        assert len(result.metadata["filters_applied"]) == 6

    @pytest.mark.asyncio
    async def test_invalid_inputs(self, tool: SeismicVisualFilterTool):
        """Test input validation rejection."""
        result = await tool.run({})
        assert result.success is False
        assert result.error is not None

        result = await tool.run({"image_path": "x", "filter_type": "nonexistent"})
        assert result.success is False

    @pytest.mark.asyncio
    async def test_with_location(self, tool: SeismicVisualFilterTool, small_slice: np.ndarray):
        """Test with explicit geographic anchor."""
        result = await tool.run({
            "image_array": small_slice,
            "image_path": "<test>",
            "filter_type": "sobel",
            "location": CoordinatePoint(latitude=5.2, longitude=104.8),
        })

        assert result.success is True
        for q in result.quantities:
            assert q.coordinates.latitude == 5.2
            assert q.coordinates.longitude == 104.8

    @pytest.mark.asyncio
    async def test_checksum_in_provenance(self, tool: SeismicVisualFilterTool, small_slice: np.ndarray):
        """F1 Amanah: image checksum must appear in metadata."""
        result = await tool.run({
            "image_array": small_slice,
            "image_path": "<test>",
            "filter_type": "mean",
        })

        assert result.success is True
        assert "image_checksum" in result.metadata
        assert len(result.metadata["image_checksum"]) == 16
        assert result.raw_output["image_checksum_sha256"] == result.metadata["image_checksum"]


# ---------------------------------------------------------------------------
# Constitutional Compliance Tests
# ---------------------------------------------------------------------------

class TestConstitutionalCompliance:
    """Verify arifOS Constitutional Floor enforcement."""

    @pytest.mark.asyncio
    async def test_f7_humility_perception_floor(self, small_slice: np.ndarray):
        """F7: All perception outputs must have uncertainty ≥ 0.15."""
        tool = SeismicVisualFilterTool()
        result = await tool.run({
            "image_array": small_slice,
            "image_path": "<test>",
            "filter_type": "all",
        })

        for q in result.quantities:
            assert q.uncertainty >= 0.15, (
                f"F7 VIOLATION: {q.quantity_type} has uncertainty={q.uncertainty} < 0.15"
            )

    @pytest.mark.asyncio
    async def test_f9_anti_hantu_no_geological_claims(self, small_slice: np.ndarray):
        """F9: Outputs must NOT claim geological truth from visual data alone."""
        tool = SeismicVisualFilterTool()
        result = await tool.run({
            "image_array": small_slice,
            "image_path": "<test>",
            "filter_type": "all",
        })

        # Check that hypothesis status is "unverified"
        hypothesis = result.raw_output.get("hypothesis", {})
        assert hypothesis.get("status") == "unverified"

        # Check quantity types are labelled as "visual_*"
        for q in result.quantities:
            assert q.quantity_type.startswith("visual_"), (
                f"F9 VIOLATION: {q.quantity_type} must be prefixed with 'visual_'"
            )

    @pytest.mark.asyncio
    async def test_contract_2_perception_bridge(self, small_slice: np.ndarray):
        """Contract 2: Perception Bridge — non-visual confirmation required."""
        tool = SeismicVisualFilterTool()
        result = await tool.run({
            "image_array": small_slice,
            "image_path": "<test>",
            "filter_type": "sobel",
        })

        assert result.metadata["multisensor_required"] is True
        assert "CONTRACT 2 ACTIVE" in result.raw_output["perception_bridge_warning"]

        hypothesis = result.raw_output["hypothesis"]
        assert "EarthModelTool" in hypothesis["requires_confirmation_by"]
