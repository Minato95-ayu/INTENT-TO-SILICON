# install.ps1
# AAYU Language Windows Installer (Development Version)

Write-Host "Installing AAYU Compiler..." -ForegroundColor Cyan

# Check if Python is installed
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Error: Python is required to run the AAYU VM." -ForegroundColor Red
    exit 1
}

# The path to the AAYU installation
$AayuHome = Join-Path $env:USERPROFILE ".aayu"
$BinDir = Join-Path $AayuHome "bin"

# Create directories
if (!(Test-Path $BinDir)) {
    New-Item -ItemType Directory -Force -Path $BinDir | Out-Null
}

# Create aayu.bat
$BatContent = @"
@echo off
python "$env:PWD\prototype\cli.py" %*
"@

$BatPath = Join-Path $BinDir "aayu.bat"
Set-Content -Path $BatPath -Value $BatContent -Encoding UTF8

Write-Host "Created aayu.bat at $BatPath" -ForegroundColor Green

# Check if BinDir is in PATH
$UserPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($UserPath -notlike "*$BinDir*") {
    Write-Host "Adding $BinDir to your PATH..." -ForegroundColor Yellow
    [Environment]::SetEnvironmentVariable("PATH", "$UserPath;$BinDir", "User")
    Write-Host "PATH updated. Please restart your terminal for changes to take effect." -ForegroundColor Green
}

Write-Host ""
Write-Host "AAYU Installation Complete!" -ForegroundColor Magenta
Write-Host "Try running: aayu new myapp" -ForegroundColor Magenta
