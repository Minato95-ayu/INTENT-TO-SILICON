# AAYU Reproducible Benchmarking Suite
# Measures latency, cold-start, and throughput across multiple iterations

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "      AAYU REPRODUCIBLE BENCHMARK RUNNER          " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$cpu = (Get-CimInstance Win32_Processor).Name
$os = (Get-CimInstance Win32_OperatingSystem).Caption
$cores = (Get-CimInstance Win32_Processor).NumberOfCores

Write-Host "Hardware Context:" -ForegroundColor Yellow
Write-Host "  CPU: $cpu ($cores cores)"
Write-Host "  OS:  $os"
Write-Host ""

$binAayuc = "$PSScriptRoot\..\bin\aayuc.exe"
$binVm = "$PSScriptRoot\..\bin\aayu-vm.exe"

$benchmarks = @(
    @{ Name = "Data Crunching (100k loop)"; File = "02_data_crunching.aayu" },
    @{ Name = "Fibonacci Recursion (15 levels)"; File = "01_compute_stress.aayu" }
)

$results = @()

foreach ($bench in $benchmarks) {
    $srcPath = Join-Path $PSScriptRoot $bench.File
    $aycPath = Join-Path $PSScriptRoot ($bench.File -replace '\.aayu$', '.ayc')

    # Compile
    & $binAayuc $srcPath -o $aycPath | Out-Null
    if (-not (Test-Path $aycPath)) {
        Write-Host "Failed to compile $($bench.Name)" -ForegroundColor Red
        continue
    }

    # Warmup
    & $binVm $aycPath | Out-Null

    # 5 Iterations
    $times = @()
    for ($i = 1; $i -le 5; $i++) {
        $sw = [System.Diagnostics.Stopwatch]::StartNew()
        & $binVm $aycPath | Out-Null
        $sw.Stop()
        $times += $sw.Elapsed.TotalMilliseconds
    }

    $sorted = $times | Sort-Object
    $min = [math]::Round($sorted[0], 2)
    $max = [math]::Round($sorted[-1], 2)
    $median = [math]::Round($sorted[2], 2)
    $avg = [math]::Round(($times | Measure-Object -Average).Average, 2)

    Write-Host "Bench: $($bench.Name)" -ForegroundColor Green
    Write-Host "  Median: ${median}ms | Min: ${min}ms | Max: ${max}ms | Mean: ${avg}ms"

    $results += [PSCustomObject]@{
        Benchmark = $bench.Name
        MedianMs  = $median
        MinMs     = $min
        MaxMs     = $max
        MeanMs    = $avg
    }

    Remove-Item $aycPath -Force -ErrorAction SilentlyContinue
}

# Category B: Pure In-Process Micro-Execution Timing (1M loop, zero OS process startup)
Write-Host ""
Write-Host "Category B: In-Process Micro-Execution (1M iterations):" -ForegroundColor Magenta
$vmSumOut = & $binVm --sum 1000000 2>&1 | Out-String
$vmNsMatch = [regex]::Match($vmSumOut, 'AAYU_VM_NS\s+(\d+)')
$vmNs = if ($vmNsMatch.Success) { [int64]$vmNsMatch.Groups[1].Value } else { 0 }
$vmMs = [math]::Round($vmNs / 1000000.0, 2)
$vmPerOp = [math]::Round($vmNs / 1000000.0, 2)
Write-Host "  VM Interpreter (1M loop): ${vmMs} ms (${vmPerOp} ns/op)"

$jitSumOut = & $binVm --sum 1000000 --jit 2>&1 | Out-String
$jitNsMatch = [regex]::Match($jitSumOut, 'AAYU_VM_NS\s+(\d+)')
$jitNs = if ($jitNsMatch.Success) { [int64]$jitNsMatch.Groups[1].Value } else { 0 }
$jitMs = [math]::Round($jitNs / 1000000.0, 2)
$jitPerOp = [math]::Round($jitNs / 1000000.0, 2)
Write-Host "  Native JIT Engine (1M loop): ${jitMs} ms (${jitPerOp} ns/op)"

# Run Pure C baseline if present
$cBench = Join-Path $PSScriptRoot "bench_pure_c.exe"
$cMs = 0
$cPerOp = 0
if (Test-Path $cBench) {
    $cOut = & $cBench | Out-String
    $cNsMatch = [regex]::Match($cOut, 'PURE_C_NS:\s+(\d+)')
    if ($cNsMatch.Success) {
        $cNs = [int64]$cNsMatch.Groups[1].Value
        $cMs = [math]::Round($cNs / 1000000.0, 2)
        $cPerOp = [math]::Round($cNs / 10000000.0, 2)
    }
    Write-Host "  Pure C Baseline (10M loop): ${cMs} ms (${cPerOp} ns/op)" -ForegroundColor Magenta
}

# Write results markdown
$reportPath = Join-Path $PSScriptRoot "BENCHMARK_RESULTS.md"
$lines = @()
$lines += "# AAYU Reproducible Benchmark Report"
$lines += ""
$lines += "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$lines += ""
$lines += "## Test Environment"
$lines += "- **CPU**: $cpu ($cores cores)"
$lines += "- **OS**: $os"
$lines += "- **Architecture**: x86_64"
$lines += "- **VM Engine**: AAYU Silicon VM (Rust v0.3.1, opt-level=3, LTO=fat)"
$lines += ""
$lines += "## Category A: End-to-End Cold Execution (Wall-Clock)"
$lines += "> **Scope:** Measures full process boot, dynamic linking, file IO, bytecode verification, and execution."
$lines += ""
$lines += "| Benchmark Scenario | Median (ms) | Min (ms) | Max (ms) | Mean (ms) |"
$lines += "|---|---|---|---|---|"
foreach ($r in $results) {
    $lines += "| **$($r.Benchmark)** | $($r.MedianMs) | $($r.MinMs) | $($r.MaxMs) | $($r.MeanMs) |"
}
$lines += ""
$lines += "## Category B: In-Process Micro-Execution (Pure Dispatch)"
$lines += "> **Scope:** Measures pure instruction dispatch latency inside the VM engine without OS process startup overhead."
$lines += ""
$lines += "| Engine Mode | Iterations | Time (ms) | Per-Op Latency |"
$lines += "|---|---|---|---|"
$lines += "| **Silicon VM (Interpreter)** | 1,000,000 | ${vmMs} ms | ~${vmPerOp} ns/op |"
$lines += "| **Silicon VM (Native JIT)** | 1,000,000 | ${jitMs} ms | ~${jitPerOp} ns/op |"
if ($cMs -gt 0) {
    $lines += "| **Pure C Baseline (-O2)** | 10,000,000 | ${cMs} ms | ~${cPerOp} ns/op |"
}
$lines += ""
$lines += "## Reproducibility"
$lines += "To reproduce these measurements on your machine:"
$lines += '```powershell'
$lines += 'powershell -ExecutionPolicy Bypass -File benchmarks/run_benchmarks.ps1'
$lines += '```'

$lines -join "`r`n" | Out-File -FilePath $reportPath -Encoding utf8
Write-Host ""
Write-Host "Benchmark report generated: $reportPath" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
