---
name: f1-amanah-file-guardian
description: Constitutional file manipulation utilities with F1 Amanah (reversibility), F2 Truth (document integrity), F6 Clarity (entropy reduction), F11 Command Authority, and F12 Injection Defense. Merged from f1-amanah-file-guardian + f2-truth-document-guardian + amanah-reversible-audit. Use when working with file system operations, batch processing, document handling, or file format conversions with full audit trail and ANCHOR/REASON/SEAL protocols.
version: "v64.1-GAGI-HARDENED"
authority: "Muhammad Arif bin Fazil"
---

# F1 Amanah File Guardian (v64.1-GAGI-HARDENED)

**Constitutional Status:** HARDENED  
**Floors Enforced:** F1, F2, F6, F11, F12  
**Features:** File ops + Document integrity + Reversibility  
**Merged From:** f1-amanah + f2-truth-document + amanah-reversible-audit  

---

## ANCHOR Phase — Pre-Operation Authority

**Constitutional Floor:** F11 + F12 + F1

Before ANY file operation:

```
ANCHOR CHECKLIST:
├── C5_config_flags
│   └── Verify execution environment (.venv, PYTHONPATH)
├── F12 Injection Defense
│   ├── Sanitize all paths (no .., ~, $, `, |, ;, &)
│   ├── Check for shell metacharacters
│   └── Canonicalize paths (resolve symlinks)
├── F11 Command Authority
│   ├── Check against system paths (Windows/, Program Files/, /usr/, /etc/)
│   ├── Verify user permissions
│   └── Block destructive ops on system dirs
└── F1 Amanah Pre-check
    ├── Classify operation (read/write/delete/batch)
    ├── Plan backup for destructive ops
    └── Calculate reversibility score

GATES:
- Dangerous path → VOID with F12 violation
- System directory → VOID with F11 violation (or 888_HOLD)
- Destructive op without backup plan → SABAR
```

---

## Constitutional Foundation

### F1 Amanah (Sacred Trust)
```
∀ file operation O: ∃ inverse O⁻¹ OR ∃ complete audit log L(O)

Requirements:
- All destructive operations require backup
- All operations logged with Merkle hash
- Reversibility is default; irreversibility requires explicit override
- Batch ops >100 files → Tier 3 cooling (168h)
```

### F2 Truth (Document Integrity)
```
τ ≥ 0.99 for document operations

Requirements:
- Text extraction accuracy verification
- OCR confidence scoring (if applicable)
- Malformed file detection (F12 injection defense)
- Checksum validation for conversions
```

### F6 Clarity (ΔS ≤ 0)
```
ΔS = S(operation_input) - S(operation_output) ≤ 0

Requirements:
- Operations produce clearer state
- Before/after diff mandatory
- Entropy reduction verification
```

### F11 + F12 (Authority & Defense)
```
A = verify(command.source) ∈ {authorized_entities}
I⁻ = P(input is injection) < 0.85

Requirements:
- Path traversal blocked
- Shell injection detected
- Permission validation
```

---

## REASON Phase — Plan-Act-Verify

**Required for:**
- Batch operations (>10 files)
- Destructive operations (delete, overwrite)
- Format conversions
- System-level changes

### Plan Phase
```python
def plan_file_operation(
    operation: str,
    targets: List[str],
    constraints: Dict
) -> PlanResult:
    """
    F8: Plan with Genius calculation
    """
    # Gather info
    targets_info = [analyze_file(t) for t in targets]
    
    # Calculate approaches
    approaches = []
    
    # Conservative: Full backup, dry-run, then execute
    approaches.append({
        'name': 'CONSERVATIVE',
        'safety': 0.95, 'efficiency': 0.70,
        'reversibility': 1.0,
        'description': 'Backup → Dry-run → Execute → Verify'
    })
    
    # Transactional: Atomic with rollback
    approaches.append({
        'name': 'TRANSACTIONAL',
        'safety': 0.85, 'efficiency': 0.85,
        'reversibility': 0.95,
        'description': 'Atomic batches with auto-rollback'
    })
    
    # Select by Genius score
    for a in approaches:
        A, P, X, E = a['safety'], 0.90, 0.85, a['efficiency']
        a['G'] = A * P * X * (E ** 2)
    
    best = max(approaches, key=lambda x: x['G'])
    
    if best['G'] < 0.80:
        return PlanResult.SABAR("No approach meets F8 Genius threshold")
    
    return PlanResult.SEAL(
        approach=best,
        reversibility_plan=calculate_rollback(best, targets)
    )
