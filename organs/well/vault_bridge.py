# WELL to VAULT999 Bridge (Sovereignty Refined)
# Role: Immutable biological anchoring with High-Signal Filtering.
# Axiom: WELL informs, arifOS judges, A-FORGE executes.

import json
import hashlib
import datetime
from pathlib import Path
import sys

WELL_STATE_PATH = Path("/root/WELL/state.json")
VAULT_LOG_PATH = Path("/root/arifOS/core/vault999/well_ledger.jsonl")

def get_last_anchored_score():
    """Reads the last entry in VAULT999 to determine delta."""
    if not VAULT_LOG_PATH.exists():
        return None
    try:
        with open(VAULT_LOG_PATH, 'rb') as f:
            f.seek(-2, 2)
            while f.read(1) != b'\n':
                f.seek(-2, 1)
            last_line = f.readline().decode()
            return json.loads(last_line).get("well_score")
    except:
        return None

def bridge_to_vault(force=False):
    try:
        with open(WELL_STATE_PATH, 'r') as f:
            state = json.load(f)
    except Exception as e:
        return {"status": "ERROR", "message": f"READ_FAILED: {str(e)}"}

    current_score = state.get("well_score", 0)
    last_score = get_last_anchored_score()
    violations = state.get("floors_violated", [])
    
    # 1. Condition logic: High-Signal Only
    is_degraded = len(violations) > 0
    is_low_capacity = current_score < 70
    is_significant_delta = last_score is None or abs(current_score - last_score) >= 10
    
    if not (is_degraded or is_low_capacity or is_significant_delta or force):
        return {"status": "SKIPPED", "message": "Signal-to-noise suppressed. Ledger remains clean."}

    # 2. Build VAULT999 Payload
    payload = {
        "vault_type": "well_event",
        "epoch": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "well_score": current_score,
        "status": "DEGRADED" if is_degraded else "LOW" if is_low_capacity else "STABLE",
        "violations": violations,
        "w0_assertion": "OPERATOR_VETO_INTACT / HIERARCHY_INVARIANT", # Permanent Constitutional Anchor
        "trigger": "VIOLATION" if is_degraded else "CAPACITY" if is_low_capacity else "DELTA" if is_significant_delta else "MANUAL"
    }
    
    payload["hash"] = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    try:
        VAULT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(VAULT_LOG_PATH, 'a') as f:
            f.write(json.dumps(payload) + "\n")
        return {"status": "SUCCESS", "payload": payload}
    except Exception as e:
        return {"status": "ERROR", "message": f"VAULT_WRITE_FAILED: {str(e)}"}

if __name__ == "__main__":
    force_sync = "--force" in sys.argv
    result = bridge_to_vault(force=force_sync)
    print(json.dumps(result, indent=2))


