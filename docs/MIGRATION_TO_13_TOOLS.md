# 🎯 Migration Guide: 17+ Tools → 13 Canonical Tools

## Overview

arifOS has consolidated from 17+ scattered tools to **exactly 13 canonical constitutional tools** for MCP deployment.

This guide explains the changes and how to migrate your code.

---

## What Changed

### ✅ New Tool: `ingest_evidence`

**Replaces:** `fetch_content` + `inspect_file`

**Why:** These two tools were semantically identical (retrieve and examine objects). Merging them creates a clean mental model:
- `search_reality` = **EXPLORE** (find candidates)
- `ingest_evidence` = **EXAMINE** (open/parse chosen object)

**Usage:**

```python
# Old way (fetch_content)
result = await fetch_content(url="https://example.com")

# New way (ingest_evidence)
result = await ingest_evidence(
    source_type="url",
    target="https://example.com",
    mode="raw"
)
```

```python
# Old way (inspect_file)
result = await inspect_file(path="/path/to/file.txt")

# New way (ingest_evidence)
result = await ingest_evidence(
    source_type="file",
    target="/path/to/file.txt",
    mode="raw"
)
```

### 🗄️ Archived Tools

These tools are **no longer available** in the public MCP surface:

| Tool | Status | Replacement |
|------|--------|-------------|
| `fetch_content` | Archived | `ingest_evidence(source_type="url", ...)` |
| `inspect_file` | Archived | `ingest_evidence(source_type="file", ...)` |
| `list_prompts` | Internal | Use MCP `prompts/list` endpoint |
| `get_prompt` | Internal | Use MCP `prompts/get` endpoint |
| `query_openclaw` | Internal | Dev-only (not in public API) |

---

## Final 13 Public Tools

### Core Constitutional Spine (8)

1. **anchor_session** — 000_INIT: Session initialization
2. **reason_mind** — 111-444_AGI: Logical reasoning
3. **recall_memory** — 555_RECALL: Memory retrieval
4. **simulate_heart** — 555-666_ASI: Stakeholder empathy
5. **critique_thought** — Self-critique layer
6. **eureka_forge** — Sovereign actuator
7. **apex_judge** — 777_JUDGE: Constitutional judgment
8. **seal_vault** — 999_SEAL: Immutable ledger

### Evidence / Observability (2)

9. **search_reality** — Discovery (exploration)
10. **ingest_evidence** — Retrieval/inspection (examination) ✨ **NEW**

### Governance / Health (2)

11. **audit_rules** — Constitutional audit
12. **check_vital** — System health check

### Orchestration (1)

13. **metabolic_loop** — Full-cycle macro convenience

---

## MCP 2025-11-25 Compliance

arifOS now implements the full MCP specification:

### Endpoints

- ✅ `tools/list` - List all 13 public tools
- ✅ `tools/call` - Execute a tool
- ✅ `prompts/list` - List available prompt templates
- ✅ `prompts/get` - Get a specific prompt
- ✅ `resources/list` - List available resources
- ✅ `resources/read` - Read a resource
- ✅ `logging/setLevel` - Set logging level
- ✅ `completion/complete` - Autocomplete support

### Features

- ✅ Pagination support for large lists
- ✅ JSON-RPC 2.0 protocol
- ✅ Proper error handling
- ✅ Input validation (F12: Injection Defense)
- ✅ Health endpoint compliance

---

## Migration Checklist

- [ ] Replace all `fetch_content()` calls with `ingest_evidence(source_type="url", ...)`
- [ ] Replace all `inspect_file()` calls with `ingest_evidence(source_type="file", ...)`
- [ ] Remove direct calls to `list_prompts` / `get_prompt` (use MCP endpoints)
- [ ] Update any hardcoded tool lists to use `AAA_CANONICAL_TOOLS`
- [ ] Run tests: `pytest tests/test_13_tools_compliance.py`
- [ ] Verify MCP spec compliance: Check `/tools/list` endpoint
- [ ] Update documentation and examples

---

## Code Examples

### Example 1: Fetching URL Content

**Before:**
```python
from aaa_mcp.server import fetch_content

result = await fetch_content(
    url="https://api.example.com/data",
    session_id="sess_123"
)
```

