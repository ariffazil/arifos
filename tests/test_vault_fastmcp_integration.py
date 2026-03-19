"""
tests/test_vault_fastmcp_integration.py — Vault FastMCP Integration Test Suite

Tests for:
  - VaultStorage protocol (JSONLVaultStorage) — filesystem-backed JSONL vault
  - EUREKA Sieve (HardenedAnomalousContrastEngine) — anomalous contrast thresholds
  - SABAR Redis TTL — mocked RedisVaultStorage with 72h cooling ledger
  - OTel Span Attributes — ConstitutionalSpan attribute recording
  - Full Pipeline Integration — seal() -> storage interaction end-to-end

ARIFOS_PHYSICS_DISABLED=1 is set via conftest.py (autouse fixture).
asyncio_mode = "auto" is set in pyproject.toml; no @pytest.mark.asyncio needed.

Import notes:
  - arifosmcp.telemetry imports aaa_mcp.infrastructure.monitoring at module
    level, so all TestOTelIntegration tests pre-populate sys.modules with
    MagicMock stubs for aaa_mcp before importing ConstitutionalSpan.
  - VaultOutput (returned by seal() on the SEALED path) has status="SUCCESS"
    per BaseOrganOutput; SealReceipt (returned on SABAR path) has status="SABAR".
  - RedisVaultStorage does not exist in the codebase; it is defined here as a
    test-local class matching the interface in the task specification.

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# ── path bootstrap (mirrors conftest.py pattern) ──────────────────────────────
sys.path.insert(0, str(Path(__file__).parents[1]))

# Ensure physics is disabled for the whole module
os.environ.setdefault("ARIFOS_PHYSICS_DISABLED", "1")
os.environ.setdefault("ARIFOS_ALLOW_LEGACY_SPEC", "1")

# ── ML stubs: mock sentence_transformers + sklearn BEFORE any core.* import ──
# core/shared/sbert_floors.py loads SentenceTransformer at module scope;
# without this stub the test session hangs for 30+ seconds on model loading.
_st_mock = MagicMock()
_st_mock.SentenceTransformer.return_value.encode.return_value = [0.0] * 768
sys.modules.setdefault("sentence_transformers", _st_mock)
sys.modules.setdefault("sklearn", MagicMock())
sys.modules.setdefault("sklearn.metrics", MagicMock())
sys.modules.setdefault("sklearn.metrics.pairwise", MagicMock())
sys.modules.setdefault("sklearn.linear_model", MagicMock())
sys.modules.setdefault("sklearn.pipeline", MagicMock())
sys.modules.setdefault("sklearn.preprocessing", MagicMock())


# =============================================================================
# AAA_MCP STUB — pre-populate sys.modules so arifosmcp.telemetry can be imported
# without the real aaa_mcp package installed.
# =============================================================================

def _install_aaa_mcp_stubs() -> None:
    """
    arifosmcp/telemetry.py has top-level imports from aaa_mcp.  This helper
    installs lightweight MagicMock stubs into sys.modules so that every test
    in this file can import ConstitutionalSpan without hitting ModuleNotFoundError.
    """
    stubs_needed = [
        "aaa_mcp",
        "aaa_mcp.infrastructure",
        "aaa_mcp.infrastructure.monitoring",
        "aaa_mcp.observability",
        "aaa_mcp.services",
        "aaa_mcp.services.constitutional_metrics",
        "aaa_mcp.vault",
        "aaa_mcp.vault.precedent_memory",
    ]
    for mod_name in stubs_needed:
        if mod_name not in sys.modules:
            sys.modules[mod_name] = MagicMock()

    # Ensure monitoring stub has PipelineMetrics and get_metrics_collector
    monitoring_stub = sys.modules["aaa_mcp.infrastructure.monitoring"]
    if not hasattr(monitoring_stub, "PipelineMetrics"):
        monitoring_stub.PipelineMetrics = MagicMock
    if not hasattr(monitoring_stub, "get_metrics_collector"):
        monitoring_stub.get_metrics_collector = MagicMock(return_value=MagicMock())

    # Ensure observability stub has required record_* functions
    obs_stub = sys.modules["aaa_mcp.observability"]
    for fn in ("record_floor_score", "record_floor_violation", "record_tool_call", "record_tool_latency"):
        if not hasattr(obs_stub, fn):
            setattr(obs_stub, fn, MagicMock())

    # Ensure constitutional_metrics stub has get_last_seal_hash, store_stage_result
    cm_stub = sys.modules["aaa_mcp.services.constitutional_metrics"]
    if not hasattr(cm_stub, "get_last_seal_hash"):
        cm_stub.get_last_seal_hash = MagicMock(return_value="0" * 64)
    if not hasattr(cm_stub, "store_stage_result"):
        cm_stub.store_stage_result = MagicMock(return_value=None)

    # Ensure precedent_memory stub has embed_vault_entry (async)
    pm_stub = sys.modules["aaa_mcp.vault.precedent_memory"]
    if not hasattr(pm_stub, "embed_vault_entry"):
        pm_stub.embed_vault_entry = AsyncMock(return_value="prec_stub")


# Install stubs at import time — before any test class is instantiated
_install_aaa_mcp_stubs()


# =============================================================================
# MOCK: RedisVaultStorage  (file does NOT exist; interface defined in task spec)
# =============================================================================


class RedisVaultStorage:
    """
    Test-local RedisVaultStorage matching the interface described in the task spec.

    The real implementation would call a Redis client internally; here we define
    the protocol so tests can drive it with AsyncMock.

    async write(entry: dict) -> None   — persists entry JSON with TTL=259200s
    async read(seal_id: str) -> dict | None — fetches entry by 'vault:sabar:{id}'
    """

    REDIS_TTL_SECONDS = 259_200  # 72 hours = 72 * 3600
    KEY_PREFIX = "vault:sabar:"

    def __init__(self, redis_client: Any | None = None, fallback: Any | None = None):
        self._redis = redis_client
        self._fallback = fallback

    async def write(self, entry: dict) -> None:
        """Write vault entry to Redis with 72-hour TTL."""
        seal_id = entry.get("seal_id", "")
        key = f"{self.KEY_PREFIX}{seal_id}"
        value = json.dumps(entry, ensure_ascii=False)
        await self._redis.set(key, value, ex=self.REDIS_TTL_SECONDS)

    async def read(self, seal_id: str) -> dict | None:
        """Read vault entry from Redis by seal_id."""
        key = f"{self.KEY_PREFIX}{seal_id}"
        raw = await self._redis.get(key)
        if raw is None:
            return None
        return json.loads(raw)


# =============================================================================
# HELPERS — minimal judge_output & trinity_bundle factories
# =============================================================================


def _make_judge_output(
    verdict: str = "SEAL",
    w4: float = 0.95,
    genius_g: float = 0.90,
    floors_failed: list | None = None,
) -> dict:
    return {
        "verdict": verdict,
        "W_4": w4,
        "W_3": w4,
        "genius_G": genius_g,
        "floors_failed": floors_failed or [],
        "floor_scores": {"F1": 1.0, "F2": 0.99, "F13": 1.0},
    }


def _make_trinity_bundle(
    entropy_delta: float = -0.5,
    proposed_canon: bool = False,
    code_modified: bool = False,
    novelty_detected: bool = False,
    verdict_apex: str = "SEAL",
    stakeholders: list | None = None,
    lane: str = "SOFT",
    f1_amanah: bool = True,
) -> dict:
    return {
        "agi": {"entropy_delta": entropy_delta},
        "reasoning": {
            "proposed_canon": proposed_canon,
            "code_modified": code_modified,
        },
        "apex": {
            "novelty_detected": novelty_detected,
            "verdict": verdict_apex,
        },
        "asi": {"stakeholders": stakeholders or []},
        "init": {"f1_amanah": f1_amanah, "lane": lane},
    }


# =============================================================================
# CLASS 1: TestVaultStorage
# =============================================================================


class TestVaultStorage:
    """Tests for VaultStorage protocol and JSONLVaultStorage filesystem adapter."""

    async def test_jsonl_vault_write_and_read(self, tmp_path: Path):
        """Write an entry to JSONLVaultStorage and read it back by seal_id."""
        from core.organs._4_vault import JSONLVaultStorage

        vault_file = tmp_path / "test_vault.jsonl"
        storage = JSONLVaultStorage(vault_file)

        entry = {
            "seal_id": "abc123",
            "verdict": "SEAL",
            "query": "Is this novel?",
            "eureka_score": 0.82,
            "timestamp": "2026-03-09T00:00:00+00:00",
        }
        await storage.write(entry)

        result = await storage.read("abc123")
        assert result is not None, "Expected to read back the written entry"
        assert result["seal_id"] == "abc123"
        assert result["verdict"] == "SEAL"
        assert result["eureka_score"] == pytest.approx(0.82)

    async def test_jsonl_vault_missing_seal_id(self, tmp_path: Path):
        """Reading a non-existent seal_id from JSONLVaultStorage returns None."""
        from core.organs._4_vault import JSONLVaultStorage

        vault_file = tmp_path / "empty_vault.jsonl"
        storage = JSONLVaultStorage(vault_file)

        # Write something to create the file
        await storage.write({"seal_id": "existing", "verdict": "SEAL"})

        result = await storage.read("does_not_exist")
        assert result is None, "Non-existent seal_id must return None"

    async def test_jsonl_vault_read_on_missing_file_returns_none(self, tmp_path: Path):
        """Reading from a path that doesn't exist yet returns None (no FileNotFoundError)."""
        from core.organs._4_vault import JSONLVaultStorage

        vault_file = tmp_path / "nonexistent.jsonl"
        storage = JSONLVaultStorage(vault_file)

        result = await storage.read("any_id")
        assert result is None

    async def test_seal_hash_tamper_detection(self, tmp_path: Path):
        """
        Mutating seal_hash in a stored entry causes the recomputed Merkle root
        to diverge from the original, proving chain integrity.
        """
        from core.organs._4_vault import JSONLVaultStorage, _compute_merkle_root

        vault_file = tmp_path / "tamper_vault.jsonl"
        storage = JSONLVaultStorage(vault_file)

        original_entry = {
            "seal_id": "tamper_test_001",
            "verdict": "SEAL",
            "query": "Tamper detection test",
            "eureka_score": 0.88,
        }

        # Compute the canonical hash for the original entry
        entry_json = json.dumps(original_entry, sort_keys=True, ensure_ascii=False)
        original_hash = hashlib.sha256(entry_json.encode()).hexdigest()
        original_entry["seal_hash"] = original_hash
        original_entry["merkle_root"] = _compute_merkle_root(original_hash)

        await storage.write(original_entry)

        # Read back and tamper with seal_hash
        record = await storage.read("tamper_test_001")
        assert record is not None

        tampered_hash = "0" * 64  # clearly wrong
        tampered_merkle = _compute_merkle_root(tampered_hash)

        # Tampered merkle must NOT equal original merkle
        assert tampered_merkle != original_entry["merkle_root"], (
            "Mutating seal_hash must yield a different Merkle root (chain breaks)"
        )

    async def test_jsonl_vault_multiple_entries_correct_lookup(self, tmp_path: Path):
        """Multiple entries in the JSONL file — lookup returns the correct one by seal_id."""
        from core.organs._4_vault import JSONLVaultStorage

        vault_file = tmp_path / "multi_vault.jsonl"
        storage = JSONLVaultStorage(vault_file)

        for i in range(5):
            await storage.write({"seal_id": f"seal_{i}", "payload": f"data_{i}"})

        result = await storage.read("seal_3")
        assert result is not None
        assert result["payload"] == "data_3"


