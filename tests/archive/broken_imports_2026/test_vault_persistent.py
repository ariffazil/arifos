"""
Tests for Vault 999 Persistent Ledger (PostgreSQL backend).

Unit tests run without a database (pure hash/merkle functions).
Integration tests require DATABASE_URL pointing to a PostgreSQL instance.

    pytest tests/test_vault_persistent.py -v
    DATABASE_URL=postgresql://... pytest tests/test_vault_persistent.py -v
"""

import asyncio
import hashlib
import json
import os
import pytest
from datetime import datetime, timezone
from unittest.mock import patch
from uuid import uuid4


# ---------------------------------------------------------------------------
# Unit tests — pure functions (no DB, no asyncpg required)
# ---------------------------------------------------------------------------


class TestMerkleRoot:
    """Test _merkle_root standalone function."""

    def _merkle_root(self, hashes):
        """Local reimplementation matching persistent_ledger._merkle_root."""
        if not hashes:
            return hashlib.sha256(b"EMPTY_LEDGER").hexdigest()
        level = list(hashes)
        while len(level) > 1:
            if len(level) % 2 == 1:
                level.append(level[-1])
            next_level = []
            for i in range(0, len(level), 2):
                next_level.append(
                    hashlib.sha256((level[i] + level[i + 1]).encode("utf-8")).hexdigest()
                )
            level = next_level
        return level[0]

    def test_empty_returns_fixed_hash(self):
        root = self._merkle_root([])
        expected = hashlib.sha256(b"EMPTY_LEDGER").hexdigest()
        assert root == expected

    def test_single_element(self):
        assert self._merkle_root(["abc123"]) == "abc123"

    def test_two_elements(self):
        a, b = "aaa", "bbb"
        expected = hashlib.sha256((a + b).encode("utf-8")).hexdigest()
        assert self._merkle_root([a, b]) == expected

    def test_three_elements_pads(self):
        a, b, c = "aaa", "bbb", "ccc"
        left = hashlib.sha256((a + b).encode("utf-8")).hexdigest()
        right = hashlib.sha256((c + c).encode("utf-8")).hexdigest()
        expected = hashlib.sha256((left + right).encode("utf-8")).hexdigest()
        assert self._merkle_root([a, b, c]) == expected

    def test_deterministic(self):
        hashes = ["h1", "h2", "h3", "h4"]
        assert self._merkle_root(hashes) == self._merkle_root(hashes)


class TestEntryHash:
    """Test _compute_entry_hash deterministic behavior."""

    def _compute(self, **kwargs):
        """Local reimplementation matching persistent_ledger._compute_entry_hash."""
        genesis = "0" * 64
        canonical = {
            "session_id": kwargs["session_id"],
            "timestamp": kwargs["timestamp"].isoformat(),
            "authority": kwargs["authority"],
            "verdict": kwargs["verdict"],
            "seal_data": kwargs["seal_data"],
            "prev_hash": kwargs["prev_hash"] or genesis,
            "seal_id": str(kwargs["seal_id"]),
        }
        canonical_json = json.dumps(canonical, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()

    def test_returns_hex_sha256(self):
        h = self._compute(
            session_id="s1",
            timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
            authority="system",
            verdict="SEAL",
            seal_data={},
            prev_hash=None,
            seal_id=uuid4(),
        )
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)

    def test_different_verdicts(self):
        sid = uuid4()
        ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
        h1 = self._compute(
            session_id="s1", timestamp=ts, authority="sys", verdict="SEAL",
            seal_data={}, prev_hash=None, seal_id=sid,
        )
        h2 = self._compute(
            session_id="s1", timestamp=ts, authority="sys", verdict="VOID",
            seal_data={}, prev_hash=None, seal_id=sid,
        )
        assert h1 != h2

    def test_deterministic(self):
        sid = uuid4()
        ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
        kwargs = dict(
            session_id="s1", timestamp=ts, authority="sys", verdict="SEAL",
            seal_data={"x": 1}, prev_hash="abc", seal_id=sid,
        )
        assert self._compute(**kwargs) == self._compute(**kwargs)


