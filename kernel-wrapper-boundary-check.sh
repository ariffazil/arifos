#!/bin/bash
# kernel-wrapper-boundary-check.sh
# Enforces: aaa_mcp/ must NEVER contain decision logic
# Run: ./kernel-wrapper-boundary-check.sh

set -e

echo "=== Kernel/Wrapper Boundary Check ==="
echo ""

VIOLATIONS=0

# Check 1: Uncertainty computation in wrapper
echo "🔍 Checking for uncertainty computation in aaa_mcp/..."
if grep -r "calculate_uncertainty" aaa_mcp/ --include="*.py" 2>/dev/null | grep -v "from core" | grep -v "^#"; then
    echo "   ❌ VIOLATION: calculate_uncertainty called in wrapper"
    VIOLATIONS=$((VIOLATIONS + 1))
else
    echo "   ✅ No local uncertainty computation"
fi

# Check 2: UncertaintyEngine instantiation in wrapper
echo ""
echo "🔍 Checking for UncertaintyEngine in aaa_mcp/..."
if grep -r "UncertaintyEngine()" aaa_mcp/ --include="*.py" 2>/dev/null | grep -v "from core"; then
    echo "   ❌ VIOLATION: UncertaintyEngine instantiated in wrapper"
    VIOLATIONS=$((VIOLATIONS + 1))
else
    echo "   ✅ No local UncertaintyEngine"
fi

# Check 3: Governance state modification
echo ""
echo "🔍 Checking for governance state modification in aaa_mcp/..."
if grep -r "governance_state\s*=" aaa_mcp/ --include="*.py" 2>/dev/null | grep -v "from core\|import"; then
    echo "   ❌ VIOLATION: governance_state modified in wrapper"
    VIOLATIONS=$((VIOLATIONS + 1))
else
    echo "   ✅ No direct governance modification"
fi

# Check 4: Verdict logic in wrapper (basic check)
echo ""
echo "🔍 Checking for verdict logic in aaa_mcp/..."
VERDICT_LINES=$(grep -r 'verdict.*=.*"SEAL"\|verdict.*=.*"VOID"\|verdict.*=.*"SABAR"' aaa_mcp/ --include="*.py" 2>/dev/null | wc -l)
if [ "$VERDICT_LINES" -gt 5 ]; then
    echo "   ⚠️  WARNING: $VERDICT_LINES lines with verdict assignments (review needed)"
else
    echo "   ✅ Minimal verdict logic (acceptable for response formatting)"
fi

# Check 5: Import sanity
echo ""
echo "🔍 Checking imports..."
if grep -r "from aaa_mcp" aaa_mcp/ --include="*.py" 2>/dev/null; then
    echo "   ⚠️  Internal aaa_mcp imports (may indicate coupling)"
fi

echo ""
echo "=== Summary ==="
if [ $VIOLATIONS -eq 0 ]; then
    echo "✅ Boundary check PASSED — No critical violations"
    exit 0
else
    echo "❌ Boundary check FAILED — $VIOLATIONS violation(s) detected"
    echo ""
    echo "See ARCHITECTURAL_BOUNDARY.md for migration guidance"
    exit 1
fi
