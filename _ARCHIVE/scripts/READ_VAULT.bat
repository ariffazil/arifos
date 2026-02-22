@echo off
title VAULT999 Reader
echo.
echo =========================================
echo   VAULT999 Seal Reader
echo =========================================
echo.

cd /d "%~dp0"

if "%~1"=="" (
    echo Usage:
    echo   READ_VAULT list       - Show last 10 seals
    echo   READ_VAULT 12         - Read seal #12
    echo.
    set /p seq="Enter seal number (or 'list'): "
) else (
    set seq=%~1
)

python read_vault.py %seq%

echo.
pause
