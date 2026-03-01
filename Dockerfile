# ── arifOS AAA MCP Server ──────────────────────────────────────────────
# Single process, single port.  Runs FastMCP streamable-HTTP transport
# with REST endpoints (/health, /tools, /version) as custom routes.
#
# Build:  docker build -t arifos .
# Run:    docker run -p 8080:8080 arifos
# ───────────────────────────────────────────────────────────────────────

FROM python:3.12-slim AS build

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY . .
COPY aclip_cai/embeddings /app/models/bge

RUN python -m pip install --upgrade pip && \
    if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi && \
    pip install --no-cache-dir .


FROM python:3.12-slim AS runtime

WORKDIR /usr/src/app

ARG ARIFOS_VERSION=unknown
ARG GIT_SHA=unknown
ARG BUILD_TIME=unknown

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /usr/local /usr/local
COPY . .
COPY aclip_cai/embeddings /app/models/bge

# Install a deterministic Chromium runtime for Playwright-based search/fetch paths.
RUN python -m playwright install --with-deps chromium

# Writable directories for runtime data
RUN mkdir -p /usr/src/app/telemetry \
    /usr/src/app/data \
    /usr/src/app/VAULT999 \
    /usr/src/app/memory \
    && chmod -R 777 /usr/src/app/telemetry \
    /usr/src/app/data \
    /usr/src/app/VAULT999 \
    /usr/src/app/memory

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8080
ENV HOST=0.0.0.0
ENV ARIFOS_VERSION=${ARIFOS_VERSION}
ENV GIT_SHA=${GIT_SHA}
ENV BUILD_TIME=${BUILD_TIME}

EXPOSE 8080

# Real HTTP healthcheck against the /health endpoint
HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS --max-time 3 http://localhost:8080/health || exit 1

LABEL io.modelcontextprotocol.server.name="io.github.ariffazil/arifos-mcp"
LABEL io.modelcontextprotocol.server.version="${ARIFOS_VERSION}"
LABEL io.modelcontextprotocol.server.description="Constitutional AI governance server with 13-tool surface and F1-F13 floor enforcement."
LABEL io.modelcontextprotocol.server.transport="streamable-http"
LABEL io.modelcontextprotocol.server.url="https://arifosmcp.arif-fazil.com/mcp"
LABEL io.modelcontextprotocol.server.license="AGPL-3.0-only"

# ONE process.  FastMCP streamable-HTTP on port 8080.
# MCP protocol at /mcp, REST at /health /tools /version etc.
CMD ["python", "-m", "arifos_aaa_mcp", "http"]
