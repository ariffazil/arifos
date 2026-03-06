---
name: mcp-builder
description: Build MCP servers with arifOS governance and mandatory Inspector validation.
---

# MCP Builder (arifOS)

Use this skill when creating or upgrading MCP servers.

## Governance First

Before implementation:

1. Anchor session and state assumptions.
2. Map tools to read-only vs destructive behavior.
3. Mark irreversible operations as `888_HOLD`.

## Preferred Defaults

- Language: TypeScript first, Python second.
- Transport: `stdio` for local development, HTTP for remote runtime.
- Design: comprehensive API coverage first, add workflow tools second.

## Tool Design Rules

- Use clear, discoverable tool names with stable prefixes.
- Define strict input schemas and constraints.
- Return focused data with pagination/filter support.
- Emit actionable errors with next-step guidance.
- Add annotations: `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`.

## arifOS Wrapper Pattern

All destructive tool calls must pass constitutional checks before execution.

## Phase Workflow

### Phase 1: Research

- Read protocol/spec pages needed for the target MCP server.
- Read target API docs and auth model.
- Produce endpoint map: required, optional, destructive.

### Phase 2: Implementation

- Scaffold server structure.
- Build shared API client, auth, pagination, and error helpers.
- Implement tools in priority order.

### Phase 2.5: Inspector (Mandatory)

Run MCP Inspector before seal:

```bash
npx @modelcontextprotocol/inspector node dist/index.js
```

Validate:

- Connection/capabilities handshake
- Tools listed and callable
- Read-only tools execute cleanly
- Destructive tools produce `888_HOLD` path
- Errors are actionable and schema-aligned

### Phase 3: Audit

- Run build/lint/type checks.
- Verify no duplicate tool behavior.
- Verify transport behavior for stdio/http.

### Phase 4: Evaluation

- Create 10 read-only, realistic, verifiable evaluation questions.
- Ensure questions need multi-step exploration.

## Definition of Done

- Build passes.
- Inspector passes.
- Destructive operations are gated.
- Docs include setup, env vars, and run commands.

## Do Not

- Do not bypass governance gates for destructive actions.
- Do not expose private servers publicly by default.
- Do not hardcode tokens or secrets.
