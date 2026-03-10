---
id: api
title: MCP API Reference (L4 Tools)
sidebar_position: 3
description: JSON-RPC contracts, protocol negotiation, and canonical arifOS AAA MCP tool surface.
---

# MCP API Reference (The "Tools Menu")

If you are building an AI agent or connecting arifOS to an app like Claude Desktop, this page lists the specific tools the AI is allowed to use. 

Unlike a normal API where tools just execute blindly, arifOS exposes a **"governed"** surface using the Model Context Protocol (MCP). This means every time the AI tries to use a tool, arifOS intercepts the request and runs it through the 13 constitutional safety gates before letting the action happen.

## Protocol versioning

- Current protocol: `2025-11-25`
- Supported versions: `2025-11-25`, `2025-03-26`
- Negotiated during `initialize`; one session must use one agreed version.

## JSON-RPC call shape

```json
{
  "jsonrpc": "2.0",
  "id": 42,
  "method": "tools/call",
  "params": {
    "name": "reason_mind_synthesis",
    "arguments": {
      "query": "Is this deployment ready?",
      "session_id": "sess_abc",
      "auth_context": { ... }
    }
  }
}
```

## Tool Surface Is Layered

- Public profile (`ARIFOS_PUBLIC_TOOL_PROFILE=chatgpt`): small, stable operator interface.
- Full profile (`ARIFOS_PUBLIC_TOOL_PROFILE=full`): internal 10-tool constitutional assembly line.

### Public Tool Interface (`chatgpt` profile)

| Tool | Role |
|------|------|
| `arifOS.kernel` | One-call governed constitutional execution entrypoint. |
| `search_reality` | External grounding and source discovery. |
| `ingest_evidence` | Fetch/read evidence from URL sources. |
| `session_memory` | Session context and reasoning artifact memory. |
| `audit_rules` | Read-only constitutional audit surface. |
| `check_vital` | Read-only runtime health surface. |
| `open_apex_dashboard` | Opens the APEX Sovereign Dashboard (MCP App). |

Legacy alias: `metabolic_loop_router` refers to `arifOS.kernel`.

`arifOS.kernel` accepts a claimed `actor_id` for routing intent, but continuity is established by `auth_context`. For the first anchored call, run `init_anchor_state`; for subsequent governed calls, pass the returned `auth_context` back into `arifOS.kernel`.

## Canonical 10-Tool Metabolic Stack (`full` profile)

The core governance assembly line. These tools must be called in sequence (000→999) to reach a sealed action.

| Stage | Tool Name | Role |
|-------|-----------|------|
| 000 | `init_anchor_state` | Governed session bootstrap. Mints auth chain. |
| 111 | `integrate_analyze_reflect` | Problem framing and integrative analysis. |
| 333 | `reason_mind_synthesis` | Multi-step reasoning with Eureka synthesis slot. |
| 444 | `metabolic_loop_router` | Full 000→999 pipeline orchestrator (internal legacy name for `arifOS.kernel`). |
| 555 | `vector_memory_store` | BBB associative vector memory (store/recall/search). |
| 666A | `assess_heart_impact` | Empathy and ethical safety engine. |
| 666B | `critique_thought_audit` | Adversarial internal thought audit. |
| 777 | `quantum_eureka_forge` | Sandboxed discovery actuator. Proposes actions. |
| 888 | `apex_judge_verdict` | Constitutional judgment. Produces governance token. |
| 999 | `seal_vault_commit` | Immutable VAULT999 ledger sealing. Append-only. |

### Stage 222 Reality Verification (inside the kernel)

`arifOS.kernel` (legacy internal: `metabolic_loop_router`) executes an explicit `222_REALITY` policy stage between `333_MIND` and `666_HEART` for configured risk tiers, then forwards grounding status into `888_JUDGE` synthesis.

## Resources and prompts

The server exposes read-only resources and orchestration prompts for LLMs:

- **Resources:** `canon://index`, `canon://tools`, `canon://floors`, `governance://law`, `schema://tools/output`, `vault://latest`, `telemetry://summary`, `ui://apex/dashboard-v2.html`.
- **Prompts:** `arifos_kernel_prompt`, `search_reality_prompt`, `ingest_evidence_prompt`, `session_memory_prompt`, `audit_rules_prompt`, `check_vital_prompt`, `open_apex_dashboard_prompt`.

URL mapping for operators:
- **Widget domain / app origin**: `https://arifosmcp.arif-fazil.com`
- **MCP endpoint**: `https://arifosmcp.arif-fazil.com/mcp`
- **Dashboard page**: `https://arifosmcp.arif-fazil.com/dashboard/`

## Response Envelope (`RuntimeEnvelope`)

Every tool returns a structured JSON contract containing the **APEX 5-Layer Stack**:

```json
{
  "verdict": "SEAL | PARTIAL | SABAR | VOID | HOLD-888",
  "stage": "888_APEX",
  "session_id": "sess_a1b2c3d4",
  "apex_output": {
    "capacity_layer": { "A": 0.95, "P": 1.0, "X": 0.9, "capacity_product": 0.855 },
    "effort_layer": { "E": 0.9, "effort_amplifier": 0.81, "reasoning_steps": 1, "tool_calls": 1 },
    "entropy_layer": { "H_before": 1.0, "H_after": 0.9, "delta_S": -0.1 },
    "efficiency_layer": { "compute_cost": 60.0, "entropy_removed": 0.1, "intelligence_efficiency": 0.001667 },
    "governed_intelligence": { "G_star": 0.6925, "efficiency": 0.001667, "governed_score": 0.001154 }
  },
  "auth_context": {
    "actor_id": "user",
    "token_fingerprint": "...",
    "nonce": 42
  },
  "data": {
    "result": "...",
    "timestamp": "2026-03-08T12:00:00Z"
  }
}
```

### Verdict Behavior

*(Curious how these look in practice? [View the live APEX Dashboard](https://arifosmcp.arif-fazil.com/dashboard/))*

- **✅ `SEAL`** -> Approved. Passed all 13 laws and the $G^\dagger \ge 0.80$ gate.
- **🟡 `PARTIAL`** -> Approved with constraints. Soft floors failed or low $G^\dagger$.
- **⚠️ `SABAR`** -> Hold/Refine. Blocked temporarily; AI must refine reasoning.
- **❌ `VOID`** -> Blocked entirely. Hard floor violation (Truth, Auth, Injection).
- **🛑 `HOLD-888`** -> Blocked. Requires explicit cryptographic signature from human.

## Session Contrast Note

Current kernel outputs expose per-call governance deltas (`score_delta`), telemetry, and stage traces. They do **not** yet expose a first-class turn-to-turn contrast metric (for example semantic drift vs previous turn). For now, use `trace_replay` for sealed historical traces and treat contrast analytics as a planned capability.
