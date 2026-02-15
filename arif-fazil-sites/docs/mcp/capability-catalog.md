# arifOS MCP Capability Catalog

This catalog lists all MCP capabilities exposed by the arifOS server. All tools are model-agnostic and JSON-Schema-typed.

## Tools

### anchor (000)
| Property | Value |
|----------|-------|
| Name | anchor |
| Description | Init & Sense — Establish authority and context (F11/F12) |
| Schema | [anchor.schema.json](schemas/anchor.schema.json) |
| Auth Scope | session:init |
| Safety Constraints | F12 Injection Guard |
| Version | 1.0 |
| Specification | [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) |

### reason (222)
| Property | Value |
|----------|-------|
| Name | reason |
| Description | Think & Hypothesize — Generate hypotheses and analyze (F2/F4/F8) |
| Schema | [reason.schema.json](schemas/reason.schema.json) |
| Auth Scope | cognition:reason |
| Safety Constraints | None |
| Version | 1.0 |
| Specification | [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) |

### integrate (333)
| Property | Value |
|----------|-------|
| Name | integrate |
| Description | Map & Ground — Integrate context and external knowledge (F7/F10) |
| Schema | [integrate.schema.json](schemas/integrate.schema.json) |
| Auth Scope | context:integrate |
| Safety Constraints | None |
| Version | 1.0 |
| Specification | [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) |

### respond (444)
| Property | Value |
|----------|-------|
| Name | respond |
| Description | Draft & Plan — Create draft response/plan (F4/F6) |
| Schema | [respond.schema.json](schemas/respond.schema.json) |
| Auth Scope | response:draft |
| Safety Constraints | None |
| Version | 1.0 |
| Specification | [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) |

### validate (555)
| Property | Value |
|----------|-------|
| Name | validate |
| Description | Check Impact — Stakeholder impact and safety validation (F5/F6/F1) |
| Schema | [validate.schema.json](schemas/validate.schema.json) |
| Auth Scope | empathy:validate |
| Safety Constraints | None |
| Version | 1.0 |
| Specification | [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) |

### align (666)
| Property | Value |
|----------|-------|
| Name | align |
| Description | Check Ethics — Ethics and Anti-Hantu verification (F9) |
| Schema | [align.schema.json](schemas/align.schema.json) |
| Auth Scope | ethics:align |
| Safety Constraints | F9 Anti-Hantu enforcement |
| Version | 1.0 |
| Specification | [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) |

### forge (777)
| Property | Value |
|----------|-------|
| Name | forge |
| Description | Synthesize Solution — Crystalize plan into actionable artifact (F2/F4/F7) |
| Schema | [forge.schema.json](schemas/forge.schema.json) |
| Auth Scope | synthesis:forge |
| Safety Constraints | None |
| Version | 1.0 |
| Specification | [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) |

### audit (888)
| Property | Value |
|----------|-------|
| Name | audit |
| Description | Verify & Judge — Final judgment and consensus (F3/F11/F13) |
| Schema | [audit.schema.json](schemas/audit.schema.json) |
| Auth Scope | governance:audit |
| Safety Constraints | None |
| Version | 1.0 |
| Specification | [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) |

### seal (999)
| Property | Value |
|----------|-------|
| Name | seal |
| Description | Commit to Vault — Cryptographic seal with integrity (F1/F3) |
| Schema | [seal.schema.json](schemas/seal.schema.json) |
| Auth Scope | vault:seal |
| Safety Constraints | None |
| Version | 1.0 |
| Specification | [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) |

## Resources

### VAULT999
| Property | Value |
|----------|-------|
| URI | vault://arifos/sealed_events |
| MIME Type | application/json |
| Access | Read/Write |
| Version | 1.0 |
| Description | Immutable ledger of sealed decisions |
| Specification | [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) |

## Prompts

### trinity_analysis
| Property | Value |
|----------|-------|
| Name | trinity_analysis |
| Description | Comprehensive analysis using ΔΩΨ framework |
| Parameters | query, context |
| Safety Constraints | None |
| Version | 1.0 |
| Specification | [MCP 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) |

## Governance

### Invariants
- All tools are model-agnostic
- All I/O uses JSON Schema
- All side-effects are auditable
- All actions are reversible
- Human sovereignty is preserved

### Tool-to-Floor Mapping

| Tool | Stage | Floors Enforced |
|------|-------|-----------------|
| anchor | 000 | F11 (Command Auth), F12 (Injection) |
| reason | 222 | F2 (Truth), F4 (Clarity), F8 (Genius) |
| integrate | 333 | F7 (Humility), F10 (Ontology) |
| respond | 444 | F4 (Clarity), F6 (Empathy) |
| validate | 555 | F5 (Peace²), F6 (Empathy), F1 (Amanah) |
| align | 666 | F9 (Anti-Hantu) |
| forge | 777 | F2 (Truth), F4 (Clarity), F7 (Humility) |
| audit | 888 | F3 (Tri-Witness), F11 (Command Auth), F13 (Sovereign) |
| seal | 999 | F1 (Amanah), F3 (Tri-Witness) |

### Versioning
- Semantic versioning (MAJOR.MINOR.PATCH)
- MAJOR for breaking changes
- MINOR for backward-compatible additions
- PATCH for backward-compatible fixes

### Change Process
1. Propose change in GitHub issue
2. Discuss with stakeholders
3. Implement with tests
4. Document changes
5. Update version
6. Notify users

### References
- [MCP 2025-11-25 Specification](https://modelcontextprotocol.io/specification/2025-11-25)
- [MCP Architecture Overview](https://modelcontextprotocol.io/docs/learn/architecture)
- [MCP Tools Specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
