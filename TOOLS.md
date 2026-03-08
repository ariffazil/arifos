# arifOS MCP Tools (Canonical 13)

This document describes the active canonical tool surface in this repository and the expected input/output contracts.

Source of truth used:
- `arifosmcp/transport/server.py` (registered tools)
- `arifosmcp/transport/protocol/schemas.py` (JSON schemas)
- `arifosmcp/transport/protocol/response.py` (response envelope)
- `spec/mcp-manifest.json` (published tool list)

## Common output envelope (expected)

Most tools return a normalized response envelope with these top-level fields:

```json
{
  "status": "OK | ERROR | BLOCKED | PENDING | ARTIFACT_READY",
  "session_id": "string",
  "stage": "000|111|222|333|444|555|666|777|888|999|ROUTER",
  "message": "string",
  "policy_verdict": "SEAL|PARTIAL|SABAR|VOID|888_HOLD",
  "next_tool": "string|null",
  "data": {},
  "_constitutional": {}
}
```

MCP-facing responses may also be wrapped as:

```json
{
  "content": [{ "type": "text", "text": "..." }],
  "structuredContent": {
    "tool": "stage_xxx",
    "stage": "...",
    "session_id": "...",
    "status": "...",
    "verdict": "...",
    "next_action": "...",
    "next_tool": "...",
    "data": {}
  }
}
```

## Canonical tools: input, output, functionality

## 1) `anchor_session`
- Functionality: Stage `000` session ignition, identity binding, authority/injection pre-check.
- Required input: `query: string`
- Common optional input: `actor_id`, `auth_token`, `session_id`, `mode`, `grounding_required`, `auth_context`
- Expected output: envelope + `data.mode`, `data.grounding_required`, governance boot details.

## 2) `reason_mind`
- Functionality: AGI reasoning path; truth/clarity-oriented inference on session context.
- Required input: `query: string`, `session_id: string`
- Common optional input: `grounding`, `capability_modules`, `actor_id`, `auth_token`, `risk_mode`
- Expected output: envelope + reasoning summary in `data` (truth/confidence metrics and rationale artifacts).

## 3) `vector_memory`
- Functionality: PHOENIX associative recall from vector memory.
- Required input: `query: string`, `session_id: string`
- Common optional input: `depth` (1-10), `domain` (`canon|manifesto|docs|all`), `debug`
- Expected output: memory recall object (memories/metrics) in `data`.

## 4) `simulate_heart`
- Functionality: ASI empathy simulation and stakeholder impact checks.
- Required input: `query: string`, `session_id: string`
- Common optional input: `stakeholders`, `actor_id`, `auth_token`, `risk_mode`
- Expected output: empathy/stakeholder assessment in `data` (kappa-r style signals).

## 5) `critique_thought`
- Functionality: Psi-Shadow style adversarial critique/alignment stress test of a plan.
- Required input: `session_id: string`, `plan: object`
- Common optional input: `actor_id`, `auth_token`, `auth_context`
- Expected output: critique findings and risk/alignment indicators in `data`.

## 6) `eureka_forge`
- Functionality: Governed actuation/sandboxed command execution.
- Required input: `session_id: string`, `command: string`
- Common optional input: `working_dir`, `timeout`, `confirm_dangerous`, `agent_id`, `purpose`, `approval_bundle`
- Expected output: forge execution status, instruction/message, and governance verdict in `data`.

## 7) `apex_judge`
- Functionality: Stage `888` sovereign verdict synthesis (quad-witness aware).
- Required input: `query: string`, `session_id: string`
- Common optional input: `proposed_verdict`, `human_approve`, `agi_result`, `asi_result`, `actor_id`, `auth_token`
- Expected output: verdict payload with witness block, truth score, and justification.

## 8) `seal_vault`
- Functionality: Immutable vault seal / ledger commit.
- Required input: `session_id: string`, `summary: string`, `governance_token: string`
- Common optional input: `verdict`, `approval_bundle`, `thermodynamic_statement`
- Expected output: seal result (`SEALED|PARTIAL`), seal id/hash, pipeline completion details.

## 9) `search_reality`
- Functionality: External grounding search across configured evidence providers.
- Required input: `query: string` (or grounding alias pair in legacy schema)
- Common optional input: `intent`, `session_id/session_token`, `region`, `timelimit`, `force_source`
- Expected output: evidence list + grounding metadata with verdict/stage context.

## 10) `ingest_evidence`
- Functionality: Unified evidence ingestion from URL or file sources.
- Required input: `source_type: "url"|"file"`, `target: string`
- Common optional input: `mode`, `max_chars`, `depth`, `pattern`, `max_files`, `include_hidden`
- Expected output: `{ target, status, content?, metadata?, error? }` + envelope context when routed.

## 11) `audit_rules`
- Functionality: Constitutional/system audit check.
- Required input: none
- Common optional input: `audit_scope`, `verify_floors`, `session_id`
- Expected output: audit summary/details and floor verification status.

## 12) `check_vital`
- Functionality: Runtime health/vital checks.
- Required input: `session_id: string` (tool implementation accepts health flags)
- Common optional input: `include_swap`, `include_io`, `include_temp`
- Expected output: health status summary (and optional subsystem telemetry).

## 13) `metabolic_loop`
- Functionality: Full orchestrated 000->999 pipeline execution.
- Required input: `query: string`
- Common optional input: `risktier`, `actor_id`, `proposed_verdict`
- Expected output: session verdict, next actions, trace/floor state, and governance token if produced.

## Practical calling notes
- Use canonical names above for new integrations.
- Backward-compat aliases still exist internally, but canonical names are the stable public surface.
- For strict integrations, validate payloads using `arifosmcp/transport/protocol/schemas.py` (`TOOL_INPUT_SCHEMAS` and `TOOL_OUTPUT_SCHEMAS`).
