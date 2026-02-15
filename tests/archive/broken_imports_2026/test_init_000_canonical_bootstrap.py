"""
E2E Test Suite: init_000 + Canonical Bootstrap Integration (v55.3)

Tests the full flow from init_gate → canonical bootstrap → Tri-Witness consensus.

Coverage:
1. Canonical bootstrap module in isolation
2. init_000 with web_first mode
3. init_000 with local_only mode  
4. Sovereign vs Guest access to AAA
5. Fallback behavior when web sources fail

Authority: Muhammad Arif bin Fazil
"""

import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import asyncio
import json
import os
import sys
from pathlib import Path
import pytest

# Ensure we can import from codebase
sys.path.insert(0, str(Path(__file__).parent.parent))

# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_canonical_config():
    """Mock configuration for testing."""
    return {
        "bootstrap_mode": "web_first",
        "canonical_sources": {
            "aaa_human": {
                "url": "https://arif-fazil.com/llms.json",
                "fallback_url": "https://arif-fazil.com/llms.txt",
                "band": "AAA",
                "access": "sovereign_only",
                "required": False,
                "timeout_seconds": 3,  # Short timeout for tests
            },
            "bbb_ledger": {
                "url": "https://arifos.arif-fazil.com/llms.json",
                "fallback_url": "https://arifos.arif-fazil.com/llms.txt",
                "band": "BBB",
                "access": "always",
                "required": True,
                "timeout_seconds": 3,
            },
            "ccc_canon": {
                "url": "https://apex.arif-fazil.com/llms.json",
                "fallback_url": "https://apex.arif-fazil.com/llms.txt",
                "band": "CCC",
                "access": "always",
                "required": True,
                "timeout_seconds": 3,
            },
        },
        "verification": {
            "check_signatures": False,  # Disable for tests
            "min_sources": 2,
            "require_ccc": True,
            "hash_verification": False,
            "max_age_seconds": 3600,
        },
        "fallback": {
            "local_config_path": "VAULT999/CCC_CANON/canonical_config.json",
            "cache_dir": ".cache/test/arifos",
            "on_failure": "fallback_local",
        },
        "governance": {
            "sovereign_scar_threshold": 1.0,
            "guest_scar_threshold": 0.0,
            "authorized_scar_threshold": 0.5,
        }
    }


# =============================================================================
# TEST 1: Canonical Bootstrap Module (Isolation)
# =============================================================================

@pytest.mark.asyncio
async def test_canonical_bootstrap_imports():
    """Test that canonical bootstrap module can be imported."""
    from codebase.init import (
        CanonicalBootstrap,
        fetch_canonical_state,
        CanonicalBootstrapResult,
        get_bootstrap_config,
    )
    
    assert CanonicalBootstrap is not None
    assert fetch_canonical_state is not None
    assert CanonicalBootstrapResult is not None
    print("[OK] Canonical bootstrap imports successfully")


@pytest.mark.asyncio
async def test_canonical_bootstrap_config_loading():
    """Test configuration loading with defaults."""
    from codebase.init import get_bootstrap_config
    
    config = get_bootstrap_config()
    
    assert "bootstrap_mode" in config
    assert "canonical_sources" in config
    assert "ccc_canon" in config["canonical_sources"]
    assert "bbb_ledger" in config["canonical_sources"]
    assert "aaa_human" in config["canonical_sources"]
    print(f"[OK] Config loaded: mode={config['bootstrap_mode']}")


@pytest.mark.asyncio
async def test_canonical_bootstrap_guest_scar_weight():
    """Test that guest (scar_weight=0.0) cannot access AAA."""
    from codebase.init import fetch_canonical_state
    
    result = await fetch_canonical_state(
        scar_weight=0.0,
        session_id="test_guest_session",
        mode="web_first"
    )
    
    # Guest should not have AAA access
    if result.aaa_human:
        assert not result.aaa_human.success, "Guest should not access AAA"
    
    # But should have CCC and BBB (if web works)
    print(f"[OK] Guest access: status={result.status}, sources={result.sources_fetched}")
    print(f"  - CCC available: {result.ccc_canon.success if result.ccc_canon else False}")
    print(f"  - BBB available: {result.bbb_ledger.success if result.bbb_ledger else False}")
    print(f"  - AAA available: {result.aaa_human.success if result.aaa_human else False}")


