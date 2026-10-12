# AAYU Compiler and Runtime Confidence Report

> **Review date:** 12 October 2026
> **Scope:** Windows x86_64 repository audit and local Release build. This is not a security certification or cross-platform release sign-off.

## Summary

AAYU has a functioning Rust bytecode VM and Rust bootstrap compiler for a small, tested core language. It is **not self-hosted**: current `.aayu` execution invokes `compiler_bootstrap/` (Rust) and then `runtime_rs/` (Rust). Two AAYU source probes now compile and run, but no AAYU compiler stage yet replaces the production Rust bootstrap.

The tested language subset now includes user-defined `action` calls, positional parameters, local frames, returns, recursion, global variables, relative source-file imports, array/dictionary literals, indexed reads, and `len`, alongside scalar expressions, comparisons, `if`/`else`, `while`, and `print`. Package resolution does not exist. See the [full repository audit](REPOSITORY_AUDIT.md) and [known limitations](KNOWN_LIMITATIONS.md).

## Current verification

- `cargo test --manifest-path runtime_rs/Cargo.toml`: 4 passed, including signed 48-bit integer, negative float, overflow-range, and JSON persistence tests.
- `cargo test --manifest-path compiler_bootstrap/Cargo.toml`: 8 passed, including import cycle/missing path/absolute path rejection, HTML escaping, function arity checks, integer range checking, and multibyte UTF-8.
- Release builds completed for the Rust executables; `bin/aayuc.exe` was refreshed with relative import support. The VM binaries were unchanged in this step.
- `tests/run_tests.ps1`: 11/11 AAYU examples pass exact output checks in normal and `--jit` CLI modes; 8/8 malformed-bytecode cases rejected in interpreter and JIT modes; both AAYU self-host probes pass. The module regression is included in those 11 examples.
- The function regression `tests/test_06_functions.aayu` runs recursive factorial and produces `120`; array and dictionary regressions check indexing, `len`, and missing-key behavior.
- `compiler/lexer.aayu` compiled and ran its tokenization sample. `compiler/compiler.aayu` compiled and ran its demo, but the emitted bytecode has not passed equivalence tests against the Rust compiler.
- `benchmarks/run_workload_matrix.ps1 -Trials 11`: all 20 checked scalar workload patterns passed expected-output verification on warmup and 11 trials; results are in [`benchmarks/BENCHMARK_MATRIX_RESULTS.md`](benchmarks/BENCHMARK_MATRIX_RESULTS.md). Timings show notable run-to-run system noise and are not language-wide performance claims.
- `npx tsc --noEmit` in `website/`: passed. Source JS/JSON and the regenerated VSIX manifest were integrity-checked. The VS Code app itself was not launched in this environment.

## Known implementation limits

- Basic action calls, relative source-file imports, and collection operations are runnable. AAYU package management and the drafted standard library are not verified runnable APIs.
- The 48-bit integer payload accepts `-140737488355328..=140737488355327`; literals outside are rejected and arithmetic overflow produces a runtime error.
- The VM’s Rust DB module is a JSON key/value store, not SQL/SQLite. Rust UI/network/tensor code is not generally exposed as AAYU library modules.
- HTTP server TLS/proxy support and AI/ML/vision/RAG/crypto package claims are incomplete or illustrative; do not use demos as production integrations.
- The optional C emitter produces wrong results for typed values. The CLI disables it for bytecode execution until differential conformance tests pass. `--sum` measures generated C directly and is not VM JIT performance.
- Release workflows package multiple platforms, but CI currently verifies Windows and Linux; macOS release behavior was not tested here.
- AAYU Studio has no verified release build or AAYU VM integration. Its synthetic “training” action is disabled in the UI and unregistered.

## Environment-limited checks

Website TypeScript checking passed, but the production Next.js build stopped after compilation when its worker hit `spawn EPERM`. AAYU Studio's offline Cargo check could not resolve the uncached `dirs` crate, and its npm dependencies are unavailable. Installer scripts were parsed but not executed because they change the user install directory and `PATH`; the VSIX archive was checked structurally, but VS Code was not launched.

See the audit report for detailed evidence and prioritized next steps.
