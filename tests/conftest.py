"""Pytest configuration and fixtures for arifOS tests."""

from __future__ import annotations

import asyncio
import os
import sys
import warnings
from pathlib import Path

import pytest

try:
    import asyncpg
    import redis
except ImportError:  # pragma: no cover
    asyncpg = None
    redis = None


# Add project root to sys.path for imports when running from repo checkout.
sys.path.insert(0, str(Path(__file__).parents[1]))


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
    """Disable physics globally for all tests (performance optimization)."""

    os.environ["ARIFOS_PHYSICS_DISABLED"] = "1"
    yield
    if "ARIFOS_PHYSICS_DISABLED" in os.environ:
        del os.environ["ARIFOS_PHYSICS_DISABLED"]


@pytest.fixture(scope="session", autouse=True)
def allow_legacy_spec_for_tests():
    """Allow legacy spec loading for tests (bypasses cryptographic manifest requirement)."""

    os.environ["ARIFOS_ALLOW_LEGACY_SPEC"] = "1"
    yield
    if "ARIFOS_ALLOW_LEGACY_SPEC" in os.environ:
        del os.environ["ARIFOS_ALLOW_LEGACY_SPEC"]


@pytest.fixture(scope="module")
def enable_physics_for_apex_theory():
    """Enable physics for APEX THEORY system flow tests."""

    original_state = os.environ.get("ARIFOS_PHYSICS_DISABLED")
    if "ARIFOS_PHYSICS_DISABLED" in os.environ:
        del os.environ["ARIFOS_PHYSICS_DISABLED"]

    yield

    if original_state is not None:
        os.environ["ARIFOS_PHYSICS_DISABLED"] = original_state
    else:
        os.environ["ARIFOS_PHYSICS_DISABLED"] = "1"


def pytest_ignore_collect(collection_path, config):
    """Avoid collecting archived/legacy tests.

    This repo contains multiple historical MCP surfaces. For the arifOS AAA MCP
    13-tool surface, we only collect tests that target `arifos_aaa_mcp`.
    """

    path_str = str(collection_path)
    if "tests/archive" in path_str or "tests\\archive" in path_str:
        return True
    if "tests/legacy" in path_str or "tests\\legacy" in path_str:
        return True

    if collection_path.suffix != ".py":
        return False

    try:
        text = collection_path.read_text(encoding="utf-8", errors="ignore")
        if "from arifos" in text or "import arifos" in text:
            return True
        if "import codebase" in text or "from codebase" in text:
            return True

        # Focus on the canonical 13-tool surface (`arifos_aaa_mcp`).
        legacy_markers = (
            "import aaa_mcp.server",
            "from aaa_mcp.server import",
            "import aaa_mcp.tools",
            "from aaa_mcp.tools import",
            "from aaa_mcp.tools.",
            "import aclip_cai.mcp_server",
            "from aclip_cai.mcp_server import",
            "import aaa_mcp.__main__",
            "from aaa_mcp.__main__ import",
        )
        if any(m in text for m in legacy_markers) and "arifos_aaa_mcp" not in text:
            return True
    except Exception:
        return False

    return False


def is_postgres_running() -> bool:
    """Check if PostgreSQL is running and accessible."""

    db_url = os.environ.get("DATABASE_URL")
    if not db_url or asyncpg is None:
        return False

    import asyncpg as asyncpg_mod

    async def check_pg() -> bool:
        try:
            conn = await asyncio.wait_for(asyncpg_mod.connect(dsn=db_url), timeout=2.0)
            await conn.close()
            return True
        except (OSError, asyncio.TimeoutError, asyncpg_mod.PostgresError):
            return False

    try:
        return asyncio.run(check_pg())
    except Exception:
        return False


def is_redis_running() -> bool:
    """Check if Redis is running and accessible."""

    redis_url = os.environ.get("REDIS_URL")
    if not redis_url or redis is None:
        return False

    import redis as redis_mod
    from redis import exceptions as redis_exceptions

    try:
        r = redis_mod.from_url(redis_url, socket_connect_timeout=2)
        return bool(r.ping())
    except (redis_exceptions.ConnectionError, redis_exceptions.TimeoutError):
        return False


postgres_required = pytest.mark.skipif(
    not is_postgres_running(),
    reason="PostgreSQL service not running or configured via DATABASE_URL",
)


redis_required = pytest.mark.skipif(
    not is_redis_running(),
    reason="Redis service not running or configured via REDIS_URL",
)


@pytest.fixture
async def aaa_client():
    """In-memory MCP client for the canonical AAA server."""

    from fastmcp import Client

    from arifos_aaa_mcp.server import create_aaa_mcp_server

    async with Client(create_aaa_mcp_server()) as client:
        yield client
