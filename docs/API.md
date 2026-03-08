# REST API Reference

The arifOS MCP server exposes HTTP REST endpoints alongside the MCP protocol.

## Base URL

```
http://localhost:8080
```

## Endpoints

### `GET /health`

Health check with governance metrics.

**Response:**
```json
{
  "status": "alive",
  "version": "2026.03.08",
  "floors": {"F1": "PASS", "F2": "PASS", ...},
  "uptime_s": 42
}
```

---

### `GET /version`

Build information.

**Response:**
```json
{
  "version": "2026.03.08",
  "git_sha": "abc123",
  "build_time": "2026-03-08T00:00:00Z"
}
```

---

### `GET /tools`

List all 13 canonical tools.

**Response:**
```json
{
  "tools": [
    {"name": "anchor_session", "stage": "000", "description": "..."},
    ...
  ],
  "count": 13
}
```

---

### `POST /tools/{tool_name}`

Call a tool via REST.

**Request:**
```json
{
  "session_id": "...",
  "task": "..."
}
```

**Response:** Tool result envelope with `verdict`, `stage`, `floors`.

---

### `GET /api/governance-status`

Current governance telemetry.

---

### `GET /api/governance-history`

VAULT999 audit history.

---

### `POST /checkpoint`

Constitutional validation endpoint (ChatGPT Deep Research integration).

---

### `GET /.well-known/mcp/server.json`

MCP server discovery metadata.

---

### `GET /openapi.json`

OpenAPI schema.

---

### `GET /openapi.yaml`

OpenAPI schema in YAML format.
