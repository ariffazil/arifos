#!/bin/bash
# preseal_evidence.sh — Pre-seal evidence collector for arifOS deployments
# Skill: vps_preseal_evidence
# DITEMPA BUKAN DIBERI — Forged, not given
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARIFOS_DIR="${SCRIPT_DIR}/.."
EVIDENCE_DIR="${ARIFOS_DIR}/evidence"
COMPOSE_DIR="${ARIFOS_DIR}/../compose"
COMPOSE_FILE="${COMPOSE_DIR}/docker-compose.yml"
TIMESTAMP=$(date -u +%Y%m%d_%H%M%S)
EVIDENCE_FILE="${EVIDENCE_DIR}/preseal_evidence_${TIMESTAMP}.json"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

DRY_RUN="${DRY_RUN:-false}"
GIT_BRANCH="${GIT_BRANCH:-main}"
STATUS="PASS"
REASONS=()
RISK="LOW"
RECOMMENDATION="PROCEED"
HOLD_ISSUES=()

echo "=== PRESEAL EVIDENCE ==="
echo ""

# ── 1. Git commit info ────────────────────────────────────────────────────────
echo "[1] Git commit info..."
GIT_COMMIT=$(git -C "$ARIFOS_DIR" rev-parse HEAD 2>/dev/null || echo "unknown")
GIT_COMMIT_SHORT=$(git -C "$ARIFOS_DIR" rev-parse --short HEAD 2>/dev/null || echo "unknown")
GIT_BRANCH=$(git -C "$ARIFOS_DIR" branch --show-current 2>/dev/null || echo "unknown")
GIT_STATUS=$(git -C "$ARIFOS_DIR" status --porcelain 2>/dev/null | wc -l | xargs || echo "0")
GIT_LOG=$(git -C "$ARIFOS_DIR" log --oneline -5 2>/dev/null | head -5 || echo "unknown")
GIT_MESSAGE=$(git -C "$ARIFOS_DIR" log -1 --format='%s' 2>/dev/null || echo "unknown")
echo "  commit:      ${GIT_COMMIT_SHORT}"
echo "  branch:      ${GIT_BRANCH}"
echo "  uncommitted:  ${GIT_STATUS} files"
echo "  last msg:    ${GIT_MESSAGE}"
if [ "$GIT_STATUS" -gt 0 ]; then
    STATUS="HOLD"
    RECOMMENDATION="HOLD"
    HOLD_ISSUES+=("uncommitted_changes:${GIT_STATUS}")
    REASONS+=("uncommitted_files:${GIT_STATUS}")
    RISK="MEDIUM"
    echo "  [WARN] Uncommitted files — seal will not include these"
fi

# ── 2. Image digest ────────────────────────────────────────────────────────────
echo ""
echo "[2] Image digest..."
ARIFOS_RUNNING=$(docker ps --format '{{.Names}}' | grep '^arifosmcp$' | head -1 || echo "")
if [ -n "$ARIFOS_RUNNING" ]; then
    CURRENT_IMAGE=$(docker inspect "${ARIFOS_RUNNING}" --format '{{.Config.Image}}' 2>/dev/null | head -12 || echo "unknown")
    CURRENT_DIGEST=$(docker image inspect "${CURRENT_IMAGE}" --format '{{.ID}}' 2>/dev/null | head -12 || echo "unknown")
    echo "  running image:  ${CURRENT_IMAGE}"
    echo "  digest:        ${CURRENT_DIGEST}"
else
    CURRENT_IMAGE="none"
    CURRENT_DIGEST="none"
    echo "  [WARN] arifosmcp not running"
fi

# ── 3. Compose image reference vs running image ─────────────────────────────
echo ""
echo "[3] Compose image reference vs running image..."
COMPOSE_IMAGE=$(grep -A5 '^\s*arifosmcp:' "$COMPOSE_FILE" 2>/dev/null | grep '^\s*image:' | head -1 | awk '{print $2}' | tr -d ' "' || echo "none")
echo "  compose image: ${COMPOSE_IMAGE}"
echo "  running image: ${CURRENT_IMAGE}"
if [ "$COMPOSE_IMAGE" != "$CURRENT_IMAGE" ] && [ "$CURRENT_IMAGE" != "none" ]; then
    echo "  [INFO] Compose and running image differ — likely live mount"
