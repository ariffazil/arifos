# arifOS MCP Quick Start

## Local (stdio)

```bash
pip install -e ".[dev]"
python -m arifosmcp.runtime stdio
```

Claude Desktop config snippet:

```json
{
  "mcpServers": {
    "arifOS": {
      "command": "python",
      "args": ["-m", "arifosmcp.runtime", "stdio"]
    }
  }
}
```

## Remote (SSE + HTTP fallback)

```bash
HOST=0.0.0.0 PORT=8080 python -m arifosmcp.runtime sse
PORT=8089 python -m arifosmcp.runtime http
```

Test endpoints:

```bash
curl -N --max-time 2 https://<your-domain>/sse
curl -X POST https://<your-domain>/mcp -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
curl https://<your-domain>/health
```

## Canonical Surface

- 13 tools
- resources: `arifos://aaa/schemas`, `arifos://aaa/full-context-pack`
- prompt: `arifos.prompt.aaa_chain`
