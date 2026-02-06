@echo off
REM arifOS Unified MCP Server Startup Script (Live SSE Mode)
REM Starts the MCP server via scripts/start_server.py

echo ================================================================================
echo arifOS Unified MCP Server v49.0.0 (SSE/Live)
echo ================================================================================
echo.

REM Set environment variables
set ARIFOS_ALLOW_LEGACY_SPEC=1
set ARIFOS_PHYSICS_DISABLED=0
set AAA_MCP_TRANSPORT=sse
set PORT=8080
set HOST=0.0.0.0
set PYTHONPATH=%PYTHONPATH%;%CD%

echo Environment:
echo   ARIFOS_ALLOW_LEGACY_SPEC=%ARIFOS_ALLOW_LEGACY_SPEC%
echo   ARIFOS_PHYSICS_DISABLED=%ARIFOS_PHYSICS_DISABLED%
echo   AAA_MCP_TRANSPORT=%AAA_MCP_TRANSPORT%
echo   PORT=%PORT%
echo   HOST=%HOST%
echo.

echo Starting SSE Server (Port %PORT%)...
echo Press Ctrl+C to stop
echo.

REM Start the live server entrypoint
python scripts\start_server.py

echo.
echo MCP server stopped.
pause
