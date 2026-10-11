# AAYU Intermediate Representation (IR)

The AAYU Intermediate Representation (IR) is a formal, stable JSON contract representing the architectural intent of an application. 

While the AAYU compiler's Abstract Syntax Tree (AST) captures the entire syntactic tree of a program, including loops and expressions, the **IR strictly captures architecture, not behavior**. 

The IR acts as the primary input for the AAYU **Target Selection Engine**, allowing it to analyze the shape of an application (e.g., does it use a database? does it have RBAC?) to select the optimal technology stack (e.g., Python, Rust, React, Flutter) before passing the IR to the respective Code Generators.

## Generating the IR
Developers can inspect the generated IR for any `.aayu` file using the CLI tool:

```bash
aayu inspect app.aayu --pretty
```
This generates an `app.ir.json` file.

## Schema Structure (IR v1)

The v1 IR schema is a flat JSON object containing arrays of architectural declarations.

### `ir_version`
The version of the IR specification. Allows backward compatibility as the AAYU language evolves.
```json
"ir_version": "1.0"
```

### `system`
Metadata about the compiled application.
```json
"system": {
  "name": "HospitalApp"
}
```

### `features`
An automatically generated list of required capabilities based on the application's intent. The Target Selection Engine uses this to rule out incompatible tech stacks.
```json
"features": ["database", "ui", "api", "rbac", "workflow"]
```

### `entities`
Data models mapped from `entity` blocks.
```json
"entities": [
  {
    "name": "Patient",
    "fields": [
      { "name": "name", "type": "text" },
      { "name": "age", "type": "number" }
    ]
  }
]
```

### `relations`
Connections between entities mapped from `relation` keywords.
```json
"relations": [
  {
    "source": "Doctor",
    "type": "one_to_many",
    "target": "Appointment"
  }
]
```

### `roles` and `permissions`
Access control structures derived from `role` and `allow` blocks.
```json
"roles": [
  { "name": "Admin" }
],
"permissions": [
  {
    "role": "Admin",
    "action": "create",
    "target": "Doctor"
  }
]
```

### `pages`
UI representations mapped from `page` blocks.
```json
"pages": [
  { "name": "HospitalDashboard" }
]
```

### `workflows`
State machines mapped from `workflow` blocks.
```json
"workflows": [
  {
    "name": "PatientVisit",
    "entity": "Appointment",
    "steps": ["Scheduled", "CheckedIn", "Completed"]
  }
]
```

### `routes`
API or navigation endpoints mapped from HTTP verbs (`get`, `post`).
```json
"routes": [
  {
    "path": "/dashboard",
    "method": "GET",
    "handler": "handle_dashboard"
  }
]
```

### `modules`
Required standard library or third-party packages mapped from `use` statements.
```json
"modules": [
  { "name": "http" },
  { "name": "db" }
]
```

---

> [!IMPORTANT]
> **Behavior vs. Architecture**
> The AAYU IR v1 does not contain logic for internal task bodies (like `if` statements, `return` expressions, or arithmetic). Behavior remains inside the internal AST until a future execution IR is introduced.
