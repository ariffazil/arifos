# App Interface Contracts — Manifest & Event Bus

> **DITEMPA BUKAN DIBERI**
> **Authority:** ΔΩΨ | **Standard:** FastMCP 3.x Compliant

This document defines the technical contracts for GEOX Microfrontends (Apps) to interact with any compliant AI Host (ChatGPT, Claude, FastMCP Dashboard).

## 1. Canonical Manifest
Each app must provide a `manifest.json` in its root directory.

### Schema
- `app_id`: `geox.[domain].[name]`
- `ui_entry`: URI to the index.html (Standard MIME: `text/html;profile=mcp-app`).
- `tools_required`: Array of MCP tool names.
- `visibility`: `["model"]` for LLM entry points, `["app"]` for backend tools.

## 2. Event Bus (JSON-RPC 2.0)
Communication occurs via `window.postMessage` using the `@modelcontextprotocol/ext-apps` bridge.

### App-to-Host
- `app.initialize`: Initial handshake and capabilities report.
- `callServerTool`: Request host to execute an MCP tool (proxied to `tools/call`).
- `ui.action`: Signal a user interaction (e.g., "pick_horizon").
- `ui.state.sync`: Periodic state update for LLM context.

### Host-to-App
- `app.context.patch`: Update geological focus (coordinates, well_id).
- `tool.response`: (Standard RPC result) The output of a `callServerTool` request.

## 3. The `_meta` Envelope
All tool results triggering an app must include the following metadata:

```json
{
  "view": { "type": "SeismicSection", ... },
  "state": { "line_id": "L-101", ... },
  "_meta": {
    "fastmcp": {
      "app": "geox.seismic.viewer"
    },
    "ui": {
      "resourceUri": "ui://geox/seismic-viewer/index.html",
      "visibility": ["model"]
    }
  }
}
```

---

*Reference Implementation: arifos/geox/contracts/manifest.py*
