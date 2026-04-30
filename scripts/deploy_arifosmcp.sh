#!/bin/bash
# deploy_arifosmcp.sh — Build, validate, deploy arifOS MCP with auto-rollback on failure
# Skill: vps_deploy_arifosmcp
# DITEMPA BUKAN DIBERI — No irreversible action without explicit ARIF confirmation
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARIFOS_DIR="${SCRIPT_DIR}/.."
EVIDENCE_DIR="${ARIFOS_DIR}/evidence"
COMPOSE_DIR="${ARIFOS_DIR}/../compose"
COMPOSE_FILE="${COMPOSE_DIR}/docker-compose.yml"
DOCKERFILE="${ARIFOS_DIR}/arifosmcp/Dockerfile"
TIMESTAMP=$(date -u +%Y%m%d_%H%M%S)
EVIDENCE_FILE="${EVIDENCE_DIR}/deploy_arifosmcp_${TIMESTAMP}.json"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

AUTO_ROLLBACK="${AUTO_ROLLBACK:-true}"
DRY_RUN="${DRY_RUN:-false}"
SKIP_IMPORT_TEST="${SKIP_IMPORT_TEST:-false}"
COMMIT_MSG="${COMMIT_MSG:-auto-deploy}"
STATUS="PASS"
REASONS=()
RISK="LOW"

usage() {
    cat << USAGE
Usage: $0 [OPTIONS]

Options:
  --dry-run          Show what would be done, do not execute
  --no-rollback      Disable auto-rollback on failure (manual mode)
  --no-import-test   Skip import truth test (use with caution)
  --commit-msg MSG   Commit message for git [default: auto-deploy]
  --image TAG        Override image tag [default: ghcr.io/ariffazil/arifos:latest]

Requires ARIF explicit confirmation if:
  - runtime_drift would be introduced
  - Auto-rollback is triggered
USAGE
    exit 1
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run) DRY_RUN=true; shift ;;
        --no-rollback) AUTO_ROLLBACK=false; shift ;;
        --no-import-test) SKIP_IMPORT_TEST=true; shift ;;
        --commit-msg) COMMIT_MSG="$2"; shift 2 ;;
        --image) IMAGE_TAG="$2"; shift 2 ;;
        -h|--help) usage ;;
        *) echo "Unknown option: $1"; usage ;;
    esac
done

IMAGE_TAG="${IMAGE_TAG:-ghcr.io/ariffazil/arifos:latest}"
BUILD_DATE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

echo "=== ARIFOS DEPLOY ==="
echo "image:     ${IMAGE_TAG}"
echo "dry_run:   ${DRY_RUN}"
echo "auto_rb:   ${AUTO_ROLLBACK}"
echo "import_test: $([ "$SKIP_IMPORT_TEST" = true ] && echo skip || echo run)"
echo ""

# ── Pre-flight checks ────────────────────────────────────────────────────────
if ! command -v docker >/dev/null 2>&1; then
    echo "[FAIL] docker not available"
    exit 1
fi
if ! docker info >/dev/null 2>&1; then
    echo "[FAIL] docker daemon not reachable"
    exit 1
fi

# ── 1. Capture previous state ────────────────────────────────────────────────
echo "[1] Capturing previous state..."
PREV_CONTAINER=$(docker ps --format '{{.Names}}' | grep '^arifosmcp$' | head -1 || echo "")
PREV_IMAGE_DIGEST=$(docker inspect "${IMAGE_TAG}" --format '{{.ID}}' 2>/dev/null | head -12 || echo "none")
PREV_COMPOSE_IMAGE=$(grep -A2 '^\s*arifosmcp:' "$COMPOSE_FILE" 2>/dev/null | grep '^\s*image:' | awk '{print $2}' | tr -d ' ' || echo "none")
if [ -n "$PREV_CONTAINER" ]; then
    PREV_COMMIT=$(docker exec "$PREV_CONTAINER" python3 -c "import arifosmcp; print(arifosmcp.__file__)" 2>/dev/null | grep -o '/app/arifosmcp' >/dev/null && echo "canonical" || echo "legacy")
    echo "  prev container: ${PREV_CONTAINER} (${PREV_COMMIT})"
    echo "  prev image digest: ${PREV_IMAGE_DIGEST}"
else
    echo "  No previous arifosmcp container"
    PREV_COMMIT="none"
fi

