@echo off
title VAULT999 Verification
echo.
echo =========================================
echo   VAULT999 Verification Tool
echo =========================================
echo.
echo Testing PostgreSQL connection and vault...
echo.

cd /d "%~dp0"
python railway_verify.py

if errorlevel 1 (
    echo.
    echo Verification failed.
    pause
    exit /b 1
)
