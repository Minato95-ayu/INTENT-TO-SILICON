# AAYU Core Workload Matrix

Generated: 2026-10-12 19:50:25 +05:30

Environment: Microsoft Windows 10.0.26300  | X64 | Intel64 Family 6 Model 142 Stepping 10, GenuineIntel | 8 logical processors
VM: Rust crate v0.3.1. Process wall-clock timings include VM process startup and bytecode loading; compiler time is excluded. Each case is warmed once and then measured for 11 trials. Output is checked against the expected result on warmup and every trial.

These are 20 distinct code patterns from the currently supported core subset, each measured with N=10,000. This is not a comparison against other languages. Results vary by machine and build.

| # | Workload | N | Expected output | Median ms | Min ms | Max ms |
|---:|---|---:|---:|---:|---:|---:|
| 1 | Integer addition accumulator | 10000 | 49995000 | 73.546 | 70.314 | 199.249 |
| 2 | Integer subtraction countdown | 10000 | 0 | 74.215 | 70.876 | 155.731 |
| 3 | Integer multiply-accumulate | 10000 | 149985000 | 76.679 | 74.669 | 91.06 |
| 4 | Integer divide-accumulate | 10000 | 24995000 | 112.868 | 87.982 | 163.001 |
| 5 | Float half-step accumulation | 10000 | 5000 | 75.452 | 70.692 | 77.032 |
| 6 | Float multiply-accumulate | 10000 | 24997500 | 73.279 | 70.933 | 77.946 |
| 7 | Less-than true branch | 10000 | 5000 | 72.851 | 71.212 | 77.565 |
| 8 | Greater-than true branch | 10000 | 4999 | 72.784 | 72.227 | 77.527 |
| 9 | Equality branch | 10000 | 1 | 73.867 | 70.723 | 78.43 |
| 10 | Inequality branch | 10000 | 9999 | 74.745 | 71.805 | 78.093 |
| 11 | Less-or-equal branch | 10000 | 5001 | 72.496 | 71.005 | 76.236 |
| 12 | Greater-or-equal branch | 10000 | 5000 | 73.431 | 70.292 | 77.896 |
| 13 | Nested loop counter | 10000 | 10000 | 76.886 | 70.722 | 80.723 |
| 14 | Nested loop weighted sum | 10000 | 495000 | 73.169 | 69.788 | 81.36 |
| 15 | Mixed multiply and subtract | 10000 | 49995000 | 73.878 | 72.859 | 99.137 |
| 16 | Multiply then divide | 10000 | 249975000 | 74.592 | 70.753 | 82.061 |
| 17 | Descending sum | 10000 | 50005000 | 75.985 | 72.07 | 86.114 |
| 18 | Variable copy and accumulate | 10000 | 49995000 | 73.45 | 69.887 | 99.145 |
| 19 | Nested conditional branches | 10000 | 19999 | 74.717 | 72.385 | 78.386 |
| 20 | Comparison loop boundary | 10000 | 50005000 | 71.639 | 70.375 | 77.727 |

Reproduce on Windows: `powershell -ExecutionPolicy Bypass -File benchmarks/run_workload_matrix.ps1`
