Specification: 03_TYPE_SYSTEM.md
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

# 03 Type System Spec (Frozen)

## Purpose
This document defines AAYU's strong, static type system. It outlines primitive types, collection types, type inference rules, and type compatibility.

## Definitions
- **Static Typing:** All variables have a type known at compile time.
- **Type Inference:** The compiler automatically deduces the type of a variable if not explicitly declared.
- **Strong Typing:** Implicit type coercions (e.g., adding an Int to a String) are strictly forbidden unless explicitly cast.

## Core Mechanics

### 1. Primitive Types
- `Int`: 64-bit signed integer.
- `Float`: 64-bit floating point.
- `Bool`: Boolean `true` or `false`.
- `String`: UTF-8 encoded string.
- `Char`: A single Unicode scalar value.
- `Null`: Represents the intentional absence of a value (only allowed for Optional types).

### 2. Collection Types
- `List[T]`: A dynamically sized array of type `T`.
- `Map[K, V]`: A hash map with keys of type `K` and values of type `V`.
- `Set[T]`: A collection of unique elements of type `T`.

### 3. Type Inference & Declaration
Variables can be explicitly typed or inferred:
```aayu
let x: Int = 10.      // Explicit
let y = "Hello".      // Inferred as String
```

### 4. Optional Types
AAYU avoids Null Pointer Exceptions by using Optional types `T?`.
```aayu
let name: String? = null.
```

## Compiler Rules
1. **Rule T.1:** The Semantic Analyzer MUST throw a `TypeError` if a variable is assigned a value of an incompatible type.
2. **Rule T.2:** The compiler MUST NOT perform implicit type casting between numeric types and strings.
3. **Rule T.3:** Optional types (`T?`) MUST be unwrapped or checked before accessing their methods, otherwise the compiler MUST throw a `NullSafetyError`.

## Status Update
- Changed from Draft to **Frozen**. Compiler team is authorized to implement.
