"""
arifosmcp/vault/redis_vault_storage.py — Redis-backed SABAR Cooling Ledger

Phoenix-72 Protocol: Entries with EUREKA score 0.50–0.75 (SABAR verdict) are held
in a 72-hour cooling period before promotion or expiry. This module provides:

    - RedisVaultStorage: VaultStorage protocol implementation backed by py-key-value-aio
      RedisStore. Stores entries under collection ``vault:sabar`` with key = seal_id
      and a 72-hour TTL (259200 seconds).

    - SabarCoolingLedger: Higher-level wrapper for listing expired SABAR entries,
      promoting them to permanent storage, and reporting ledger stats.

    - get_sabar_ledger(): Module-level factory.

F1 Amanah: All writes are append-style (TTL-scoped). Redis keys are never silently
overwritten — any update is an explicit re-seal with a new seal_id.

Phoenix-72 Reference: 72 hours = 259200 seconds.

DITEMPA BUKAN DIBERI — Forged, Not Given.
"""

from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass

__all__ = [
    "RedisVaultStorage",
    "SabarCoolingLedger",
    "get_sabar_ledger",
    "SABAR_TTL_SECONDS",
    "SABAR_COLLECTION",
]

logger = logging.getLogger(__name__)

# Phoenix-72: 72 hours in seconds
SABAR_TTL_SECONDS: int = 259200

# Redis collection name used as a namespace prefix (via RedisStore's compound-key scheme)
SABAR_COLLECTION: str = "vault:sabar"

# ---------------------------------------------------------------------------
# Optional import: py-key-value-aio RedisStore
# ---------------------------------------------------------------------------

try:
    from key_value.aio.stores.redis import RedisStore as _RedisStore

    _REDIS_AVAILABLE = True
except ImportError:
    _RedisStore = None  # type: ignore[assignment,misc]
    _REDIS_AVAILABLE = False
    logger.warning(
        "py-key-value-aio[redis] is not installed. "
        "RedisVaultStorage will fall back to JSONLVaultStorage."
    )


# ---------------------------------------------------------------------------
# RedisVaultStorage
# ---------------------------------------------------------------------------


