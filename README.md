# AAYU: Intent-to-Silicon Architecture

![AAYU Ecosystem Overview](https://via.placeholder.com/1000x300?text=AAYU+Architecture)

**AAYU** is an Architecture-Aware Programming Platform. 
It bridges the gap between human intent (what you want to build) and the silicon layer (the code that executes it). AAYU allows you to declare business entities, workflows, and roles using a highly readable DSL, and deterministically generates pristine, full-stack applications.

---

## What is AAYU?

AAYU is **not** an AI that writes messy, unpredictable code. It is a deterministic compiler and orchestration engine. 

You write **Intent**:
```aayu
use db.
use http.

entity Product.
    text name.
    number price.
end.

relation Category one_to_many Product.
```

AAYU parses this intent into an Abstract Syntax Tree (AST), maps it to our Intermediate Representation (IR), and triggers Target Engines to scaffold a complete, professional repository.

---

## The Dual-Track Vision

AAYU operates on two parallel tracks to ensure both immediate value and future-proof scalability:

### Track A: The Software Factory (v1.0 Frozen)
Generates industry-standard codebases that you can deploy today.
- **Frontend**: React + Vite
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL (with automated schema generation)
- **Orchestrator**: Auto-generates `docker-compose.yml`, `.env`, and deployment instructions.

### Track B: The Native Runtime (Research)
The future of execution. Bypassing traditional code generation to execute AAYU directly via the `AAYU Bytecode (AYC)` format on our ultra-fast Rust Virtual Machine.

---

## How it Works

1. **Parser & Lexer**: Reads `.aayu` files and builds an AST.
2. **IR Generator**: Extracts semantic meaning without locking into a specific framework.
3. **Target Engine**: Uses scoring heuristics to determine the best tech stack.
4. **Code Generators**: Scaffolds React, FastAPI, and PostgreSQL files.
5. **Orchestrator**: Wires the frontend and backend together using Docker.

---

## Quick Start

### 1. Installation
Clone the repository and install the prototype tools:
```bash
git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON.git
cd INTENT-TO-SILICON
```

### 2. Generate Your First App
AAYU comes with examples out of the box (e.g., E-commerce, Hospital, CRM, AI Agent).
```bash
python prototype/cli.py generate examples/ecommerce.aayu
```

### 3. Run the Generated Output
AAYU automatically creates a `generated/` directory complete with instructions.
```bash
cd generated
docker-compose up --build
```
Your full-stack application is now live!

---

## Roadmap

- **Sprint 32 (Complete)**: Architecture Freeze v1.0. End-to-end validation across multiple industry examples.
- **Sprint 33 (Upcoming)**: Developer Experience Upgrade (`aayu init`, `aayu doctor`, enhanced CLI diagnostics).
- **Sprint 34+**: Advanced Code Generators (CRUD endpoints, robust UI forms) and Runtime Variable Management.

## Contributing

AAYU is an open research project exploring the limits of compiler-driven architecture. We welcome contributions to our `prototype/generators` and `aayu-rs` runtime engine.
