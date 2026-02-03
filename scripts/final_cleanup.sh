#!/bin/bash
# FINAL CLEANUP — Remove All Chaos Before Shipping v55.4
# Execute: bash scripts/final_cleanup.sh

set -e

echo "🔥 FINAL CLEANUP — arifOS v55.4"
echo "================================"

cd ~/arifOS

# 1. Remove duplicate/stub files that don't connect to real engines
echo "🗑️  Removing stub files..."

# Remove any __pycache__ recursively
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Remove .pyc files
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# Remove test artifacts
rm -f tests/*.log 2>/dev/null || true
rm -f tests/*_results.json 2>/dev/null || true
rm -rf .pytest_cache/ 2>/dev/null || true

# 2. Verify critical files exist
echo "✅ Verifying critical files..."

required_files=(
    "codebase/floors/canonical.py"
    "codebase/agi/engine.py"
    "codebase/asi/engine.py"
    "codebase/apex/kernel.py"
    "codebase/vault/persistence.py"
    "codebase/mcp/fastmcp_clean.py"
    "codebase/mcp/constitutional_decorator.py"
    "codebase/mcp/engine_adapters.py"
    "codebase/init/000_init/mcp_bridge.py"
    "tests/day1_e2e_test.py"
    "docs/INDEX.md"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ MISSING: $file"
    fi
done

# 3. Count final metrics
echo ""
echo "📊 Final Metrics:"
echo "   Python files: $(find codebase -name '*.py' | wc -l)"
echo "   Test files: $(find tests -name '*.py' 2>/dev/null | wc -l)"
echo "   Archive tarballs: $(ls archive/*.tar.gz 2>/dev/null | wc -l)"

# 4. Git status
echo ""
echo "📦 Git Status:"
git status --short

echo ""
echo "================================"
echo "✅ CLEANUP COMPLETE"
echo ""
echo "Ready for:"
echo "   pip install fastmcp"
echo "   python codebase/mcp/fastmcp_clean.py"
echo ""
echo "DITEMPA BUKAN DIBERI 💎🔥🧠"
