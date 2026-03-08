# arifOS MCP Ecosystem v55.5-EIGEN

> **Motto:** *DITEMPA BUKAN DIBERI* — Forged, Not Given

Complete Model Context Protocol (MCP) configuration for Kimi CLI, aligning 9 canonical constitutional tools with 6 external MCP servers.

---

## 🏛️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         arifOS MCP ECOSYSTEM                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  LAYER 1: CONSTITUTIONAL CORE (9 Canonical Tools)                           │
│  ─────────────────────────────────────────────────                          │
│                                                                             │
│   000_INIT        AGI (Mind)        ASI (Heart)       APEX (Soul)   999    │
│      │              │                   │                │           VAULT  │
│      ▼              ▼                   ▼                ▼                 │
│  ┌────────┐    ┌──────────┐        ┌──────────┐    ┌──────────┐   ┌──────┐ │
│  │init    │───►│agi_sense │───────►│asi_       │───►│apex      │──►│vault │ │
│  │_gate   │    │agi_think │        │empathize  │    │_verdict   │   │_seal │ │
│  │        │    │agi_reason│        │asi_align  │    │          │   │      │ │
│  └────────┘    └──────────┘        └──────────┘    └──────────┘   └──────┘ │
│                      │                      │                           │  │
│                      └──────────────────────┘                           │  │
│                               │                                         │  │
│                               ▼                                         │  │
│                        ┌────────────┐                                   │  │
│                        │reality_    │◄──────────────────────────────────┘  │
│                        │search      │ (Auxiliary - F2/F7)                  │
│                        └────────────┘                                      │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  LAYER 2: EXTERNAL EXECUTION (6 Reference MCPs)                             │
│  ──────────────────────────────────────────────                             │
│                                                                             │
│   ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌─────────┐ │
│   │filesystem │  │    git    │  │  memory   │  │sequential │  │  fetch  │ │
│   │  (F1)     │  │   (F2)    │  │   (F8)    │  │thinking   │  │  (F2)   │ │
│   └───────────┘  └───────────┘  └───────────┘  │   (F8)    │  └─────────┘ │
│                                                 └───────────┘              │
│   ┌───────────┐                                                            │
│   │   time    │                                                            │
│   │   (F6)    │                                                            │
│   └───────────┘                                                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 MCP Configuration

### File Locations

| Location | Purpose |
|----------|---------|
| `~/.kimi/mcp.json` | **User-level Kimi CLI config** (primary) |
| `C:\Users\User\arifOS\.mcp.json` | **Project-level config** (repo reference) |

### Quick Setup

```bash
# 1. Ensure Kimi CLI is installed
kimi --version

# 2. Install MCP servers
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-memory
npm install -g @modelcontextprotocol/server-sequential-thinking
npm install -g @modelcontextprotocol/server-fetch
npm install -g @modelcontextprotocol/server-time
uvx install mcp-server-git

# 3. Verify configuration
kimi mcp list
```

---

## 🎯 The 9 Canonical Tools (Constitutional Core)

| Tool | Trinity | Floors | Purpose |
|------|---------|--------|---------|
| `init_gate` | 000_INIT | F11, F12 | Session initialization, injection scan |
| `agi_sense` | AGI (Δ) | F2, F4 | Intent detection, query classification |
| `agi_think` | AGI (Δ) | F2, F4, F7 | Hypothesis generation with uncertainty |
| `agi_reason` | AGI (Δ) | F2, F4, F7 | Deep logical reasoning |
| `asi_empathize` | ASI (Ω) | F5, F6 | Stakeholder impact assessment |
| `asi_align` | ASI (Ω) | F5, F6, F9 | Ethics/law alignment, anti-hantu |
| `apex_verdict` | APEX (Ψ) | F3, F5, F8 | Final judgment (SEAL/VOID/PARTIAL) |
| `reality_search` | Auxiliary | F2, F7 | Web search with uncertainty tracking |
| `vault_seal` | 999_VAULT | F1, F3 | Immutable ledger recording |

---

## 🔌 The 6 External MCPs (Execution Layer)

### 1. **filesystem** — F1 AMANAH (Reversibility)
```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem@latest", "C:/Users/User/arifOS"]
}
```
**Tools:** `read_file`, `write_file`, `edit_file`, `list_directory`, `search_files`

