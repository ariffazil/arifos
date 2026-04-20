"""
tests/test_contrast_metadata.py — Contrast Canon Schema Tests
DITEMPA BUKAN DIBERI

Validates:
  1. ContrastMetadata construction and field population
  2. Contrast Canon validators (processing chain order, unknown domain)
  3. ConfidenceClass constraints (interpretation ≤ signal)
  4. Factory helpers for filter and meta-attribute outputs
  5. Governance properties (amplification, confirmation status, governance_status)
  6. Constitutional compliance: F2 (truth), F4 (clarity), F9 (anti-hantu)
"""

from __future__ import annotations

import pytest

from arifos.geox.tools.contrast_metadata import (
    ConfidenceClass,
    ContrastMetadata,
    ContrastSourceDomain,
    PhysicalProxy,
    VisualTransform,
    create_filter_contrast_metadata,
    create_meta_attribute_contrast_metadata,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def valid_source_domain() -> ContrastSourceDomain:
    return ContrastSourceDomain(
        domain="reflectivity",
        measurement_units="fraction",
        acquisition_type="seismic_3d",
        vertical_resolution_m=15.0,
        lateral_resolution_m=25.0,
    )


@pytest.fixture
def valid_transform() -> VisualTransform:
    return VisualTransform(
        transform_type="gaussian_filter",
        parameters={"kernel_size": 5, "sigma": 1.4},
        order_index=0,
        reversible=False,
        contrast_amplification_factor=1.2,
        notes="Gaussian smoothing for noise reduction.",
    )


@pytest.fixture
def valid_proxy() -> PhysicalProxy:
    return PhysicalProxy(
        proxy_name="structural_discontinuity",
        proxy_type="qualitative_indicator",
        physical_range=(0.0, 1.0),
        physical_units="fraction",
    )


@pytest.fixture
def valid_confidence() -> ConfidenceClass:
    return ConfidenceClass(
        signal_confidence=0.65,
        interpretation_confidence=0.40,
        anomalous_contrast_risk="medium",
        risk_factors=["single_attribute_only"],
    )


@pytest.fixture
def valid_contrast_metadata(
    valid_source_domain, valid_transform, valid_proxy, valid_confidence
) -> ContrastMetadata:
    return ContrastMetadata(
        source_domain=valid_source_domain,
        processing_chain=[valid_transform],
        physical_proxy=valid_proxy,
        confidence_class=valid_confidence,
        requires_non_visual_confirmation=True,
    )


# ---------------------------------------------------------------------------
# Unit Tests: Schema Construction
# ---------------------------------------------------------------------------

class TestContrastSourceDomain:
    def test_valid_construction(self, valid_source_domain):
        assert valid_source_domain.domain == "reflectivity"
        assert valid_source_domain.measurement_units == "fraction"
        assert valid_source_domain.acquisition_type == "seismic_3d"

    def test_unknown_domain_allowed(self):
        d = ContrastSourceDomain(
            domain="unknown",
            measurement_units="n/a",
            acquisition_type="computed",
        )
        assert d.domain == "unknown"


class TestVisualTransform:
    def test_valid_construction(self, valid_transform):
        assert valid_transform.transform_type == "gaussian_filter"
        assert valid_transform.order_index == 0
        assert valid_transform.contrast_amplification_factor == 1.2

    def test_default_amplification(self):
        t = VisualTransform(
            transform_type="colormap",
            parameters={},
            order_index=0,
        )
        assert t.contrast_amplification_factor == 1.0


class TestPhysicalProxy:
    def test_valid_construction(self, valid_proxy):
        assert valid_proxy.proxy_name == "structural_discontinuity"
        assert valid_proxy.proxy_type == "qualitative_indicator"

    def test_speculative_proxy(self):
        p = PhysicalProxy(
            proxy_name="hidden_channel_edge",
            proxy_type="speculative",
        )
        assert p.proxy_type == "speculative"
        assert p.calibration_source is None


class TestConfidenceClass:
    def test_valid_construction(self, valid_confidence):
        assert valid_confidence.signal_confidence == 0.65
        assert valid_confidence.interpretation_confidence == 0.40
        assert valid_confidence.anomalous_contrast_risk == "medium"

    def test_interpretation_cannot_exceed_signal(self):
        """Interpretation confidence must be ≤ signal confidence."""
        with pytest.raises(ValueError, match="cannot exceed signal_confidence"):
            ConfidenceClass(
                signal_confidence=0.40,
                interpretation_confidence=0.60,  # VIOLATION
                anomalous_contrast_risk="medium",
            )

    def test_equal_confidences_allowed(self):
        c = ConfidenceClass(
            signal_confidence=0.50,
            interpretation_confidence=0.50,
            anomalous_contrast_risk="low",
        )
        assert c.interpretation_confidence == c.signal_confidence


# ---------------------------------------------------------------------------
# Unit Tests: ContrastMetadata Core
# ---------------------------------------------------------------------------

class TestContrastMetadata:
    def test_valid_construction(self, valid_contrast_metadata):
        assert valid_contrast_metadata.source_domain.domain == "reflectivity"
        assert len(valid_contrast_metadata.processing_chain) == 1
        assert valid_contrast_metadata.requires_non_visual_confirmation is True
        assert valid_contrast_metadata.contrast_id.startswith("CC-")

    def test_processing_chain_must_be_ordered(
        self, valid_source_domain, valid_proxy, valid_confidence
    ):
        """Processing chain order_index must be sequential."""
        with pytest.raises(ValueError, match="ordered by order_index"):
            ContrastMetadata(
                source_domain=valid_source_domain,
                processing_chain=[
                    VisualTransform(
                        transform_type="gaussian_filter",
                        parameters={},
                        order_index=2,  # Out of order
                    ),
                    VisualTransform(
                        transform_type="clahe",
                        parameters={},
                        order_index=0,  # Should be first
                    ),
                ],
                physical_proxy=valid_proxy,
                confidence_class=valid_confidence,
            )

    def test_unknown_domain_caps_signal_confidence(self, valid_proxy):
        """F9: unknown source domain forces signal_confidence ≤ 0.5."""
        with pytest.raises(ValueError, match="signal_confidence"):
            ContrastMetadata(
                source_domain=ContrastSourceDomain(
                    domain="unknown",
                    measurement_units="n/a",
                    acquisition_type="computed",
                ),
                processing_chain=[],
                physical_proxy=valid_proxy,
                confidence_class=ConfidenceClass(
                    signal_confidence=0.80,  # Too high for unknown source
                    interpretation_confidence=0.30,
                    anomalous_contrast_risk="high",
                ),
            )

    def test_unknown_domain_with_low_confidence_allowed(self, valid_proxy):
        """Unknown domain is fine if confidence is properly capped."""
        cm = ContrastMetadata(
            source_domain=ContrastSourceDomain(
                domain="unknown",
                measurement_units="n/a",
                acquisition_type="computed",
            ),
            processing_chain=[],
            physical_proxy=valid_proxy,
            confidence_class=ConfidenceClass(
                signal_confidence=0.40,
                interpretation_confidence=0.20,
                anomalous_contrast_risk="high",
            ),
        )
        assert cm.source_domain.domain == "unknown"


# ---------------------------------------------------------------------------
# Unit Tests: Governance Properties
# ---------------------------------------------------------------------------

class TestGovernanceProperties:
    def test_total_contrast_amplification(self, valid_source_domain, valid_proxy):
        """Product of all amplification factors in chain."""
        cm = ContrastMetadata(
            source_domain=valid_source_domain,
            processing_chain=[
                VisualTransform(
                    transform_type="gaussian_filter",
                    parameters={},
                    order_index=0,
                    contrast_amplification_factor=1.5,
                ),
                VisualTransform(
                    transform_type="clahe",
                    parameters={},
                    order_index=1,
                    contrast_amplification_factor=2.0,
                ),
            ],
            physical_proxy=valid_proxy,
            confidence_class=ConfidenceClass(
                signal_confidence=0.60,
                interpretation_confidence=0.35,
                anomalous_contrast_risk="medium",
            ),
        )
        assert cm.total_contrast_amplification == pytest.approx(3.0)

    def test_is_confirmed_false_by_default(self, valid_contrast_metadata):
        assert valid_contrast_metadata.is_confirmed is False

    def test_is_confirmed_with_sources(self, valid_contrast_metadata):
        valid_contrast_metadata.confirmed_by = ["well_PM3_001"]
        assert valid_contrast_metadata.is_confirmed is True

    def test_governance_status_unverified(self, valid_contrast_metadata):
        assert valid_contrast_metadata.governance_status == "unverified"

    def test_governance_status_confirmed(self, valid_contrast_metadata):
        valid_contrast_metadata.confirmed_by = ["core_analysis_2024"]
        assert valid_contrast_metadata.governance_status == "confirmed"

    def test_governance_status_high_risk(self, valid_source_domain, valid_proxy):
        cm = ContrastMetadata(
            source_domain=valid_source_domain,
            processing_chain=[],
            physical_proxy=valid_proxy,
            confidence_class=ConfidenceClass(
                signal_confidence=0.50,
                interpretation_confidence=0.25,
                anomalous_contrast_risk="critical",
            ),
        )
        assert cm.governance_status == "high_risk"

    def test_governance_status_suspicious_amplification(
        self, valid_source_domain, valid_proxy
    ):
        """Amplification > 10x triggers 'suspicious' status."""
        cm = ContrastMetadata(
            source_domain=valid_source_domain,
            processing_chain=[
                VisualTransform(
                    transform_type="clahe",
                    parameters={},
                    order_index=0,
                    contrast_amplification_factor=12.0,
                ),
            ],
            physical_proxy=valid_proxy,
            confidence_class=ConfidenceClass(
                signal_confidence=0.50,
                interpretation_confidence=0.30,
                anomalous_contrast_risk="medium",
            ),
        )
        assert cm.governance_status == "suspicious"


# ---------------------------------------------------------------------------
# Unit Tests: Factory Helpers
# ---------------------------------------------------------------------------

class TestFactoryHelpers:
    def test_create_filter_contrast_metadata(self):
        cm = create_filter_contrast_metadata(
            filter_type="gaussian",
            filter_params={"kernel_size": 5, "sigma": 1.4},
        )
        assert cm.source_domain.domain == "reflectivity"
        assert cm.requires_non_visual_confirmation is True
        assert cm.created_by == "SeismicVisualFilterTool"
        assert cm.confidence_class.anomalous_contrast_risk == "low"
        assert len(cm.processing_chain) == 1

    def test_create_filter_sobel_medium_risk(self):
        cm = create_filter_contrast_metadata(
            filter_type="sobel",
            filter_params={"operator": "3x3"},
        )
        assert cm.confidence_class.anomalous_contrast_risk == "medium"

    def test_create_meta_attribute_contrast_metadata(self):
        cm = create_meta_attribute_contrast_metadata(
            attribute_name="fault_probability",
            input_attributes=["coherence", "curvature_max", "dip"],
            method="cnn_segmentation",
            proxy_name="fault_likelihood",
        )
        assert cm.confidence_class.anomalous_contrast_risk == "high"
        assert cm.requires_non_visual_confirmation is True
        assert "multi_attribute_fusion" in cm.confidence_class.risk_factors
        # Processing chain: 3 input attributes + 1 fusion step
        assert len(cm.processing_chain) == 4

    def test_meta_attribute_pca_lower_risk(self):
        cm = create_meta_attribute_contrast_metadata(
            attribute_name="texture_volume",
            input_attributes=["coherence", "curvature"],
            method="pca",
            proxy_name="seismic_texture",
        )
        assert cm.confidence_class.anomalous_contrast_risk == "medium"
