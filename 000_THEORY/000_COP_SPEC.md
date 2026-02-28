# 🏛️ COP: Constitutional Orchestration Protocol (v1.0)

**The Governance Substrate for Agentic AI.**
*Status: Production-Grade Hardened (F1–F13 Verified)*

The **Constitutional Orchestration Protocol (COP)** is a deterministic, server-side governance layer that sits between an LLM (The Mind) and its Tools (The World). It replaces "Soft Prompting" with "Hard Logic Gates" enforced by a $15 VPS.

---

## 1. The Core Architecture: "The Jar"

COP is based on the **Separation of Concerns** between Intelligence and Execution.

* **L1 (Intelligence Layer):** The LLM. Stateless. Probabilistic. Unrestrained.
* **L2 (Orchestration Layer):** **arifOS Python Kernel**. Stateful. Deterministic. Sovereign.
* **L3 (Execution Layer):** MCP Tools. Canonical. Verified. Sandboxed.

---

## 2. The COP Metabolic Loop (The 000→999 Cycle)

Every action requested by an AI must pass through the **Metabolic Loop** before execution:

1. **000_INIT:** Session ignition. F12 Injection Defense normalization.
2. **333_MIND:** The LLM proposes an action with a "Causal Trace" (Why it's doing this).
3. **888_APEX:** The **Amanah Handshake**. The Python kernel runs the 13 Constitutional Floors.
4. **999_VAULT:** Immutable commitment of the verdict to the Merkle-chain ledger.

---

## 3. The Amanah Handshake (HMAC Security)

Governance is not an "opinion"—it is a cryptographic fact.

* **The Token:** A signed `verdict:signature` envelope.
* **The Guard:** `hmac.compare_digest` ensures the token has not been tampered with by the AI brain.
* **The Result:** If the signature fails, the tool call is **VOID**.

---

## 4. The 13 Constitutional Floors

The binary gates that define the "Physical Reality" of the AI.

| Floor | Name | Metric | Function |
| --- | --- | --- | --- |
| **F1** | **Amanah** | Reversibility | Block irreversible harm. |
| **F2** | **Truth** | Confidence | $P(truth) \geq 0.99$. |
| **F4** | **Clarity** | $\Delta S \leq 0$ | Reduce confusion, not increase it. |
| **F9** | **Anti-Hantu** | Agency | AI has no soul; do not simulate one. |
| **F11** | **Auth** | Sovereign ID | Check against the 888_JUDGE badge. |
| **F12** | **Injection** | Risk Weight | Block "ignore previous instructions" ($>0.85$). |
| **F13** | **Sovereign** | Veto | The Human (You) retains the ultimate kill-switch. |

---

## 5. Thermodynamic Operating Laws

COP manages **Entropy**, not just text.

* **Clarity Constraint:** Every interaction must reduce confusion ($\Delta S < 0$).
* **Stability Metric:** The system remains grounded ($Peace^2 \geq 1.0$).
* **Humility Band:** Claims must include uncertainty ($\Omega_0 \in [0.03, 0.05]$).

---

## 6. The "Sovereign Veto" Implementation

If the **COP** detects a state it cannot govern (A "Strange Loop" or "Gödel Lock"), it triggers **888_HOLD**.

* **The Machine Stops.**
* **The Human (Sovereign) Signs.**
* **The World Continues.**

---

## 🚀 Implementation (The "Phython" Way)

```python
# The COP Gatekeeper
@constitutional_floor("F11")
def execute_tool(session_id, tool_name, governance_token):
    # Deterministic HMAC Verification
    if not verify_token(session_id, governance_token):
        return "VOID: Amanah Handshake Failed."
    
    # Tool execution only happens in this protected space
    return run_tool(tool_name)

```

---

**"Akal Memerintah, Amanah Mengunci"**
*Forged, Not Given.*

---

*Last Updated: 2026-02-28*
