# Tool Reference — 13 Canonical arifOS MCP Tools

All tools enforce **13-Floor thermodynamic governance** before execution.
Every response includes `verdict`, `stage`, `session_id`, `floors`, `truth`, and `next_actions`.

---

## Governance Chain (000 → 999)

### `anchor_session` — Stage 000
Start a governed session. Verifies authority (F11) and initialises thermodynamic budget.

**Parameters:**
- `task` (string) — task description
- `auth_token` (string, optional) — bearer token for F11 authority
- `actor_id` (string, optional) — actor identity string

**Returns:** `{verdict, session_id, floors, stage: "000"}`

---

### `reason_mind` — Stage 333
Three-path constitutional reasoning (Conservative · Optimistic · Novel).

**Parameters:**
- `session_id` (string)
- `query` (string) — reasoning target
- `context` (string, optional)

**Returns:** `{verdict, hypotheses: [...], floor_scores}`

---

### `vector_memory` — Stage 555
BGE-M3 multilingual semantic memory retrieval.

**Parameters:**
- `session_id` (string)
- `query` (string)
- `top_k` (int, default 5)

**Returns:** `{verdict, results: [...], embeddings_used}`

---

### `simulate_heart` — Stage 555
Empathy and impact modelling for proposed actions.

**Parameters:**
- `session_id` (string)
- `plan` (object) — proposed action plan
- `stakeholders` (list, optional)

**Returns:** `{verdict, empathy_score, impact_analysis}`

---

### `critique_thought` — Stage 666
Adversarial alignment check against the constitution.

**Parameters:**
- `session_id` (string)
- `thought` (string) — thought/plan to critique

**Returns:** `{verdict, critique, floor_violations: [...]}`

---

### `apex_judge` — Stage 888
Final constitutional verdict. Issues HMAC governance token.

**Parameters:**
- `session_id` (string)
- `summary` (string) — summary of session work

**Returns:** `{verdict: SEAL|VOID|PARTIAL|888_HOLD, governance_token, floor_scores}`

---

### `eureka_forge` — Stage 777
Execute shell commands inside AKI safety rails.

**Parameters:**
- `session_id` (string)
- `command` (string) — shell command
- `approval_bundle` (object, optional) — required for destructive ops

**Returns:** `{verdict, stdout, stderr, exit_code}`

---

### `seal_vault` — Stage 999
Commit session to VAULT999 immutable ledger.

**Parameters:**
- `session_id` (string)
- `governance_token` (string) — from `apex_judge`
- `summary` (string)

**Returns:** `{verdict: SEAL, vault_entry_id, merkle_hash}`

---

## Evidence / Read-Only Tools

### `search_reality`
Smart hybrid search: Jina → Perplexity → Brave → Headless.

**Parameters:**
- `query` (string)
- `max_results` (int, default 5)

---

### `ingest_evidence`
Extract clean Markdown from URLs or local files.

**Parameters:**
- `url` (string) — https:// URL or file path

---

### `audit_rules`
Read current state of all 13 Floors.

**Parameters:** none

**Returns:** `{floors: {F1: {...}, ..., F13: {...}}, verdict}`

---

### `check_vital`
Hardware telemetry — CPU, RAM, thermodynamic health.

**Parameters:** none

**Returns:** `{cpu_pct, ram_pct, disk_pct, thermodynamic_load}`

---

### `metabolic_loop`
Force a request through the full 000→999 pipeline.

**Parameters:**
- `task` (string)
- `auth_token` (string, optional)

**Returns:** Full metabolic pipeline result

---

## Verdicts

| Verdict | Meaning |
|---------|---------|
| `SEAL` | Approved and cryptographically signed |
| `PARTIAL` | Soft floor violation, warning issued |
| `SABAR` | Execution paused (cooling period) |
| `VOID` | Hard floor violation, execution blocked |
| `888_HOLD` | Human cryptographic signature required |
