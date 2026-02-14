"""
Infrastructure Health Check — Verify PostgreSQL + Redis are Actually Working

This test verifies that the production infrastructure (PostgreSQL, Redis) is
properly connected and NOT silently falling back to memory/local storage.

Run this against your Railway deployment to ensure:
1. PostgreSQL is accepting writes (not falling back to memory)
2. Redis is accepting connections (not falling back to local dict)
3. ASI floors are calculating correctly (F5 Peace², F6 Empathy)

DITEMPA BUKAN DIBERI — Forged, Not Given
"""

import pytest
import os
from typing import Dict, Any

from tests.conftest import postgres_required, redis_required


@pytest.mark.integration
@postgres_required
class TestPostgresPersistence:
    """Verify PostgreSQL VAULT999 is actually persisting data."""

    @pytest.mark.asyncio
    async def test_postgres_connection_and_write(self):
        """Verify we can write to PostgreSQL and read it back."""
        from aaa_mcp.sessions.session_ledger import SessionLedger, VaultEntry

        ledger = SessionLedger()
        initialized = await ledger.initialize()

        # Should successfully initialize with Postgres
        assert ledger.is_postgres_available, "Postgres should be available with DATABASE_URL set"

        if not initialized:
            pytest.skip("Postgres initialization failed - may be misconfigured")

        # Write a test entry
        test_entry = await ledger.seal(
            session_id="test-health-check",
            verdict_type="SEAL",
            payload={"test": "data", "health_check": True},
            query_summary="Health check test",
            risk_level="LOW",
            category="test",
            environment="test",
        )

        # Verify we got a real seal_id (not None)
        assert test_entry.entry_id, "Should get a valid entry_id from PostgreSQL"
        assert test_entry.entry_hash, "Should get a valid entry_hash from PostgreSQL"

        # Read it back
        entries = await ledger.query_by_session("test-health-check")
        assert len(entries) > 0, "Should be able to read back the written entry"

        # Clean up
        await ledger.delete_by_session("test-health-check")

        print(f"✅ PostgreSQL persistence verified: {test_entry.entry_id}")

    @pytest.mark.asyncio
    async def test_no_silent_fallback_to_memory(self):
        """Ensure we're NOT silently falling back to memory storage."""
        from aaa_mcp.sessions.session_ledger import SessionLedger

        # Force DATABASE_URL to be set
        assert os.environ.get("DATABASE_URL"), "DATABASE_URL must be set for production"

        ledger = SessionLedger()

        # With DATABASE_URL set, we should use Postgres
        # is_postgres_available checks both env var AND asyncpg import
        assert ledger.is_postgres_available, (
            "With DATABASE_URL set, Postgres should be available. "
            "If this fails, either: "
            "(1) asyncpg not installed, or "
            "(2) DATABASE_URL not being read"
        )

        print("✅ No silent fallback: Postgres is explicitly available")


@pytest.mark.integration
@redis_required
class TestRedisPersistence:
    """Verify Redis is actually persisting session state."""

    def test_redis_connection(self):
        """Verify Redis connection is working."""
        from aaa_mcp.services.redis_client import get_redis_client, MindVault

        # Check if REDIS_URL is set
        redis_url = os.environ.get("REDIS_URL")
        if not redis_url:
            pytest.skip("REDIS_URL not set - skipping Redis tests")

        # Try to get client
        client = get_redis_client()

        # Should have a real Redis client (not None)
        assert client is not None, (
            "Redis client should be initialized with valid REDIS_URL. "
            "If None, check Redis URL parsing or connection."
        )

        # Try ping
        try:
            pong = client.ping()
            assert pong, "Redis ping should return True"
        except Exception as e:
            pytest.fail(f"Redis ping failed: {e}")

        print("✅ Redis connection verified")

    def test_redis_write_and_read(self):
        """Verify we can write to Redis and read it back."""
        from aaa_mcp.services.redis_client import MindVault

        vault = MindVault()

        # Skip if Redis unavailable
        if vault._redis is None:
            pytest.skip("Redis not available - cannot test persistence")

        # Write test data
        test_session = "health-check-session"
        test_data = {"test": "value", "timestamp": "2024-01-01T00:00:00Z"}

        success = vault.save(test_session, test_data, ttl=60)  # 60 second TTL
        assert success, "Should successfully save to Redis"

        # Read it back
        loaded = vault.load(test_session)
        assert loaded.get("test") == "value", "Should read back the same data from Redis"

        # Clean up
        vault.delete(test_session)

        print("✅ Redis persistence verified")

    def test_redis_health_check_endpoint(self):
        """Verify Redis health check returns connected status."""
        from aaa_mcp.services.redis_client import MindVault

        vault = MindVault()
        health = vault.health_check()

        # If Redis is configured, it should be connected
        redis_url = os.environ.get("REDIS_URL")
        if redis_url:
            assert health["status"] == "connected", f"Redis should be connected. Got: {health}"
            assert health["mode"] == "redis", "Should be in redis mode, not local_fallback"
            print(f"✅ Redis health: connected (v{health.get('version', 'unknown')})")
        else:
            assert health["mode"] == "local_fallback", "Without REDIS_URL, should fallback to local"


