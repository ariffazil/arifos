"""
Test script for T000 RUKUN AGI foundation (core/ architecture).
Verifies that all 4 core.shared modules and core.organs can be imported correctly.
T000: 2026.02.15-FORGE-TRINITY-SEAL
"""

import os
import sys

# Add project root to Python path (one level up from tests/)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_physics_module():
    """core.shared.physics exports thermodynamic primitives."""
    from core.shared.physics import W_3, G, delta_S, geometric_mean

    assert callable(W_3)
    assert callable(G)
    assert callable(delta_S)
    assert callable(geometric_mean)


def test_atlas_module():
    """core.shared.atlas exports governance routing."""
    from core.shared.atlas import Lambda, Lane

    assert Lambda is not None
    assert Lane is not None


def test_types_module():
    """core.shared.types exports Pydantic contracts."""
    from core.shared.types import VaultOutput, Verdict

    verdicts = [v.value for v in Verdict]
    assert len(verdicts) > 0
    assert "SEAL" in verdicts


def test_crypto_module():
    """core.shared.crypto exports trust primitives."""
    from core.shared.crypto import generate_session_id, sha256_hash

    session_id = generate_session_id()
    assert isinstance(session_id, str)
    assert len(session_id) > 0


def test_airlock_organ():
    """core.organs._0_init exports constitutional airlock."""
    from core.organs._0_init import init, scan_injection

    assert callable(init)
    assert callable(scan_injection)
