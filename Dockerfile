# arifOS MCP Server Dockerfile
# Production-ready container for VPS deployment
# Supports: PostgreSQL (VAULT999), Redis (MindVault), SSE transport
#
# Build: docker build -t arifos .
# Run:   docker run -p 8080:8080 --env-file .env arifos

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

# Clean stale packages from site-packages
RUN pip uninstall -y codebase arifos 2>/dev/null || true

# Copy package configuration
COPY pyproject.toml .
COPY README.md .
COPY ARCHITECTURE.md .

# Copy source code — REST bridge for OpenAI compatibility
COPY core/ core/
COPY aaa_mcp/ aaa_mcp/

# Verify REST bridge exists (critical for OpenAI adapter)
RUN python3 -c "from aaa_mcp.rest import TOOLS; print(f'✓ REST bridge: {len(TOOLS)} tools: {list(TOOLS.keys())}')"

# NOTE: aclip_cai/ not copied — deployed separately as its own MCP server

# Clear Python cache to ensure fresh imports
RUN find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
RUN find . -name "*.pyc" -delete 2>/dev/null || true

# Install package in editable mode
RUN pip install --no-cache-dir -e .

# Verify package is importable (AAA Core only)
RUN python3 -c "import core; from core.judgment import judge_cognition; print(f'✓ Kernel: {core.__file__}')"
RUN python3 -c "import aaa_mcp; from aaa_mcp.server import mcp; print(f'✓ AAA-MCP: {aaa_mcp.__file__}')"
# Using aaa_mcp directly (no router)

# Create non-root user for security
RUN useradd -m -u 1000 arifos && chown -R arifos:arifos /app
USER arifos

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -sf http://localhost:${PORT:-8080}/health || exit 1

# Run with unbuffered output for real-time log streaming
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command
CMD ["python", "-m", "aaa_mcp", "sse", "--port", "8080", "--host", "0.0.0.0"]
