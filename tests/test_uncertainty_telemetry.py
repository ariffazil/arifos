"""
Tests for core/uncertainty_engine.py and core/telemetry.py.

Covers: UncertaintyVector, UncertaintyEngine, TelemetryStore, log_telemetry.
"""

from __future__ import annotations

import os
import tempfile

import pytest


# =============================================================================
# UNCERTAINTY ENGINE
# =============================================================================


class TestUncertaintyVector:
    def test_default_values(self):
        from core.uncertainty_engine import UncertaintyVector

        v = UncertaintyVector()
        assert v.grounding == 0.0
        assert v.reasoning == 0.0
        assert v.epistemic == 0.0
        assert v.aleatoric == 0.0
        assert v.model_confidence == 0.0

    def test_to_dict(self):
        from core.uncertainty_engine import UncertaintyVector

        v = UncertaintyVector(grounding=0.2, reasoning=0.3, epistemic=0.1)
        d = v.to_dict()
        assert d["grounding"] == 0.2
        assert d["reasoning"] == 0.3
        assert d["epistemic"] == 0.1

    def test_weights_sum_to_one(self):
        from core.uncertainty_engine import UncertaintyVector

        total = sum(UncertaintyVector.WEIGHTS.values())
        assert abs(total - 1.0) < 0.01


class TestOmniscienceLock:
    def test_high_confidence_raises(self):
        from core.uncertainty_engine import check_omniscience_lock, OmniscienceError

        with pytest.raises(OmniscienceError):
            check_omniscience_lock(1.0, is_mathematical=False)

    def test_high_confidence_math_ok(self):
        from core.uncertainty_engine import check_omniscience_lock

        # Should not raise for mathematical claims
        check_omniscience_lock(1.0, is_mathematical=True)

    def test_normal_confidence_ok(self):
        from core.uncertainty_engine import check_omniscience_lock

        check_omniscience_lock(0.95, is_mathematical=False)


class TestHumilityBand:
    def test_below_min_clamped(self):
        from core.uncertainty_engine import enforce_humility_band, HUMILITY_MIN

        result = enforce_humility_band(0.0)
        assert result == HUMILITY_MIN

    def test_in_band_unchanged(self):
        from core.uncertainty_engine import enforce_humility_band

        result = enforce_humility_band(0.04)
        assert result == 0.04

    def test_above_max_but_below_critical(self):
        from core.uncertainty_engine import enforce_humility_band

        result = enforce_humility_band(0.06)
        assert result == 0.06  # Returned as-is (above max but below critical)

    def test_critical_raises(self):
        from core.uncertainty_engine import enforce_humility_band, HumilityBandViolation

        with pytest.raises(HumilityBandViolation):
            enforce_humility_band(0.09)