fi

# ── 4. Runtime state from /health ────────────────────────────────────────────
echo ""
echo "[4] Runtime state from /health..."
if [ -n "$ARIFOS_RUNNING" ]; then
    HEALTH_RESP=$(curl -sf http://127.0.0.1:8080/health 2>/dev/null || echo "{}")
    TOOL_REGISTRY_HASH=$(echo "$HEALTH_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_registry_hash','unknown'))" 2>/dev/null || echo "unreachable")
    SCHEMA_HASH=$(echo "$HEALTH_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('schema_hash','unknown'))" 2>/dev/null || echo "unreachable")
    RUNTIME_DRIFT=$(echo "$HEALTH_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('runtime_drift','unknown'))" 2>/dev/null || echo "unknown")
    CONSTITUTION_HASH=$(echo "$HEALTH_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('constitution_hash','unknown'))" 2>/dev/null || echo "unknown")
    VERSION=$(echo "$HEALTH_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('version','unknown'))" 2>/dev/null || echo "unknown")
    STATUS_HEALTH=$(echo "$HEALTH_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','unknown'))" 2>/dev/null || echo "unknown")
    echo "  tool_registry_hash: ${TOOL_REGISTRY_HASH}"
    echo "  schema_hash:        ${SCHEMA_HASH}"
    echo "  runtime_drift:      ${RUNTIME_DRIFT}"
    echo "  constitution_hash:  ${CONSTITUTION_HASH}"
    echo "  version:            ${VERSION}"
    echo "  health_status:      ${STATUS_HEALTH}"
else
    TOOL_REGISTRY_HASH="not_running"
    SCHEMA_HASH="not_running"
    RUNTIME_DRIFT="unknown"
    CONSTITUTION_HASH="unknown"
    VERSION="unknown"
    STATUS_HEALTH="not_running"
fi

if [ "$RUNTIME_DRIFT" = "true" ]; then
    STATUS="HOLD"
    RECOMMENDATION="HOLD"
    HOLD_ISSUES+=("runtime_drift:true")
    REASONS+=("runtime_drift:true")
    RISK="MEDIUM"
    echo "  [HOLD] runtime_drift=true — local code diverges from image"
fi

if [ "$STATUS_HEALTH" != "healthy" ]; then
    STATUS="DEGRADED"
    RECOMMENDATION="HOLD"
    HOLD_ISSUES+=("health_not_healthy:${STATUS_HEALTH}")
    REASONS+=("health_not_healthy:${STATUS_HEALTH}")
    RISK="MEDIUM"
fi

# ── 5. MCP routes verification ───────────────────────────────────────────────
echo ""
echo "[5] MCP routes verification..."
CADDYFILE="${COMPOSE_DIR}/Caddyfile"
if [ -f "$CADDYFILE" ]; then
    MCP_ROUTE=$(grep 'reverse_proxy.*arifosmcp' "$CADDYFILE" 2>/dev/null | head -1 || echo "")
    MCP_ROUTE_COUNT=$(grep -c 'reverse_proxy.*arifosmcp' "$CADDYFILE" 2>/dev/null || echo 0)
    echo "  arifosmcp routes: ${MCP_ROUTE_COUNT}"
    if [ "$MCP_ROUTE_COUNT" -eq 0 ]; then
        STATUS="HOLD"
        RECOMMENDATION="HOLD"
        HOLD_ISSUES+=("no_arifmcp_route_in_caddy")
        REASONS+=("no_arifmcp_route_in_caddy")
        RISK="CRITICAL"
        echo "  [FAIL] No arifosmcp reverse_proxy in Caddyfile"
    else
        echo "  [OK] MCP route found"
    fi
else
    CADDYFILE="none"
    echo "  [WARN] Caddyfile not found"
fi

# ── 6. Vault999 health ─────────────────────────────────────────────────────────
echo ""
echo "[6] Vault999 health..."
VAULT_RUNNING=$(docker ps --format '{{.Names}}' | grep 'vault999' | head -1 || echo "")
if [ -n "$VAULT_RUNNING" ]; then
    VAULT_HEALTH=$(docker exec "$VAULT_RUNNING" curl -sf http://localhost:8100/health 2>/dev/null || echo "{}")
    VAULT_STATUS=$(echo "$VAULT_HEALTH" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','unknown'))" 2>/dev/null || echo "unreachable")
    VAULT_CHAIN_HEIGHT=$(echo "$VAULT_HEALTH" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('chain_height',0))" 2>/dev/null || echo 0)
    echo "  vault999 status:   ${VAULT_STATUS}"
    echo "  chain_height:      ${VAULT_CHAIN_HEIGHT}"
else
    VAULT_STATUS="not_running"
    VAULT_CHAIN_HEIGHT=0
fi

# ── 7. Langfuse trace presence ────────────────────────────────────────────────
echo ""
echo "[7] Langfuse trace presence..."
if [ -n "$ARIFOS_RUNNING" ]; then
    RECENT_SPANS=$(docker exec "$ARIFOS_RUNNING" find /var/lib/arifos/telemetry -name "*.jsonl" 2>/dev/null | head -5 || echo "")
    if [ -n "$RECENT_SPANS" ]; then
        echo "  [INFO] Local telemetry files present"
    fi
    LANGFUSE_KEYS_PRESENT=$(docker exec "$ARIFOS_RUNNING" python3 -c "import os; print('yes' if os.getenv('LANGFUSE_PUBLIC_KEY') else 'no')" 2>/dev/null || echo "unknown")
    echo "  LANGFUSE keys present in container: ${LANGFUSE_KEYS_PRESENT}"
else
    echo "  [WARN] arifosmcp not running — cannot check Langfuse"
fi

# ── 8. Tool registry sync check ──────────────────────────────────────────────
echo ""
echo "[8] Tool registry sync check..."
if [ -n "$ARIFOS_RUNNING" ]; then
    EXPECTED_TOOLS=13
    ACTUAL_TOOLS=$(docker exec "$ARIFOS_RUNNING" python3 -c "
from arifosmcp.constitutional_map import TOOL_REGISTRY
print(len(TOOL_REGISTRY))
" 2>/dev/null || echo "unknown")
    echo "  expected tools: ${EXPECTED_TOOLS}"
    echo "  actual tools:   ${ACTUAL_TOOLS}"
    if [ "$ACTUAL_TOOLS" != "unknown" ] && [ "$ACTUAL_TOOLS" -lt "$EXPECTED_TOOLS" ]; then
        STATUS="HOLD"
        RECOMMENDATION="HOLD"
        HOLD_ISSUES+=("tool_count_mismatch:${ACTUAL_TOOLS}")
        REASONS+=("tool_count_mismatch:${ACTUAL_TOOLS}")
        RISK="MEDIUM"
        echo "  [WARN] Tool count mismatch"
    fi
else
    echo "  [SKIP] arifosmcp not running"
fi

# ── 9. Evidence JSON assembly ────────────────────────────────────────────────
echo ""
echo "[9] Assembling evidence JSON..."

REASONS_JSON=$(printf '%s\n' "${REASONS[@]}" | jq -R . | jq -s . 2>/dev/null || echo '[]')
HOLD_JSON=$(printf '%s\n' "${HOLD_ISSUES[@]}" | jq -R . | jq -s . 2>/dev/null || echo '[]')

cat > "$EVIDENCE_FILE" << EOF
{
  "skill": "vps_preseal_evidence",
  "status": "${STATUS}",
  "timestamp_utc": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "recommendation": "${RECOMMENDATION}",
  "evidence": {
    "git": {
      "commit": "${GIT_COMMIT}",
      "commit_short": "${GIT_COMMIT_SHORT}",
      "branch": "${GIT_BRANCH}",
      "uncommitted_files": ${GIT_STATUS},
      "last_message": "${GIT_MESSAGE}",
      "log_5": "$(echo "$GIT_LOG" | tr '\n' '|' | sed 's/|/\\n/g')"
    },
    "image": {
      "current": "${CURRENT_IMAGE}",
      "digest": "${CURRENT_DIGEST}",
      "compose_ref": "${COMPOSE_IMAGE}"
    },
    "runtime": {
      "tool_registry_hash": "${TOOL_REGISTRY_HASH}",
      "schema_hash": "${SCHEMA_HASH}",
      "runtime_drift": "${RUNTIME_DRIFT}",
      "constitution_hash": "${CONSTITUTION_HASH}",
      "version": "${VERSION}",
      "health_status": "${STATUS_HEALTH}"
    },
    "vault999": {
      "status": "${VAULT_STATUS}",
      "chain_height": ${VAULT_CHAIN_HEIGHT}
    },
    "mcp": {
      "caddyfile_route_count": ${MCP_ROUTE_COUNT:-0},
      "caddyfile_found": "$( [ -f "$CADDYFILE" ] && echo "yes" || echo "no" )"
    },
    "tools": {
      "expected_count": ${EXPECTED_TOOLS:-13},
      "actual_count": "${ACTUAL_TOOLS:-unknown}"
    },
    "langfuse": {
      "keys_in_container": "${LANGFUSE_KEYS_PRESENT:-unknown}"
    }
  },
  "reasons": ${REASONS_JSON},
  "hold_issues": ${HOLD_JSON},
  "risk": "${RISK}",
  "seal_warrant": $(python3 -c "
import hashlib, json, datetime
payload = {
    'git_commit': '${GIT_COMMIT}',
    'image_digest': '${CURRENT_DIGEST}',
    'tool_registry_hash': '${TOOL_REGISTRY_HASH}',
    'schema_hash': '${SCHEMA_HASH}',
    'timestamp': '$(date -u +%Y-%m-%dT%H:%M:%SZ)'
}
h = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:16]
print(f'\"sha256:{h}\"')
" 2>/dev/null),
  "next_safe_action": "$(if [ "$RECOMMENDATION" = "HOLD" ]; then echo "resolve_holds_then_recheck"; elif [ "$RECOMMENDATION" = "PROCEED" ]; then echo "invoke_arif_judge_deliberate_then_seal"; else echo "inspect_evidence"; fi)"
}
EOF

echo "  Evidence written: ${EVIDENCE_FILE}"

# ── Final report ──────────────────────────────────────────────────────────────
echo ""
echo "=== PRESEAL EVIDENCE REPORT ==="
echo "status:        ${STATUS}"
echo "recommendation: ${RECOMMENDATION}"
echo "risk:          ${RISK}"
echo "git_commit:    ${GIT_COMMIT_SHORT}"
echo "image_digest:  ${CURRENT_DIGEST}"
echo "tool_hash:    ${TOOL_REGISTRY_HASH}"
echo "schema_hash:  ${SCHEMA_HASH}"
echo "runtime_drift: ${RUNTIME_DRIFT}"
echo "vault999:     ${VAULT_STATUS} (chain: ${VAULT_CHAIN_HEIGHT})"
echo "health:       ${STATUS_HEALTH}"
if [ ${#HOLD_ISSUES[@]} -gt 0 ]; then
    echo "hold_issues:"
    for h in "${HOLD_ISSUES[@]}"; do
        echo "  - $h"
    done
fi
if [ ${#REASONS[@]} -gt 0 ]; then
    echo "reasons:"
    for r in "${REASONS[@]}"; do
        echo "  - $r"
    done
fi

echo ""
echo "next_safe_action: $(if [ "$RECOMMENDATION" = "HOLD" ]; then echo "resolve_holds_then_recheck"; elif [ "$RECOMMENDATION" = "PROCEED" ]; then echo "invoke_arif_judge_deliberate_then_seal"; else echo "inspect_evidence"; fi)"
echo ""
echo "evidence:  ${EVIDENCE_FILE}"
echo "=== END PRESEAL ==="

[ "$STATUS" = "PASS" ] || [ "$RECOMMENDATION" = "PROCEED" ]