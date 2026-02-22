#!/bin/bash
set -e

# Ensure writable directories exist
mkdir -p /usr/src/app/telemetry /usr/src/app/data /usr/src/app/VAULT999 /usr/src/app/memory

echo "[TRINITY] Starting SSE server on port 8080..."
python -m aaa_mcp sse &
SSE_PID=$!

echo "[TRINITY] Starting REST bridge on port 8089..."
PORT=8089 python -m aaa_mcp rest &
REST_PID=$!

echo "[TRINITY] Both servers running (SSE=$SSE_PID, REST=$REST_PID)"

# Wait for either to exit — if one dies, kill the other
wait -n $SSE_PID $REST_PID
echo "[TRINITY] A process exited. Shutting down..."
kill $SSE_PID $REST_PID 2>/dev/null
wait