**Constitutional Role:**
- F1 Amanah: All file operations are reversible (edit history preserved)
- F6 Clarity: Organized directory structure
- F11 Sovereignty: Configurable access controls

**Usage:**
```python
# Read constitutional spec
read_file(path: "spec/constitutional_floors.json")

# Edit with audit trail
edit_file(path: "arifosmcp.transport/server.py", edits: [...])
```

---

### 2. **git** — F2 TRUTH (Version Control as Evidence)
```json
{
  "command": "uvx",
  "args": ["mcp-server-git"],
  "cwd": "C:/Users/User/arifOS"
}
```
**Tools:** `git_status`, `git_diff`, `git_log`, `git_branch`, `git_commit`

**Constitutional Role:**
- F2 Truth: Commit history as immutable evidence
- F3 Tri-Witness: Git as consensus mechanism (Human × AI × System)
- F7 Humility: Track changes with uncertainty metadata

**Usage:**
```python
# Verify before changes
git_status()
git_diff()

# Branch for safe experimentation (F1)
git_create_branch(branch_name: "feature/f7-uncertainty-band")

# Commit with constitutional audit
git_commit(message: "F7: Calibrate Ω₀ to [0.03,0.05] band")
```

---

### 3. **memory** — F8 WISDOM (Pattern Storage)
```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-memory@latest"],
  "env": {
    "MEMORY_FILE_PATH": "C:/Users/User/arifOS/.kimi/memory.json"
  }
}
```
**Tools:** `read_graph`, `search_nodes`, `create_entities`, `create_relations`

**Constitutional Role:**
- F8 Wisdom: Pattern recognition across sessions
- F5 Peace²: Knowledge graph reduces entropy
- F3 Tri-Witness: Persistent facts as third witness

**Usage:**
```python
# Store architectural decision
create_entities(entities: [{
  "name": "reality_grounding",
  "entityType": "module",
  "observations": [
    "Uses thermodynamic cascade: DDGS → Playwright",
    "F7 Humility: Uncertainty Ω₀ tracked per result"
  ]
}])

# Query patterns
search_nodes(query: "constitutional enforcement")
```

---

### 4. **sequential-thinking** — F8 WISDOM (Multi-step Reasoning)
```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-sequential-thinking@latest"]
}
```
**Tools:** `sequentialthinking`

**Constitutional Role:**
- F8 Wisdom: Dynamic reflective problem-solving
- F7 Humility: State uncertainty at each thought step
- F2 Truth: Build conclusions from validated premises

**Usage:**
```python
# Complex constitutional analysis
sequentialthinking(
  thought: "Analyzing F3 Tri-Witness consensus...",
  thoughtNumber: 1,
  totalThoughts: 5,
  nextThoughtNeeded: true
)
```

---

### 5. **fetch** — F2 TRUTH (Web Content Retrieval)
```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-fetch@latest"]
}
```
**Tools:** `fetch`

**Constitutional Role:**
- F2 Truth: Content verification from web sources
- F7 Humility: Flag content age and reliability
- **Complements:** `reality_search` for deep content extraction

**Usage:**
```python
# Fetch and verify source
fetch(url: "https://example.com/article")

# Use with reality_search
reality_search(query: "AI regulation Malaysia 2026")
fetch(url: result[0].url)  # Extract full content
```

**Difference from `reality_search`:**
| Tool | Use Case | API Key |
|------|----------|---------|
| `reality_search` | Search + results list | ❌ No (DDGS) |
| `fetch` | Extract full page content | ❌ No |

---

### 6. **time** — F6 CLARITY (Temporal Precision)
```json
{
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-time@latest"]
}
```
**Tools:** `get_current_time`, `convert_time`

**Constitutional Role:**
- F6 Clarity: Precise temporal awareness
- F2 Truth: Timestamp evidence for audits
- VAULT999: Time-indexed ledger entries

**Usage:**
```python
# Timestamp constitutional session
get_current_time(timezone: "Asia/Singapore")

# Coordinate across timezones
convert_time(
  source_timezone: "America/New_York",
  time: "14:30",
  target_timezone: "Asia/Singapore"
)
```

---

## 🔗 Alignment Matrix: 9 Tools × 6 MCPs

