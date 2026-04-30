#!/bin/bash
# predeploy_audit.sh — Pre-deploy validation of compose, docker, healthchecks, security
# Skill: vps_compose_guardian
# DITEMPA BUKAN DIBERI
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARIFOS_DIR="${SCRIPT_DIR}/.."
EVIDENCE_DIR="${ARIFOS_DIR}/evidence"
COMPOSE_DIR="${ARIFOS_DIR}/../compose"
TIMESTAMP=$(date -u +%Y%m%d_%H%M%S)
EVIDENCE_FILE="${EVIDENCE_DIR}/predeploy_audit_${TIMESTAMP}.json"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

STATUS="PASS"
REASONS=()
RISK="LOW"
HOLD_ISSUES=()

echo "=== PREDEPLOY AUDIT ==="
echo "arifOS dir:   ${ARIFOS_DIR}"
echo "compose dir:  ${COMPOSE_DIR}"
echo ""

# ── 1. Compose file existence ────────────────────────────────────────────────
COMPOSE_FILE="${COMPOSE_DIR}/docker-compose.yml"
if [ ! -f "$COMPOSE_FILE" ]; then
    STATUS="FAIL"
    REASONS+=("compose_file_missing:${COMPOSE_FILE}")
    RISK="CRITICAL"
    echo "[FAIL] docker-compose.yml not found"
else
    echo "[OK] docker-compose.yml found"
fi

# ── 2. Compose config validation ──────────────────────────────────────────────
if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
    if ! docker compose -f "$COMPOSE_FILE" config > "$TMP_DIR/compose_config.out" 2>&1; then
        STATUS="FAIL"
        REASONS+=("compose_config_invalid")
        RISK="CRITICAL"
        echo "[FAIL] docker compose config validation failed:"
        cat "$TMP_DIR/compose_config.out" | head -5
    else
        echo "[OK] docker compose config valid"
    fi
else
    echo "[WARN] docker not available for compose validation"
fi

# ── 3. Critical services healthcheck presence ─────────────────────────────────
CRITICAL_SVCS="arifosmcp postgres vault999-writer redis qdrant caddy"
MISSING_HC=()
for svc in $CRITICAL_SVCS; do
    if grep -q "^\s*${svc}:" "$COMPOSE_FILE" 2>/dev/null; then
        HAS_HC=$(grep -A20 "^\s*${svc}:" "$COMPOSE_FILE" 2>/dev/null | grep -c "healthcheck:" || echo 0)
        if [ "$HAS_HC" -gt 0 ]; then
            echo "[OK] ${svc}: has healthcheck"
        else
            MISSING_HC+=("${svc}_no_healthcheck")
            echo "[WARN] ${svc}: missing healthcheck"
        fi
    fi