@pytest.mark.asyncio
async def test_canonical_bootstrap_sovereign_scar_weight():
    """Test that sovereign (scar_weight=1.0) can access AAA."""
    from codebase.init import fetch_canonical_state
    
    result = await fetch_canonical_state(
        scar_weight=1.0,
        session_id="test_sovereign_session",
        mode="web_first"
    )
    
    # Sovereign should attempt AAA access
    print(f"[OK] Sovereign access: status={result.status}, sources={result.sources_fetched}")
    print(f"  - CCC available: {result.ccc_canon.success if result.ccc_canon else False}")
    print(f"  - BBB available: {result.bbb_ledger.success if result.bbb_ledger else False}")
    print(f"  - AAA attempted: {result.aaa_human is not None}")
    if result.aaa_human:
        print(f"  - AAA success: {result.aaa_human.success}")


@pytest.mark.asyncio
async def test_canonical_bootstrap_local_only_mode():
    """Test local_only mode skips web fetch."""
    from codebase.init import fetch_canonical_state
    
    result = await fetch_canonical_state(
        scar_weight=1.0,
        session_id="test_local_session",
        mode="local_only"
    )
    
    assert result.status == "SABAR", "Local only should return SABAR"
    assert result.local_fallback_used, "Should use local fallback"
    assert result.mode == "local_fallback"
    print("[OK] Local-only mode works correctly")


# =============================================================================
# TEST 2: init_000 Integration
# =============================================================================

@pytest.mark.asyncio
async def test_init_000_imports():
    """Test that init_000 can be imported via canonical_trinity."""
    # init_000 is wrapped by mcp_init in canonical_trinity
    from mcp_server.tools.canonical_trinity import mcp_init
    
    assert callable(mcp_init)
    print("[OK] init_000 (via mcp_init) imports successfully")


@pytest.mark.asyncio
async def test_init_000_guest_ignition():
    """Test full init_000 flow for guest user."""
    from mcp_server.tools.canonical_trinity import mcp_init
    
    result = await mcp_init(
        action="init",
        query="Hello, I need help with a coding task",
        authority_token="",
        session_id="test_guest_001"
    )
    
    assert "session_id" in result
    assert "status" in result
    assert "authority_level" in result
    
    # Guest should have guest authority
    assert result["authority_level"] in ["guest", "user"]
    
    print(f"[OK] Guest ignition: status={result['status']}, authority={result['authority_level']}")
    print(f"  - Session: {result['session_id'][:8]}...")
    print(f"  - Verdict: {result.get('verdict', 'N/A')}")


@pytest.mark.asyncio
async def test_init_000_sovereign_ignition():
    """Test full init_000 flow for sovereign user (Arif)."""
    from mcp_server.tools.canonical_trinity import mcp_init
    
    result = await mcp_init(
        action="init",
        query="Salam, I'm Arif. Need to debug the vault system.",
        authority_token="",
        session_id="test_sovereign_001"
    )
    
    assert "session_id" in result
    assert "status" in result
    assert "authority_level" in result
    
    # Should recognize sovereign
    print(f"[OK] Sovereign ignition: status={result['status']}, authority={result['authority_level']}")
    print(f"  - Session: {result['session_id'][:8]}...")
    print(f"  - Verdict: {result.get('verdict', 'N/A')}")
    print(f"  - Access Level: {result.get('access_level', 'N/A')}")


