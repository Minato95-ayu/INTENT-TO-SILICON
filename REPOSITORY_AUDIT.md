# AAYU Repository Audit

**Reviewed:** 12 October 2026  
**Scope:** Rust VM/bootstrap compiler, AAYU source pipeline, standard-library and package samples, CLI/installers, benchmarks, website docs, VS Code extension, and AAYU Studio prototype.  
**Environment:** Windows x86_64; fresh local Rust release builds. This is a functional repository review, not a security audit or cross-platform release certification.

## What works now

- `bin/aayu.exe` / `bin/aayu-vm.exe` runs `.aayu` by invoking the separate `bin/aayuc.exe`, then verifies and executes `.ayc` bytecode in the Rust VM.
- The checked core subset is declarations, reassignment, integer/float/string expressions, comparisons, `if`/`else`, `while`, and `print`. The regression set verifies six programs with expected outputs.
- The VM has a bytecode verifier; eight malformed-bytecode cases were rejected in interpreter and `--jit` modes.
- Release archives are designed to include both the VM and bootstrap compiler. The Windows local Release build was run from `bin/`; the release workflow also defines Linux and macOS archives.
- The benchmark matrix contains 20 distinct scalar-code patterns. The current recorded run checks every expected output on warmup and all 11 trials. Timings include a new VM process and bytecode loading, with compilation excluded; recorded values vary substantially with system load.
- The VS Code extension now provides syntax highlighting, snippets, and a **Run Current File** command. It has no language server or debugger.

## Major gaps found

| Area | Current evidence | Status |
|---|---|---|
| Self-hosting | `compiler/lexer.aayu` now compiles and runs; `compiler/compiler.aayu` compiles and its demonstration emits a bytecode array. | Production `.aayu` execution still uses the Rust bootstrap compiler. No end-to-end emitted-bytecode equivalence or reproducible self-hosting stage has been demonstrated. |
| Functions/actions | `action add(a,b)` previously ran and returned the last argument (`3` instead of `5`). | Added direct-call bytecode targets, isolated 256-slot local frames, positional args, returns, recursion, call-depth limit, and wrong-arity/unknown-function checks. Recursive factorial regression passes. Closures and named/default arguments remain unsupported. |
| Core collections | Added array and dictionary literals, array/dictionary/string reads by index/key, and array/dictionary length through `len`; regression programs cover these operations. | Indexed writes, iteration helpers, and broader collection behavior need more tests. |
| Modules and libraries | The Rust bootstrap compiler now expands relative `import "path.aayu"` statements (optional `.aayu` extension), recursively, once per canonical file. The regression suite verifies duplicate-import deduplication; compiler unit checks reject missing, absolute, and cyclic imports. Imports share one program scope. | Namespaces, aliases, package resolution, and automatic standard-library lookup are absent. `std/` and `official_packages/` remain sketches, not a verified installable package set. |
| HTTP/server/proxy | `runtime_rs/src/net.rs` has a small raw TCP HTTP server and a `ureq` HTTPS client. The TLS certificate fields do not create a TLS listener; `new_with_proxy` stores paths only. The server reads one fixed buffer per connection. | No stable AAYU server/proxy API; do not claim production HTTP/TLS support. |
| UI | The compiler HTML path now escapes widget text and inline style attributes. There is no verified native app/window/event loop wired to AAYU code. The separate Rust UI renderer still serializes caller-provided attributes/text without escaping. | Static HTML/demo path, not a verified native interactive UI toolkit; the Rust UI API still needs escaping. |
| Database | `runtime_rs/src/db.rs` is a JSON-backed key/value store; flush uses a synced same-directory temporary file and replace. | Escaping and persistence round-trip are tested. It is not SQLite/SQL/WAL, has no multi-process writer coordination, `set_json` suppresses flush errors, and it is not an AAYU-importable module. |
| Math, crypto, AI/ML, vision, RAG | There is a Rust tensor type; AAYU-facing drafts call undefined functions. The crypto draft synthesizes digest-looking text, and vision/RAG samples return fixed demo strings. VM demo opcodes contain simulated AI/blockchain narratives. | No verified AAYU math/crypto/ML/LLM/vision/RAG packages. Do not use them for security or real inference. |
| JIT | `--jit` on negative float code produced `0` where the VM produced `-2.5`; the C emitter treats constants as integers and does not compare output with VM results. | The CLI now gates native bytecode execution off and falls back to Rust VM. `--sum` remains a generated-C microkernel diagnostic, not VM JIT throughput. |
| Integer representation | Values use a signed 48-bit payload. Negative values were decoded incorrectly; integers above the range silently truncated. | Sign extension is fixed; compiler rejects out-of-range literals and integer arithmetic returns overflow errors. |
| VS Code | `vscode-aayu` now has syntax/snippets/run-command support; old `editors/vscode` still points to nonexistent `aayu lsp`. | Packaged extension has no diagnostics, autocomplete, hover, or debugger. Studio/extension integration is not a full IDE. |
| AAYU Studio | Tauri/Next prototype uses a Python build-runner default and Cargo-only export. The former “Vertex training” action wrote fabricated fixed scores rather than training. | UI now marks training unavailable and command is unregistered. Studio has no verified installer or working AAYU project run integration. |
| CLI and installation | The VM has `run`, `build`, `version`, `help`; source files require the compiler binary. `.ayc` is bytecode, not an EXE. | Old Python package, formatter, linter, scaffold, package manager, BrainOS, and LSP commands are not implemented in the VM CLI. |
| Dependencies | Rust manifests include external crates/build dependencies; the HTTPS client uses `ureq`. AAYU source execution requires two executables. | “Zero dependencies” and “one self-contained AAYU compiler/VM binary” are inaccurate. |

