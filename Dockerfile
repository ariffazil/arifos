# arifOS MCP Server Dockerfile (v65.0-ROUTER)
# Production-ready container for Railway deployment
# Supports: PostgreSQL (VAULT999), Redis (MindVault), SSE transport
# v65.0 Features: arifos-router gateway, AAA-MCP + ACLIP-CAI backends
#
# CACHE BUST: 2026-02-14T04-25-00Z (Force Railway rebuild)
#
# Build: docker build -t arifos-governed-backend .
# Run:   docker run -p 8080:8080 --env-file .env arifos-governed-backend

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
# - curl: healthcheck support
# - gcc: compile native extensions if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Remove old conflicting codebase package from site-packages
RUN pip uninstall -y codebase 2>/dev/null || true
RUN rm -rf /usr/local/lib/python*/site-packages/codebase* 2>/dev/null || true

# Copy package configuration
COPY pyproject.toml .
COPY README.md .
COPY ARCHITECTURE.md .

# Copy source code in dependency order (least likely to change first)
COPY scripts/start_server.py scripts/start_server.py
# v65.0: Router + AAA Core (ACLIP on Hostinger — hybrid topology)
COPY core/ core/
COPY aaa_mcp/ aaa_mcp/
COPY arifos_router.py .
# NOTE: aclip_cai/ not copied — deployed separately on Hostinger (F13 Sovereignty)

# Clear Python cache to ensure fresh imports
RUN find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
RUN find . -name "*.pyc" -delete 2>/dev/null || true

# Install package in editable mode
RUN pip install --no-cache-dir -e .

# Verify package is importable (AAA Core only — ACLIP on Hostinger)
RUN python3 -c "import core; from core.judgment import judge_cognition; print(f'✓ Kernel: {core.__file__}')"
RUN python3 -c "import aaa_mcp; from aaa_mcp.server import mcp; print(f'✓ AAA-MCP: {aaa_mcp.__file__}')"
RUN python3 -c "import arifos_router; print(f'✓ Router: {arifos_router.__file__}')"
# NOTE: ACLIP-CAI verification skipped — requires psutil build deps
# ACLIP deployed separately on Hostinger (Option C hybrid)

# Create non-root user for security
RUN useradd -m -u 1000 arifos && chown -R arifos:arifos /app
USER arifos

# Expose port (Railway sets PORT env var)
EXPOSE 8080

# Health check for Railway monitoring
# Hits /health on the MCP server
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:${PORT:-8080}/health || exit 1

# Run with unbuffered output for real-time log streaming
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command (can be overridden in railway.toml)
CMD ["arifos-router", "--sse", "--port", "8080", "--host", "0.0.0.0"]
