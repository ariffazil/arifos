# Insight: API Reliability Pattern

**Source**: 2026-03-13, 2026-03-14 sessions  
**Pattern Type**: Operational/System

## Observation

Image analysis tool exhibits cascading failure across multiple providers:

| Provider | Error | Root Cause |
|----------|-------|------------|
| OpenAI | 401 | Incorrect/missing API key |
| Venice | 402 | Insufficient balance |
| Anthropic | 404 | Model/tool mismatch |
| Gemini | Unsupported | Integration constraint |

Parallel issue: MCP tool name divergence — documented `arifOS.kernel` does not exist; actual tools are `agentzero_engineer`, `agentzero_memory_query`, etc.

## Generalization

**Multi-provider single-point-of-failure**: Distributing across providers does not eliminate failure when all depend on:
- Valid credential state
- Provider account standing
- Integration maintenance

**Documentation drift risk**: Tool naming in docs vs runtime can diverge silently.

## Action

- Verify all API keys at gateway startup
- Single source of truth for tool manifest (runtime reflection > static docs)
- Provider-agnostic fallback chain with explicit degradation path

---
*Extracted: 2026-03-23 hygiene cycle*
