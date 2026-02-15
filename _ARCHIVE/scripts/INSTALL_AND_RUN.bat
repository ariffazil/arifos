@echo off
title VAULT999 Setup - Installing Railway CLI...
echo.
echo =========================================
echo   VAULT999 Setup - Step 1 of 2
echo =========================================
echo.
echo This will install Railway CLI (one-time setup).
echo.

:: Check if npm is installed
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Node.js/npm not found!
    echo.
    echo Please install Node.js first:
    echo 1. Go to https://nodejs.org
    echo 2. Click the green "LTS" button
    echo 3. Run the installer
    echo 4. Restart your computer
    echo 5. Run this script again
    echo.
    start https://nodejs.org
    pause
    exit /b 1
)

echo OK Node.js found!
echo.

:: Check if railway is already installed
where railway >nul 2>nul
if %errorlevel% equ 0 (
    echo OK Railway CLI already installed!
    goto :run_migration
)

echo Installing Railway CLI... (this may take a minute)
echo.

call npm install -g @railway/cli

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install Railway CLI
    echo Try running this as Administrator
    echo.
    pause
    exit /b 1
)

echo.
echo OK Railway CLI installed!
echo.
echo Reloading PATH...
echo.

:: Reload PATH from registry
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul ^| findstr /i "Path"') do set "SYSPATH=%%b"
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul ^| findstr /i "Path"') do set "USERPATH=%%b"
set "PATH=%SYSPATH%;%USERPATH%;%PATH%"

:run_migration
echo =========================================
echo   Now running migration...
echo =========================================
echo.
timeout /t 2 >nul

cd /d "%~dp0"

:: Try to find railway in common locations
if exist "%LOCALAPPDATA%\npm\railway.cmd" (
    set "RAILWAY_CMD=%LOCALAPPDATA%\npm\railway.cmd"
) else if exist "%APPDATA%\npm\railway.cmd" (
    set "RAILWAY_CMD=%APPDATA%\npm\railway.cmd"
) else if exist "%ProgramFiles%\nodejs\railway.cmd" (
    set "RAILWAY_CMD=%ProgramFiles%\nodejs\railway.cmd"
) else (
    set "RAILWAY_CMD=railway"
)

echo Using Railway command: %RAILWAY_CMD%
echo.

:: Set the railway command for the Python script
set "RAILWAY_EXE=%RAILWAY_CMD%"
python railway_migration.py

pause
