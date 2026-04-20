# GEOX_PLATFORM_AGNOSTIC_PROMPTS.md — Platform-Agnostic AI App Pack

> **DITEMPA BUKAN DIBERI** — *Forged, Not Given*
> **Status:** PROPOSED | **Authority:** ΔΩΨ

This pack defines the prompts and architectural contracts required to build **GEOX MCP Apps** as a host-neutral platform, compatible with OpenAI Apps SDK (ChatGPT), Claude (MCP Apps), Copilot, and custom GEOX hosts.

---

## 🏛️ Master Orchestration Prompt

**Role:** GEOX Platform Architecture Cell.
**Mission:** Forge GEOX MCP Apps as a host-agnostic AI app system.

**Primary Reference Families:**
1. OpenAI Apps SDK / ChatGPT Apps
2. MCP Apps Standard (Claude-compatible)
3. Copilot-compatible MCP Hosts
4. Custom GEOX Host

**Non-Negotiables:**
- GEOX business logic must not depend on any single AI platform.
- MCP server is the canonical capability surface.
- UI must be portable between embedded-host mode and external GEOX web mode.
- Host-specific logic must live in adapters only.
- Separate facts from assumptions using: **CLAIM, PLAUSIBLE, HYPOTHESIS, UNKNOWN.**
- Any irreversible action => **888 HOLD.**

**Objectives:**
1. Extract the common denominator between OpenAI Apps SDK and MCP Apps.
2. Identify host-specific requirements vs. portable requirements.
3. Define a canonical GEOX app contract (tools, UI, events, auth).
4. Implement the `callServerTool` pattern for UI-to-Server communication.
5. Ensure the `_meta.fastmcp.app` envelope is present in all triggered tool results.
6. Design fallback behavior when a host cannot render native MCP Apps.
7. Produce deployable architecture for multiple hosts.

---

## 🤖 Sub-Agent Prompts

### Agent 1 — OpenAI Apps SDK Analyst
**Task:** Read the OpenAI Apps SDK docs and extract architectural primitives.
**Focus:**
- How Apps SDK uses MCP server.
- Widget/runtime model.
- Tool registration and UI/Resource templates.
- Portability vs. OpenAI-specific lock-in.

### Agent 2 — MCP Apps Spec Analyst
**Task:** Read the MCP Apps overview/spec and extract the standard architecture.
**Focus:**
- UI resource model (`_meta.ui.resourceUri`).
- Sandbox and JSON-RPC/postMessage communication.
- Host assumptions and framework constraints.

### Agent 3 — Cross-Platform Architect
**Task:** Synthesize OpenAI and MCP Apps into a host-agnostic GEOX architecture.
**Design:**
- Canonical app manifest and tool schemas.
- Canonical event bus and adapter interfaces.
- Fallback strategy for non-interactive hosts.

### Agent 4 — GEOX Product Definer
**Task:** Define the first GEOX MCP Apps (Seismic Viewer, Basin Explorer, etc.).
**Focus:**
- User problems and required MCP tools.
- UI surfaces and state models.
- External web fallback behavior.

### Agent 5 — Delivery Planner
**Task:** Convert architecture into execution steps.
**Focus:**
- Repo structure and package boundaries.
- Cloud deployment and observability (Audit/Vault).
- Acceptance criteria for host portability.

---

## 📜 Canonical App Contract

| Key | Description |
|---|---|
| `app_id` | Unique GEOX identifier (e.g., `geox.seismic-viewer`) |
| `domain` | Subsurface domain (Seismic, Well, Map) |
| `tools[]` | List of required/optional MCP tools |
| `ui_entry` | Path to the portable UI resource (e.g., `/geox-gui/index.html`) |
| `event_protocol` | Version of the GEOX Event Bus (JSON-RPC) |
| `fallback_mode` | Behavior if host is "tool-only" (e.g., `deep_link_to_web`) |

### Canonical Event Bus (JSON-RPC)
- `app.initialize`: Handshake between host and GEOX app.
- `app.context.patch`: Sync geological context (basin, well_id, coordinates).
- `tool.request / tool.result`: Bridge for MCP tool execution.
- `ui.action`: User interaction event.
- `telemetry.emit`: Constitutional audit logging.

---

## 🚦 Host Adapter Matrix

| Host | Capability Plane | UI Runtime | Adapter Responsibility |
|---|---|---|---|
| **ChatGPT** | OpenAI Apps SDK | Widget/Webview | Map GEOX tools to OpenAI Tool Schema. |
| **Claude** | MCP Apps | Sandboxed Iframe | Map `ui_entry` to `_meta.ui.resourceUri`. |
| **Copilot** | MCP Tools | Native/Webview | Handle context injection via system prompts. |
| **GEOX Web** | Custom FastMCP | Full Browser | Direct host of the GEOX UI runtime. |

---

## 📝 Fallback Decision Tree

1. **Host supports Inline Apps?** 
   - YES => Render native `ui_entry`.
2. **Host supports MCP Tools?** 
   - YES => Execute tool + Return signed link to GEOX Web App.
3. **Host is text-only?**
   - YES => Standard LLM interaction with governance text badges.

---

*Sealed by: 888_JUDGE | 2026.04.09*
*DITEMPA BUKAN DIBERI*
