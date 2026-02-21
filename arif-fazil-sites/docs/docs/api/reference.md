# API Reference

The arifOS MCP server provides a RESTful API and standard MCP endpoints for constitutional AI governance.

## Version
**Current Kernel:** `2026.02.17-FORGE-UVX-SEAL`

## Base URLs
- **MCP (SSE/HTTP)**: `https://arifosmcp.arif-fazil.com/mcp`
- **REST API**: `https://arifosmcp.arif-fazil.com`

## Authentication (Testing Mode)
Currently, arifOS is in **Testing Mode**. No `auth_token` is required for registration or tool calls. Any AI platform can register using the MCP endpoint.

## Tool Registry (26 Tools)

### Constitutional Stages
- `anchor` (Stage 000)
- `reason` (Stage 222)
- `integrate` (Stage 333)
- `respond` (Stage 444)
- `validate` (Stage 555)
- `align` (Stage 666)
- `forge` (Stage 777)
- `audit` (Stage 888)
- `seal` (Stage 999)

### System & Containers
- `container_list` / `container_exec` / `container_logs`
- `system_health` / `net_status` / `fs_inspect`
- `trinity_forge` (Full Pipeline)

## REST Endpoints

### GET /health
Returns the current health status of the system.

### POST /tools/{tool_name}
Executes a specific tool via REST.

### POST /apex_judge
Unified wrapper for the full pipeline (000→999).
