# GEOX MCP Apps Architecture

**Parent:** [[80_INTEGRATION/MCP_Integration]]
**Status:** 🔐 SEALED ✅ · G★ 0.92
**Epoch:** 2026-04-09

---

## 1. Executive Summary
GEOX MCP Apps are host-agnostic, interactive microfrontends designed to run inside any AI surface (ChatGPT, Copilot, Claude) while remaining grounded in the **Sovereign GEOX Core**.

---

## 2. The Dual-Mode Model (Capability + Enhancement)
GEOX capabilities operate in two concurrent modes, ensuring they are functional in "Text-Only" hosts and premium in "App-Capable" hosts.

- **Mode A: Normal MCP**: The tool returns high-signal Markdown and structured JSON. It is 100% useful without a UI.
- **Mode B: MCP App**: The same tool attaches a UI resource URI (e.g., `_meta.ui.resourceUri`). Hosts supporting Apps render an interactive HTML interface on top of the data.

### Design Rule:
> **"If the UI disappears, the tool must still be useful."**
Essential domain logic (physics models, governance checks) must live in the MCP server, never exclusively in the frontend.

---

## 3. The 6-Layer Stack

| Layer | Component | Responsibility |
| :--- | :--- | :--- |
| **L6** | Security | AuthN (JWT), 999_VAULT Audit, Iframe Sandboxing. |
| **L5** | UI Layer | React + TypeScript + Tailwind (geox-gui). |
| **L4** | Host Adapter | Translation between GEOX and Vendor SDKs (OpenAI, MS). |
| **L3** | Orchestration | App manifests, Intent resolution, Capability negotiation. |
| **L2** | Domain Logic | geox_mcp_server.py, Physics Engine, F1-F13 Validation. |
| **L1** | Transport | standard MCP JSON-RPC 2.0 (stdio/SSE). |

---

## 3. Host Rendering Levels (L1-L4)
1. **L1 (Text)**: Markdown response (Universal).
2. **L2 (Rich Cards)**: Structured UI (Copilot Adaptive Cards).
3. **L3 (Inline Iframe)**: Embedded interactive app (ChatGPT Widget, Claude Artifact).
4. **L4 (External)**: Full-screen Web Shell (Universal via Signed Deep Link).

---

## 4. Interaction Protocol
Communication between the GEOX App and the Host environment uses a standardized **JSON-RPC Bridge**:
- `ui.action`: User clicks/zooms in the GUI.
- `ui.state.sync`: App state (e.g., current seismic slice) synced to the LLM context.
- `tool.request`: App UI requesting more data from the MCP server.

---

## 5. Security Boundaries
- **HMAC Links**: External web shell sessions are protected by short-lived, signed tokens.
- **CSP**: All inline apps operate under strict Content Security Policies.
- **888_HOLD**: All irreversible or physically invalid actions are gated by human sign-off.

---

**Audit Reference:** `VOID_20260409_074257`
