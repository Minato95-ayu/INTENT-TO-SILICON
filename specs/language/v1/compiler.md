# AAYU Compiler (implementation notes)

**Status:** describes current components; not a frozen language or bytecode contract.

The repository contains AAYU compiler source under `compiler/` and a Rust bootstrap compiler under `compiler_bootstrap/`. The current VM command-line path invokes the bootstrap compiler to turn `.aayu` source into `.ayc` bytecode. Full reproducible self-hosting convergence remains pending.

## Current pipeline

```text
source -> lexer -> parser/AST -> bytecode emitter -> .ayc -> VM verifier -> execution
```

The AAYU source files include lexer, parser, analyzer, bytecode compiler, and UI renderer components. The Rust bootstrap compiler also has its own implementation. Do not assume the two compilers accept every same construct or emit byte-for-byte identical output until a comparison gate exists.

The VM CLI's `build` command emits bytecode, not a native application. The experimental JIT emitter is separate from source compilation and currently disabled for normal bytecode execution because it has incorrect typed-value behavior.
