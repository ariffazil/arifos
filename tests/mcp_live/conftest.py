import pytest
from aclip_cai.core.kernel import get_kernel

@pytest.fixture(scope="session")
async def kernel():
    """Provides a shared constitutional kernel singleton for test life-cycle."""
    return await get_kernel()

@pytest.fixture(scope="session")
def session_id():
    """Provides a shared session ID for triad and pipeline tests."""
    return "test-session-mcp-live-xyz123"
