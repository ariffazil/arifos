from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest

from arifos.geox.geox_hardened import HardenedGeoxAgent
from arifos.geox.geox_memory import DualMemoryStore, GeoMemoryEntry, GeoMemoryStore
from arifos.geox.geox_schemas import CoordinatePoint
from arifos.geox.geox_validator import GeoXValidator


def test_geo_memory_entry_round_trip_preserves_datetime_fields():
    now = datetime.now(timezone.utc).replace(microsecond=0)
    entry = GeoMemoryEntry(
        entry_id="GEO-MEM-1",
        prospect_name="Lead A",
        basin="Malay Basin",
        insight_text="Reservoir quality remains moderate.",
        verdict="SEAL",
        confidence=0.82,
        timestamp=now,
        last_accessed=now,
        ttl_expiry=now + timedelta(days=1),
    )

    restored = GeoMemoryEntry.from_dict(entry.to_dict())

    assert restored.entry_id == entry.entry_id
    assert restored.timestamp == entry.timestamp
    assert restored.last_accessed == entry.last_accessed
    assert restored.ttl_expiry == entry.ttl_expiry


@pytest.mark.asyncio
async def test_memory_forget_tombstones_entry_and_retrieve_skips_it(
    geo_request, mock_agent
):
    response = await mock_agent.evaluate_prospect(geo_request)
    memory: GeoMemoryStore = mock_agent.memory_store  # type: ignore[assignment]

    entry_id = await memory.store(response, geo_request)
    assert await memory.forget(entry_id) is True

    results = await memory.retrieve("Blok Selatan", basin="Malay Basin")
    assert results == []


@pytest.mark.asyncio
async def test_memory_retrieve_skips_quarantined_entries():
    memory = GeoMemoryStore()
    entry = GeoMemoryEntry(
        entry_id="GEO-MEM-Q1",
        prospect_name="Lead Q",
        basin="Malay Basin",
        insight_text="Adequate length insight text.",
        verdict="PARTIAL",
        confidence=0.5,
        timestamp=datetime.now(timezone.utc),
        metadata={
            "location": {"latitude": 4.5, "longitude": 103.7, "depth_m": 2000.0},
        },
        is_quarantined=True,
    )
    memory._store[entry.entry_id] = entry

    results = await memory.retrieve("Lead Q", basin="Malay Basin")

    assert results == []


@pytest.mark.asyncio
async def test_memory_export_jsonl_writes_current_entries(tmp_path, geo_request, mock_agent):
    response = await mock_agent.evaluate_prospect(geo_request)
    memory: GeoMemoryStore = mock_agent.memory_store  # type: ignore[assignment]
    await memory.store(response, geo_request)

    export_path = tmp_path / "memory.jsonl"
    memory.export_jsonl(str(export_path))

    payload = [json.loads(line) for line in export_path.read_text(encoding="utf-8").splitlines()]
    assert len(payload) == 1
    assert payload[0]["basin"] == "Malay Basin"


@pytest.mark.asyncio
async def test_qdrant_upsert_falls_back_to_in_memory_on_exception():
    class BrokenQdrant:
        def upsert(self, **_: object) -> None:
            raise RuntimeError("boom")

    memory = GeoMemoryStore(qdrant_client=BrokenQdrant())
    entry = GeoMemoryEntry(
        entry_id="GEO-MEM-Q",
        prospect_name="Lead Q",
        basin="Malay Basin",
        insight_text="Valid geological insight text.",
        verdict="SEAL",
        confidence=0.8,
        timestamp=datetime.now(timezone.utc),
        embedding_vector=[0.1, 0.2, 0.3],
    )

    await memory._qdrant_upsert(entry)

    assert memory.count() == 1
    assert memory._store["GEO-MEM-Q"].prospect_name == "Lead Q"


@pytest.mark.asyncio
async def test_dual_memory_store_query_dual_uses_local_fallback_when_no_macrostrat():
    store = DualMemoryStore(macrostrat_tool=None, cache_dir="/tmp/geox-memory-cache-test")
    result = await store.query_dual(
        location=CoordinatePoint(latitude=4.5, longitude=103.7),
        query_text="prospect context",
        top_k=2,
    )

    assert result["ok"] is True
    assert isinstance(result["discrete"], list)
    assert result["continuous"][0]["source"] == "LocalVectorStore"
    assert result["governance"]["status"] in {"SEALED", "PARTIAL"}


def test_public_validator_accepts_non_none_and_rejects_none():
    validator = GeoXValidator(strict_mode=True)

    supported = validator.validate({"prospect": "Lead A"})
    contradicted = validator.validate(None)

    assert supported.verdict == "supported"
    assert contradicted.verdict == "contradicted"
    assert contradicted.floor_violations == ["F2_truth"]


@pytest.mark.asyncio
async def test_hardened_agent_process_and_history():
    agent = HardenedGeoxAgent(session_id="sess-1")

    valid = await agent.process({"prospect": "Lead A"})
    invalid = await agent.process(None)

    assert valid["verdict"] == "SEAL"
    assert invalid["verdict"] == "VOID"
    assert len(agent.get_history()) == 1
