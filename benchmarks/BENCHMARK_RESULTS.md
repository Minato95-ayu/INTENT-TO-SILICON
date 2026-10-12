# AAYU Reproducible Benchmark Report

Generated: 2026-10-12 14:32:06

## Test Environment
- **CPU**: Intel64 Family 6 Model 142 Stepping 10, GenuineIntel (8 cores)
- **OS**: Microsoft Windows 10.0.26300
- **Architecture**: X64
- **VM Engine**: AAYU Silicon VM (Rust v0.3.1, opt-level=3, LTO=fat)

## Category A: AAYU VM process execution
> **Scope:** Measures launching the VM on previously compiled bytecode, including process startup and bytecode loading. Compilation is excluded. One warm-up is discarded; each median/min/max/mean is from five launches. These are correctness-checked against expected output.

| Benchmark Scenario | Median (ms) | Min (ms) | Max (ms) | Mean (ms) |
|---|---|---|---|---|
| **Integer accumulation (100k iterations)** | 717.74 | 400.11 | 865.82 | 671.99 |
| **Iterative Fibonacci (15 steps)** | 195.25 | 141.31 | 219.71 | 186.95 |

## Category B: Sum-loop microkernels
> **Scope:** Measures a hand-built sum-loop bytecode kernel in-process. This is not general application throughput; each iteration executes multiple bytecode instructions. The JIT path compiles equivalent generated C and times that C loop, so it is not a VM JIT dispatch measurement.

| Engine / kernel | Loop iterations | Time (ms) | Per-iteration time |
|---|---|---|---|
| **AAYU VM interpreter** | 1,000,000 | 2143.16 ms | ~2143.16 ns/iteration |
| **JIT-generated C kernel** | 1,000,000 | 70.91 ms | ~70.91 ns/iteration |
| **Standalone C (-O2) kernel** | 10,000,000 | 272.07 ms | ~27.21 ns/iteration |

## Reproducibility
To reproduce these measurements on your machine:
```powershell
powershell -ExecutionPolicy Bypass -File benchmarks/run_benchmarks.ps1
```