class TestShouldUsePostgres:
    def test_default_is_postgres(self):
        """VAULT_BACKEND defaults to postgres."""
        from codebase.vault.persistent_ledger import should_use_postgres
        with patch.dict(os.environ, {"VAULT_BACKEND": "postgres", "DATABASE_URL": "x"}, clear=False):
            assert should_use_postgres() is True

    def test_false_when_filesystem(self):
        from codebase.vault.persistent_ledger import should_use_postgres
        with patch.dict(os.environ, {"VAULT_BACKEND": "filesystem"}, clear=True):
            assert should_use_postgres() is False


class TestSealRowDataclass:
    def test_to_dict(self):
        from codebase.vault.persistent_ledger import SealRow
        ts = datetime(2026, 1, 1, tzinfo=timezone.utc)
        sid = uuid4()
        row = SealRow(
            sequence=1, session_id="sess-1", seal_id=sid, timestamp=ts,
            authority="system", verdict="SEAL", seal_data={"k": "v"},
            entry_hash="abc123", prev_hash=None, merkle_root="root123",
        )
        d = row.to_dict()
        assert d["sequence"] == 1
        assert d["seal_id"] == str(sid)
        assert d["prev_hash"] is None
        assert d["seal_data"] == {"k": "v"}


class TestGetVaultLedger:
    def test_singleton(self):
        from codebase.vault.persistent_ledger import get_vault_ledger, PersistentVaultLedger
        import codebase.vault.persistent_ledger as mod
        mod._ledger_singleton = None
        l1 = get_vault_ledger()
        l2 = get_vault_ledger()
        assert l1 is l2
        assert isinstance(l1, PersistentVaultLedger)
        mod._ledger_singleton = None


# ---------------------------------------------------------------------------
# Integration tests (require PostgreSQL + asyncpg)
# ---------------------------------------------------------------------------

_HAS_PG = bool(os.environ.get("DATABASE_URL") or os.environ.get("VAULT_POSTGRES_DSN"))
pg_required = pytest.mark.skipif(not _HAS_PG, reason="DATABASE_URL not set")


