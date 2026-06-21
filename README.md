<div align="center">
  <h1>🚀 AAYU</h1>
  <h3>The Intent Operating System & Full-Stack Programming Language</h3>

  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20668914.svg)](https://doi.org/10.5281/zenodo.20668914)
  [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![Status: Research Prototype](https://img.shields.io/badge/Status-Platform_Candidate-green.svg)]()
  [![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

  <p align="center">
    A deterministic, human-readable programming language featuring a Native Intent Engine, built-in web framework, native SQLite support, RBAC, Workflows, and a high-performance virtual machine. Built to bridge the gap between human intent and machine execution.
  </p>
</div>

---

## 🤖 What is AAYU?

AAYU is a **deterministic Architecture Definition Language (ADL)** and a complete **Intent Operating System**. 

Originally conceived to eliminate "Requirement Drift" in AI-agentic software development, AAYU has evolved to be the ultimate **Intent-to-Silicon Platform**. With AAYU, you don't need to manually glue together Express.js, Prisma, RBAC, state machines, and React. 

**Routing, Database CRUD, Session Authentication, Roles & Permissions, and Workflows are built directly into the language syntax.**

Even more powerful, AAYU ships with **Intent Engine v4 (Native)**, allowing you to generate an entire application from a single human-readable prompt.

---

## ✨ What AAYU is Capable of Doing

AAYU allows developers and non-developers alike to build enterprise-grade software simply by describing intent.

1. **Auto-Generate Enterprise Applications**: Using the `aayu build` CLI, you can type an intent like `"Build a Police Complaint System"` or `"Build a Hospital Management System"`, and the Intent Engine will natively output a perfectly mapped business system without requiring an external API.
2. **Handle Complex Relationships**: Built-in `one_to_one`, `one_to_many`, and `many_to_many` mappings embedded right into the language.
3. **Role-Based Access Control (RBAC)**: Define permissions naturally (`allow Doctor create Prescription.`) and secure routes instantly.
4. **State Machine Workflows**: Use the `workflow` and `step` keywords to build sequential business pipelines natively (e.g., `Filed -> Verified -> Closed`).
5. **UI DSL & Auto-CRUD**: With commands like `crud Patient.` or `page Dashboard.`, AAYU generates backend Admin REST routes and custom Frontend pages dynamically.

---

## 🧩 Available Packages & Modules

AAYU provides built-in packages that handle the core logic of modern web applications:

- `use http.`: Spun up via `serve on 8080.`. Handles explicit verbs (`get`, `post`), routing, extracting `form` parameters, mapping context, and returning `render` templates.
- `use db.`: Natively interfaces with a thread-safe SQLite WAL instance for `create`, `find`, `update`, `delete`, and `find_all` operations.
- `use auth.`: Built-in Stateful Session isolation, PBKDF2 hashing, and `guard session.` mechanics.
- `use rbac.`: (Internal) Validates users against the generated `Role` and `Permission` matrices dynamically.
- `use workflow.`: (Internal) Maintains states in the database via the `Workflow`, `WorkflowStep`, and `WorkflowState` logic.

---

## ⚡ Architecture: The Pipeline

AAYU's architecture operates in two massive phases: **The Intent Engine** and **The Web Runtime**.

### 1. Intent Engine v4 (Native Brain)
A deterministic inference pipeline that translates raw text into business architecture:
- **Capability Engine**: Maps text to domains (e.g., Hospital, LMS, CRM, Police).
- **Inference Engines**: Traverses the Knowledge Base to extract Roles, Entities, Relations, and Workflows.
- **AAYU Emitter**: Synthesizes a valid `main.aayu` output file.

### 2. The Language Pipeline
1. **The Lexer & Parser**: Tokenizes the `.aayu` source code into an Abstract Syntax Tree (AST).
2. **The Compiler (`.aayu` -> `.ayc`)**: Emits flat bytecode instructions (e.g., `CALL_TASK`, `LOAD_CONST`).
3. **The Opcode Execution Engine (VM)**: A deterministic interpreter executing your app in real-time.
4. **Thread-Safe Sub-VMs**: When an HTTP request comes in, a unique `sub_vm` thread spins up, ensuring safe execution without leaking memory or global variables.

---

## 💻 How to Use AAYU (Coding Steps)

Coding in AAYU revolves around the `.aayu` file extension. The standard entry point is typically `main.aayu`.

### Step 1: Auto-Generate an App (Optional but Recommended)
Instead of writing from scratch, let AAYU's Intent Engine scaffold the project for you based on a prompt.
```bash
python prototype/cli.py build "Build a Hospital Management System"
```
*This natively generates a `main.aayu` file populated with Roles, Entities, Workflows, and CRUD logic!*

### Step 2: Write/Edit your `.aayu` file
Open the generated `main.aayu` (or create a new one). AAYU code reads like pseudo-code:

```aayu
# 1. Define Entities & Relations
entity Doctor.
    text name.
end.

entity Appointment.
    text name.
end.

relation Doctor one_to_many Appointment.

# 2. Define Roles
role Admin.
role Doctor.

# 3. Define Workflows
workflow AppointmentWorkflow for Appointment.
    step Booked.
    step Completed.
end.

# 4. Generate Auto-CRUD pages
crud Doctor.
crud Appointment.

# 5. Start Server
serve on 8080.
```

### Step 3: Compile the Source Code
Compile the `main.aayu` script into an optimized Bytecode binary (`main.ayc`).
```bash
python prototype/cli.py compile prototype/main.aayu
```

### Step 4: Run the Virtual Machine
Boot the compiled bytecode using the VM. The engine will instantly create the SQLite databases, map your relations and workflows, and start an HTTP server.
```bash
python prototype/cli.py vm prototype/main.ayc
```
*Visit `http://localhost:8080` to see your running application!*

---

## 📂 Repository Structure

```text
INTENT-TO-SILICON/
├── README.md                          ← You are here
├── prototype/
│   ├── intent_v4/                     ← Native Intent Engine (Capabilities, Role Inferencers)
│   ├── aayu_language/                 ← AAYU Grammar, Lexer, Parser, Compiler
│   │   └── runtime/                   ← AAYU VM (Python) & Stdlib Web Server
│   ├── cli.py                         ← CLI tool (build, compile, vm, format)
│   ├── examples/                      
│   │   └── adumate-student-module/    ← Reference Full-Stack App
│   └── tests/                         ← Comprehensive Parity & End-to-End Tests
├── aayu-rs/                           ← Native Rust VM Runtime (v0.6.0 Prototype)
├── paper/                             ← Intent-to-Silicon Research Paper
└── schemas/                           ← Core IR Schemas
```

---

## 👤 Author & Research

**Ayush Kumar Mishra** (Pen name: **Ayush Kaushik**)  
*B.Sc. Mathematics Honours — Delhi, India*  
Self-taught full-stack developer, AI builder, and Founder of [Adumate.in](https://adumate.in).

* **GitHub:** [github.com/Minato95-ayu](https://github.com/Minato95-ayu)
* **X (Twitter):** [x.com/o_Ayush_kaushik](https://x.com/o_Ayush_kaushik)

**License:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0)  
*First commit: June 2026 | © 2026 Ayush Kumar Mishra*
