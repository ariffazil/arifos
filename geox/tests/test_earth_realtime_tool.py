"""
tests/test_earth_realtime_tool.py — EarthRealtimeTool unit tests
DITEMPA BUKAN DIBERI

Tests live Earth observation signals tool:
  - USGS earthquake parsing
  - Open-Meteo climate parsing
  - Graceful degradation on API failure
  - F7 HUMILITY: uncertainty bounds on all quantities
  - F11 AUDIT: provenance on all GeoQuantity objects
"""

from __future__ import annotations

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import httpx

from arifos.geox.geox_schemas import CoordinatePoint
from arifos.geox.tools.earth_realtime_tool import EarthRealtimeTool


SABAH_LOCATION = CoordinatePoint(latitude=5.9792, longitude=116.0733)  # Kota Kinabalu

# ── Fixtures ──────────────────────────────────────────────────────────────────

MOCK_USGS_RESPONSE = {
    "type": "FeatureCollection",
    "features": [
        {
            "id": "us7000abcd",
            "type": "Feature",
            "properties": {
                "mag": 4.2,
                "place": "50 km NE of Kota Kinabalu",
                "time": 1700000000000,
                "url": "https://earthquake.usgs.gov/earthquakes/eventpage/us7000abcd",
            },
            "geometry": {"type": "Point", "coordinates": [116.5, 6.1, 12.5]},
        },
        {
            "id": "us7000efgh",
            "type": "Feature",
            "properties": {
                "mag": 2.8,
                "place": "20 km SW of Ranau",
                "time": 1699900000000,
                "url": "https://earthquake.usgs.gov/earthquakes/eventpage/us7000efgh",
            },
            "geometry": {"type": "Point", "coordinates": [116.4, 5.8, 8.0]},
        },
    ],
}

MOCK_METEO_RESPONSE = {
    "current": {
        "time": "2026-04-03T10:00",
        "temperature_2m": 29.5,
        "relative_humidity_2m": 82,
        "precipitation": 0.0,
        "surface_pressure": 1007.3,
        "wind_speed_10m": 12.4,
        "wind_direction_10m": 220,
        "cloud_cover": 60,
        "weather_code": 2,
    },
    "current_units": {
        "temperature_2m": "°C",
        "surface_pressure": "hPa",
    },
}

MOCK_GEOMAG_RESPONSE = {
    "geomagnetic-field-model-result": {
        "field-value": {
            "declination": {"units": "deg (east)", "value": 0.72},
            "inclination": {"units": "deg (down)", "value": -20.5},
            "total-intensity": {"units": "nT", "value": 40662},
        }
    }
}


# ── Helper ────────────────────────────────────────────────────────────────────

def _make_mock_response(data: dict, status_code: int = 200):
    mock = MagicMock(spec=httpx.Response)
    mock.status_code = status_code
    mock.json.return_value = data
    mock.raise_for_status = MagicMock()
    return mock


# ── Tests ──────────────────────────────────────────────────────────────────────

class TestEarthRealtimeToolValidation:
    def test_validate_inputs_valid(self):
        tool = EarthRealtimeTool()
        assert tool.validate_inputs({"location": SABAH_LOCATION}) is True

    def test_validate_inputs_missing_location(self):
        tool = EarthRealtimeTool()
        assert tool.validate_inputs({}) is False

    def test_validate_inputs_wrong_type(self):
        tool = EarthRealtimeTool()
        assert tool.validate_inputs({"location": "not-a-point"}) is False


class TestUSGSParsing:
    @pytest.mark.asyncio
    async def test_usgs_quantities_produced(self):
        tool = EarthRealtimeTool()
        mock_resp = _make_mock_response(MOCK_USGS_RESPONSE)

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client.get = AsyncMock(return_value=mock_resp)
            mock_client_cls.return_value = mock_client

            result = await tool._fetch_usgs_earthquakes(SABAH_LOCATION, 300.0, 10)

        assert result["raw"]["count"] == 2
        assert result["raw"]["largest_magnitude"] == pytest.approx(4.2)
        # 2 events × 2 quantities (magnitude + depth) = 4
        assert len(result["quantities"]) == 4

    @pytest.mark.asyncio
    async def test_usgs_quantity_uncertainty_bounds(self):
        tool = EarthRealtimeTool()
        mock_resp = _make_mock_response(MOCK_USGS_RESPONSE)

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client.get = AsyncMock(return_value=mock_resp)
            mock_client_cls.return_value = mock_client

            result = await tool._fetch_usgs_earthquakes(SABAH_LOCATION, 300.0, 10)

        # F7 HUMILITY: all quantities must carry explicit uncertainty
        for qty in result["quantities"]:
            assert qty.uncertainty is not None
            assert 0.0 < qty.uncertainty <= 0.15

    @pytest.mark.asyncio
    async def test_usgs_quantity_provenance(self):
        tool = EarthRealtimeTool()
        mock_resp = _make_mock_response(MOCK_USGS_RESPONSE)

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client.get = AsyncMock(return_value=mock_resp)
            mock_client_cls.return_value = mock_client

            result = await tool._fetch_usgs_earthquakes(SABAH_LOCATION, 300.0, 10)

        # F11 AUTHORITY: every quantity must carry provenance
        for qty in result["quantities"]:
            assert qty.provenance is not None
            assert qty.provenance.source_type == "sensor"
            assert qty.provenance.confidence >= 0.95


