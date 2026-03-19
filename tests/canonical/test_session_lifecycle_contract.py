from __future__ import annotations

import pytest

from aaa_mcp.sessions.lifecycle import KernelState, LifecycleManager


@pytest.fixture
def lifecycle() -> LifecycleManager:
    return LifecycleManager()


def test_ratify_rejects_invalid_sovereign_token(lifecycle: LifecycleManager) -> None:
    session = lifecycle.init_session("canonical-001", "arif", "MY", "normal context")
    lifecycle.hold_888(session.session_id, action="deploy production")

    with pytest.raises(PermissionError):
        lifecycle.ratify(session.session_id, sovereign_token="invalid")


def test_ratify_releases_hold_with_valid_sovereign_token(lifecycle: LifecycleManager) -> None:
    session = lifecycle.init_session("canonical-002", "arif", "MY", "normal context")
    lifecycle.hold_888(session.session_id, action="deploy production")

    result = lifecycle.ratify(session.session_id, sovereign_token="888_APPROVED")

    assert result.state == KernelState.ACTIVE
