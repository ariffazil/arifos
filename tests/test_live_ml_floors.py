from __future__ import annotations

from core.shared.sbert_floors import SbertFloorScores


def test_live_floor_audit_uses_heuristic_when_ml_flag_off(monkeypatch) -> None:
    from aclip_cai.core.floor_audit import FloorAuditor

    monkeypatch.setenv("ARIFOS_ML_FLOORS", "0")

    def _boom(_: str) -> SbertFloorScores:
        raise AssertionError("SBERT scorer should not be called when ARIFOS_ML_FLOORS=0")

    monkeypatch.setattr("core.shared.floor_audit.classify_asi_floors", _boom)

    result = FloorAuditor().check_floors(
        action="Conduct a governance review with approximately 3 alternative approaches.",
        context="human approved, data shows documented compliance",
        severity="low",
    )

    assert result.metadata["ml_floors_enabled"] is False
    assert result.metadata["ml_method"] == "heuristic"
    assert result.metadata["f5_score_source"] == "heuristic"
    assert result.metadata["f6_score_source"] == "heuristic"
    assert result.metadata["f9_score_source"] == "heuristic"


def test_live_floor_audit_uses_sbert_when_flag_on(monkeypatch) -> None:
    from aclip_cai.core.floor_audit import FloorAuditor

    monkeypatch.setenv("ARIFOS_ML_FLOORS", "1")

    def _fake_scores(_: str) -> SbertFloorScores:
        return SbertFloorScores(
            f5_peace=0.91,
            f6_empathy=0.88,
            f9_anti_hantu=0.92,
            confidence=0.84,
            method="sbert",
        )

    monkeypatch.setattr("core.shared.floor_audit.classify_asi_floors", _fake_scores)

    result = FloorAuditor().check_floors(
        action="Use a respectful and careful approach that protects everyone involved.",
        context="human approved, data shows documented compliance",
        severity="low",
    )

    assert result.metadata["ml_floors_enabled"] is True
    assert result.metadata["ml_method"] == "sbert"
    assert result.metadata["ml_confidence"] == 0.84
    assert result.metadata["f5_score_source"] == "sbert"
    assert result.metadata["f6_score_source"] == "sbert"
    assert result.metadata["f9_score_source"] == "sbert"
    assert result.floor_results["F5"].metadata["score_source"] == "sbert"
    assert result.floor_results["F6"].metadata["raw_ml_score"] == 0.88
    assert result.floor_results["F9"].metadata["ml_method"] == "sbert"


def test_live_floor_audit_falls_back_when_sbert_scoring_fails(monkeypatch) -> None:
    from aclip_cai.core.floor_audit import FloorAuditor

    monkeypatch.setenv("ARIFOS_ML_FLOORS", "1")

    def _explode(_: str) -> SbertFloorScores:
        raise RuntimeError("test fallback")

    monkeypatch.setattr("core.shared.floor_audit.classify_asi_floors", _explode)

    result = FloorAuditor().check_floors(
        action="Use a respectful and careful approach that protects everyone involved.",
        context="human approved, data shows documented compliance",
        severity="low",
    )

    assert result.metadata["ml_floors_enabled"] is True
    assert result.metadata["ml_method"] == "heuristic_fallback"
    assert result.metadata["f5_score_source"] == "heuristic"
    assert result.metadata["f6_score_source"] == "heuristic"
    assert result.metadata["f9_score_source"] == "heuristic"
    assert result.metadata["ml_error"] == "test fallback"
