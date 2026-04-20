from __future__ import annotations

from pathlib import Path

import numpy as np

from arifos.geox.renderers.cigvis_adapter import CigvisAdapter
from arifos.geox.renderers.primitives import (
    FaultPrimitive,
    RenderColor,
    SliceDirection,
    SurfacePrimitive,
    Vector3,
    VolumeSlicePrimitive,
    WellTrajectoryPrimitive,
)


def test_volume_slice_to_node_uses_cigvis_v020_api(monkeypatch):
    adapter = CigvisAdapter()
    volume_slice = VolumeSlicePrimitive(
        data=np.arange(27, dtype=np.float32).reshape(3, 3, 3),
        direction=SliceDirection.CROSSLINE,
        slice_value=2,
        clim=(-1.0, 1.0),
        cmap="gray",
    )
    captured = {}

    def fake_create_slices(volume, **kwargs):
        captured["volume_shape"] = volume.shape
        captured["kwargs"] = kwargs
        return ["slice-node", "line-node"]

    monkeypatch.setattr("arifos.geox.renderers.cigvis_adapter.cigvis.create_slices", fake_create_slices)

    nodes = adapter._volume_slice_to_node(volume_slice)

    assert nodes == ["slice-node", "line-node"]
    assert captured["volume_shape"] == (3, 3, 3)
    assert captured["kwargs"]["pos"] == {"x": [], "y": [2], "z": []}
    assert captured["kwargs"]["clim"] == [-1.0, 1.0]
    assert captured["kwargs"]["cmap"] == "gray"
    assert captured["kwargs"]["intersection_lines"] is False


def test_surface_to_node_uses_create_surfaces(monkeypatch):
    adapter = CigvisAdapter()
    surface = SurfacePrimitive(
        vertices=[
            Vector3(0.0, 0.0, 0.0),
            Vector3(0.0, 1.0, -1.0),
            Vector3(1.0, 0.0, -2.0),
            Vector3(1.0, 1.0, -3.0),
        ],
        color=RenderColor.from_hex("#3366cc"),
    )
    captured = {}

    def fake_create_surfaces(surfaces, **kwargs):
        captured["surfaces"] = surfaces
        captured["kwargs"] = kwargs
        return ["surface-node"]

    monkeypatch.setattr(
        "arifos.geox.renderers.cigvis_adapter.cigvis.create_surfaces",
        fake_create_surfaces,
    )

    nodes = adapter._surface_to_node(surface)

    assert nodes == ["surface-node"]
    assert len(captured["surfaces"]) == 1
    assert captured["surfaces"][0].shape == (4, 3)
    assert captured["kwargs"]["shape"] == (2, 2)
    assert captured["kwargs"]["value_type"] == "depth"
    assert captured["kwargs"]["cmap"] == "jet"
    assert captured["kwargs"]["color"] == "#3366cc"
    assert captured["kwargs"]["shading"] == "smooth"


def test_fault_to_node_uses_create_points(monkeypatch):
    adapter = CigvisAdapter()
    fault = FaultPrimitive(
        trace_points=[
            Vector3(0.0, 0.0, 0.0),
            Vector3(1.0, 1.0, -1.0),
            Vector3(2.0, 2.0, -2.0),
        ],
        color=RenderColor.from_hex("#ff0000"),
    )
    captured = {}

    def fake_create_points(points, **kwargs):
        captured["points"] = points
        captured["kwargs"] = kwargs
        return "fault-node"

    monkeypatch.setattr("arifos.geox.renderers.cigvis_adapter.cigvis.create_points", fake_create_points)

    nodes = adapter._fault_to_node(fault)

    assert nodes == ["fault-node"]
    assert captured["points"].shape == (3, 3)
    assert captured["kwargs"]["r"] == 2
    assert captured["kwargs"]["color"] == "#ff0000"


