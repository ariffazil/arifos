# arifOS MCP — Engineering Remediation Checklist v1.0

**Date:** 2026-03-20  
**Status:** P0 Items In Progress  
**Severity:** Contract Drift 6.5/10 → Target 0/10

---

## P0 — Critical (Blocks Production)

### 1. Protected Sovereign ID Hard-Fail ✅ IMPLEMENTED
- [x] Reserved principal registry: `governance_identities.py`
- [x] Protected IDs: arif, ariffazil, sovereign, admin, root, system
- [x] Hard-fail logic in `init_anchor` without proof/approval
- [x] Explicit error: AUTH_PROTECTED_ID_REQUIRED
- [ ] VPS validation pending

**Test:** `{actor_id: "arif", intent: "test"}` → AUTH_FAILURE  
**Location:** `arifosmcp/runtime/tools.py:180-208`

---

### 2. Unified ABI Adapter ❌ NOT DONE
**Issue:** FastMCP exposes flat args, not `{mode, payload}` envelope
**Root Cause:** Schema auto-generated from type hints, not ToolSpec

**Required:**
- [ ] Custom schema injection for FastMCP tools
- [ ] OR: Wrapper layer that transforms flat → envelope internally
- [ ] Add `abi_version` to all responses

**Current Workaround:** Legacy flat args work, envelope not enforced

---

### 3. Structured Intent Normalization ✅ IMPLEMENTED
- [x] Accept `str | dict | None` in `init_anchor_impl`
- [x] Auto-normalize string to `{query, task_type}`
- [x] Support domain, task_type, desired_output fields
- [ ] Schema mismatch hides this from clients (see Item 2)

**Location:** `arifosmcp/runtime/tools_internal.py:214-239`

---

### 4. Human Approval Enforcement ⚠️ PARTIAL
- [x] Field added to payload schema
- [x] Logic to bypass protected ID check
- [ ] NOT in FastMCP-generated schema (hidden from clients)
- [ ] Wiring to session state incomplete

**Required:**
- [ ] Force FastMCP to include human_approval in schema
- [ ] Persist to session: `approval_state`, `approval_scope`
- [ ] Block privileged tools when pending

---

## P1 — Important (Architecture Hardening)

### 5. Claimed vs Resolved Identity ⚠️ PARTIAL
- [x] Fields added to RuntimeEnvelope payload
- [ ] Not propagated through all response paths
- [ ] audit trail incomplete

### 6. Formal Session State Machine ❌ NOT DONE
Current: Implicit states (anchored, verified, etc.)
Required:
- UNVERIFIED → ANCHORED → VERIFIED → APPROVED
- Explicit transitions with reason

### 7. Central Capability Gating ❌ NOT DONE
Current: Distributed checks in each tool
Required:
- Session stores capabilities list
- Tools declare required capabilities
- Central resolver enforces

### 8. Standard Error Taxonomy ⚠️ PARTIAL
Current: Mixed error styles
Required:
- ABI_*, AUTH_*, SESSION_*, APPROVAL_* prefixes
- Consistent structure: code, message, recoverable, remediation

---

## P2 — Strengthening (Operator Experience)

### 9. Tool Naming Alignment ❌ NOT DONE
Issue: Dashboard shows `agi_mind`, but callable is `agi_reason`
Required:
- Canonical mapping metadata
- Conceptual → implementation registry

### 10. Router-First Enforcement ❌ NOT DONE
Issue: Low-level tools exposed directly
Required:
- Mark tools: canonical | low_level | internal | legacy
- Recommend canonical path in responses

### 11. Telemetry Provenance Labels ❌ NOT DONE
Issue: Mixed real/simulated metrics
Required:
- `source_type`: host_runtime | derived_symbolic | simulated
- `enforcement`: hard | informational

### 12. Resource-Driven Contract Introspection ⚠️ PARTIAL
Resources exist but not auto-linked in responses.

### 13. Revocation Regression Tests ❌ NOT DONE
Kill switch needs validation suite.

### 14. Full Conformance Suite ❌ NOT DONE
CI/CD enforcement of all items above.

---

## Current Blockers 🚧

1. **FastMCP Schema Generation** — Auto-generated schemas don't match ToolSpec
2. **VPS Deployment Sync** — Agent rebase may cause conflicts
3. **End-to-End Testing** — Cannot validate without deployed instance

---

## Definition of Done ✅

arifOS MCP v1.0 is hardened when:

- [ ] Protected ID without token → hard AUTH_FAILURE
- [ ] Structured intent → accepted and routed correctly  
- [ ] Human approval → stored, enforced, blocks privileged ops
- [ ] Claimed vs resolved identity → clear in every response
- [ ] All tools accept unified `{mode, payload}` envelope
- [ ] Error taxonomy → machine-readable, consistent
- [ ] Revocation → kills session, requires re-init
- [ ] Conformance suite → blocks deployment on regression

---

**Next Sprint:** Items 2, 4 (FastMCP schema alignment)  
**Owner:** arifOS Engineering  
**Motto:** DITEMPA BUKAN DIBERI — Forged, Not Given
