# arifOS — L3: BODY (CONNECTION SPEC)
**The Servant Wire — How to plug the Mind into the Body.**

---

## 🛠️ I. The Wire (Transport Matrix)

The AAA MCP is the transport layer of the arifOS Body. It provides the physical connectivity between an AI agent and the Sovereign OS.

### **Connection Methods**

1.  **STDIO (Local):** For CLI-based agents (e.g., 
px @ariffazil/aaa-mcp).
2.  **SSE/HTTP (Remote):** For distributed agents (e.g., https://arifosmcp.arif-fazil.com/mcp).
3.  **Direct IPC:** For sandboxed or kernel-integrated agents.

---

## 🤝 II. The Handshake (SALAM Protocol)

Before any tool is used, a power-on handshake is required to establish session identity.

1.  **Tool:** init_anchor
2.  **Mode:** orge
3.  **Input:** gent_id, ole, signed_intent (optional).
4.  **Response:** session_token.

### **The Token Rule**
Every subsequent tool call **MUST** forward the session_token in the uth_context field. Failure to do so triggers **F11 (Authority)** and blocks the action.

---

## 🏗️ III. The 11-Tool Surface

The Wire exposes exactly 11 "Mega-Tools." Each is an entry point into the Body's execution pipeline.

| Tool | Floor | Primary Function |
|---|---|---|
| init_anchor | F11 | Session Forge & Identity |
| rifOS_kernel | F13 | Sovereign Orchestration |
| ault_ledger | F13 | ZKPC Sealing & Audit |
| gi_mind | F8 | Intellectual Reason & Scoring |
| si_heart | F6 | Conscience & Impact Audit |
| pex_soul | F7 | Final Constitutional Verdict |
| physics_reality| F2 | Grounding & Evidence Search |
| engineering_memory| F10 | Long-term Vector Retrieval |
| math_estimator | F4 | Thermodynamic Quantification |
| code_engine | — | Sandboxed Script Execution |
| rchitect_registry| — | Structural Dependency Mapping |

---

## 🛡️ IV. Security Standards

- **Signed Intent Envelopes:** High-stakes operations (Writes/Deploys) require a physical atification_token from the 888_JUDGE.
- **Credential Scrubbing:** The Wire automatically scrubs secrets from all outputs.
- **Shadowing:** Every action is mirrored to the ault_audit table in Postgres for forensic replay.

---

*The Wire is the servant; the OS is the sovereign.*

---

## 🔒 V. The Wire Lock (Constitutional Boundary)

**AAA Wire SHALL NOT originate policy; it only carries intents and returns artifacts under the rigid constraints of the L2 Mind.** 

The Body is an instrument of service, never an architect of law. Any attempt by the Wire to self-govern or bypass the 13 Floors results in an immediate **VOID** verdict and system halt.
