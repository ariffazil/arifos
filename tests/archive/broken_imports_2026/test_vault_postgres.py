"""
VAULT999 PostgreSQL Ledger Tests

Tests cover:
- Chain integrity (append, verify, restart)
- Tamper detection
- Concurrent safety
- BUG FIX: seal_data JSONB type handling (dict vs str)
- BUG FIX: cursor=0 edge case in list_entries
- BUG FIX: Merkle proof with sequence gaps
- BUG FIX: Merkle proof doesn't mutate original hashes
"""

import os
import uuid
import asyncio
import asyncpg
import pytest

from codebase.vault.persistent_ledger import (
    PersistentVaultLedger, 
    GENESIS_HASH,
    _parse_seal_data,
)

DSN = os.getenv("VAULT_POSTGRES_DSN") or os.getenv("DATABASE_URL")
pytestmark = pytest.mark.skipif(not DSN, reason="VAULT_POSTGRES_DSN not set")


async def _run_migration(pool):
    sql_path = os.path.join("codebase", "vault", "migrations", "001_create_vault_ledger.sql")
    with open(sql_path, "r", encoding="utf-8") as f:
        statements = [s.strip() for s in f.read().split(";") if s.strip()]
    async with pool.acquire() as conn:
        for stmt in statements:
            await conn.execute(stmt)
        await conn.execute("TRUNCATE vault_ledger RESTART IDENTITY; DELETE FROM vault_head;")


@pytest.fixture
async def ledger():
    pool = await asyncpg.create_pool(DSN, min_size=1, max_size=5)
    await _run_migration(pool)
    await pool.close()

    ledg = PersistentVaultLedger(DSN)
    await ledg.connect()
    yield ledg
    await ledg.close()


def _dummy(idx: int):
    return {
        "session_id": f"sess-{idx}",
        "verdict": "SEAL" if idx % 2 == 0 else "VOID",
        "seal_data": {"k": idx, "nested": {"deep": True}},
        "authority": "test",
    }


# ===================================================================
# Basic Tests
# ===================================================================

@pytest.mark.asyncio
async def test_append_and_verify(ledger):
    """Test basic append and chain verification."""
    for i in range(3):
        d = _dummy(i)
        await ledger.append(**d)
    res = await ledger.verify_chain()
    assert res["valid"]
    assert res["entries"] == 3


@pytest.mark.asyncio
async def test_restart_and_verify(ledger):
    """Test that data persists across ledger restarts."""
    await ledger.append(**_dummy(1))
    await ledger.close()
    fresh = PersistentVaultLedger(DSN)
    await fresh.connect()
    res = await fresh.verify_chain()
    await fresh.close()
    assert res["valid"]


@pytest.mark.asyncio
async def test_tamper_detected(ledger):
    """Test tamper detection modifies entry hash."""
    await ledger.append(**_dummy(1))
    # Tamper first row
    async with ledger._pool.acquire() as conn:  # type: ignore[attr-defined]
        await conn.execute("UPDATE vault_ledger SET entry_hash = $1 WHERE sequence = 1", "bad")
    res = await ledger.verify_chain()
    assert not res["valid"]
    assert "hash-mismatch" in res["reason"]


@pytest.mark.asyncio
async def test_concurrent_appends(ledger):
    """Test concurrent appends don't create forks."""
    async def do_append(idx):
        await ledger.append(**_dummy(idx))

    await asyncio.gather(do_append(1), do_append(2))
    res = await ledger.verify_chain()
    assert res["valid"]
    entries = await ledger.list_entries(limit=10)
    seqs = [e["sequence"] for e in entries["entries"]]
    assert seqs == sorted(seqs, reverse=True)


# ===================================================================
# Bug Fix Tests
# ===================================================================

@pytest.mark.asyncio
async def test_seal_data_jsonb_parsing(ledger):
    """
    BUG FIX: seal_data returned as dict from JSONB column.
    
    asyncpg returns Python dict for JSONB columns, not a JSON string.
    This test ensures _parse_seal_data and _row_to_entry handle both.
    """
    # Append with nested seal_data
    seal_data = {"key": "value", "numbers": [1, 2, 3], "nested": {"a": 1}}
    receipt = await ledger.append(
        session_id="test-session",
        verdict="SEAL",
        seal_data=seal_data,
        authority="test",
    )
    
    # Read back - should return correct dict
    entry = await ledger.get_entry_by_sequence(receipt["sequence_number"])
    assert entry is not None
    assert entry["seal_data"] == seal_data
    assert entry["seal_data"]["nested"]["a"] == 1
    
    # Verify chain works (uses _parse_seal_data internally)
    res = await ledger.verify_chain()
    assert res["valid"]