## Benchmark interpretation

The 20 rows are correctness-checked variants of scalar integer/float arithmetic, comparisons, branches, and loops at `N=10,000`. They are useful repeatable smoke/microbenchmarks of this VM build. They are **not** 20 application domains, a cross-language comparison, instruction-throughput numbers, or evidence for game graphics, ML, database, server, crypto, or UI performance. See [`benchmarks/BENCHMARK_MATRIX_RESULTS.md`](benchmarks/BENCHMARK_MATRIX_RESULTS.md) and its runner.

## Fixes made during this review

- Corrected signed 48-bit integer decoding and negative float classification; added range checking for literals and integer operations.
- Made invalid lexer characters, unterminated strings, missing expressions, unknown functions, bad arity, and out-of-scope returns fail compilation instead of producing misleading output.
- Implemented local function frames, direct call targets, recursion, and return-address restoration; added a recursive factorial golden program and bytecode verification for function entries.
- Added unary minus, 48-bit minimum literal support, array/dictionary literal construction, indexed reads, and global slots shared between action calls.
- Escaped JSON quotes, backslashes, and control characters correctly; database flush now syncs a temporary file and replaces the target without truncating the old file first.
- Escaped text and inline style attributes in the compiler's generated HTML path and added a focused escaping regression.
- Ran `compiler/lexer.aayu`; it tokenizes its sample. Ran `compiler/compiler.aayu`; its demonstration prints a generated array, but that output is not yet proven equivalent to Rust compiler bytecode.
- Added a compiler-path override for source-run verification; made CLI compile/read failures return nonzero status; removed false speed, dependency, and standalone-binary claims from VM help.
- Disabled the incorrect CLI native-JIT path pending conformance tests.
- Added a negative integer/float golden-output program and `--jit` fallback parity checks.
- Rebuilt local Windows Release VM/compiler, reran the full test/security harness, and regenerated the 20-case matrix.
- Replaced obsolete getting-started, installation, language, package-manager, and CLI guidance; added explicit status files for `compiler/`, `std/`, `official_packages/`, and `examples/`.
- Disabled the legacy doc generator that used to write stale lesson templates to an absolute path outside the repository.
- Replaced the VS Code extension’s nonexistent language-server/debugger startup with a configurable VM run command and regenerated the downloadable VSIX.
- Disabled/unregistered AAYU Studio’s synthetic model-training control and marked the old fake implementation as retired code.

## Checks limited by this environment

- Website TypeScript checking passes. The production Next.js build compiles but its worker exits with `spawn EPERM` in this environment.
- AAYU Studio's offline Cargo check is blocked because the `dirs` crate is not cached; its npm dependencies are also unavailable here.
- Installer scripts passed PowerShell parsing, but were not run because they modify the user install directory and `PATH`. The VSIX archive was structurally checked, but VS Code itself was not launched.
- The older `editors/vscode` copy still invokes the removed `aayu lsp` command; only `vscode-aayu` is the current extension path.

## Suggested order for future work

1. Freeze a small executable language spec and bytecode version; add parser/compiler tests for every accepted form.
2. Add module/import and package resolution, then validate the design against actual standard-library packages.
3. Build a real standard library API and test it from AAYU programs; only then implement HTTP, DB, UI, math, and crypto packages.
4. Replace simulated AI/chain opcodes with explicit host APIs or remove them; add security review for network/UI surfaces.
5. Restore JIT only after differential VM-vs-C tests cover every opcode, value type, errors, and overflow.
6. Add cross-platform release archive smoke tests, VS Code extension tests, Studio build tests, and actual installer tests.
