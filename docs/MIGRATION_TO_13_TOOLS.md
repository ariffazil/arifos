# 🎯 Migration Guide: Consolidated 13 Canonical Tools

## Overview

arifOS has consolidated from a fragmented 17+ tool surface to **exactly 13 canonical
constitutional tools** aligned with the MCP 2025-11-25 specification.

---

## What Changed

### ✅ New Tool: `ingest_evidence`

**Replaces:** `fetch_content` + `inspect_file`

**Why:** Both tools performed the same cognitive act — retrieving and examining an
object from the environment. Merging them into one entry point:
- Reduces conceptual overhead for agents and humans
- Creates a clean "discovery vs. retrieval" split:
  - `search_reality` → **EXPLORE** (find candidates)
  - `ingest_evidence` → **EXAMINE** (open/parse a chosen object)
- Produces cleaner audit trails (one tool name, two input paths)

### ✅ Promoted: `metabolic_loop`

`metabolic_loop` was previously classified as an L5 composite orchestration tool.
It is now a first-class L4 canonical tool, completing the 13-tool surface.

---

## Migration Examples

### From `fetch_content` (URL retrieval)

**Before:**
```python
result = await fetch_content(id="https://example.com", max_chars=500)
```

**After:**
```python
result = await ingest_evidence(
    source_type="url",
    target="https://example.com",
    mode="raw",
    max_chars=500,
)
```

### From `inspect_file` (filesystem inspection)

**Before:**
```python
result = await inspect_file(path="/path/to/dir", depth=2, max_files=50)
```

**After:**
```python
result = await ingest_evidence(
    source_type="file",
    target="/path/to/dir",
    depth=2,
    max_files=50,
)
```

### Processing Modes

```python
# Raw content (default)
result = await ingest_evidence(source_type="url", target="https://example.com", mode="raw")

# Quick summary (first 500 chars)
result = await ingest_evidence(source_type="url", target="https://example.com", mode="summary")

# Chunked (list of 1000-char segments)
result = await ingest_evidence(source_type="url", target="https://example.com", mode="chunks")
```

---

## Final 13 Public Tools

### Core Constitutional Spine (8)

| # | Tool | Stage | Floor |
|---|------|-------|-------|
| 1 | `anchor_session` | 000_INIT | F11, F12 |
| 2 | `reason_mind` | 333_REASON | F2, F4, F7 |
| 3 | `recall_memory` | 444_SYNC | F4, F7 |
| 4 | `simulate_heart` | 555_EMPATHY | F5, F6 |
| 5 | `critique_thought` | 666_ALIGN | F4, F7, F8 |
| 6 | `eureka_forge` | 777_FORGE | F5, F6, F9 |
| 7 | `apex_judge` | 888_JUDGE | F1–F13 |
| 8 | `seal_vault` | 999_SEAL | F1, F3 |

### Evidence / Observability (4)

| # | Tool | Purpose |
|---|------|---------|
| 9 | `search_reality` | Discovery — find evidence candidates |
| 10 | `ingest_evidence` | Retrieval — fetch URL or inspect file (**NEW**) |
| 11 | `audit_rules` | Constitutional audit + rule validation |
| 12 | `check_vital` | System health diagnostics |

### Orchestration (1)

| # | Tool | Purpose |
|---|------|---------|
| 13 | `metabolic_loop` | Full 000→999 macro cycle |

---

## Archived Tools

| Tool | Archived In | Replacement |
|------|-------------|-------------|
| `fetch_content` | `ARCHIVED_TOOLS/README.md` | `ingest_evidence(source_type="url", ...)` |
| `inspect_file` | `ARCHIVED_TOOLS/README.md` | `ingest_evidence(source_type="file", ...)` |

The internal implementations remain in `aaa_mcp/server.py` as **non-decorated** helper
functions (`_fetch` / `_inspect_file`) and will not appear in `/tools/list`.

---

## Breaking Changes

| Change | Impact | Fix |
|--------|--------|-----|
| `fetch_content` removed from public surface | Calls will fail | Migrate to `ingest_evidence(source_type="url", ...)` |
| `inspect_file` removed from public surface | Calls will fail | Migrate to `ingest_evidence(source_type="file", ...)` |
| `/tools/list` now returns exactly 13 tools | Health checks expecting 15+ will fail | Update count assertions to 13 |
| `_ALLOWED_TOOLS` frozenset updated | Calls to old names denied at F12 layer | Update tool name to `ingest_evidence` |

---

## Compliance Verification

```bash
# Run 13-tool compliance tests
pytest tests/test_13_tools_compliance.py -v

# Verify canonical count
python -c "from aaa_mcp.protocol.aaa_contract import AAA_CANONICAL_TOOLS; print(len(AAA_CANONICAL_TOOLS))"
# Expected: 13

# Verify no ghost imports
grep -n "fetch_content\|inspect_file" aaa_mcp/server.py | grep "@mcp.tool"
# Expected: (no output)
```

---

## Rollback Instructions

```bash
git revert HEAD
git push
```

---

*Migration effective: 2026-03-06*  
*Target MCP Spec: 2025-11-25*  
*arifOS Version: v60.0-FORGE*