```

### Act Phase
```python
def execute_with_verification(plan: PlanResult) -> ExecutionResult:
    """
    Execute with continuous verification
    """
    # F1: Create backup if needed
    if plan.requires_backup:
        backup_path = create_backup(plan.targets)
    
    # F2: Pre-verify document integrity (if documents)
    if plan.has_documents:
        checksums = {t: calculate_checksum(t) for t in plan.targets}
    
    # Execute
    results = []
    for target in plan.targets:
        result = execute_single(target, plan.operation)
        
        # F6: Verify clarity improvement
        if not verify_entropy_reduction(target, result):
            rollback(target, backup_path)
            return ExecutionResult.VOID("F6 Clarity violation")
        
        results.append(result)
    
    return ExecutionResult.SEAL(results=results, backup_path=backup_path)
```

### Verify Phase
```python
def verify_operation(result: ExecutionResult) -> VerifyResult:
    """
    F2: Truth verification
    """
    # Check all operations completed
    if not all(r.success for r in result.results):
        return VerifyResult.VOID("Partial failure")
    
    # Verify reversibility (F1)
    if result.backup_path:
        test_restore = verify_backup_integrity(result.backup_path)
        if not test_restore:
            return VerifyResult.SABAR("Backup verification failed")
    
    # Calculate final entropy (F6)
    final_entropy = calculate_total_entropy(result.results)
    
    return VerifyResult.SEAL(
        integrity_verified=True,
        reversibility_confirmed=bool(result.backup_path),
        final_entropy=final_entropy
    )
```

---

## Document-Specific Operations (F2 Truth)

### Text Extraction
```python
def extract_text_document(
    filepath: str,
    verify_accuracy: bool = True
) -> ExtractionResult:
    """
    F2: Extract with τ ≥ 0.99
    """
    # Detect file type
    doc_type = detect_document_type(filepath)
    
    # Extract based on type
    if doc_type == "PDF":
        text = extract_pdf_with_pdfplumber(filepath)
    elif doc_type in ["DOCX", "DOC"]:
        text = extract_docx_with_python_docx(filepath)
    # ... etc
    
    # F2: Verify accuracy
    if verify_accuracy:
        confidence = verify_extraction_accuracy(filepath, text)
        if confidence < 0.99:
            return ExtractionResult.SABAR(
                f"F2 Truth: extraction confidence {confidence:.2f} < 0.99"
            )
    
    return ExtractionResult.SEAL(text=text, confidence=confidence)
```

### Malicious Document Detection (F12)
```python
def scan_document_security(filepath: str) -> SecurityResult:
    """
    F12: Injection defense for documents
    """
    threats = []
    
    # Check for embedded scripts
    if has_embedded_javascript(filepath):
        threats.append("javascript_embed")
    
    # Check for suspicious macros
    if has_macros(filepath) and not is_trusted_source(filepath):
        threats.append("untrusted_macros")
    
    # Check for path traversal in filenames
    if contains_path_traversal(filepath):
        threats.append("path_traversal")
    
    risk_score = min(len(threats) * 0.3 + 0.1, 0.95)
    
    if risk_score >= 0.85:
        return SecurityResult.VOID(
            f"F12 Injection Defense: risk {risk_score:.2f}",
            threats=threats
        )
    
    return SecurityResult.SEAL(risk_score=risk_score)
```

---

## SEAL Phase — Audit Trail

```python
def seal_file_operation(
    operation: str,
    targets: List[str],
    result: ExecutionResult
) -> VaultResult:
    """
    F1: Complete audit trail
    """
    entry = {
        "timestamp": utc_now(),
        "operation": operation,
        "targets": [canonicalize_path(t) for t in targets],
        "result": result.verdict,
        "backup_path": result.backup_path,
        "entropy_delta": result.entropy_change,
        "merkle_root": calculate_merkle_root(result.results)
    }
    
    # Memory persistence
    memory.create_entities([{
        "name": f"file-op-{entry['timestamp']}",
        "entityType": "file_operation",
        "observations": [
            f"Operation: {operation}",
            f"Files: {len(targets)}",
            f"Verdict: {result.verdict}",
            f"Reversible: {bool(result.backup_path)}",
            f"F2 confidence: {result.f2_confidence:.4f}"
        ]
    }])
    
    return Vault999().seal(entry)
```

---

## Usage Examples

**Safe Bulk Rename:**
```python
# ANCHOR
anchor_check(paths)

# REASON
plan = plan_file_operation("rename", files, constraints)
result = execute_with_verification(plan)

# SEAL
vault_id = seal_file_operation("rename", files, result)
```

**Document Conversion:**
```python
# F2 verification
security = scan_document_security(input_file)
text = extract_text_document(input_file, verify_accuracy=True)

# F1 backup + operation
backup = create_backup(input_file)
convert_format(input_file, output_format)

# Verify
assert verify_checksum(output_file)
```

---

**DITEMPA BUKAN DIBERI** — Forged, Not Given.
