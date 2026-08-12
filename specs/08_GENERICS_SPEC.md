Specification: 08_GENERICS_SPEC.md
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

# 08 Generics Spec (Frozen)

## Purpose
This document defines AAYU's Generic programming capabilities, allowing developers to write flexible and reusable code without sacrificing static type safety.

## Definitions
- **Generic Type Parameter:** A placeholder type (e.g., `T`, `K`, `V`) defined in square brackets `[ ]`.
- **Monomorphization:** The process by which the compiler generates specific machine code for each unique generic type instantiation.

## Core Mechanics

### 1. Generic Models
Models can accept generic type parameters.
```aayu
model Response[T] {
    status: Int
    data: T
}
```

### 2. Generic Functions
Functions can operate on generic types.
```aayu
task first[T](items: List[T]) -> T? {
    if items.length > 0 {
        return items[0].
    }
    return null.
}
```

### 3. Multiple Constraints
Generic types can be constrained using multiple traits.
```aayu
task serialize_all[T: Serializable + Loggable](items: List[T]) {
    // ...
}
```

## Compiler Rules
1. **Rule GE.1:** AAYU uses **Monomorphization** for Generics (similar to Rust/C++). The compiler backend MUST generate a unique symbol and implementation for every unique type `T` used at compile time.
2. **Rule GE.2:** The Type Checker MUST verify that any operations performed on a generic type `T` are explicitly permitted by the traits bounding `T`.
3. **Rule GE.3:** There is no runtime overhead or type-erasure (like Java). Generics resolve statically.

## Status Update
- Changed from Draft to **Frozen**. Compiler team is authorized to implement.