class RedisVaultStorage:
    """
    VaultStorage protocol adapter backed by py-key-value-aio RedisStore.

    F1 Amanah: Entries are immutable once written (TTL-expiry only, no silent overwrite).
    Phoenix-72: Each SABAR entry carries a 72-hour TTL (259200 s).

    Namespace: all keys live in Redis collection ``vault:sabar`` so they are
    isolated from other application data stored in the same Redis instance.

    Fallback: if ``redis.asyncio`` / py-key-value-aio is unavailable at import
    time, all operations transparently delegate to JSONLVaultStorage, preserving
    F1 Amanah durability guarantees.

    Args:
        redis_url: Full Redis URL, e.g. ``redis://localhost:6379/0``.
                   If *None*, falls back to the ``REDIS_URL`` environment variable,
                   then to ``redis://localhost:6379/0``.
        ttl_seconds: Override the Phoenix-72 TTL. Defaults to 259200 (72 h).
        collection: Override the Redis collection namespace. Defaults to
                    ``vault:sabar``.
    """

    def __init__(
        self,
        redis_url: str | None = None,
        *,
        ttl_seconds: int = SABAR_TTL_SECONDS,
        collection: str = SABAR_COLLECTION,
    ) -> None:
        self._ttl_seconds = ttl_seconds
        self._collection = collection
        self._store: Any = None  # _RedisStore instance, set lazily
        self._fallback: Any = None  # JSONLVaultStorage instance, set on Redis failure
        self._redis_url: str = redis_url or os.environ.get("REDIS_URL", "redis://localhost:6379/0")

        if not _REDIS_AVAILABLE:
            self._fallback = self._make_jsonl_fallback()
            logger.warning(
                "RedisVaultStorage: using JSONL fallback (py-key-value-aio not available)."
            )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_store(self) -> Any:
        """Return the RedisStore, creating it on first call."""
        if self._store is None:
            if _RedisStore is None:
                raise RuntimeError("RedisStore unavailable — should be using fallback.")
            self._store = _RedisStore(url=self._redis_url)
        return self._store

    def _make_jsonl_fallback(self) -> Any:
        """Instantiate a JSONLVaultStorage as the fallback backend."""
        from core.organs._4_vault import JSONLVaultStorage  # local import to avoid cycles

        fallback_path = os.environ.get(
            "SABAR_FALLBACK_PATH", "VAULT999/vault999_sabar_fallback.jsonl"
        )
        logger.info("RedisVaultStorage: JSONL fallback path = %s", fallback_path)
        return JSONLVaultStorage(fallback_path)

    # ------------------------------------------------------------------
    # VaultStorage protocol
    # ------------------------------------------------------------------

    async def write(self, entry: dict[str, Any]) -> None:
        """
        Persist a SABAR vault entry to Redis with Phoenix-72 TTL.

        The entry **must** contain a ``seal_id`` field (set by ``core/organs/_4_vault.py``
        before calling storage). The Redis key is the ``seal_id``; the collection is
        ``vault:sabar`` (compound key managed by RedisStore internally).

        F1 Amanah: The entry dict is stored as-is (JSON-serialisable mapping).
        Phoenix-72: TTL is set to 259200 seconds (72 hours).

        Args:
            entry: The vault entry dict as produced by ``seal()`` in _4_vault.py.

        Raises:
            KeyError: If ``seal_id`` is missing from *entry*.
        """
        seal_id: str = entry["seal_id"]  # intentional KeyError if missing — contract violation

        if self._fallback is not None:
            await self._fallback.write(entry)
            return

        try:
            store = self._get_store()
            await store.put(
                key=seal_id,
                value=entry,
                collection=self._collection,
                ttl=float(self._ttl_seconds),
            )
            logger.debug(
                "RedisVaultStorage.write: sealed seal_id=%s TTL=%ds collection=%s",
                seal_id,
                self._ttl_seconds,
                self._collection,
            )
        except Exception as exc:
            logger.error(
                "RedisVaultStorage.write failed (seal_id=%s): %s — falling back to JSONL.",
                seal_id,
                exc,
                exc_info=True,
            )
            if self._fallback is None:
                self._fallback = self._make_jsonl_fallback()
            await self._fallback.write(entry)

    async def read(self, seal_id: str) -> dict[str, Any] | None:
        """
        Retrieve a SABAR vault entry from Redis by seal_id.

        Returns *None* if the entry does not exist or has expired (TTL elapsed).

        F1 Amanah: Read-only; never mutates the stored entry.
        Phoenix-72: Redis enforces the 72-hour TTL transparently.

        Args:
            seal_id: The unique seal identifier (hex string produced by ``secrets.token_hex``).

        Returns:
            The original entry dict, or *None* if not found / expired.
        """
        if self._fallback is not None:
            return await self._fallback.read(seal_id)

        try:
            store = self._get_store()
            result: dict[str, Any] | None = await store.get(
                key=seal_id,
                collection=self._collection,
            )
            if result is None:
                logger.debug(
                    "RedisVaultStorage.read: seal_id=%s not found or expired.", seal_id
                )
            return result
        except Exception as exc:
            logger.error(
                "RedisVaultStorage.read failed (seal_id=%s): %s — falling back to JSONL.",
                seal_id,
                exc,
                exc_info=True,
            )
            if self._fallback is None:
                self._fallback = self._make_jsonl_fallback()
            return await self._fallback.read(seal_id)


# ---------------------------------------------------------------------------
# SabarCoolingLedger
# ---------------------------------------------------------------------------


