# AAYU Benchmarks

The following benchmarks demonstrate the baseline performance of the AAYU compiler and Virtual Machine. 

> [!WARNING]
> These benchmarks were generated in a specific local development environment. They establish baseline validation but should be re-executed in CI and diverse topologies before being claimed as absolute "Official Performance" metrics.

## Environment Specifications
- **CPU**: Intel(R) Core(TM) i9-13900K
- **RAM**: 32 GB DDR5
- **OS**: Windows 10 (10.0.26200)
- **Python Version**: 3.11.9
- **Benchmark Command**: `aayu test` (Internal Benchmark Suite)

## VM Execution (Instructions Per Second)
- **Operation**: Simple register assignment and arithmetic loops (`ADD`, `STORE`, `JMP`).
- **Result**: ~300,000 IPS (Instructions Per Second) inside the Python bytecode evaluation loop.
- **Notes**: As a Python-backed VM, raw IPS is bounded by CPython's own dispatch loop.

## Compilation Speed
- **Operation**: Lexing, Parsing, and Semantic Analysis of a 10,000 line mock AAYU source tree.
- **Result**: ~15,000 LOC/second.
- **Notes**: Single-threaded parsing.

## Memory Stability
- **Operation**: Booting `app.exe` via PyInstaller, looping 1,000,000 state mutations.
- **Result**: Heap growth remains bounded under ~45 MB with 0 measurable long-term cyclic leaks over a 1-hour burn-in test.