def test_well_to_node_uses_create_well_logs(monkeypatch):
    adapter = CigvisAdapter()
    well = WellTrajectoryPrimitive(
        trajectory=[
            Vector3(0.0, 0.0, 0.0),
            Vector3(0.0, 0.0, -1.0),
            Vector3(0.0, 0.0, -2.0),
        ],
        md_values=[0.0, 10.0, 20.0],
        color=RenderColor.from_hex("#00aa55"),
    )
    captured = {}

    def fake_create_well_logs(points, **kwargs):
        captured["points"] = points
        captured["kwargs"] = kwargs
        return ["well-node"]

    monkeypatch.setattr(
        "arifos.geox.renderers.cigvis_adapter.cigvis.vispyplot.create_well_logs",
        fake_create_well_logs,
    )

    nodes = adapter._well_to_node(well)

    assert nodes == ["well-node"]
    assert captured["points"].shape == (3, 3)
    assert captured["kwargs"]["values"].shape == (3, 1)
    assert captured["kwargs"]["cmap"] == "#00aa55"
    assert captured["kwargs"]["cyclinder"] is True
    assert captured["kwargs"]["radius_tube"] == 1.5


def test_render_snapshot_uses_plot3d_savename(monkeypatch, tmp_path):
    adapter = CigvisAdapter(output_dir=str(tmp_path))
    output_path = tmp_path / "scene.png"
    captured = {}

    def fake_plot3d(nodes, **kwargs):
        captured["nodes"] = nodes
        captured["kwargs"] = kwargs
        Path(kwargs["savename"]).write_bytes(b"png")

    monkeypatch.setattr("arifos.geox.renderers.cigvis_adapter.cigvis.plot3D", fake_plot3d)

    result = adapter.render_snapshot(
        {"nodes": ["node-a"], "metadata": {"title": "demo"}},
        output_path=str(output_path),
        width=640,
        height=480,
    )

    assert result.success is True
    assert output_path.exists()
    assert captured["nodes"] == ["node-a"]
    assert captured["kwargs"]["savename"] == str(output_path)
    assert captured["kwargs"]["size"] == (640, 480)
    assert captured["kwargs"]["run_app"] is False


def test_launch_interactive_uses_viserplot_server(monkeypatch):
    adapter = CigvisAdapter()
    captured = {}

    def fake_create_server(port):
        captured["port"] = port
        return {"port": port}

    def fake_plot3d(nodes, **kwargs):
        captured["nodes"] = nodes
        captured["kwargs"] = kwargs

    monkeypatch.setattr(
        "arifos.geox.renderers.cigvis_adapter.cigvis.viserplot.create_server",
        fake_create_server,
    )
    monkeypatch.setattr(
        "arifos.geox.renderers.cigvis_adapter.cigvis.viserplot.plot3D",
        fake_plot3d,
    )

    result = adapter.launch_interactive(
        {"nodes": ["node-a"], "metadata": {"title": "Interactive Scene"}},
        port=8111,
        ttl_seconds=30,
    )

    assert result.success is True
    assert result.session is not None
    assert result.embedded_url == "http://localhost:8111"
    assert captured["port"] == 8111
    assert captured["nodes"] == ["node-a"]
    assert captured["kwargs"]["server"] == {"port": 8111}
    assert captured["kwargs"]["run_app"] is False


def test_compile_cross_section_well_creates_cigvis_node(monkeypatch):
    adapter = CigvisAdapter()
    captured = {}

    def fake_create_well_logs(points, **kwargs):
        captured["points"] = points
        captured["kwargs"] = kwargs
        return ["well-node"]

    monkeypatch.setattr(
        "arifos.geox.renderers.cigvis_adapter.cigvis.vispyplot.create_well_logs",
        fake_create_well_logs,
    )

    canonical_state = {
        "state_type": "cross_section",
        "profile_name": "Section A",
        "wells": [
            {
                "well_id": "W-1",
                "well_name": "Well 1",
                "source": "well_log",
                "trajectory": [
                    {"x": 10.0, "y": 0.0, "z": 0.0},
                    {"x": 10.0, "y": 0.0, "z": -1000.0},
                    {"x": 10.0, "y": 0.0, "z": -2000.0},
                ],
            }
        ],
        "faults": [],
        "units": [],
    }

    scene = adapter.compile_scene(canonical_state)

    assert scene["nodes"] == ["well-node"]
    assert captured["points"].shape == (3, 3)
    assert scene["metadata"]["primitive_count"] == 1
    assert scene["metadata"]["title"] == "Section A"
