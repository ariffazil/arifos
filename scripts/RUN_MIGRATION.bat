@echo off
title VAULT999 Railway Migration
echo.
echo =========================================
echo   VAULT999 Railway Migration Tool
echo =========================================
echo.
echo This will set up your PostgreSQL tables on Railway.
echo.
echo Requirements:
echo  - Node.js installed (from https://nodejs.org)
echo  - Railway account with arifOS project
echo.
pause
echo.
echo Starting migration...
echo.

cd /d "%~dp0"
python railway_migration.py

if errorlevel 1 (
    echo.
    echo Migration failed.
    pause
    exit /b 1
)
