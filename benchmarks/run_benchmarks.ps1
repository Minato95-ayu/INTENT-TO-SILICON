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

# Run Pure C baseline if present
$cBench = Join-Path $PSScriptRoot "bench_pure_c.exe"
if (Test-Path $cBench) {
    $cOut = & $cBench
    Write-Host ""
    Write-Host "Pure C Baseline (10M loop):" -ForegroundColor Magenta
    $cOut | ForEach-Object { Write-Host "  $_" }
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
$lines += "## Benchmark Measurements (5 Iterations, Post-Warmup)"
$lines += ""
$lines += "| Benchmark Scenario | Median (ms) | Min (ms) | Max (ms) | Mean (ms) |"
$lines += "|---|---|---|---|---|"
foreach ($r in $results) {
    $lines += "| **$($r.Benchmark)** | $($r.MedianMs) | $($r.MinMs) | $($r.MaxMs) | $($r.MeanMs) |"
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