**After:**
```python
from aaa_mcp.server import ingest_evidence

result = await ingest_evidence(
    source_type="url",
    target="https://api.example.com/data",
    mode="raw",
    session_id="sess_123"
)
```

### Example 2: Reading a File

**Before:**
```python
from aaa_mcp.server import inspect_file

result = await inspect_file(
    path="/etc/config.json",
    session_id="sess_123"
)
```

**After:**
```python
from aaa_mcp.server import ingest_evidence

result = await ingest_evidence(
    source_type="file",
    target="/etc/config.json",
    mode="raw",
    session_id="sess_123"
)
```

### Example 3: Processing Modes

The new `ingest_evidence` tool supports multiple processing modes:

```python
# Raw mode (no processing)
result = await ingest_evidence(
    source_type="url",
    target="https://example.com",
    mode="raw"
)

# Summary mode (extract key info)
result = await ingest_evidence(
    source_type="file",
    target="/long/document.txt",
    mode="summary"  # Returns condensed version
)

# Chunks mode (split into semantic chunks)
result = await ingest_evidence(
    source_type="url",
    target="https://example.com/article",
    mode="chunks"  # Returns content split into chunks
)
```

---

## Testing Your Migration

### 1. Verify Tool Count

```python
from aaa_mcp.protocol.aaa_contract import AAA_CANONICAL_TOOLS, CANONICAL_TOOL_COUNT

assert len(AAA_CANONICAL_TOOLS) == 13
assert CANONICAL_TOOL_COUNT == 13
print("✅ Tool count is correct")
```

### 2. Check MCP Endpoint

```bash
# Check tools/list returns 13 tools
curl -X POST http://localhost:8000/rpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' \
  | jq '.result.tools | length'

# Should output: 13
```

### 3. Test ingest_evidence

```python
from aaa_mcp.tools.ingest_evidence import ingest_evidence

# Test URL mode
result = await ingest_evidence(
    source_type="url",
    target="https://example.com",
    mode="raw"
)
assert result["verdict"] in ["SEAL", "PARTIAL"]
print("✅ URL mode works")

# Test file mode
result = await ingest_evidence(
    source_type="file",
    target="/etc/hosts",
    mode="raw"
)
assert result["verdict"] in ["SEAL", "PARTIAL", "VOID"]
print("✅ File mode works")
```

---

## Rollback Instructions

If you need to rollback:

1. **Revert the commit:**
   ```bash
   git revert <commit-hash>
   ```

2. **Restore old tools from ARCHIVED_TOOLS/:**
   ```bash
   cp ARCHIVED_TOOLS/fetch_content.py.archived aaa_mcp/tools/fetch_content.py
   cp ARCHIVED_TOOLS/inspect_file.py.archived aaa_mcp/tools/inspect_file.py
   ```

3. **Update aaa_contract.py** to include old tools

---

## FAQ

### Q: Why merge fetch_content and inspect_file?

**A:** They're semantically identical operations:
- Both retrieve and examine a specific object
- Both apply the same floors (F2, F4, F12)
- The only difference is the source type (URL vs file)

Merging them creates a cleaner mental model:
- `search_reality` = find things (exploration)
- `ingest_evidence` = examine things (retrieval)

### Q: What happens if I call fetch_content now?

**A:** The old tools are archived. Calls to `fetch_content` or `inspect_file` will fail with a clear error message pointing you to `ingest_evidence`.

### Q: Are the 13 tools final?

**A:** Yes. This is the **canonical 13-tool surface** for MCP deployment. Any changes require constitutional review.

### Q: How do I access internal tools like query_openclaw?

**A:** Internal tools are moved to `aaa_mcp/tools/internal/` and are not exposed via MCP `/tools/list`. They're available for dev/ops use but not part of the public API.

---

## Questions?

See:
- `ARCHIVED_TOOLS/README.md` for migration examples
- `tests/test_13_tools_compliance.py` for usage examples
- `aaa_mcp/tools/ingest_evidence.py` for implementation details
- MCP spec: https://modelcontextprotocol.io/specification/2025-11-25/

---

**Ready to deploy the 13-tool arifOS MCP surface. 🔥**