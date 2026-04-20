from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from arifos.geox.renderers.base import RenderSession
from arifos.geox.renderers.cigvis_adapter import (
    CigvisAdapter,
    InteractiveCigvisRenderer,
    StaticCigvisRenderer,
)


def test_compile_scene_returns_empty_when_cigvis_is_unavailable(monkeypatch):
    monkeypatch.setattr("arifos.geox.renderers.cigvis_adapter.CIGVIS_AVAILABLE", False)
    adapter = CigvisAdapter()

    scene = adapter.compile_scene({"state_type": "cross_section"})

    assert scene == {"nodes": [], "camera": None}


def test_surface_to_node_handles_empty_surface_vertices():
    adapter = CigvisAdapter()
    surface = type("Surface", (), {"vertices": [], "color": None})()

    assert adapter._surface_to_node(surface) == []


def test_render_snapshot_rejects_empty_node_scene():
    adapter = CigvisAdapter()

    result = adapter.render_snapshot({"nodes": [], "metadata": {}})

    assert result.success is False
    assert result.errors == ["No renderable nodes in scene"]


def test_render_snapshot_reports_missing_output_file(monkeypatch, tmp_path):
    adapter = CigvisAdapter(output_dir=str(tmp_path))
    monkeypatch.setattr(
        "arifos.geox.renderers.cigvis_adapter.cigvis.plot3D",
        lambda *args, **kwargs: None,
    )

    result = adapter.render_snapshot({"nodes": ["node"], "metadata": {}}, output_path=str(tmp_path / "missing.png"))

    assert result.success is False
    assert result.errors == ["Snapshot file was not created"]


def test_render_snapshot_adds_headless_hint_for_viewport_errors(monkeypatch):
    adapter = CigvisAdapter()

    def fake_plot3d(*args, **kwargs):
        raise RuntimeError("viewport should be 1D 4-element array-like")

    monkeypatch.setattr("arifos.geox.renderers.cigvis_adapter.cigvis.plot3D", fake_plot3d)

    result = adapter.render_snapshot({"nodes": ["node"], "metadata": {}})

    assert result.success is False
    assert any("Headless render failed" in error for error in result.errors)


def test_launch_interactive_respects_supports_interactive_flag():
    adapter = CigvisAdapter()
    adapter.supports_interactive = False

    result = adapter.launch_interactive({"nodes": ["node"], "metadata": {}})

    assert result.success is False
    assert result.errors == ["Interactive mode not supported by this adapter"]


def test_session_cleanup_and_shutdown_release_ports():
    adapter = CigvisAdapter()
    session = RenderSession(
        session_id="viser_8100",
        started_at=datetime.now(timezone.utc) - timedelta(seconds=10),
        scene_id="scene-a",
        access_url="http://localhost:8100",
        port=8100,
        ttl_seconds=1,
    )
    adapter._sessions[session.session_id] = session
    adapter._used_ports.add(8100)

    assert adapter.cleanup_expired_sessions() == 1
    assert adapter.get_active_sessions() == []
    assert 8100 not in adapter._used_ports


def test_allocate_port_raises_when_none_are_available(monkeypatch):
    adapter = CigvisAdapter()
    monkeypatch.setattr(adapter, "_is_port_available", lambda port: False)

    with pytest.raises(RuntimeError, match="No available ports"):
        adapter._allocate_port()


def test_static_and_interactive_renderer_fail_cleanly_without_cigvis(monkeypatch):
    monkeypatch.setattr("arifos.geox.renderers.cigvis_adapter.CIGVIS_AVAILABLE", False)

    static_renderer = StaticCigvisRenderer(adapter=CigvisAdapter())
    interactive_renderer = InteractiveCigvisRenderer(adapter=CigvisAdapter())

    static_result = static_renderer.render({"state_type": "cross_section"})
    interactive_result = interactive_renderer.render({"state_type": "cross_section"})

    assert static_result.success is False
    assert interactive_result.success is False
    assert "CIGVis not installed" in static_result.errors[0]
    assert "CIGVis not installed" in interactive_result.errors[0]
