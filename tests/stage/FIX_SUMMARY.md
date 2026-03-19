# MCP Bridge Server — Fix Summary

## Problem
The original bridge server (`server.py`) called endpoints like `/forge`, `/think`, `/init` that don't exist in the arifOS REST API.

## Root Cause
The arifOS REST API (`aaa_mcp/rest.py`) uses a **generic tool calling pattern**:
- Endpoint: `POST /{tool_name}` or `POST /tools/{tool_name}`
- Tool names: `anchor`, `reason`, `integrate`, `respond`, `validate`, `align`, `forge`, `audit`, `seal`, `self_diagnose`

## Solution (`server_fixed.py`)
Maps MCP tools directly to REST API tool endpoints:

| MCP Tool | REST Endpoint | Description |
|----------|---------------|-------------|
| `anchor` | `POST /anchor` | 000_INIT — Session ignition |
| `reason` | `POST /reason` | 222_REASON — AGI Mind |
| `integrate` | `POST /integrate` | 333_INTEGRATE — Grounding |
| `respond` | `POST /respond` | 444_RESPOND — Drafting |
| `validate` | `POST /validate` | 555_VALIDATE — ASI Heart |
| `align` | `POST /align` | 666_ALIGN — Ethics (F9) |
| `forge` | `POST /forge` | 777_FORGE — Synthesis |
| `audit` | `POST /audit` | 888_AUDIT — APEX verdict |
| `seal` | `POST /seal` | 999_SEAL — VAULT |
| `self_diagnose` | `POST /self_diagnose` | Infrastructure health |

## Deployment

```bash
# Set environment variable
export ARIFOS_API_URL="https://aaamcp.arif-fazil.com"

# Run bridge
python tests/stage/server_fixed.py
```

## Claude.ai Configuration

Set connector URL to:
```
https://YOUR-BRIDGE-URL/sse
```

## Files

- `server.py` — Original (broken, wrong endpoints)
- `server_fixed.py` — Corrected (maps to actual REST API)
- `Dockerfile_1` — Can be used with either (update CMD)

## Note

The arifOS REST API already has `/sse` and `/messages` endpoints for MCP protocol. If those work, you might not need this bridge at all—just point Claude.ai directly to `https://aaamcp.arif-fazil.com/sse`.

This bridge is only needed if:
1. The native MCP endpoints have protocol issues
2. You need to transform/augment requests
3. You want to add middleware/logging
