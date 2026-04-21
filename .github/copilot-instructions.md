# arifOS Copilot Instructions

## Repository focus
- This repository is the canonical source for `arifosmcp`.
- Primary package: `arifosmcp/`.
- Canonical governance context lives in `AGENTS.md`.

## Runtime and tooling
- Python requirement: `>=3.12`.
- Install dev dependencies with: `pip install -e ".[dev]"`.
- Run tests with: `pytest tests/ -v`.
- Prefer repo-local commands and existing tooling over ad hoc scripts.

## Coding conventions
- Keep changes surgical and safety-first.
- Prefer explicit, honest naming and transparent behavior.
- Reuse existing helpers and patterns before adding new abstractions.
- Avoid hidden side effects and broad exception handling.

## Project-specific guidance
- Confirm current MCP tool surfaces against checked-in registry/config files before editing.
- For transport/runtime work, check `arifosmcp/`, `server.py`, `run.py`, `mcp.json`, and `mcp_servers.json`.
- Preserve constitutional/governance behavior described in `AGENTS.md`.

## Validation
- Run only the relevant existing tests, linters, or checks for the files you change.