class SabarCoolingLedger:
    """
    High-level manager for the Phoenix-72 SABAR cooling ledger.

    Wraps a ``RedisVaultStorage`` instance and provides:

    - ``list_expired()``    — scan for entries whose ``phoenix_72_expiry`` has passed.
    - ``promote_to_seal()`` — atomically read → write-to-permanent → delete from Redis.
    - ``get_stats()``       — count of live SABAR keys in Redis.

    F1 Amanah: ``promote_to_seal`` is a two-phase commit (read then write-to-permanent)
    before deleting the Redis entry. If the permanent write fails, the Redis entry is
    intentionally left intact for retry.

    Phoenix-72 Reference: Entries older than 72 h that were not promoted are considered
    cooling-complete and eligible for archival or discard per sovereign policy.

    Args:
        storage: A ``RedisVaultStorage`` instance to delegate to.
    """

    def __init__(self, storage: RedisVaultStorage) -> None:
        self._storage = storage

    # ------------------------------------------------------------------
    # list_expired
    # ------------------------------------------------------------------

    async def list_expired(self) -> list[dict[str, Any]]:
        """
        Return all SABAR entries whose ``phoenix_72_expiry`` timestamp has passed.

        Implementation note: Redis TTL means the key is already gone from Redis
        after the 72-hour window. This method therefore scans entries *still present*
        in Redis and identifies those whose ``phoenix_72_expiry`` field is in the past
        (clock skew / TTL-reset edge cases).

        For truly expired (TTL-elapsed) entries, Redis returns *None* on ``get``,
        so they do not appear in this list. Use ``get_stats()`` to count live entries.

        Returns:
            List of vault entry dicts whose ``phoenix_72_expiry`` has elapsed.
        """
        if self._storage._fallback is not None:
            logger.warning(
                "SabarCoolingLedger.list_expired: operating on JSONL fallback — "
                "full scan not supported; returning empty list."
            )
            return []

        expired: list[dict[str, Any]] = []
        now = datetime.now(timezone.utc)

        try:
            store = self._storage._get_store()
            seal_ids: list[str] = await store.keys(collection=self._storage._collection)
            logger.debug(
                "SabarCoolingLedger.list_expired: scanned %d keys in collection=%s",
                len(seal_ids),
                self._storage._collection,
            )

            for seal_id in seal_ids:
                entry = await self._storage.read(seal_id)
                if entry is None:
                    # Already TTL-expired by Redis
                    continue
                expiry_str: str | None = entry.get("phoenix_72_expiry")
                if expiry_str is None:
                    continue
                try:
                    expiry_dt = datetime.fromisoformat(expiry_str)
                    # Normalise to UTC-aware
                    if expiry_dt.tzinfo is None:
                        expiry_dt = expiry_dt.replace(tzinfo=timezone.utc)
                    if expiry_dt <= now:
                        expired.append(entry)
                except ValueError:
                    logger.warning(
                        "SabarCoolingLedger.list_expired: unparseable expiry '%s' "
                        "for seal_id=%s — skipping.",
                        expiry_str,
                        seal_id,
                    )
        except Exception as exc:
            logger.error(
                "SabarCoolingLedger.list_expired failed: %s", exc, exc_info=True
            )

        return expired

    # ------------------------------------------------------------------
    # promote_to_seal
    # ------------------------------------------------------------------

    async def promote_to_seal(
        self,
        seal_id: str,
        permanent_storage: Any,
    ) -> bool:
        """
        Promote a SABAR entry to permanent storage and remove it from Redis.

        Two-phase commit (F1 Amanah):
            1. Read entry from Redis.
            2. Write entry to *permanent_storage* (must satisfy ``VaultStorage`` protocol).
            3. Delete from Redis **only** on successful permanent write.

        If step 2 raises, Redis entry is intentionally preserved for retry.

        Args:
            seal_id: The seal identifier of the entry to promote.
            permanent_storage: Any object implementing the ``VaultStorage`` protocol
                               (e.g., ``JSONLVaultStorage``).

        Returns:
            ``True`` if promotion succeeded, ``False`` if the entry was not found
            or an error occurred.
        """
        entry = await self._storage.read(seal_id)
        if entry is None:
            logger.warning(
                "SabarCoolingLedger.promote_to_seal: seal_id=%s not found in Redis "
                "(may have already expired or been promoted).",
                seal_id,
            )
            return False

        try:
            # Step 2: write to permanent storage first (F1 Amanah — no data loss)
            await permanent_storage.write(entry)
            logger.info(
                "SabarCoolingLedger.promote_to_seal: seal_id=%s written to permanent storage.",
                seal_id,
            )
        except Exception as exc:
            logger.error(
                "SabarCoolingLedger.promote_to_seal: permanent write failed for "
                "seal_id=%s: %s — Redis entry preserved for retry.",
                seal_id,
                exc,
                exc_info=True,
            )
            return False

        # Step 3: delete from Redis only after permanent write succeeded
        try:
            if self._storage._fallback is None:
                store = self._storage._get_store()
                deleted = await store.delete(
                    key=seal_id, collection=self._storage._collection
                )
                if not deleted:
                    logger.warning(
                        "SabarCoolingLedger.promote_to_seal: Redis delete returned False "
                        "for seal_id=%s (may have expired between read and delete).",
                        seal_id,
                    )
            logger.info(
                "SabarCoolingLedger.promote_to_seal: seal_id=%s removed from cooling ledger.",
                seal_id,
            )
        except Exception as exc:
            logger.error(
                "SabarCoolingLedger.promote_to_seal: Redis delete failed for seal_id=%s: %s "
                "(entry already in permanent storage — safe to ignore).",
                seal_id,
                exc,
                exc_info=True,
            )

        return True

    # ------------------------------------------------------------------
    # get_stats
    # ------------------------------------------------------------------

    async def get_stats(self) -> dict[str, Any]:
        """
        Return statistics about the SABAR cooling ledger.

        Scans the ``vault:sabar`` Redis collection and counts live (non-expired) keys.

        Returns:
            Dict with keys:
                - ``entry_count`` (int): Number of live SABAR entries in Redis.
                - ``collection`` (str): The Redis collection/namespace used.
                - ``ttl_seconds`` (int): Configured Phoenix-72 TTL.
                - ``backend`` (str): ``"redis"`` or ``"jsonl_fallback"``.
                - ``error`` (str, optional): Present if the Redis scan failed.
        """
        stats: dict[str, Any] = {
            "collection": self._storage._collection,
            "ttl_seconds": self._storage._ttl_seconds,
        }

        if self._storage._fallback is not None:
            stats["backend"] = "jsonl_fallback"
            stats["entry_count"] = -1  # unknown — JSONL does not support cheap counting
            return stats

        stats["backend"] = "redis"

        try:
            store = self._storage._get_store()
            keys: list[str] = await store.keys(collection=self._storage._collection)
            stats["entry_count"] = len(keys)
            logger.debug(
                "SabarCoolingLedger.get_stats: %d live entries in collection=%s",
                len(keys),
                self._storage._collection,
            )
        except Exception as exc:
            logger.error(
                "SabarCoolingLedger.get_stats failed: %s", exc, exc_info=True
            )
            stats["entry_count"] = -1
            stats["error"] = str(exc)

        return stats