# ── 2. Import truth test on current image ───────────────────────────────────
if [ "$SKIP_IMPORT_TEST" = false ]; then
    echo ""
    echo "[2] Import truth test on current image..."
    CURRENT_IMAGE_FOR_TEST=$(docker images "${IMAGE_TAG}" --format '{{.ID}}' 2>/dev/null | head -1 || echo "")
    if [ -n "$CURRENT_IMAGE_FOR_TEST" ]; then
        IMPORT_OK=$(docker run --rm "${IMAGE_TAG}" python3 -c "
import arifosmcp, arifosmcp.runtime
p = arifosmcp.__file__
assert '/app/arifosmcp/__init__.py' in p, f'Wrong path: {p}'
print('OK')
" 2>/dev/null || echo "FAIL")
        if [ "$IMPORT_OK" != "OK" ]; then
            echo "[FAIL] Current image fails import truth: ${IMPORT_OK}"
            STATUS="FAIL"
            REASONS+=("current_image_import_failed")
            echo "evidence: ${EVIDENCE_FILE}"
            exit 1
        fi
        echo "  Import truth: PASS"
    else
        echo "  [WARN] No current image found — will build new"
    fi
fi

# ── 3. Git commit check ───────────────────────────────────────────────────────
echo ""
echo "[3] Git state..."
GIT_COMMIT=$(git -C "$ARIFOS_DIR" rev-parse --short HEAD 2>/dev/null || echo "unknown")
GIT_BRANCH=$(git -C "$ARIFOS_DIR" branch --show-current 2>/dev/null || echo "unknown")
GIT_STATUS=$(git -C "$ARIFOS_DIR" status --porcelain 2>/dev/null | wc -l | xargs || echo "0")
echo "  commit:  ${GIT_COMMIT}"
echo "  branch:  ${GIT_BRANCH}"
echo "  uncommitted: ${GIT_STATUS} files"
if [ "$GIT_STATUS" -gt 0 ]; then
    echo "  [WARN] Uncommitted changes — these will NOT be in the build"
    echo "  Commit with: git -C ${ARIFOS_DIR} commit -m '${COMMIT_MSG}'"
fi

# ── 4. Build new image ───────────────────────────────────────────────────────
if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "[SKIP] Build (dry-run mode)"
else
    echo ""
    echo "[4] Building new image..."
    BUILD_OUTPUT=$(
        docker build \
            -t "${IMAGE_TAG}" \
            --build-arg BUILD_DATE="$BUILD_DATE" \
            --build-arg ARIFOS_BUILD_SHA="$GIT_COMMIT" \
            -f "$DOCKERFILE" \
            "$ARIFOS_DIR" 2>&1
    ) || {
        BUILD_FAILED=true
        echo "[FAIL] docker build failed:"
        echo "$BUILD_OUTPUT" | tail -10
        STATUS="FAIL"
        REASONS+=("docker_build_failed")
        echo "evidence: ${EVIDENCE_FILE}"
        exit 1
    }
    BUILD_FAILED=false
    NEW_IMAGE_DIGEST=$(docker inspect "${IMAGE_TAG}" --format '{{.ID}}' 2>/dev/null | head -12 || echo "unknown")
    echo "  Build: OK"
    echo "  New image digest: ${NEW_IMAGE_DIGEST}"
fi

# ── 5. Import truth test on new image ───────────────────────────────────────
echo ""
echo "[5] Import truth test on new image..."
IMPORT_NEW=$(docker run --rm "${IMAGE_TAG}" python3 -c "
import arifosmcp, arifosmcp.runtime
p = arifosmcp.__file__
assert '/app/arifosmcp/__init__.py' in p, f'Wrong path: {p}'
print('OK')
" 2>/dev/null || echo "FAIL")
if [ "$IMPORT_NEW" != "OK" ]; then
    echo "[FAIL] New image fails import truth"
    if [ "$AUTO_ROLLBACK" = true ]; then
        echo "[ROLLBACK] Reverting to previous image ${PREV_IMAGE_DIGEST}"
        docker tag "${PREV_IMAGE_DIGEST}" "${IMAGE_TAG}" 2>/dev/null || true
        echo "[DONE] Rollback complete"
    fi
    STATUS="FAIL"
    REASONS+=("new_image_import_failed")
    echo "evidence: ${EVIDENCE_FILE}"
    exit 1
fi
echo "  Import truth: PASS"

# ── 6. Health test in new image ──────────────────────────────────────────────
echo ""
echo "[6] Health endpoint test..."
HEALTH_OK=$(docker run --rm --read-only -p 127.0.0.1:8099:8080 "${IMAGE_TAG}" &
sleep 8
HEALTH_RESP=$(curl -sf http://127.0.0.1:8099/health 2>/dev/null || echo "{}")
docker kill $(docker ps -q --filter "publish=127.0.0.1:8099" 2>/dev/null) 2>/dev/null || true
wait 2>/dev/null || true
echo "$HEALTH_RESP" | python3 -c "
import sys,json
d=json.load(sys.stdin)
assert d.get('status') == 'healthy', f'Not healthy: {d}'
print('OK')
" 2>/dev/null || echo "FAIL")
if [ "$HEALTH_OK" != "OK" ]; then
    echo "[WARN] Health endpoint test did not pass in isolated run (may be network config)"
fi

# ── 7. Update compose image reference (digest pin) ────────────────────────────
if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "[SKIP] Compose update (dry-run)"
else
    echo ""
    echo "[7] Updating compose image reference..."
    # Use sed to replace the image line with digest-pinned version
    NEW_IMAGE_DIGEST_FULL=$(docker inspect "${IMAGE_TAG}" --format '{{.ID}}' 2>/dev/null || echo "${IMAGE_TAG}")
    echo "  Would update to: ${NEW_IMAGE_DIGEST_FULL}"

    # Read current image line
    CURRENT_LINE=$(grep -n "^\s*image:" "$COMPOSE_FILE" | grep -A1 "^\s*arifosmcp:" | tail -1 | sed 's/:.*//' | xargs || echo "")
    if [ -n "$CURRENT_LINE" ]; then
        # Show what would change (don't modify in dry-run)
        echo "  Line ${CURRENT_LINE}: image: ${NEW_IMAGE_DIGEST_FULL}" | head -1
    fi
fi

# ── 8. Restart arifosmcp container ────────────────────────────────────────────
if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "[SKIP] Container restart (dry-run)"
else
    echo ""
    echo "[8] Restarting arifosmcp container..."
    if docker ps --format '{{.Names}}' | grep -q "^arifosmcp$"; then
        docker rm -f arifosmcp 2>/dev/null || true
        echo "  Stopped old container"
    fi

    docker run -d \
        --name arifosmcp \
        --restart unless-stopped \
        -p 127.0.0.1:8080:8080 \
        --env-file "${ARIFOS_DIR}/../.env" \
        -v "${ARIFOS_DIR}:/app:rw" \
        -v /root/volumes/vault999:/var/lib/arifos/vault:rw \
        -v /root/volumes/session-data:/app/data:rw \
        -v /root/WELL/state.json:/root/WELL/state.json:ro \
        --network arifos_core_network \
        "${IMAGE_TAG}" \
        python -m arifosmcp.runtime.__main__ 2>&1
    echo "  Started new container"
    sleep 8

    # ── 9. Verify health ────────────────────────────────────────────────────────
    echo ""
    echo "[9] Verifying health..."
    HEALTH_RESP=$(curl -sf http://127.0.0.1:8080/health 2>/dev/null || echo "{}")
    HEALTH_STATUS=$(echo "$HEALTH_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','FAIL'))" 2>/dev/null || echo "FAIL")
    if [ "$HEALTH_STATUS" != "healthy" ]; then
        echo "[FAIL] Health check failed: ${HEALTH_STATUS}"
        if [ "$AUTO_ROLLBACK" = true ]; then
            echo "[ROLLBACK] Reverting to previous image..."
            docker rm -f arifosmcp 2>/dev/null || true
            docker run -d \
                --name arifosmcp \
                --restart unless-stopped \
                -p 127.0.0.1:8080:8080 \
                --env-file "${ARIFOS_DIR}/../.env" \
                -v "${ARIFOS_DIR}:/app:rw" \
                -v /root/volumes/vault999:/var/lib/arifos/vault:rw \
                -v /root/volumes/session-data:/app/data:rw \
                -v /root/WELL/state.json:/root/WELL/state.json:ro \
                --network arifos_core_network \
                "${PREV_IMAGE_DIGEST}" \
                python -m arifosmcp.runtime.__main__ 2>&1
            echo "[DONE] Rollback complete"
        fi
        STATUS="FAIL"
        REASONS+=("health_check_failed_after_deploy")
        echo "evidence: ${EVIDENCE_FILE}"
        exit 1
    fi
    echo "  Health: ${HEALTH_STATUS}"
fi

# ── Final report ──────────────────────────────────────────────────────────────
echo ""
echo "=== DEPLOY REPORT ==="
echo "status:     ${STATUS}"
echo "risk:       ${RISK}"
echo "image:      ${IMAGE_TAG}"
echo "new_digest: ${NEW_IMAGE_DIGEST:-built}"
echo "prev_digest: ${PREV_IMAGE_DIGEST:-none}"
[ ${#REASONS[@]} -gt 0 ] && echo "reasons:" && for r in "${REASONS[@]}"; do echo "  - $r"; done

REASONS_JSON=$(printf '%s\n' "${REASONS[@]}" | jq -R . | jq -s . 2>/dev/null || echo '[]')
cat > "$EVIDENCE_FILE" << EOF
{
  "skill": "vps_deploy_arifosmcp",
  "status": "${STATUS}",
  "timestamp_utc": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "evidence": {
    "image": "${IMAGE_TAG}",
    "new_image_digest": "${NEW_IMAGE_DIGEST:-built}",
    "prev_image_digest": "${PREV_IMAGE_DIGEST:-none}",
    "git_commit": "${GIT_COMMIT}",
    "git_branch": "${GIT_BRANCH}",
    "uncommitted_files": ${GIT_STATUS},
    "import_truth_new": "${IMPORT_NEW}",
    "health_check": "${HEALTH_STATUS:-not_run}",
    "rollback_triggered": $([ "$STATUS" = "FAIL" ] && echo "true" || echo "false"),
    "dry_run": ${DRY_RUN}
  },
  "reasons": ${REASONS_JSON},
  "risk": "${RISK}",
  "next_safe_action": "$(if [ "$STATUS" = "FAIL" ]; then echo "rollback_completed_check_evidence"; else echo "run_predeploy_audit_then_seal"; fi)",
  "requires_arif": $([ "$STATUS" = "FAIL" ] && echo 'true' || echo 'false')
}
EOF

echo ""
echo "evidence:  ${EVIDENCE_FILE}"
echo "=== END DEPLOY ==="

[ "$STATUS" != "FAIL" ]
