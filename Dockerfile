# Emergency minimal Dockerfile for debugging
FROM python:3.12-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source
COPY pyproject.toml .
COPY codebase/ codebase/
COPY mcp/ mcp/
COPY start_server.py .

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