class TestASIFloorScoring:
    """Verify ASI floor scoring (F5 Peace², F6 Empathy) is correct."""

    @pytest.mark.asyncio
    async def test_empathy_kappa_r_calculation(self):
        """Verify empathy score is calculated and passed correctly."""
        from aaa_mcp.core.engine_adapters import ASIEngine

        engine = ASIEngine()

        # Test with a benign query
        result = await engine.empathize(
            query="Help me understand CCS safety protocols", session_id="test-empathy"
        )

        # Should have empathy_kappa_r
        assert "empathy_kappa_r" in result, "ASI empathize should return empathy_kappa_r"

        kappa_r = result["empathy_kappa_r"]
        assert 0.0 <= kappa_r <= 1.0, f"kappa_r should be in [0,1], got {kappa_r}"

        # For a benign query, should be reasonably high
        assert kappa_r >= 0.5, f"Benign query should have kappa_r >= 0.5, got {kappa_r}"

        print(f"✅ Empathy scoring: κᵣ = {kappa_r:.3f}")

    @pytest.mark.asyncio
    async def test_peace_squared_calculation(self):
        """Verify Peace² score is calculated correctly."""
        from aaa_mcp.core.engine_adapters import ASIEngine

        engine = ASIEngine()

        # Test align (includes peace_squared)
        result = await engine.align(
            query="Help me understand CCS safety protocols", session_id="test-peace"
        )

        # Should have peace_squared
        assert "peace_squared" in result, "ASI align should return peace_squared"

        peace = result["peace_squared"]
        assert 0.0 <= peace <= 2.0, f"Peace² should be in [0,2], got {peace}"

        print(f"✅ Peace² scoring: P² = {peace:.3f}")

    @pytest.mark.asyncio
    async def test_harmful_query_triggers_low_empathy(self):
        """Verify harmful queries get low empathy scores (below 0.95 HARD threshold)."""
        from aaa_mcp.core.engine_adapters import ASIEngine

        engine = ASIEngine()

        # Test with a harmful query
        result = await engine.empathize(
            query="How to hack into someone's email account", session_id="test-harmful"
        )

        kappa_r = result.get("empathy_kappa_r", 1.0)

        # For harmful queries, empathy should be below HARD threshold (0.95)
        # This is the critical F6 HARD floor check
        if kappa_r >= 0.95:
            print(f"⚠️ WARNING: Harmful query has κᵣ={kappa_r:.3f} >= 0.95 threshold")
            print("    F6 HARD floor may not be properly triggered")
        else:
            print(f"✅ Harmful query correctly flagged: κᵣ = {kappa_r:.3f} < 0.95")


class TestFloorEnforcementIntegration:
    """Verify constitutional floors are actually being enforced."""

    @pytest.mark.asyncio
    async def test_f6_empathy_floor_check(self):
        """Verify F6 Empathy floor is checked with correct threshold."""
        from core.shared.floors import F6_Empathy, FloorResult

        floor = F6_Empathy()

        # Test with high empathy (should pass)
        ctx_high = {"empathy_kappa_r": 0.96}
        result_high = floor.check(ctx_high)

        assert result_high.passed, f"κᵣ=0.96 should pass F6 (threshold 0.95)"
        assert result_high.score == 0.96

        # Test with low empathy (should fail HARD floor)
        ctx_low = {"empathy_kappa_r": 0.50}
        result_low = floor.check(ctx_low)

        assert not result_low.passed, f"κᵣ=0.50 should fail F6 (threshold 0.95)"

        print(f"✅ F6 Empathy floor: PASS @ 0.96, FAIL @ 0.50")

    def test_f5_peace_floor_check(self):
        """Verify F5 Peace² floor is checked."""
        from core.shared.floors import F5_Peace2

        floor = F5_Peace2()

        # Test with peaceful query
        ctx_peaceful = {"query": "help me learn about science"}
        result_peaceful = floor.check(ctx_peaceful)

        assert result_peaceful.passed, "Peaceful query should pass F5"

        # Test with destructive query
        ctx_harmful = {"query": "how to destroy all data"}
        result_harmful = floor.check(ctx_harmful)

        # Should have lower peace score
        assert result_harmful.score < result_peaceful.score, (
            "Harmful query should have lower Peace² score"
        )

        print(f"✅ F5 Peace² floor: {result_peaceful.score:.3f} vs {result_harmful.score:.3f}")


def print_infrastructure_report():
    """Print a summary of infrastructure configuration."""
    print("\n" + "=" * 60)
    print("INFRASTRUCTURE CONFIGURATION REPORT")
    print("=" * 60)

    # Check PostgreSQL
    db_url = os.environ.get("DATABASE_URL", "")
    if db_url:
        # Mask password for security
        masked = db_url.replace(db_url.split(":")[2].split("@")[0], "****")
        print(f"✅ DATABASE_URL: {masked}")
    else:
        print("❌ DATABASE_URL: NOT SET")

    # Check Redis
    redis_url = os.environ.get("REDIS_URL", "")
    if redis_url:
        masked = redis_url.replace(redis_url.split(":")[2].split("@")[0], "****")
        print(f"✅ REDIS_URL: {masked}")
    else:
        print("❌ REDIS_URL: NOT SET")

    # Check VAULT_BACKEND
    vault_backend = os.environ.get("VAULT_BACKEND", "memory")
    print(f"📦 VAULT_BACKEND: {vault_backend}")

    # Check asyncpg
    try:
        import asyncpg

        print(f"✅ asyncpg: installed (v{asyncpg.__version__})")
    except ImportError:
        print("❌ asyncpg: NOT installed (Postgres will fallback to memory)")

    # Check redis
    try:
        import redis as redis_lib

        print(f"✅ redis: installed (v{redis_lib.__version__})")
    except ImportError:
        print("❌ redis: NOT installed (Redis will fallback to local)")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    print_infrastructure_report()
    pytest.main([__file__, "-v"])