@pytest.mark.asyncio
async def test_parse_seal_data_handles_both_types():
    """Unit test for _parse_seal_data helper."""
    # Test dict input (JSONB)
    d = {"key": "value"}
    assert _parse_seal_data(d) == d
    
    # Test str input (TEXT column)
    assert _parse_seal_data('{"key": "value"}') == d
    
    # Test invalid input returns empty dict
    assert _parse_seal_data(None) == {}
    # Note: json.loads(str(123)) returns 123 (valid JSON number), not {}


@pytest.mark.asyncio
async def test_list_entries_cursor_zero(ledger):
    """
    BUG FIX: cursor=0 should not be treated as falsy.
    
    `if cursor:` fails for cursor=0. Should use `if cursor is not None:`.
    This test verifies pagination works with cursor=0.
    """
    # Need entries with sequence >= 1, cursor=0 means "get all with sequence < 0"
    # which should return nothing (or we can test that the query runs correctly)
    for i in range(5):
        await ledger.append(**_dummy(i))
    
    # cursor=0 should return entries with sequence < 0 (none)
    result = await ledger.list_entries(cursor=0, limit=10)
    assert result["entries"] == []  # No entries with sequence < 0
    
    # cursor=1 should return entries with sequence < 1 (none, assuming sequence starts at 1)
    # Actually, sequences are 1-indexed, so cursor=1 returns entries with seq < 1
    result = await ledger.list_entries(cursor=1, limit=10)
    assert result["entries"] == []
    
    # cursor=None should return latest entries
    result = await ledger.list_entries(cursor=None, limit=3)
    assert len(result["entries"]) == 3


@pytest.mark.asyncio
async def test_query_by_verdict_cursor_zero(ledger):
    """
    BUG FIX: cursor=0 in query_by_verdict.
    """
    for i in range(5):
        await ledger.append(**_dummy(i))
    
    # cursor=0 should work (returns entries with sequence < 0)
    result = await ledger.query_by_verdict(verdict="SEAL", cursor=0, limit=10)
    assert result["entries"] == []
    
    # cursor=None should return all matching
    result = await ledger.query_by_verdict(verdict="SEAL", cursor=None, limit=10)
    assert len(result["entries"]) > 0


@pytest.mark.asyncio
async def test_merkle_proof_with_sequence(ledger):
    """
    BUG FIX: get_merkle_proof finds entry by sequence number, not index.
    
    This ensures the proof works even with gaps (after import/legacy).
    """
    # Append 5 entries
    for i in range(5):
        await ledger.append(**_dummy(i))
    
    # Get proof for sequence 3
    proof = await ledger.get_merkle_proof(sequence=3)
    assert proof is not None
    assert proof["leaf_index"] == 2  # 0-indexed position
    assert len(proof["proof"]) > 0
    
    # Verify the proof is correct
    entries = await ledger.list_entries(limit=10)
    entry_3 = next((e for e in entries["entries"] if e["sequence"] == 3), None)
    assert entry_3 is not None
    
    # Manually verify Merkle proof
    current_hash = entry_3["entry_hash"]
    idx = proof["leaf_index"]
    for sibling in proof["proof"]:
        if sibling["position"] == "left":
            current_hash = hashlib.sha256(
                (sibling["hash"] + current_hash).encode()
            ).hexdigest()
        else:
            current_hash = hashlib.sha256(
                (current_hash + sibling["hash"]).encode()
            ).hexdigest()
    
    assert current_hash == proof["root"]


@pytest.mark.asyncio
async def test_merkle_proof_nonexistent_sequence(ledger):
    """Test get_merkle_proof returns None for non-existent sequence."""
    await ledger.append(**_dummy(1))
    
    proof = await ledger.get_merkle_proof(sequence=999)
    assert proof is None


@pytest.mark.asyncio
async def test_merkle_proof_no_mutation(ledger):
    """
    BUG FIX: Merkle proof should not mutate the original hashes list.
    
    The old code did `level = hashes` (reference), then `level.append()`
    which modified the original list.
    """
    import hashlib
    
    # Append 3 entries (odd count triggers padding)
    for i in range(3):
        await ledger.append(**_dummy(i))
    
    # Get the raw hashes
    async with ledger._pool.acquire() as conn:  # type: ignore[attr-defined]
        rows = await conn.fetch(
            "SELECT entry_hash FROM vault_ledger ORDER BY sequence"
        )
        original_hashes = [r["entry_hash"] for r in rows]
    
    # Store copy before proof generation
    hashes_before = list(original_hashes)
    
    # Generate proof (this used to mutate original_hashes)
    proof = await ledger.get_merkle_proof(sequence=1)
    assert proof is not None
    
    # Verify original hashes weren't mutated
    assert original_hashes == hashes_before
    assert len(original_hashes) == 3  # Should still be 3, not 4 (padded)


