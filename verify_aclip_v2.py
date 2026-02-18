
import sys
import os
import json
import importlib

# Add tool directory to sys.path
sys.path.append(os.path.join(os.getcwd(), 'aclip_cai', 'tools'))

print("--- TESTING NERVOUS SYSTEM (V2) ---")

try:
    print("\n[0] CHECKING DEPENDENCIES...")
    try:
        import psutil
        print(f"psutil version: {psutil.__version__}")
        if not hasattr(psutil, "AccessDenied"):
            print("WARNING: psutil.AccessDenied missing!")
    except ImportError:
        print("ERROR: psutil not installed. Net monitor will fail.")
except Exception as e:
    print(f"DEP FAIL: {e}")

try:
    print("\n[1] TESTING FS_INSPECTOR (The Touch)...")
    import fs_inspector
    # Test entropy limits
    result = fs_inspector.fs_inspect(path=".", max_files=5, depth=2)
    print(f"Status: {result.get('status')}")
    print(f"Limit Reached: {result.get('stats', {}).get('limit_reached')}")
    print(f"Files Returned: {len(result.get('tree', []))}")
except Exception as e:
    print(f"FAIL: {e}")

try:
    print("\n[2] TESTING NET_MONITOR (The Sight)...")
    import net_monitor
    # Reload to ensure clean state
    importlib.reload(net_monitor)
    # Test interface and routing awareness
    result = net_monitor.net_status(check_interfaces=True, check_routing=True)
    if "error" in result:
        print(f"Net Monitor Error: {result['error']}")
    else:
        print(f"Interfaces Found: {list(result.get('interfaces', {}).keys())}")
        print(f"Default Route IP: {result.get('routing', {}).get('default_route_interface_ip')}")
except Exception as e:
    print(f"FAIL: {e}")

try:
    print("\n[3] TESTING CONFIG_READER (The Prevention)...")
    import config_reader
    importlib.reload(config_reader)
    # Mock an environment variable with correct prefix
    os.environ["ARIFOS_TEST_SECRET"] = "super_secret_password_123"
    result = config_reader.config_flags()
    val = result.get("environment_variables", {}).get("ARIFOS_TEST_SECRET", "NOT_FOUND")
    print(f"Secret Masking Check: {val}")
except Exception as e:
    print(f"FAIL: {e}")

print("\n--- TEST COMPLETE ---")
