# AAYU Reproducible Benchmark Report

Generated: 2026-10-12 02:04:31

## Test Environment
- **CPU**: Intel(R) Core(TM) i5-8350U CPU @ 1.70GHz (4 cores)
- **OS**: Microsoft Windows 11 Home
- **Architecture**: x86_64
- **VM Engine**: AAYU Silicon VM (Rust v0.3.1, opt-level=3, LTO=fat)

## Benchmark Measurements (5 Iterations, Post-Warmup)

| Benchmark Scenario | Median (ms) | Min (ms) | Max (ms) | Mean (ms) |
|---|---|---|---|---|
| **Data Crunching (100k loop)** | 161.19 | 146.76 | 311.3 | 188.24 |
| **Fibonacci Recursion (15 levels)** | 83.82 | 77.87 | 87.14 | 83.66 |

## Reproducibility
To reproduce these measurements on your machine:
```powershell
powershell -ExecutionPolicy Bypass -File benchmarks/run_benchmarks.ps1
```
