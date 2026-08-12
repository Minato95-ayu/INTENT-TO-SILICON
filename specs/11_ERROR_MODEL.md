Specification: 11_ERROR_MODEL.md
Version: 0.1.0
Status:
[x] Draft
[ ] Review
[ ] Frozen
[ ] Deprecated

Owner: Compiler Team
Depends On: 01_LANGUAGE_SPEC
Compiler Version: >=0.5.0
Last Updated: 2026-08-04

---

# 11 Error Model Spec (Frozen)

## Purpose
This document defines how exceptions, errors, and panics are handled in AAYU. AAYU uses a standard structured exception handling model.

## Definitions
- **Exception:** A recoverable error that occurs during program execution (e.g., `FileNotFound`, `NetworkError`).
- **Panic:** An unrecoverable error that immediately aborts the current process (e.g., `OutOfMemory`, `StackOverflow`).
- **Catch:** A block that intercepts and handles exceptions.

## Core Mechanics

### 1. Try / Catch / Finally
Recoverable errors are handled using the `try` block.
```aayu
try {
    let file = fs.read("data.txt").
} catch e: IOError {
    print "I/O Error occurred: " + e.message.
} finally {
    print "Cleanup complete.".
}
```

### 2. Throwing Errors
Developers can throw specific errors using the `throw` keyword.
```aayu
if age < 0 {
    throw ValidationError("Age cannot be negative").
}
```

### 3. Panics
For unrecoverable states, the `panic` keyword terminates the process and dumps the stack trace.
```aayu
panic("Critical security violation detected!").
```

## Compiler Rules
1. **Rule E.1:** The compiler MUST verify that custom errors inherit from the base `Error` trait.
2. **Rule E.2:** The `finally` block MUST always execute, even if a `return` or `throw` occurs inside the `try` or `catch` block. The compiler backend is responsible for emitting the appropriate landing pads.
3. **Rule E.3:** Panics bypass `catch` blocks completely. They trigger immediate process teardown via the `aayu_runtime` OS interface.

## Status Update
- Changed from Draft to **Frozen**. Compiler team is authorized to implement.
