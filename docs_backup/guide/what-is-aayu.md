# What is AAYU?

**AAYU is an Architecture-First Software Factory with an experimental runtime track.**

AAYU turns business intent or direct `.aayu` source into a structured software architecture, then generates the application stack around it. The verified capability today is generation: entities, relations, workflows, pages, backend, frontend, database, and deployment structure.

Sprint 35 also proves the beginning of Track B: AAYU can execute its own bytecode path through the prototype VM.

```text
AAYU Source
down
Parser
down
Compiler
down
AYC
down
VM
down
Execution
```

The current runtime is experimental. It supports variables, print, and if execution in the verified Sprint 35 path. Functions, loops, modules, collections, packages, and runtime libraries remain roadmap work.

## The AAYU Philosophy

**Write Intent. Or Write Code. Both become Software.**

AAYU offers two interfaces:

1. **Intent Mode**
   Describe the application, such as "I need a CRM with customers, leads, and a sales dashboard." The Intent Engine converts that into AAYU architecture.

2. **Developer Mode**
   Write `.aayu` code directly. The syntax is clean, domain-specific, and declarative, so the architecture stays readable.

```aayu
system CRM

entity Customer.
    text name.
    text email.
end

entity Lead.
    text company.
end

relation Customer one_to_many Lead.

page Dashboard.
    sidebar.
        text "Customers".
        text "Leads".
    end.
end.
```

## The Current Architecture

```text
Business Intent
        OR
AAYU Code

        down

AAYU Language

        down

AAYU Compiler

        down

AAYU IR

        down

Target Selection Engine

        down

React + FastAPI + PostgreSQL

        down

Production-Ready Software
```

## Runtime Roadmap

```text
AAYU Code
down
AYC Bytecode
down
AAYU Runtime (Rust)
down
Execution
```

## Why AAYU Exists

If AI directly generates Python, React, or SQL, the developer still has to debug a large amount of framework-specific glue. AAYU keeps the software definition in a smaller, architecture-first language before generating target code.

That gives AAYU three practical goals:

- **Readable architecture:** Humans can inspect the `.aayu` source.
- **Deterministic generation:** The compiler owns the structural output.
- **Portable intent:** The same architecture can target different stacks over time.

AAYU does not replace Python, React, Rust, or databases. It sits above them and generates the boring parts of software structure.
