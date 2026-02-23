---
id: intro
title: Introduction
slug: /intro
sidebar_position: 1
description: arifOS is a constitutional intelligence kernel with canonical AAA MCP 13-tool surface and governed 000->999 pipeline.
---

# arifOS - Forged, Not Given

arifOS is a constitutional intelligence kernel that governs AI cognition through 13 floors and a staged pipeline ending in auditable verdicts.

## Canonical runtime

- Python: `>=3.12`
- Module: `arifos_aaa_mcp`
- Transports: `stdio`, `sse`, `http`
- MCP surface: 13 tools, 2 resources, 1 prompt

## Quick start

```bash
pip install arifos

# Local clients (Claude Desktop / Cursor)
python -m arifos_aaa_mcp stdio

# Remote SSE runtime
HOST=0.0.0.0 PORT=8080 python -m arifos_aaa_mcp sse

# HTTP MCP fallback
PORT=8089 python -m arifos_aaa_mcp http
```

Live endpoints:

- SSE: `https://arifosmcp.arif-fazil.com/sse`
- MCP HTTP: `https://arifosmcp.arif-fazil.com/mcp`
- Health: `https://arifosmcp.arif-fazil.com/health`

## Canonical tools (13)

1. `anchor_session`
2. `reason_mind`
3. `recall_memory`
4. `simulate_heart`
5. `critique_thought`
6. `judge_soul`
7. `forge_hand`
8. `seal_vault`
9. `search_reality`
10. `fetch_content`
11. `inspect_file`
12. `audit_rules`
13. `check_vital`

## Resources and prompt

- `arifos://aaa/schemas`
- `arifos://aaa/full-context-pack`
- `arifos.prompt.aaa_chain`

## Governance verdicts

- `SEAL` - approved
- `PARTIAL` - approved with warnings
- `SABAR` - hold/refine
- `VOID` - blocked
- `888_HOLD` - mandatory human ratification

Continue with:

- [MCP Server](./mcp-server)
- [API Reference](./api)
- [Governance](./governance)
- [Deployment](./deployment)
