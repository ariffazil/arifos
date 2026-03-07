# arifOS Recovery Doctrine: Active Healing (The Phoenix Protocol)

This document formalizes the mechanisms for self-healing and failure recovery within the arifOS kernel.

---

## 1. Failure Taxonomy

| Type | Severity | Mechanism | Trigger |
| :--- | :--- | :--- | :--- |
| **Constitutional Breach** | HIGH | Quarantine | Repeated Violation of Hard Floors (F2, F5, F11). |
| **Homeostatic Collapse** | CRITICAL | Rollback | Energy < 0 or Entropy (ΔS) > Threshold. |
| **Tool Failure** | LOW | Retry/Sabar | External L3 system error. |

---

## 2. Agent Quarantine Logic (The Cooling Tank)

When an agent process in **Operation (L2)** breaches a Hard Floor, it is moved to the **Quarantine Subsystem** (`core/recovery/quarantine.py`).

1. **Detection**: The `agent_registry` tracks violation counts.
2. **Isolation**: If violation count ≥ 3, the agent status is set to `QUARANTINED`.
3. **Cooling**: The agent's priority is set to zero, and it is excluded from the Metabolic Scheduler.
4. **Resurrection**: Only the **888 Judge** can manually release an agent from quarantine.

## 3. State Rollback Logic (Ψ-Restoration)

If a session's **Governance Kernel (Ψ)** reaches a state of homeostatic collapse (e.g., irreversible damage detected in Stage 888), the **Rollback Engine** (`core/recovery/rollback_engine.py`) is engaged.

1. **Checkpoints**: The system automatically saves a deep-copy of the kernel state at the start of every metabolic loop.
2. **Detection**: Triggered by a `HomeostaticCollapse` exception or APEX VOID verdict with high irreversibility.
3. **Restoration**: The session state is replaced with the last known "Healthy" checkpoint.
4. **Audit**: The rollback event is logged in **VAULT999** with a `Rollback-Signature`.

---

**DITEMPA BUKAN DIBERI — Forged, Not Given**
