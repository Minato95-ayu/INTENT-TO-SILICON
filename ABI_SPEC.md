# AAYU Application Binary Interface (ABI) Specification

This document defines the formal Application Binary Interface (ABI) for the AAYU Native Runtime. Adhering to these specifications is mandatory to ensure cross-platform compatibility, Native FFI interoperability, and future integrations such as an LLVM-based JIT compiler.

## 1. Object Header ABI

All heap-allocated AAYU objects MUST begin with the standardized `AayuObjectHeader`. 
The header is exactly 32 bytes (on 64-bit platforms) to guarantee alignment and extensibility.

```c
struct AayuObjectHeader {
    uint32_t type;         // ObjectType enum (4 bytes)
    uint32_t flags;        // GC markings, mutability, etc. (4 bytes)

    uint64_t size;         // Total size of the object in bytes, including header (8 bytes)

    struct AayuObjectHeader* next; // Pointer to next object in global list or free list (8 bytes)

    uint32_t generation;   // Reserved for future generational GC (4 bytes)
    uint32_t reserved;     // Reserved for padding/future use (4 bytes)
};
```

## 2. Object Alignment Rules

- **Header Alignment**: All `AayuObjectHeader` structures MUST be allocated on 8-byte aligned addresses.
- **Payload Alignment**: The payload of an object (the data following the header) starts immediately after the 32-byte header, inherently making it 8-byte aligned.
- **Heap Pages**: Memory pages allocated from the OS MUST be page-aligned (e.g., 4096-byte boundaries).

## 3. Primitive Type ABI

Primitive types in AAYU map directly to native C types to simplify JIT and FFI interactions:

| AAYU Type | C Type    | Size (Bytes) | Alignment (Bytes) |
|-----------|-----------|--------------|-------------------|
| Int       | int64_t   | 8            | 8                 |
| Float     | double    | 8            | 8                 |
| Bool      | uint8_t   | 1            | 1                 |
| Nil       | (none)    | 0            | N/A               |

Values passed around the VM use the `Value` union, which is exactly 16 bytes:
```c
typedef union {
    int64_t i_val;
    double f_val;
    uint8_t b_val;
    struct AayuObjectHeader* obj;
} ValuePayload;

typedef struct {
    uint32_t type;       // ValueType enum
    uint32_t pad;        // 4 bytes padding
    ValuePayload value;  // 8 bytes
} Value;
```

## 4. Aggregate Types

### Strings (`AayuString`)
- Immutable sequence of UTF-8 characters.
- Follows the `AayuObjectHeader`.
- Contains `length` (uint32_t) and a pointer to a null-terminated `char*` buffer.
- *Future*: Inline string buffering for short strings (SSO) may be implemented.

### Arrays (`AayuArray`)
- Dynamic array of `Value`s.
- Follows the `AayuObjectHeader`.
- Contains `capacity` (uint32_t), `count` (uint32_t), and a pointer to `Value* elements`.

### Dictionaries (`AayuDict`)
- Hash table of Key-Value pairs.
- Follows the `AayuObjectHeader`.
- Contains `capacity` (uint32_t), `count` (uint32_t), and a pointer to `AayuDictEntry* entries`.

## 5. Calling Convention

All internal VM dispatches and function calls use the standard C calling convention (`cdecl` or platform-specific equivalent like Microsoft x64 calling convention or System V AMD64 ABI). 

Native functions bound to AAYU must adhere to the `NativeFn` signature:
```c
typedef Value (*NativeFn)(int arg_count, Value* args);
```

## 6. Stack Frame Layout

The call stack in the VM is a fixed array of `CallFrame` structures.
Each frame manages its own instruction pointer and a window into the global value stack.
```c
typedef struct {
    uint32_t action_address;   // Offset in the bytecode array
    uint32_t ip;               // Current instruction pointer
    uint32_t stack_base;       // Starting index in the value stack
} CallFrame;
```

## 7. Register Usage (Future JIT)

*(Reserved for LLVM/JIT backend integration)*
- Callee-saved vs Caller-saved registers will follow the System V ABI for Linux/macOS and Microsoft x64 ABI for Windows.
- The AAYU VM state pointer (`vm`) will ideally be pinned to a specific register (e.g., `r12` on x64).

## 8. Native Function ABI

To expose a C function to AAYU, the function must be wrapped to match `NativeFn`.
The runtime is responsible for boxing/unboxing `Value` structs into native C primitives before executing FFI logic.

## 9. Bytecode ABI Compatibility

Bytecode files (`.aybc`) format must comply with `BYTECODE_SPEC.md`. Changes to the instruction width, header layout, or opcode values are considered breaking ABI changes and require a major version bump.

## 10. Versioning Policy

- **Major (Breaking)**: Changes to `AayuObjectHeader`, `Value` struct size, or `BYTECODE_SPEC.md` opcodes.
- **Minor (Compatible)**: Adding new native functions, new optional flags, or internal memory allocator optimizations.
- **Patch (Fixes)**: Bug fixes in bytecode generation or VM execution that do not alter data layout.
