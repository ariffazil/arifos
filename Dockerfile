# arifOS MCP Server Dockerfile (v65.0-AAA-MCP)
# Production-ready container for Railway deployment
# Supports: PostgreSQL (VAULT999), Redis (MindVault), SSE transport
# v65.0 Features: AAA-MCP directly (no router)
#
# CACHE BUST: 2026-02-14T08-00-00Z (v64.2.2 - Core module update)
#
# Build: docker build -t arifos-governed-backend .
# Run:   docker run -p 8080:8080 --env-file .env arifos-governed-backend

# Set the working directory inside the container
WORKDIR /usr/src/app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     && rm -rf /var/lib/apt/lists/*

# Install system dependencies
# - curl: healthcheck support
# - gcc: compile native extensions if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt if it exists (using wildcard to avoid build failure)
COPY requirements.tx[t] ./requirements.txt

# Remove old conflicting codebase package from site-packages
RUN pip uninstall -y codebase 2>/dev/null || true
RUN rm -rf /usr/local/lib/python*/site-packages/codebase* 2>/dev/null || true

# Copy the rest of the application source code
COPY . .

# Copy source code — REST bridge for OpenAI compatibility
COPY core/ core/
COPY aaa_mcp/ aaa_mcp/
COPY start-trinity.sh .
RUN chmod +x start-trinity.sh

# Set the working directory
WORKDIR /usr/src/app

# NOTE: aclip_cai/ not copied — deployed separately on Hostinger (F13 Sovereignty)
# NOTE: scripts/start_server.py removed — using REST bridge instead

# Copy the application code
COPY --from=build /usr/src/app .

# Set the virtual environment as the active Python environment
ENV PATH="/opt/venv/bin:$PATH"

# Verify package is importable (AAA Core only)
RUN python3 -c "import core; from core.judgment import judge_cognition; print(f'✓ Kernel: {core.__file__}')"
RUN python3 -c "import aaa_mcp; from aaa_mcp.server import mcp; print(f'✓ AAA-MCP: {aaa_mcp.__file__}')"
# Router removed from build - using aaa_mcp directly (see railway.toml)

# Expose the port your app runs on
ENV PORT=8080
EXPOSE $PORT

# Expose port (Railway sets PORT env var)
EXPOSE 8080

# Health check for Railway monitoring
# Health check: verify both SSE and HTTP processes are running
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD pgrep -f "python -m aaa_mcp sse" && pgrep -f "python -m aaa_mcp http" || exit 1

# Run with unbuffered output for real-time log streaming
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command (overridden by railway.toml)
CMD ["python", "-m", "aaa_mcp", "sse", "--port", "8080", "--host", "0.0.0.0"]
# CACHE BUST: 20260214080000 (FORCE REBUILD - Core update)
