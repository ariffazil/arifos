# Add uv to PATH permanently for current user
$uvPath = "C:\Users\User\.local\bin"

# Get current user PATH
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Check if already in PATH
if ($currentPath -notlike "*$uvPath*") {
    # Add to PATH
    $newPath = "$uvPath;$currentPath"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "[OK] Added $uvPath to user PATH" -ForegroundColor Green
    Write-Host "[!]  Please restart your PowerShell session for changes to take effect" -ForegroundColor Yellow
} else {
    Write-Host "[OK] $uvPath already in PATH" -ForegroundColor Green
}

# Also set for current session
$env:PATH = "$uvPath;$env:PATH"
Write-Host "[OK] Updated PATH for current session" -ForegroundColor Green

# Test
Write-Host "`nTesting installations:" -ForegroundColor Cyan
Write-Host "UV: " -NoNewline
& uv --version 2>$null
if ($?) { Write-Host "  [OK]" -ForegroundColor Green } else { Write-Host "  [FAIL]" -ForegroundColor Red }

Write-Host "Kimi: " -NoNewline
& kimi --version 2>$null
if ($?) { Write-Host "  [OK]" -ForegroundColor Green } else { Write-Host "  [FAIL]" -ForegroundColor Red }