class TestUncertaintyEngine:
    def setup_method(self):
        from core.uncertainty_engine import UncertaintyEngine

        self.engine = UncertaintyEngine()

    def test_harmonic_mean_returns_float(self):
        from core.uncertainty_engine import UncertaintyVector

        v = UncertaintyVector(
            grounding=0.3, reasoning=0.2, epistemic=0.1, aleatoric=0.1, model_confidence=0.1
        )
        result = self.engine.harmonic_mean(v)
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_harmonic_mean_boosts_high_uncertainty(self):
        from core.uncertainty_engine import UncertaintyVector

        # High grounding uncertainty should be boosted
        v_high = UncertaintyVector(
            grounding=0.8, reasoning=0.1, epistemic=0.1, aleatoric=0.1, model_confidence=0.1
        )
        v_low = UncertaintyVector(
            grounding=0.2, reasoning=0.1, epistemic=0.1, aleatoric=0.1, model_confidence=0.1
        )
        assert self.engine.harmonic_mean(v_high) > self.engine.harmonic_mean(v_low)

    def test_geometric_mean_returns_float(self):
        from core.uncertainty_engine import UncertaintyVector

        v = UncertaintyVector(
            grounding=0.3, reasoning=0.3, epistemic=0.3, aleatoric=0.3, model_confidence=0.3
        )
        result = self.engine.geometric_mean(v)
        assert isinstance(result, float)

    def test_arithmetic_mean_returns_float(self):
        from core.uncertainty_engine import UncertaintyVector

        v = UncertaintyVector(
            grounding=0.4, reasoning=0.3, epistemic=0.2, aleatoric=0.1, model_confidence=0.1
        )
        result = self.engine.arithmetic_mean(v)
        assert isinstance(result, float)
        assert 0.0 <= result <= 1.0

    def test_calculate_returns_dict(self):
        from core.uncertainty_engine import UncertaintyVector

        v = UncertaintyVector(
            grounding=0.04, reasoning=0.04, epistemic=0.04, aleatoric=0.04, model_confidence=0.04
        )
        result = self.engine.calculate(v)
        assert "safety_omega" in result
        assert "display_omega" in result
        assert "recommendation" in result

    def test_calculate_low_uncertainty_proceed(self):
        from core.uncertainty_engine import UncertaintyVector

        # Very low uncertainty → clamped to HUMILITY_MIN (0.03) by band enforcement
        # so minimum possible recommendation is PROCEED_WITH_CAUTION
        v = UncertaintyVector(
            grounding=0.01, reasoning=0.01, epistemic=0.01, aleatoric=0.01, model_confidence=0.01
        )
        result = self.engine.calculate(v)
        assert result["recommendation"] in ("PROCEED", "PROCEED_WITH_CAUTION")

    def test_calculate_high_uncertainty_void(self):
        from core.uncertainty_engine import UncertaintyVector

        # Very high uncertainty → VOID or HumilityBandViolation caught
        v = UncertaintyVector(
            grounding=0.9, reasoning=0.9, epistemic=0.9, aleatoric=0.9, model_confidence=0.9
        )
        result = self.engine.calculate(v)
        assert "recommendation" in result
        # Either VOID_ACTION_REQUIRED from band violation or from threshold
        assert result["recommendation"] in (
            "VOID_ACTION_REQUIRED",
            "HUMAN_REVIEW_RECOMMENDED",
            "PROCEED_WITH_CAUTION",
        )

    def test_from_evidence_creates_vector(self):
        from core.uncertainty_engine import UncertaintyVector

        v = self.engine.from_evidence(
            evidence_count=5,
            evidence_relevance=0.9,
            reasoning_consistency=0.8,
            knowledge_gaps=["gap1"],
            model_logits_confidence=0.85,
        )
        assert isinstance(v, UncertaintyVector)
        assert 0.0 <= v.grounding <= 1.0
        assert 0.0 <= v.reasoning <= 1.0

    def test_from_evidence_no_evidence_high_uncertainty(self):
        v = self.engine.from_evidence()  # Defaults: zero evidence
        # No evidence → high grounding uncertainty
        assert v.grounding > 0.5

    def test_recommendation_proceed(self):
        assert self.engine._recommendation(0.02) == "PROCEED"

    def test_recommendation_proceed_with_caution(self):
        assert self.engine._recommendation(0.04) == "PROCEED_WITH_CAUTION"

    def test_recommendation_human_review(self):
        assert self.engine._recommendation(0.06) == "HUMAN_REVIEW_RECOMMENDED"

    def test_recommendation_void(self):
        assert self.engine._recommendation(0.10) == "VOID_ACTION_REQUIRED"


class TestCalculateUncertainty:
    def test_returns_dict(self):
        from core.uncertainty_engine import calculate_uncertainty

        result = calculate_uncertainty(
            evidence_count=3,
            evidence_relevance=0.8,
            reasoning_consistency=0.7,
            knowledge_gaps=["gap1"],
            model_logits_confidence=0.9,
        )
        assert isinstance(result, dict)
        assert "safety_omega" in result
        assert "components" in result

    def test_no_args(self):
        from core.uncertainty_engine import calculate_uncertainty

        result = calculate_uncertainty()
        assert isinstance(result, dict)


# =============================================================================
# TELEMETRY
# =============================================================================


class TestConstitutionalTelemetry:
    def test_creation(self):
        from core.telemetry import ConstitutionalTelemetry

        t = ConstitutionalTelemetry(session_id="sess-1")
        assert t.session_id == "sess-1"
        assert t.omega_0 == 0.0
        assert t.drift_score == 0.0

    def test_timestamp_set(self):
        from core.telemetry import ConstitutionalTelemetry

        t = ConstitutionalTelemetry(session_id="sess-2")
        assert isinstance(t.timestamp, str)
        assert len(t.timestamp) > 10


