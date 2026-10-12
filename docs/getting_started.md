# Getting Started with AAYU

AAYU is an experimental language with a Rust bytecode VM and a separate Rust bootstrap compiler. The verified starter syntax is small: `let`, reassignment, arithmetic, `if`/`else`, `while`, and `print`.

## Build the tools

Install Rust, then run these commands from the repository root:

```powershell
cargo build --release --manifest-path runtime_rs/Cargo.toml
cargo build --release --manifest-path compiler_bootstrap/Cargo.toml
```

The VM executable is `runtime_rs/target/release/aayu-vm.exe` on Windows or `runtime_rs/target/release/aayu-vm` on Linux/macOS. The compiler executable is `compiler_bootstrap/target/release/aayuc.exe` or `aayuc`. Keep both executables together (or put both on `PATH`) to run `.aayu` source through the VM.

## Run a program

```powershell
.\runtime_rs\target\release\aayu-vm.exe run hello.aayu
```

Compile to bytecode and run it separately:

```powershell
.\runtime_rs\target\release\aayu-vm.exe build hello.aayu -o hello.ayc
.\runtime_rs\target\release\aayu-vm.exe run hello.ayc
```

`build` creates `.ayc` bytecode. It does not create a standalone native application. See [README](../README.md), the [verified core tests](../tests/), and [known limitations](../KNOWN_LIMITATIONS.md).
