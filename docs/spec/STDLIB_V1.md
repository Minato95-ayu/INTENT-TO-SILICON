# AAYU Standard Library & Diagnostics v1.0

This specification mandates a strict decoupling of the AAYU Compiler from the Standard Library. The compiler must not hardcode logic, type checking overrides, or code generation routines for standard APIs. The `core` module provides these APIs natively.

## 1. Core Built-ins

The following functions are guaranteed to be provided by the standard library (`core`). The compiler's only responsibility is to resolve their symbols and generate standard function calls according to the ABI.

### 1.1 I/O
- `fn print(text: String) -> Void`
- `fn println(text: String) -> Void`
- `fn panic(message: String) -> Never`
- `fn exit(code: Int) -> Never`

### 1.2 Data Operations
- `fn len(data: String) -> Int`
- `fn len(data: List) -> Int` (Future List support)

### 1.3 Type Conversions
- `fn toInt(value: String) -> Int`
- `fn toFloat(value: String) -> Float`
- `fn toString(value: Int) -> String`
- `fn toString(value: Float) -> String`

*(Note: In AAYU, type coercion is entirely explicit. The compiler will not implicitly cast `Int` to `String`. Developers must invoke these `core` functions.)*

---

## 2. Permanent Diagnostic Error Codes

The AAYU compiler uses a permanent, never-changing diagnostic error code system. This guarantees that IDEs, Language Servers, and CI/CD pipelines can reliably depend on the compiler's output.

### 2.1 Lexer & Parser Errors (`E1xx`)
- **E101:** Syntax Error (Unexpected token).
- **E102:** Unresolved Module (Import failed).
- **E103:** Invalid Identifier.

### 2.2 Semantic & Symbol Errors (`E2xx`)
- **E201:** Undefined Symbol (Variable, Struct, Function not found in scope).
- **E202:** Duplicate Declaration (Symbol already declared in current scope).
- **E203:** Immutable Mutation (Attempted to mutate a variable declared with `let` instead of `mut`).

### 2.3 Type Errors (`E3xx`)
- **E301:** Type Mismatch (e.g., assigning `String` to `Int`).
- **E302:** Invalid Enum Variant (Accessing a non-existent variant).
- **E303:** Argument Mismatch (Function called with wrong number/type of arguments).
- **E304:** Invalid Operator (E.g., attempting `String + Int` without explicit `toString()`).
- **E305:** Missing Return (Function signature demands a return, but none provided).
- **E306:** Condition Not Boolean (e.g., `if 1 { ... }`).
- **E307:** Invalid Struct Field (Accessing a non-existent field).

### 2.4 Future Expansion
- **E4xx:** Memory & Ownership Errors (Lifetime mismatch, Use-after-free).
- **E5xx:** Lowering & LLVM Errors (Unsupported IR generation, Backend panic).

---

### Metadata
- **Version:** 1.0
- **Status:** Frozen
- **Owner:** AAYU Core Team
- **Frozen Date:** 2026-08-07
- **Last Modified:** 2026-08-07
- **Compatibility:** Guaranteed for 1.x
- **Breaking Changes:** Not Allowed
