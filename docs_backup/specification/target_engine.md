# Target Selection Engine

The Target Selection Engine is what makes AAYU an **architecture-aware software factory**.

Instead of generating code for a single predetermined language or VM, AAYU analyzes the architectural intent (via the AAYU IR) and automatically recommends the optimal modern software stack (Frontend, Backend, Database).

## How it Works

The engine operates in three layers:

1. **Feature Extraction**: It parses the AAYU IR and flags necessary capabilities (e.g., `ui`, `api`, `database`, `rbac`, `workflow`, `ai`, `mobile`).
2. **Metadata Scoring**: It maps these features against a heuristic matrix of known technologies. For example, if the `ai` feature is detected, Python/FastAPI and Jupyter receive a massive score boost. If `mobile` is detected, Flutter receives a boost.
3. **Recommendation**: It computes the highest-scoring combination for Frontend, Backend, and Database, along with a statistical `confidence` metric.

## Inspecting the Target Plan

Developers can view the generated Target Plan for any `.aayu` source file:

```bash
aayu target app.aayu --pretty
```

This generates an `app.target.json` file.

## Schema Structure (Target Plan v1)

```json
{
  "target_plan_version": "1.0",
  "confidence": 92,
  "stack": {
    "frontend": "React",
    "backend": "FastAPI",
    "database": "PostgreSQL",
    "special": ["Jupyter"]
  },
  "generators": [
    "react-generator",
    "fastapi-generator"
  ]
}
```

### `confidence`
A normalized score (0-100) indicating how clear the stack decision was. A score of `50` means two tech stacks tied or were very close in score, indicating the architectural intent might be ambiguous or equally suited for multiple paradigms.

### `stack`
The recommended technology stack.
- `frontend`: HTML/CSS/JS, React, Vue, Angular, Flutter
- `backend`: Python/FastAPI, Node/NestJS, Java/Spring, Go, Rust
- `database`: SQLite, PostgreSQL, MySQL
- `special`: Specific auxiliary tools required (e.g., Solidity, Jupyter, Kotlin, Swift).

### `generators`
An array specifying which AAYU Code Generators need to be invoked in the final stage of compilation to convert the AAYU AST/IR into the physical source code files for the chosen stack.

---

> [!TIP]
> **Manual Overrides**
> In the future, developers will be able to manually override the Target Selection Engine by specifying their desired stack in the project's `aayu.toml` file.