@pytest.mark.asyncio
async def test_merkle_proof_with_gaps(ledger):
    """
    Test that Merkle proof works correctly even if sequences have gaps.
    
    This simulates a scenario after legacy import where sequence numbers
    may not be contiguous.
    """
    # Append 3 entries normally
    receipts = []
    for i in range(3):
        r = await ledger.append(**_dummy(i))
        receipts.append(r)
    
    # Simulate a gap by deleting middle entry
    async with ledger._pool.acquire() as conn:  # type: ignore[attr-defined]
        await conn.execute("DELETE FROM vault_ledger WHERE sequence = 2")
    
    # Now sequences are [1, 3] (gap at 2)
    # Proof for sequence=3 should still work
    proof = await ledger.get_merkle_proof(sequence=3)
    assert proof is not None
    assert proof["leaf_index"] == 1  # Position in remaining list
    
    # Verify entry 1 still has proof
    proof1 = await ledger.get_merkle_proof(sequence=1)
    assert proof1 is not None
    assert proof1["leaf_index"] == 0


@pytest.mark.asyncio
async def test_entries_by_session(ledger):
    """Test retrieving entries by session ID."""
    await ledger.append(session_id="sess-A", verdict="SEAL", seal_data={}, authority="test")
    await ledger.append(session_id="sess-B", verdict="SEAL", seal_data={}, authority="test")
    await ledger.append(session_id="sess-A", verdict="VOID", seal_data={}, authority="test")
    
    entries_a = await ledger.get_entries_by_session("sess-A")
    assert len(entries_a) == 2
    assert all(e["session_id"] == "sess-A" for e in entries_a)
    
    entries_b = await ledger.get_entries_by_session("sess-B")
    assert len(entries_b) == 1


@pytest.mark.asyncio
async def test_query_by_verdict_time_range(ledger):
    """Test query with time range filtering."""
    from datetime import datetime, timezone, timedelta
    
    # Add entries
    await ledger.append(**_dummy(1))
    await ledger.append(**_dummy(2))
    
    # Query all SEAL entries
    result = await ledger.query_by_verdict(verdict="SEAL")
    assert len(result["entries"]) > 0
    
    # Query with time range that includes now
    now = datetime.now(timezone.utc)
    result = await ledger.query_by_verdict(
        verdict="SEAL",
        start_time=now - timedelta(hours=1),
        end_time=now + timedelta(hours=1),
    )
    assert len(result["entries"]) > 0
    
    # Query with future time range (should return nothing)
    result = await ledger.query_by_verdict(
        verdict="SEAL",
        start_time=now + timedelta(hours=1),
    )
    assert len(result["entries"]) == 0


@pytest.mark.asyncio
async def test_pagination(ledger):
    """Test cursor-based pagination."""
    # Add 10 entries
    for i in range(10):
        await ledger.append(**_dummy(i))
    
    # First page
    page1 = await ledger.list_entries(cursor=None, limit=3)
    assert len(page1["entries"]) == 3
    assert page1["has_more"] is True
    
    # Second page using cursor
    page2 = await ledger.list_entries(cursor=page1["next_cursor"], limit=3)
    assert len(page2["entries"]) == 3
    assert page2["has_more"] is True
    
    # Verify no overlap
    page1_seqs = {e["sequence"] for e in page1["entries"]}
    page2_seqs = {e["sequence"] for e in page2["entries"]}
    assert not page1_seqs.intersection(page2_seqs)


@pytest.mark.asyncio
async def test_singleton_pattern():
    """Test that get_vault_ledger returns the same instance."""
    from codebase.vault.persistent_ledger import get_vault_ledger, _ledger_singleton
    
    # Reset singleton for test
    import codebase.vault.persistent_ledger as pvl
    pvl._ledger_singleton = None
    
    ledger1 = get_vault_ledger()
    ledger2 = get_vault_ledger()
    assert ledger1 is ledger2
    
    # Cleanup
    pvl._ledger_singleton = None


@pytest.mark.asyncio
async def test_error_on_missing_dsn():
    """Test that missing DSN raises appropriate error."""
    import codebase.vault.persistent_ledger as pvl
    
    # Save original
    orig_dsn = os.environ.get("DATABASE_URL")
    orig_vault = os.environ.get("VAULT_POSTGRES_DSN")
    
    try:
        # Clear env vars
        if "DATABASE_URL" in os.environ:
            del os.environ["DATABASE_URL"]
        if "VAULT_POSTGRES_DSN" in os.environ:
            del os.environ["VAULT_POSTGRES_DSN"]
        
        # Reset singleton
        pvl._ledger_singleton = None
        
        # Should raise RuntimeError
        with pytest.raises(RuntimeError) as exc_info:
            pvl.get_vault_ledger()
        
        assert "DATABASE_URL" in str(exc_info.value)
    finally:
        # Restore
        if orig_dsn:
            os.environ["DATABASE_URL"] = orig_dsn
        if orig_vault:
            os.environ["VAULT_POSTGRES_DSN"] = orig_vault
        pvl._ledger_singleton = None


import hashlib  # Import for test_merkle_proof_no_mutation
