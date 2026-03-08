# ── arifOS Trinity Body — Constitutional Kernel ────────────────────────
# FastMCP-compliant runtime.  Runs via core/server.py (arifos-mcp entry).
# Transport: streamable-HTTP  Port: 8080
# ───────────────────────────────────────────────────────────────────────

FROM python:3.12-slim AS build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/usr/src/app/models

WORKDIR /usr/src/app

# Build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock* ./
COPY core/ ./core/
COPY aaa_mcp/ ./aaa_mcp/
COPY arifos_aaa_mcp/ ./arifos_aaa_mcp/
COPY aclip_cai/ ./aclip_cai/
COPY config/ ./config/
COPY resources/ ./resources/
COPY fastmcp.json ./

# Install package + deps
RUN pip install --upgrade pip && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir .

# Pre-bake BGE-M3 model — strip ONNX/ORT to keep size ~570 MB not ~4 GB
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-m3'); print('BGE-M3 baked')" && \
    find models -name "*.onnx" -delete 2>/dev/null || true && \
    find models -name "*.ort" -delete 2>/dev/null || true && \
    find models -type d -name "onnx" -exec rm -rf {} + 2>/dev/null || true


FROM python:3.12-slim AS runtime

RUN groupadd -g 1000 arifos && useradd -u 1000 -g arifos -m -s /bin/bash arifos

WORKDIR /usr/src/app

ARG ARIFOS_VERSION=2026.03.08
ARG GIT_SHA=unknown
ARG BUILD_TIME=unknown

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HF_HOME=/usr/src/app/models \
    PORT=8080 \
    HOST=0.0.0.0 \
    ARIFOS_VERSION=${ARIFOS_VERSION} \
    GIT_SHA=${GIT_SHA} \
    BUILD_TIME=${BUILD_TIME}

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates && rm -rf /var/lib/apt/lists/*

# Copy build artefacts
COPY --from=build /usr/local /usr/local
COPY --from=build /usr/src/app/models ./models
COPY . .

RUN mkdir -p telemetry data VAULT999 memory logs && \
    mkdir -p /ms-playwright && \
    chown -R arifos:arifos /usr/src/app /ms-playwright

RUN python -m playwright install --with-deps chromium && \
    chown -R arifos:arifos /ms-playwright

USER arifos

EXPOSE 8080

HEALTHCHECK --interval=20s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -fsS --max-time 3 http://localhost:8080/health || exit 1

LABEL io.modelcontextprotocol.server.name="io.github.ariffazil/arifos-mcp"
LABEL io.modelcontextprotocol.server.version="${ARIFOS_VERSION}"
LABEL io.modelcontextprotocol.server.description="Trinity Body: Constitutional AI governance runtime — 13-tool surface, 13-Floor thermodynamics."
LABEL org.opencontainers.image.source="https://github.com/ariffazil/arifosmcp"

CMD ["python", "-m", "arifos_aaa_mcp", "http"]
