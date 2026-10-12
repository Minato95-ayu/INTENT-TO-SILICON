# CLI Reference

The Rust VM CLI supports a small command set. Run `aayu-vm --help` for the output from the built executable.

```text
aayu-vm run <file.aayu> [--jit]
aayu-vm run <file.ayc> [--jit]
aayu-vm build <file.aayu> [-o output.ayc]
aayu-vm version
aayu-vm help
```

Running source requires the separate `aayuc` compiler executable beside the VM or on `PATH`. `build` outputs `.ayc` bytecode, not a native executable. The `--jit` compatibility flag currently falls back to the Rust VM because the C emitter has not passed typed-value conformance checks. Project scaffolding, formatting, linting, package management, BrainOS, and language-server commands are not implemented by this CLI.
