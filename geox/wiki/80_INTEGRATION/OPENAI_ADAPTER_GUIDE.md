# OpenAI Adapter Guide — ChatGPT Apps SDK Integration

> **DITEMPA BUKAN DIBERI** — *Forged, Not Given*  
> **Version:** 0.6.1  
> **Authority:** 888_JUDGE | ARIF  
> **Seal:** ACTIVE

---

## Overview

The **OpenAI Adapter** enables GEOX Earth Witness tools to be invoked directly from ChatGPT conversations via the ChatGPT Apps SDK (Actions API). This bridges natural language queries to constitutional geoscience computation.

```
User in ChatGPT
      ↓
Natural language query
      ↓
ChatGPT → OpenAI Adapter → MCP Bridge → GEOX Backend
      ↓
Constitutional result with F1-F13 verification
```

---

## Quick Start

### For ChatGPT Users

1. **Install GEOX App** (when published to GPT Store)
   - Search "GEOX Earth Witness" in ChatGPT
   - Click "Add to ChatGPT"

2. **Start Querying**
   ```
   "Check GEOX system health"
   "Query Malay Basin statistics"
   "Calculate water saturation using Archie model"
   ```

### For Developers

```typescript
import { useOpenAI } from './adapters';

function MyComponent() {
  const { init, isReady, status } = useOpenAI();

  useEffect(() => {
    init(); // Auto-registers all GEOX tools
  }, []);

  return <div>Adapter: {status}</div>;
}
```

---

## Architecture

### File Structure

```
geox-gui/src/adapters/
├── index.ts                    # Central exports
├── openai_types.ts             # Type definitions + tool registry
├── openai_adapter.ts           # Core adapter implementation
├── useOpenAI.ts                # React hooks
└── openai_manifest.json        # ChatGPT Apps SDK manifest
```

### Data Flow

| Step | Component | Action |
|------|-----------|--------|
| 1 | ChatGPT | User sends natural language query |
| 2 | OpenAI LLM | Decides to call GEOX function |
| 3 | `window.openai` | SDK invokes registered tool |
| 4 | `openai_adapter.ts` | Receives `OpenAIToolCall` |
| 5 | Adapter | Maps to GEOX tool name |
| 6 | MCP Bridge | Sends `tool.request` via postMessage |
| 7 | GEOX Backend | Executes tool with F1-F13 checks |
| 8 | MCP Bridge | Returns `tool.response` |
| 9 | Adapter | Formats `OpenAIToolResponse` |
| 10 | ChatGPT | Displays result to user |

---

## Constitutional Integration

### F1 Amanah (Trust)
- All sessions are reversible
- Audit trail preserved in vault
- Session timeout: 30 minutes

### F2 Truth (Evidence)
- All tool outputs include confidence levels
- Data sources explicitly cited
- Limitations documented per tool

### F3 Tri-Witness (Consensus)
- Human: Natural language intent
- AI: ChatGPT interpretation
- System: GEOX constitutional verification

### F7 Humility (Uncertainty)
```typescript
// Confidence capped at 0.90
confidence: Math.min(result.confidence, 0.90)
```

### F11 Auditability
- Every OpenAI interaction logged
- Event types: `tool.start`, `tool.complete`, `tool.error`, `session.update`
- Logs sent to parent for vault storage

### F13 Sovereign (Human Override)
```typescript
// High-risk operations trigger 888_HOLD
if (highRiskTools.includes(toolName)) {
  return {
    verdict: 'HOLD',
    error: '888_HOLD: Action blocked pending sovereign review'
  };
}
```

---

## Available Tools

| OpenAI Name | GEOX Tool | Description |
|-------------|-----------|-------------|
| `geox_system_health` | `geox_health` | System status + F1-F13 floors |
| `geox_query_malay_basin` | `geox_malay_basin_pilot` | Malay Basin petroleum data |
| `geox_load_seismic` | `geox_load_seismic_line` | Seismic line loading |
| `geox_analyze_structure` | `geox_build_structural_candidates` | Structural interpretation |
| `geox_evaluate_prospect` | `geox_evaluate_prospect` | Prospect viability (888_HOLD possible) |
| `geox_compute_saturation` | `geox_calculate_saturation` | Sw calculation with uncertainty |
| `geox_query_geology` | `geox_query_macrostrat` | Macrostrat database queries |

