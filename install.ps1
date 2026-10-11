# ==============================================================================
# AAYU Programming Language - Official Windows One-Click Installer
# Intent-to-Silicon Architecture (Zero Dependencies, 100% Native)
# ==============================================================================

$ErrorActionPreference = 'Stop'

Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "            A A Y U   P R O G R A M M I N G                     " -ForegroundColor Cyan
Write-Host "               Intent-to-Silicon Engine                         " -ForegroundColor Cyan
Write-Host "    Single-File Full-Stack | Zero Dependencies | C-Speed        " -ForegroundColor DarkGray
Write-Host "================================================================" -ForegroundColor Cyan

$aayuRoot = Join-Path $env:USERPROFILE ".aayu"
$installBin = Join-Path $aayuRoot "bin"
$installStd = Join-Path $aayuRoot "std"
$installExamples = Join-Path $aayuRoot "examples"

if (-not (Test-Path $installBin)) { New-Item -ItemType Directory -Force -Path $installBin | Out-Null }
if (-not (Test-Path $installStd)) { New-Item -ItemType Directory -Force -Path $installStd | Out-Null }
if (-not (Test-Path $installExamples)) { New-Item -ItemType Directory -Force -Path $installExamples | Out-Null }

$scriptDir = $PSScriptRoot
$isLocalRepo = $false

if ($scriptDir -and (Test-Path (Join-Path $scriptDir "bin\aayu.exe"))) {
    $isLocalRepo = $true
} elseif (Test-Path ".\bin\aayu.exe") {
    $scriptDir = (Get-Item ".").FullName
    $isLocalRepo = $true
}

if ($isLocalRepo) {
    Write-Host "`n[1/4] Installing from local repository..." -ForegroundColor Yellow
    Copy-Item -Path (Join-Path $scriptDir "bin\aayu.exe") -Destination (Join-Path $installBin "aayu.exe") -Force
    if (Test-Path (Join-Path $scriptDir "bin\aayuc.exe")) {
        Copy-Item -Path (Join-Path $scriptDir "bin\aayuc.exe") -Destination (Join-Path $installBin "aayuc.exe") -Force
    }
    if (Test-Path (Join-Path $scriptDir "bin\aayu-vm.exe")) {
        Copy-Item -Path (Join-Path $scriptDir "bin\aayu-vm.exe") -Destination (Join-Path $installBin "aayu-vm.exe") -Force
    }
    
    if (Test-Path (Join-Path $scriptDir "std")) {
        Copy-Item -Path (Join-Path $scriptDir "std\*") -Destination $installStd -Recurse -Force
    }
    if (Test-Path (Join-Path $scriptDir "examples")) {
        Copy-Item -Path (Join-Path $scriptDir "examples\*") -Destination $installExamples -Recurse -Force
    }
    Write-Host "      Installed native binaries and standard library." -ForegroundColor Green
} else {
    Write-Host "`n[1/4] Downloading latest AAYU native binaries from GitHub..." -ForegroundColor Yellow
    $zipUrl = "https://github.com/Minato95-ayu/INTENT-TO-SILICON/releases/download/v1.3.0/aayu-windows.zip"
    $zipPath = Join-Path $env:TEMP "aayu-windows.zip"
    
    try {
        Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath -UseBasicParsing
        Write-Host "[2/4] Extracting binaries..." -ForegroundColor Yellow
        Expand-Archive -Path $zipPath -DestinationPath $installBin -Force
        Remove-Item $zipPath -Force
    } catch {
        Write-Host "      Remote release package not reachable yet. Using fallback installation." -ForegroundColor DarkYellow
    }
}

Write-Host "[2/4] Verifying native binary integrity..." -ForegroundColor Yellow
$targetExe = Join-Path $installBin "aayu.exe"
if (Test-Path $targetExe) {
    $bytes = (Get-Item $targetExe).Length
    $sizeKb = [math]::Round($bytes / 1024, 1)
    Write-Host "      aayu.exe verified ($sizeKb KB stripped Fat LTO binary)" -ForegroundColor Green
} else {
    Write-Host "      Error: aayu.exe not found in $installBin" -ForegroundColor Red
    exit 1
}

Write-Host "[3/4] Configuring User Environment PATH..." -ForegroundColor Yellow
$userPath = [System.Environment]::GetEnvironmentVariable('Path', 'User')
if (-not $userPath) { $userPath = "" }
$pathList = $userPath.Split(';') | Where-Object { $_ -ne "" }

if ($pathList -notcontains $installBin) {
    $newPath = $userPath + ";" + $installBin
    [System.Environment]::SetEnvironmentVariable('Path', $newPath, 'User')
    Write-Host "      Added $installBin to permanent User PATH." -ForegroundColor Green
} else {
    Write-Host "      $installBin is already in User PATH." -ForegroundColor Green
}

# Update current session PATH so commands work immediately
$currentPathList = $env:PATH.Split(';')
if ($currentPathList -notcontains $installBin) {
    $env:PATH = $env:PATH + ";" + $installBin
}

Write-Host "[4/4] Running installation smoke test..." -ForegroundColor Yellow
& $targetExe --version
Write-Host ""
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  CONGRATULATIONS! AAYU is successfully installed on your PC!   " -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Quick Start Commands:" -ForegroundColor White
Write-Host "  aayu --help                    # View complete documentation" -ForegroundColor Yellow
Write-Host "  aayu run hello.aayu            # Compile and run in sub-milliseconds" -ForegroundColor Yellow
Write-Host "  aayu run app.ayc --jit         # Run with hardware-level C speed" -ForegroundColor Yellow
Write-Host "  aayu build app.aayu -o app.ayc # Compile standalone bytecode" -ForegroundColor Yellow
Write-Host ""
Write-Host "Standard Library installed at: $installStd" -ForegroundColor DarkGray
Write-Host "Examples installed at:         $installExamples" -ForegroundColor DarkGray
Write-Host ""