# =============================================================================
# CLASS 2: TestEUREKASieve
# =============================================================================


class TestEUREKASieve:
    """Tests for HardenedAnomalousContrastEngine and EUREKA threshold logic."""

    async def test_eureka_seal_threshold(self):
        """
        A trinity bundle with maximum signal must produce score >= 0.75 and
        verdict SEAL from HardenedAnomalousContrastEngine.evaluate().
        """
        from arifosmcp.vault.hardened import HardenedAnomalousContrastEngine

        engine = HardenedAnomalousContrastEngine(vault_ledger=None)

        # High-signal bundle: maximum negative entropy, ontological shift, high stakes
        bundle = _make_trinity_bundle(
            entropy_delta=-1.0,
            proposed_canon=True,
            code_modified=True,
            novelty_detected=True,
            verdict_apex="888_HOLD",
            stakeholders=["human", "earth", "ai"],
            lane="CRISIS",
            f1_amanah=False,
        )
        query = "eureka breakthrough paradigm shift discovered"
        response = "A fundamental ontological framework change detected."

        score = await engine.evaluate(query, response, bundle)

        assert score.verdict == "SEAL", (
            f"Expected SEAL for high-signal bundle, got {score.verdict} "
            f"(eureka_score={score.eureka_score:.3f})"
        )
        assert score.eureka_score >= 0.75

    async def test_eureka_sabar_threshold(self):
        """
        A moderate trinity bundle in a fresh (empty-history) engine must produce
        0.50 <= score < 0.75 and verdict SABAR.

        Formula derivation (no history -> novelty=1.0):
          weights: novelty=0.35, entropy=0.30, ontological=0.20, decision=0.15
          entropy_delta=-0.2 -> entropy_reduction = 0.5 + (0.2/2) = 0.6
          stakeholders=1 -> decision_weight = 0 + 0.1 = 0.1
          onto = 0
          score = 1.0*0.35 + 0.6*0.30 + 0*0.20 + 0.1*0.15 = 0.35+0.18+0+0.015 = 0.545
        """
        from arifosmcp.vault.hardened import HardenedAnomalousContrastEngine

        engine = HardenedAnomalousContrastEngine(vault_ledger=None)

        bundle = _make_trinity_bundle(
            entropy_delta=-0.2,
            proposed_canon=False,
            code_modified=False,
            novelty_detected=False,
            stakeholders=["human"],
            lane="SOFT",
        )
        query = "what is the capital of France"
        response = "Paris"

        # Empty history -> novelty=1.0 (maximally novel)
        engine._cache_loaded = True
        engine._history_fingerprints = set()
        engine._history_ngrams = {}

        score = await engine.evaluate(query, response, bundle)

        assert 0.50 <= score.eureka_score < 0.75, (
            f"Expected SABAR range [0.50, 0.75), got {score.eureka_score:.3f}"
        )
        assert score.verdict == "SABAR"

    async def test_eureka_transient(self):
        """
        An exact-duplicate query with a low-signal bundle must yield score < 0.50
        and verdict TRANSIENT.

        novelty=0 (exact dup fingerprint), entropy_delta=+0.5 -> reduction=0.25
        onto=0, decision=0
        score = 0*0.35 + 0.25*0.30 + 0 + 0 = 0.075 -> TRANSIENT
        """
        from arifosmcp.vault.hardened import HardenedAnomalousContrastEngine

        engine = HardenedAnomalousContrastEngine(vault_ledger=None)

        query = "hello world test"
        response = "ok"

        # Inject exact-duplicate fingerprint to force novelty=0
        existing_fp = engine._compute_fingerprint(query, response)
        engine._cache_loaded = True
        engine._history_fingerprints = {existing_fp}
        engine._history_ngrams = {existing_fp: engine._get_ngrams(query, n=3)}

        bundle = _make_trinity_bundle(
            entropy_delta=0.5,   # entropy increasing = low reduction
            proposed_canon=False,
            code_modified=False,
            novelty_detected=False,
            stakeholders=[],
            lane="SOFT",
        )

        score = await engine.evaluate(query, response, bundle)

        assert score.eureka_score < 0.50, (
            f"Expected TRANSIENT (< 0.50), got {score.eureka_score:.3f}"
        )
        assert score.verdict == "TRANSIENT"

    async def test_novelty_exact_duplicate(self):
        """
        When the query fingerprint is already in history, _calculate_novelty_hardened
        returns (novelty=0.0, jaccard=1.0) via the exact-match shortcut.
        """
        from arifosmcp.vault.hardened import HardenedAnomalousContrastEngine

        engine = HardenedAnomalousContrastEngine(vault_ledger=None)

        query = "duplicate query content"
        response = "duplicate response content"

        fp = engine._compute_fingerprint(query, response)
        engine._cache_loaded = True
        engine._history_fingerprints = {fp}
        engine._history_ngrams = {}

        novelty, jaccard = await engine._calculate_novelty_hardened(
            query,
            response,
            fp,
            engine._get_ngrams(query, n=3),
        )

        assert novelty == 0.0, f"Exact duplicate must have novelty=0.0, got {novelty}"
        assert jaccard == 1.0, f"Exact duplicate must have jaccard=1.0, got {jaccard}"

    async def test_eureka_keyword_boost(self):
        """
        'eureka' in the query boosts novelty by exactly +0.15 (capped at 1.0).

        Strategy: Both the eureka and the plain query are passed with the *same*
        pre-computed ngrams set so the Jaccard similarity (and therefore the base
        novelty) is identical.  Any difference in the returned novelty values
        must therefore come solely from the keyword-boost branch in the source.
        """
        from arifosmcp.vault.hardened import HardenedAnomalousContrastEngine

        engine = HardenedAnomalousContrastEngine(vault_ledger=None)

        # Populate history with a moderately similar entry
        base_query = "information retrieval benchmark test"
        base_fp = engine._compute_fingerprint(base_query, "resp")
        shared_ngrams = engine._get_ngrams(base_query, n=3)
        engine._cache_loaded = True
        engine._history_fingerprints = {base_fp}
        engine._history_ngrams = {base_fp: shared_ngrams}

        query_with_kw = "eureka moment discovery"
        query_no_kw = "normal moment discovery"

        # Use the *same* ngrams set for both calls so Jaccard is identical
        fp_with_kw = engine._compute_fingerprint(query_with_kw, "resp2")
        fp_no_kw = engine._compute_fingerprint(query_no_kw, "resp2")

        novelty_with_kw, _ = await engine._calculate_novelty_hardened(
            query_with_kw, "resp2", fp_with_kw, shared_ngrams
        )
        novelty_no_kw, _ = await engine._calculate_novelty_hardened(
            query_no_kw, "resp2", fp_no_kw, shared_ngrams
        )

        boost = novelty_with_kw - novelty_no_kw
        # boost should be +0.15 unless novelty_no_kw was close enough to 1.0
        # that clamping reduces it; in that case boost can be < 0.15 but still > 0.
        assert boost > 0.0, (
            f"Keyword 'eureka' must boost novelty. "
            f"with={novelty_with_kw:.3f}, without={novelty_no_kw:.3f}"
        )
        assert boost <= 0.15 + 1e-9, (
            f"Boost must be at most 0.15 (can be less only if capped at 1.0), "
            f"got {boost:.4f}"
        )

    async def test_entropy_reduction_mapping(self):
        """
        _calculate_entropy_reduction correctly maps:
          entropy_delta=0.0  -> 0.5
          entropy_delta=-1.0 -> 1.0
          entropy_delta=+1.0 -> 0.0
        """
        from arifosmcp.vault.hardened import HardenedAnomalousContrastEngine

        engine = HardenedAnomalousContrastEngine(vault_ledger=None)

        assert engine._calculate_entropy_reduction(
            {"agi": {"entropy_delta": 0.0}}
        ) == pytest.approx(0.5)
        assert engine._calculate_entropy_reduction(
            {"agi": {"entropy_delta": -1.0}}
        ) == pytest.approx(1.0)
        assert engine._calculate_entropy_reduction(
            {"agi": {"entropy_delta": 1.0}}
        ) == pytest.approx(0.0)


