# AAYU Compiler Sources

These `.aayu` files are an experimental self-hosting compiler implementation sketch. The production command path in this repository does not execute them: `aayu-vm run file.aayu` invokes the separate Rust bootstrap compiler under `compiler_bootstrap/` and then runs bytecode in `runtime_rs/`.

The bootstrap compiler now accepts and runs the lexer draft, and `compiler/compiler.aayu` compiles and runs its demonstration that prints a bytecode array. This does not establish a usable self-hosted compiler: the emitted bytecode has not been shown to execute equivalently to the Rust compiler, and several compiler drafts may rely on unsupported semantics. The production source path still uses `compiler_bootstrap/` (Rust) and `runtime_rs/` (Rust). Reproducible self-hosting and byte-for-byte stage comparison have not been achieved.
