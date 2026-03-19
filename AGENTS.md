# arifOS MCP Kernel — AGENTS.md
**Version:** 2026.03.19-REALITY-SEALED  
**Runtime:** arifos-aaa-mcp v2026.03.14-VALIDATED  
**Contract:** Constitutional governance layer via MCP — 000→999 pipeline, F1–F13 floors, sBERT ML enforcement

---

## What This Server Does

arifOS MCP is the **constitutional spine** for any AI agent (ChatGPT, Claude, OpenClaw, arifOS_bot, etc.) that needs governed execution. It transforms "ask → answer" into **"ask → anchor → reason → memory → critique → judge → seal"** with hard floors on reversibility, truth, and human dignity.

**Core value:** Agents delegate high-stakes cognition to the kernel; the kernel delegates irreversible actions to humans (F13/Sovereignty).

---

## Canonical Tool Contract

**Rule #1: Anchor First**
All constitutional sessions MUST start with `init_anchor`. The kernel will reject calls from unanchored sessions.

| Stage | Tool | Purpose |
|-------|------|---------|
| **000_INIT** | `init_anchor` | Bootstrap session, bind actor_id, risk tier, floors state |
| **333→888** | `arifOS_kernel` | **Canonical kernel.** Full pipeline: reason → memory/heart → critique → forge → judge |
| **888_JUDGE** | `apex_judge` | Cross-check decisions, issue verdicts |
| **999_VAULT** | `vault_seal`, `verify_vault_ledger` | Persist to VAULT999, audit trail |

**⚠️ Breaking Change Notice:**  
Historical docs referenced `arifOS.kernel` (dot notation). **Current canonical name is `arifOS_kernel` (underscore).** Update all client configs. Old name returns "Unknown tool" error.

---

## 42-Tool Runtime (Don't Hard-Code Count)

The server currently exposes **42 tools** grouped by function. Tool count is an implementation detail — it expands as the kernel evolves. Agents must not assert exact counts; assert **capability presence** instead.

| Group | Tools |
|-------|-------|
| **Constitutional** | `arifOS_kernel`, `metabolic_loop_router` (legacy alias), `audit_rules`, `apex_judge` |
| **Anchor/Auth** | `init_anchor`, `init_anchor_state`, `revoke_anchor_state`, `get_caller_status` |
| **Evidence** | `search_reality`, `ingest_evidence`, `reality_compass`, `reality_atlas` |
| **Intelligence** | `agi_reason`, `agi_reflect`, `asi_critique`, `asi_simulate` |
| **AgentZero** | `agentzero_engineer`, `agentzero_memory_query`, `agentzero_validate`, `agentzero_armor_scan`, `agentzero_hold_check` |
| **VAULT** | `vault_seal`, `verify_vault_ledger` |
| **System** | `check_vital`, `system_health`, `fs_inspect`, `process_list`, `net_status` |
| **Resources** | `arifos_list_resources`, `arifos_read_resource`, `list_resources`, `read_resource` |
| **Utils** | `forge`, `cost_estimator`, `log_tail`, `chroma_query`, `trace_replay` |

**Sanity check:** Query `tools/list` via MCP. Expect diverse schema versions. Don't cache tool list across sessions.

---

## How to Call (MCP JSON-RPC Examples)

### Transport
- **Protocol:** MCP streamable-http
- **Endpoint:** `POST http://arifosmcp_server:8080/mcp`
- **Health:** `GET http://arifosmcp_server:8080/health`

### Golden Test A: Bootstrap Session
```bash
curl -s -X POST http://arifosmcp_server:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "init_anchor",
      "arguments": {
        "actor_id": "arif",
        "risk_tier": "low",
        "intent": "diagnostic_bootstrap",
        "session_id": "test-001"
      }
    }
  }'
```
**Expect:** Anchored session object with `authority.claim_status: "anchored"` and floors state initialized.

### Golden Test B: Kernel Dry-Run
```bash
curl -s -X POST http://arifosmcp_server:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "arifOS_kernel",
      "arguments": {
        "query": "Explain arifOS constitutional pipeline in 3 bullets",
        "actor_id": "arif",
        "risk_tier": "low",
        "use_memory": false,
        "use_heart": false,
        "use_critique": true,
        "allow_execution": false,
        "dry_run": true
      }
    }
  }'
```
**Expect:** Simulated 000→999 pipeline, no external tool execution, structured verdict in response.

---

## Safety, Floors, and Permissions (F1–F13)

The kernel enforces **13 constitutional floors** via sBERT ML layer. Fail-closed bias: uncertainty triggers HOLD, not proceed.

| Floor | Name | Enforcement |
|-------|------|-------------|
| F1 | **Amanah (Reversibility)** | `requires_human: true` for irreversible actions |
| F2 | **Truth (τ ≥ 0.99)** | `ingest_evidence` required before factual claims |
| F3 | **Tri-Witness** | `witness: {human, ai, earth}` block in output |
| F4 | **Clarity (ΔS ≤ 0)** | High entropy blocks Forge stage |
| F5 | **Peace²** | Lyapunov stability check; low Peace blocks Execute |
| F6 | **Empathy (κᵣ)** | Maruah score; low score raises Hold |
| F7 | **Humility (Ω₀)** | Confidence bounds; high uncertainty requires Hold |
| F8 | **Genius (G★)** | Coherence score; <0.80 blocks Forge |
| F9 | **Anti-Hantu** | No consciousness claims in output |
| F10 | **Ontology** | No mysticism; grounded evidence only |
| F11 | **Command Auth** | Destructive ops require explicit approval scope |
| F12 | **Injection Defense** | Untrusted input sanitized before processing |
| F13 | **Sovereignty** | Human veto absolute; `verdict: "HOLD_888"` available |