done
if [ ${#MISSING_HC[@]} -gt 0 ]; then
    STATUS="HOLD"
    REASONS+=("${MISSING_HC[*]}")
    RISK="MEDIUM"
fi

# ── 4. Public port exposure check ─────────────────────────────────────────────
DANGEROUS_PORTS=$(grep -E '^\s*-\s+"(127\.0\.0\.1)?:5432' "$COMPOSE_FILE" 2>/dev/null || true)
if [ -n "$DANGEROUS_PORTS" ]; then
    STATUS="FAIL"
    REASONS+=("public_postgres_exposed")
    RISK="CRITICAL"
    echo "[FAIL] Postgres exposed on public interface:"
    echo "$DANGEROUS_PORTS"
else
    echo "[OK] No dangerous port exposures found"
fi

# ── 5. Image tag vs digest check ─────────────────────────────────────────────
ARIFOS_SVC=$(grep -A15 '^\s*arifosmcp:' "$COMPOSE_FILE" 2>/dev/null | grep '^\s*image:' | head -1 || echo "")
echo "arifosmcp image: ${ARIFOS_SVC:-none}"
if echo "$ARIFOS_SVC" | grep -q '@sha256:'; then
    echo "[OK] arifosmcp uses digest pinned image"
elif echo "$ARIFOS_SVC" | grep -q ':latest'; then
    STATUS="HOLD"
    REASONS+=("arifosmcp_uses_latest_tag")
    RISK="MEDIUM"
    echo "[WARN] arifosmcp uses :latest tag (not digest-pinned)"
else
    echo "[INFO] arifosmcp uses custom tag"
fi

# ── 6. Live mount check ─────────────────────────────────────────────────────
HAS_LIVE_MOUNT=$(grep -A30 '^\s*arifosmcp:' "$COMPOSE_FILE" 2>/dev/null | grep '/root/arifOS:/app' || echo "")
if [ -n "$HAS_LIVE_MOUNT" ]; then
    STATUS="HOLD"
    REASONS+=("arifosmcp_has_live_mount")
    RISK="MEDIUM"
    echo "[WARN] arifosmcp has live mount /root/arifOS:/app (causes runtime_drift=true)"
else
    echo "[OK] No live mount detected in arifosmcp service"
fi

# ── 7. Environment file check ─────────────────────────────────────────────────
ENV_FILE=$(grep '^\s*env_file:' "$COMPOSE_FILE" 2>/dev/null | head -1 || echo "")
if [ -n "$ENV_FILE" ]; then
    ENV_PATH=$(echo "$ENV_FILE" | awk '{print $2}' | tr -d ' ')
    if [ -f "${COMPOSE_DIR}/${ENV_PATH}" ] || [ -f "$ENV_PATH" ]; then
        echo "[OK] env_file exists: ${ENV_PATH}"
    else
        STATUS="HOLD"
        REASONS+=("env_file_missing:${ENV_PATH}")
        RISK="MEDIUM"
        echo "[WARN] env_file declared but not found: ${ENV_PATH}"
    fi
fi

# ── 8. Network configuration ──────────────────────────────────────────────────
NETWORKS=$(grep -E '^\s*networks:' "$COMPOSE_FILE" 2>/dev/null | wc -l || echo 0)
echo "[OK] ${NETWORKS} network definitions found"
if grep -q 'external: true' "$COMPOSE_FILE" 2>/dev/null; then
    echo "[INFO] Compose uses external networks"
fi

# ── 9. Tool registry hash from health ────────────────────────────────────────
ARIFOS_RUNNING=$(docker ps --format '{{.Names}}' 2>/dev/null | grep '^arifosmcp$' || echo "")
if [ -n "$ARIFOS_RUNNING" ]; then
    HEALTH=$(docker exec "$ARIFOS_RUNNING" curl -sf http://localhost:8080/health 2>/dev/null || echo "{}")
    TOOL_HASH=$(echo "$HEALTH" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_registry_hash','unknown'))" 2>/dev/null || echo "unavailable")
    SCHEMA_HASH=$(echo "$HEALTH" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('schema_hash','unknown'))" 2>/dev/null || echo "unavailable")
    RUNTIME_DRIFT=$(echo "$HEALTH" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('runtime_drift','unknown'))" 2>/dev/null || echo "unavailable")
    echo ""
    echo "Runtime state:"
    echo "  tool_registry_hash: ${TOOL_HASH}"
    echo "  schema_hash:       ${SCHEMA_HASH}"
    echo "  runtime_drift:    ${RUNTIME_DRIFT}"
    if [ "$RUNTIME_DRIFT" = "true" ]; then
        STATUS="HOLD"
        REASONS+=("runtime_drift:true")
        RISK="MEDIUM"
        echo "  [WARN] runtime_drift=true (local code diverges from image)"
    fi
else
    echo "[INFO] arifosmcp not running — cannot probe runtime state"
fi

# ── 10. Vault999 health check ─────────────────────────────────────────────────
VAULT_RUNNING=$(docker ps --format '{{.Names}}' 2>/dev/null | grep 'vault999$' || echo "")
if [ -n "$VAULT_RUNNING" ]; then
    VAULT_HEALTH=$(docker exec "$VAULT_RUNNING" curl -sf http://localhost:8100/health 2>/dev/null || echo "{}")
    VAULT_STATUS=$(echo "$VAULT_HEALTH" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','unknown'))" 2>/dev/null || echo "unreachable")
    echo ""
    echo "Vault999 health: ${VAULT_STATUS}"
    if [ "$VAULT_STATUS" != "healthy" ]; then
        STATUS="HOLD"
        REASONS+=("vault999_unhealthy:${VAULT_STATUS}")
        RISK="MEDIUM"
    fi
fi

# ── 11. Caddy routes check ───────────────────────────────────────────────────
CADDYFILE="${COMPOSE_DIR}/Caddyfile"
if [ -f "$CADDYFILE" ]; then
    HAS_ARIF_MCP=$(grep -c 'reverse_proxy.*arifosmcp' "$CADDYFILE" 2>/dev/null || echo 0)
    HAS_LANGFUSE=$(grep -c 'reverse_proxy.*langfuse' "$CADDYFILE" 2>/dev/null || echo 0)
    echo ""
    echo "Caddyfile routes:"
    echo "  arifosmcp reverse_proxies: ${HAS_ARIF_MCP}"
    echo "  langfuse reverse_proxies:  ${HAS_LANGFUSE}"
fi

# ── Print report ──────────────────────────────────────────────────────────────
echo ""
echo "=== PREDEPLOY AUDIT REPORT ==="
echo "status:  ${STATUS}"
echo "risk:    ${RISK}"
if [ ${#REASONS[@]} -gt 0 ]; then
    echo "reasons:"
    for r in "${REASONS[@]}"; do
        echo "  - $r"
    done
fi

# ── Write evidence JSON ──────────────────────────────────────────────────────
REASONS_JSON=$(printf '%s\n' "${REASONS[@]}" | jq -R . | jq -s . 2>/dev/null || echo '[]')

cat > "$EVIDENCE_FILE" << EOF
{
  "skill": "vps_compose_guardian",
  "status": "${STATUS}",
  "timestamp_utc": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "evidence": {
    "compose_valid": $(docker compose -f "$COMPOSE_FILE" config >/dev/null 2>&1 && echo "true" || echo "false"),
    "compose_file": "${COMPOSE_FILE}",
    "missing_healthchecks": $(printf '%s\n' "${MISSING_HC[@]:-[]}" | jq -R . | jq -s . 2>/dev/null || echo '[]'),
    "arifosmcp_image_line": "${ARIFOS_SVC:-none}",
    "arifosmcp_live_mount": $([ -n "$HAS_LIVE_MOUNT" ] && echo "true" || echo "false"),
    "tool_registry_hash": "${TOOL_HASH:-unknown}",
    "schema_hash": "${SCHEMA_HASH:-unknown}",
    "runtime_drift": "${RUNTIME_DRIFT:-unknown}",
    "vault999_status": "${VAULT_STATUS:-not_checked}",
    "docker_ps_count": $(docker ps -a 2>/dev/null | wc -l || echo 0)
  },
  "reasons": ${REASONS_JSON},
  "risk": "${RISK}",
  "next_safe_action": "$(if [ "$STATUS" = "FAIL" ]; then echo "fix_critical_issues_first"; elif [ "$STATUS" = "HOLD" ]; then echo "resolve_holds_before_deploy"; else echo "proceed_to_deploy"; fi)",
  "requires_arif": $([ "$STATUS" != "PASS" ] && echo 'true' || echo 'false')
}
EOF

echo ""
echo "evidence:  ${EVIDENCE_FILE}"
echo "=== END PREDEPLOY AUDIT ==="

[ "$STATUS" != "FAIL" ]
