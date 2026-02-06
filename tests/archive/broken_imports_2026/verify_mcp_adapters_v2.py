
import sys
import os
import asyncio
from unittest.mock import MagicMock, patch

# Force unbuffered stdout
sys.stdout.reconfigure(encoding='utf-8')

print("STARTING VERIFICATION SCRIPT...", flush=True)

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
print(f"PYTHONPATH: {sys.path[0]}", flush=True)

# MOCK EVERYTHING before importing canonical_trinity
# This prevents ImportErrors from missing dependencies
sys.modules["codebase.kernel"] = MagicMock()
sys.modules["codebase.init.000_init.mcp_bridge"] = MagicMock()
sys.modules["mcp.core.bridge"] = MagicMock()
sys.modules["mcp.core.tool_registry"] = MagicMock()
sys.modules["mcp.transports.sse"] = MagicMock()

# Setup Mock Returns
async def mock_init_execute(*args, **kwargs):
    return {
        "status": "SEAL",
        "session_id": "test_sess_123",
        "authority": "GUEST",
        "injection_risk": 0.00,
        "energy_budget": 1.0,
        "lane": "SOFT",
        "reason": "Mock init success"
    }

sys.modules["codebase.init.000_init.mcp_bridge"].mcp_000_init = mock_init_execute

mock_km = MagicMock()
mock_km.get_agi.return_value.execute.return_value = {"session_id": "test", "clarity_score": 0.9, "status": "SEAL"}
mock_km.get_asi.return_value.execute.return_value = {"session_id": "test", "omega_total": 0.99, "vote": "SEAL"}
mock_km.get_apex.return_value.execute.return_value = {"session_id": "test", "verdict": "SEAL"}

print("MOCKS INSTALLED. IMPORTING TRINITY...", flush=True)

try:
    with patch("codebase.kernel.get_kernel_manager", return_value=mock_km):
        # Local import to simulate running the tool
        from mcp_server.tools.canonical_trinity import mcp_init, mcp_agi, mcp_asi, mcp_apex
        
    print("IMPORT SUCCESS.", flush=True)

except Exception as e:
    import traceback
    print(f"FATAL IMPORT ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

async def verify():
    print("--- TESTING _init_ ---", flush=True)
    try:
        res = await mcp_init(action="init", query="test")
        print(f"RESULT: {res}", flush=True)
        
        # Check adapters
        if "authority_level" in res and res["authority_level"] == "guest":
            print("✅ authority_level OK")
        else:
            print(f"❌ authority_level FAIL: {res.get('authority_level')}")
            
        if "injection_check_passed" in res and res["injection_check_passed"] is True:
             print("✅ injection_check_passed OK")
        else:
             print(f"❌ injection_check_passed FAIL: {res.get('injection_check_passed')}")
             
    except Exception as e:
        print(f"❌ EXECUTION FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(verify())
