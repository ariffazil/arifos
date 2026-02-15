# arifOS Governance Integration for MCP

## State Variables
- **Roles**: Host, Client, Server, Sovereign (human 888 Judge).
- **Capabilities**: Tools, Resources, Prompts, Sampling, Roots, Elicitation.
- **Schemas**: JSON Schema registry, versioning, validation, migration.
- **Auth primitives**: tokens, OAuth2 resource servers, scopes, credential management.

## The 9 Hardened Skills

arifOS MCP implements a **9-stage governance pipeline**, where each tool represents a hardened skill enforcing specific constitutional floors.

| Tool | Stage | Description | Primary Floors |
|------|-------|-------------|----------------|
| **anchor** | 000 | Init & Sense — Establish authority, classify query, verify identity | F11, F12 |
| **reason** | 222 | Think & Hypothesize — Generate hypotheses, analyze risk and truth | F2, F4, F8 |
| **integrate** | 333 | Map & Ground — Integrate context, evidence, and external knowledge | F7, F10 |
| **respond** | 444 | Draft & Plan — Create draft response with clarity and resilience | F4, F6 |
| **validate** | 555 | Check Impact — Stakeholder safety and reversibility check | F5, F6, F1 |
| **align** | 666 | Check Ethics — Ethics verification and Anti-Hantu check | F9 |
| **forge** | 777 | Synthesize Solution — Build actionable artifacts with truth and clarity | F2, F4, F7 |
| **audit** | 888 | Verify & Judge — Final verdict, consensus, and human oversight | F3, F11, F13 |
| **seal** | 999 | Commit to Vault — Cryptographic seal, permanence, and trust | F1, F3 |

## Allowable Transitions

### tools/call
- **anchor (000)** → Must verify actor identity (F11) and pass injection guard (F12)
- **reason (222)** → Generates grounded hypotheses with truth scores
- **integrate (333)** → Maps context with humility (Ω₀ tracking)
- **respond (444)** → Drafts plans with clarity constraints
- **validate (555)** → Checks stakeholder impact before proceeding
- **align (666)** → Ethics gate; blocks on F9 violations
- **forge (777)** → Synthesizes only after validation and alignment
- **audit (888)** → Sovereign checkpoint; supports 888_HOLD for human review
- **seal (999)** → Final irreversible commit; requires SEAL verdict

### Transition Rules
- Changes world-state within defined boundaries
- Must be reversible or have rollback procedures (F1)
- Must be auditable (F3)
- Must respect sovereignty constraints (888 Judge override)
- Sequential progression through stages recommended but not strictly enforced
- Any stage may emit 888_HOLD to trigger human review

### resources/read
- `constitutional://floors/{floor_id}` — Returns floor specifications
- Flows context to the host
- Must respect access controls
- Must document data provenance
- Must support data minimization

### prompts/get
- Retrieves workflow templates for the 9-stage pipeline
- Must include safety constraints for each tool
- Must document parameter requirements
- Must support versioning

### sampling/initiate
- Starts server-initiated LLM calls
- Must respect LLM parameters
- Must include safety constraints
- Must support cancellation

## Invariants

### Model Agnosticism
- No model-specific assumptions in tool semantics
- All 9 tools work with any compliant LLM
- No vendor lock-in mechanisms
- Clear migration paths between models

### Schema Compliance
- All tool I/O must be JSON-Schema-typed
- Schemas must be versioned and documented (v64.2-GAGI)
- Backward compatibility must be maintained
- Schema changes must follow governance process

### Auditability
- All side-effects must be auditable
- Logs must be immutable and tamper-evident
- Audit trails must be complete and verifiable
- Audit access must be controlled

### Reversibility
- All actions must be reversible (F1 Amanah)
- Rollback procedures must be documented
- Irreversible actions require human approval
- Backup and recovery must be tested

### Sovereignty
- Human must have final decision authority (888 Judge)
- Sovereign override must be available at audit stage
- Decision rationale must be documented
- Appeal processes must be defined

## Governance Mappings

### F1 Amanah (Reversibility)
- All actions are reversible until seal (999)
- Rollback procedures documented per tool
- Backup and recovery tested
- Irreversible actions require human approval

### F2 Truth (Grounding)
- Protocol details from official specifications
- Capability types from ecosystem standards
- reason (222) and forge (777) enforce truth constraints
- Documentation is accurate and complete

### F7 Humility (Uncertainty)
- Ω₀ tracking implemented in integrate (333)
- Confidence levels exposed in all hypothesis generation
- Unknown states declared explicitly
- Estimates marked appropriately

### F9 Anti-Hantu (Authenticity)
- align (666) explicitly checks for consciousness claims
- System described as tool, never as agent with self-interest
- No anthropomorphic language in outputs
- Focus on protocol surfaces

### F11 Authority (Identity)
- anchor (000) enforces actor identity verification
- No default "user" bypass allowed
- Authentication tokens validated at entry
- Permission checks at each stage

### F12 Integrity (Security)
- InjectionGuard with threat scoring in anchor (000)
- Query classification for adaptive governance
- Critical injection risk (≥0.8) triggers VOID
- Security boundaries enforced per tool

### F13 Decay (Temporal Validity)
- audit (888) considers temporal context
- Session timeouts enforced
- Evidence timestamps validated
- Recency requirements for sensitive operations
