# arifOS ChatGPT Integration Configuration

## Current Server Status
- **Live Production Server**: https://aaamcp.arif-fazil.com
- **Health Check**: https://aaamcp.arif-fazil.com/health
- **Current Version**: v55.4-SEAL
- **Tools Available**: 9 canonical tools (init_gate, agi_sense, agi_think, agi_reason, asi_empathize, asi_align, apex_verdict, reality_search, vault_seal)

## ChatGPT Integration Options

### Option 1: Remote MCP Connector (Recommended)
Use the live production server with ChatGPT Developer Mode / remote MCP:

**Endpoint**: `https://aaamcp.arif-fazil.com/mcp`

**Configuration for ChatGPT**:
1. Open ChatGPT Developer Mode / connector setup.
2. Add the remote MCP server URL:
   - **URL**: `https://aaamcp.arif-fazil.com/mcp`
3. Do not point ChatGPT at `python -m arifosmcp.transport rest` or the root base URL.
4. In deployment, set:
   - `ARIFOS_GOVERNANCE_SECRET` to the same stable value on every worker/replica
   - `ARIFOS_PUBLIC_TOOL_PROFILE=chatgpt` to expose the orchestrator-first MCP surface

### Option 2: REST/OpenAPI Compatibility Surface
Use this only when you intentionally need the simplified checkpoint REST API:

**Endpoint**: `https://aaamcp.arif-fazil.com/checkpoint`

This surface is for OpenAPI/action-style compatibility and is not the MCP transport.

### Option 3: OpenAI API Integration
For developers using the OpenAI API directly:

```python
import openai
from arifos import ConstitutionalAgent

# Configure the agent
agent = ConstitutionalAgent(
    mcp_server="https://aaamcp.arif-fazil.com",
    floors="all"  # Enforce all 9 constitutional floors
)

# Use in your application
response = agent.process("Your query here")
print(response.verdict)  # SEAL, VOID, SABAR, or 888_HOLD
```

### Option 4: MCP Protocol Integration
For Claude, Cursor, or other MCP-compatible editors:

**Add to your .mcp.json or editor configuration**:
```json
{
    "mcpServers": {
      "arifos": {
      "url": "https://aaamcp.arif-fazil.com/mcp"
      }
    }
  }
```

## Available Tools (9 Canonical Tools)

1. **init_gate** - Session initialization and injection defense (F11, F12)
2. **agi_sense** - Input parsing and intent detection (F2, F4) 
3. **agi_think** - Hypothesis generation (F2, F4, F7)
4. **agi_reason** - Deep logical reasoning (F2, F4, F7)
5. **asi_empathize** - Stakeholder impact assessment (F5, F6)
6. **asi_align** - Constitutional alignment check (F5, F6, F9)
7. **apex_verdict** - Final constitutional judgment (F3, F8)
8. **reality_search** - External fact-checking (F2, F7)
9. **vault_seal** - Immutable audit logging (F1, F3)

## OpenAPI Schema Structure
The REST compatibility surface provides an OpenAPI 3.1.0 specification for `/checkpoint`. Remote MCP clients should use `/mcp` instead of the OpenAPI schema.

## Testing Your Integration
```bash
# Health check
curl https://aaamcp.arif-fazil.com/health

# Test MCP endpoint reachability
curl -i https://aaamcp.arif-fazil.com/mcp

# Test checkpoint REST compatibility endpoint
curl -X POST https://aaamcp.arif-fazil.com/checkpoint \
  -H "Content-Type: application/json" \
  -d '{"query":"Test query"}'
```

## Production Endpoints
- **Health**: https://aaamcp.arif-fazil.com/health
- **MCP**: https://aaamcp.arif-fazil.com/mcp
- **SSE**: https://aaamcp.arif-fazil.com/sse (only if intentionally deployed)
- **Checkpoint REST**: https://aaamcp.arif-fazil.com/checkpoint
- **Dashboard**: https://aaamcp.arif-fazil.com/dashboard
- **Docs**: https://aaamcp.arif-fazil.com/docs

## Constitutional Enforcement
Every tool enforces specific constitutional floors:
- **F1 Amanah**: Reversibility and audit trails
- **F2 Truth**: Verifiable claims only
- **F3 Tri-Witness**: Consensus requirements
- **F5 Peace²**: Stability requirements
- **F7 Ω₀**: Humility (3-5% uncertainty)
- **F9 Anti-Hantu**: No consciousness claims

The server returns verdicts: SEAL (approved), VOID (blocked), SABAR (caution), or 888_HOLD (human review).
