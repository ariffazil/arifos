#!/usr/bin/env bash
# SCAFFOLD.sh — arifOS Docs Site Setup Script
#
# ────────────────────────────────────────────────────────────────────────────
# 888_HOLD: Review every command before running.
# This script installs npm dependencies and (optionally) runs a local preview.
# It does NOT deploy, push to git, or modify any server configuration.
# ────────────────────────────────────────────────────────────────────────────
#
# Usage:
#   cd sites/docs
#   bash SCAFFOLD.sh          # install + local preview
#   bash SCAFFOLD.sh build    # install + production build only
#
# Requirements:
#   - Node.js >= 18
#   - npm >= 9 (or use pnpm/yarn if preferred)
#
# F1 Amanah: This script only installs and builds — no irreversible actions.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "═══════════════════════════════════════════════════════════"
echo "  arifOS Docs — Scaffold & Preview"
echo "  Target: https://arifos.arif-fazil.com/docs/"
echo "  Node: $(node --version 2>/dev/null || echo 'NOT FOUND — install Node >= 18')"
echo "═══════════════════════════════════════════════════════════"
echo ""

# ── Step 1: Check Node version ──────────────────────────────────────────────
NODE_VERSION=$(node --version 2>/dev/null | sed 's/v//' | cut -d. -f1)
if [ -z "$NODE_VERSION" ] || [ "$NODE_VERSION" -lt 18 ]; then
  echo "ERROR: Node.js >= 18 is required. Current: $(node --version 2>/dev/null || echo 'none')"
  echo "Install: https://nodejs.org or use nvm: nvm install 20"
  exit 1
fi

# ── Step 2: Install dependencies ────────────────────────────────────────────
echo "▶ Installing npm dependencies..."
npm install

echo ""
echo "✅ Dependencies installed."
echo ""

# ── Step 3: Build or serve ───────────────────────────────────────────────────
if [ "${1:-serve}" = "build" ]; then
  echo "▶ Building production site..."
  npm run build
  echo ""
  echo "✅ Build complete. Output: sites/docs/build/"
  echo ""
  echo "To serve the build locally:"
  echo "  npm run serve"
  echo ""
  echo "To deploy: copy build/ to your Nginx web root or run:"
  echo "  rsync -av build/ user@your-vps:/var/www/arifos-docs/"
else
  echo "▶ Starting local dev server at http://localhost:3000/docs/"
  echo "   (Press Ctrl+C to stop)"
  echo ""
  npm run start
fi
