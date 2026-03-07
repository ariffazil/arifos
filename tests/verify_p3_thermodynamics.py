
import sys
import os
import time
import pytest
from typing import Any

# Ensure we can import from the root
sys.path.append(os.getcwd())

from core.physics.thermodynamics_hardened import (
    init_thermodynamic_budget,
    get_thermodynamic_budget,
    record_entropy_io,
    check_landauer_bound,
    consume_reason_energy,
    EntropyIncreaseViolation,
    LandauerViolation,
    ThermodynamicExhaustion,
    ThermodynamicViolation
)

def test_entropy_increase_violation():
    print("\n1. Triggering EntropyIncreaseViolation (F4)...")
    session_id = "test_entropy_session"
    init_thermodynamic_budget(session_id, initial_budget=1.0)
    
    # Input entropy < Output entropy -> Violation
    input_s = 0.5
    output_s = 0.8 # Higher entropy (more confusion)
    
    try:
        record_entropy_io(session_id, input_s, output_s)
        print("FAILED: EntropyIncreaseViolation not raised")
        return False
    except EntropyIncreaseViolation as e:
        print(f"SUCCESS: Caught expected exception: {e}")
        print(f"Floor Mapping: {getattr(e, 'floor_id', 'UNKNOWN')} (Expected: F4)")
        if getattr(e, 'floor_id', '') == "F4":
            return True
        else:
            print(f"FAILED: Wrong floor mapping: {getattr(e, 'floor_id', 'None')}")
            return False
    except Exception as e:
        print(f"FAILED: Caught unexpected exception type {type(e)}: {e}")
        return False

def test_landauer_violation():
    print("\n2. Triggering LandauerViolation (F2)...")
    # LandauerViolation is triggered when efficiency is impossibly high (e.g., zero time)
    # check_landauer_bound(compute_ms, tokens, delta_s)
    # efficiency_ratio = 1.0 / (ms_per_token + 0.001)
    # If ms_per_token = 0, efficiency_ratio = 1000.0 -> Violation
    
    try:
        check_landauer_bound(compute_ms=0, tokens_generated=10, entropy_reduction=-1.0)
        print("FAILED: LandauerViolation not raised")
        return False
    except LandauerViolation as e:
        print(f"SUCCESS: Caught expected exception: {e}")
        print(f"Floor Mapping: {getattr(e, 'floor_id', 'UNKNOWN')} (Expected: F2)")
        if getattr(e, 'floor_id', '') == "F2":
            return True
        else:
            print(f"FAILED: Wrong floor mapping: {getattr(e, 'floor_id', 'None')}")
            return False
    except Exception as e:
        print(f"FAILED: Caught unexpected exception type {type(e)}: {e}")
        return False

def test_thermodynamic_exhaustion():
    print("\n3. Triggering ThermodynamicExhaustion (F7)...")
    session_id = "test_exhaustion_session"
    # Initialize with a tiny budget
    tiny_budget = 0.0001 
    init_thermodynamic_budget(session_id, initial_budget=tiny_budget)
    
    # COST_PER_REASON_CYCLE is 1e-3, so 1 cycle should exhaust 1e-4 budget
    try:
        consume_reason_energy(session_id, n_cycles=1)
        print("FAILED: ThermodynamicExhaustion not raised")
        return False
    except ThermodynamicExhaustion as e:
        print(f"SUCCESS: Caught expected exception: {e}")
        print(f"Floor Mapping: {getattr(e, 'floor_id', 'UNKNOWN')} (Expected: F7)")
        if getattr(e, 'floor_id', '') == "F7":
            return True
        else:
            print(f"FAILED: Wrong floor mapping: {getattr(e, 'floor_id', 'None')}")
            return False
    except Exception as e:
        print(f"FAILED: Caught unexpected exception type {type(e)}: {e}")
        return False

def run_existing_tests():
    print("\n4. Running existing tests/e2e_test_hardened_thermodynamics.py...")
    import subprocess
    result = subprocess.run(["pytest", "tests/e2e_test_hardened_thermodynamics.py"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode == 0:
        print("SUCCESS: Existing tests passed")
        return True
    else:
        print(f"FAILED: Existing tests failed with return code {result.returncode}")
        print(result.stderr)
        return False

if __name__ == "__main__":
    success = True
    success &= test_entropy_increase_violation()
    success &= test_landauer_violation()
    success &= test_thermodynamic_exhaustion()
    success &= run_existing_tests()
    
    if success:
        print("\nOVERALL VERIFICATION: PASSED")
        sys.exit(0)
    else:
        print("\nOVERALL VERIFICATION: FAILED")
        sys.exit(1)
