# Lessons — What We Learned

## 2026-02-07: VAULT999 Schema Design

### Lesson: Trim Redundancy
- `floors_passed` can be computed from `floors_checked - floors_failed`
- External auditor suggested removal, but kept for query convenience
- Trade-off: Storage vs Query simplicity

### Lesson: JSONB Fallback
- New schema fields stored in `seal_data._v2_metadata`
- No migration required for backwards compatibility
- Can add columns later for performance

### Lesson: 9 Categories (APEX Compression)
- 22 fields map to 9 conceptual categories
- Identity, Integrity, Verdict, Context, Risk, Floors, Metrics, Oversight, Provenance
- Hybrid approach: Key columns + JSONB composites

---

## External Auditor Sources

| Source | Key Insight |
|--------|-------------|
| ISACA | Hash integrity for audit trails |
| Databricks | Human override tracking |
| MCP Audit Layer | Tool chain verification |
| Newline.co | Model version comparison |
| Scalevise | Environment separation |
| Swept AI | Actor accountability chain |

---

## Memory Architecture

### 4 Tiers Identified
1. **Working:** Context window (OpenClaw built-in)
2. **Decision:** VAULT999 (verdicts, floors, overrides)
3. **Semantic:** memory/*.md + future pgvector
4. **Adaptive:** Future — learn from patterns

### Key Insight
> "VAULT999 is decision memory, not content memory. It remembers verdicts, not knowledge."

---

*Last updated: 2026-02-07*