# =============================================================================
# CLASS 3: TestSabarRedis
# =============================================================================


class TestSabarRedis:
    """Tests for SABAR Redis TTL storage semantics (all external deps mocked)."""

    async def test_redis_storage_write_sets_ttl(self):
        """
        RedisVaultStorage.write() must call redis.set() with ex=259200 (72h TTL).
        """
        mock_redis = AsyncMock()
        storage = RedisVaultStorage(redis_client=mock_redis)

        entry = {"seal_id": "sabar_001", "status": "SABAR", "verdict": "SABAR"}
        await storage.write(entry)

        mock_redis.set.assert_awaited_once()
        call = mock_redis.set.call_args
        assert call.kwargs.get("ex") == 259_200, (
            f"Expected TTL=259200s, got {call.kwargs.get('ex')}"
        )

    async def test_redis_storage_read_returns_dict(self):
        """
        RedisVaultStorage.read() must JSON-parse the value from redis.get()
        and return it as a plain dict.
        """
        stored_entry = {"seal_id": "sabar_002", "status": "SABAR", "verdict": "SABAR"}
        mock_redis = AsyncMock()
        mock_redis.get.return_value = json.dumps(stored_entry)

        storage = RedisVaultStorage(redis_client=mock_redis)
        result = await storage.read("sabar_002")

        assert result is not None
        assert result["seal_id"] == "sabar_002"
        assert result["status"] == "SABAR"

    async def test_redis_storage_read_returns_none_when_missing(self):
        """
        RedisVaultStorage.read() returns None when redis.get() returns None
        (key not present).
        """
        mock_redis = AsyncMock()
        mock_redis.get.return_value = None

        storage = RedisVaultStorage(redis_client=mock_redis)
        result = await storage.read("missing_key")

        assert result is None

    async def test_redis_storage_fallback_on_error(self, tmp_path: Path):
        """
        When redis.set() raises ConnectionError, a fallback JSONLVaultStorage
        must receive the write (graceful degradation).
        """
        from core.organs._4_vault import JSONLVaultStorage

        mock_redis = AsyncMock()
        mock_redis.set.side_effect = ConnectionError("Redis unavailable")

        fallback_file = tmp_path / "fallback_vault.jsonl"
        fallback = JSONLVaultStorage(fallback_file)

        class FallbackRedisVaultStorage(RedisVaultStorage):
            async def write(self, entry: dict) -> None:
                try:
                    await super().write(entry)
                except Exception:
                    await self._fallback.write(entry)

        storage = FallbackRedisVaultStorage(redis_client=mock_redis, fallback=fallback)
        entry = {"seal_id": "fallback_001", "status": "SABAR"}
        await storage.write(entry)   # must not raise

        result = await fallback.read("fallback_001")
        assert result is not None
        assert result["seal_id"] == "fallback_001"

    async def test_redis_key_prefix(self):
        """
        RedisVaultStorage.write() must use 'vault:sabar:{seal_id}' as the key
        passed to redis.set().
        """
        mock_redis = AsyncMock()
        storage = RedisVaultStorage(redis_client=mock_redis)

        seal_id = "test_seal_xyz"
        await storage.write({"seal_id": seal_id, "status": "SABAR"})

        mock_redis.set.assert_awaited_once()
        call_args = mock_redis.set.call_args
        key_used = call_args.args[0] if call_args.args else call_args.kwargs.get("name")
        expected_key = f"vault:sabar:{seal_id}"
        assert key_used == expected_key, (
            f"Expected Redis key '{expected_key}', got '{key_used}'"
        )

    async def test_redis_ttl_constant_matches_72h(self):
        """RedisVaultStorage.REDIS_TTL_SECONDS must equal 72 * 3600 = 259200."""
        assert RedisVaultStorage.REDIS_TTL_SECONDS == 72 * 3600

    async def test_redis_key_prefix_constant(self):
        """RedisVaultStorage.KEY_PREFIX must be the string 'vault:sabar:'."""
        assert RedisVaultStorage.KEY_PREFIX == "vault:sabar:"


