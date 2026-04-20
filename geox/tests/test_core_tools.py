from __future__ import annotations

import pytest

from arifos.geox.geox_schemas import CoordinatePoint
from arifos.geox.geox_tools import (
    EOFoundationModelTool,
    EarthModelTool,
    GeoRAGTool,
    SeismicVLMTool,
    SimulatorTool,
    ToolRegistry,
)


@pytest.mark.asyncio
async def test_earth_model_tool_returns_reproducible_quantities():
    tool = EarthModelTool()
    location = CoordinatePoint(latitude=4.5, longitude=103.7, depth_m=2500.0)
    inputs = {
        "query": "Estimate reservoir properties",
        "location": location,
        "depth_range_m": (2000.0, 3000.0),
    }

    result_a = await tool.run(inputs)
    result_b = await tool.run(inputs)

    assert result_a.success is True
    assert [q.quantity_type for q in result_a.quantities] == [
        "seismic_velocity",
        "density",
        "porosity",
    ]
    assert [q.value for q in result_a.quantities] == [q.value for q in result_b.quantities]
    assert result_a.raw_output["physics_check"] == "passed"


@pytest.mark.asyncio
async def test_earth_model_tool_rejects_invalid_inputs():
    tool = EarthModelTool()

    result = await tool.run({"query": "missing location"})

    assert result.success is False
    assert "Invalid inputs" in (result.error or "")


@pytest.mark.asyncio
async def test_eo_foundation_model_tool_runs_with_bbox_inputs():
    tool = EOFoundationModelTool()
    result = await tool.run(
        {
            "bbox": {"west": 103.0, "south": 4.0, "east": 104.0, "north": 5.0},
            "bands": ["B02", "B04", "TIR"],
            "date_range": ("2026-01-01", "2026-01-31"),
        }
    )

    assert result.success is True
    assert {q.quantity_type for q in result.quantities} == {
        "surface_reflectance",
        "ndvi",
        "thermal_anomaly",
    }
    assert result.metadata["bands"] == ["B02", "B04", "TIR"]


@pytest.mark.asyncio
async def test_seismic_vlm_tool_enforces_perception_uncertainty_floor():
    tool = SeismicVLMTool()
    result = await tool.run(
        {
            "image_path": "/tmp/example.png",
            "interpretation_query": "Identify likely faults",
        }
    )

    assert result.success is True
    assert all(q.uncertainty >= 0.15 for q in result.quantities)
    assert result.metadata["multisensor_required"] is True
    assert result.raw_output["perception_bridge_warning"]


@pytest.mark.asyncio
async def test_simulator_tool_requires_non_empty_timesteps():
    tool = SimulatorTool()

    result = await tool.run({"scenario": {"target_depth_m": 2500.0}, "timesteps_ma": []})

    assert result.success is False
    assert result.error == "timesteps_ma must be a non-empty list."


@pytest.mark.asyncio
async def test_simulator_tool_returns_forward_model_outputs():
    tool = SimulatorTool()
    result = await tool.run(
        {
            "scenario": {
                "latitude": 4.5,
                "longitude": 103.7,
                "target_depth_m": 2800.0,
                "geothermal_gradient_degc_km": 32.0,
            },
            "timesteps_ma": [0.0, 5.0, 10.0],
        }
    )

    assert result.success is True
    assert [q.quantity_type for q in result.quantities] == [
        "pressure_psi",
        "temperature_degC",
        "maturity_ro",
    ]
    assert result.raw_output["model"] == "BASIN-SIM-GEOX-v0.1-mock"


@pytest.mark.asyncio
async def test_georag_tool_falls_back_to_global_literature_when_basin_has_no_match():
    tool = GeoRAGTool()
    result = await tool.run(
        {
            "query": "reservoir porosity",
            "basin": "Nonexistent Basin",
            "max_results": 2,
        }
    )

    assert result.success is True
    assert result.metadata["literature_hits"] == 2
    assert len(result.metadata["citations"]) == 2
    assert all("DOI:" in citation for citation in result.metadata["citations"])


def test_tool_registry_duplicate_and_missing_lookup_errors():
    registry = ToolRegistry()
    registry.register(EarthModelTool())

    with pytest.raises(ValueError):
        registry.register(EarthModelTool())

    with pytest.raises(KeyError):
        registry.get("missing-tool")


def test_tool_registry_default_registry_contains_expected_aliases():
    registry = ToolRegistry.default_registry()

    names = registry.list_tools()
    assert "EarthModelTool" in names
    assert "SingleLineInterpreter" in names
    assert "WellLogTool" in names
    assert "PetroPhysicsTool" in names
    assert registry.health_check_all()["EarthModelTool"] is True
