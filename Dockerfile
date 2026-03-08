# ── arifOS AAA MCP Server ──────────────────────────────────────────────
# Single process, single port.  Runs FastMCP sse transport.
# Hardened for Production (v2026.03.08-SEAL)
# ───────────────────────────────────────────────────────────────────────

FROM python:3.12-slim AS build

# Build-time environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install dependencies in build stage
RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -e .

# Pre-bake BGE-M3 model (F2 Truth / Sensory support)
ENV HF_HOME=/usr/src/app/models
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-m3'); print('BGE-M3 baked in')"


FROM python:3.12-slim AS runtime

# Create non-root user (F11 Authority / F1 Law)
RUN groupadd -g 1000 arifos && \
    useradd -u 1000 -g arifos -m -s /bin/bash arifos

WORKDIR /usr/src/app

# Build arguments for metadata
ARG ARIFOS_VERSION=2026.03.08-SEAL
ARG GIT_SHA=unknown
ARG BUILD_TIME=unknown

# Environment configuration
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8080
ENV HOST=0.0.0.0
ENV AAA_MCP_TRANSPORT=http
ENV ARIFOS_VERSION=${ARIFOS_VERSION}
ENV GIT_SHA=${GIT_SHA}
ENV BUILD_TIME=${BUILD_TIME}

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy artifacts from build stage
COPY --from=build /usr/local /usr/local
COPY --from=build /usr/src/app/models /usr/src/app/models
COPY . .

# Setup dirs and fix ownership
ENV HF_HOME=/usr/src/app/models
RUN mkdir -p telemetry data VAULT999 memory static/dashboard && \
    mkdir -p /ms-playwright && \
    chown -R arifos:arifos /usr/src/app /ms-playwright

# Install Playwright browser (F2 Grounding)
RUN python -m playwright install --with-deps chromium && \
    chown -R arifos:arifos /ms-playwright

# Switch to non-root user
USER arifos

# Expose canonical MCP port
EXPOSE 8080

# Production Healthcheck
HEALTHCHECK --interval=20s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -fsS --max-time 3 http://localhost:8080/health || exit 1

# Execute consolidated entrypoint
CMD ["python", "-m", "arifosmcp.runtime"]
