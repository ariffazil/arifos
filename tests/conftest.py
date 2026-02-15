"""Pytest configuration and fixtures for arifOS tests"""

import os
import sys
import warnings
from pathlib import Path
import asyncio

try:
    import asyncpg
    import redis
except ImportError:
    asyncpg = None
    redis = None

# Add project root to sys.path to resolve 'aaa_mcp'
sys.path.insert(0, str(Path(__file__).parents[1]))

import pytest

# Silence langsmith/pydantic v1 warning on Python 3.14 (benign in this env)
warnings.filterwarnings(
    "ignore",
    message="Core Pydantic V1 functionality isn't compatible with Python 3.14 or greater.",
    category=UserWarning,
    module="langsmith.schemas",
)

# Ensure legacy spec bypass is active during import/collection
os.environ.setdefault("ARIFOS_ALLOW_LEGACY_SPEC", "1")
os.environ.setdefault("ARIFOS_PHYSICS_DISABLED", "1")
# Default to debug output in tests to preserve rich contracts for assertions.
os.environ.setdefault("AAA_MCP_OUTPUT_MODE", "debug")


@pytest.fixture(scope="session", autouse=True)
def disable_physics_globally():
    """
    Disable TEARFRAME Physics globally for all tests (performance optimization).

    Most unit tests don't need physics computation (Ψ, floor checks, etc).
    This fixture runs once per test session and disables physics by default.

    Individual test modules can override this by removing the env var.
    """
    os.environ["ARIFOS_PHYSICS_DISABLED"] = "1"
    yield
    # Cleanup after all tests
    if "ARIFOS_PHYSICS_DISABLED" in os.environ:
        del os.environ["ARIFOS_PHYSICS_DISABLED"]


@pytest.fixture(scope="session", autouse=True)
def allow_legacy_spec_for_tests():
    """
    Allow legacy spec loading for tests (bypasses cryptographic manifest requirement).

    The test environment doesn't require Track B cryptographic authority validation.
    This enables tests to run without MANIFEST.sha256.json file.

    Production code MUST NOT use this bypass - it's test-only.
    """
    os.environ["ARIFOS_ALLOW_LEGACY_SPEC"] = "1"
    yield
    # Cleanup after all tests
    if "ARIFOS_ALLOW_LEGACY_SPEC" in os.environ:
        del os.environ["ARIFOS_ALLOW_LEGACY_SPEC"]


# === NEW: Physics override for APEX THEORY tests ===


@pytest.fixture(scope="module")
def enable_physics_for_apex_theory():
    """
    Enable TEARFRAME Physics for APEX THEORY system flow tests.

    These tests verify constitutional governance behavior that
    requires active physics computation (Ψ, floor checks, etc).

    Scope: module (enable for entire test_system_flows.py file)
    """
    # Store original state
    original_state = os.environ.get("ARIFOS_PHYSICS_DISABLED")

    # Enable physics (remove disable flag)
    if "ARIFOS_PHYSICS_DISABLED" in os.environ:
        del os.environ["ARIFOS_PHYSICS_DISABLED"]

    yield

    # Restore original state
    if original_state is not None:
        os.environ["ARIFOS_PHYSICS_DISABLED"] = original_state
    else:
        os.environ["ARIFOS_PHYSICS_DISABLED"] = "1"


# Skip legacy tests that still reference arifos (the old package name before v52)
def pytest_ignore_collect(collection_path, config):
    """
    Skips collecting tests from files that still import the legacy `arifos` package.
    This is necessary after the migration to the `codebase` package structure.
    """
    if collection_path.suffix != ".py":
        return False

    # Ignore anything in a 'legacy' or 'archive' directory explicitly
    path_str = str(collection_path)
    if (
        "tests/legacy" in path_str
        or "tests\\legacy" in path_str
        or "tests/archive" in path_str
        or "tests\\archive" in path_str
    ):
        return True

    try:
        # A simple text check is much faster than AST parsing
        text = collection_path.read_text(encoding="utf-8", errors="ignore")
        if "from arifos" in text or "import arifos" in text:
            return True
    except Exception:
        # If we can't read the file, let pytest handle the error
        return False

    return False


# === Infrastructure Health Checks for Skippable Tests ===


def is_postgres_running():
    """Check if PostgreSQL is running and accessible."""
    db_url = os.environ.get("DATABASE_URL")
    if not db_url or not asyncpg:
        return False
    try:
        # Try to connect with a short timeout
        async def check_pg():
            try:
                conn = await asyncio.wait_for(asyncpg.connect(dsn=db_url), timeout=2.0)
                await conn.close()
                return True
            except (OSError, asyncio.TimeoutError, asyncpg.PostgresError):
                return False

        return asyncio.run(check_pg())
    except Exception:
        return False


def is_redis_running():
    """Check if Redis is running and accessible."""
    redis_url = os.environ.get("REDIS_URL")
    if not redis_url or not redis:
        return False
    try:
        # The from_url function attempts to connect
        r = redis.from_url(redis_url, socket_connect_timeout=2)
        return r.ping()
    except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError):
        return False


postgres_required = pytest.mark.skipif(
    not is_postgres_running(),
    reason="PostgreSQL service not running or configured via DATABASE_URL",
)

redis_required = pytest.mark.skipif(
    not is_redis_running(), reason="Redis service not running or configured via REDIS_URL"
)
