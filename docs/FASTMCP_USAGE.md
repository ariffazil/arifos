# FastMCP Usage Guide

## Installation

```bash
# From PyPI
pip install arifos

# From source
git clone https://github.com/ariffazil/arifosmcp.git
cd arifosmcp
pip install -e .
```

## Running the Server

### stdio (Local MCP Clients)

```bash
# Direct
python -m arifos_aaa_mcp stdio

# Via FastMCP
fastmcp run
```

### HTTP (Production)

```bash
python -m arifos_aaa_mcp http
```

### SSE (Web Clients)

```bash
python -m arifos_aaa_mcp sse
```

## FastMCP Configuration

The `fastmcp.json` at the repository root points to `core/server.py`:

```json
{
  "source": {
    "type": "filesystem",
    "path": "core/server.py",
    "entrypoint": "mcp"
  }
}
```

## MCP Client Setup

### Claude Desktop

```json
{
  "mcpServers": {
    "arifos": {
      "command": "python",
      "args": ["-m", "arifos_aaa_mcp", "stdio"]
    }
  }
}
```

### Via FastMCP

```json
{
  "mcpServers": {
    "arifos": {
      "command": "fastmcp",
      "args": ["run", "/path/to/arifosmcp/fastmcp.json"]
    }
  }
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | `0.0.0.0` | Server bind address |
| `PORT` | `8080` | Server port |
| `AAA_MCP_TRANSPORT` | `sse` | Transport: stdio, http, sse |
| `ARIFOS_GOVERNANCE_SECRET` | — | HMAC secret for governance tokens |
| `ARIFOS_PHYSICS_DISABLED` | `0` | Disable P3 thermodynamics (test only!) |
| `REDIS_URL` | — | Redis for session persistence |

## Docker

```bash
docker build -t arifos-mcp .
docker run -p 8080:8080 arifos-mcp
curl http://localhost:8080/health
```
