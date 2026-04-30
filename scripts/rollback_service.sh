#!/bin/bash
# rollback_service.sh — Bounded rollback with ARIF confirmation gate for irreversible targets
# Skill: vps_rollback_guardian
# DITEMPA BUKAN DIBERI — Forged, not given
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARIFOS_DIR="${SCRIPT_DIR}/.."
EVIDENCE_DIR="${ARIFOS_DIR}/evidence"
COMPOSE_DIR="${ARIFOS_DIR}/../compose"
COMPOSE_FILE="${COMPOSE_DIR}/docker-compose.yml"
TIMESTAMP=$(date -u +%Y%m%d_%H%M%S)
EVIDENCE_FILE="${EVIDENCE_DIR}/rollback_${TIMESTAMP}.json"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

DRY_RUN="${DRY_RUN:-false}"
SERVICE="${SERVICE:-arifosmcp}"
TARGET_IMAGE="${TARGET_IMAGE:-}"
STATUS="PASS"
REASONS=()
RISK="LOW"
HOLD_ISSUES=()

usage() {
    cat << USAGE
Usage: $0 [OPTIONS]

Options:
  --dry-run              Show what would be done, do not execute
  --service NAME         Service to rollback [default: arifosmcp]
  --target-image DIGEST  Image digest or tag to rollback to [required]
  --skip-health          Skip post-rollback health check

Requires ARIF explicit confirmation for:
  - postgres service rollback
  - vault999 service rollback
  - Any service with --ack-irreversible=false

USAGE
    exit 1
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run) DRY_RUN=true; shift ;;
        --service) SERVICE="$2"; shift 2 ;;
        --target-image) TARGET_IMAGE="$2"; shift 2 ;;
        --skip-health) SKIP_HEALTH=true; shift ;;
        -h|--help) usage ;;
        *) echo "Unknown option: $1"; usage ;;
    esac
done

if [ -z "$TARGET_IMAGE" ]; then
    echo "[FAIL] --target-image is required"
    usage
fi

echo "=== ROLLBACK SERVICE ==="
echo "service:       ${SERVICE}"
echo "target_image:  ${TARGET_IMAGE}"
echo "dry_run:       ${DRY_RUN}"
echo ""

# ── Irreversible service gate ─────────────────────────────────────────────────
IRREVERSIBLE_SVCS="postgres vault999 vault postgresdb"
if echo "$IRREVERSIBLE_SVCS" | grep -qw "$SERVICE"; then
    echo "[HOLD] ${SERVICE} is an irreversible target."
    echo "       Postgres/Vault data loss risk."
    echo ""
    echo "ARIF confirmation required. Options:"
    echo "  1) Abort — safest, preserves data"
    echo "  2) Proceed with explicit --ack-irreversible"
    echo ""
    read -rp "Choice [1]: " CHOICE
    CHOICE="${CHOICE:-1}"
    if [ "$CHOICE" != "2" ]; then
        echo "[ABORT] Rollback cancelled for ${SERVICE}"
        STATUS="ABORTED"
        REASONS+=("user_aborted_irreversible_target")
        RISK="LOW"
        echo "evidence: ${EVIDENCE_FILE}"
        exit 0
    fi
    echo "[ACK] Proceeding with irreversible rollback of ${SERVICE}"
fi

# ── Pre-flight ────────────────────────────────────────────────────────────────
if ! command -v docker >/dev/null 2>&1; then
    echo "[FAIL] docker not available"
    exit 1
fi

# ── 1. Capture current state ─────────────────────────────────────────────────
echo "[1] Capturing current state..."
CURRENT_CONTAINER=$(docker ps --format '{{.Names}}' | grep "^${SERVICE}$" | head -1 || echo "")
CURRENT_IMAGE=$(docker inspect "${SERVICE}" --format '{{.Image}}' 2>/dev/null | head -12 || echo "unknown")
CURRENT_DIGEST=$(docker inspect "${SERVICE}" --format '{{.Config.Image}}' 2>/dev/null | head -12 || echo "unknown")
echo "  current container: ${CURRENT_CONTAINER:-none}"
echo "  current image:     ${CURRENT_IMAGE:-unknown}"
echo "  current digest:    ${CURRENT_DIGEST:-unknown}"
echo "  target image:      ${TARGET_IMAGE}"

# ── 2. Validate target image exists ─────────────────────────────────────────
echo ""
echo "[2] Validating target image..."
if docker image inspect "${TARGET_IMAGE}" >/dev/null 2>&1; then
    TARGET_DIGEST=$(docker image inspect "${TARGET_IMAGE}" --format '{{.ID}}' 2>/dev/null | head -12)
    echo "  Target image: OK (${TARGET_DIGEST})"
