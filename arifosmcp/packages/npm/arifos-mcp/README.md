# @arifos/mcp

**L2 Skills Adapter** — TypeScript client for the arifOS Constitutional AI Governance System.

> **F4 CLARITY:** This package is a **CABLE**, not the **KERNEL**.  
> Governance authority resides exclusively in the PyPI [`arifosmcp`](https://pypi.org/project/arifosmcp/) package.  
> This npm package only provides TypeScript types and a thin MCP transport client.

---

## Installation

```bash
npm install @arifos/mcp
# or
pnpm add @arifos/mcp
# or
yarn add @arifos/mcp
```

---

## Quick Start

### HTTP Mode (Remote VPS)

```typescript
import { createClient, ENDPOINTS } from '@arifos/mcp';

const client = await createClient({
  transport: 'http',
  endpoint: ENDPOINTS.VPS,  // https://arifosmcp.arif-fazil.com/mcp
});

await client.connect();

// Start a governed session
const { session_id } = await client.anchorSession('My research task');
console.log('Session:', session_id);

// Execute governed reasoning
const result = await client.reasonMind('What is quantum computing?');
console.log('Verdict:', result.verdict);  // SEAL | PARTIAL | SABAR | VOID | 888_HOLD
console.log('Floors passed:', result.floors.passed.length);

await client.disconnect();
```

### stdio Mode (Local)

> **⚠️ SECURITY:** Never hardcode secrets. Load from `.env` or a secrets manager.

```typescript
import { createClient } from '@arifos/mcp';

const client = await createClient({
  transport: 'stdio',
  env: {
    // Load from environment — never commit these values
    ARIFOS_GOVERNANCE_SECRET: process.env.ARIFOS_GOVERNANCE_SECRET!,
    DATABASE_URL: process.env.DATABASE_URL!,
  },
});

await client.connect();
// ... use client
await client.disconnect();
```

---

## Architecture

```text
┌─────────────────────────────────────┐
│  Your Application (JS/TS)           │
│  ┌─────────────────────────────┐    │
│  │  @arifos/mcp (L2 Adapter)   │    │
│  │  ├── types.ts (mirrors)     │    │
│  │  ├── client.ts (transport)  │    │
│  │  └── langchain.ts (stub)    │    │
│  └───────────┬─────────────────┘    │
└──────────────┼──────────────────────┘
               │ MCP Protocol
┌──────────────▼──────────────────────┐
│  arifosmcp (PyPI) — THE KERNEL         │
│  ├── core/ (13 Floors, Trinity)     │
│  ├── arifosmcp.runtime/ (MCP server)   │
│  └── VAULT999 (immutable ledger)    │
└─────────────────────────────────────┘
```

**Key Principle:** This package has **ZERO governance logic**. All constitutional enforcement (F1-F13) happens server-side in the Python kernel. The npm client is a transport client that passes through whatever the kernel decides.

---

## API Reference

### `createClient(config)`

Create an MCP client connection to arifOS.

```typescript
interface ArifOSClientConfig {
  transport: 'stdio' | 'http';
  endpoint?: string;          // Required for http
  env?: Record<string, string>; // Required for stdio
  timeout?: number;           // Default: 60000ms
  debug?: boolean;
}
```

### Client Methods

| Method | Description |
| :--- | :--- |
| `client.connect()` | Establish MCP connection |
| `client.disconnect()` | Close connection |
| `client.anchorSession(context?)` | Start new governed session |
| `client.reasonMind(query, context?)` | Execute 333_MIND reasoning |
| `client.apexJudge(action, risk_level?)` | Get 888_APEX judgment |
| `client.callTool(name, params)` | Call any of 13 canonical tools |
| `client.listTools()` | Discover available tools |

### Types

```typescript
import type { 
  Verdict,        // 'SEAL' | 'PARTIAL' | 'SABAR' | 'VOID' | '888_HOLD'
  FloorCode,      // 'F1' | 'F2' | ... | 'F13'
  Stage,          // '000_INIT' | ... | '999_VAULT'
  VerdictEnvelope,
  ArifOSMetadata,
} from '@arifos/mcp';
```

---

## Compatibility Matrix

| @arifos/mcp | Node.js | arifOS (PyPI) | Transport | Status |
| :--- | :--- | :--- | :--- | :--- |
| 0.2.0 | ≥18 | ≥2026.3.1 | HTTP/SSE | 🔄 **Current** |
| 0.1.1 | ≥18 | 2026.2.22 | HTTP/SSE | ✅ Tested |
| 0.1.0 | ≥18 | 2026.2.17 | HTTP/SSE | ✅ Stable |

**Notes:**
- All versions tested against production VPS endpoint (`arifosmcp.arif-fazil.com`)
- `stdio` transport tested locally with `arifosmcp>=2026.2.17`
- Verdicts observed: `SEAL`, `PARTIAL`, `SABAR`, `VOID`, `HOLD`, `888_HOLD`

---

## The 13 Canonical Tools

All tools return a `VerdictEnvelope` with `{ verdict, stage, session_id, floors, ... }`.

> **Note on 888_HOLD:** This verdict indicates an irreversible action requiring human approval. The call may remain pending until a human sovereign signs off. Handle this as an async event, not a timeout.

### Governance Spine (8 tools)

| Tool | Stage | Purpose |
| :--- | :--- | :--- |
| `anchor_session` | 000_INIT | Session ignition & injection defense |
| `reason_mind` | 333_MIND | AGI cognition & causal tracing |
| `recall_memory` | 444_PHOENIX | Associative memory recall |
| `simulate_heart` | 555_HEART | Stakeholder impact analysis |
| `critique_thought` | 666_CRITIQUE | Self-critique & bias detection |
| `apex_judge` | 888_APEX | Sovereign verdict + governance_token |
| `eureka_forge` | 777_FORGE | Sandboxed action execution |
| `seal_vault` | 999_VAULT | Immutable ledger commit |

### Utility Tools (5 tools, read-only)

| Tool | Purpose |
| :--- | :--- |
| `search_reality` | Web grounding |
| `fetch_content` | URL retrieval |
| `inspect_file` | Filesystem inspection |
| `audit_rules` | Governance rule audit |
| `check_vital` | System health |

---

## Error Handling

```typescript
import { ArifOSError } from '@arifos/mcp';

try {
  await client.reasonMind('...');
} catch (error) {
  if (error instanceof ArifOSError) {
    console.log(error.code);   // 'CONNECTION_FAILED' | 'INVALID_RESPONSE' | ...
    console.log(error.stage);  // Stage where error occurred
    console.log(error.floor);  // Floor that triggered error (if any)
  }
}
```

---

## Development

```bash
# Install dependencies
pnpm install

# Build
pnpm run build

# Type check
pnpm run typecheck

# Test
pnpm test
```

---

## License

AGPL-3.0-only — Same as arifOS kernel.

---

## Links

- **arifOS Kernel:** <https://pypi.org/project/arifosmcp/>
- **Documentation:** <https://arifos.arif-fazil.com>
- **Repository:** <https://github.com/ariffazil/arifosmcp>
- **MCP Protocol:** <https://modelcontextprotocol.io>

*Ditempa Bukan Diberi* — Forged, Not Given