class TestOpenMeteoParsing:
    @pytest.mark.asyncio
    async def test_climate_quantities_produced(self):
        tool = EarthRealtimeTool()
        mock_resp = _make_mock_response(MOCK_METEO_RESPONSE)

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client.get = AsyncMock(return_value=mock_resp)
            mock_client_cls.return_value = mock_client

            result = await tool._fetch_open_meteo(SABAH_LOCATION)

        assert result["raw"]["temperature_2m_c"] == pytest.approx(29.5)
        assert result["raw"]["surface_pressure_hpa"] == pytest.approx(1007.3)
        # Should produce at least temperature + pressure + humidity + wind
        assert len(result["quantities"]) >= 4

    @pytest.mark.asyncio
    async def test_climate_quantity_units_present(self):
        tool = EarthRealtimeTool()
        mock_resp = _make_mock_response(MOCK_METEO_RESPONSE)

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client.get = AsyncMock(return_value=mock_resp)
            mock_client_cls.return_value = mock_client

            result = await tool._fetch_open_meteo(SABAH_LOCATION)

        for qty in result["quantities"]:
            assert qty.units is not None and len(qty.units) > 0
            assert qty.quantity_type is not None


class TestGeoMagParsing:
    @pytest.mark.asyncio
    async def test_geomag_declination_parsed(self):
        tool = EarthRealtimeTool()
        mock_resp = _make_mock_response(MOCK_GEOMAG_RESPONSE)

        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = AsyncMock()
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=False)
            mock_client.get = AsyncMock(return_value=mock_resp)
            mock_client_cls.return_value = mock_client

            result = await tool._fetch_geomag(SABAH_LOCATION)

        assert result["raw"]["declination_deg"] == pytest.approx(0.72)
        assert result["raw"]["inclination_deg"] == pytest.approx(-20.5)
        # Should have declination + inclination
        assert len(result["quantities"]) == 2


class TestGracefulDegradation:
    @pytest.mark.asyncio
    async def test_full_run_succeeds_with_all_mocked(self):
        tool = EarthRealtimeTool()

        async def mock_usgs(loc, radius, limit):
            return {
                "quantities": [],
                "raw": {"count": 0, "radius_km": radius, "largest_magnitude": None, "events": []},
            }

        async def mock_meteo(loc):
            return {
                "quantities": [],
                "raw": {"temperature_2m_c": 28.0, "surface_pressure_hpa": 1010.0},
            }

        async def mock_geomag(loc):
            return {"quantities": [], "raw": {"declination_deg": 0.5}}

        tool._fetch_usgs_earthquakes = mock_usgs
        tool._fetch_open_meteo = mock_meteo
        tool._fetch_geomag = mock_geomag

        result = await tool.run({"location": SABAH_LOCATION})
        assert result.success is True
        assert result.metadata.get("confidence") is not None

    @pytest.mark.asyncio
    async def test_partial_failure_still_returns_success(self):
        """If one source fails, tool should still return data from others."""
        tool = EarthRealtimeTool()

        async def mock_usgs(loc, radius, limit):
            raise ConnectionError("USGS unreachable")

        async def mock_meteo(loc):
            return {
                "quantities": [],
                "raw": {"temperature_2m_c": 30.0},
            }

        async def mock_geomag(loc):
            return {"quantities": [], "raw": {"declination_deg": 1.0}}

        tool._fetch_usgs_earthquakes = mock_usgs
        tool._fetch_open_meteo = mock_meteo
        tool._fetch_geomag = mock_geomag

        result = await tool.run({"location": SABAH_LOCATION})
        assert result.success is True
        assert len(result.raw_output.get("warnings", [])) >= 1
        # Degraded confidence when a source fails
        assert result.metadata.get("confidence", 1.0) < 0.90

    @pytest.mark.asyncio
    async def test_summary_string_always_contains_coordinates(self):
        tool = EarthRealtimeTool()
        raw = {
            "earthquakes": {"count": 3, "largest_magnitude": 3.5, "events": []},
            "climate": {"temperature_2m_c": 27.0, "surface_pressure_hpa": 1008.0},
            "geomagnetic": {"declination_deg": 0.9},
        }
        summary = tool._build_summary(raw, SABAH_LOCATION, 300.0)
        assert "5.979" in summary
        assert "116.073" in summary
        assert "DITEMPA" in summary


class TestToolRegistration:
    def test_earth_realtime_in_default_registry(self):
        from arifos.geox.geox_tools import ToolRegistry
        registry = ToolRegistry.default_registry()
        assert "EarthRealtimeTool" in registry.list_tools()

    def test_macrostrat_still_in_registry(self):
        from arifos.geox.geox_tools import ToolRegistry
        registry = ToolRegistry.default_registry()
        assert "MacrostratTool" in registry.list_tools()
