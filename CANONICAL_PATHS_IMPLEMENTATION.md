# Canonical Tool Paths Implementation (v60.0-FORGE)

## Problem (Auditor Feedback)

Path inconsistency observed:
- Some tools under `/link_.../`
- Some tools under `/AAA MCP by arifOS/`
- "connector not installed" errors
- Agents interpret tool failures as "governance failed" rather than "plumbing failed"

## Solution

### 1. Canonical Tool Registry (`aaa_mcp/protocol/tool_registry.py`)

Created centralized registry with stable identifiers:

```python
CANONICAL_TOOLS = {
    "init_gate": ToolSpec(
        name="init_gate",
        canonical_path="aaa.init_gate",  # ← Stable identifier
        stage="000",
        next_tool="aaa.agi_sense",       # ← Deterministic routing
        ...
    ),
    ...
}
```

### 2. Updated Response Builders

All `next_tool` paths now use `get_next_tool()` from registry:

| Function | Before | After |
|----------|--------|-------|
| build_init_response | `"/arifos.aaa/v1/agi_sense"` | `get_next_tool("init_gate")` → `"aaa.agi_sense"` |
| build_sense_response | `"/arifos.aaa/v1/agi_think"` | `get_next_tool("agi_sense")` → `"aaa.agi_think"` |
| ... | ... | ... |

### 3. Standardized Error Envelopes

#### Tool Unavailable Error
```python
build_tool_unavailable_error(
    requested_tool="aaa.some_tool",
    session_id="...",
    reason="Connector not installed"
)
# Returns structured error, not runtime exception
```

#### Hard Floor Block
```python
build_hard_floor_block(
    floor="F6",
    score=0.50,
    threshold=0.95,
    reason="Weakest stakeholder at risk",
    session_id="..."
)
# Returns standardized block envelope with remediation
```

## Canonical Path Format

```
aaa.init_gate
aaa.agi_sense
aaa.agi_think
aaa.agi_reason
aaa.asi_empathize
aaa.asi_align
aaa.apex_verdict
aaa.vault_seal
aaa.trinity_forge
```

- **Prefix**: `aaa.` (arifOS AAA MCP)
- **Separator**: `.` (dot notation, language-agnostic)
- **No version**: Paths are stable across versions
- **No slashes**: Avoids URL/URI confusion

## Pipeline Sequence

```python
get_pipeline_sequence()
# Returns: ["aaa.init_gate", "aaa.agi_sense", "aaa.agi_think", ...]
```

## Benefits

1. **Deterministic Routing**: `next_action` always points to valid callable path
2. **Clear Errors**: Structured error instead of "connector not installed"
3. **Agent Trust**: Agents know it's "plumbing" not "governance" failure
4. **Namespace Stability**: `aaa.*` won't collide with other MCP servers

## Integration

```python
from aaa_mcp.protocol.tool_registry import (
    get_tool_spec,
    get_next_tool,
    validate_tool_path,
    build_tool_unavailable_error,
    build_hard_floor_block
)

# Validate a path
if validate_tool_path("aaa.agi_sense"):
    spec = get_tool_spec("agi_sense")
    next_path = get_next_tool("agi_sense")  # "aaa.agi_think"
```

## Files Changed

- `aaa_mcp/protocol/tool_registry.py` (NEW)
- `aaa_mcp/protocol/response.py` (UPDATED to use canonical paths)

## Never Change (Invariants Preserved)

✅ Progressive disclosure (only check what's observable)  
✅ Fail-closed on uncertainty  
✅ Hard floors stay hard (F6 κᵣ ≥ 0.95)  
✅ 888_HOLD for high-stakes  
✅ Vault sealing (auditability)  
✅ Stage separation of concerns

---

**Authority:** External Auditor Feedback + Kimi Code CLI  
**Version:** v60.0-FORGE  
**Creed:** DITEMPA BUKAN DIBERI