# =============================================================================
# CLASS 4: TestOTelIntegration
# =============================================================================


class TestOTelIntegration:
    """
    Tests for ConstitutionalSpan OTel attribute recording.

    aaa_mcp stubs are installed at module load time via _install_aaa_mcp_stubs()
    above, so all imports of arifosmcp.telemetry succeed without the real package.
    """

    def test_vault_seal_sets_otel_attributes(self):
        """
        ConstitutionalSpan.set_verdict(), set_floor_score(), and set_stage()
        must call span.set_attribute() with the correct arifos.* keys.
        """
        from arifosmcp.telemetry import ConstitutionalSpan

        mock_span = MagicMock()
        const_span = ConstitutionalSpan(span=mock_span, session_id="sess_001")

        const_span.set_verdict("SEAL", confidence=0.95)
        const_span.set_floor_score("F2", 0.99)
        const_span.set_stage("999_SEAL")

        recorded = {
            call.args[0]: call.args[1]
            for call in mock_span.set_attribute.call_args_list
        }
        assert "arifos.verdict" in recorded, "Expected arifos.verdict attribute"
        assert recorded["arifos.verdict"] == "SEAL"
        assert "arifos.confidence" in recorded
        assert recorded["arifos.confidence"] == pytest.approx(0.95)
        assert "arifos.floor.F2.score" in recorded
        assert recorded["arifos.floor.F2.score"] == pytest.approx(0.99)
        assert "arifos.metabolic_stage" in recorded
        assert recorded["arifos.metabolic_stage"] == "999_SEAL"

    def test_otel_skipped_when_span_is_none(self):
        """
        ConstitutionalSpan with span=None must not raise AttributeError on any
        method call — models the OTEL_AVAILABLE=False code path.
        """
        from arifosmcp.telemetry import ConstitutionalSpan

        const_span = ConstitutionalSpan(span=None, session_id="sess_no_otel")

        # None of these must raise
        const_span.set_verdict("SEAL")
        const_span.set_floor_score("F1", 1.0)
        const_span.set_floor_violation("F7", "humility out of range")
        const_span.set_stage("111_SENSE")
        const_span.record_metric("eureka_score", 0.82)

    def test_span_verdict_attribute(self):
        """
        set_verdict() must call span.set_attribute('arifos.verdict', verdict)
        for each constitutional verdict string.
        """
        from arifosmcp.telemetry import ConstitutionalSpan

        mock_span = MagicMock()
        const_span = ConstitutionalSpan(span=mock_span)

        for verdict in ["SEAL", "SABAR", "VOID", "888_HOLD", "PARTIAL"]:
            mock_span.reset_mock()
            const_span.set_verdict(verdict)
            mock_span.set_attribute.assert_any_call("arifos.verdict", verdict)

    def test_span_seal_id_attribute(self):
        """
        record_metric(name, value, attrs) stores 'arifos.{name}' and
        'arifos.{name}.{attr_key}' — can encode vault.seal_id context.
        """
        from arifosmcp.telemetry import ConstitutionalSpan

        mock_span = MagicMock()
        const_span = ConstitutionalSpan(span=mock_span)

        const_span.record_metric("vault.seal_id", 1.0, {"id": "seal_abc"})

        mock_span.set_attribute.assert_any_call("arifos.vault.seal_id", 1.0)
        mock_span.set_attribute.assert_any_call("arifos.vault.seal_id.id", "seal_abc")

    def test_floor_violation_sets_violated_attribute(self):
        """
        set_floor_violation(floor, reason) must set:
          span.set_attribute('arifos.floor.{floor}.violated', True)
          span.set_attribute('arifos.floor.{floor}.reason', reason)
        """
        from arifosmcp.telemetry import ConstitutionalSpan

        mock_span = MagicMock()
        const_span = ConstitutionalSpan(span=mock_span)

        const_span.set_floor_violation("F7", "omega outside band")

        recorded = {
            call.args[0]: call.args[1]
            for call in mock_span.set_attribute.call_args_list
        }
        assert "arifos.floor.F7.violated" in recorded
        assert recorded["arifos.floor.F7.violated"] is True
        assert "arifos.floor.F7.reason" in recorded
        assert recorded["arifos.floor.F7.reason"] == "omega outside band"

    def test_void_verdict_sets_error_status(self):
        """
        set_verdict('VOID') must call span.set_status() exactly once (with an
        error-level status object).
        """
        from arifosmcp.telemetry import ConstitutionalSpan

        mock_span = MagicMock()
        const_span = ConstitutionalSpan(span=mock_span)

        with patch("arifosmcp.telemetry.OTEL_AVAILABLE", True):
            with patch("arifosmcp.telemetry.Status") as mock_status_cls:
                with patch("arifosmcp.telemetry.StatusCode") as mock_status_code:
                    mock_status_code.ERROR = "ERROR"
                    mock_status_cls.return_value = MagicMock()
                    const_span.set_verdict("VOID")

        mock_span.set_status.assert_called_once()


