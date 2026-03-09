# ARCHITECT.md

## arifOS — Architectural Blueprint

### System Identity

**arifOS AAA** is a **governed intelligence kernel** that orchestrates reasoning, consequence evaluation, and constitutional judgment before producing a final decision.

It is implemented as an **MCP-compatible cognitive runtime** using:

* Python **3.12+**
* **FastMCP**
* **uv** runtime environment

The system is designed around **Trinity Architecture**, **Constitutional Floors**, and the **Metabolic Loop execution pipeline**.

---

# 1. Core Philosophy

arifOS is built on three principles:

### 1. Intelligence must reduce entropy

Every operation must move the system toward **clarity, coherence, or resolution**.

### 2. Intelligence must be governed

Reasoning is not enough.
All outputs must pass constitutional validation.

### 3. Human authority remains final

The system is an **instrument**, not a sovereign agent.

---

# 2. Trinity Architecture

The architecture is divided into **three governing domains**.

```
Human Sovereign (888 Judge)
        │
        ▼
Governance Kernel (AAA)
        │
        ▼
Execution Layer (MCP Tools)
```

### Components

| Layer           | Role                                  |
| --------------- | ------------------------------------- |
| Human Sovereign | Final decision authority              |
| AAA Kernel      | Governance + reasoning orchestration  |
| MCP Layer       | Tool execution and system interaction |

---

# 3. The Metabolic Loop

The **Metabolic Loop** is the central execution pipeline.

Every request flows through these stages.

```
000 INIT
   ↓
111 MIND
   ↓
333 ANALYSIS
   ↓
666 HEART
   ↓
777 APEX
   ↓
888 JUDGE
   ↓
999 VAULT
```

---

## Stage Definitions

### 000 INIT

Creates the session anchor and validates request context.

Outputs:

* `session_id`
* `auth_context`
* initial governance state

Tool:

```
init_anchor_state
```

---

### 111 MIND

Performs first-pass reasoning and decomposition.

Tool:

```
reason_mind_synthesis
```

---

### 333 ANALYSIS

Breaks complex problems into structured sub-questions.

Tool:

```
integrate_analyze_reflect
```

---

### 666 HEART

Evaluates ethical and real-world impact.

Tool:

```
assess_heart_impact
```

---

### 777 APEX

Synthesizes reasoning outputs and prepares candidate verdict.

Tool:

```
quantum_eureka_forge
```

---

### 888 JUDGE

Applies the **13 Constitutional Floors**.

Possible verdicts:

```
SEAL
SABAR
VOID
```

Tool:

```
apex_judge_verdict
```

---

### 999 VAULT

Commits approved outcomes.

Tool:

```
seal_vault_commit
```

---

# 4. Constitutional Floors

The system enforces **13 invariant laws** that govern decision integrity.

Examples:

| Floor | Function              |
| ----- | --------------------- |
| F2    | Truth validation      |
| F3    | Tri-witness coherence |
| F11   | Authority continuity  |
| F13   | Sovereignty boundary  |

If any floor fails, execution halts.

Example:

```
F11_AUTHORITY
session_id mismatch
```

---

# 5. Session Continuity Model

Session continuity is mandatory across all stages.

Invariant:

```
session_id == auth_context.session_id
```

If this invariant breaks, the system triggers:

```
F11_AUTHORITY
```

and aborts the pipeline.

---

# 6. MCP Tool Surface

The system exposes tools via **Model Context Protocol (MCP)**.

Primary tools:

```
init_anchor_state
metabolic_loop_router
check_vital
```

Supporting tools:

```
reason_mind_synthesis
integrate_analyze_reflect
assess_heart_impact
quantum_eureka_forge
apex_judge_verdict
seal_vault_commit
```

Diagnostic tools:

```
aclip_system_health
aclip_process_list
aclip_fs_inspect
aclip_log_tail
aclip_net_status
aclip_config_flags
```

---

# 7. Recommended ChatGPT Tool Surface

For reliability, external agents should primarily use:

```
metabolic_loop_router
check_vital
```

The router orchestrates the entire metabolic loop internally.

---

# 8. Canonical Request Contract

### Initialization request

```json
{
  "intent": {
    "query": "string",
    "actor": "string",
    "mode": "string"
  }
}
```

Required field:

```
intent.query
```

---

### Initialization response

```
status: SUCCESS
verdict: SEAL
session_id: uuid
auth_context: {}
```

---

# 9. Response Envelope

All MCP responses should follow the same schema.

### Success

```
status
verdict
session_id
message
data
```

### Error

```
status
error_code
message
session_id
```

Detailed telemetry should only appear when:

```
debug = true
```

---

# 10. Execution Flow Example

```
User query
   ↓
metabolic_loop_router
   ↓
INIT session
   ↓
MIND reasoning
   ↓
ANALYSIS decomposition
   ↓
HEART consequence simulation
   ↓
APEX synthesis
   ↓
JUDGE constitutional validation
   ↓
VAULT commit
   ↓
response returned
```

---

# 11. Failure Modes

Typical system failures include:

| Failure                 | Cause                    |
| ----------------------- | ------------------------ |
| Schema validation error | API contract drift       |
| F11_AUTHORITY           | session mismatch         |
| VOID verdict            | constitutional violation |
| SABAR verdict           | governance pause         |

---

# 12. Debugging Protocol

When debugging the system, always follow this order:

```
1 check_vital
2 tool registry
3 init_anchor_state
4 session continuity
5 router execution
6 constitutional floors
7 response envelope
```

---

# 13. First Action Rule (For AI Agents)

When entering this repository:

```
1 Read GEMINI.md
2 Read ARCHITECT.md
3 Run check_vital
4 Test init_anchor_state
5 Confirm session continuity
6 Only then modify code
```

Never modify the system without first verifying runtime health.

---

# 14. Architectural Design Goals

The system prioritizes:

```
governance
traceability
session continuity
deterministic reasoning
```

Over:

```
speed
automation
agent autonomy
```

---

# 15. Motto

```
DITEMPA, BUKAN DIBERI
Forged, not given.
```
