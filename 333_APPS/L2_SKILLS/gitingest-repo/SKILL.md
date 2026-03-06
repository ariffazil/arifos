---
name: gitingest-repo
description: Repository ingestion for AI analysis — convert GitHub repos to LLM-readable format
---

# GitIngest Repository Analysis

## Scope
Convert any Git repository into prompt-ready text digest for AI analysis.

## Constitutional Alignment
- **F2 Truth**: Accurate source representation
- **F4 Clarity**: Structured output format
- **F7 Humility**: Token estimation prevents overload

## Installation
```bash
# Already installed on VPS via pipx
pipx install gitingest
```

## Key Components
- CLI: `gitingest <repo-url> -o <output>`
- Python: `from gitingest import ingest`
- Output: summary + tree + content

## Operational Rules

**Trigger When:**
- Analyzing external repositories
- Code review of PRs
- Batch processing multiple repos
- Creating project documentation

**Allowed Operations:**
- Public repo ingestion
- Private repo ingestion (with GITHUB_TOKEN)
- Filtered ingestion (include/exclude patterns)
- Branch-specific analysis

**888_HOLD Required:**
- None (read-only operation)

## Quick Reference

### CLI Usage
```bash
# Basic ingestion
gitingest https://github.com/user/repo -o digest.txt

# Filter for specific files
gitingest https://github.com/user/repo -i "*.py" -i "*.md" -o -

# Exclude dependencies
gitingest https://github.com/user/repo -e "node_modules/*" -e "*.lock" -o -

# Private repo
export GITHUB_TOKEN="ghp_xxx"
gitingest https://github.com/user/private-repo -t $GITHUB_TOKEN -o -
```

### Python Usage
```python
from gitingest import ingest

summary, tree, content = ingest("https://github.com/user/repo")

# With filtering
summary, tree, content = ingest(
    "https://github.com/user/repo",
    include_patterns=["*.py", "*.js"],
    max_file_size=51200  # 50KB
)
```

## Verification
```bash
gitingest --version
python -c "from gitingest import ingest; print('GitIngest ready')"
```
