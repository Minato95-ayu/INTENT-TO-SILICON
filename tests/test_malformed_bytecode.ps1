# Malformed Bytecode Security Verification Suite
# Strict test: checks specific error messages, non-zero exit codes, and both Interpreter and JIT modes

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "     AAYU BYTECODE VERIFIER & SECURITY TEST SUITE " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$vm = "$PSScriptRoot\..\bin\aayu.exe"
if (-not (Test-Path $vm)) {
    $vm = "$PSScriptRoot\..\runtime_rs\target\release\aayu-vm.exe"
}

if (-not (Test-Path $vm)) {
    Write-Host "[ERROR] VM executable not found!" -ForegroundColor Red
    exit 1
}

$tempDir = Join-Path $PSScriptRoot "temp_malformed"
if (-not (Test-Path $tempDir)) { New-Item -ItemType Directory -Path $tempDir | Out-Null }

$testCases = @(
    @{
        Name = "Empty file"
        Bytes = [byte[]]@()
        Expected = "missing magic header"
    },
    @{
        Name = "Invalid magic header"
        Bytes = [byte[]]@(0x42, 0x41, 0x44, 0x21, 0x00, 0x00, 0x00, 0x00) # BAD!
        Expected = "Invalid magic header"
    },
    @{
        Name = "Truncated string table"
        Bytes = [byte[]]@(0x41, 0x41, 0x59, 0x55, 0x05, 0x00, 0x00, 0x00) # 5 strings declared, but EOF
        Expected = "Truncated bytecode"
    },
    @{
        Name = "Illegal opcode (0xEE)"
        # Valid header, 0 strings, 0 constants, bytecode: [0xEE]
        Bytes = [byte[]]@(0x41, 0x41, 0x59, 0x55, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xEE)
        Expected = "illegal opcode 0xEE"
    },
    @{
        Name = "Out-of-bounds jump target"
        # Valid header, 0 strings, 0 constants, bytecode: JMP (0x20) target=0xFF00
        Bytes = [byte[]]@(0x41, 0x41, 0x59, 0x55, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x20, 0xFF, 0x00)
        Expected = "exceeds bytecode bounds"
    },
    @{
        Name = "Truncated PUSH_CONST operand"
        # Valid header, 0 strings, 0 constants, bytecode: PUSH_CONST (0x01) with only 1 byte operand
        Bytes = [byte[]]@(0x41, 0x41, 0x59, 0x55, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00)
        Expected = "Truncated operand for PUSH_CONST"
    }
)

$passed = 0
$failed = 0

foreach ($tc in $testCases) {
    $filePath = Join-Path $tempDir "corrupt_test.ayc"
    [System.IO.File]::WriteAllBytes($filePath, $tc.Bytes)

    # 1. Test Interpreter Mode
    $outInterp = & $vm run $filePath 2>&1 | Out-String
    $codeInterp = $LASTEXITCODE

    $interpOk = ($outInterp -match $tc.Expected) -and ($codeInterp -ne 0)

    # 2. Test JIT Mode (Verifier must NOT be bypassed)
    $outJit = & $vm run $filePath --jit 2>&1 | Out-String
    $codeJit = $LASTEXITCODE

    $jitOk = ($outJit -match $tc.Expected) -and ($codeJit -ne 0)

    if ($interpOk -and $jitOk) {
        Write-Host " [PASS] $($tc.Name) safely rejected on both Interpreter & JIT (Code: $codeInterp/$codeJit)" -ForegroundColor Green
        $passed++
    } else {
        Write-Host " [FAIL] $($tc.Name) rejection failed:" -ForegroundColor Red
        if (-not $interpOk) {
            Write-Host "   Interpreter failed: Code=$codeInterp, Output=$outInterp" -ForegroundColor Red
        }
        if (-not $jitOk) {
            Write-Host "   JIT failed: Code=$codeJit, Output=$outJit" -ForegroundColor Red
        }
        $failed++
    }
}

Remove-Item -Recurse -Force $tempDir

Write-Host "--------------------------------------------------" -ForegroundColor Cyan
Write-Host "Security Results: $passed Passed | $failed Failed" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Red" })
Write-Host "==================================================" -ForegroundColor Cyan

if ($failed -gt 0) { exit 1 } else { exit 0 }
