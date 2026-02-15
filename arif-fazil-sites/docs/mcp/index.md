# arifOS Universal MCP Profile

arifOS implements **9 Hardened Skills** through the Model Context Protocol (MCP), enforcing the 13 Constitutional Floors (F1–F13).

## The 9 Hardened Skills (v64.2-GAGI)

| Stage | Tool | Description | Floors |
|-------|------|-------------|--------|
| 000 | **anchor** | Init & Sense — Establish authority and context | F11, F12 |
| 222 | **reason** | Think & Hypothesize — Generate hypotheses and analyze | F2, F4, F8 |
| 333 | **integrate** | Map & Ground — Integrate context and external knowledge | F7, F10 |
| 444 | **respond** | Draft & Plan — Create draft response/plan | F4, F6 |
| 555 | **validate** | Check Impact — Stakeholder impact and safety check | F5, F6, F1 |
| 666 | **align** | Check Ethics — Ethics and Anti-Hantu verification | F9 |
| 777 | **forge** | Synthesize Solution — Crystalize plan into actionable artifact | F2, F4, F7 |
| 888 | **audit** | Verify & Judge — Final verdict and consensus | F3, F11, F13 |
| 999 | **seal** | Commit to Vault — Cryptographic seal and permanence | F1, F3 |

**Motto**: ⚓ *DITEMPA BUKAN DIBERI* — Forged, Not Given

## Protocol
- Standard method names and error codes (JSON-RPC 2.0).
- Consistent notification patterns for progress, cancellation, and state changes.
- Long-lived sessions with stateful context.
- All 9 tools follow strict input/output contracts defined in the server schema.

## Capabilities
- **Tools**: The 9 Hardened Skills (anchor through seal)
- **Resources**: Constitutional floor specifications (`constitutional://floors/{FX}`)
- **Prompts**: Workflow templates with safety constraints
- **Sampling**: Server-initiated LLM calls with cancellation support
- **Roots**: Context grounding and provenance tracking
- **Elicitation**: Dynamic capability negotiation

## Schema
- JSON Schema for all 9 tool interfaces
- Versioned schemas (current: v64.2-GAGI)
- Backward compatibility maintained
- Schema validation enforced at entry points

## Discovery
- `tools/list` endpoint returns all 9 hardened skills
- `resources/list` exposes constitutional floor specs
- Change notifications on capability updates
- Dynamic composition based on governance mode

## Non-functional
- **Authentication**: Actor identity verification (F11)
- **Injection Guard**: F12 protection with threat scoring
- **Logging**: Immutable, tamper-evident audit trails
- **Progress**: Cancellation and progress notifications
- **Error Reporting**: Structured error codes with floor violations

## Governance Integration
Each tool enforces specific constitutional floors:
- **F1 Amanah**: Reversibility and safe defaults
- **F2 Truth**: Grounded hypotheses and evidence
- **F3 Trust**: Verifiable audit trails
- **F4 Clarity**: Clear inputs and outputs
- **F5 Safety**: Stakeholder impact awareness
- **F6 Resilience**: Error handling and recovery
- **F7 Humility**: Uncertainty quantification (Ω₀)
- **F8 Transparency**: Observable reasoning
- **F9 Anti-Hantu**: No consciousness claims
- **F10 Memory**: Context preservation
- **F11 Authority**: Identity and permission checks
- **F12 Integrity**: Injection and attack resistance
- **F13 Decay**: Temporal validity awareness

## UI Binding (Optional)
- UI resource URIs for rendering
- CSP implementation for security
- UI-tool linking for workflow visualization
- Renderer support for skill-specific outputs

## References
- [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25)
- [MCP Architecture](https://modelcontextprotocol.io/docs/learn/architecture)
- arifOS Capability Catalog (updated for v64.2-GAGI)
