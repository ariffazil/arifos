# L5 Eureka Plan - AAA MCP Alignment

Date: 2026-02-27
Owner: arifOS node operator

## Why This Plan Exists

L5 is still pilot-level, while L4 tooling is production-level. The highest leverage is to wire L5 agent behavior to the real AAA MCP 13-tool contract without bypassing `core/` governance.

## Extracted Eureka Context (from 333_APPS)

1. Stack maturity is uneven by design
   - L0-L4 are production/hardened.
   - L5 is pilot and still has legacy wiring notes.

2. L5 social layer intends role separation
   - Architect (plan), Engineer (build), Auditor (truth), Validator (judge/seal).
   - This maps naturally to AAA MCP tool families.

3. L4 already exposes the constitutional contract
   - Canonical tool surface exists and is usable from OpenCode.
   - Alias compatibility exists (`apex_judge`/`apex_judge`, `eureka_forge`/`eureka_forge`).

4. L3 workflows already define sequence discipline
   - 000->999 lifecycle is specified and should be enforced in agents, not just docs.

## Improvement Plan

### Track A - OpenCode Config (Low risk, immediate)

1. Keep one canonical runtime path
   - Use `/root/arifOS` in all examples and commands.

2. Move toward least privilege
   - Reduce global `permission` breadth in `opencode.json`.
   - Grant elevated permissions per agent role.

3. Policy by role
   - `arif-architect`: full governance planning + AAA tool use.
   - `devops-builder`: build/test/edit, but AAA high-impact calls require explicit delegation.
   - `recon-researcher`: read/web only, no mutation.

### Track B - AAA MCP 13-Tool Contract (Medium risk)

1. Freeze canonical naming map in one place
   - Publish one table from `aaa_mcp/server.py` and keep aliases explicit.

2. Enforce lifecycle gate in wrappers
   - Require `anchor_session` receipt before mid/late-stage calls in L5 orchestration.
   - Require `seal_vault` at session close for high-impact runs.

3. Normalize tool schema strictness
   - Keep input contracts strict and explicit (example: `critique_thought` plan payload).
   - Add schema examples in docs to reduce operator entropy.

### Track C - Code Updates (Planned, test-backed)

1. L5 orchestration adapter
   - Add an adapter layer that maps L5 roles to AAA tools without importing transport logic into `core/`.

2. Contract tests for canonical flow
   - Tests for: `anchor -> reason -> simulate -> critique -> judge -> seal`.
   - Tests for alias compatibility and missing-field errors.

3. Docs/runtime parity checks
   - Add a CI check that compares documented tool names/count against `aaa_mcp/server.py` registrations.

## Proposed Execution Order

1. Harden config and role permissions.
2. Add contract tests for the 13-tool sequence.
3. Implement L5 orchestration adapter.
4. Sync docs and add parity checks.

## Non-Goals (for this phase)

- No destructive repo history edits.
- No production transport migration unless explicitly requested.
- No bypass of constitutional floors for speed.
