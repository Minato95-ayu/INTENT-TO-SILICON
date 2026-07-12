# AAYU Language Specification v1.0 & Vision

This document is the "source of truth" for the AAYU programming language and ecosystem. 
AAYU is NOT just a React, Flutter, or Python replacement, nor is it merely a SQL abstraction. **AAYU is a complete, integrated full-stack application platform.**

The core philosophy of AAYU is that a developer **only writes AAYU code**. They never write HTML, CSS, JavaScript, React, Flutter, or SQL. A single syntax and runtime handle the frontend UI, backend servers, routing, and database storage.

---

## The 12 Core Pillars of AAYU

AAYU is built upon 12 foundational pillars that make it a unified platform:

### 1. Core Language
Equivalent to Python/C++, providing the logical foundation.
- Variables, Constants, Data Types, Expressions, Operators.
- Functions (`task`), Classes / Models, Modules, Packages, Imports.
- Error Handling (`try`, `catch`, `finally`, `throw`, `panic`).
- Syntax: Blocks use `{ }`, statements terminate with `.`.
```aayu
let name = "Ayush".
let age = 20.
task hello() {
    print name.
}
```

### 2. Native UI Framework
Replaces HTML/CSS.
- Elements: `page`, `window`, `layout`, `row`, `column`, `stack`, `grid`, `card`, `button`, `text`, `heading`, `image`, `icon`, `table`, `list`, `tabs`, `dialog`, `drawer`, `sidebar`.
```aayu
page Home {
    column {
        heading "Welcome".
        button "Login".
    }
}
```

### 3. Forms Framework
Native support for data collection and validation.
- Inputs: `input`, `password`, `email`, `phone`, `date`, `file`, `checkbox`, `radio`, `dropdown`, `submit`.
```aayu
form Login {
    input Email.
    input Password.
    submit Login.
}
```

### 4. State Management
Built-in reactive state without external libraries.
```aayu
state counter = 0.
counter += 1.
```

### 5. Events
Native event handlers for user interaction.
- Types: `click`, `hover`, `change`, `submit`, `load`, `scroll`, `drag`, `drop`.
```aayu
button "Save" {
    click {
        print "Saved".
    }
}
```

### 6. Routing & Navigation
Seamless navigation built directly into the language.
- Commands: `route`, `goto`, `back`, `redirect`, Dynamic Routes.
```aayu
goto Dashboard.
```

### 7. Web Framework
Built-in backend server capabilities.
- Support: `server`, `route`, `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, middleware, static files.
```aayu
server 8080.
route "/users" {
    // handle request
}
```

### 8. Storage System
Native database modeling and queries. No SQL required.
- Commands: `storage`, `model`, `insert`, `find`, `update`, `delete`, transactions, relations, migrations.
```aayu
model User {
    name String.
}
insert User {
    name = "Ayush".
}
```

### 9. Authentication
First-class support for secure authentication.
- Support: Login, Logout, Register, Session, JWT, OAuth, Roles, Permissions.
```aayu
auth JWT.
```

### 10. Networking
Native API and communication tools.
- Support: HTTP Client, REST, WebSocket, GraphQL, File Upload/Download.
```aayu
request GET "/users".
```

### 11. Native Standard Library
A rich set of built-in modules.
- Modules: Math, String, JSON, File, Path, Date, Time, Crypto, Random, HTTP, Regex, Compression, XML, CSV.
```aayu
json.parse(data).
```

### 12. Runtime & VM
The heart of AAYU that seamlessly executes everything above.
- Handles: Bytecode, Garbage Collection, Memory, Scheduler, Storage, UI rendering, Networking, Events, Threads, and Async Tasks.
- The internal compiler pipeline (Source -> Lexer -> Parser -> AST -> Compiler -> Bytecode -> VM -> Native UI/Web/Storage) handles all lower-level translation.

---

## Execution Pipeline Architecture

```text
Application
      │
      ▼
AAYU Source Code
      │
      ▼
Lexer
      │
      ▼
Parser
      │
      ▼
AST
      │
      ▼
Compiler
      │
      ▼
Bytecode
      │
      ▼
Virtual Machine
      │
      ▼
┌──────────────────────────────┐
│ Native UI                    │
│ Native Web Server            │
│ Native Storage               │
│ Native Networking            │
│ Native Authentication        │
│ Native Standard Library      │
└──────────────────────────────┘
      │
      ▼
Operating System
```
