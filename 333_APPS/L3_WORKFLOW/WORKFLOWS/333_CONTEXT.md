# Workflow: 333_CONTEXT

**Stage:** 333 (Atlas/Context)  
**Purpose:** Gather and map relevant context for the task  
**Trigger:** After 111_INTENT lane assignment  
**Output:** Context map with file inventory and dependency graph

---

## 🎯 When to Use

Use this workflow after intent is understood to gather all relevant files, dependencies, and context needed for safe execution.

---

## 📋 Workflow Steps

### Step 1: File Discovery
```markdown
Based on intent_map, discover relevant files:

1. Primary targets (explicitly mentioned):
   - grep for entity names
   - locate exact file paths
   - verify file existence

2. Secondary dependencies (implicit):
   - imports/requires
   - related tests
   - configuration files
   - documentation

3. Tertiary context (ecosystem):
   - Similar implementations
   - Pattern examples
   - Style guides
```

### Step 2: Dependency Mapping
```markdown
Build dependency graph:

UPSTREAM (what this depends on):
├── Imported modules
├── Parent classes
├── Configuration sources
└── Data schemas

DOWNSTREAM (what depends on this):
├── Tests
├── Child classes
├── UI components
├── API consumers
└── Documentation

SIBLINGS (related components):
├── Similar features
├── Alternative implementations
├── Parallel modules
```

### Step 3: Constitutional Constraints Check
```markdown
Check for constraints based on file types:

CODE files:
├── Check for F1 Amanah (reversibility markers)
├── Check for F9 Anti-Hantu (dark patterns)
└── Check for F12 Injection (input handling)

CONFIG files:
├── Check for secrets/credentials
├── Check for environment-specific values
└── Check for backup requirements

DOC files:
├── Check for accuracy markers
├── Check for F2 Truth citations
└── Check for freshness dates
```

### Step 4: Entropy Analysis
```markdown
Measure information entropy:

1. Read relevant files
2. Calculate S_current (current entropy of context)
3. Compare to S_target from 000_SESSION_INIT
4. If S_current > S_target:
   - Prune non-essential files
   - Summarize verbose content
   - Focus on essential context
5. Goal: ΔS ≤ 0 (reduce confusion)
```

### Step 5: Safety Markers
```markdown
Identify safety-critical elements:

🔴 CRITICAL (HARD lane trigger):
├── Authentication/Authorization code
├── Database migrations
├── API contracts
├── Security configurations
└── Production secrets

🟡 IMPORTANT (SOFT lane):
├── Business logic
├── Data models
├── Error handling
└── Logging

🟢 STANDARD (PHATIC lane):
├── Comments
├── Formatting
├── Naming
└── Documentation
```

### Step 6: Atlas Generation
```markdown
Create context atlas (knowledge map):

atlas:
  session_id: "..."
  center: "target_file"
  radius: "dependency_depth"
  nodes:
    - id: "file_path"
      type: "code|config|doc|test"
      importance: "critical|important|standard"
      constitutional_markers: [F1, F2, ...]
  edges:
    - from: "file_a"
      to: "file_b"
      type: "imports|tests|documents"
  coverage:
    - percentage of relevant context captured
    - gaps identified
    - assumptions documented
```

---

## 📝 Output Specification

### Context Map Object
```yaml
context_map:
  session_id: "session_2026-01-31_abc123"
  
  files:
    primary:
      - path: "src/auth/settings.tsx"
        type: "code"
        size: 2450
        importance: "critical"
        markers: ["F1", "F9"]
    
    secondary:
      - path: "src/auth/theme.ts"
        type: "code"
        size: 890
        importance: "important"
        markers: ["F4"]
      
      - path: "tests/auth/settings.test.tsx"
        type: "test"
        size: 1200
        importance: "important"
        markers: ["F2"]
    
    tertiary:
      - path: "docs/ui-guidelines.md"
        type: "doc"
        size: 5600
        importance: "standard"
        markers: []
  
  dependencies:
    upstream:
      - "src/theme/provider.tsx"
      - "src/user/preferences.ts"
    
    downstream:
      - "src/settings/index.tsx"
      - "e2e/settings.spec.ts"
    
    siblings:
      - "src/auth/login.tsx"
      - "src/auth/profile.tsx"
  
  entropy:
    s_input: 1.0
    s_current: 0.65
    s_target: 0.7
    delta_s: -0.35  # ✅ Within target
  
  safety_markers:
    critical: 1
    important: 2
    standard: 1
  
  coverage: 0.85  # 85% of relevant context captured
  gaps:
    - "Dark mode persistence mechanism unclear"
  
  next_stage: "555_SAFETY"
```

---

## 🔄 Next Stage

After 333_CONTEXT completes → Proceed to **555_SAFETY**

---

## ✅ Completion Checklist

- [ ] Files discovered (primary/secondary/tertiary)
- [ ] Dependencies mapped (up/down/sibling)
- [ ] Constitutional markers identified
- [ ] Entropy measured (ΔS ≤ 0)
- [ ] Safety markers classified
- [ ] Atlas generated
- [ ] Coverage ≥ 80%
- [ ] Gaps documented
- [ ] Output saved to state

---

## 🛡️ Constitutional Compliance

| Floor | Verification | Status |
|-------|--------------|--------|
| F4 | Clarity (entropy reduced) | Required |
| F7 | Humility (coverage < 100%) | Required |
| F9 | Anti-Hantu (no dark patterns) | Required |
| F10 | Ontology (files exist) | Required |

---

## 📝 Usage Example

```markdown
[After 111_INTENT: "Add dark mode" → SOFT lane]

AI: [Executes 333_CONTEXT]
  → Primary: settings.tsx (critical)
  → Secondary: theme.ts, settings.test.tsx
  → Dependencies: theme provider, user prefs
  → Entropy: 0.65 (within target)
  → Coverage: 85%
  → Gap: persistence mechanism
  
Proceeding to 555_SAFETY evaluation...
```

---

## 🔄 000-999 Loop Integration

```
Previous: 111_INTENT (Understanding)
Current:  333_CONTEXT (Mapping)
Next:     555_SAFETY (Empathy/Defense)

Connection: Context enables safety evaluation
```

**Loop Reference:** Atlas stage prepares the terrain for safe navigation.

---

**DITEMPA BUKAN DIBERI**
