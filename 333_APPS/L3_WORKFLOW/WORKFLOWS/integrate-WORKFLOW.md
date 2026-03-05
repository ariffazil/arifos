# Workflow: integrate
**Stage:** 333 (Map/Atlas)  
**Purpose:** Context atlas: file discovery, dependency graph, entropy analysis.  
**Trigger:** After reason-WORKFLOW hypothesis generation.  
**Output:** Context map with file inventory and dependency graph.

---

## 🎯 When to Use
Use this to map the physical and organizational context of the codebase related to the task.

---

## 📋 Workflow Steps

### Step 1: File Discovery (Atlas)
1. Discover primary targets (explicit).
2. Trace secondary dependencies (imports, tests, configs).
3. Gather tertiary context (patterns, style guides).

### Step 2: Dependency Mapping
1. Build Upstream/Downstream/Sibling dependency graph.
2. Identify safety-critical elements (Auth, DB, Security).

### Step 3: Entropy Analysis (F4)
1. Measure S_input vs S_current.
2. Prune non-essential context to ensure ΔS ≤ 0.
3. Goal: Reduce complexity/confusion.

### Step 4: Ontology Check (F10)
1. Verify file existence and grounding.
2. Identify gaps in current knowledge mapping.

---

## 📝 Output Specification
```yaml
atlas:
  primary_targets: [...]
  dependency_depth: 2
  delta_s: -0.35
  coverage_score: 0.85
```

---

**DITEMPA BUKAN DIBERI**
