# AAYU Reproducible Benchmarking Suite
# Measures VM process wall-clock and hand-built sum-loop kernels

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "      AAYU REPRODUCIBLE BENCHMARK RUNNER          " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$cpu = $env:PROCESSOR_IDENTIFIER
if ([string]::IsNullOrWhiteSpace($cpu)) { $cpu = "Unavailable (PROCESSOR_IDENTIFIER unset)" }
$os = [System.Runtime.InteropServices.RuntimeInformation]::OSDescription.Trim()
$cores = [Environment]::ProcessorCount

Write-Host "Hardware Context:" -ForegroundColor Yellow
Write-Host "  CPU: $cpu ($cores cores)"
Write-Host "  OS:  $os"
Write-Host ""

$binAayuc = "$PSScriptRoot\..\bin\aayuc.exe"
$binVm = "$PSScriptRoot\..\bin\aayu-vm.exe"

$benchmarks = @(
    @{ Name = "Integer accumulation (100k iterations)"; File = "02_data_crunching.aayu"; Expected = @("Data Crunching Complete. Sum:", "4999950000") },
    @{ Name = "Iterative Fibonacci (15 steps)"; File = "01_compute_stress.aayu"; Expected = @("610", "PASS: fib(15) is 610") }
)

$results = @()

foreach ($bench in $benchmarks) {
    $srcPath = Join-Path $PSScriptRoot $bench.File
    $aycPath = Join-Path $PSScriptRoot ($bench.File -replace '\.aayu$', '.ayc')

    # Compile
    & $binAayuc $srcPath -o $aycPath | Out-Null
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $aycPath)) {
        Write-Host "Failed to compile $($bench.Name)" -ForegroundColor Red
        continue
    }

    # Warmup
    $warmup = @(& $binVm $aycPath 2>&1 | ForEach-Object { "$($_)".TrimEnd() })
    if ($LASTEXITCODE -ne 0) { throw "Warmup failed for $($bench.Name)" }
    if (($warmup -join "`n") -ne ($bench.Expected -join "`n")) { throw "Expected-output check failed for $($bench.Name)" }

    # 5 Iterations
    $times = @()
    for ($i = 1; $i -le 5; $i++) {
        $sw = [System.Diagnostics.Stopwatch]::StartNew()
        $output = @(& $binVm $aycPath 2>&1 | ForEach-Object { "$($_)".TrimEnd() })
        if ($LASTEXITCODE -ne 0) { throw "Execution failed for $($bench.Name)" }
        $sw.Stop()
        if (($output -join "`n") -ne ($bench.Expected -join "`n")) { throw "Output changed during timed run for $($bench.Name)" }
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

# Category B: Hand-built sum-loop microkernel
Write-Host ""
Write-Host "Category B: Sum-loop microkernel diagnostics (1M iterations):" -ForegroundColor Magenta
$vmSumOut = & $binVm --sum 1000000 2>&1 | Out-String
$vmNsMatch = [regex]::Match($vmSumOut, 'AAYU_VM_NS\s+(\d+)')
$vmNs = if ($vmNsMatch.Success) { [int64]$vmNsMatch.Groups[1].Value } else { 0 }
$vmMs = [math]::Round($vmNs / 1000000.0, 2)
$vmPerIteration = [math]::Round($vmNs / 1000000.0, 2)
Write-Host "  VM Interpreter (1M loop iterations): ${vmMs} ms (${vmPerIteration} ns/iteration)"

$jitSumOut = & $binVm --sum 1000000 --jit 2>&1 | Out-String
$jitNsMatch = [regex]::Match($jitSumOut, 'AAYU_VM_NS\s+(\d+)')
$jitNs = if ($jitNsMatch.Success) { [int64]$jitNsMatch.Groups[1].Value } else { 0 }
$jitMs = [math]::Round($jitNs / 1000000.0, 2)
$jitPerIteration = [math]::Round($jitNs / 1000000.0, 2)
Write-Host "  JIT-generated C (1M loop iterations): ${jitMs} ms (${jitPerIteration} ns/iteration)"

# Run Pure C baseline if present
$cBench = Join-Path $PSScriptRoot "bench_pure_c.exe"
$cMs = 0
$cPerIteration = 0
if (Test-Path $cBench) {
    $cTimes = @()
    for ($i = 1; $i -le 5; $i++) {
        $cOut = & $cBench | Out-String
        $cNsMatch = [regex]::Match($cOut, 'PURE_C_NS:\s+(\d+)')
        if (-not $cNsMatch.Success) { throw 'C benchmark output did not contain PURE_C_NS.' }
        $cTimes += [int64]$cNsMatch.Groups[1].Value
    }
    $cSorted = @($cTimes | Sort-Object)
    $cNs = $cSorted[2]
    $cMs = [math]::Round($cNs / 1000000.0, 2)
    $cPerIteration = [math]::Round($cNs / 10000000.0, 2)
    Write-Host "  Standalone C (-O2, 10M iterations): ${cMs} ms (${cPerIteration} ns/iteration)" -ForegroundColor Magenta
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
$lines += "- **Architecture**: $([System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture)"
$lines += "- **VM Engine**: AAYU Silicon VM (Rust v0.3.1, opt-level=3, LTO=fat)"
$lines += ""
$lines += "## Category A: AAYU VM process execution"
$lines += "> **Scope:** Measures launching the VM on previously compiled bytecode, including process startup and bytecode loading. Compilation is excluded. One warm-up is discarded; each median/min/max/mean is from five launches. These are correctness-checked against expected output."
$lines += ""
$lines += "| Benchmark Scenario | Median (ms) | Min (ms) | Max (ms) | Mean (ms) |"
$lines += "|---|---|---|---|---|"
foreach ($r in $results) {
    $lines += "| **$($r.Benchmark)** | $($r.MedianMs) | $($r.MinMs) | $($r.MaxMs) | $($r.MeanMs) |"
}
$lines += ""
$lines += "## Category B: Sum-loop microkernels"
$lines += "> **Scope:** Measures a hand-built sum-loop bytecode kernel in-process. This is not general application throughput; each iteration executes multiple bytecode instructions. The JIT path compiles equivalent generated C and times that C loop, so it is not a VM JIT dispatch measurement."
$lines += ""
$lines += "| Engine / kernel | Loop iterations | Time (ms) | Per-iteration time |"
$lines += "|---|---|---|---|"
$lines += "| **AAYU VM interpreter** | 1,000,000 | ${vmMs} ms | ~${vmPerIteration} ns/iteration |"
$lines += "| **JIT-generated C kernel** | 1,000,000 | ${jitMs} ms | ~${jitPerIteration} ns/iteration |"
if ($cMs -gt 0) {
$lines += "| **Standalone C (-O2) kernel** | 10,000,000 | ${cMs} ms | ~${cPerIteration} ns/iteration |"
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
