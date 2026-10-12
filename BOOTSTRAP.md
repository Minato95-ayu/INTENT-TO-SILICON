# AAYU Build and Bootstrap Status

This guide reflects the current repository. The CLI compiles source with a Rust bootstrap compiler; the presence of `compiler/*.aayu` and a seed bytecode file does not yet prove a reproducible self-hosting cycle.

## Build the compiler and VM

From the repository root with Rust/Cargo installed:

```powershell
cargo build --release --manifest-path runtime_rs/Cargo.toml
cargo build --release --manifest-path compiler_bootstrap/Cargo.toml
New-Item -ItemType Directory -Force bin | Out-Null
Copy-Item runtime_rs/target/release/aayu-vm.exe bin/aayu-vm.exe
Copy-Item compiler_bootstrap/target/release/aayuc.exe bin/aayuc.exe
```

On Linux or macOS, build with the same Cargo commands and copy the extensionless executables `runtime_rs/target/release/aayu-vm` and `compiler_bootstrap/target/release/aayuc` into `bin/`.

## Run source and bytecode

```powershell
.\bin\aayu-vm.exe run tests\test_01_vars.aayu
.\bin\aayu-vm.exe build tests\test_01_vars.aayu -o vars.ayc
.\bin\aayu-vm.exe run vars.ayc
```

Keep `aayuc.exe` next to `aayu-vm.exe`; the VM CLI finds the compiler there when it receives a `.aayu` input. The `build` command creates `.ayc` bytecode, not a native executable.

## Self-hosting work still required

The repository contains the AAYU compiler source in `compiler/` and seed artifacts in `bin/`. To claim reproducible self-hosting, the project still needs a documented stage sequence that builds each compiler stage from the previous one, compares outputs, and runs as a CI gate. Until that is automated, describe the compiler as implemented in AAYU source with a Rust bootstrap compiler—not as a fully verified self-hosting toolchain.

See [the confidence report](COMPILER_CONFIDENCE_REPORT.md), [CI workflow](.github/workflows/ci.yml), and [roadmap](ROADMAP.md).