**For agent authors:** Start with `risk_tier: "low"`, `allow_execution: false`, `dry_run: true`. Escalate privilege deliberately, never by default.

---

## Identity & Auth (F11)

arifOS uses an **explicit identity model** — no OAuth, no implicit trust. The server is the source of truth for actor identity and capabilities.

### Actor Registry

| Actor ID | Level | Scopes | Use Case |
|----------|-------|--------|----------|
| `ariffazil` | sovereign | `arifOS_kernel:execute`, `vault:seal`, `audit_rules:read`, `agentzero:engineer` | Human sovereign (Muhammad Arif) |
| `arif`, `arif-fazil` | sovereign | (same as above) | Aliases for sovereign |
| `openclaw` | agent | `arifOS_kernel:execute_limited`, `audit_rules:read` | OpenClaw agent (limited scope) |
| `agentzero` | agent | `arifOS_kernel:execute_limited`, `audit_rules:read` | Meta/orchestration agent |
| `operator`, `cli` | operator | `arifOS_kernel:execute`, `audit_rules:read` | Trusted operators |
| `user`, `test_user` | user | `arifOS_kernel:execute_limited` | Standard users |
| *(any other)* | declared | `audit_rules:read` | Diagnostics only |
| `anonymous` | anonymous | *(none)* | Blocked from kernel execution |

### Auth Context

When `init_anchor` succeeds, it returns an `auth_context` — a **signed, time-bound token** containing:

```json
{
  "session_id": "uuid-v7",
  "actor_id": "ariffazil",
  "authority_level": "sovereign",
  "token_fingerprint": "sha256:...",
  "nonce": "...",
  "iat": 1773897701,
  "exp": 1773898601,
  "approval_scope": ["arifOS_kernel:execute", "vault:seal"],
  "parent_signature": "...",
  "prev_vault_hash": "0x...",
  "signature": "hmac-sha256-signed"
}
```

**Rules:**

1. **Identity Precedence** — Core to F1 (Amanah) and F11 (Command Auth), the system enforces a strict identity hierarchy: `actor_id` (canonical) > `declared_name` (display) > `anonymous` (fallback). `actor_id` is the indisputable cryptographically bound source of truth.
2. **Forward auth_context** — All `arifOS_kernel` calls must include the auth_context from init_anchor
3. **Expiry** — Tokens valid for 15 minutes (TTL=900s). Re-anchor to refresh.
4. **Session binding** — Tokens are bound to session_id; cross-session use fails F11
5. **Signature verification** — Tampered tokens are rejected with `TOKEN_EXPIRED`

### Anonymous Callers

Anonymous callers (no actor_id or unknown actor) receive:
- `caller_state: "anonymous"`
- Empty approval_scope
- **HOLD on kernel execution** with `machine_issue: "INSUFFICIENT_SCOPE"`

To execute kernel operations, callers must:
1. Call `init_anchor` with a recognized `actor_id`
2. Receive signed `auth_context`
3. Forward auth_context in kernel calls

---

## For Agent Authors: Do / Don't

### ✅ Do
- **Always call `init_anchor` first** — kernel rejects unanchored sessions
- **Use canonical name `arifOS_kernel`** — not `arifOS.kernel`, not `metabolic_loop_router`
- **Pass truthful `actor_id`** — impersonation violates F2/F13
- **Default to `dry_run: true`** — verify before executing
- **Delegate high-risk decisions** — let kernel issue verdict, don't bypass
- **Check `result.requires_human`** — if true, pause for human confirmation

### ❌ Don't
- **Don't hard-code tool count** — 42 today, expands tomorrow
- **Don't cache tool list across sessions** — schema evolves
- **Don't bypass anchor** — calling kernel directly returns auth error
- **Don't mutate VAULT without approval** — `vault_seal` requires explicit scope
- **Don't assume model availability** — providers listed in `/health` capability map

---

## Capability Map (from /health)

Query `GET /health` for runtime capabilities:

```json
{
  "status": "healthy",
  "version": "2026.03.14-VALIDATED",
  "tools_loaded": 42,
  "ml_floors": {
    "ml_floors_enabled": true,
    "ml_model_available": true,
    "ml_method": "sbert"
  },
  "capability_map": {
    "vault_persistence": "enabled",
    "vector_memory": "enabled",
    "external_grounding": "limited",
    "model_provider_access": "enabled",
    "local_model_runtime": "enabled"
  }
}
```

**Redaction policy:** No raw credentials in capability map. Check capability state, not secrets.

---

## Version History

| Date | Change |
|------|--------|
| 2026.03.19 | AGENTS.md v2 — reality-sealed for 42-tool runtime, `arifOS_kernel` canonical name, anchor-first requirement |
| 2026.03.14 | Runtime validated — sBERT floors active, capability map redaction |
| (legacy) | Old "13 tools" spec — obsolete, preserved for archaeology only |

---

*Ditempa Bukan Diberi* — The contract is forged from running code, not given from old documents.
