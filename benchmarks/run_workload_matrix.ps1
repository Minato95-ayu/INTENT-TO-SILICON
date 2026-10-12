param([int]$Trials = 5)

$ErrorActionPreference = 'Stop'
if ($Trials -lt 3) { throw 'Use at least 3 trials for a useful median.' }

$vm = Join-Path $PSScriptRoot '..\bin\aayu-vm.exe'
$compiler = Join-Path $PSScriptRoot '..\bin\aayuc.exe'
if (-not (Test-Path $vm) -or -not (Test-Path $compiler)) {
    throw 'Build runtime_rs and compiler_bootstrap, then put aayu-vm.exe and aayuc.exe in bin/.'
}

$cpu = $env:PROCESSOR_IDENTIFIER
if ([string]::IsNullOrWhiteSpace($cpu)) { $cpu = 'Unavailable (PROCESSOR_IDENTIFIER unset)' }
$os = [System.Runtime.InteropServices.RuntimeInformation]::OSDescription
$arch = [System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture
$n = 10000
$workloads = @(
    @{ Name = 'Integer addition accumulator'; Build = { param($n) "let i = 0`nlet sum = 0`nwhile i < $n`n    sum = sum + i`n    i = i + 1`nend`nprint(sum)`n" }; Expected = { param($n) [string]([long]$n * ($n - 1) / 2) } },
    @{ Name = 'Integer subtraction countdown'; Build = { param($n) "let i = $n`nwhile i > 0`n    i = i - 1`nend`nprint(i)`n" }; Expected = { param($n) '0' } },
    @{ Name = 'Integer multiply-accumulate'; Build = { param($n) "let i = 0`nlet sum = 0`nwhile i < $n`n    sum = sum + i * 3`n    i = i + 1`nend`nprint(sum)`n" }; Expected = { param($n) [string](3 * [long]$n * ($n - 1) / 2) } },
    @{ Name = 'Integer divide-accumulate'; Build = { param($n) "let i = 0`nlet sum = 0`nwhile i < $n`n    sum = sum + i / 2`n    i = i + 1`nend`nprint(sum)`n" }; Expected = { param($n) [string]([long]$n * ($n - 2) / 4) } },
    @{ Name = 'Float half-step accumulation'; Build = { param($n) "let i = 0`nlet total = 0.0`nwhile i < $n`n    total = total + 0.5`n    i = i + 1`nend`nprint(total)`n" }; Expected = { param($n) [string]($n / 2) } },
    @{ Name = 'Float multiply-accumulate'; Build = { param($n) "let i = 0`nlet total = 0.0`nwhile i < $n`n    total = total + i * 0.5`n    i = i + 1`nend`nprint(total)`n" }; Expected = { param($n) [string]([long]$n * ($n - 1) / 4) } },
    @{ Name = 'Less-than true branch'; Build = { param($n) $h=$n/2; "let i = 0`nlet sum = 0`nwhile i < $n`n    if i < $h`n        sum = sum + 1`n    end`n    i = i + 1`nend`nprint(sum)`n" }; Expected = { param($n) [string]($n/2) } },
    @{ Name = 'Greater-than true branch'; Build = { param($n) $h=$n/2; "let i = 0`nlet sum = 0`nwhile i < $n`n    if i > $h`n        sum = sum + 1`n    end`n    i = i + 1`nend`nprint(sum)`n" }; Expected = { param($n) [string]($n/2-1) } },
    @{ Name = 'Equality branch'; Build = { param($n) $h=$n/2; "let i = 0`nlet sum = 0`nwhile i < $n`n    if i == $h`n        sum = sum + 1`n    end`n    i = i + 1`nend`nprint(sum)`n" }; Expected = { param($n) '1' } },
    @{ Name = 'Inequality branch'; Build = { param($n) $h=$n/2; "let i = 0`nlet sum = 0`nwhile i < $n`n    if i != $h`n        sum = sum + 1`n    end`n    i = i + 1`nend`nprint(sum)`n" }; Expected = { param($n) [string]($n-1) } },
    @{ Name = 'Less-or-equal branch'; Build = { param($n) $h=$n/2; "let i = 0`nlet sum = 0`nwhile i < $n`n    if i <= $h`n        sum = sum + 1`n    end`n    i = i + 1`nend`nprint(sum)`n" }; Expected = { param($n) [string]($n/2+1) } },
    @{ Name = 'Greater-or-equal branch'; Build = { param($n) $h=$n/2; "let i = 0`nlet sum = 0`nwhile i < $n`n    if i >= $h`n        sum = sum + 1`n    end`n    i = i + 1`nend`nprint(sum)`n" }; Expected = { param($n) [string]($n/2) } },
    @{ Name = 'Nested loop counter'; Build = { param($n) $outer=$n/100; "let i = 0`nlet sum = 0`nwhile i < $outer`n    let j = 0`n    while j < 100`n        sum = sum + 1`n        j = j + 1`n    end`n    i = i + 1`nend`nprint(sum)`n" }; Expected = { param($n) [string]$n } },
    @{ Name = 'Nested loop weighted sum'; Build = { param($n) $outer=$n/100; "let i = 0`nlet sum = 0`nwhile i < $outer`n    let j = 0`n    while j < 100`n        sum = sum + i`n        j = j + 1`n    end`n    i = i + 1`nend`nprint(sum)`n" }; Expected = { param($n) [string](100 * [long]($n/100) * (($n/100)-1) / 2) } },
    @{ Name = 'Mixed multiply and subtract'; Build = { param($n) "let i = 0`nlet sum = 0`nwhile i < $n`n    sum = sum + i * 2 - i`n    i = i + 1`nend`nprint(sum)`n" }; Expected = { param($n) [string]([long]$n * ($n - 1) / 2) } },
    @{ Name = 'Multiply then divide'; Build = { param($n) "let i = 0`nlet sum = 0`nwhile i < $n`n    sum = sum + i * 10 / 2`n    i = i + 1`nend`nprint(sum)`n" }; Expected = { param($n) [string](5 * [long]$n * ($n - 1) / 2) } },
    @{ Name = 'Descending sum'; Build = { param($n) "let i = $n`nlet sum = 0`nwhile i > 0`n    sum = sum + i`n    i = i - 1`nend`nprint(sum)`n" }; Expected = { param($n) [string]([long]$n * ($n + 1) / 2) } },
    @{ Name = 'Variable copy and accumulate'; Build = { param($n) "let i = 0`nlet current = 0`nlet sum = 0`nwhile i < $n`n    current = i`n    sum = sum + current`n    i = i + 1`nend`nprint(sum)`n" }; Expected = { param($n) [string]([long]$n * ($n - 1) / 2) } },
    @{ Name = 'Nested conditional branches'; Build = { param($n) $h=$n/2; "let i = 0`nlet sum = 0`nwhile i < $n`n    if i < $h`n        sum = sum + 1`n    else`n        if i == $h`n            sum = sum + 2`n        else`n            sum = sum + 3`n        end`n    end`n    i = i + 1`nend`nprint(sum)`n" }; Expected = { param($n) [string]($n*2-1) } },
    @{ Name = 'Comparison loop boundary'; Build = { param($n) "let i = 1`nlet sum = 0`nwhile i <= $n`n    sum = sum + i`n    i = i + 1`nend`nprint(sum)`n" }; Expected = { param($n) [string]([long]$n * ($n + 1) / 2) } }
)

$tempRoot = Join-Path ([IO.Path]::GetTempPath()) ("aayu-bench-" + [guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($tempRoot) | Out-Null
$results = [System.Collections.Generic.List[object]]::new()

try {
    foreach ($workload in $workloads) {
            $id = '{0:D2}' -f ($results.Count + 1)
            $sourcePath = Join-Path $tempRoot "workload_$id.aayu"
            $bytecodePath = Join-Path $tempRoot "workload_$id.ayc"
            $source = & $workload.Build $n
            [IO.File]::WriteAllText($sourcePath, $source, [Text.UTF8Encoding]::new($false))

            & $compiler $sourcePath -o $bytecodePath | Out-Null
            if ($LASTEXITCODE -ne 0 -or -not (Test-Path $bytecodePath)) { throw "Compile failed: $($workload.Name), N=$n" }

            $expected = & $workload.Expected $n
            $warmup = @(& $vm $bytecodePath 2>&1 | ForEach-Object { "$($_)".Trim() })
            if ($LASTEXITCODE -ne 0 -or $warmup[-1] -ne $expected) {
                throw "Correctness check failed: $($workload.Name), N=$n; expected '$expected', got '$($warmup[-1])'"
            }

            $times = [System.Collections.Generic.List[double]]::new()
            for ($trial = 1; $trial -le $Trials; $trial++) {
                $watch = [Diagnostics.Stopwatch]::StartNew()
                $output = @(& $vm $bytecodePath 2>&1 | ForEach-Object { "$($_)".Trim() })
                $watch.Stop()
                if ($LASTEXITCODE -ne 0 -or $output[-1] -ne $expected) {
                    throw "Trial failed correctness: $($workload.Name), N=$n, trial=$trial"
                }
                $times.Add($watch.Elapsed.TotalMilliseconds)
            }

            $sorted = @($times | Sort-Object)
            $median = [math]::Round($sorted[[int][math]::Floor($Trials / 2)], 3)
            $results.Add([pscustomobject]@{
                Workload = $workload.Name
                N = $n
                Expected = $expected
                Trials = $Trials
                MedianMs = $median
                MinMs = [math]::Round($sorted[0], 3)
                MaxMs = [math]::Round($sorted[-1], 3)
            })
            Write-Host ("PASS {0}: median {1} ms, output {2}" -f $workload.Name, $median, $expected)
    }
}
finally {
    Get-ChildItem -LiteralPath $tempRoot -File -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $tempRoot -Force -ErrorAction SilentlyContinue
}

$report = @(
    '# AAYU Core Workload Matrix',
    '',
    "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')",
    '',
    "Environment: $os | $arch | $cpu | $([Environment]::ProcessorCount) logical processors",
    "VM: Rust crate v0.3.1. Process wall-clock timings include VM process startup and bytecode loading; compiler time is excluded. Each case is warmed once and then measured for $Trials trials. Output is checked against the expected result on warmup and every trial.",
    '',
    'These are 20 distinct code patterns from the currently supported core subset, each measured with N=10,000. This is not a comparison against other languages. Results vary by machine and build.',
    '',
    '| # | Workload | N | Expected output | Median ms | Min ms | Max ms |',
    '|---:|---|---:|---:|---:|---:|---:|'
)
for ($i = 0; $i -lt $results.Count; $i++) {
    $r = $results[$i]
    $report += "| $($i + 1) | $($r.Workload) | $($r.N) | $($r.Expected) | $($r.MedianMs) | $($r.MinMs) | $($r.MaxMs) |"
}
$report += ''
$report += 'Reproduce on Windows: `powershell -ExecutionPolicy Bypass -File benchmarks/run_workload_matrix.ps1`'
$reportPath = Join-Path $PSScriptRoot 'BENCHMARK_MATRIX_RESULTS.md'
[IO.File]::WriteAllText($reportPath, ($report -join "`r`n") + "`r`n", [Text.UTF8Encoding]::new($false))
Write-Host "Wrote $($results.Count) checked workload measurements to $reportPath"
