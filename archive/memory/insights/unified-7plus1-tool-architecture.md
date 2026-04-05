# Insight: Unified 7+1 Tool Architecture

**Source**: 2026-03-10 session  
**Pattern Type**: Technical/Architectural

## Decision

Unified all constitutional tools into single `arifOS_kernel` entrypoint with internal pipeline stages (000-999), replacing previous 13 separate tools.

## Architecture

**Two-layer identity system:**

| Layer | Purpose | Schema |
|-------|---------|--------|
| auth_context | Human authority | actor_id, authority_level, continuity |
| caller_context | AI execution identity | agent_type whitelist (architect/engineer/auditor/validator) |

## Implementation

- auth_context: auto-populated server-side from actor_id
- caller_context: v2 iteration (separate from auth_context fix)
- Lower entropy path: auth_context first, caller_context second

## Status

- Auth fix deployed and documented
- caller_context v2 pending implementation

---
*Extracted: 2026-03-23 hygiene cycle*
