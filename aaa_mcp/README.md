# arifOS MCP Server Integration

ASI (Arif's Sidekick Intelligence) Gateway for external MCP servers with constitutional governance.

## Overview

This package wraps 9 external MCP servers with arifOS 13 Floors constitutional enforcement, mapping each to the Trinity architecture (AGI·ASI·APEX).

## Quick Start

### 1. Install Dependencies

```bash
pip install fastmcp pydantic
```

### 2. Start the ASI Gateway

```bash
python -m mcp_server
# or
python mcp_server/asi_gateway.py
```

The gateway runs on port **6277** by default.

### 3. Configure Claude Desktop

Copy `claude_desktop_config.json` to your Claude Desktop config:

```bash
# macOS
cp mcp_server/claude_desktop_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Linux
cp mcp_server/claude_desktop_config.json ~/.config/Claude/claude_desktop_config.json
```

## MCP Server Registry

| Server | Trinity | Floors | Atomic Action | Ω₀ Threshold |
|--------|---------|--------|---------------|--------------|
| **filesystem** | APEX(Ψ) | F1, F3 | VAULT999 | 0.04 |
| **memory** | ASI(Ω) | F2, F7 | Memory Weaver (#9) | 0.05 |
| **fetch** | AGI(Δ) | F2, F4 | Geo-Radar (#4) | 0.06 |
| **everything** | APEX(Ψ) | F3, F8 | Peace² Auditor (#2) | 0.03 |
| **git** | AGI(Δ) | F1, F2, F3 | PyPI Sentinel (#3) | 0.04 |
| **time** | ASI(Ω) | F6, F4 | Meeting Metabolizer (#6) | 0.02 |
| **sequential_thinking** | ASI(Ω) | F5, F7, F9 | ASI Align/Reason | 0.05 |
| **brave_search** | AGI(Δ) | F2, F8 | Reality Search | 0.06 |
| **memory_enhanced** | ASI(Ω) | F6, F9 | ASI Empathize | 0.05 |

## Trinity Architecture

### AGI(Δ) — Mind/Logic
- **agi_sense**: Perception and parsing
- **agi_think**: Structured cognition  
- **agi_reason**: Formal logic

### ASI(Ω) — Heart/Care
- **asi_empathize**: Emotional intelligence
- **asi_align**: Constitutional harmony

### APEX(Ψ) — Crown/Law
- **apex_verdict**: Governance judgment
- **vault_seal**: Immutable ledger

## Constitutional Enforcement

All MCP calls are wrapped with:

1. **Ω₀ Uncertainty Tracking** — F7 Humility
2. **Floor Validation** — Appropriate floors per server
3. **Audit Logging** — Complete call history
4. **Reversibility Check** — F1 Amanah compliance

## API Usage

### Direct MCP Call

```python
from mcp_server import mcp_call

result = await mcp_call(
    server="filesystem",
    operation="read",
    params={"path": "/tmp/test.txt"},
    omega_estimate=0.04
)
```

### Trinity Tools

```python
from mcp_server import agi_think, asi_empathize, apex_verdict

# AGI reasoning
think_result = await agi_think("Analyze this data", "session-123")

# ASI care
empathy_result = await asi_empathize("User seems frustrated", "session-123")

# APEX judgment
verdict = await apex_verdict("Is this action safe?", "session-123")
```

### Audit Trail

```python
from mcp_server import get_audit_log

logs = await get_audit_log(limit=50)
```

## Configuration

Environment variables for each MCP server:

```bash
# Constitutional metadata
ARIFOS_FLOORS="F1,F2,F3"
ARIFOS_TRINITY="ASI"
ARIFOS_ATOMIC_ACTION="MemoryWeaver"

# External APIs
BRAVE_API_KEY="your-api-key"
```

## Verdict System

- **SEAL** ✅ — Operation approved and executed
- **VOID** ❌ — Operation rejected (constitutional violation)
- **SABAR** ⏸️ — Operation pending (high uncertainty, needs review)

## Files

| File | Purpose |
|------|---------|
| `asi_gateway.py` | FastMCP server with Trinity tools |
| `mcp_integration.py` | Constitutional enforcement layer |
| `mcp_config.py` | Server registry and configuration |
| `constitutional_decorator.py` | Floor enforcement decorators |
| `claude_desktop_config.json` | Claude Desktop integration |

## Motto

**DITEMPA BUKAN DIBERI** 💎🔥🧠

*(Forged, Not Given)*