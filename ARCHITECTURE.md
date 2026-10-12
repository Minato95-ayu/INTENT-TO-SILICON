# AAYU Architecture

This document describes the implementation currently present in this repository. AAYU is evolving; planned features are listed separately in [ROADMAP.md](ROADMAP.md).

## Main components

| Path | Role | Implementation |
|---|---|---|
| `compiler/` | Lexer, parser, analyzer, bytecode emitter, and related compiler sources | AAYU source files |
| `compiler_bootstrap/` | Bootstrap compiler executable (`aayuc`) | Rust; uses the runtime crate |
| `runtime_rs/` | CLI, bytecode validation, VM, memory manager, disabled experimental C emitter, HTTP and UI support | Rust |
| `std/` | AAYU standard-library source modules | AAYU |
| `brainos/` | Workflow and project-generation prototype | Python |
| `intent_engine/` | Intent parsing and resolution prototype | Python |
| `website/` | Documentation site | Next.js/React/TypeScript |
| `vscode-aayu/` | VS Code language support and extension | JavaScript/TypeScript |

These components are not one dependency-free executable. The Rust crates, website, editor extension, and Python tools have their own build or runtime dependencies.

## Compiler and execution path

```text
.aayu source
    -> Rust bootstrap compiler (aayuc)
    -> AAYU bytecode (.ayc)
    -> bytecode loader and verifier
    -> Rust VM
```

The repository also contains a compiler pipeline written in AAYU under `compiler/`. The bootstrap compiler is the compiler used by the current VM CLI. A verified, byte-for-byte self-hosting bootstrap chain is still pending; source-language implementation and reproducible self-hosting are separate milestones.

The repository contains an experimental C emitter, but the CLI does not use it for bytecode because it has incorrect typed-value behavior. `--jit` currently falls back to the Rust VM. It is not an LLVM backend.

## Runtime details

- Values use a 64-bit NaN-box representation in the VM.
- The runtime heap manager implements mark-and-sweep garbage collection; it is not deterministic reference counting.
- The HTTP and UI modules are implemented in the Rust runtime. Their feature limits are described in [KNOWN_LIMITATIONS.md](KNOWN_LIMITATIONS.md).
- `runtime_rs/src/db.rs` implements an in-memory key-value map that loads and saves JSON data. It calls `sync_all` when flushing the file. This is not SQLite, a write-ahead log, or a relational database.
- Build dependencies are not zero: the Rust crates declare external crates, and the website/editor projects use npm packages.

## Validation and CI

The GitHub Actions workflow builds the Rust VM and bootstrap compiler, runs Rust unit tests and the AAYU test scripts on Windows and Linux, and builds the website. The workflow does not currently run a full test suite for every Python tool or the VS Code extension. See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

For build instructions, see [README.md](README.md). For the implemented language subset and known gaps, see [the language grammar](specs/language/v1/grammar.md) and [confidence report](COMPILER_CONFIDENCE_REPORT.md).
