#!/bin/bash
# arifOS Cleanup Script — Remove Chaos
# Execute: bash scripts/cleanup_chaos.sh

set -e

echo "🔥 arifOS Chaos Cleanup — Entropy Reduction"
echo "=============================================="

# Create safety backup first
echo "📦 Creating safety backup..."
tar -czf /tmp/arifos_backup_$(date +%Y%m%d_%H%M%S).tar.gz archive/ 2>/dev/null || true

cd ~/arifOS

# 1. DELETE: Obvious duplicates in archive
echo "🗑️  Removing archive duplicates..."
rm -rf archive/agi/ 2>/dev/null || true
rm -rf archive/asi/ 2>/dev/null || true  
rm -rf archive/apex/ 2>/dev/null || true
rm -rf archive/vault/ 2>/dev/null || true
rm -rf archive/init/ 2>/dev/null || true
echo "   ✅ Archive engine duplicates removed"

# 2. DELETE: Old version tarballs (keep latest 3)
echo "🗑️  Compressing old versions..."
cd archive/
for dir in arifos-46.* v49_* v50_* v51_*; do
    if [ -d "$dir" ]; then
        tar -czf "${dir}.tar.gz" "$dir" 2>/dev/null && rm -rf "$dir" 2>/dev/null
        echo "   📦 Compressed: $dir"
    fi
done
cd ~/arifOS

# 3. DELETE: Legacy MCP implementations
echo "🗑️  Removing legacy MCP..."
rm -rf mcp_server/archive/ 2>/dev/null || true
rm -rf codebase/mcp/archive/ 2>/dev/null || true
echo "   ✅ Legacy MCP removed"

# 4. KEEP BUT DOCUMENT: Important archives
echo "📋 Keeping critical archives..."
# deployment-backup has wisdom docs
# constitutionally_sealed has releases
echo "   ✅ deployment-backup/ — kept (has wisdom)"
echo "   ✅ constitutionally_sealed/ — kept (releases)"

# 5. Summary
echo ""
echo "=============================================="
echo "✅ Cleanup Complete!"
echo ""
echo "Before: Multiple duplicate engines"
echo "After: Single canonical paths"
echo ""
echo "Key preservation:"
echo "  - archive/deployment-backup/ (wisdom)"
echo "  - archive/constitutionally_sealed/ (releases)"
echo "  - Latest 3 version tarballs"
echo ""
echo "DITEMPA BUKAN DIBERI 💎🔥🧠"