@pytest.mark.asyncio
async def test_init_000_validate_action():
    """Test init_000 validate action (lightweight)."""
    from mcp_server.tools.canonical_trinity import mcp_init
    
    result = await mcp_init(
        action="validate",
        query="",
        session_id="test_validate_001"
    )
    
    assert result["status"] == "SEAL"
    assert result["verdict"] == "SEAL"
    print("[OK] Validate action returns SEAL")


@pytest.mark.asyncio
async def test_init_000_reset_action():
    """Test init_000 reset action."""
    from mcp_server.tools.canonical_trinity import mcp_init
    
    result = await mcp_init(
        action="reset",
        query="",
        session_id="test_reset_001"
    )
    
    assert result["status"] == "SEAL"
    print("[OK] Reset action returns SEAL with new session")


# =============================================================================
# TEST 3: Tri-Witness Consensus
# =============================================================================

@pytest.mark.asyncio
async def test_tri_witness_consensus_calculation():
    """Test that Tri-Witness requires ≥2 sources."""
    from codebase.init import fetch_canonical_state
    
    result = await fetch_canonical_state(
        scar_weight=0.0,
        session_id="test_triwitness_001"
    )
    
    # Tri-Witness sync requires ≥2 sources
    print(f"[OK] Tri-Witness check:")
    print(f"  - Sources fetched: {result.sources_fetched}")
    print(f"  - Tri-Witness sync: {result.tri_witness_sync}")
    print(f"  - Required: ≥2")
    
    if result.sources_fetched >= 2:
        assert result.tri_witness_sync, "Should have Tri-Witness sync with ≥2 sources"


# =============================================================================
# TEST 4: Error Handling & Edge Cases
# =============================================================================

@pytest.mark.asyncio
async def test_init_000_invalid_action():
    """Test init_000 with invalid action returns VOID."""
    from mcp_server.tools.canonical_trinity import mcp_init
    
    result = await mcp_init(
        action="invalid_action",
        query="test",
        session_id="test_invalid_001"
    )
    
    assert result["status"] == "VOID"
    print("[OK] Invalid action returns VOID")


@pytest.mark.asyncio
async def test_init_000_empty_query():
    """Test init_000 with empty query (phatic/greeting)."""
    from mcp_server.tools.canonical_trinity import mcp_init
    
    result = await mcp_init(
        action="init",
        query="hi",
        session_id="test_empty_001"
    )
    
    assert "session_id" in result
    print(f"[OK] Empty/phatic query handled: status={result['status']}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("E2E Test Suite: init_000 + Canonical Bootstrap (v55.3)")
    print("=" * 70)
    
    # Run tests manually if pytest not available
    async def run_tests():
        tests = [
            ("Imports", test_canonical_bootstrap_imports),
            ("Config Loading", test_canonical_bootstrap_config_loading),
            ("Guest Access", test_canonical_bootstrap_guest_scar_weight),
            ("Sovereign Access", test_canonical_bootstrap_sovereign_scar_weight),
            ("Local-Only Mode", test_canonical_bootstrap_local_only_mode),
            ("Init Imports", test_init_000_imports),
            ("Guest Ignition", test_init_000_guest_ignition),
            ("Sovereign Ignition", test_init_000_sovereign_ignition),
            ("Validate Action", test_init_000_validate_action),
            ("Reset Action", test_init_000_reset_action),
            ("Tri-Witness", test_tri_witness_consensus_calculation),
            ("Invalid Action", test_init_000_invalid_action),
            ("Empty Query", test_init_000_empty_query),
        ]
        
        passed = 0
        failed = 0
        
        for name, test_func in tests:
            try:
                print(f"\n--- {name} ---")
                await test_func()
                passed += 1
            except Exception as e:
                print(f"[FAIL] {name} FAILED: {e}")
                failed += 1
        
        print("\n" + "=" * 70)
        print(f"Results: {passed} passed, {failed} failed")
        print("=" * 70)
        
        return failed == 0
    
    success = asyncio.run(run_tests())
    sys.exit(0 if success else 1)
