# MEMORY.md — OPENCLAW Selective Persistence

**Version:** 2026.05.01-KANON
**Last updated:** 2026-05-01 03:17 UTC

---

## Sealed Facts

### arifOS MCP v0.2 REAL BACKEND — Deployed 2026-04-26

6 governance backend files created and wired into `server.py`:
- `vault_chain.py` — real hash-chain append
- `session_state.py` — session lifecycle state machine
- `interceptor.py` — governance interceptor
- `forge_app.py` — double-gated execution
- `judge_app.py` — verdict engine
- `vault_audit.py` — VAULT999 reader

### arif-fazil.com HUMAN ROOT — Implementation Log

**Cloudflare cache issue:** API token lacks "Cache Purge" permission — manual purge required via Cloudflare Dashboard.

**.well-known files:** did.json, arif-human.json, arifos.json, 000_GENESIS.md return HTTP 200 from origin but Cloudflare caches old 404s.

### wealth-organ Fix — 2026-04-29

Fixed: `TypeError: FastMCP.run() got an unexpected keyword argument 'transport'` — bind mount overwriting image's `.venv`.

### WEALTH MCP Exposed — 2026-05-01

**Critical bug found:** wealth-organ ran with `transport="sse"` which only exposes `GET /sse` and `POST /messages/` — no `/mcp` endpoint. Fixed by changing to `transport="http"` in monolith.py line 4115.

Added `wealth.arif-fazil.com` → `wealth-organ:8082` route to Caddyfile.

WEALTH MCP now live at `https://wealth.arif-fazil.com/mcp` (HTTP transport, session-based).

### OPENCLAW Governance Upgrade — 2026-05-01

**Task OC-001 complete.** All gap files created:

| File | Status | Purpose |
|------|--------|---------|
| AGENTS.md | ✅ Updated | ReAct loop → 000–999 governed loop |
| AUTONOMY.md | ✅ Created | L0–L5 permission ladder |
| CHECKPOINT.md | ✅ Created | Session continuity + recovery |
| HEARTBEAT.md | ✅ Rewritten | Live runtime protocol |
| LOOP.md | ✅ Created | 000–999 operational implementation |
| DECISIONS.md | ✅ Created | Sealed decision log |
| TASKS.md | ✅ Created | Active work ledger |
| TOOLS.md | ✅ Populated | Local environment notes |
| RECOVERY.md | ✅ Created | Failure recovery runbook |
| FLOORS.md | ✅ Created | F1–F13 standalone reference |

**Archived (stale, conflicting governance):** CLAUDE.md, GEMINI.md, ARIF.md — prepended archive notice.

---

## Archived Logs

*(Older entries in memory/*.md)*
