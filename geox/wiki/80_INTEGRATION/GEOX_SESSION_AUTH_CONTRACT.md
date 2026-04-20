# GEOX Session & Auth Contract — Sovereign Identity

**Status:** ✅ SEALED
**Authority:** 888_JUDGE
**Epoch:** 2026-04-09

---

## 1. Objective

Enable seamless, secure transition from a Host AI chat to a stand-alone GEOX Web Shell without losing context or violating tenant boundaries.

---

## 2. The Sovereign Bridge

### 2.1 The Auth Token (JWT)

The GEOX MCP server issues short-lived, signed JWTs containing:

- `sub`: The host-specific user identifier.
- `app_id`: The intention (e.g., `geox.view.seismic`).
- `context_id`: Hash of the current chat session.
- `floors`: The active constitutional floors for this user.

### 2.2 Token Exchange

1. **AI Host** requests a "Deep Link" tool.
2. **GEOX Server** signs a token and returns a URL: `https://geox.apps/launch?token={JWT}`.
3. **GEOX Web Shell** validates the JWT on the server before rendering protected geological data.

---

## 3. Session Stability

- **Context Preservation**: The Web Shell must request the latest "Context Patch" from the MCP server to replicate the LLM's current understanding.
- **Audit Logging**: Every access via deep link is recorded in **999_VAULT**.

---

**Audit Reference:** `VOID_20260409_074829`
