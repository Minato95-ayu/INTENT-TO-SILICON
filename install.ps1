$ErrorActionPreference = 'Stop'
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Installing AAYU (Intent-to-Silicon)     " -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

$url = "https://github.com/Minato95-ayu/INTENT-TO-SILICON/releases/download/v1.3.0/aayu-windows.zip"
$installDir = "$env:USERPROFILE\.aayu\bin"
New-Item -ItemType Directory -Force -Path $installDir | Out-Null
$zipPath = "$env:TEMP\aayu-windows.zip"

Write-Host "[1/3] Downloading Native Rust Binary for Windows..."
Invoke-WebRequest -Uri $url -OutFile $zipPath

Write-Host "[2/3] Extracting Engine..."
Expand-Archive -Path $zipPath -DestinationPath $installDir -Force
Remove-Item $zipPath -Force

Write-Host "[3/3] Finalizing..."
Write-Host "AAYU installed successfully to $installDir!" -ForegroundColor Green
Write-Host ""
Write-Host "=> To get started, please add AAYU to your environment PATH variable:"
Write-Host "   $installDir"
Write-Host "==========================================" -ForegroundColor Cyan
