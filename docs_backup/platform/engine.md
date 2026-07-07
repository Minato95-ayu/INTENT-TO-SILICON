# AAYU Engine

**Status: Developer Preview**

The AAYU Engine is the core compiler and runtime that powers the entire ecosystem. It translates `.aayu` files into AAYU Intermediate Representation (IR), and then routes them to Target Generators.

## The Builder API

The Builder API is the **single point of truth** for compilation. It orchestrates the pipeline and ensures that CLI, Chat, and VS Code Extensions all produce the exact same results.

```python
from builder.pipeline import build
build("main.aayu", "generated_project")
```

## Pipeline Stages

### 1. Lexer & Parser
Reads `.aayu` source code and builds the Abstract Syntax Tree (AST). It strictly enforces the AAYU grammar (`record`, `task`, `end.`).

### 2. IR Generator
Converts the AST into **AAYU IR** (a standardized JSON format). This abstracts away the syntax so that generators only care about *features* and *entities*.

### 3. Target Scorer
Analyzes the IR and decides what technology stack to generate.
- e.g., If IR contains Database models, it triggers the `PostgresGenerator`.
- e.g., If IR contains HTTP interactions, it triggers the `FastAPIGenerator`.

### 4. Generators
The final stage of the Software Factory. It outputs raw, production-ready code into the output directory.

## Experimental Runtime (VM)
Parallel to the code generators, the AAYU Engine includes an experimental Stack-based Virtual Machine (VM) that executes `.aayu` bytecode (`.ayc`) directly for scripts that do not require full software generation.
