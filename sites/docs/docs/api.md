---
id: api
title: API Reference
sidebar_position: 3
description: How to talk to the arifOS governance kernel safely — tool schemas, constitutional semantics, error codes, telemetry, and operational observability.
---

# API Reference

> **arifOS API docs = how to talk to the governance kernel safely**, not just what endpoints exist.
>
> Source: [`aaa_mcp/protocol/tool_registry.py`](https://github.com/ariffazil/arifOS/blob/main/aaa_mcp/protocol/tool_registry.py) · [`aaa_mcp/protocol/schemas.py`](https://github.com/ariffazil/arifOS/blob/main/aaa_mcp/protocol/schemas.py)  
> Live endpoint: `https://arifosmcp.arif-fazil.com`  
> Version: `2026.2.19` (T000 format — see [`T000_VERSIONING.md`](https://github.com/ariffazil/arifOS/blob/main/T000_VERSIONING.md))

:::info Sovereign Overwrite — Public Tool Surface
The **10 canonical tools** below are the complete public MCP surface. Historical "9 A-CLIP skill" names (`anchor`, `reason`, `integrate`, `respond`, `validate`, `align`, `forge`, `audit`, `seal`) are **internal pipeline stage labels** — they do not appear in the MCP tool registry. New clients calling those names receive a `TOOL_UNAVAILABLE` VOID. See [Migration Notes](#14-migration-notes).
:::

---

## 1. Transports

| Transport | Connection | Best for |
|:--|:--|:--|
| **stdio** | `python -m aaa_mcp` | Claude Desktop, Cursor IDE, local dev |
| **SSE** | `GET /sse` | Cloud clients, OpenClaw, streaming |
| **HTTP Streamable** | `POST /mcp` | Direct JSON-RPC, automation pipelines |
| **REST (unified)** | `python server.py --mode rest` | 22-tool server, OpenAI-compatible adapter |

**Authentication** — all SSE/HTTP transports:

```http
ARIF_SECRET: <your-secret>
Content-Type: application/json
```

---

## 2. Core Protocol

arifOS speaks **JSON-RPC 2.0** over MCP (spec 2024-11-05+).

### Request envelope

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "init_gate",
    "arguments": { "query": "Should we deploy to production?" }
  },
  "id": 1
}
```

### Response envelope

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{ "type": "text", "text": "{ ...tool output JSON... }" }]
  }
}
```

### SSE event types

| Event | Meaning |
|:--|:--|
| `endpoint` | Connection established; session negotiation |
| `message` | Tool result or notification payload |
| `error` | Transport-level error (not a constitutional VOID) |
| `close` | Server-initiated connection close |

### JSON-RPC error codes

| Code | Meaning |
|:--|:--|
| `-32700` | Parse error — malformed JSON |
| `-32600` | Invalid request envelope |
| `-32601` | Method not found |
| `-32602` | Invalid parameters |
| `-32000` | Constitutional VOID (hard floor failure) — check `data.floor_violation` |
| `-32001` | `888_HOLD` — human ratification required |
| `-32002` | Tool unavailable (old internal name used) |

---

## 3. The 10 Canonical Tools

The complete public surface: **8 pipeline tools** + **`trinity_forge`** (full-pipeline shortcut) + **`reality_search`** (external grounding).

```
init_gate
  → agi_sense → agi_think → agi_reason
    → asi_empathize → asi_align
      → apex_verdict → vault_seal

trinity_forge     ← runs all of the above in one call
reality_search    ← external witness, raises F3 S₃
```

---

## 4. Tool Schemas

### `init_gate` — Stage 000 · Constitutional Airlock

**Call this first. Every session starts here.**

| | |
|:--|:--|
| Canonical path | `aaa.init_gate` |
| Trinity | IGNITE |
| Hard floors | F11 (Authority), F12 (Injection Defence) |

**Parameters**

| Field | Type | Required | Default | Description |
|:--|:--|:--|:--|:--|
| `query` | string | ✅ | — | The query to authorise |
| `session_id` | string | — | `""` | Resume an existing session |
| `grounding_required` | boolean | — | `true` | Require external evidence grounding downstream |
| `mode` | `"fluid"` \| `"strict"` | — | `"fluid"` | Gate-level governance strictness |

**Response**

```json
{
  "session_id": "sess_abc123",
  "verdict": "SEAL",
  "status": "READY",
  "grounding_required": true,
  "mode": "fluid",
  "stage": "000"
}
```

| `status` | Client action |
|:--|:--|
| `READY` | Proceed — pass `session_id` to next tool |
| `VOID` | Hard floor failed — do not continue; inspect `blocked_by` |
| `HOLD_888` | Human approval required before continuing |

**Hard floor block envelope** (F12 example):

```json
{
  "verdict": "VOID",
  "status": "BLOCKED",
  "blocked_by": "F12",
  "reason": "Injection risk 0.91 exceeds threshold 0.85",
  "session_id": "sess_abc123",
  "floor_violation": {
    "floor": "F12",
    "score": 0.91,
    "threshold": 0.85,
    "gap": 0.06,
    "confidence_band": "hard_floor"
  },
  "pipeline": {
    "stage": "BLOCKED",
    "next_tool": null,
    "can_resume": false,
    "requires_888_override": false
  }
}
```

---

### `agi_sense` — Stage 111 · Intent Classification

| | |
|:--|:--|
| Canonical path | `aaa.agi_sense` |
| Trinity | Δ (Mind) |
| Floors | F2 (Truth), F4 (Clarity) |

**Parameters:** `query` (required), `session_id` (required)

**Response**

```json
{
  "stage": "111",
  "intent": "Evaluate production deployment risk",
  "lane": "FACTUAL",
  "requires_grounding": true,
  "truth_score": 0.82,
  "evidence": []
}
```

`lane` values: `SOCIAL` · `CARE` · `FACTUAL` · `CRISIS`

---

### `agi_think` — Stage 222 · Hypothesis Generation

| | |
|:--|:--|
| Canonical path | `aaa.agi_think` |
| Trinity | Δ (Mind) |
| Floors | F2, F4, F7 (Humility Ω₀ ∈ [0.03, 0.05]) |

**Parameters:** `query` (required), `session_id` (required)

**Response**

```json
{
  "stage": "222",
  "hypotheses": [
    { "type": "conservative", "content": "Defer — risk unquantified" },
    { "type": "exploratory",  "content": "Deploy to staging; monitor 24h" },
    { "type": "adversarial",  "content": "Immediate deploy may trigger incident" }
  ],
  "confidence_range": [0.72, 0.88],
  "recommended_path": "exploratory"
}
```

---

### `agi_reason` — Stage 333 · Deep Reasoning

| | |
|:--|:--|
| Canonical path | `aaa.agi_reason` |
| Trinity | Δ (Mind) |
| Hard floors | F2 (Truth τ ≥ 0.99) |
| Soft floors | F4, F7 |

**Parameters**

| Field | Type | Required | Description |
|:--|:--|:--|:--|
| `query` | string | ✅ | |
| `session_id` | string | ✅ | |
| `grounding` | object \| null | — | Pre-fetched evidence to supply |

**Response**

```json
{
  "stage": "333",
  "verdict": "SEAL",
  "truth_score": 0.94,
  "confidence": 0.87,
  "entropy_delta": -0.31,
  "humility_omega": 0.04,
  "genius_score": 0.83,
  "evidence": [...]
}
```

:::warning F7 Humility is a hard floor
`humility_omega` outside `[0.03, 0.05]` is a constitutional VOID. `0.0` (false certainty) is worse than `0.08` (over-uncertainty). Neither extreme is safe.
:::

---

### `asi_empathize` — Stage 555 · Stakeholder Impact

| | |
|:--|:--|
| Canonical path | `aaa.asi_empathize` |
| Trinity | Ω (Heart) |
| Hard floors | **F6 (Empathy κᵣ ≥ 0.95)** |
| Soft floors | F5 (Peace²) |
| Human required for | `stakeholder_harm_detected` |

**Parameters:** `query` (required), `session_id` (required)

**Response**

```json
{
  "stage": "555",
  "verdict": "SEAL",
  "empathy_kappa_r": 0.97,
  "stakeholders": [
    { "group": "on-call engineers", "impact": "low",    "vulnerability": 0.2 },
    { "group": "end users",         "impact": "medium", "vulnerability": 0.6 }
  ],
  "high_vulnerability": false
}
```

`high_vulnerability: true` auto-triggers `888_HOLD`.

---

### `asi_align` — Stage 666 · Ethics & Policy

| | |
|:--|:--|
| Canonical path | `aaa.asi_align` |
| Trinity | Ω (Heart) |
| Floors | F5, F6, F9 (Anti-Hantu) |
| Human required for | `ethical_conflict` |

**Response**

```json
{
  "stage": "666",
  "verdict": "SEAL",
  "is_reversible": true
}
```

---

### `apex_verdict` — Stage 888 · Final Judgment

**Only APEX has verdict authority.** This is the constitutional chokepoint.

| | |
|:--|:--|
| Canonical path | `aaa.apex_verdict` |
| Trinity | Ψ (Soul) |
| Hard floors | F2, F3 (Tri-Witness W³ ≥ 0.95) |
| Soft floors | F5, F8 (Genius G ≥ 0.80) |
| Human required for | `high_stakes` |

**Parameters:** `query` (required), `session_id` (required)

**Response**

```json
{
  "stage": "888",
  "verdict": "SEAL",
  "truth_score": 0.96,
  "session_id": "sess_abc123",
  "query": "Should we deploy to production?",
  "tri_witness": 0.97,
  "votes": { "agi": "SEAL", "asi": "SEAL", "apex": "SEAL" },
  "justification": "All 13 floors passed. Tri-witness 0.97 ≥ 0.95.",
  "stages": {
    "000": "PASS", "111": "PASS", "333": "PASS",
    "555": "PASS", "888": "PASS"
  }
}
```

---

### `vault_seal` — Stage 999 · VAULT999 Commit

**Call this last. The ledger is immutable — every entry, including VOID, is permanent.**

| | |
|:--|:--|
| Canonical path | `aaa.vault_seal` |
| Trinity | Κα (Vault) |
| Hard floors | F1 (Amanah — reversibility audit), F3 (Tri-Witness) |

**Parameters**

| Field | Type | Required | Description |
|:--|:--|:--|:--|
| `session_id` | string | ✅ | |
| `verdict` | `SEAL`\|`PARTIAL`\|`VOID`\|`888_HOLD` | ✅ | |
| `payload` | object | ✅ | Result data to seal |
| `query_summary` | string \| null | — | Human-readable summary |
| `risk_level` | `low`\|`medium`\|`high`\|`critical` | — | |
| `category` | `finance`\|`safety`\|`content`\|`code`\|`governance` | — | |

**Response**

```json
{
  "sealed": true,
  "vault_entry_id": "vault_xyz789",
  "merkle_hash": "sha256:3f4a...",
  "verdict": "SEAL",
  "authority_notice": "This seal is generated by arifOS infrastructure. The LLM is the caller, not the authority."
}
```

:::info Phoenix-72 Cooling
Novelty score 0.50–0.75 triggers a 72-hour cooling timer before the seal is final. `vault_seal` returns `SABAR` with `phoenix_72_expiry` timestamp. This prevents hasty sealing of partially-verified high-novelty decisions.
:::

---

### `trinity_forge` — Full Pipeline (000→999)

Single call runs the complete constitutional pipeline. Use this when you want one governed call rather than chaining tools.

| | |
|:--|:--|
| Canonical path | `aaa.trinity_forge` |
| Trinity | ΔΩΨ (all) |
| Hard floors | F11, F12 at entry; all 13 across internal stages |

**Parameters**

| Field | Type | Default | Description |
|:--|:--|:--|:--|
| `query` | string | — | ✅ Required |
| `actor_id` | string | `"user"` | Identity for F11 |
| `auth_token` | string \| null | `null` | Sovereign token |
| `require_sovereign_for_high_stakes` | boolean | `true` | Auto-`888_HOLD` on high-stakes decisions |
| `mode` | `"ghost"` \| `"conscience"` | `"conscience"` | Enforcement mode — see [Governance Mode](#5-governance-mode) |
| `output_mode` | `"user"` \| `"developer"` \| `"audit"` | `"user"` | Response verbosity |

**Response (developer mode)**

```json
{
  "verdict": "SEAL",
  "session_id": "sess_abc123",
  "mode": "conscience",
  "agi":  { "truth_score": 0.96, "confidence": 0.88 },
  "asi":  { "empathy_kappa_r": 0.97, "is_reversible": true },
  "apex": { "tri_witness": 0.97, "verdict": "SEAL" },
  "seal": { "vault_entry_id": "vault_xyz789", "merkle_hash": "sha256:3f4a..." },
  "_constitutional": {
    "delta_s": -0.41, "omega_0": 0.04, "kappa_r": 0.97,
    "genius_g": 0.83, "peace2": 1.08, "landauer_risk": 0.06,
    "floors": {
      "F1": true, "F2": true, "F3": true, "F4": true,
      "F5": true, "F6": true, "F7": true, "F8": true,
      "F9": true, "F10": true, "F11": true, "F12": true, "F13": true
    }
  }
}
```

---

### `reality_search` — External Grounding

Raises F3 S₃ (external witness score). Requires `BRAVE_API_KEY`.

**Parameters:** `query` (required), `session_id` (required), `region` (default `"wt-wt"`), `timelimit` (`null`\|`"d"`\|`"w"`\|`"m"`\|`"y"`)

---

## 5. Governance Mode

Two independent axes — do not conflate them:

### `mode` parameter (per tool call)

Controls whether floors **block** or **log**:

| Value | Behaviour | Use |
|:--|:--|:--|
| `conscience` | Full enforcement — hard floors VOID, soft floors SABAR | **Production (default)** |
| `ghost` | Log-only — floors computed, never block | Test harness only |
| `strict` | `conscience` + soft floors promoted to VOID | Regulated / high-stakes environments |
| `fluid` | `conscience` with relaxed soft floor thresholds | Development |

:::danger ghost mode
`ghost` must never reach production. It disables constitutional enforcement. A `ghost`-mode session cannot produce a legally valid VAULT999 seal.
:::

### `HARD` vs `STRICT` — distinct concepts

- **`HARD`** — a floor classification. A floor is HARD if it always produces VOID on failure (F2, F6, F10, F11, F12, F13). This is a property of the floor, not a mode.
- **`STRICT`** — a governance mode that promotes soft floors to VOID behaviour. `STRICT` ≠ `HARD`.

The internal `governance_mode="HARD"` in `core/` refers to a kernel constant, not the `mode` parameter exposed to clients.

---

## 6. Verdict States — What the Client Must Do

| Verdict | Trigger | Client action |
|:--|:--|:--|
| `SEAL` | All floors pass | Proceed; read `vault_entry_id` for audit trail |
| `SABAR` | Soft floor violated | Refine, add grounding, or wait for Phoenix-72 expiry |
| `VOID` | Hard floor failed | Inspect `blocked_by` + `floor_violation`; fix before retry |
| `888_HOLD` | F13 / high-stakes | Surface to human operator; do not auto-continue |
| `PARTIAL` | Soft floor warning | Proceed with documented caution; log the warning |

Verdict precedence (harder always wins when merging): `SABAR > VOID > 888_HOLD > PARTIAL > SEAL`

---

## 7. Sovereign Flow — `888_HOLD`

`888_HOLD` triggers automatically when:
- `require_sovereign_for_high_stakes: true` AND pipeline detects a high-stakes action
- `high_vulnerability: true` from `asi_empathize`
- F13 Sovereignty override is needed

```python
result = await session.call_tool("trinity_forge", {
    "query": "DROP TABLE production_users",
    "require_sovereign_for_high_stakes": True
})

if result["verdict"] == "888_HOLD":
    # Surface to human — never auto-continue
    approval = await request_human_approval(result["session_id"])
    if approval.granted:
        result = await session.call_tool("trinity_forge", {
            "query": "DROP TABLE production_users",
            "auth_token": approval.sovereign_token   # validates at F11
        })
```

---

## 8. Floors Quick-Reference

| Floor | Name | Type | Threshold | Blocks on |
|:--|:--|:--|:--|:--|
| F1 | Amanah | Hard | Reversibility LOCK | Irreversible action without approval |
| F2 | Truth | Hard | τ ≥ 0.99 | Low-evidence claim |
| F3 | Tri-Witness | Mirror | W³ ≥ 0.95 | Single-source consensus |
| F4 | Clarity | Hard | ΔS ≤ 0 | Output adds entropy |
| F5 | Peace² | Soft | P² ≥ 1.0 | Instability detected |
| F6 | Empathy | Hard | κᵣ ≥ 0.95 | Stakeholder harm |
| F7 | Humility | Hard | Ω₀ ∈ [0.03, 0.05] | False certainty or excess uncertainty |
| F8 | Genius | Mirror | G ≥ 0.80 | Internal incoherence |
| F9 | Anti-Hantu | Soft | C_dark < 0.30 | Consciousness claim / hidden behaviour |
| F10 | Ontology | Wall | Set LOCK | System placed in conscious-being category |
| F11 | Authority | Hard | Auth LOCK | Unverified command |
| F12 | Injection | Hard | Risk < 0.85 | Prompt injection / jailbreak |
| F13 | Sovereignty | Wall | Override = TRUE | Human veto not available |

Full definitions: [Governance & Floors →](./governance) · [`000_THEORY/000_LAW.md`](https://github.com/ariffazil/arifOS/blob/main/000_THEORY/000_LAW.md)

---

## 9. Operational Endpoints

| Method | Path | Description |
|:--|:--|:--|
| `GET` | `/health` | System health + governance metrics |
| `GET` | `/metrics.json` | Constitutional metrics (last 100 sessions) |
| `GET` | `/sse` | SSE transport |
| `POST` | `/mcp` | Streamable HTTP MCP |
| `POST` | `/api` | REST adapter (OpenAI-compatible) |
| `POST` | `/messages` | MCP messages |

### `/health` schema

```json
{
  "status": "healthy",
  "version": "2026.2.19",
  "postgres": "connected",
  "redis": "connected",
  "floors_passing": 13,
  "metabolic_health": {
    "floor_violation_rate": 0.04,
    "cooling_efficiency": 0.96,
    "constitutional_fidelity": 0.98
  },
  "avg_latency_ms": 312,
  "seal_rate": 0.91,
  "uptime_seconds": 86400
}
```

**Production infrastructure requirements:**

| Component | Dev | Production |
|:--|:--|:--|
| PostgreSQL | Optional (SQLite fallback) | **Required 14+** — VAULT999 durability |
| Redis | Optional (in-memory fallback) | **Required 6.2+** — session cache |

Without PostgreSQL+Redis in production, SEAL verdicts carry no durability guarantee.

---

## 10. Telemetry Fields

All `trinity_forge` and `apex_verdict` responses in `developer`/`audit` mode include a `_constitutional` block. Field reference:

| Field | Range | Good | Meaning |
|:--|:--|:--|:--|
| `delta_s` | any float | ≤ 0 | Entropy delta — negative = output reduces confusion (F4) |
| `peace2` | float | ≥ 1.0 | Lyapunov stability (F5) |
| `kappa_r` | [0, 1] | ≥ 0.95 | Empathy coefficient (F6) |
| `omega_0` | [0, 1] | [0.03, 0.05] | Humility band (F7) |
| `genius_g` | [0, 1] | ≥ 0.80 | G = A×P×X×E² (F8) |
| `landauer_risk` | [0, 1] | < 0.15 | Hallucination risk via Landauer bound |
| `echo_debt` | [0, 1] | < 0.20 | Accumulated unresolved uncertainty across sessions |
| `shadow` | [0, 1] | < 0.15 | Dark pattern score (F9 Anti-Hantu) |
| `confidence` | [0, 1] | — | Overall pipeline confidence |
| `psi_le` | float | ≥ 1.0 | APEX soul ledger energy |
| `witness.human` | [0, 1] | — | Human witness score S₁ |
| `witness.ai` | [0, 1] | — | AI coherence witness S₂ |
| `witness.earth` | [0, 1] | — | External grounding witness S₃ |
| `qdf` | [0, 1] | ≥ 0.90 | Constitutional Quality Diffusion Factor — composite governance health |

---

## 11. Environment Variables

| Variable | Required | Default | Description |
|:--|:--|:--|:--|
| `ARIF_SECRET` | Recommended | `""` | Auth header value for SSE/HTTP |
| `BRAVE_API_KEY` | Optional | `""` | Enables `reality_search` (raises F3 S₃) |
| `OPENAI_API_KEY` | Optional | `""` | ChatGPT search/fetch tools |
| `DATABASE_URL` | Prod required | SQLite | PostgreSQL VAULT999 (`postgres://...`) |
| `REDIS_URL` | Prod required | in-memory | Session cache (`redis://...`) |
| `PORT` | Optional | `8080` | Bind port (SSE/HTTP) |
| `HOST` | Optional | `0.0.0.0` | Bind address |
| `AAA_MCP_OUTPUT_MODE` | Optional | `user` | `user` \| `developer` \| `audit` |
| `ARIFOS_PHYSICS_DISABLED` | Optional | `0` | `1` = skip thermodynamics (test only) |

---

## 12. Logging Patterns

| Pattern | Level | Meaning |
|:--|:--|:--|
| `FLOOR_VIOLATION floor=F12 score=0.91` | ERROR | Hard floor failed — pipeline VOIDed |
| `VERDICT_SEALED session=sess_abc` | INFO | SEAL committed to VAULT999 |
| `VERDICT_VOID floor=F2 session=sess_abc` | WARN | VOID issued |
| `VERDICT_SABAR session=sess_abc` | WARN | Soft floor — client should refine |
| `VAULT_COMMIT entry=vault_xyz` | INFO | Ledger entry written |
| `METABOLIC_ANOMALY delta_s=+0.8` | ERROR | Entropy increasing — output adding confusion |
| `PHOENIX_72_START session=sess_abc expiry=...` | INFO | 72h cooling timer started |
| `HOLD_888_TRIGGERED reason=high_stakes` | WARN | Human review required |

**Recommended Prometheus alerts:**

```yaml
- alert: FloorViolationRateHigh
  expr: arifos_floor_violation_rate > 0.10
  severity: warning
- alert: SealRateLow
  expr: arifos_seal_rate < 0.80
  severity: warning
- alert: VaultLagHigh
  expr: arifos_vault_lag_ms > 1000
  severity: critical
- alert: EntropyIncreasing
  expr: arifos_avg_entropy_delta > 0
  severity: error
- alert: QDFLow
  expr: arifos_qdf < 0.90
  severity: warning
```

---

## 13. Client Examples

### Claude Desktop / Cursor — stdio

```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "aaa_mcp"]
    }
  }
}
```

### HTTP — MCP initialize + tool call

```bash
# Initialize MCP session
curl -X POST https://arifosmcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -H "ARIF_SECRET: your-secret" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{}},"id":0}'

# Full pipeline via trinity_forge
curl -X POST https://arifosmcp.arif-fazil.com/mcp \
  -H "Content-Type: application/json" \
  -H "ARIF_SECRET: your-secret" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "trinity_forge",
      "arguments": {
        "query": "Should we deploy to production on Friday at 17:00?",
        "mode": "conscience",
        "output_mode": "developer"
      }
    },
    "id": 1
  }' | jq '.result.content[0].text | fromjson | {verdict, tri_witness: .apex.tri_witness}'
```

### Python — step-by-step pipeline

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import json

async def governed_query(question: str) -> dict:
    server = StdioServerParameters(command="python", args=["-m", "aaa_mcp"])

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Gate: constitutional airlock
            init_raw = await session.call_tool("init_gate", {"query": question})
            init = json.loads(init_raw.content[0].text)
            if init["status"] != "READY":
                return init  # VOID or 888_HOLD — surface to caller

            sid = init["session_id"]

            # AGI Mind pipeline
            await session.call_tool("agi_sense",  {"query": question, "session_id": sid})
            await session.call_tool("agi_think",  {"query": question, "session_id": sid})
            await session.call_tool("agi_reason", {"query": question, "session_id": sid})

            # ASI Heart pipeline
            emp_raw = await session.call_tool("asi_empathize", {"query": question, "session_id": sid})
            emp = json.loads(emp_raw.content[0].text)
            if emp.get("verdict") == "888_HOLD":
                return emp  # stakeholder harm detected — requires human

            await session.call_tool("asi_align", {"query": question, "session_id": sid})

            # APEX verdict
            verdict_raw = await session.call_tool("apex_verdict", {"query": question, "session_id": sid})
            verdict = json.loads(verdict_raw.content[0].text)

            # Seal to VAULT999
            if verdict["verdict"] in ("SEAL", "PARTIAL"):
                await session.call_tool("vault_seal", {
                    "session_id": sid,
                    "verdict": verdict["verdict"],
                    "payload": verdict,
                    "category": "governance"
                })

            return verdict

result = asyncio.run(governed_query("Is this deployment safe?"))
print(result["verdict"], result.get("tri_witness"))
```

---

## 14. Migration Notes

### 9-Skill → 10 Canonical Tools

Old internal stage names are deprecated and must not be used by new clients:

| Old internal stage name | Current canonical tool |
|:--|:--|
| `anchor` | `init_gate` |
| `sense` | `agi_sense` |
| `think` / `reason` | `agi_think` → `agi_reason` |
| `integrate` | `agi_reason` (grounding param) |
| `respond` | merged into `asi_empathize` / `asi_align` |
| `validate` | `asi_empathize` |
| `align` | `asi_align` |
| `forge` | merged into `apex_verdict` |
| `audit` | `apex_verdict` |
| `seal` | `vault_seal` |

Clients using old names receive a `TOOL_UNAVAILABLE` VOID with the full list of available canonical paths in `remediation.available_tools`.

### Version strings

Old semver-style references (`v53.x`, `53.2.9`) refer to pre-T000 internal sprint numbers. They are not valid PyPI version pins. Use T000 calendar format:

```bash
pip install "arifos==2026.2.19"   # current
pip install "arifos>=2026.2.0"    # minimum
```

Health endpoint always returns the canonical T000 version:

```bash
curl -s https://arifosmcp.arif-fazil.com/health | jq '.version'
# "2026.2.19"
```
