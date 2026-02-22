#!/usr/bin/env bash
# DEPLOY.sh — arifOS Docs Site Production Deployment
#
# ╔══════════════════════════════════════════════════════════════════════╗
# ║  888_HOLD: This script modifies production server state.            ║
# ║  Review every step. Run only after explicit human ratification.     ║
# ║  F1 Amanah: rsync preserves originals; no destructive operations.  ║
# ╚══════════════════════════════════════════════════════════════════════╝
#
# Usage (on VPS, from repo root):
#   bash sites/docs/DEPLOY.sh [--dry-run]
#
# Prerequisites:
#   - Nginx installed, certbot installed
#   - DNS: arifos.arif-fazil.com → 72.62.71.199
#   - This script run as root (or sudo)
#
# What this script does:
#   1. Copies build/ to /var/www/arifos-docs/
#   2. Installs Nginx config
#   3. Tests Nginx config
#   4. Reloads Nginx (non-destructive — no restart)
#   5. Runs a health check on the live URL

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BUILD_DIR="$REPO_ROOT/sites/docs/build"
WEB_ROOT="/var/www/arifos-docs"
NGINX_CONF="$REPO_ROOT/sites/docs/arifos-docs-nginx.conf"
NGINX_SITES_AVAILABLE="/etc/nginx/sites-available/arifos-docs"
NGINX_SITES_ENABLED="/etc/nginx/sites-enabled/arifos-docs"
DOMAIN="arifos.arif-fazil.com"
DRY_RUN="${1:-}"

echo "══════════════════════════════════════════════════════════"
echo "  arifOS Docs — Production Deploy"
echo "  Source:  $BUILD_DIR"
echo "  Target:  $WEB_ROOT"
echo "  Domain:  https://$DOMAIN/docs/"
echo "  Mode:    ${DRY_RUN:-live}"
echo "══════════════════════════════════════════════════════════"
echo ""

if [ ! -d "$BUILD_DIR" ]; then
    echo "ERROR: Build directory not found: $BUILD_DIR"
    echo "Run 'npm run build' in sites/docs/ first."
    exit 1
fi

# Count files in build
FILE_COUNT=$(find "$BUILD_DIR" -type f | wc -l)
BUILD_SIZE=$(du -sh "$BUILD_DIR" | cut -f1)
echo "▶ Build verified: $FILE_COUNT files, $BUILD_SIZE"
echo ""

if [ "$DRY_RUN" = "--dry-run" ]; then
    echo "DRY RUN — showing what would be executed:"
    echo ""
    echo "  mkdir -p $WEB_ROOT"
    echo "  rsync -av --delete $BUILD_DIR/ $WEB_ROOT/"
    echo "  chown -R www-data:www-data $WEB_ROOT"
    echo "  cp $NGINX_CONF $NGINX_SITES_AVAILABLE"
    echo "  ln -sf $NGINX_SITES_AVAILABLE $NGINX_SITES_ENABLED"
    echo "  nginx -t"
    echo "  systemctl reload nginx"
    echo "  curl -I https://$DOMAIN/docs/intro"
    echo ""
    echo "No changes made. Remove --dry-run to execute."
    exit 0
fi

# ── Step 1: Create web root ──────────────────────────────────────────────────
echo "▶ Step 1: Preparing web root..."
mkdir -p "$WEB_ROOT"

# ── Step 2: Sync build to web root ──────────────────────────────────────────
echo "▶ Step 2: Syncing build/ → $WEB_ROOT/"
echo "  (rsync --delete removes stale files — reversible by re-deploying)"
rsync -av --delete --checksum "$BUILD_DIR/" "$WEB_ROOT/"
chown -R www-data:www-data "$WEB_ROOT"
echo "  ✅ Sync complete."
echo ""

# ── Step 3: Install Nginx config ────────────────────────────────────────────
echo "▶ Step 3: Installing Nginx config..."
cp "$NGINX_CONF" "$NGINX_SITES_AVAILABLE"
ln -sf "$NGINX_SITES_AVAILABLE" "$NGINX_SITES_ENABLED"
echo "  ✅ Config installed: $NGINX_SITES_AVAILABLE"
echo ""

# ── Step 4: Test Nginx config ────────────────────────────────────────────────
echo "▶ Step 4: Testing Nginx config..."
if nginx -t; then
    echo "  ✅ Nginx config test passed."
else
    echo "  ❌ Nginx config test FAILED."
    echo "  SABAR: rolling back Nginx config install."
    rm -f "$NGINX_SITES_ENABLED"
    exit 1
fi
echo ""

# ── Step 5: Obtain TLS cert if needed ───────────────────────────────────────
if [ ! -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]; then
    echo "▶ Step 5: TLS certificate not found — requesting via Certbot..."
    echo "  [888_HOLD] This modifies /etc/letsencrypt/ — confirm? (Ctrl+C to abort)"
    read -r -t 30 -p "  Press Enter to continue or Ctrl+C to abort..."
    certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos \
        --email "arifbfazil@gmail.com" --redirect
    echo "  ✅ Certificate obtained."
else
    echo "▶ Step 5: TLS certificate found — skipping Certbot."
fi
echo ""

# ── Step 6: Reload Nginx ────────────────────────────────────────────────────
echo "▶ Step 6: Reloading Nginx (graceful — no downtime)..."
systemctl reload nginx
echo "  ✅ Nginx reloaded."
echo ""

# ── Step 7: Live health check ────────────────────────────────────────────────
echo "▶ Step 7: Live health check..."
sleep 2   # brief settle time

HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN/docs/intro" --max-time 10 || echo "000")

if [ "$HTTP_STATUS" = "200" ]; then
    echo "  ✅ https://$DOMAIN/docs/intro → HTTP $HTTP_STATUS — SEAL"
else
    echo "  ⚠️  https://$DOMAIN/docs/intro → HTTP $HTTP_STATUS"
    echo "  SABAR: Check Nginx error log: tail -50 /var/log/nginx/arifos-docs-error.log"
fi

echo ""
echo "══════════════════════════════════════════════════════════"
echo "  Deploy complete."
echo "  Docs live at: https://$DOMAIN/docs/"
echo "  Nginx root:   $WEB_ROOT"
echo "  Logs:         /var/log/nginx/arifos-docs-access.log"
echo "  Sitemap:      https://$DOMAIN/docs/sitemap.xml"
echo "══════════════════════════════════════════════════════════"
