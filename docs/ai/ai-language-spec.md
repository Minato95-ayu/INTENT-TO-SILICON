# AAYU Language Specification v1.0

This document is the "source of truth" for the AAYU programming language. AAYU is NOT a React or Flutter replacement, nor is it a SQL language. It is a general-purpose programming language designed with specific syntax and features outlined below.

## 1. Language Philosophy
AAYU is designed to be highly readable, robust, and capable of seamlessly interacting with storage and APIs.
- Statements in AAYU always terminate with a period (`.`).
- Code blocks are enclosed in curly braces (`{}`).
- AAYU abstracts database operations. Developers write native `insert`, `update`, `find`, and `delete` statements, and the internal compiler pipeline (Parser -> Storage AST -> Planner -> Optimizer -> SQLite Adapter -> SQLite) translates this into SQL. Users never write SQL directly.

## 2. Grammar
- Statements must end with a period `.`.
- Blocks use `{` and `}`.
- Single-line comments start with `//`.
- Multi-line comments are enclosed in `/*` and `*/`.

## 3. Keywords
Programming keywords include:
`task`, `return`, `if`, `else`, `while`, `for`, `each`, `break`, `continue`, `let`, `const`, `print`, `input`, `assert`.

## 4. Identifiers
Standard identifier rules apply (alphanumeric and underscores, cannot start with a number).

## 5. Variables
Variables are declared using `let` and `const`.
```aayu
let name = "Ayush".
let age = 18.
const PI = 3.14.
```

## 6. Data Types
**Primitive Data Types:**
- `Int`, `Float`, `Bool`, `String`, `Char`, `Null`

## 7. Expressions
AAYU supports standard arithmetic, comparison, and logical expressions.

**Operators:**
- **Arithmetic:** `+`, `-`, `*`, `/`, `//` (integer division), `%`, `**` (power)
- **Comparison:** `==`, `!=`, `>`, `<`, `>=`, `<=`
- **Logical:** `and`, `or`, `not`
- **Assignment:** `=`, `+=`, `-=`, `*=`, `/=`

## 8. Statements
All valid AAYU statements must end with a period `.`.

## 9. Functions (task)
Functions are defined using the `task` keyword.
```aayu
task add(a, b) {
    return a + b.
}
```

## 10. Collections
AAYU supports several collection types:
- `List`, `Map`, `Set`, `Tuple`, `Record`

## 11. Storage System
AAYU provides native keywords for data modeling and persistence: `storage`, `model`, `insert`, `find`, `update`, `delete`.
```aayu
storage Main.

model User {
    name String.
    age Int.
}

insert User {
    name = "Ayush".
}
```

## 12. Error Handling
AAYU uses `try`, `catch`, `finally`, `throw`, and `panic`.
```aayu
try {
    // code here.
} catch {
    // handle error.
} finally {
    // cleanup.
}
```

## 13. Modules
Modules can be imported and exported.
```aayu
import math.

export task hello() {
    print "Hello".
}
```

## 14. Standard Library
(To be documented - includes core system, math, and file utilities.)

## 15. Compiler Pipeline
AAYU code is executed through the following pipeline:
1. Source Code
2. Lexer
3. Parser
4. AST
5. Compiler
6. Bytecode
7. VM
8. Runtime
9. Storage / HTTP / UI

## 16. VM & Bytecode
The Virtual Machine executes compiled AAYU bytecode. The VM has distinct subsystems:
- Opcode handlers
- Storage runtime
- Runtime manager
- Execution pipeline

## 17. Runtime APIs
AAYU provides runtime support for Storage, HTTP, and UI execution environments.

## 18. Complete Example Programs

**File Structure:**
Typical AAYU projects contain files like:
- `project.aayu`
- `storage.aayu`
- `main.aayu`
- `routes.aayu`
- `models.aayu`
- `config.aayu`

**Example:**
```aayu
import math.

storage Main.

model User {
    name String.
    age Int.
}

task main() {
    let age = 18.
    
    if age >= 18 {
        print "Adult".
    } else {
        print "Minor".
    }

    for i = 0 to 10 {
        print i.
    }

    insert User {
        name = "Ayush".
    }
}
```
