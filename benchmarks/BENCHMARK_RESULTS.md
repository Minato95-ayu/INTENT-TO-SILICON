# AAYU Reproducible Benchmark Report

Generated: 2026-10-12 02:27:35

## Test Environment
- **CPU**: Intel(R) Core(TM) i5-8350U CPU @ 1.70GHz (4 cores)
- **OS**: Microsoft Windows 11 Home
- **Architecture**: x86_64
- **VM Engine**: AAYU Silicon VM (Rust v0.3.1, opt-level=3, LTO=fat)

## Category A: End-to-End Cold Execution (Wall-Clock)
> **Scope:** Measures full process boot, dynamic linking, file IO, bytecode verification, and execution.

| Benchmark Scenario | Median (ms) | Min (ms) | Max (ms) | Mean (ms) |
|---|---|---|---|---|
| **Data Crunching (100k loop)** | 169.73 | 145.24 | 213.95 | 178.8 |
| **Fibonacci Recursion (15 levels)** | 82.94 | 82.11 | 86.3 | 83.7 |

## Category B: In-Process Micro-Execution (Pure Dispatch)
> **Scope:** Measures pure instruction dispatch latency inside the VM engine without OS process startup overhead.

| Engine Mode | Iterations | Time (ms) | Per-Op Latency |
|---|---|---|---|
| **Silicon VM (Interpreter)** | 1,000,000 | 713.71 ms | ~713707.9 ns/op |
| **Silicon VM (Native JIT)** | 1,000,000 | 47.98 ms | ~47984.7 ns/op |
| **Pure C Baseline (-O2)** | 10,000,000 | 220.83 ms | ~3.2 ns/op |

## Reproducibility
To reproduce these measurements on your machine:
```powershell
powershell -ExecutionPolicy Bypass -File benchmarks/run_benchmarks.ps1
```
