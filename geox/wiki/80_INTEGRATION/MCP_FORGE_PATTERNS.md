# MCP_FORGE_PATTERNS.md — Canonical MCP App Patterns

> **DITEMPA BUKAN DIBERI** — *Forged, Not Given*
> **Status:** PROPOSED | **Authority:** ΔΩΨ

This document identifies canonical patterns for building platform-agnostic MCP Apps, extracted from high-signal repositories including `modelcontextprotocol/ext-apps`, `openai/openai-apps-sdk-examples`, and `github/github-mcp-server`.

---

## 🏗️ Architectural Invariants

### 1. Capability Plane First
The MCP server is the canonical capability plane. Tools, resources, and prompts should be fully functional in a text-only environment before being "decorated" with a UI.
- **Reference:** `github/github-mcp-server`, `gofastmcp.com/apps/interactive-apps`
- **Pattern:** Use `@app.ui()` for LLM-visible entry points and `@app.tool(visibility=["app"])` for private UI-only backend tools.

### 2. Portable UI Microfrontends
UI should be an interactive HTML/JS package that communicates with the host via a standard JSON-RPC/postMessage bridge.
- **Reference:** `modelcontextprotocol/ext-apps`
- **Pattern:** Use `_meta.ui.resourceUri` to point to a portable index.html inside a sandboxed iframe. Register the resource with MIME type `text/html;profile=mcp-app`.

### 3. Modular Folder Structure
Separate code by responsibility to ensure scalability and portability.
- **Reference:** `tayler-id/social-media-mcp`
- **Structure:**
  - `/core`: Domain logic, models, physics, and theory.
  - `/types`: Typed schemas for tools and events.
  - `/platforms`: Host adapters (OpenAI, Claude, Custom).
  - `/config`: Env-specific and deployment settings.

### 4. Self-Knowledge Retrieval
Implement MCP tools that allow the agent to reason over its own documentation, code, and architectural history.
- **Reference:** `probelabs/docs-mcp`
- **Pattern:** A `geox_query_memory` tool that bridges the current evaluation with the philosophical atlas and past results.

### 5. Session-Aware State Management
Explicitly track `widgetSessionId` and sync state across turns to ensure the UI feels "alive" and persistent within a conversation.
- **Reference:** `openai/openai-apps-sdk-examples`
- **Pattern:** Wrap host-specific session metadata in a canonical `GEOX_SESSION` object.

---

## 🛠️ Implementation SNIPPETS

### Canonical Manifest Fragment
```json
{
  "app_id": "geox.seismic-viewer",
  "version": "1.0.0",
  "capabilities": {
    "tools": ["load_line", "build_candidates"],
    "resources": ["seismic_schema"]
  },
  "ui": {
    "entry": "public/index.html",
    "mode": "sandboxed-iframe"
  }
}
```

### Event Bus Pattern (JSON-RPC)
```javascript
// App-side listener
window.addEventListener('message', (event) => {
  const { method, params, id } = event.data;
  if (method === 'app.context.patch') {
    updateState(params);
  }
});

// Requesting a tool call from UI
window.parent.postMessage({
  jsonrpc: "2.0",
  method: "tool.request",
  params: { name: "geox_calculate_saturation", args: { ... } },
  id: "uuid-123"
}, "*");
```

---

*Sealed by: 888_JUDGE | 2026.04.09*
*DITEMPA BUKAN DIBERI*
