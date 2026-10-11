# Malformed Bytecode Security Verification Suite
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "     AAYU BYTECODE VERIFIER & SECURITY TEST SUITE " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$vm = ".\bin\aayu.exe"
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
        Bytes = [byte[]]@(0x41, 0x41, 0x59, 0x55, 0x05, 0x00, 0x00, 0x00) # Says 5 strings, but EOF
        Expected = "Truncated bytecode"
    },
    @{
        Name = "Illegal opcode (0xEE)"
        # Valid header, 0 strings, 0 constants, bytecode: [0xEE]
        Bytes = [byte[]]@(0x41, 0x41, 0x59, 0x55, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xEE)
        Expected = "Unknown or illegal opcode"
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

    $output = & $vm run $filePath 2>&1 | Out-String
    
    if ($output -match $tc.Expected -or $output -match "Security Error" -or $output -match "Malformed Bytecode") {
        Write-Host " [PASS] $($tc.Name) safely rejected: Invariant preserved." -ForegroundColor Green
        $passed++
    } else {
        Write-Host " [FAIL] $($tc.Name) was not rejected properly. Output: $output" -ForegroundColor Red
        $failed++
    }
}

Remove-Item -Recurse -Force $tempDir

Write-Host "--------------------------------------------------" -ForegroundColor Cyan
Write-Host "Security Results: $passed Passed | $failed Failed" -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan

if ($failed -gt 0) { exit 1 } else { exit 0 }
