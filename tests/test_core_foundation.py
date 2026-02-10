"""
Test script for v55.5 RUKUN AGI foundation (core/ architecture).
Verifies that all 4 core.shared modules and core.organs can be imported correctly.
"""
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== TESTING v55.5 RUKUN AGI FOUNDATION (core/) ===")
print()

# Test 1: Physics
print("[1/5] Testing core.shared.physics...")
from core.shared.physics import W_3, delta_S, G, geometric_mean
print("      ✓ Physics module OK")

# Test 2: ATLAS
print("[2/5] Testing core.shared.atlas...")
from core.shared.atlas import Lane, Lambda
print("      ✓ ATLAS module OK")

# Test 3: Types
print("[3/5] Testing core.shared.types...")
from core.shared.types import Verdict, VaultOutput
print("      ✓ Types module OK")
print(f"      Verdicts: {[v.value for v in Verdict]}")

# Test 4: Crypto
print("[4/5] Testing core.shared.crypto...")
from core.shared.crypto import generate_session_id, sha256_hash
session_id = generate_session_id()
print("      ✓ Crypto module OK")
print(f"      Session ID sample: {session_id[:20]}...")

# Test 5: Organs (Airlock)
print("[5/5] Testing core.organs._0_init...")
from core.organs._0_init import init, scan_injection
print("      ✓ Airlock organ OK")

print()
print("=== v55.5 RUKUN AGI FOUNDATION VERIFIED ✓ ===")
print()
print("Summary (core/ architecture):")
print("  ✓ core.shared.physics  - Thermodynamic primitives (W_3, delta_S, G)")
print("  ✓ core.shared.atlas    - Governance routing (Lambda, Lane)")
print("  ✓ core.shared.types    - Pydantic contracts (Verdict)")
print("  ✓ core.shared.crypto   - Trust primitives (Ed25519, Merkle)")
print("  ✓ core.organs._0_init  - Constitutional Airlock (F11/F12)")
print()
print("RUKUN AGI - The Five Pillars: 555")
print("Source of Truth: core/ directory")
