# AAYU Runtime (implementation notes)

**Status:** working description of the current Rust VM, not a frozen contract.

The runtime in `runtime_rs/` loads AAYU bytecode, validates instruction and control-flow structure, then executes the program in a Rust virtual machine. The command-line executable is `aayu-vm`; source execution also requires the Rust bootstrap compiler executable `aayuc` beside it.

## Runtime values and memory

The VM uses a 64-bit NaN-boxed value representation. Heap objects include strings, arrays, and dictionaries. The memory manager uses mark-and-sweep collection; it is not deterministic ARC.

## Built-in subsystems

The opcode definitions include operations for console output, tensors, JSON-backed key-value persistence, HTTP/server work, and UI nodes. Opcode presence is not a guarantee that each feature has complete language-level integration or production readiness. The database module is not SQLite or relational SQL.

## Execution and limitations

The VM verifies bytecode before execution. The experimental C emitter has incorrect typed-value behavior, so normal CLI execution routes `--jit` through the VM. See `runtime_rs/src/vm.rs`, `jit.rs`, `memory.rs`, and `db.rs` for implementation details, and [KNOWN_LIMITATIONS.md](../../../KNOWN_LIMITATIONS.md) for current gaps.
