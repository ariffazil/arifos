
import sys
import os
import asyncio
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Mock codebase.kernel.get_kernel_manager
sys.modules["codebase.kernel"] = MagicMock()
sys.modules["codebase.init.000_init.mcp_bridge"] = MagicMock()
sys.modules["mcp.core.bridge"] = MagicMock()

# Mock definitions
async def mock_init_execute(*args, **kwargs):
    return {
        "status": "SEAL",
        "session_id": "test_sess_123",
        "authority": "GUEST",
        "injection_risk": 0.0,
        "energy_budget": 1.0,
        "lane": "SOFT",
        "reason": "Mock init success"
    }

async def mock_agi_execute(*args, **kwargs):
    # Simulate DeltaBundle or dict
    return {
        "session_id": "test_sess_123",
        "clarity_score": 0.8,
        "omega_0": 0.04,
        "status": "SEAL",
        "action_policy": {"action": "think"},
        "hierarchical_beliefs": {}
    }

async def mock_asi_execute(*args, **kwargs):
    # Simulate OmegaBundle
    return {
        "session_id": "test_sess_123",
        "omega_total": 0.95,
        "vote": "SEAL",
        "empathy": {"kappa_r": 0.9},
        "system": {"peace_squared": 1.0},
        "society": {"thermodynamic_justice": 0.95},
        "floor_scores": {"F1_reversibility": 1.0, "F11_consent": True}
    }

async def mock_apex_execute(*args, **kwargs):
    # Simulate verdict strict
    return {
        "status": "SEAL", 
        "verdict": "SEAL", 
        "session_id": "test_sess_123",
        "trinity_score": 0.92,
        "paradox_scores": {},
        "equilibrium": {"score": 0.92},
        "proof": {"hash": "abc"}
    }

# Patch get_kernel_manager
mock_km = MagicMock()
mock_km.get_agi.return_value.execute = mock_agi_execute
mock_km.get_asi.return_value.execute = mock_asi_execute
mock_km.get_apex.return_value.execute = mock_apex_execute

# Patch mcp_bridge for init
sys.modules["codebase.init.000_init.mcp_bridge"].mcp_000_init = mock_init_execute

try:
    with patch("codebase.kernel.get_kernel_manager", return_value=mock_km):
        from mcp_server.tools.canonical_trinity import mcp_init, mcp_agi, mcp_asi, mcp_apex
except Exception as e:
    import traceback
    print(f"IMPORT ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

    async def verify():
        print("Verifying MCP Adapters...")
        
        # 1. Verify INIT
        print("Testing mcp_init...")
        init_res = await mcp_init(action="init", query="test")
        print(f"INIT Result keys: {init_res.keys()}")
        assert "authority_level" in init_res
        assert "injection_check_passed" in init_res
        assert init_res["authority_level"] == "guest"
        assert init_res["injection_check_passed"] == True
        print("✅ INIT Passed")

        # 2. Verify AGI
        print("Testing mcp_agi...")
        agi_res = await mcp_agi(action="full", query="test")
        print(f"AGI Result keys: {agi_res.keys()}")
        assert "entropy_delta" in agi_res
        assert "vote" in agi_res
        assert agi_res["entropy_delta"] == 0.3 # 0.8 - 0.5
        print("✅ AGI Passed")
        
        # 3. Verify ASI
        print("Testing mcp_asi...")
        asi_res = await mcp_asi(action="full", query="test")
        print(f"ASI Result keys: {asi_res.keys()}")
        assert "omega_total" in asi_res
        assert "vote" in asi_res
        assert "empathy_kappa_r" in asi_res
        print("✅ ASI Passed")

        # 4. Verify APEX
        print("Testing mcp_apex...")
        apex_res = await mcp_apex(action="judge", query="test")
        print(f"APEX Result keys: {apex_res.keys()}")
        assert "final_verdict" in apex_res
        assert "trinity_score" in apex_res
        assert apex_res["final_verdict"] == "SEAL"
        print("✅ APEX Passed")
        
        print("\n🎉 ALL TESTS PASSED!")

    if __name__ == "__main__":
        asyncio.run(verify())
