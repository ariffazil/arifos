# MCP_FORGE_ANTI_PATTERNS.md — MCP Implementation Risks

> **DITEMPA BUKAN DIBERI** — *Forged, Not Given*
> **Status:** PROPOSED | **Authority:** ΔΩΨ

This document flags implementation choices that lead to vendor lock-in, architectural fragility, or constitutional violations, derived from common pitfalls in the MCP/AI App ecosystem.

---

## 🛑 Anti-Patterns to Avoid

### 1. Vendor-Specific Runtime Coupling
**The Risk:** Building logic that only works within the ChatGPT widget runtime or the Claude MCP iframe without an abstraction layer.
**Avoid:** Using `window.openai` or similar global objects directly in domain-critical code.
**Solution:** Use a GEOX-managed event bridge that translates host-specific APIs into a unified platform contract.

### 2. Buried Domain Logic
**The Risk:** Implementing geological physics or interpretation rules inside the UI (React/Vue/Svelte) instead of the MCP server.
**Avoid:** Calculating `Sw` or `Vcl` in a JavaScript frontend handler.
**Solution:** The UI should only capture inputs and display results; all heavy lifting remains in the **333_MIND (Python Core)**.

### 3. State-in-the-Blind
**The Risk:** Assuming the UI state is perfectly preserved across turns without explicit server-side backing.
**Avoid:** Relying on the host's "temporary" session storage for critical interpretation data.
**Solution:** Every significant UI change must sync back to the MCP server's canonical state (or be persisted in the `999_VAULT`).

### 4. Direct External API Calls from UI
**The Risk:** Bypassing the MCP server to call external data sources (e.g., Macrostrat, OSDU) from the browser.
**Avoid:** Performing `fetch()` calls to secured endpoints from the sandboxed iframe.
**Solution:** Use the MCP server as a proxy to ensure auth tokens are managed securely and all data access is audited.

### 5. Silent Failure Modes
**The Risk:** Failing silently when a host doesn't support a specific capability (like 3D rendering).
**Avoid:** Broken UI components or empty viewports.
**Solution:** Implement a **Graceful Degradation** fallback (e.g., "3D view unavailable — switching to 2D cross-section and text summary").

---

## ⚠️ Governance Redlines

- **No Secret Commits:** Never hardcode API keys in the app manifest or UI code.
- **No Ungrounded Claims:** UI must never present a "final interpretation" without surfacing the associated confidence band (F7 Humility).
- **No Conflation:** Avoid visual artifacts that mimic geological features (ToAC protection).

---

*Sealed by: 888_JUDGE | 2026.04.09*
*DITEMPA BUKAN DIBERI*