else
    echo "[FAIL] Target image ${TARGET_IMAGE} not found locally"
    STATUS="FAIL"
    REASONS+=("target_image_not_found:${TARGET_IMAGE}")
    echo "evidence: ${EVIDENCE_FILE}"
    exit 1
fi

# ── 3. Detect if rollback would introduce runtime_drift ────────────────────
echo ""
echo "[3] Runtime drift check..."
if [ -f "${ARIFOS_DIR}/arifosmcp/runtime/kernel_runtime.py" ]; then
    LOCAL_GIT_SHA=$(cd "$ARIFOS_DIR" && git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    CONTAINER_GIT_SHA=$(docker exec "${CURRENT_CONTAINER}" git -C /app rev-parse --short HEAD 2>/dev/null || echo "unknown")
    echo "  local git SHA:  ${LOCAL_GIT_SHA}"
    echo "  container SHA:  ${CONTAINER_GIT_SHA}"
    if [ "$LOCAL_GIT_SHA" != "$CONTAINER_GIT_SHA" ] && [ "$LOCAL_GIT_SHA" != "unknown" ]; then
        echo "  [INFO] Drift: local code diverges from running container"
        RUNTIME_DRIFT="true"
    else
        RUNTIME_DRIFT="false"
    fi
else
    RUNTIME_DRIFT="unknown"
fi

# ── 4. Determine compose config for service ─────────────────────────────────
echo ""
echo "[4] Compose service mapping..."
COMPOSE_SERVICE_LINE=$(grep -n "^\s*${SERVICE}:" "$COMPOSE_FILE" 2>/dev/null | head -1 || echo "")
if [ -n "$COMPOSE_SERVICE_LINE" ]; then
    LINE_NUM=$(echo "$COMPOSE_SERVICE_LINE" | cut -d: -f1)
    echo "  ${SERVICE} found at line ${LINE_NUM} in compose file"
    COMPOSE_IMAGE_LINE=$((LINE_NUM + 1))
    COMPOSE_IMAGE=$(sed -n "${COMPOSE_IMAGE_LINE}p" "$COMPOSE_FILE" 2>/dev/null | awk '{print $2}' | tr -d ' "' || echo "none")
    echo "  compose image: ${COMPOSE_IMAGE}"
else
    echo "  [WARN] ${SERVICE} not found in compose file — standalone container?"
    COMPOSE_IMAGE="none"
fi

# ── 5. Rollback execution ────────────────────────────────────────────────────
if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "[SKIP] Rollback execution (dry-run mode)"
    echo "  Would stop container: ${CURRENT_CONTAINER}"
    echo "  Would tag: ${TARGET_IMAGE} → current (for compose)"
    echo "  Would start: ${SERVICE} with image ${TARGET_IMAGE}"
else
    echo ""
    echo "[5] Executing rollback..."
    # Stop current container
    if [ -n "$CURRENT_CONTAINER" ]; then
        docker stop "${CURRENT_CONTAINER}" 2>/dev/null || true
        docker rm -f "${CURRENT_CONTAINER}" 2>/dev/null || true
        echo "  Stopped: ${CURRENT_CONTAINER}"
    fi

    # Tag target as current
    docker tag "${TARGET_IMAGE}" "${SERVICE}:rollback" 2>/dev/null || true

    # Get restart policy from compose or default
    RESTART_POLICY=$(grep -A10 "^\s*${SERVICE}:" "$COMPOSE_FILE" 2>/dev/null | grep 'restart:' | head -1 | awk '{print $2}' | tr -d ' "' || echo "unless-stopped")

    # Determine port mapping
    case "$SERVICE" in
        arifosmcp)
            PORT_MAP="127.0.0.1:8080:8080"
            ENV_FILE="${ARIFOS_DIR}/../.env"
            ;;
        postgres)
            PORT_MAP="127.0.0.1:5432:5432"
            ENV_FILE=""
            ;;
        redis)
            PORT_MAP="127.0.0.1:6379:6379"
            ENV_FILE=""
            ;;
        *)
            PORT_MAP=""
            ENV_FILE=""
            ;;
    esac

    # Build docker run command
    RUN_CMD="docker run -d --name ${SERVICE} --restart ${RESTART_POLICY}"
    if [ -n "$PORT_MAP" ]; then
        RUN_CMD="${RUN_CMD} -p ${PORT_MAP}"
    fi
    if [ -n "$ENV_FILE" ] && [ -f "$ENV_FILE" ]; then
        RUN_CMD="${RUN_CMD} --env-file ${ENV_FILE}"
    fi
    RUN_CMD="${RUN_CMD} --network arifos_core_network ${TARGET_IMAGE}"

    echo "  Running: ${RUN_CMD}"
    ${RUN_CMD}
    echo "  Started: ${SERVICE}"
    sleep 5