class TestTelemetryStore:
    def setup_method(self):
        import tempfile
        from core.telemetry import TelemetryStore

        self.tmpdir = tempfile.mkdtemp()
        self.store = TelemetryStore(storage_path=self.tmpdir)

    def teardown_method(self):
        import shutil

        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_first_date_none_initially(self):
        import tempfile
        from core.telemetry import TelemetryStore

        # Fresh store with empty dir
        d = tempfile.mkdtemp()
        store = TelemetryStore(storage_path=d)
        import shutil

        shutil.rmtree(d, ignore_errors=True)
        assert store.first_telemetry_date is None

    def test_log_creates_file(self):
        from core.telemetry import ConstitutionalTelemetry

        t = ConstitutionalTelemetry(session_id="test-sess")
        self.store.log(t)
        # After logging, first date should be set
        assert self.store.first_telemetry_date is not None
        # A daily file should exist
        daily_files = [f for f in os.listdir(self.tmpdir) if f.startswith("telemetry-")]
        assert len(daily_files) >= 1

    def test_log_second_time_keeps_first_date(self):
        from core.telemetry import ConstitutionalTelemetry

        t1 = ConstitutionalTelemetry(session_id="s1")
        self.store.log(t1)
        first_date = self.store.first_telemetry_date
        t2 = ConstitutionalTelemetry(session_id="s2")
        self.store.log(t2)
        assert self.store.first_telemetry_date == first_date

    def test_get_telemetry_days_zero_before_log(self):
        assert self.store.get_telemetry_days() == 0

    def test_get_telemetry_days_after_log(self):
        from core.telemetry import ConstitutionalTelemetry

        t = ConstitutionalTelemetry(session_id="s")
        self.store.log(t)
        days = self.store.get_telemetry_days()
        assert days >= 0

    def test_can_adapt_new_store(self):
        result = self.store.can_adapt()
        assert isinstance(result, dict)
        assert "can_adapt" in result
        assert result["human_approval_required"] is True
        assert result["can_adapt"] is False  # < 30 days

    def test_can_adapt_requires_human(self):
        result = self.store.can_adapt()
        assert "Human approval required" in str(result["reasons"])

    def test_calculate_weekly_drift_no_data(self):
        drift = self.store._calculate_weekly_drift()
        assert drift == 0.0

    def test_calculate_weekly_drift_with_data(self):
        from core.telemetry import ConstitutionalTelemetry

        t = ConstitutionalTelemetry(
            session_id="s",
            predicted_risk=0.3,
            observed_outcome=0.7,
            misprediction_delta=0.4,
        )
        self.store.log(t)
        drift = self.store._calculate_weekly_drift()
        assert drift >= 0.0

    def test_generate_weekly_report(self):
        report = self.store.generate_weekly_report()
        assert "report_date" in report
        assert "telemetry_days" in report
        assert report["q3_compliance"] == "TELEMETRY_FIRST"
        assert report["adaptation_lock_status"] == "LOCKED"

    def test_first_date_persisted(self):
        from core.telemetry import TelemetryStore, ConstitutionalTelemetry

        t = ConstitutionalTelemetry(session_id="persist-test")
        self.store.log(t)
        # Reload from same path
        store2 = TelemetryStore(storage_path=self.tmpdir)
        assert store2.first_telemetry_date is not None


class TestLogTelemetryFunction:
    def test_log_telemetry_void(self, tmp_path):
        from core.telemetry import TelemetryStore, ConstitutionalTelemetry
        import core.telemetry as tel_module

        # Temporarily override the global store
        old_store = tel_module.telemetry_store
        tel_module.telemetry_store = TelemetryStore(storage_path=str(tmp_path))
        try:
            tel_module.log_telemetry(
                session_id="void-test",
                omega_0=0.04,
                irreversibility_index=0.3,
                verdict="VOID",
            )
        finally:
            tel_module.telemetry_store = old_store

    def test_log_telemetry_seal(self, tmp_path):
        import core.telemetry as tel_module

        old_store = tel_module.telemetry_store
        tel_module.telemetry_store = tel_module.TelemetryStore(storage_path=str(tmp_path))
        try:
            tel_module.log_telemetry("sess", 0.04, 0.1, verdict="SEAL")
        finally:
            tel_module.telemetry_store = old_store

    def test_log_telemetry_sabar(self, tmp_path):
        import core.telemetry as tel_module

        old_store = tel_module.telemetry_store
        tel_module.telemetry_store = tel_module.TelemetryStore(storage_path=str(tmp_path))
        try:
            tel_module.log_telemetry("sess", 0.04, 0.1, verdict="SABAR")
        finally:
            tel_module.telemetry_store = old_store

    def test_log_telemetry_888_hold(self, tmp_path):
        import core.telemetry as tel_module

        old_store = tel_module.telemetry_store
        tel_module.telemetry_store = tel_module.TelemetryStore(storage_path=str(tmp_path))
        try:
            tel_module.log_telemetry("sess", 0.04, 0.1, verdict="888_HOLD", gate_activated=True)
        finally:
            tel_module.telemetry_store = old_store

    def test_log_telemetry_gate_reason_omega(self, tmp_path):
        import core.telemetry as tel_module

        old_store = tel_module.telemetry_store
        tel_module.telemetry_store = tel_module.TelemetryStore(storage_path=str(tmp_path))
        try:
            # omega_0 > 0.06 → gate_reason = "uncertainty"
            tel_module.log_telemetry("sess", omega_0=0.07, irreversibility_index=0.1)
        finally:
            tel_module.telemetry_store = old_store

    def test_log_telemetry_gate_reason_irreversibility(self, tmp_path):
        import core.telemetry as tel_module

        old_store = tel_module.telemetry_store
        tel_module.telemetry_store = tel_module.TelemetryStore(storage_path=str(tmp_path))
        try:
            # irreversibility_index > 0.6 → gate_reason = "irreversibility"
            tel_module.log_telemetry("sess", omega_0=0.04, irreversibility_index=0.7)
        finally:
            tel_module.telemetry_store = old_store

    def test_check_adaptation_status(self, tmp_path):
        import core.telemetry as tel_module

        old_store = tel_module.telemetry_store
        tel_module.telemetry_store = tel_module.TelemetryStore(storage_path=str(tmp_path))
        try:
            result = tel_module.check_adaptation_status()
            assert "can_adapt" in result
        finally:
            tel_module.telemetry_store = old_store
