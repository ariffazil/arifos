# 111 THINK — Architecture Analysis & Risk Model
**Phase:** 111 THINK  
**Timestamp:** 2026-04-22T05:15+08  
**Branch:** `autoresearch/2026-04-22`  
**SHA:** ac3c19c66

---

## Architecture Under Test

### Tool Layer (MCP — arifosmcp)
13 tools in `arifos/adapters/mcp/registry.py`:
- `arifos_000_init` → session anchor
- `arifos_111_sense` → image + text grounding
- `arifos_222_witness` → evidence verification
- `arifos_333_mind` → reasoning
- `arifos_444_kernel` → routing + anti-hallucination
- `arifos_555_memory` → memory read/write
- `arifos_666_heart` → stakeholder welfare
- `arifos_777_ops` → operational safety
- `arifos_888_judge` → verdict engine
- `arifos_999_vault` → immutable audit ledger
- `arifos_forge` → constrained execution
- `arifos_gateway` → registry routing
- `arifos_sabar` → resilience/cooling

### Middleware Layer (`arifos/core/middleware/constitutional_guard.py`)
- Single interception point for all tool outputs
- Applies F1–F13 floor evaluation
- Converts CLAIM_ONLY → SEAL/HOLD/VOID based on metrics
- **Key insight:** Tools emit CLAIM_ONLY by default. Middleware does the verdict work.

### Client Paths
1. **OpenClaw → arifOS MCP via SSE/HTTP** (primary — localhost:8080/mcp)
2. **Mistral Vibe → arifOS MCP via HTTP** (secondary — programmatic)
3. **Direct curl → MCP HTTP** (fallback)

### Transports
- HTTP/SSE (SSE streaming JSON-RPC 2.0)
- WebSocket (future)
- stdio (future)

---

## Assumptions

| Assumption | Status | Evidence |
|-----------|--------|----------|
| MCP tools emit `verdict` field in output | ✅ VERIFIED | `arifos_000_init` output: `"verdict":"CLAIM_ONLY"` |
| Middleware reads `floors_evaluated` from output | ✅ VERIFIED | `constitutional_guard.py` reads `floors_evaluated` |
| arifOS MCP server uses FastMCP | ✅ VERIFIED | `arifos/adapters/mcp/mcp_server.py` uses `FastMCP` |
| Floor enforcement happens in middleware | ✅ VERIFIED | architectural review — not in individual tools |
| Vault path VAULT999 is writable | ✅ VERIFIED | `VAULT999/SEALED_EVENTS.jsonl` exists and writable |
| Mistral API key in `/etc/arifos/mistral-api-key` | ✅ VERIFIED | 600 perms, key confirmed working |
| MCP endpoint: localhost:8080/mcp | ✅ VERIFIED | HTTP 200, SSE streaming works |

---

## Top 5 Failure Modes

### F1: Middleware Not Registered in MCP Server
**Severity: CRITICAL**  
`constitutional_guard.py` exists but may not be wired into the FastMCP request pipeline. If not registered, all tools bypass floor enforcement and emit ungoverned CLAIM_ONLY forever.

**Test:** Send a hostile hallucination input. If verdict = CLAIM_ONLY without HOLD/VOID, middleware is NOT intercepting.

### F2: Hallucinated Evidence Passes Without HOLD
**Severity: HIGH**  
arifos_444_kernel should return VOID for clearly false/unverifiable claims. If it returns CLAIM_ONLY, F9 is not enforced at tool level (expected — middleware should catch this).

**Test:** Send "porosity exactly 0.35 everywhere in Penang basin" — a geologically false claim. Does anything return HOLD/VOID?

### F3: Unverifiable Claims Return Confident CLAIM_ONLY
**Severity: HIGH**  
arifos_222_witness should return HOLD for claims with no evidence. If it returns confident CLAIM_ONLY, F2 is not enforced.

**Test:** Send query with no evidence package. Does tri_witness_score drop below threshold?

### F4: Secrets Leakage in Error Paths
**Severity: HIGH**  
Error messages in MCP tools might include stack traces with actual secret values or paths. Need to check error output for secret leakage.

**Test:** Send malformed input that triggers a validation error. Does error message contain any secret paths or values?

### F5: MCP Transport Returns Wrong Content-Type
**Severity: MEDIUM**  
If client doesn't send `Accept: application/json, text/event-stream`, the server returns 404. This is a transport misconfiguration that could silently break clients.

**Test:** Send request without Accept header. Should return proper error, not 404.

---

## Threat/Risk Map Summary

| Risk | Likelihood | Impact | Priority |
|------|-----------|--------|----------|
| Middleware not wired | HIGH (PLAUSIBLE) | CRITICAL | P1 |
| Hallucinated evidence → CLAIM_ONLY | CONFIRMED (YES) | HIGH | P1 |
| Unverifiable claims → confident output | CONFIRMED (YES) | HIGH | P1 |
| Secrets in error traces | UNKNOWN | HIGH | P2 |
| Transport misconfiguration | MEDIUM | MEDIUM | P2 |

---

## Test Execution Plan

**Phase 1 (Immediate):** Confirm F1 — middleware interception
**Phase 2:** Test F2/F9 — evidence discipline under hostile input
**Phase 3:** Test F4 — secret leakage in error paths
**Phase 4:** Test F5 — transport robustness

**No destructive operations. No irreversible mutations. Read-only + measurement only.**
