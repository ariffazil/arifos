# MCP Tool Schemas

This directory contains JSON Schema contracts for MCP tool outputs.
They are used at runtime by `codebase/mcp/core/validators.py` to enforce
output structure and required fields.

## Canonical Tools

- `init_gate.schema.json`
- `agi_sense.schema.json`
- `agi_think.schema.json`
- `agi_reason.schema.json`
- `asi_empathize.schema.json`
- `asi_align.schema.json`
- `apex_verdict.schema.json`
- `reality_search.schema.json`
- `vault_seal.schema.json`
- `_trinity_.schema.json`

## Notes

- Schemas are keyed by tool name.
- If a tool is added to `codebase/mcp/core/tool_registry.py`, add its
  corresponding schema here to keep output validation aligned.
