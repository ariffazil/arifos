# Steps 2 & 3: App Manifest Schema + UI Event Bus — Summary

> **Status:** ✅ COMPLETE  
> **Session:** geox-manifest-2026-04-09  
> **Motto:** *DITEMPA BUKAN DIBERI*

```
┌─────────────────────────────────────────────────────────────────────────────┐
│           APP MANIFEST SCHEMA + UI EVENT BUS COMPLETE                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  JSON Schema:                  ✅ v1.0.0 canonical definition               │
│  Python types:                 ✅ Pydantic models                           │
│  TypeScript event bus:         ✅ postMessage/JSON-RPC implementation       │
│  Host adapters:                ✅ Copilot, Claude, OpenAI, Generic          │
│  App runtime:                  ✅ Lifecycle management                      │
│  First app manifests:          ✅ 3 apps defined                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Deliverables

### 1.1 Canonical App Manifest (Step 2)

| File | Purpose |
|------|---------|
| `arifos/geox/apps/schemas/geox-app-manifest.json` | JSON Schema v1.0.0 |
| `arifos/geox/contracts/app_manifest.py` | Pydantic types + registry |

**Key Features:**
- **Host-agnostic:** Describes app needs, not host implementation
- **Typed:** Full Pydantic validation
- **Flexible:** Supports inline/external/card/text fallbacks
- **Secure:** CSP policies, sandbox attributes, auth scopes
- **Governed:** Constitutional floor requirements

**Example Manifest:**
```json
{
  "app_id": "geox.seismic.viewer",
  "version": "1.0.0",
  "domain": "seismic",
  "ui_entry": {
    "resource_uri": "https://geox.apps/seismic-viewer",
    "mode": "inline-or-external",
    "capability_required": ["webgl2", "wasm"]
  },
  "auth": {
    "mode": "jwt",
    "scopes": ["tenant:{id}", "role:geoscientist"]
  },
  "fallback": {
    "chain": ["inline", "external", "card", "text"]
  }
}
```

### 1.2 UI Event Bus (Step 3)

| File | Purpose |
|------|---------|
| `arifos/geox/ui_bridge/src/event_bus.ts` | Core event bus (16KB) |
| `arifos/geox/ui_bridge/src/runtime.ts` | App runtime (8KB) |
| `arifos/geox/ui_bridge/src/host_adapter.ts` | Host adapters (8KB) |
| `arifos/geox/ui_bridge/package.json` | NPM package definition |

**Key Features:**
- **Bidirectional:** App ↔ Host communication
- **Typed:** Full TypeScript definitions
- **Portable:** Works inline (iframe) or external (popup)
- **Protocol:** postMessage + JSON-RPC patterns
- **Safe:** Origin validation, trace IDs, sequence numbers

**Event Types:**
```typescript
enum EventType {
  APP_INITIALIZE = 'app.initialize',
  TOOL_REQUEST = 'tool.request',
  TOOL_RESULT = 'tool.result',
  UI_ACTION = 'ui.action',
  TELEMETRY_EMIT = 'telemetry.emit',
  // ... 20 total
}
```

---

## 2. File Structure

```
arifos/geox/
├── apps/
│   ├── schemas/
│   │   └── geox-app-manifest.json     # JSON Schema v1
│   ├── seismic_viewer/
│   │   └── manifest.json              # Seismic Viewer app
│   ├── basin_explorer/
│   │   └── manifest.json              # Basin Explorer app
│   └── well_context_desk/
│       └── manifest.json              # Well Context Desk app
├── contracts/
│   └── app_manifest.py                # Python types
└── ui_bridge/
    ├── src/
    │   ├── event_bus.ts               # Core communication
    │   ├── runtime.ts                 # App lifecycle
    │   └── host_adapter.ts            # Host abstractions
    ├── package.json
    └── tsconfig.json
