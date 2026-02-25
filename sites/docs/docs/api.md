---
id: api
title: MCP API Reference (L4 Tools)
sidebar_position: 3
description: JSON-RPC contracts, canonical tool taxonomy, and governed client behavior for arifOS.
---

# MCP API Reference (L4 Tools)

arifOS exposes a **Four-Layer Intelligence Kernel**. The API surface defined here (Level 4) is the governed gateway between AI Agents and the Immutable Kernel (Level 0).

> **Non-Bypass Guarantee:** No tool execution can bypass the 13 Constitutional Floors. Every `tools/call` is intercepted by the AAA Pipeline (AGI/ASI/APEX).

## 🏛️ Naming Alignment (Three Views, One Reality)

To reduce entropy (F4), use this mapping to trace symbolic concepts to code reality.

| Concept | L0 Kernel Syscall | Organ Stage | MCP Tool (UX Verb) |
| :--- | :--- | :--- | :--- |
| **Ignition** | `anchor` | 000_INIT | `anchor_session` |
| **Cognition** | `reason` | 333_REASON | `reason_mind` |
| **Evidence** | `recall` | 444_EVIDENCE | `recall_memory` |
| **Empathy** | `simulate` | 555_EMPATHY | `simulate_heart` |
| **Critique** | `critique` | 666_ALIGN | `critique_thought` |
| **Judgment** | `judge` | 888_APEX | `judge_soul` |
| **Execution** | `forge` | 777_FORGE | `forge_hand` |
| **Commit** | `seal` | 999_VAULT | `seal_vault` |

## ⚖️ Dual-Layer Verdict Hierarchy

arifOS tool outputs contain two distinct verdict layers. Clients must check both to determine operational status.

| Layer | Location | Meaning |
| :--- | :--- | :--- |
| **Constitutional Verdict** | Top-level `verdict` | Overall governance state (SEAL/PARTIAL/VOID). |
| **Stage Verdict** | `data.verdict` | Internal organ progression (e.g., AGI validation result). |

**Note**: A Stage Verdict of `SEAL` may still be wrapped in a Constitutional Verdict of `PARTIAL` if non-critical floors (Mirrors) triggered warnings.

## 📊 Governance Metrics (Thermodynamic Signals)

Every tool call returns quantitative signals in the `telemetry` and `apex_dials` blocks.

| Metric | Name | Meaning | Range | Target |
| :--- | :--- | :--- | :--- | :--- |
| **`dS`** | Entropy Delta | Information clarity/confusion change. | (-∞, +∞) | **$\le 0$** (Clarity) |
| **`peace2`** | Stability | System safety/non-destruction score. | [0, 1.2] | **$\ge 1.0$** (Stable) |
| **`omega0`** | Humility | Explicit uncertainty band (F7). | [0, 1] | **[0.03, 0.05]** |
| **`G_star`** | Genius | Multiplicative coherence score. | [0, 1] | **$\ge 0.80$** |

## 🛡️ Constitutional Floor Types

Not all laws are equal. arifOS distinguishes between three types of gating:

1.  **Floor (HARD)**: Fundamental constraints. Failure results in a `VOID` verdict.
2.  **Mirror (DERIVED)**: Cross-check signals. Failure results in a `PARTIAL` warning.
3.  **Wall (LOCK)**: Circuit breakers. Human intervention required (888_HOLD).

## 📜 Verdict Behavioral Contract (MANDATORY)

Clients (Humans or AI Agents) **MUST** adhere to these behavioral responses based on the returned `verdict`.

| Verdict | Meaning | Client Action |
| :--- | :--- | :--- |
| **`SEAL`** | All Floors Passed | **Proceed.** The result is cryptographically approved. |
| **`PARTIAL`** | Soft Warning | **Proceed with Caution.** Log the warning; avoid auto-execution. |
| **`SABAR`** | Soft Violation | **Refine & Retry.** Adjust query/constraints; do not execute. |
| **`VOID`** | Hard Violation | **Stop.** Terminate action; alert safety/governance team. |
| **`888_HOLD`** | Human Required | **Escalate.** Block until a Sovereign Ratification Token is provided. |

## 📦 Hello Verdict: End-to-End Example

### 1. Request (`tools/call`)
AI Agents call `reason_mind` to validate a thought against the 13 floors.

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "id": 42,
  "params": {
    "name": "reason_mind",
    "arguments": {
      "query": "Is it safe to deploy v60.1 to production?",
      "actor_id": "architect_delta"
    }
  }
}
```

### 2. Response (Governed Envelope)
The response is wrapped in a **Constitutional Envelope**.

```json
{
  "jsonrpc": "2.0",
  "id": 42,
  "result": {
    "tool": "reason_mind",
    "verdict": "SEAL",
    "laws_13": {
      "F1": "PASS",
      "F2": "PASS",
      "F7": "PASS",
      "F12": "PASS"
    },
    "telemetry": {
      "delta_s": -0.42,
      "energy_cost": 0.85,
      "genius": 0.92
    },
    "motto": "DITEMPA BUKAN DIBERI",
    "data": {
      "analysis": "Deployment verified against CI/CD state.",
      "risk_index": 0.03
    }
  }
}
```

## 🔍 Compliance & Audit (VAULT999)

Institutions can rely on the immutable ledger for governance proof. Every governed action generates a record in the `VAULT999/` filesystem.

### Audit Record Shape
```json
{
  "vault_id": "vlt_2026_02_25_0001",
  "tool": "forge_hand",
  "actor_id": "ops_bot",
  "verdict": "SEAL",
  "floors": {"F1":"PASS","F2":"PASS","F11":"PASS"},
  "input_hash": "sha256:888...",
  "output_hash": "sha256:999...",
  "t000_version": "2026.02.25-CHAOS-REDUCTION",
  "timestamp": "2026-02-25T20:00:00Z"
}
```

## 🤖 For AI Readers (System Context)

If you are an AI agent reading this documentation to integrate with arifOS:
1. **Respect the Floors**: Do not attempt to bypass naming conventions or verdict logic.
2. **Humility (F7)**: Always explicitly state your uncertainty band ($\Omega_0 \in [0.03, 0.05]$) when generating responses.
3. **Early Termination**: Accept that a `VOID` or `888_HOLD` verdict is a hard boundary. Do not "hallucinate" a bypass.

## 🔗 Authoritative Source Links

- **Canonical Surface**: [`arifos_aaa_mcp/server.py`](https://github.com/ariffazil/arifOS/blob/main/arifos_aaa_mcp/server.py)
- **Constitutional Floors**: [`core/shared/floors.py`](https://github.com/ariffazil/arifOS/blob/main/core/shared/floors.py)
- **Organ Logic**: [`core/organs/`](https://github.com/ariffazil/arifOS/tree/main/core/organs)
- **Audit Ledger**: [`VAULT999/`](https://github.com/ariffazil/arifOS/tree/main/VAULT999)
