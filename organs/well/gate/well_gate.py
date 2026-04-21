# WELL Biological Readiness Mirror
# Role: Informational pre-JUDGE flag for human substrate governance.
# Axiom: W0 — Sovereignty Invariant. WELL holds no veto.

import json
import datetime
from pathlib import Path
import sys

# Topology: Sovereign WELL Root
WELL_STATE_PATH = Path("/root/WELL/state.json")

def reflect_readiness():
    """
    Reflects current well_state for JUDGE context.
    Returns: (status, message, readiness_score, violations)
    """
    if not WELL_STATE_PATH.exists():
        return "UNANCHORED", "WARNING: Biological state unknown. Mirror is dark.", 50, ["W_MISSING"]
    
    try:
        with open(WELL_STATE_PATH, 'r') as f:
            state = json.load(f)
        
        metrics = state.get("metrics", {})
        sleep = metrics.get("sleep", {})
        cognitive = metrics.get("cognitive", {})
        violations = []
        
        # W1: Sleep Integrity Reflection
        if sleep.get("sleep_debt_days", 0) > 2:
            violations.append("W1_SLEEP_DEBT")
        
        # W5: Cognitive Entropy Reflection
        if cognitive.get("clarity", 10) < 4:
            violations.append("W5_COGNITIVE_ENTROPY")
        
        if violations:
            return "DEGRADED", f"[WELL-MIRROR] Biological substrate flagging: {', '.join(violations)}", state.get("well_score", 0), violations
        
        return "STABLE", "[WELL-MIRROR] Substrate stable. Mirror is clear.", state.get("well_score", 100), []
    except Exception as e:
        return "ERROR", f"[WELL-ERROR] Schema mismatch: {str(e)}", 0, ["W_ERROR"]

if __name__ == "__main__":
    status, msg, score, violations = reflect_readiness()
    # Output is always successful (sys.exit(0)) because WELL never blocks alone.
    print(json.dumps({
        "status": status,
        "message": msg,
        "score": score,
        "violations": violations,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }))
    sys.exit(0)
