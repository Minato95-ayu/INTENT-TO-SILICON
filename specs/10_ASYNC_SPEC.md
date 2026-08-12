Specification: 10_ASYNC_SPEC.md
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

# 10 Async Spec (Frozen)

## Purpose
This document defines how asynchronous operations (Tasks, Promises, and the Event Loop) are represented and executed in AAYU.

## Definitions
- **Task:** A function declared with the `async task` keyword that runs asynchronously.
- **Await:** The keyword used to pause execution of an async task until a promise resolves.
- **Promise:** An object representing the eventual completion (or failure) of an asynchronous operation.

## Core Mechanics

### 1. Declaring Async Tasks
Any function that performs I/O or takes time should be declared as an `async task`.
```aayu
async task fetch_data() {
    return "{ data: 42 }".
}
```

### 2. Awaiting Promises
The `await` keyword can only be used inside an `async task`.
```aayu
async task process() {
    let result = await fetch_data().
    print result.
}
```

### 3. Concurrent Execution
To run multiple tasks concurrently without blocking, developers can spawn them using the `spawn` keyword (which schedules them on the Event Loop without awaiting immediately).

## Compiler Rules
1. **Rule A.1:** The Semantic Analyzer MUST throw an error if the `await` keyword is used inside a synchronous `task` or `fn`.
2. **Rule A.2:** All `async task` functions implicitly return a `Promise[T]`, where `T` is the underlying return type.
3. **Rule A.3:** The Compiler Backend MUST emit non-blocking state-machine structures (or coroutines) for async functions.

## Status Update
- Changed from Draft to **Frozen**. Compiler team is authorized to implement.
