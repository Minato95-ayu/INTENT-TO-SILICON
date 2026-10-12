# AAYU Bytecode Format (implementation notes)

**Status:** current implementation notes; the format is not declared frozen or backward-compatible.

The VM loader in `runtime_rs/src/main.rs` expects a file beginning with the four-byte `AAYU` magic header, followed by a string table, a constant table, and the instruction stream. Integer fields in the current loader are read little-endian. See the loader and `runtime_rs/src/opcodes.rs` for authoritative details.

The opcode enum currently includes stack/value operations, arithmetic and comparison, jumps and calls, arrays and dictionaries, printing, state, tensor, database, server, and UI operations. Operand sizes vary by opcode. Do not build another compiler or VM against this page alone; the format needs a versioned specification and compatibility tests before it can be treated as a stable ISA.

`LOAD_GLOBAL` (`0x07`) and `STORE_GLOBAL` (`0x08`) each take a one-byte slot index. `CREATE_ARRAY` (`0x86`) takes a big-endian 16-bit element count; `BUILD_DICT` (`0x80`) takes a big-endian 16-bit entry count. `LOAD_SUBSCR` (`0x88`) consumes object and key and leaves a value.

Opcode `0x24` (`CALL_LOCAL`) carries a big-endian 16-bit argument count and a big-endian 16-bit absolute bytecode entry offset. It consumes the arguments, enters a fresh 256-slot local frame, and leaves one return value for the caller. `RET` restores the saved locals and return address. This encoding caps code offsets and call arity at 65535 and is an implementation detail pending a versioned ISA.

The VM validates loaded bytecode before execution. Validation is a defense layer, not a guarantee that every arbitrary or adversarial program is safe. See the malformed bytecode scripts under `tests/` and the current limitations in `KNOWN_LIMITATIONS.md`.