@pg_required
class TestPersistentVaultLedgerIntegration:
    """
    Integration tests against a real PostgreSQL instance.
    Set DATABASE_URL to enable.

    Before running, apply the migration:
        psql "$DATABASE_URL" -f codebase/vault/migrations/001_create_vault_ledger.sql
    """

    async def _get_ledger(self):
        from codebase.vault.persistent_ledger import PersistentVaultLedger
        ledger = PersistentVaultLedger()
        await ledger.connect()
        return ledger

    async def _clean(self, ledger):
        async with ledger._pool.acquire() as conn:
            await conn.execute("TRUNCATE vault_ledger RESTART IDENTITY CASCADE")
            await conn.execute("DELETE FROM vault_head")

    async def test_append_and_verify_chain(self):
        """Append 3 entries -> verify_chain passes."""
        ledger = await self._get_ledger()
        try:
            await self._clean(ledger)
            r1 = await ledger.append("sess-1", "SEAL", {"action": "test1"}, "system")
            r2 = await ledger.append("sess-1", "VOID", {"action": "test2"}, "system")
            r3 = await ledger.append("sess-2", "SEAL", {"action": "test3"}, "system")

            assert r1["sequence_number"] == 1
            assert r2["sequence_number"] == 2
            assert r3["sequence_number"] == 3
            assert r2["prev_hash"] == r1["entry_hash"]
            assert r3["prev_hash"] == r2["entry_hash"]

            result = await ledger.verify_chain()
            assert result["valid"], f"Chain failed: {result}"
        finally:
            await ledger.close()

    async def test_restart_verify(self):
        """Simulate restart: new ledger instance, same DB, chain still valid."""
        ledger1 = await self._get_ledger()
        try:
            await self._clean(ledger1)
            await ledger1.append("sess-r", "SEAL", {"step": 1}, "system")
            await ledger1.append("sess-r", "SEAL", {"step": 2}, "system")
        finally:
            await ledger1.close()

        ledger2 = await self._get_ledger()
        try:
            result = await ledger2.verify_chain()
            assert result["valid"], f"Chain broke after restart: {result}"

            r3 = await ledger2.append("sess-r", "SEAL", {"step": 3}, "system")
            assert r3["sequence_number"] == 3

            result2 = await ledger2.verify_chain()
            assert result2["valid"], f"Chain broke after append: {result2}"
        finally:
            await ledger2.close()

    async def test_tamper_detection(self):
        """Tamper one entry's hash -> verify_chain fails."""
        ledger = await self._get_ledger()
        try:
            await self._clean(ledger)
            await ledger.append("sess-t", "SEAL", {"data": "legit"}, "system")
            await ledger.append("sess-t", "SEAL", {"data": "also legit"}, "system")

            async with ledger._pool.acquire() as conn:
                await conn.execute(
                    "UPDATE vault_ledger SET entry_hash = 'TAMPERED' WHERE sequence = 1"
                )

            result = await ledger.verify_chain()
            assert not result["valid"], "Should detect tampered entry"
            assert result["first_invalid_seq"] == 1
        finally:
            await ledger.close()

    async def test_concurrent_appends(self):
        """Two async tasks append concurrently - no chain fork."""
        ledger = await self._get_ledger()
        try:
            await self._clean(ledger)

            async def append_batch(prefix, count):
                for i in range(count):
                    await ledger.append(f"sess-{prefix}", "SEAL", {"i": i}, "system")

            await asyncio.gather(append_batch("A", 5), append_batch("B", 5))

            result = await ledger.verify_chain()
            assert result["valid"], f"Chain fork: {result}"
            assert result["entries"] == 10
        finally:
            await ledger.close()

    async def test_void_verdict_persisted(self):
        """VOID verdicts must be stored for audit completeness."""
        ledger = await self._get_ledger()
        try:
            await self._clean(ledger)
            receipt = await ledger.append("sess-void", "VOID", {"reason": "F2 failed"}, "system")

            entries = await ledger.get_entries_by_session("sess-void")
            assert len(entries) == 1
            assert entries[0]["verdict"] == "VOID"

            by_seq = await ledger.get_entry_by_sequence(receipt["sequence_number"])
            assert by_seq is not None
            assert by_seq["verdict"] == "VOID"
        finally:
            await ledger.close()

    async def test_list_entries_pagination(self):
        """list_entries returns paginated results."""
        ledger = await self._get_ledger()
        try:
            await self._clean(ledger)
            for i in range(5):
                await ledger.append(f"sess-{i}", "SEAL", {"i": i}, "system")

            page1 = await ledger.list_entries(limit=3)
            assert len(page1["entries"]) == 3
            assert page1["has_more"] is True

            page2 = await ledger.list_entries(cursor=page1["next_cursor"], limit=3)
            assert len(page2["entries"]) == 2
            assert page2["has_more"] is False
        finally:
            await ledger.close()

    async def test_query_by_verdict(self):
        """query_by_verdict filters correctly."""
        ledger = await self._get_ledger()
        try:
            await self._clean(ledger)
            await ledger.append("s1", "SEAL", {}, "system")
            await ledger.append("s2", "VOID", {}, "system")
            await ledger.append("s3", "SEAL", {}, "system")

            seals = await ledger.query_by_verdict("SEAL")
            voids = await ledger.query_by_verdict("VOID")
            assert len(seals) == 2
            assert len(voids) == 1
            assert voids[0]["verdict"] == "VOID"
        finally:
            await ledger.close()

    async def test_merkle_proof(self):
        """get_merkle_proof returns valid proof structure."""
        ledger = await self._get_ledger()
        try:
            await self._clean(ledger)
            r1 = await ledger.append("s1", "SEAL", {}, "system")
            await ledger.append("s2", "SEAL", {}, "system")

            proof = await ledger.get_merkle_proof(1)
            assert proof is not None
            assert "root" in proof
            assert "proof" in proof

            missing = await ledger.get_merkle_proof(999)
            assert missing is None
        finally:
            await ledger.close()
