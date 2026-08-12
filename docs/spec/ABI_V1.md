# AAYU ABI Specification (AAYU ABI 1.0)

The AAYU Application Binary Interface (ABI) guarantees stability, deterministic memory layouts, and seamless foreign function interface (FFI) interoperability with C, C++, Rust, and LLVM targets. 

## 1. Primitive Sizes and Alignment

AAYU primitives map directly to strictly sized hardware representations:

| AAYU Type | Bit Width | Byte Alignment | LLVM IR Type |
|-----------|-----------|----------------|--------------|
| `Int`     | 64-bit    | 8 bytes        | `i64`        |
| `Float`   | 64-bit    | 8 bytes        | `double`     |
| `Bool`    | 8-bit     | 1 byte         | `i8`         |
| `Byte`    | 8-bit     | 1 byte         | `i8`         |
| `Char`    | 32-bit    | 4 bytes        | `i32`        |
| `Void`    | 0-bit     | N/A            | `void`       |

## 2. Struct Layout

- **Ordering:** The compiler retains the declaration order of fields by default, but reserves the right to reorder fields to minimize padding unless explicitly marked with a `#[repr(C)]` equivalent in the future.
- **Padding:** Padding bytes are inserted between fields to satisfy the alignment requirements of the subsequent field.
- **Alignment:** The alignment of a struct is equal to the maximum alignment of any of its fields. 
- **Size:** The total size of a struct is a multiple of its alignment (padding is added at the end if necessary).

## 3. Enum Layout

AAYU Enums are Algebraic Data Types (Tagged Unions).
- **Discriminator Tag:** An enum always begins with a hidden integer tag indicating the active variant.
- **Tag Size:** The tag size is determined by the number of variants.
  - $\le 256$ variants: 8-bit (`i8`)
  - $\le 65536$ variants: 16-bit (`i16`)
  - Otherwise: 32-bit (`i32`)
- **Payload (Union):** Following the tag (and necessary padding), the largest variant's payload size determines the total union size.
- **Alignment:** The alignment of the enum is the maximum of the tag's alignment and the alignment of the largest payload.

## 4. Calling Conventions

AAYU ABI 1.0 utilizes the **System V AMD64 ABI** on Unix-like systems and the **Microsoft x64 Calling Convention** on Windows. This ensures native C-interoperability.

### 4.1 Register Passing
- The first few integer/pointer arguments are passed in registers.
  - *Unix (SysV):* `RDI`, `RSI`, `RDX`, `RCX`, `R8`, `R9`.
  - *Windows:* `RCX`, `RDX`, `R8`, `R9`.
- Floating-point arguments are passed in `XMM0` through `XMM7` (SysV) or `XMM0` through `XMM3` (Windows).

### 4.2 Stack Passing
- Arguments exceeding the available registers are pushed onto the stack from right to left.
- The stack must be 16-byte aligned before making a call.

### 4.3 Return Convention
- **Primitives & Small Structs:** Returned in `RAX` (integer) or `XMM0` (floating-point). Structs up to 16 bytes may be split across `RAX` and `RDX` (SysV).
- **Large Structs:** The caller allocates space on the stack and passes a hidden pointer to this space as the first argument (in `RDI` or `RCX`). The callee writes the return value directly into this memory block.

---

### Metadata
- **Version:** 1.0
- **Status:** Frozen
- **Owner:** AAYU Core Team
- **Frozen Date:** 2026-08-07
- **Last Modified:** 2026-08-07
- **Compatibility:** Guaranteed for 1.x
- **Breaking Changes:** Not Allowed
