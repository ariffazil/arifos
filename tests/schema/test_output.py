"""
tests/schema/test_output.py — Canonical ArifOSOutput Envelope Tests

Validates that the canonical output schema behaves correctly:
- Correct top-level fields
- Verdict contract (6 values only)
- Status contract (4 values only)
- Metrics defaults and ranges
- Trace serialization
- Authority defaults
- Error normalization
- Meta defaults
- Production serialization (debug stripped)
- Legacy compat adapter
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from core.schema import (
    ArifOSOutput,
    Authority,
    AuthorityLevel,
    AuthState,
    DebugBlock,
    Meta,
    Metrics,
    SchemaError,
    Stage,
    Status,
    Trace,
    Verdict,
)

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────


def make_output(**overrides) -> ArifOSOutput:
    """Build a minimal valid ArifOSOutput for tests."""
    defaults = dict(
        tool="reason_mind",
        session_id="sess_test",
        stage=Stage.MIND.value,
        verdict=Verdict.PROVISIONAL,
        status=Status.SUCCESS,
    )
    defaults.update(overrides)
    return ArifOSOutput(**defaults)


# ──────────────────────────────────────────────────────────────────────────────
# Structure
# ──────────────────────────────────────────────────────────────────────────────


class TestCanonicalOutputStructure:
    def test_required_top_level_fields_present(self):
        out = make_output()
        d = out.to_production()
        for field in (
            "ok",
            "tool",
            "session_id",
            "stage",
            "verdict",
            "status",
            "metrics",
            "trace",
            "authority",
            "payload",
            "errors",
            "meta",
        ):
            assert field in d, f"Missing top-level field: {field}"

    def test_ok_defaults_true(self):
        out = make_output()
        assert out.ok is True

    def test_session_id_nullable(self):
        out = make_output(session_id=None)
        assert out.session_id is None

    def test_payload_defaults_empty_dict(self):
        out = make_output()
        assert out.payload == {}

    def test_errors_defaults_empty_list(self):
        out = make_output()
        assert out.errors == []


# ──────────────────────────────────────────────────────────────────────────────
# Verdict contract
# ──────────────────────────────────────────────────────────────────────────────


class TestVerdictContract:
    def test_all_six_verdicts_accepted(self):
        for v in ("SEAL", "PROVISIONAL", "PARTIAL", "SABAR", "HOLD", "VOID"):
            out = make_output(verdict=v)
            assert out.verdict == v

    def test_unknown_verdict_rejected(self):
        with pytest.raises(ValidationError):
            make_output(verdict="APPROVED")

    def test_legacy_hold_888_rejected(self):
        # The canonical schema does NOT accept the legacy 888_HOLD alias
        with pytest.raises(ValidationError):
            make_output(verdict="888_HOLD")


# ──────────────────────────────────────────────────────────────────────────────
# Status contract
# ──────────────────────────────────────────────────────────────────────────────


class TestStatusContract:
    def test_all_four_statuses_accepted(self):
        for s in ("SUCCESS", "ERROR", "TIMEOUT", "DRY_RUN"):
            out = make_output(status=s)
            assert out.status == s

    def test_unknown_status_rejected(self):
        with pytest.raises(ValidationError):
            make_output(status="PENDING")

    def test_status_defaults_success(self):
        out = make_output()
        assert out.status == "SUCCESS"


# ──────────────────────────────────────────────────────────────────────────────
# Metrics
# ──────────────────────────────────────────────────────────────────────────────


class TestMetrics:
    def test_metrics_all_none_by_default(self):
        m = Metrics()
        for field in (
            "truth",
            "clarity_delta",
            "confidence",
            "peace",
            "vitality",
            "entropy_delta",
            "authority",
            "risk",
        ):
            assert getattr(m, field) is None

    def test_metrics_range_validation_truth(self):
        with pytest.raises(ValidationError):
            Metrics(truth=1.5)
        with pytest.raises(ValidationError):
            Metrics(truth=-0.1)

    def test_metrics_range_validation_clarity_delta(self):
        with pytest.raises(ValidationError):
            Metrics(clarity_delta=1.5)
        with pytest.raises(ValidationError):
            Metrics(clarity_delta=-1.5)

    def test_metrics_range_validation_peace(self):
        with pytest.raises(ValidationError):
            Metrics(peace=2.1)

    def test_metrics_range_validation_vitality(self):
        with pytest.raises(ValidationError):
            Metrics(vitality=10.1)

    def test_metrics_to_dict_compact(self):
        m = Metrics(truth=0.9, confidence=0.8)
        compact = m.to_dict_compact()
        assert compact == {"truth": 0.9, "confidence": 0.8}
        assert "clarity_delta" not in compact

    def test_full_metrics_in_output(self):
        out = make_output(
            metrics=Metrics(
                truth=0.82,
                clarity_delta=-0.08,
                confidence=0.72,
                peace=1.0,
                vitality=9.7,
                entropy_delta=-0.08,
                authority=1.0,
                risk=0.14,
            )
        )
        assert out.metrics.truth == 0.82
        assert out.metrics.authority == 1.0
        assert out.metrics.risk == 0.14


# ──────────────────────────────────────────────────────────────────────────────
# Trace
# ──────────────────────────────────────────────────────────────────────────────


class TestTrace:
    def test_trace_empty_by_default(self):
        t = Trace()
        assert t.to_dict() == {}

    def test_trace_to_dict_only_executed_stages(self):
        t = Trace(stage_000_init=Verdict.SEAL, stage_333_mind=Verdict.PROVISIONAL)
        d = t.to_dict()
        assert d == {"000_INIT": "SEAL", "333_MIND": "PROVISIONAL"}

    def test_trace_from_dict(self):
        raw = {"000_INIT": "SEAL", "111_SENSE": "PARTIAL", "333_MIND": "PROVISIONAL"}
        t = Trace.from_dict(raw)
        assert t.stage_000_init == Verdict.SEAL
        assert t.stage_111_sense == Verdict.PARTIAL
        assert t.stage_333_mind == Verdict.PROVISIONAL
        assert t.stage_444_router is None

    def test_trace_from_dict_unknown_key_ignored(self):
        raw = {"000_INIT": "SEAL", "UNKNOWN_STAGE": "VOID"}
        t = Trace.from_dict(raw)
        assert t.stage_000_init == Verdict.SEAL

    def test_trace_from_dict_invalid_verdict_falls_back(self):
        raw = {"000_INIT": "GIBBERISH"}
        t = Trace.from_dict(raw)
        assert t.stage_000_init == Verdict.SABAR


# ──────────────────────────────────────────────────────────────────────────────
# Authority
# ──────────────────────────────────────────────────────────────────────────────


class TestAuthority:
    def test_authority_defaults(self):
        a = Authority()
        assert a.actor_id == "anonymous"
        assert a.level == AuthorityLevel.ANONYMOUS
        assert a.human_required is False
        assert a.approval_scope == []
        assert a.auth_state == AuthState.ANONYMOUS

    def test_authority_human_level(self):
        a = Authority(
            actor_id="arif",
            level=AuthorityLevel.HUMAN,
            human_required=False,
            approval_scope=["forge", "seal"],
            auth_state=AuthState.VERIFIED,
        )
        assert a.actor_id == "arif"
        assert a.level == "human"
        assert a.auth_state == "verified"


# ──────────────────────────────────────────────────────────────────────────────
# Errors
# ──────────────────────────────────────────────────────────────────────────────


class TestErrors:
    def test_schema_error_structure(self):
        e = SchemaError(
            code="IMPORT_ERROR",
            message="cannot import name 'get_session_manager'",
            stage="777_FORGE",
            recoverable=True,
        )
        assert e.code == "IMPORT_ERROR"
        assert e.stage == "777_FORGE"
        assert e.recoverable is True

    def test_schema_error_in_output(self):
        out = make_output(
            ok=False,
            status=Status.ERROR,
            errors=[
                SchemaError(
                    code="AUTH_FAIL",
                    message="Token invalid",
                    stage="000_INIT",
                    recoverable=False,
                )
            ],
        )
        assert out.ok is False
        assert out.errors[0].code == "AUTH_FAIL"


# ──────────────────────────────────────────────────────────────────────────────
# Meta
# ──────────────────────────────────────────────────────────────────────────────


class TestMeta:
    def test_meta_defaults(self):
        m = Meta()
        assert m.schema_version == "1.0.0"
        assert m.debug is False
        assert m.dry_run is False
        assert "T" in m.timestamp  # ISO-8601 format

    def test_meta_debug_flag(self):
        m = Meta(debug=True)
        assert m.debug is True


# ──────────────────────────────────────────────────────────────────────────────
# Production serialization
# ──────────────────────────────────────────────────────────────────────────────


class TestProductionSerialization:
    def test_debug_stripped_when_meta_debug_false(self):
        out = make_output(
            meta=Meta(debug=False),
            debug=DebugBlock(reasoning={"step": "1"}, assumptions=["assume safe"]),
        )
        prod = out.to_production()
        assert "debug" not in prod

    def test_debug_present_when_meta_debug_true(self):
        out = make_output(
            meta=Meta(debug=True),
            debug=DebugBlock(assumptions=["assume safe"]),
        )
        prod = out.to_production()
        assert "debug" in prod
        assert prod["debug"]["assumptions"] == ["assume safe"]

    def test_production_has_no_final_verdict(self):
        out = make_output()
        prod = out.to_production()
        assert "final_verdict" not in prod
        assert "telemetry" not in prod
        assert "score_delta" not in prod
        assert "philosophy" not in prod
        assert "opex" not in prod

    def test_to_legacy_compat_adds_aliases(self):
        out = make_output(verdict=Verdict.SEAL)
        legacy = out.to_legacy_compat()
        assert legacy["final_verdict"] == "SEAL"
        assert "auth_context" in legacy
        assert "telemetry" in legacy
        assert "score_delta" in legacy
        assert legacy["data"] == legacy["payload"]


# ──────────────────────────────────────────────────────────────────────────────
# Full canonical example (from spec)
# ──────────────────────────────────────────────────────────────────────────────


class TestCanonicalExample:
    def test_full_canonical_example(self):
        """The canonical example from the spec must round-trip correctly."""
        out = ArifOSOutput(
            ok=True,
            tool="reason_mind",
            session_id="sess_123",
            stage="333_MIND",
            verdict=Verdict.PROVISIONAL,
            status=Status.SUCCESS,
            metrics=Metrics(
                truth=0.82,
                clarity_delta=-0.08,
                confidence=0.72,
                peace=1.0,
                vitality=9.7,
                entropy_delta=-0.08,
                authority=1.0,
                risk=0.14,
            ),
            trace=Trace.from_dict(
                {
                    "000_INIT": "SEAL",
                    "111_SENSE": "SEAL",
                    "222_REALITY": "PARTIAL",
                    "333_MIND": "PROVISIONAL",
                }
            ),
            authority=Authority(
                actor_id="arif",
                level=AuthorityLevel.HUMAN,
                human_required=False,
                approval_scope=[],
                auth_state=AuthState.VERIFIED,
            ),
            payload={
                "reasoning_status": "exploratory",
                "confidence_band": "PLAUSIBLE",
                "needs_grounding": True,
                "next_stage": "666_CRITIQUE",
                "hypotheses": [
                    {
                        "path": "conservative",
                        "band": "CLAIM",
                        "confidence": 0.91,
                        "hypothesis": "...",
                    }
                ],
            },
            errors=[],
            meta=Meta(schema_version="1.0.0", debug=False, dry_run=False),
        )

        prod = out.to_production()

        assert prod["ok"] is True
        assert prod["tool"] == "reason_mind"
        assert prod["session_id"] == "sess_123"
        assert prod["stage"] == "333_MIND"
        assert prod["verdict"] == "PROVISIONAL"
        assert prod["status"] == "SUCCESS"
        assert prod["metrics"]["truth"] == 0.82
        assert prod["trace"]["000_INIT"] == "SEAL"
        assert prod["trace"]["333_MIND"] == "PROVISIONAL"
        assert prod["authority"]["actor_id"] == "arif"
        assert prod["authority"]["auth_state"] == "verified"
        assert prod["payload"]["reasoning_status"] == "exploratory"
        assert prod["errors"] == []
        assert prod["meta"]["schema_version"] == "1.0.0"
        assert "debug" not in prod
