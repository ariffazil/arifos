# arifOS MCP Server Dockerfile (v55.3.2-9tools-SEAL)
# Cache-bust: 2026-02-03-14-50-FORCE-REBUILD-v2
FROM python:3.12-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl git && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source - CRITICAL: Copy in order of least to most likely to change
COPY pyproject.toml .
COPY start_server.py .
COPY codebase/ codebase/
COPY mcp_server/ mcp_server/

# Debug: Verify code version
RUN echo "=== Build Time ===" && date -u +"%Y-%m-%dT%H:%M:%SZ"
RUN echo "=== Git Commit ===" && git rev-parse --short HEAD 2>/dev/null || echo "no git"
RUN echo "=== mcp_server contents ===" && ls -la mcp_server/
RUN echo "=== init_gate code ===" && grep -A2 'motto.*=' mcp_server/tools/canonical_trinity.py | head -5
RUN echo "=== codebase/init exports ===" && python3 -c "from codebase.init import mcp_000_init; print('mcp_000_init:', mcp_000_init)"

# Clear Python cache to ensure fresh imports
RUN find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
RUN find . -name "*.pyc" -delete 2>/dev/null || true

# Install package
RUN pip install -e .

# Expose port
EXPOSE 8080

# Simple health check
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -sf http://localhost:${PORT:-8080}/health || exit 1

# Run with unbuffered output for logs
ENV PYTHONUNBUFFERED=1
CMD ["python", "-u", "start_server.py"]
