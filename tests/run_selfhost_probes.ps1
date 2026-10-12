$ErrorActionPreference = "Stop"
$vm = if ($env:AAYU_VM_PATH) { $env:AAYU_VM_PATH } else { Join-Path $PSScriptRoot "..\bin\aayu-vm.exe" }
if (-not (Test-Path -LiteralPath $vm)) { Write-Error "AAYU VM not found: $vm"; exit 1 }

$repo = Split-Path -Parent $PSScriptRoot
$lexer = Join-Path $repo "compiler\lexer.aayu"
$compiler = Join-Path $repo "compiler\compiler.aayu"

$lexerOutput = (& $vm run $lexer 2>&1 | Out-String)
if ($LASTEXITCODE -ne 0 -or $lexerOutput -notmatch "TOKENIZATION RESULT" -or $lexerOutput -notmatch "IDENTIFIER") {
    Write-Error "AAYU lexer probe failed or did not produce token output.`n$lexerOutput"
    exit 1
}
Write-Host "[PASS] AAYU lexer source runs and tokenizes its sample"

$compilerOutput = (& $vm run $compiler 2>&1 | Out-String)
if ($LASTEXITCODE -ne 0 -or $compilerOutput -notmatch "Compiler Success") {
    Write-Error "AAYU compiler demo failed.`n$compilerOutput"
    exit 1
}
$lengthMatch = [regex]::Match($compilerOutput, "Bytecode Array Length:\s*(\d+)")
if (-not $lengthMatch.Success -or [int]$lengthMatch.Groups[1].Value -le 0) {
    Write-Error "AAYU compiler demo did not produce a non-empty bytecode array.`n$compilerOutput"
    exit 1
}
Write-Host "[PASS] AAYU compiler demo runs and emits a non-empty bytecode array"