fi

# ── 6. Post-rollback health check ──────────────────────────────────────────
if [ "${SKIP_HEALTH:-false}" = true ]; then
    echo ""
    echo "[SKIP] Health check (--skip-health)"
else
    echo ""
    echo "[6] Post-rollback health check..."
    case "$SERVICE" in
        arifosmcp)
            HEALTH_RESP=$(curl -sf http://127.0.0.1:8080/health 2>/dev/null || echo "{}")
            HEALTH_STATUS=$(echo "$HEALTH_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','FAIL'))" 2>/dev/null || echo "unreachable")
            ;;
        postgres)
            HEALTH_STATUS=$(docker exec "${SERVICE}" pg_isready 2>/dev/null && echo "healthy" || echo "unhealthy")
            ;;
        redis)
            HEALTH_STATUS=$(docker exec "${SERVICE}" redis-cli ping 2>/dev/null | grep -q PONG && echo "healthy" || echo "unhealthy")
            ;;
        *)
            HEALTH_STATUS="unknown"
            ;;
    esac

    echo "  Health: ${HEALTH_STATUS}"
    if [ "$HEALTH_STATUS" != "healthy" ]; then
        STATUS="DEGRADED"
        REASONS+=("health_check_failed_after_rollback:${HEALTH_STATUS}")
        RISK="MEDIUM"
        echo "[WARN] Health check did not return healthy"
    fi
fi

# ── 7. Runtime drift verification ────────────────────────────────────────────
echo ""
echo "[7] Verifying runtime drift..."
NEW_DIGEST=$(docker inspect "${SERVICE}" --format '{{.Config.Image}}' 2>/dev/null | head -12 || echo "unknown")
NEW_GIT_SHA=$(docker exec "${SERVICE}" git -C /app rev-parse --short HEAD 2>/dev/null || echo "unknown")
echo "  new image digest: ${NEW_DIGEST}"
echo "  new git SHA:      ${NEW_GIT_SHA}"
if [ "$LOCAL_GIT_SHA" != "unknown" ] && [ "$LOCAL_GIT_SHA" != "$NEW_GIT_SHA" ]; then
    echo "  [INFO] runtime_drift: local (${LOCAL_GIT_SHA}) ≠ container (${NEW_GIT_SHA})"
    NEW_RUNTIME_DRIFT="true"
else
    NEW_RUNTIME_DRIFT="false"
fi

# ── Final report ──────────────────────────────────────────────────────────────
echo ""
echo "=== ROLLBACK REPORT ==="
echo "status:        ${STATUS}"
echo "risk:          ${RISK}"
echo "service:       ${SERVICE}"
echo "prev_digest:   ${CURRENT_DIGEST}"
echo "target_digest: ${TARGET_DIGEST}"
echo "new_digest:    ${NEW_DIGEST}"
echo "runtime_drift: ${NEW_RUNTIME_DRIFT}"
[ ${#REASONS[@]} -gt 0 ] && echo "reasons:" && for r in "${REASONS[@]}"; do echo "  - $r"; done

REASONS_JSON=$(printf '%s\n' "${REASONS[@]}" | jq -R . | jq -s . 2>/dev/null || echo '[]')
cat > "$EVIDENCE_FILE" << EOF
{
  "skill": "vps_rollback_guardian",
  "status": "${STATUS}",
  "timestamp_utc": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "evidence": {
    "service": "${SERVICE}",
    "prev_digest": "${CURRENT_DIGEST}",
    "target_digest": "${TARGET_DIGEST}",
    "new_digest": "${NEW_DIGEST}",
    "runtime_drift_after": "${NEW_RUNTIME_DRIFT}",
    "local_git_sha": "${LOCAL_GIT_SHA}",
    "container_git_sha": "${NEW_GIT_SHA}",
    "dry_run": ${DRY_RUN},
    "health_check": "${HEALTH_STATUS:-not_run}"
  },
  "reasons": ${REASONS_JSON},
  "risk": "${RISK}",
  "next_safe_action": "$(if [ "$STATUS" = "FAIL" ]; then echo "inspect_evidence_fix_issue"; elif [ "$STATUS" = "DEGRADED" ]; then echo "resolve_health_check_then_seal"; else echo "run_predeploy_audit"; fi)",
  "requires_arif": $([ "$STATUS" != "PASS" ] && echo 'true' || echo 'false')
}
EOF

echo ""
echo "evidence:  ${EVIDENCE_FILE}"
echo "=== END ROLLBACK ==="

[ "$STATUS" = "PASS" ] || [ "$STATUS" = "ABORTED" ]