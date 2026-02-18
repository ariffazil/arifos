# arifOS Architecture

**Version:** v65.0-AAA-MCP (2026-02-15)
**Status:** Production-ready for VPS deployment

## Core Components

### 1. AAA-MCP Server
- **Purpose:** Constitutional AI governance layer
- **Protocol:** Model Context Protocol (MCP)
- **Transport:** HTTP/REST with SSE support
- **Features:** F1-F13 floor enforcement, thermodynamic constraints

### 2. REST Bridge
- **Purpose:** OpenAI-compatible API adapter
- **Compatibility:** Works with standard OpenAI clients
- **Tools:** Exposes arifOS tools via REST endpoints

### 3. PostgreSQL Backend (VAULT999)
- **Purpose:** Constitutional ledger storage
- **Schema:** Decision logs, verdicts, entropy tracking
- **Port:** 5432 (local development)

### 4. Redis Cache (MindVault)
- **Purpose:** Session state and temporary memory
- **Use:** Tool execution context, short-term caching

## Deployment Architecture

```
┌─────────────────┐    HTTP/SSE    ┌─────────────────┐
│   AI Clients    │◄──────────────►│  AAA-MCP Server │
│ (OpenAI format) │                │   (Port: 8080)  │
└─────────────────┘                └─────────────────┘
                                            │
                                            ▼
                                 ┌─────────────────────┐
                                 │   PostgreSQL DB     │
                                 │   (VAULT999 Ledger) │
                                 └─────────────────────┘
```

## Security Model

- **F1 Amanah:** All actions reversible
- **F12 Containment:** Sandboxed tool execution
- **F13 Sovereignty:** Human oversight preserved

## Current Deployment
- **VPS:** srv1325122 (72.62.71.199)
- **Container:** arifos-mcp:vps
- **Port:** 8000 (localhost only)
- **Status:** ✅ Operational

---
*Auto-generated for Docker build compatibility*
