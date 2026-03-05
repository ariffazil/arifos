# Constitutional Decision Visualizer

A dual-mode MCP App that visualizes arifOS governance metrics in real-time.

## Modes

| Mode | Output | Usage |
|------|--------|-------|
| **MCP App** | `dist/mcp-app.html` | Served via `ui://constitutional-visualizer/mcp-app.html` resource |
| **Standalone Web** | `dist-web/` | Served at `/dashboard` via FastAPI static files |

## Build Instructions

```bash
# Install dependencies
npm install

# Build both modes (MCP App + standalone web)
npm run build

# Build only the MCP App (dist/)
npm run build:mcp

# Build only the standalone web dashboard (dist-web/)
npm run build:web
```

## Local Development

```bash
# MCP App mode (default)
npm run dev:mcp

# Standalone web mode
npm run dev:web

# Serve built standalone dashboard
npm run serve
```

## API Endpoints

The visualizer connects to these arifOS REST endpoints:

### `GET /api/governance-status`

Returns current governance telemetry.

```json
{
  "telemetry": {
    "dS": -0.35,
    "peace2": 1.04,
    "kappa_r": 0.97,
    "echoDebt": 0.4,
    "shadow": 0.3,
    "confidence": 0.88,
    "psi_le": 0.82,
    "verdict": "SEAL"
  },
  "witness": {
    "human": 0.42,
    "ai": 0.32,
    "earth": 0.26
  },
  "qdf": 0.83,
  "floors": {
    "F1": 0.85,
    "F2": 0.99,
    "F3": 0.95,
    "F4": 0.90,
    "F5": 1.04,
    "F6": 0.97,
    "F7": 0.04,
    "F8": 0.88,
    "F9": 0.12,
    "F10": 1.0,
    "F11": 1.0,
    "F12": 0.15,
    "F13": 1.0
  },
  "session_id": "sess_abc123",
  "timestamp": "2026-03-05T12:00:00Z",
  "metabolic_stage": 333
}
```

### `GET /api/governance-history?limit=20`

Returns recent VAULT999 session history.

```json
{
  "sessions": [
    {
      "session_id": "sess_abc123",
      "verdict": "SEAL",
      "stage": "999_VAULT",
      "timestamp": "2026-03-05T12:00:00Z",
      "floors": {}
    }
  ],
  "count": 1,
  "limit": 20
}
```

## MCP Tool

The visualizer is exposed as an MCP tool:

```
Tool: visualize_governance
Parameter: session_id (optional, str)
Returns: { _meta: { ui: { resourceUri: "ui://constitutional-visualizer/mcp-app.html" } } }
```

## Deployment Verification

After deployment:

```bash
# Check governance status API
curl http://localhost:8080/api/governance-status

# Check standalone dashboard
curl http://localhost:8080/dashboard

# Check MCP tools list (includes visualize_governance)
curl http://localhost:8080/tools

# Check MCP resource is registered
# Connect via MCP client and call: resources/read ui://constitutional-visualizer/mcp-app.html
```

## Directory Structure

```
constitutional-visualizer/
├── src/                  # React source files
│   ├── main.tsx          # MCP App entry
│   ├── mcp-app.tsx       # MCP App component
│   └── web-main.tsx      # Standalone web entry
├── dist/                 # MCP App build output (git-ignored)
│   └── mcp-app.html      # Single-file MCP App
├── dist-web/             # Standalone web build output
│   ├── index.html
│   └── assets/
├── vite.config.ts        # MCP App Vite config
├── vite.web.config.ts    # Standalone web Vite config
└── package.json
```

> **Note:** Run `npm install && npm run build` before deploying.
> The `dist/` directory (MCP App) is required for the `ui://constitutional-visualizer/mcp-app.html` resource.
> The `dist-web/` directory is required for the `/dashboard` static file route.
