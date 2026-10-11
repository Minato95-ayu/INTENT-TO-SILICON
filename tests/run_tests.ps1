# AAYU Automated Test Harness
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "       AAYU INTENT-TO-SILICON TEST RUNNER         " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$binAayuc = "$PSScriptRoot\..\bin\aayuc.exe"
$binVm = "$PSScriptRoot\..\bin\aayu-vm.exe"

if (-not (Test-Path $binAayuc) -or -not (Test-Path $binVm)) {
    Write-Host "[ERROR] Compiler or VM not found in bin/" -ForegroundColor Red
    exit 1
}

$testFiles = Get-ChildItem -Path $PSScriptRoot -Filter "*.aayu"
$passed = 0
$failed = 0

foreach ($file in $testFiles) {
    $baseName = $file.BaseName
    $aycFile = "$PSScriptRoot\$baseName.ayc"
    
    Write-Host "[TEST] Running $($file.Name)..." -NoNewline
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    
    # 1. Compile
    & $binAayuc $file.FullName -o $aycFile | Out-Null
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $aycFile)) {
        Write-Host " FAIL (Compilation)" -ForegroundColor Red
        $failed++
        continue
    }
    
    # 2. Execute
    $out = & $binVm $aycFile 2>&1
    $sw.Stop()
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host " PASS ($($sw.ElapsedMilliseconds) ms)" -ForegroundColor Green
        $passed++
    } else {
        Write-Host " FAIL (Runtime error)" -ForegroundColor Red
        Write-Host $out
        $failed++
    }
    
    Remove-Item $aycFile -Force -ErrorAction SilentlyContinue
}

# Run Security Suite
$secScript = "$PSScriptRoot\test_malformed_bytecode.ps1"
if (Test-Path $secScript) {
    & powershell -ExecutionPolicy Bypass -File $secScript
    if ($LASTEXITCODE -ne 0) {
        $failed++
    }
}

Write-Host "--------------------------------------------------" -ForegroundColor Cyan
Write-Host "Results: $passed Passed | $failed Failed" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Red" })
Write-Host "==================================================" -ForegroundColor Cyan

if ($failed -gt 0) { exit 1 } else { exit 0 }
