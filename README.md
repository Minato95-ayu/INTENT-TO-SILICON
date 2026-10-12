# AAYU — Intent to Silicon

AAYU is an experimental programming language and toolchain. This repository also contains the BrainOS workflow prototype, an intent-processing prototype, a website, and editor tooling. These parts use different implementation languages and have different levels of maturity.

## Current implementation

- The language compiler sources are in `compiler/` and are written in AAYU. A separate Rust bootstrap compiler in `compiler_bootstrap/` currently provides the command-line compiler used by the VM. Reproducible self-hosting has not yet been established; see [the confidence report](COMPILER_CONFIDENCE_REPORT.md).
- The runtime and bytecode VM are in `runtime_rs/` (Rust). The repository contains an experimental C emitter, but the CLI routes `--jit` through the VM because emitted code has incorrect typed-value behavior.
- The runtime database module is a JSON-backed key-value store with an in-memory map and disk persistence. It is not SQLite and does not provide a relational SQL engine.
- `brainos/` and `intent_engine/` are Python projects/prototypes. The website and VS Code extension also have their own dependencies.

## Build from source

Install a current Rust toolchain, then build the VM and bootstrap compiler:

```powershell
cargo build --release --manifest-path runtime_rs/Cargo.toml
cargo build --release --manifest-path compiler_bootstrap/Cargo.toml
New-Item -ItemType Directory -Force bin | Out-Null
Copy-Item runtime_rs/target/release/aayu-vm.exe bin/aayu-vm.exe
Copy-Item compiler_bootstrap/target/release/aayuc.exe bin/aayuc.exe
```

On Linux or macOS, use the same Cargo commands and copy the outputs `runtime_rs/target/release/aayu-vm` and `compiler_bootstrap/target/release/aayuc` into `bin/` (omit `.exe`). The VM looks for `aayuc` beside itself when compiling `.aayu` files.

Run a source example or compile it to bytecode:

```text
bin/aayu-vm run tests/test_01_vars.aayu
bin/aayu-vm build tests/test_01_vars.aayu -o hello.ayc
bin/aayu-vm run hello.ayc
```

The build command creates AAYU bytecode (`.ayc`), not a native standalone application binary. The CLI currently routes `--jit` bytecode execution through the Rust VM because the C emitter has not passed type/result conformance checks. The benchmark-only `--sum` generated-C measurement is not a VM JIT performance claim.

## Language example

The currently exercised core syntax includes declarations, reassignment, arithmetic, `if`/`else`, `while`, and `print`:

```aayu
let count = 0
let total = 0

while count < 5
    total = total + count
    count = count + 1
end

if total == 10
    print("sum: 10")
else
    print("unexpected sum")
end
```

See [tests](tests/) for more examples. The formal language spec is being aligned with the implemented parser; treat unverified constructs in older docs as unsupported until documented and covered.

## Project status and docs

The compiler, VM, and surrounding tools are at different maturity levels. The [compiler confidence report](COMPILER_CONFIDENCE_REPORT.md) records known gaps; the [roadmap](ROADMAP.md) tracks planned work. Performance and readiness numbers are measurements or estimates for the listed environments, not general guarantees.

- [Architecture](ARCHITECTURE.md)
- [Language specification](specs/language/v1/grammar.md)
- [Benchmarks and methodology](benchmarks/BENCHMARK_RESULTS.md)
- [Known limitations](KNOWN_LIMITATIONS.md)
- [Website and docs](website/)

## License

The repository-level [LICENSE](LICENSE) is proprietary. The `vscode-aayu/` and `aayu_studio/` subprojects include their own MIT license files; check the applicable license before redistributing a component. `aayu.json` now reflects the repository-level license.