| arifosmcp.transport Tool | Primary MCP | Constitutional Flow |
|--------------|-------------|---------------------|
| `init_gate` | `filesystem` | Read constitutional spec → Validate F11/F12 |
| `agi_sense` | `memory` | Query patterns → Classify intent |
| `agi_think` | `sequential-thinking` | Multi-step hypothesis generation |
| `agi_reason` | `git` | Verify against codebase history |
| `asi_empathize` | `memory` | Retrieve stakeholder patterns |
| `asi_align` | `filesystem` | Read ethics policy files |
| `apex_verdict` | `git` + `memory` | Cross-reference history + patterns |
| `reality_search` | `fetch` | Search → Fetch deep content |
| `vault_seal` | `filesystem` | Write to VAULT999 ledger |

---

## 🛡️ Constitutional Enforcement

### Pre-Execution (Input Validation)
```
init_gate ──► filesystem.read_file(spec/)
     │
     ▼
F11 (Auth) + F12 (Injection) ──► VOID if fail
```

### Execution (Reality Grounding)
```
agi_reason ──► reality_search ──► fetch
     │              │               │
     ▼              ▼               ▼
F2 (Truth)    F2/F7 (Ω₀)      F2 (Content)
```

### Post-Execution (Audit)
```
apex_verdict ──► vault_seal ──► git.commit
     │               │              │
     ▼               ▼              ▼
F3/F5/F8      F1/F3 (Ledger)   F2 (History)
```

---

## 📊 Thermodynamic Profile

| MCP | Entropy | Latency | Reliability | Use Frequency |
|-----|---------|---------|-------------|---------------|
| `filesystem` | 🟢 Low | ~10ms | 99.9% | Very High |
| `git` | 🟢 Low | ~50ms | 99.5% | High |
| `memory` | 🟢 Low | ~20ms | 99.0% | Medium |
| `sequential-thinking` | 🟡 Medium | Variable | 95.0% | Low |
| `fetch` | 🟡 Medium | ~1s | 90.0% | Medium |
| `time` | 🟢 Low | ~5ms | 99.9% | Low |

---

## 🚀 Usage Examples

### Example 1: Constitutional Code Review
```python
# 1. Initialize session
init_gate(query: "Review PR for F7 compliance")

# 2. Read code
filesystem.read_file(path: "arifosmcp.transport/core/constitutional_decorator.py")

# 3. Check git history
git_log(max_count: 5, path: "arifosmcp.transport/core/constitutional_decorator.py")

# 4. Multi-step reasoning
sequentialthinking(thought: "Analyzing F7 implementation...", ...)

# 5. Reality check on patterns
reality_search(query: "Python decorator pattern best practices 2025")

# 6. Verdict
apex_verdict(query: "Is F7 properly implemented?", ...)

# 7. Seal and commit
vault_seal(session_id: "...", verdict: "SEAL", payload: {...})
git_commit(message: "F7: Calibrate humility band to [0.03,0.05]")
```

### Example 2: Research Task with Memory
```python
# 1. Search for information
reality_search(query: "ASEAN AI governance framework 2026", region: "asean")

# 2. Fetch detailed content
fetch(url: result[0].url)

# 3. Store in knowledge graph
create_entities(entities: [{
  "name": "ASEAN AI Governance",
  "entityType": "policy",
  "observations": ["..."]
}])

# 4. Future retrieval
search_nodes(query: "ASEAN AI governance")
```

---

## 🔧 Troubleshooting

### MCP Server Not Found
```bash
# Reinstall specific server
npx -y @modelcontextprotocol/server-filesystem@latest

# Or update all
npm update -g @modelcontextprotocol/server-filesystem
```

### Permission Denied
```json
// In mcp.json, add to env:
{
  "env": {
    "PYTHONPATH": "C:/Users/User/arifOS",
    "GIT_CONFIG_GLOBAL": ""
  }
}
```

### Rate Limiting (DDGS)
The `reality_search` tool has built-in throttling (2s between calls). If you hit limits:
1. Wait 60 seconds
2. Or use `fetch` directly with known URLs

---

## 📚 References

- [Model Context Protocol Spec](https://modelcontextprotocol.io/)
- [Kimi CLI MCP Docs](https://github.com/moonshotai/kimi-cli/blob/main/docs/en/customization/mcp.md)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)
- [arifOS Constitutional Framework](https://github.com/ariffazil/arifOS)

---

**Sovereign:** Muhammad Arif bin Fazil  
**Repository:** https://github.com/ariffazil/arifOS  
**Motto:** *Ditempa Bukan Diberi* (Forged, Not Given)