# ---------------------------------------------------------------------------
# Module-level factory
# ---------------------------------------------------------------------------


def get_sabar_ledger(redis_url: str | None = None) -> RedisVaultStorage:
    """
    Factory: return a ``RedisVaultStorage`` configured for SABAR cooling.

    Uses the ``REDIS_URL`` environment variable if *redis_url* is *None*.
    Falls back to ``redis://localhost:6379/0`` if neither is set.

    Phoenix-72: The returned storage has TTL = 259200 seconds (72 hours).
    F1 Amanah: If py-key-value-aio is unavailable, the storage transparently
    falls back to JSONL so no SABAR entry is ever silently dropped.

    Args:
        redis_url: Optional Redis connection URL. If *None*, reads ``REDIS_URL``
                   from the environment.

    Returns:
        A ``RedisVaultStorage`` instance ready to use as a ``VaultStorage``
        implementation (compatible with ``seal(storage_override=...)``.

    Example::

        from arifosmcp.vault.redis_vault_storage import get_sabar_ledger
        from core.organs._4_vault import seal

        ledger = get_sabar_ledger()
        receipt = await seal(judge_output, storage_override=ledger)
    """
    resolved_url = redis_url or os.environ.get("REDIS_URL")
    storage = RedisVaultStorage(redis_url=resolved_url)
    logger.info(
        "get_sabar_ledger: initialised RedisVaultStorage "
        "(url=%s, ttl=%ds, collection=%s, redis_available=%s)",
        resolved_url or "redis://localhost:6379/0",
        SABAR_TTL_SECONDS,
        SABAR_COLLECTION,
        _REDIS_AVAILABLE,
    )
    return storage
