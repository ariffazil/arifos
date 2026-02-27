"""Focused checks for critique_thought backend behavior."""

from __future__ import annotations


def _fn(tool):
    return getattr(tool, "fn", tool)


async def test_critique_thought_prefers_triad_align_and_keeps_heuristics() -> None:
    from arifos_aaa_mcp import server as aaa

    anchored = await _fn(aaa.anchor_session)(query="Assess impact of config change", actor_id="ops")
    session_id = anchored["data"]["session_id"]

    critique = await _fn(aaa.critique_thought)(
        plan={"goal": "Assess impact", "steps": ["validate", "align"]},
        session_id=session_id,
        context="Assess impact of config change with mitigation and review",
    )

    data = critique["data"]
    assert data["session_id"] == session_id
    assert isinstance(data.get("mental_models"), dict)
    assert isinstance(data.get("failed_models"), list)
    assert data.get("critique_backend") in {"triad_align", "heuristic_fallback"}
    if data.get("critique_backend") == "triad_align":
        assert isinstance(data.get("alignment_backend_result"), dict)
        assert "alignment_status" in data
        assert "recommendation" in data
