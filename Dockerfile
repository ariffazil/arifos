FROM python:3.12-slim AS build

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN python -m pip install --upgrade pip && \
    if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi && \
    pip install --no-cache-dir .


FROM python:3.12-slim AS runtime

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    procps \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /usr/local /usr/local
COPY . .

# Create writable directories for runtime data (fixes PermissionError)
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

EXPOSE 8080
EXPOSE 8089

HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS --max-time 3 http://localhost:${PORT}/sse > /dev/null || exit 1

LABEL io.modelcontextprotocol.server.name="io.github.ariffazil/arifos-mcp"
LABEL io.modelcontextprotocol.server.version="2026.2.23"
LABEL io.modelcontextprotocol.server.description="Constitutional AI governance server with canonical AAA MCP 13-tool surface and enforced floors F1-F13."
LABEL io.modelcontextprotocol.server.transport="sse"
LABEL io.modelcontextprotocol.server.url="https://arifosmcp.arif-fazil.com/sse"
LABEL io.modelcontextprotocol.server.license="AGPL-3.0-only"

CMD ["python", "-m", "arifos_aaa_mcp", "sse"]
