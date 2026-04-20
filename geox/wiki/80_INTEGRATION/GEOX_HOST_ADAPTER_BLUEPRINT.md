# GEOX Host Adapter Blueprint — Platform Agnosticism

**Status:** ✅ SEALED
**Authority:** 888_JUDGE
**Epoch:** 2026-04-09

---

## 1. Core Principle

GEOX Apps must not import vendor-specific SDKs into the domain layer. All host interaction occurs via the **Host Adapter Interface**.

---

## 2. Adapter Interface Specification

| Capability | GEOX Standard | Adapter Requirement |
| :--- | :--- | :--- |
| **Identity** | GEOX-Sovereign JWT | Map Host User ID to GEOX Tenant ID. |
| **Rendering** | Standard Web Shell | Provide sandboxed iframe or launch external URL. |
| **State Sync** | JSON-RPC Bridge | Proxy app state updates back to Host LLM context. |
| **Tooling** | standard MCP tools | Register GEOX tools with Host MCP client. |

---

## 3. Implementation Patterns

### 3.1 Inline Adapter (L3 Rendering)

Used by ChatGPT Widgets and Claude Artifacts.

- `Host -> GEOX`: PostMessage(appIntent, config).
- `GEOX -> Host`: PostMessage(uiAction, telemetry).

### 3.2 Deep-Link Adapter (L4 Rendering)

Used by Microsoft Copilot and text-only hosts.

- `Host -> User`: Signed URL (`geox.link/launch?token=...`).
- `GEOX -> WebShell`: HMAC verification and session instantiation.

---

**Audit Reference:** `VOID_20260409_074829`
