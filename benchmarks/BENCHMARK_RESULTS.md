# AAYU Reproducible Benchmark Report

Generated: 2026-10-12 04:21:17

## Test Environment
- **CPU**: Intel(R) Core(TM) i5-8350U CPU @ 1.70GHz (4 cores)
- **OS**: Microsoft Windows 11 Home
- **Architecture**: x86_64
- **VM Engine**: AAYU Silicon VM (Rust v0.3.1, opt-level=3, LTO=fat)

## Category A: End-to-End Cold Execution (Wall-Clock)
> **Scope:** Measures full process boot, dynamic linking, file IO, bytecode verification, and execution.

| Benchmark Scenario | Median (ms) | Min (ms) | Max (ms) | Mean (ms) |
|---|---|---|---|---|
| **Data Crunching (100k loop)** | 128.26 | 120.38 | 137.45 | 128.66 |
| **Fibonacci Recursion (15 levels)** | 83.78 | 70.1 | 85.42 | 80.75 |

## Category B: In-Process Micro-Execution (Pure Dispatch)
> **Scope:** Measures pure instruction dispatch latency inside the VM engine without OS process startup overhead.

| Engine Mode | Iterations | Time (ms) | Per-Op Latency |
|---|---|---|---|
| **Silicon VM (Interpreter)** | 1,000,000 | 619.59 ms | ~619.59 ns/op |
| **Silicon VM (Native JIT)** | 1,000,000 | 24.22 ms | ~24.22 ns/op |
| **Pure C Baseline (-O2)** | 10,000,000 | 76.62 ms | ~7.66 ns/op |

## Reproducibility
To reproduce these measurements on your machine:
```powershell
powershell -ExecutionPolicy Bypass -File benchmarks/run_benchmarks.ps1
```
