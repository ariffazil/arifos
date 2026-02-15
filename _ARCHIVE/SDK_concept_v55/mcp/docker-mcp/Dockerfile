FROM python:3.11-slim

WORKDIR /app

# Install only curl for healthchecks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir mcp uvicorn starlette httpx

# Copy source
COPY src/ ./src/

# Expose MCP HTTP port
EXPOSE 8080

# Run MCP server
CMD ["python", "-m", "src.server"]
