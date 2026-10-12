# Installation

The repository does not currently provide the documented `pip install aayu-lang` workflow. Build the Rust VM and bootstrap compiler from source:

```powershell
cargo build --release --manifest-path runtime_rs/Cargo.toml
cargo build --release --manifest-path compiler_bootstrap/Cargo.toml
```

Both executables are required to run `.aayu` source. Keep `aayuc` beside `aayu-vm` or configure `AAYU_COMPILER_PATH` with the compiler path. Use `aayu-vm run file.aayu`; to execute bytecode, use `aayu-vm build file.aayu -o file.ayc` followed by `aayu-vm run file.ayc`.

## VS Code

The checked-in `vscode-aayu` extension provides syntax highlighting, snippets, and **AAYU: Run Current File**. Configure VM/compiler paths if they are not on `PATH` or beside each other. It does not provide language-server diagnostics, autocomplete, hover, or debugging.

See [Getting Started](getting_started.md) for the tested command flow and [Known Limitations](../KNOWN_LIMITATIONS.md) for current tooling gaps.
