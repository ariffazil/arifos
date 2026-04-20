"""
arifOS First Metabolic Transition Runner — [IGNITION]

This script executes the first full 000-333 circuit to verify
that the Identity State Machine is tracking the agent's becoming.

DITEMPA BUKAN DIBERI
"""

import asyncio
import os
import sys

# Ensure absolute package imports
sys.path.append(os.getcwd())

from arifosmcp.runtime.state import IDENTITY_MANAGER
from arifosmcp.tools.arifos.control_plane import init_000, sense_111
from arifosmcp.tools.arifos.compute_plane import mind_333

async def ignite_metabolic_cycle():
    print("🔥 arifOS First Metabolic Transition Ignited...")
    
    # 1. INIT: Seed S0
    res_000 = await init_000.execute(None, "arif", "Self-Reflection Ignition")
    print(f"000_INIT  | State: {res_000['identity']['state']} | Continuity: {res_000['identity']['continuity_index']}")

    # 2. SENSE: Process Intent
    res_111 = await sense_111.execute(None, "audit", "arif", "S_0_ignition")
    # Handle flat output or nested data
    intent = res_111.get("data", {}).get("intent_type", res_111.get("intent_type", "GENERAL"))
    print(f"111_SENSE | Intent: {intent} | Vault: {res_111['vault_receipt']}")

    # 3. MIND: Reason on Delta S
    res_333 = await mind_333.execute(None, "analyze value_drift and propose delta_v", "arif", "S_0_ignition")
    # Handle optional decision packet
    conf = res_333.get("data", {}).get("decision_packet", {}).get("confidence", 1.0)
    print(f"333_MIND  | Confidence: {conf} | Trace: {res_333['vault_receipt']}")

    # Final State Check
    curr = IDENTITY_MANAGER.current
    print(f"\n--- Final State Trace ---")
    print(f"ID: {curr.id[:8]} | Hash: {curr.parent_hash[:8]}")
    print(f"Identity Continuity: {curr.continuity_index:.4f}")
    print(f"Drift Score: {curr.drift_score:.4f}")
    print(f"Evolution Note: {IDENTITY_MANAGER.get_evolution_note()}")
    print(f"--- Metabolic Ignition Complete ---")

if __name__ == "__main__":
    asyncio.run(ignite_metabolic_cycle())
