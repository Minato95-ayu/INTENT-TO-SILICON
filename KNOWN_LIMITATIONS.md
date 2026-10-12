# Known Limitations

This list describes limits visible in the current repository. Feature availability can differ by compiler path and runtime mode; parser support alone does not prove end-to-end support.

## Compiler and language

- The current VM CLI uses the Rust bootstrap compiler. The AAYU compiler source exists under `compiler/`, but stage-to-stage reproducible self-hosting is not yet established.
- The implemented language reference is still being aligned with the parser and regression examples. Older drafts using period-terminated `system`/`entity` syntax and LLVM do not describe the current core language.
- Not every construct recognized by the parser has demonstrated runtime coverage. Consult `tests/` and the confidence report before depending on less-used constructs.
- User-defined `action` calls now support positional arguments, isolated local frames, returns, and recursion. Relative source-file imports are supported by the Rust bootstrap compiler and are flattened into one shared program scope; there are no namespaces, aliases, package registry, or automatic standard-library lookup. Closures/captures and named/default arguments are not implemented; parameters and local slots are limited to 256.
- Array and dictionary literals, reads by index/key, string character reads, and `len` for strings/arrays are implemented. Indexed assignment, `for` iteration, and collection standard-library helpers are not implemented; the compiler limits program globals and per-function locals to 256 slots each.
- The current VM integer representation stores signed 48-bit values (`-140737488355328..=140737488355327`). The compiler rejects out-of-range integer literals, and integer arithmetic now returns a runtime overflow error when a result leaves that range.
- AAYU package resolution and a stable package registry are not implemented. The modules under `std/` and samples under `official_packages/` contain planned or illustrative calls, and are not a verified installable standard library/package set.
- The Rust runtime contains HTTP, UI, database, and tensor code, but those APIs are not uniformly exposed by the AAYU compiler. In particular, the TLS fields in `runtime_rs/src/net.rs` do not implement TLS on its raw TCP server, and its HTTPS client depends on `ureq`.

## Runtime

- The database module is a JSON-backed key-value store. It is not SQLite, relational SQL, or a write-ahead log. Flush now writes and syncs a same-directory temporary file before replacing the database file; `set_json` still discards flush errors, and concurrent multi-process writers are not coordinated.
- The VM uses a mark-and-sweep heap collector, not deterministic reference counting.
- The JIT bytecode path is disabled in the CLI because generated C loses AAYU value types and has incorrect results. `--jit` safely falls back to the Rust VM. The benchmark-only `--sum` C-kernel measurement is not JIT dispatch.
- The Rust runtime, compiler, website, extension, and Python tools have external build/runtime dependencies. “Zero dependency” is not accurate for the repository as a whole.
- Network, UI, and host integration features need separate security and operational review before production exposure. This repository review is not a security audit.

## Tooling and project coverage

- The VM CLI currently exposes `run`, `build`, `version`, and `help`; package-management and BrainOS subcommands described in older docs are not present in that CLI.
- The checked-in VS Code extension has syntax highlighting/snippets. The older extension entry point requested `aayu lsp`, but there is no such VM CLI command or language-server implementation in this repository.
- `runtime_rs/Cargo.toml` declares external build dependencies; this is not a zero-dependency Rust build. Source execution also needs the separate bootstrap compiler. The benchmark-only generated-C kernel needs a host C compiler; the normal `--jit` flag falls back to the Rust VM.
- CI builds the Rust components, runs the configured AAYU/Rust checks on Windows and Linux, and builds the website. Python tools and the VS Code extension do not have equivalent coverage in the current workflow.
- Release packaging must include the bootstrap compiler alongside the VM for source-file execution. See `.github/workflows/release.yml`.
