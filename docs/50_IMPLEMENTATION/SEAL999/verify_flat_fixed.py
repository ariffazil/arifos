"""
Verify VAULT_999 flat structure works - fixed imports
"""

import sys

# Add root to path
sys.path.insert(0, "C:\\Users\\User\\arifOS")

try:
    from VAULT_999 import VAULT999, VaultConfig

    print("[SUCCESS] Imported VAULT999 from flat VAULT_999/")

    # Test instantiation
    config = VaultConfig()
    vault = VAULT999(config=config)
    print("[SUCCESS] Created VAULT999 instance")

    print("\n[OK] VAULT_999 flat structure is working!")
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