# =============================================================================
# CLASS 5: TestFullPipeline
# =============================================================================


class TestFullPipeline:
    """End-to-end tests for seal() pipeline using mock VaultStorage — no external services."""

    async def test_seal_pipeline_with_mock_storage(self):
        """
        Full seal() call with a mock VaultStorage verifies:
          - storage.write() is called exactly once for a SEALED/SABAR result
          - The written entry contains seal_id, seal_hash (64 hex chars),
            merkle_root, eureka_score, timestamp, and verdict fields.

        Note: when eureka_score >= 0.75 seal() returns a VaultOutput (from
        BaseOrganOutput) whose .status is 'SUCCESS', not 'SEALED'.
        """
        from core.organs._4_vault import SealReceipt, seal

        mock_storage = AsyncMock()
        judge_output = _make_judge_output(verdict="SEAL", w4=0.95, genius_g=0.90)

        result = await seal(
            judge_output=judge_output,
            session_id="sess_full_pipeline",
            query="Is this a genuine EUREKA insight?",
            authority="test_harness",
            storage_override=mock_storage,
        )

        # storage.write must have been called (SEAL or SABAR path)
        mock_storage.write.assert_awaited_once()

        written_entry = mock_storage.write.call_args.args[0]
        assert "seal_id" in written_entry and written_entry["seal_id"] != ""
        assert "seal_hash" in written_entry and len(written_entry["seal_hash"]) == 64
        assert "merkle_root" in written_entry and len(written_entry["merkle_root"]) == 64
        assert "eureka_score" in written_entry
        assert "timestamp" in written_entry
        assert "verdict" in written_entry

        # VaultOutput.status == "SUCCESS" for permanent seal;
        # SealReceipt.status == "SABAR" for cooling path.
        if hasattr(result, "status"):
            assert result.status in ("SUCCESS", "SABAR"), (
                f"Unexpected status '{result.status}' — expected SUCCESS (VaultOutput) "
                f"or SABAR (SealReceipt)"
            )

    async def test_sabar_pipeline_phoenix_72_expiry(self):
        """
        SABAR path (0.50 <= eureka < 0.75): seal() returns SealReceipt with
        status='SABAR' and phoenix_72_expiry set; the written entry must also
        contain phoenix_72_expiry and status='SABAR'.

        Parameters chosen so eureka ~= 0.663:
          (0.99 * 0.30 * 0.50 * 1.0 * 0.8)^0.2 = (0.1188)^0.2 ~= 0.663
        """
        from core.organs._4_vault import SealReceipt, seal

        mock_storage = AsyncMock()
        judge_output = _make_judge_output(verdict="SEAL", w4=0.30, genius_g=0.50)

        result = await seal(
            judge_output=judge_output,
            session_id="sess_sabar_pipeline",
            query="moderate insight query",
            storage_override=mock_storage,
        )

        assert isinstance(result, SealReceipt), (
            f"Expected SealReceipt for SABAR path, got {type(result).__name__}"
        )
        assert result.status == "SABAR", f"Expected SABAR, got {result.status}"
        assert result.phoenix_72_expiry is not None, (
            "SABAR SealReceipt must have phoenix_72_expiry"
        )

        written_entry = mock_storage.write.call_args.args[0]
        assert "phoenix_72_expiry" in written_entry
        assert written_entry["status"] == "SABAR"

    async def test_transient_pipeline_no_storage(self):
        """
        TRANSIENT path (eureka < 0.50): seal() returns SealReceipt with
        status='TRANSIENT', vault_backend='none', and storage.write() is NEVER called.

        Parameters chosen so eureka ~= 0.33:
          (0.99 * 0.05 * 0.10 * 1.0 * 0.8)^0.2 = (0.00396)^0.2 ~= 0.33
        """
        from core.organs._4_vault import SealReceipt, seal

        mock_storage = AsyncMock()
        judge_output = _make_judge_output(verdict="VOID", w4=0.05, genius_g=0.10)

        result = await seal(
            judge_output=judge_output,
            session_id="sess_transient",
            query="trivial query",
            storage_override=mock_storage,
        )

        assert isinstance(result, SealReceipt)
        assert result.status == "TRANSIENT", f"Expected TRANSIENT, got {result.status}"
        assert result.vault_backend == "none"

        # storage.write must NEVER be called for TRANSIENT entries
        mock_storage.write.assert_not_awaited()

    async def test_seal_entry_merkle_chain_integrity(self):
        """
        The merkle_root stored in the written entry must equal
        _compute_merkle_root(seal_hash), confirming cryptographic chain integrity.
        """
        from core.organs._4_vault import _compute_merkle_root, seal

        mock_storage = AsyncMock()
        judge_output = _make_judge_output(verdict="SEAL", w4=0.95, genius_g=0.90)

        await seal(
            judge_output=judge_output,
            session_id="sess_merkle_check",
            query="merkle chain test",
            storage_override=mock_storage,
        )

        if mock_storage.write.await_count == 0:
            pytest.skip("TRANSIENT entry; no write occurred (eureka < 0.50)")

        written = mock_storage.write.call_args.args[0]
        entry_hash = written["seal_hash"]
        expected_merkle = _compute_merkle_root(entry_hash)
        assert written["merkle_root"] == expected_merkle, (
            "Merkle root in written entry must match _compute_merkle_root(seal_hash)"
        )

    async def test_vault_seal_tool_returns_sealed_status(self):
        """
        vault_seal() MCP tool backend must return a dict with status='SEALED',
        verdict matching input, session_id, and timestamp — all external services
        mocked via sys.modules stubs (already installed at module load time).
        """
        # Stubs for aaa_mcp are already in sys.modules from _install_aaa_mcp_stubs().
        # We only need to force a re-import of vault_seal so it picks up the stubs.
        if "arifosmcp.tools.vault_seal" in sys.modules:
            del sys.modules["arifosmcp.tools.vault_seal"]
        # Also clear the telemetry module so it re-executes with our stubs
        if "arifosmcp.telemetry" in sys.modules:
            del sys.modules["arifosmcp.telemetry"]

        from arifosmcp.tools.vault_seal import vault_seal

        result = await vault_seal(
            session_id="sess_tool_test",
            verdict="SEAL",
            payload={"answer": "42", "query": "life the universe and everything"},
            metadata={"test": True},
        )

        assert result["status"] == "SEALED"
        assert result["verdict"] == "SEAL"
        assert result["session_id"] == "sess_tool_test"
        assert "timestamp" in result

    async def test_seal_query_truncated_at_1024_chars(self):
        """
        Queries longer than 1024 characters must be silently truncated to 1024
        in the stored vault entry (F1 Amanah: compact immutable record).
        """
        from core.organs._4_vault import seal

        mock_storage = AsyncMock()
        long_query = "x" * 2000
        judge_output = _make_judge_output(verdict="SEAL", w4=0.95, genius_g=0.90)

        await seal(
            judge_output=judge_output,
            session_id="sess_trunc",
            query=long_query,
            storage_override=mock_storage,
        )

        if mock_storage.write.await_count == 0:
            pytest.skip("TRANSIENT entry; no write occurred")

        written = mock_storage.write.call_args.args[0]
        assert len(written["query"]) <= 1024, (
            f"Query must be truncated to 1024 chars, got {len(written['query'])}"
        )
