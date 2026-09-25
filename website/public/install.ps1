Write-Host "====================================" -ForegroundColor Cyan
Write-Host "🚀 Installing AAYU Language Compiler" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan

$aayuDir = "$env:USERPROFILE\.aayu\bin"
if (-not (Test-Path $aayuDir)) {
    New-Item -ItemType Directory -Force -Path $aayuDir | Out-Null
}

$exeUrl = "https://intent-to-silicon.vercel.app/releases/aayu.exe"
$exePath = "$aayuDir\aayu.exe"

Write-Host "📥 Downloading Native Windows Compiler..."
Invoke-WebRequest -Uri $exeUrl -OutFile $exePath

# Add to PATH
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notmatch "\.aayu\\bin") {
    $newPath = "$userPath;$aayuDir"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "✅ Added AAYU to System PATH." -ForegroundColor Green
} else {
    Write-Host "✅ AAYU is already in System PATH." -ForegroundColor Green
}

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "🎉 AAYU INSTALLATION SUCCESSFUL! 🎉" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "⚠️  IMPORTANT: Please RESTART your terminal or VS Code so it can detect the new command." -ForegroundColor Yellow
Write-Host "After restarting, you can run AAYU from ANY folder by typing:" -ForegroundColor White
Write-Host "> aayu run yourfile.aayu" -ForegroundColor Cyan
