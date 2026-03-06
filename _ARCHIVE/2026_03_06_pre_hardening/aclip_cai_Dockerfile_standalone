# Dockerfile for aclip_cai — Clinical Infrastructure Console
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything
COPY . .

# Expose MCP port
EXPOSE 8889

# Run aclip_cai server
CMD ["python", "aclip_cai/mcp_server.py"]
