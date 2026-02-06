# arifOS MCP Server Dockerfile (v55.5-HARDENED)
# Cache-bust: 2026-02-06-api-keys
FROM python:3.12-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source - CRITICAL: Copy in order of least to most likely to change
COPY pyproject.toml .
COPY scripts/start_server.py scripts/start_server.py
COPY codebase/ codebase/
COPY aaa_mcp/ aaa_mcp/

# Debug: Verify code version
RUN echo "=== Build Time ===" && date -u +"%Y-%m-%dT%H:%M:%SZ"
RUN echo "=== aaa_mcp contents ===" && ls -la aaa_mcp/
RUN echo "=== aaa_mcp server ===" && python3 -c "from aaa_mcp.server import mcp; print('MCP server OK')"

# Clear Python cache to ensure fresh imports
RUN find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
RUN find . -name "*.pyc" -delete 2>/dev/null || true

# Install package
RUN pip install -e .

# Expose port
EXPOSE 8080

# Health check — hits /health on the MCP server (not Flask)
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:${PORT:-8080}/health || exit 1

# Run with unbuffered output for logs
ENV PYTHONUNBUFFERED=1
CMD ["python", "-u", "scripts/start_server.py"]
