# AAYU Memory Model v1.0

The AAYU Memory Model defines how the language manages memory deterministically without a Virtual Machine or Garbage Collector. The compiler is strictly responsible for memory allocation, deallocation, and lifetimes based on this specification.

## 1. Memory Regions

### 1.1 Stack
- **Purpose:** Fast, contiguous memory for fixed-size local variables and function call frames.
- **Allocation:** Automatic upon function entry (`alloca` in LLVM).
- **Ownership:** Owned by the current function scope.
- **Lifetime:** Destroyed immediately when the function returns or the lexical scope ends.
- **Alignment:** Strictly follows the ABI (e.g., 8-byte alignment for 64-bit integers).
- **Drop Rule:** Trivially dropped (stack pointer decrement) unless it contains heap pointers (which triggers recursive drops).
- **Copy Rule:** Copied bit-for-bit (shallow copy) on assignment or function pass.
- **Move Rule:** Not applicable to plain old data (POD); moved if it contains heap allocations (future Ownership system).

### 1.2 Heap
- **Purpose:** Dynamic memory for variable-sized data (e.g., `String`, `List`) or explicitly boxed data.
- **Allocation:** Via the standard library allocator (`malloc` equivalent).
- **Ownership:** Strictly Single Ownership (in v1.0). The variable holding the heap pointer is the sole owner.
- **Lifetime:** Extends until the owner goes out of scope.
- **Alignment:** Minimum 8-byte or 16-byte alignment depending on the architecture ABI.
- **Drop Rule:** The compiler automatically inserts a `free` (or drop call) at the end of the owner's scope.
- **Copy Rule:** Deep copy (clone) is required to duplicate heap data. Shallow copies are prohibited to prevent double-free errors.
- **Move Rule:** Transfer of the pointer to a new owner; the old owner is invalidated.

### 1.3 Global (.data / .bss)
- **Purpose:** Application `state` variables.
- **Allocation:** Statically allocated at compile time.
- **Ownership:** Owned by the application runtime.
- **Lifetime:** Entire duration of the program execution.
- **Alignment:** Padded according to ABI requirements.
- **Drop Rule:** Never dropped.
- **Copy Rule:** Read/Write operations act as deep copies (or atomic operations if multi-threading is introduced).
- **Move Rule:** Cannot be moved.

### 1.4 Constant / Readonly (.rodata)
- **Purpose:** String literals, enum discriminators, and immutable compile-time constants.
- **Allocation:** Baked into the binary.
- **Ownership:** Shared universally.
- **Lifetime:** Static (program duration).
- **Alignment:** Optimized by the compiler.
- **Drop Rule:** Never dropped.
- **Copy Rule:** Only the pointer/reference is copied. The data itself is immutable.
- **Move Rule:** Cannot be moved.

### 1.5 Temporary / Compiler Generated
- **Purpose:** Intermediate values generated during expression evaluation (e.g., `a + b` before assignment).
- **Allocation:** Stack (or registers).
- **Ownership:** Owned by the current statement.
- **Lifetime:** Destroyed at the end of the statement (the `;` sequence point).
- **Alignment:** Native register size.
- **Drop Rule:** Dropped immediately after the statement completes.
- **Copy/Move Rule:** Passed directly to the consuming operation.

---

### Metadata
- **Version:** 1.0
- **Status:** Frozen
- **Owner:** AAYU Core Team
- **Frozen Date:** 2026-08-07
- **Last Modified:** 2026-08-07
- **Compatibility:** Guaranteed for 1.x
- **Breaking Changes:** Not Allowed
