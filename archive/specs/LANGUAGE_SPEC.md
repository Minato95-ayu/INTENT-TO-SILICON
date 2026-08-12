# AAYU Language Specification (ALS) v1.0

> **Vision:** AAYU is a complete application programming language. A developer writes only AAYU code. The AAYU compiler, runtime, and virtual machine generate and execute everything required for frontend, backend, routing, state management, storage, and networking.

---

## Chapter 21 — Design Principles
AAYU is guided by strict philosophical principles to ensure long-term consistency and power:
- **One Syntax Everywhere:** A single consistent style is used across UI, logic, servers, and storage. Every block uses `{ }` and every statement terminates with `.`.
- **No HTML, CSS, JavaScript, or SQL:** Developers write purely in AAYU. The language abstracts away the underlying domains.
- **Everything in AAYU:** From database models to frontend components and backend routes.
- **Reactive by Default:** UI state automatically updates when variables mutate. No manual `setState()` or `notifyListeners()`.
- **Convention over Configuration:** Sensible defaults over boilerplate.
- **Cross-Platform Runtime:** The AAYU VM handles execution seamlessly across environments.
- **AI-First Language Design:** The syntax is explicit, declarative, and easily parsable by both humans and AI models.

---

## Chapter 1 — Lexical Structure
- **Statements:** All valid statements must end with a period (`.`).
- **Blocks:** All scopes and blocks are enclosed in curly braces (`{ }`). Do not mix and match styles.
- **Comments:** 
  - Single-line: `// comment`
  - Multi-line: `/* comment */`

## Chapter 2 — Keywords
`task`, `async`, `await`, `component`, `page`, `route`, `server`, `model`, `insert`, `update`, `delete`, `find`, `state`, `let`, `const`, `return`, `if`, `else`, `while`, `for`, `each`, `break`, `continue`, `print`, `input`, `assert`, `try`, `catch`, `finally`, `throw`, `panic`, `import`, `export`, `package`, `auth`, `form`, `validate`.

## Chapter 3 — Data Types
**Primitive Data Types:**
- `Int`, `Float`, `Bool`, `String`, `Char`, `Null`

**Collections:**
- `List`, `Map`, `Set`, `Tuple`, `Record`

## Chapter 4 — Expressions
AAYU supports standard operators for evaluating expressions.
- **Arithmetic:** `+`, `-`, `*`, `/`, `//` (integer division), `%`, `**` (power)
- **Comparison:** `==`, `!=`, `>`, `<`, `>=`, `<=`
- **Logical:** `and`, `or`, `not`

## Chapter 5 — Statements
Assignments use standard operators. Remember that every statement terminates with a period (`.`).
- **Assignment:** `=`, `+=`, `-=`, `*=`, `/=`

## Chapter 6 — Functions
Standard synchronous functions use the `task` keyword.
```aayu
task add(a, b) {
    return a + b.
}
```

## Chapter 7 — Tasks (Async)
AAYU uses `async task` and `await` for asynchronous operations, maintaining consistency with modern programming paradigms.
```aayu
async task loadUsers() {
    let users = await http.get("/users").
    return users.
}
```

## Chapter 8 — Modules
Code reuse is handled via `import` and `export`.
```aayu
import math.

export task hello() {
    print "Hello".
}
```

## Chapter 9 — Packages
Defines the current package scope and external dependencies.
```aayu
package crm.

import ui.
import http.
import storage.
```

## Chapter 10 — UI
The Native UI Framework replaces HTML/CSS. It provides native elements for layout and design.
- **Elements:** `page`, `window`, `layout`, `row`, `column`, `stack`, `grid`, `card`, `button`, `text`, `heading`, `image`, `icon`, `table`, `list`, `tabs`, `dialog`, `drawer`, `sidebar`.
```aayu
page Home {
    column {
        heading "Welcome".
        button "Login".
    }
}
```

## Chapter 11 — Components
Custom, reusable UI elements are defined using the `component` keyword. Components accept parameters.
```aayu
component UserCard(name String, age Int) {
    column {
        text name.
        text age.
    }
}
```
Components are instantiated using named parameters:
```aayu
page Home {
    UserCard(
        name: "Ayush",
        age: 19
    ).
}
```

## Chapter 12 — Routing
Declarative routing directly at the language level.
```aayu
route "/" {
    page Home.
}

route "/login" {
    page Login.
}

route "/dashboard" {
    page Dashboard.
}
```
Navigation uses `goto`:
```aayu
goto Dashboard.
```

## Chapter 13 — Forms
Native structures for data collection and validation.
```aayu
form Login {
    input email.
    input password.
    button "Login".
}

validate email {
    required.
    email.
}
```

## Chapter 14 — Storage
Native database interaction without writing SQL.
```aayu
model User {
    id Int.
    name String.
    email String.
}
```
CRUD operations:
```aayu
// Insert
insert User {
    name: "Ayush".
    email: "a@example.com".
}

// Read
let users = find User.

// Update and Delete
update User.
delete User.
```

## Chapter 15 — Authentication
Built-in primitives for handling secure authentication, roles, and sessions.
```aayu
auth JWT.
```

## Chapter 16 — Networking
Server definitions and HTTP handling are built into AAYU.
**Server Definition:**
```aayu
server {
    get "/users" {
        let users = find User.
        return users.
    }
    
    post "/users" {
        insert User.
    }
}
```
**Client Requests:**
```aayu
let data = await http.get("/users").
```

## Chapter 17 — Standard Library
AAYU provides comprehensive built-in namespaces so developers don't need external packages for basic functionality:
- `math`, `string`, `json`, `http`, `file`, `time`, `crypto`, `random`, `system`, `storage`, `ui`

## Chapter 18 — Concurrency & State
AAYU UI state is reactive by default. Developers never write `setState()`.
```aayu
state counter = 0.

text counter.

button "Add" {
    click {
        counter += 1.
    }
}
```
Event handlers like `click`, `change`, `hover`, `submit`, `load`, `scroll`, `drag`, and `drop` can be attached natively:
```aayu
input email {
    change {
        print email.
    }
}
```

## Chapter 19 — Errors
Standard `try/catch/finally` syntax.
```aayu
try {
    // code that might fail
} catch error {
    print error.
} finally {
    cleanup().
}
```

## Chapter 20 — Runtime
The AAYU Virtual Machine and Runtime seamlessly handle the orchestration of the Bytecode, Garbage Collection, Scheduler, Storage translation, UI rendering, Networking, and Events. Developers interact only with the clean AAYU syntax while the runtime bridges the gap to the native operating system layers.
