# AAYU Language Specification v1.0

This specification formally defines the grammar, syntax, and semantics of the AAYU programming language. This document is the ultimate source of truth. The compiler must implement this specification exactly as written.

## 1. Lexical Structure

### 1.1 Tokens
AAYU source files are UTF-8 encoded. The lexer produces a stream of tokens, discarding whitespace and comments unless required for token separation.

### 1.2 Whitespace and Comments
- **Whitespace:** Space, tab, newline, carriage return.
- **Comments:** Single-line comments start with `//` and extend to the end of the line. Block comments are not currently supported in v1.0 to keep the parser simple.

### 1.3 Identifiers
Identifiers must start with an alphabetic character (a-z, A-Z) or an underscore `_`. Subsequent characters can be alphanumeric or underscores.
*Regex:* `[a-zA-Z_][a-zA-Z0-9_]*`

### 1.4 Keywords
The following keywords are active in v1.0:
`fn`, `action`, `state`, `struct`, `enum`, `let`, `if`, `else`, `return`, `while`, `for`, `in`, `import`, `true`, `false`, `null`.

The following keywords are strictly **reserved** for future use and cannot be used as identifiers:
`match`, `trait`, `impl`, `type`, `async`, `await`, `mut`, `ref`, `const`.

---

## 2. Declarations

### 2.1 Struct

- **Purpose:** Defines a strictly layout-compatible data aggregate.
- **Syntax:**
  ```aayu
  struct Name {
      field1: Type
      field2: Type
  }
  ```
- **Semantics:** Structs are pure data. They do not contain methods, constructors, or logic (Rule 13). 
- **Compile-time Behavior:** The compiler calculates memory layout (padding and alignment) based on the ABI.
- **Runtime Behavior:** Structs are allocated on the stack by default. Passed by value (copied) unless optimized by the compiler.
- **Error Cases:** Field re-declaration (`E202`), Missing type (`E101`).
- **Examples:**
  ```aayu
  struct Point { x: Int, y: Int }
  let p: Point = Point { x: 10, y: 20 }
  ```

### 2.2 Enum

- **Purpose:** Defines a tagged union (algebraic data type).
- **Syntax:**
  ```aayu
  enum Name {
      Variant1,
      Variant2
  }
  ```
- **Semantics:** An enum can only hold one of its defined variants at a time.
- **Compile-time Behavior:** The compiler calculates the tag size (e.g. 8-bit discriminator) and validates variant access.
- **Runtime Behavior:** Handled as a discriminator tag plus payload (if any).
- **Error Cases:** Invalid variant access (`E302`).
- **Examples:**
  ```aayu
  enum Status { Active, Inactive }
  let s: Status = Status.Active
  ```

### 2.3 Function (`fn`)

- **Purpose:** Defines synchronous logic and behavior.
- **Syntax:**
  ```aayu
  fn name(arg1: Type, arg2: Type) -> ReturnType { ... }
  ```
- **Semantics:** Functions are pure and cannot modify global `state` directly (unless passed by mutable reference, a future feature).
- **Compile-time Behavior:** Type-checked strictly against arguments and return type.
- **Runtime Behavior:** Creates a new stack frame according to the ABI calling convention.
- **Error Cases:** Argument mismatch (`E303`), Missing return statement (`E305`).
- **Examples:**
  ```aayu
  fn add(a: Int, b: Int) -> Int { return a + b }
  ```

### 2.4 Action (`action`)

- **Purpose:** Defines side-effectful event handlers (typically for UI or network events).
- **Syntax:**
  ```aayu
  action login(username: String) { ... }
  ```
- **Semantics:** Actions do not return values (implicitly `Void`). They are allowed to mutate global `state`.
- **Compile-time Behavior:** Verified for argument types.
- **Runtime Behavior:** Typically enqueued in the runtime's event loop.
- **Examples:**
  ```aayu
  action submit() { state.is_loading = true }
  ```

### 2.5 State (`state`)

- **Purpose:** Declares global reactive application state.
- **Syntax:**
  ```aayu
  state counter: Int = 0
  ```
- **Semantics:** Global singleton data.
- **Compile-time Behavior:** Enforces type safety on initialization.
- **Runtime Behavior:** Allocated in the `.data` or `.bss` section. Mutations may trigger reactive dependency graphs in the UI runtime.
- **Error Cases:** Type mismatch on initialization (`E201`).

---

## 3. Control Flow

### 3.1 `if` / `else`
- **Purpose:** Conditional execution.
- **Syntax:** `if condition { ... } else { ... }`
- **Semantics:** `condition` MUST evaluate to a `Bool`.
- **Compile-time Behavior:** Prevents implicit truthiness (e.g., `if 1` is an error).
- **Error Cases:** Condition is not a boolean (`E306`).

### 3.2 `return`
- **Purpose:** Exits a function early, returning a value.
- **Syntax:** `return expr`
- **Semantics:** Must match the enclosing function's return type.

---

## 4. Module System

### 4.1 `import`
- **Purpose:** Brings a module into the current file's namespace.
- **Syntax:** `import module_name`
- **Semantics:** Modules are resolved relative to the workspace members defined in `Aayu.toml`.
- **Compile-time Behavior:** The compiler eagerly resolves the module ID and registers it in the `SemanticContext`.
- **Error Cases:** Module not found (`E102`).
- **Examples:**
  ```aayu
  import core
  let p: core.Point = core.Point { x: 0, y: 0 }
  ```

---

### Metadata
- **Version:** 1.0
- **Status:** Frozen
- **Owner:** AAYU Core Team
- **Frozen Date:** 2026-08-07
- **Last Modified:** 2026-08-07
- **Compatibility:** Guaranteed for 1.x
- **Breaking Changes:** Not Allowed
