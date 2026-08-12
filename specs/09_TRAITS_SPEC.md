Specification: 09_TRAITS_SPEC.md
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

# 09 Traits Spec (Frozen)

## Purpose
This document defines how AAYU implements interfaces and polymorphism through the `trait` system. AAYU favors composition over inheritance.

## Definitions
- **Trait:** A collection of method signatures (and optionally default implementations) that define a behavior.
- **Implementer:** Any struct or model that provides concrete implementations for a trait's methods.

## Core Mechanics

### 1. Defining a Trait
Traits define behaviors that can be shared across different models.
```aayu
trait Serializable {
    task serialize() -> String.
}
```

### 2. Implementing a Trait
Models implement traits using the `impl` block.
```aayu
model User {
    name: String
}

impl Serializable for User {
    task serialize() -> String {
        return '{"name": "' + self.name + '"}'.
    }
}
```

### 3. Trait Bounds
Functions and Generic types can require parameters to implement specific traits.
```aayu
task print_json[T: Serializable](item: T) {
    print item.serialize().
}
```

## Compiler Rules
1. **Rule TR.1:** A model MUST provide an implementation for all non-default methods defined in the trait. The compiler MUST throw a `NotImplementedError` otherwise.
2. **Rule TR.2:** AAYU does NOT support classical inheritance (`class A extends B`). All shared behavior must be achieved via traits.
3. **Rule TR.3:** Dynamic dispatch is supported when a variable is typed explicitly as a Trait (e.g., `let x: Serializable`). The compiler MUST emit vtable lookups for such calls.

## Status Update
- Changed from Draft to **Frozen**. Compiler team is authorized to implement.
