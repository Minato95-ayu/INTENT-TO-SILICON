<div align="center">
  <h1>🚀 AAYU</h1>
  <h3>The Intent-to-Silicon Full-Stack Programming Language</h3>

  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20668914.svg)](https://doi.org/10.5281/zenodo.20668914)
  [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
  [![Status: Research Prototype](https://img.shields.io/badge/Status-Platform_Candidate-green.svg)]()
  [![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

  <p align="center">
    A deterministic, human-readable programming language with a built-in web framework, native SQLite support, and a high-performance virtual machine. Built to bridge the gap between human intent and machine execution.
  </p>
</div>

---

## 🤖 What is AAYU?

AAYU is a **deterministic Architecture Definition Language (ADL)** and complete **Web Application Platform**. 

Originally conceived to eliminate "Requirement Drift" in AI-agentic software development, AAYU has evolved into a fully functional programming language. It is designed to be effortlessly readable by humans (with syntax mimicking natural English/Hinglish flow) while compiling down to a strict bytecode executed by a highly concurrent Virtual Machine.

With AAYU, you don't need to glue together Express.js, Prisma, and JWT libraries. **Routing, Database CRUD, and Session Authentication are built directly into the language syntax.**

---

## ✨ Key Features

- **Human-First Syntax**: Read and write code that looks like pseudo-code. (`if account_len is greater than 0.0.`)
- **Built-in Web Server**: Native HTTP server, implicit request parameters, and explicit verbs (`get`, `post`, `delete`).
- **Native SQLite Integration**: Direct `find`, `create`, `update`, and `delete` entity operations using AAYU's internal thread-safe Database Serialization Lock (`RLock` + `WAL`).
- **Stateful Authentication**: Built-in Session isolation, PBKDF2 password hashing, and cookie management (`guard session.`).
- **High-Performance Rust VM Prototype**: A newly bootstrapped native Rust runtime (`aayu-rs` v0.6.0) delivering a **95x speedup** over traditional AST interpreters.

---

## 📖 Syntax Preview

Here is a real example of AAYU's elegant, built-in routing and database handling. This code spins up a web server, connects to a database, handles a POST request, and saves data to an entity.

```aayu
# Define the Data Model
entity College with "name", "location", "course".
entity SavedCollege with "student_email", "college_name".

# Define a POST route to save a bookmark
post "/save_college" to save_college.

task save_college with req.
    # Secure the route (Requires valid AAYU_SESSION cookie)
    guard session.

    # Extract form data automatically
    text college_name is form "college_name" from req.
    
    # Save to the SQLite Database natively
    map save_data.
    set "college_name" to college_name in save_data.
    create SavedCollege with save_data.
    
    # Redirect gracefully
    map context.
    set "target" to "/dashboard" in context.
    return render "views/adumate_redirect.html" with context.
end.

# Start the built-in HTTP Server
serve on 8082.
```

---

## 🏗️ The AAYU Platform (Adumate Showcase)

AAYU's architecture is actively validating itself through fully functional web applications generated and executed natively on the AAYU Web Runtime.

✅ **[Adumate Student Module (Phase 5A)](prototype/examples/adumate-student-module/)**: The first production-ready full-stack application built entirely with AAYU. It showcases SQLite session-based auth, secure templates, and dynamic APIs running locally.
✅ **Todo Application**: A complete CRUD web app with deletion, creation, and rendering running on the AAYU VM.
✅ **Library Management System**: A multi-entity relational application showcasing complex data loops and conditional rendering.

*(Coming Soon: VS Code Extension, Package Manager `aayu install`)*

---

## ⚡ Architecture: The Web Runtime

AAYU ships with a Decoupled Compiler Architecture and a Multi-Threaded Virtual Machine:

1. **The Lexer & Parser**: Tokenizes input source code and builds an Abstract Syntax Tree enforcing rigid grammatical boundaries.
2. **The Compiler (`adumate.aayu` -> `adumate.ayc`)**: Emits flat bytecode instructions (e.g., `CALL_TASK`, `LOAD_CONST`, `BUILD_MAP`).
3. **The Opcode Execution Engine**: A deterministic interpreter handling recursive call frames, variable scoping, and dynamic trait-based standard libraries.
4. **Thread-Safe Sub-VMs**: When an HTTP request is received, a unique `sub_vm` instance is cloned, inheriting standard libraries but executing in complete thread isolation to prevent cross-contamination of local variables.

---

## 💻 Getting Started (CLI)

You can compile and run AAYU applications entirely from the built-in CLI.

### 1. Compile Source Code
Compile your `.aayu` source code into AAYU Bytecode (`.ayc`):
```bash
python prototype/cli.py compile prototype/examples/adumate-student-module/adumate.aayu
```

### 2. Run the Virtual Machine Server
Boot the bytecode using the AAYU Virtual Machine. This will automatically spin up the SQLite database and start the HTTP server.
```bash
python prototype/cli.py vm prototype/adumate.ayc
```

### 3. Run Automated Benchmark Tests
Evaluate the VM against our extensive integration test suites (Testing routing, auth, databases, and collections parity):
```bash
$env:PYTHONPATH="." 
pytest prototype/tests
```

---

## 📂 Repository Structure

```text
INTENT-TO-SILICON/
├── README.md                          ← You are here
├── prototype/
│   ├── aayu_language/                 ← AAYU Grammar, Lexer, Parser, Compiler
│   │   └── runtime/                   ← AAYU VM (Python) & Stdlib Web Server
│   ├── cli.py                         ← CLI tool (compile, vm, format)
│   ├── examples/                      
│   │   └── adumate-student-module/    ← Reference Full-Stack App (Phase 5A)
│   └── tests/                         ← Comprehensive Parity & End-to-End Tests
├── aayu-rs/                           ← Native Rust VM Runtime (v0.6.0 Prototype)
├── paper/                             ← Intent-to-Silicon Research Paper
└── schemas/                           ← Core IR Schemas (Legacy NLP engine)
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
