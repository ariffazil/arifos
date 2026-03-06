---
name: agi-integrate
description: 111-444_AGI + integrate verb — Context mapping, atlas navigation, and F10 ontology
---

# agi-integrate

## Scope
Organ 111-444_AGI (Mind/Δ) + Verb integrate — Context mapping, atlas construction, ontology verification (F2, F7, F8, F10).

## Constitutional Alignment
| Floor | Role | Threshold |
|-------|------|-----------|
| F2 | Truth | τ ≥ 0.99 |
| F7 | Humility | Ω₀ ∈ [0.03, 0.05] |
| F8 | Genius | G ≥ 0.80 |
| F10 | Ontology | BOOLEAN |

## Backend Path
- `aclip_cai/triad/delta/integrate.py`
- `core/organs/_1_mind.py`
- Memory: `aclip_cai/embeddings/bge_embedder.py`

## Operational Rules

**Trigger When:**
- Context boundaries need establishment
- File discovery and dependency mapping required
- Ontology validation needed (F10)
- Memory band assignment for context

**Allowed Operations:**
- Map context files and dependencies using **Hierarchical Tree Representation**
- Classify boundaries (INTERNAL, EXTERNAL, MISSING)
- Use **Atomic File Representation** with high-entropy delimiters for aggregation
- Verify symbols exist in vocabulary (F10)
- Calculate context uncertainty (F7)
- Query vector memory for semantic context

**888_HOLD Required:**
- Ontology bypass (F10 violation)
- Context map modification without audit
- External boundary reclassification

## Quick Reference
```python
# Context mapping
from aclip_cai.triad.delta import integrate
atlas = await integrate.build_atlas(parsed_intent, session_id)

# Vector memory recall
from aclip_cai.embeddings.bge_embedder import recall_context
context = await recall_context(query_vector, top_k=5)
```

## Verification
```bash
python -c "from aclip_cai.embeddings.bge_embedder import BGEEmbedder; print('Integrate: BGE ready')"
```
