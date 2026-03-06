# 🗄️ Archived Tools (DO NOT USE IN PRODUCTION)

Archived on: 2026-03-06

These tools have been deprecated and merged into the canonical 13-tool surface.

## Archived Tools

| Tool | Reason | Replacement |
|------|--------|-------------|
| `fetch_content` | Merged into unified evidence ingestion tool | `ingest_evidence(source_type="url", target=..., mode="raw")` |
| `inspect_file` | Merged into unified evidence ingestion tool | `ingest_evidence(source_type="file", target=..., mode="raw")` |

## Migration Guide

### From `fetch_content`

**Before:**
```python
result = await fetch_content(id="https://example.com", max_chars=500)
```

**After:**
```python
result = await ingest_evidence(source_type="url", target="https://example.com", mode="raw", max_chars=500)
```

### From `inspect_file`

**Before:**
```python
result = await inspect_file(path="/path/to/dir", depth=1)
```

**After:**
```python
result = await ingest_evidence(source_type="file", target="/path/to/dir", depth=1)
```

## Implementation Reference

The archived implementations remain inside `aaa_mcp/server.py` as non-decorated
internal functions (`_fetch` and `_inspect_file`) for historical reference and can be
used as a reference during any rollback. They are **not** registered as MCP tools and
will **not** appear in `/tools/list`.

## ⚠️ DO NOT USE ARCHIVED TOOLS IN PRODUCTION ⚠️
