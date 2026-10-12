# Build and Run

Build both Rust components from the repository root:

```powershell
cargo build --release --manifest-path runtime_rs/Cargo.toml
cargo build --release --manifest-path compiler_bootstrap/Cargo.toml
```

Run source using the VM and bootstrap compiler:

```powershell
runtime_rs/target/release/aayu-vm.exe run tests/test_01_vars.aayu
```

The `.aayu` run path compiles to a temporary bytecode file and executes it. To keep the bytecode:

```powershell
runtime_rs/target/release/aayu-vm.exe build tests/test_01_vars.aayu -o app.ayc
runtime_rs/target/release/aayu-vm.exe run app.ayc
```

`.ayc` is AAYU bytecode, not a native `.exe` or web bundle. The `--jit` compatibility flag currently falls back to the Rust VM because the experimental C emitter has incorrect typed-value behavior.