---

## React Hooks

### `useOpenAI()`

Main hook for adapter state and control.

```typescript
const {
  status,           // 'idle' | 'initializing' | 'ready' | 'error'
  isReady,          // boolean
  isError,          // boolean
  error,            // string | null
  session,          // OpenAISession | null
  registeredTools,  // string[]
  init,             // () => Promise<void>
  reset,            // () => void
  sessionId,        // string | null
  toolCount,        // number
} = useOpenAI();
```

### `useAutoInitOpenAI(config?, enabled?)`

Auto-initializes on mount.

```typescript
const openai = useAutoInitOpenAI({}, true);
// Automatically calls init() when enabled
```

### `useOpenAIToolAvailable(toolName)`

Check if specific tool is registered.

```typescript
const hasSaturationTool = useOpenAIToolAvailable('geox_compute_saturation');
```

### `useOpenAISession()`

Get session metadata.

```typescript
const { sessionId, geoxSessionId, isActive } = useOpenAISession();
```

---

## Error Handling

### Verdict Types

| Verdict | Meaning | User Message |
|---------|---------|--------------|
| `SEAL` | Success | Full result with confidence |
| `COMPLY` | Success with notes | Result + warnings |
| `CAUTION` | Proceed with care | Result + floor warnings |
| `HOLD` | Blocked (F13) | "Requires human review" |
| `VOID` | Failed | Error explanation |

### Example Error Response

```json
{
  "ok": false,
  "error": "888_HOLD: Action blocked pending sovereign review (F13)",
  "verdict": "HOLD",
  "explanation": "This geox_evaluate_prospect operation requires sovereign (human) review before proceeding.",
  "floors": {
    "passed": [],
    "warned": [],
    "failed": ["F13"]
  }
}
```

---

## Security

### Domain Allowlist
```typescript
allowedDomains: [
  'https://geox.arif-fazil.com',
  'https://chat.openai.com'
]
```

### Session Management
- Sessions expire after 30 minutes
- GEOX session linked to OpenAI session
- No persistent storage of credentials

### F13 Sovereign Blocks
High-risk operations automatically trigger 888_HOLD:
- Prospect evaluation with high confidence threshold
- Any delete/modify operations
- Operations flagged by governance layer

---

## Testing

### Local Development

```bash
# Start GEOX backend
cd /root/GEOX
python geox_mcp_server.py

# In another terminal, test adapter
node -e "
  const { initOpenAIAdapter } = require('./geox-gui/src/adapters');
  initOpenAIAdapter().then(() => console.log('Ready'));
"
```

### ChatGPT Testing

1. Load manifest in ChatGPT developer mode
2. Verify tool registration
3. Test each tool with sample queries
4. Verify F13 blocks on high-risk operations

---

## Deployment

### GPT Store Publication

1. Submit `openai_manifest.json` to OpenAI
2. Provide demo video showing constitutional governance
3. Include F1-F13 explanation in app description
4. Link to GEOX wiki for documentation

### Environment Variables

```env
# .env for ChatGPT integration
OPENAI_ADAPTER_ENABLED=true
OPENAI_API_VERSION=2024-01-01
GEOX_API_URL=https://geox.arif-fazil.com
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.6.1 | 2026-04-10 | Initial OpenAI Adapter SDK implementation |

---

## Related Documentation

- [[GEOX_MCP_Apps_Architecture]] — Host-agnostic design
- [[MCP_FORGE_PATTERNS]] — Design patterns
- [[888_HOLD_Registry]] — Safety veto history
- [[Floors]] — F1-F13 constitutional reference

---

**Sealed by:** 888_JUDGE  
**Date:** 2026-04-10  
**Authority:** Muhammad Arif bin Fazil

*DITEMPA BUKAN DIBERI — Forged, Not Given*
