"""Tests for L5 physics hardening guards."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

_L5_PHYSICS_PATH = (
    Path(__file__).resolve().parents[1] / "333_APPS" / "L5_AGENTS" / "environment" / "physics.py"
)
_L5_MISSING = not _L5_PHYSICS_PATH.exists()


def _load_physics_module():
    module_path = _L5_PHYSICS_PATH
    spec = spec_from_file_location("l5_physics", module_path)
    assert spec is not None and spec.loader is not None
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.skipif(_L5_MISSING, reason="L5_AGENTS/environment/physics.py not present")
def test_token_physics_rejects_negative_tokens() -> None:
    physics_module = _load_physics_module()
    token = physics_module.TokenPhysics()

    with pytest.raises(ValueError, match="non-negative"):
        token.consume(-1, 10)


@pytest.mark.skipif(_L5_MISSING, reason="L5_AGENTS/environment/physics.py not present")
def test_token_physics_budget_exceeded_raises_permission_error() -> None:
    physics_module = _load_physics_module()
    token = physics_module.TokenPhysics()

    with pytest.raises(PermissionError, match="STARVATION"):
        token.consume(600_000, 0)
