#!/bin/bash
# Start the SSE server on port 8080 in the background
echo "[TRINITY] Starting SSE server on port 8080..."
python -m aaa_mcp sse &

# Start the REST bridge on port 8089 in the foreground (includes /health)
echo "[TRINITY] Starting REST bridge on port 8089..."
PORT=8089 python -m aaa_mcp rest