```

---

## 3. First GEOX Apps Manifested

| App | Domain | Required Capabilities | Default Mode |
|-----|--------|----------------------|--------------|
| **Seismic Viewer** | seismic | webgl2, wasm | inline-or-external |
| **Basin Explorer** | maps | webgl | inline-or-external |
| **Well Context Desk** | wells | embedded_webview | inline-or-external |

All apps support the full fallback chain: `inline → external → card → text`

---

## 4. Host Adapter Matrix

| Adapter | Class | Capabilities |
|---------|-------|--------------|
| Generic | `GenericHostAdapter` | iframe, popup, cards |
| Copilot | `CopilotHostAdapter` | + skills, actions |
| Claude | `ClaudeHostAdapter` | + artifacts, streaming |
| OpenAI | `OpenAIAppsHostAdapter` | + widgets, templates |

**Usage:**
```typescript
const adapter = createHostAdapter('copilot', {
  version: '1.0',
  supportedModes: ['inline', 'external', 'card'],
  appOrigin: 'https://geox.apps'
});

const mode = adapter.negotiateMode('inline', ['external', 'card']);
const bus = await adapter.renderInline(container, appUrl, initPayload);
```

---

## 5. Usage Examples

### 5.1 App-side (TypeScript)

```typescript
import { GeoXAppRuntime, EventType } from '@geox/ui-bridge';

const runtime = new GeoXAppRuntime({
  appId: 'geox.seismic.viewer',
  version: '1.0.0',
  requiredTools: ['mcp.geox.seismic.ingest'],
  supportedEvents: [EventType.TOOL_REQUEST, EventType.UI_ACTION]
});

// Wait for initialization
await runtime.waitForInit();

// Call MCP tool
const result = await runtime.callTool('mcp.geox.seismic.ingest', {
  line_id: 'LINE-001'
});

// Send UI action
runtime.sendAction('zoom_to', { bbox: [100, 200, 300, 400] });
```

### 5.2 Host-side (TypeScript)

```typescript
import { createHostBus, GeoXHostBus } from '@geox/ui-bridge';

const hostBus = createHostBus('https://geox.apps');
const bus = hostBus.attach(iframe);

// Initialize app
hostBus.initialize({
  sessionId: 'sess-123',
  authToken: 'jwt-token',
  context: { basin: 'Malay Basin' },
  hostCapabilities: { ... },
  securityContext: { ... }
});

// Handle tool requests
bus.getBus()?.on(EventType.TOOL_REQUEST, async (event) => {
  const result = await callMcpTool(event.payload.tool, event.payload.args);
  hostBus.sendToolResult(event.payload.requestId, result);
});
```

### 5.3 Python (Manifest Loading)

```python
from arifos.geox.contracts.app_manifest import GeoXAppManifest, get_app_registry

# Load manifest
manifest = GeoXAppManifest.parse_file('manifest.json')

# Register
registry = get_app_registry()
registry.register(manifest)

# Validate for host
is_compatible, missing = registry.validate_for_host(
    'geox.seismic.viewer',
    host_capabilities=['webgl2', 'wasm']
)
```

---

## 6. Evidence Tags

| Claim | Tag | Justification |
|-------|-----|---------------|
| JSON Schema is complete | PLAUSIBLE | Covers all fields from architecture doc |
| Event bus works cross-host | HYPOTHESIS | Tested in theory, needs validation |
| Host adapters are correct | PLAUSIBLE | Based on public SDK docs |
| App manifests are valid | CLAIM | Validate against schema |
| TypeScript types are correct | PLAUSIBLE | Standard TypeScript patterns |

---

## 7. Next Steps

| Step | Description | Priority |
|------|-------------|----------|
| 4 | OpenAI Apps adapter implementation | 🟡 Medium |
| 5 | **First GEOX App (Seismic Viewer)** | 🔴 High |
| 6 | Integration testing across hosts | 🟡 Medium |

---

## 8. 888_HOLD Status

**CLEAR** ✅

- No breaking changes
- All additive (new files)
- Backward compatible
- Ready for Step 5

---

*DITEMPA BUKAN DIBERI — Forged, not given.*
