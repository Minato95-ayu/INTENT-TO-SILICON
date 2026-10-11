# Compiler & Target Generators

Unlike traditional languages that compile down to machine code or a single virtual machine bytecode, AAYU employs a multi-stage, retargetable compilation pipeline. The compiler doesn't just evaluate syntax; it evaluates *intent* and *architecture*.

## The Compilation Pipeline

The AAYU pipeline consists of four distinct phases:

### 1. Lexing and Parsing (Frontend)
The AAYU parser reads `.aayu` source code and constructs an Abstract Syntax Tree (AST). It performs syntactic validation (e.g., ensuring blocks are closed with `end.`).

### 2. Intermediate Representation (AAYU IR)
The AST is transformed into the **AAYU IR**, a language-agnostic JSON structure. This IR represents the pure architectural intent of the software—entities, routes, workflows, and RBAC rules—stripped of syntactic sugar.

[Read the full AAYU IR Specification →](/specification/ir)

### 3. Target Selection Engine
This is a unique layer in the AAYU architecture. A rules-engine analyzes the AAYU IR and determines the optimal technology stack required to execute the intent.

For example, if the IR contains a heavy AI/ML workload, the engine might select a Python/FastAPI target. If it defines a complex UI with `dashboard` and `sidebar` components, it might select a React target for the frontend.

### 4. Target Generation (Backend)
Based on the selection, specific generators emit the final code. 
- A backend generator might emit a raw SQLite schema and FastAPI Python code.
- A frontend generator might emit a Next.js application.

Alternatively, the compiler can bypass explicit code generation and compile the IR into AAYU Bytecode (`.ayc`) to be executed directly by the **AAYU Native Runtime**.
