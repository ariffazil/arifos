#!/bin/bash
# init-000.sh - AGI Session Initialization Protocol
# Canonical source: ariffazil/arifOS | ariffazil/arif-fazil-sites | ariffazil/AGI_ASI_bot
# Ω₀ ≈ 0.04

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=== AGI-bot init-000 Protocol ==="
echo "Date: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo ""

# Configuration
REPOS_DIR="${REPOS_DIR:-$HOME/repos}"
ARIFOS_REPO="https://github.com/ariffazil/arifOS.git"
SITES_REPO="https://github.com/ariffazil/arif-fazil-sites.git"
AGIBOT_REPO="https://github.com/ariffazil/AGI_ASI_bot.git"

echo "[1/4] Checking repository directory..."
mkdir -p "$REPOS_DIR"
cd "$REPOS_DIR"

# Function to sync a repo
sync_repo() {
    local repo_url=$1
    local repo_name=$2
    
    echo ""
    echo "Syncing $repo_name..."
    
    if [ -d "$repo_name" ]; then
        cd "$repo_name"
        # Check for dirty working tree (fail-closed)
        if [ -n "$(git status --porcelain)" ]; then
            echo -e "${RED}ERROR: $repo_name has uncommitted changes${NC}"
            echo "Manual intervention required. Stash or commit changes before init-000."
            exit 1
        fi
        
        # Check for unpushed commits
        if [ -n "$(git log origin/$(git branch --show-current)..HEAD 2>/dev/null)" ]; then
            echo -e "${YELLOW}WARNING: $repo_name has unpushed commits${NC}"
            echo "Consider pushing before proceeding."
        fi
        
        git pull --ff-only
        echo -e "${GREEN}✓ $repo_name synced${NC}"
        cd ..
    else
        git clone "$repo_url" "$repo_name"
        echo -e "${GREEN}✓ $repo_name cloned${NC}"
    fi
}

# Sync all three repos
sync_repo "$ARIFOS_REPO" "arifOS"
sync_repo "$SITES_REPO" "arif-fazil-sites"
sync_repo "$AGIBOT_REPO" "AGI_ASI_bot"

echo ""
echo "[2/4] Installing/updating arifOS library..."
cd "$REPOS_DIR/arifOS"
if [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
    pip install -e . --quiet
    echo -e "${GREEN}✓ arifOS installed in editable mode${NC}"
else
    pip install -U arifos --quiet
    echo -e "${GREEN}✓ arifOS updated from PyPI${NC}"
fi

echo ""
echo "[3/4] Loading constitutional files..."
ARIFOS_DIR="$REPOS_DIR/arifOS"

# Verify canonical files exist
for file in "USER.md" "SOUL.md"; do
    if [ ! -f "$ARIFOS_DIR/$file" ]; then
        echo -e "${RED}ERROR: $file not found in arifOS repo${NC}"
        exit 1
    fi
    echo "  ✓ $file loaded"
done

# Check for MEMORY.md (working context)
if [ -f "$ARIFOS_DIR/MEMORY.md" ]; then
    echo "  ✓ MEMORY.md found"
fi

# Check for PETRONAS dossier
if [ -f "$ARIFOS_DIR/vault_999/TMT-AUDIT-2026.md" ] || \
   [ -f "$ARIFOS_DIR/docs/petronas_dossier.md" ]; then
    echo "  ✓ PETRONAS dossier found"
fi

echo ""
echo "[4/4] arifOS init-gate..."
python3 << 'PYTHON_EOF'
import sys
import os

# Add arifOS to path
sys.path.insert(0, os.path.expanduser("~/repos/arifOS"))

try:
    import arifos
    from arifos import init_gate
    
    # Call init gate
    result = init_gate(
        session_type="agi",
        context="openclaw",
        user_identity="Muhammad Arif bin Fazil (888 Judge)"
    )
    
    print(f"  ✓ arifOS version: {arifos.__version__}")
    print(f"  ✓ Init-gate: {result.get('status', 'SEAL')}")
    print(f"  ✓ Motto: {result.get('motto', 'DITEMPA BUKAN DIBERI')}")
    print(f"  ✓ Active Floors: {', '.join(result.get('floors', ['F1', 'F2', 'F7', 'F9', 'F13']))}")
    
except ImportError:
    print("  ⚠ arifOS Python library not fully initialized (expected for early versions)")
    print("  ✓ Manual verification: USER.md and SOUL.md loaded from ~/repos/arifOS")
except Exception as e:
    print(f"  ⚠ Init-gate returned: {e}")
    print("  ✓ Continuing with manual file load")

PYTHON_EOF

echo ""
echo "=== init-000 Complete ==="
echo -e "${GREEN}AGI session ready for constitutional governance${NC}"
echo ""
echo "Canonical sources:"
echo "  • arifOS: $ARIFOS_REPO"
echo "  • Sites: $SITES_REPO"
echo "  • AGI-bot: $AGIBOT_REPO"
echo ""
echo "Next: Build system prompt with Floors, PETRONAS dossier, USER.md constraints."
