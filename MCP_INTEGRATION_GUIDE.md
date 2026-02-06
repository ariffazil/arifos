# MCP (Model Context Protocol) Integration Guide

## Overview
Model Context Protocol (MCP) is an open standard by Anthropic that enables AI assistants to connect to external tools and data sources. arifOS provides a Model Context Protocol (MCP) server called "AAA MCP" that exposes 9 constitutional tools for AI governance.

## Supported Platforms

### 1. Claude Desktop / Claude Code
**Integration Method:** stdio transport
**Configuration:** Add to `.mcp.json` in project root
```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"]
    }
  }
}
```

### 2. ChatGPT (Developer Mode)
**Integration Method:** HTTP transport
**Configuration:** Point to HTTP endpoint
```bash
# Start HTTP server
python -m aaa_mcp http
# MCP endpoint: http://localhost:8000/mcp
```

### 3. Cursor IDE
**Integration Method:** stdio transport
**Configuration:** Add to `.cursor/mcp.json`
```json
{
  "mcpServers": {
    "aaa-mcp": {
      "command": "python",
      "args": ["-m", "aaa_mcp", "stdio"]
    }
  }
}
```

### 4. Qwen Models
**Integration Method:** HTTP or SSE transport
**Configuration:** Through MCP-compatible interface
```bash
# Start SSE server for cloud deployment
python -m aaa_mcp sse
# Endpoint: http://localhost:8080/sse
```

### 5. OpenAI Assistant API
**Integration Method:** HTTP transport
**Configuration:** As external tool
```bash
# Start HTTP server
python -m aaa_mcp http
# Register at: http://localhost:8000/mcp
```

### 6. Microsoft Copilot
**Integration Method:** HTTP transport
**Configuration:** Custom tool integration
```bash
# Deploy HTTP server
python -m aaa_mcp http
# MCP endpoint: http://your-domain.com/mcp
```

### 7. Google Gemini
**Integration Method:** HTTP transport
**Configuration:** External function calling
```bash
# Start HTTP server
python -m aaa_mcp http
# Endpoint: http://localhost:8080/mcp
```

## Transport Protocols

### stdio (Standard Input/Output)
- **Best for:** Local development, desktop applications
- **Usage:** `python -m aaa_mcp stdio`
- **Platforms:** Claude Code, Claude Desktop, Cursor IDE
- **Security:** Local-only, no network exposure

### SSE (Server-Sent Events)
- **Best for:** Cloud deployment, remote access
- **Usage:** `python -m aaa_mcp sse`
- **Platforms:** Railway, Fly.io, AWS, GCP, Azure
- **Endpoint:** `http://your-domain.com/sse`
- **Security:** Supports HTTPS, authentication

### HTTP (Streamable HTTP)
- **Best for:** REST-style integration, web applications
- **Usage:** `python -m aaa_mcp http`
- **Platforms:** ChatGPT, OpenAI, web apps
- **Endpoint:** `http://your-domain.com/mcp`
- **Security:** Standard HTTP(S) security

## Deployment Options

### Local Development
```bash
# Install arifOS
pip install arifos

# Start stdio server (for Claude/Cursor)
python -m aaa_mcp stdio

# Start HTTP server (for web integration)
python -m aaa_mcp http

# Start SSE server (for cloud testing)
python -m aaa_mcp sse
```

### Cloud Deployment (Railway)
```bash
# railway.toml
[build]
builder = "heroku/buildpacks:20"

[run]
command = "python -m aaa_mcp sse"
port = 8080

# Health check endpoint
[http]
  check_interval = 10
  timeout = 2
  grace_period = 30
  restart_limit = 3
```

### Docker Deployment
```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY . .
RUN pip install arifos

EXPOSE 8080
CMD ["python", "-m", "aaa_mcp", "sse"]
```

## System Architecture

### 9 Constitutional Tools
1. `init_gate` - Session initialization and sovereignty verification
2. `agi_sense` - Information gathering with truth verification
3. `agi_think` - Cognitive processing with humility tracking
4. `agi_reason` - Logical analysis with evidence grounding
5. `asi_empathize` - Stakeholder impact assessment
6. `asi_align` - Value alignment with anti-hantu guard
7. `apex_verdict` - Final judgment with tri-witness consensus
8. `reality_search` - External verification and fact-checking
9. `vault_seal` - Immutable recording and audit trail

### Integration Flow
```
AI Query → MCP Protocol → AAA MCP Server → Constitutional Tools → Verified Response
```

## Configuration Parameters

### Environment Variables
- `ARIFOS_CONSTITUTIONAL_MODE`: Set to "AAA" for full constitutional enforcement
- `MCP_SERVER_PORT`: Port for HTTP/SSE servers (default: 8080)
- `MCP_TRANSPORT`: Transport type (stdio, http, sse)
- `ARIFOS_OMEGA_THRESHOLD`: Ω₀ threshold for uncertainty escalation (default: 0.05)

### Security Settings
- Authentication tokens for remote MCP access
- Rate limiting for tool usage
- Audit logging for compliance
- SSL/TLS encryption for network traffic

## Troubleshooting

### Common Issues
1. **Connection refused**: Check if MCP server is running
2. **Tools not appearing**: Verify MCP configuration file syntax
3. **Slow response**: Check network connectivity for remote servers
4. **Authentication errors**: Verify API keys and tokens

### Debug Commands
```bash
# Check server status
curl http://localhost:8080/health

# List available tools
curl http://localhost:8080/

# Test tool call
curl -X POST http://localhost:8080/mcp -H "Content-Type: application/json" -d '{"method":"tools.list"}'
```

## Best Practices

### For Development
- Use stdio transport for local testing
- Enable detailed logging during development
- Test with multiple AI platforms

### For Production
- Use SSE transport for cloud deployment
- Implement proper authentication
- Monitor constitutional compliance metrics
- Maintain audit logs for compliance

### Performance
- Cache frequently used tools
- Optimize response times for real-time applications
- Scale horizontally for high-throughput scenarios