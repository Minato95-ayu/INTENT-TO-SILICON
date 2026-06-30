# BrainOS Vision & Agentic Pipeline

BrainOS represents the evolution of the AAYU platform from a passive compiler toolchain into an autonomous, self-improving Software Factory. It leverages advanced **agentic loop** patterns to ensure robust, deterministic, and self-healing software generation.

## The Two Independent Pillars

The ultimate vision of this ecosystem is divided into two distinct, independent, yet deeply collaborative pillars:

### Pillar 1: AAYU Language
A simple, fast, secure, and AI-first programming language.
- **Components:** Lexer, Parser, AST, Semantic Passes, Lowering, Optimizer, Compiler, Bytecode/Native, Runtime.
- **Target Features:** Memory Safe, Secure by Default, Cross Platform, WebAssembly, LLVM Backend, Self Hosting, Type System, Generics.

### Pillar 2: BrainOS Intent Engine
An AI Software Engineering Operating System (not just a chatbot).
- **Components:** Intent Engine, Clarification, Requirement Graph, Task Graph, Planner, Executor, Critic, Impact Analysis, Snapshot, Architecture Guard.
- **Responsibilities:** Understand human intent, seek clarification, convert goals to deterministic tasks, respect architecture freezes, and manage technical debt autonomously.

BrainOS acts as the Software Engineer, planning and orchestrating tasks, while AAYU acts as the Engine that compiles and runs the software.

## The 7-Stage Engineering Loop

Unlike standard AI coding loops (`Generate -> Critique -> Refine`), BrainOS operates on a rigorous 7-stage engineering loop designed to preserve architecture and project state consistency:

1. **PLAN**: Interpret human intent and formulate an implementation strategy.
2. **BUILD**: Generate AAYU code and modify necessary components.
3. **VERIFY**: Run the AAYU Compiler and execute the test suite to validate changes.
4. **CRITIQUE**: Analyze failures, errors, or missed requirements.
5. **IMPACT ANALYSIS**: Evaluate how changes affect the broader system (e.g., checking against the `ARCHITECTURE_FREEZE.md`).
6. **UPDATE PROJECT STATE**: Synchronize changes with the Project State Machine (`PROJECT_SNAPSHOT.md`, `ROADMAP.md`).
7. **CONTINUE / COMPLETE**: If success criteria are met, halt and request human review. Otherwise, begin the next iteration.

## Autonomous Pipeline Architecture

The core of BrainOS is built on a segregated responsibility model, where specialized guardrails ensure the AI cannot break frozen subsystems.

```text
Human Intent
      │
      ▼
BrainOS Planner          <-- Analyzes intent, determines required tasks
      │
      ▼
Architecture Guard       <-- Blocks changes that violate ARCHITECTURE_FREEZE.md
      │
      ▼
Task Generator           <-- Breaks intent into granular, actionable steps
      │
      ▼
AAYU Builder             <-- Writes/Modifies AAYU Code and runtime components
      │
      ▼
Compiler                 <-- Validates Syntax, AST, and Semantic constraints
      │
      ▼
Tests                    <-- Executes unit and integration test suites
      │
      ▼
Critic                   <-- Evaluates compiler/test output for errors
      │
      ▼
Impact Analyzer          <-- Checks for regressions or unintended side-effects
      │
      ▼
Project Snapshot         <-- Updates PROJECT_SNAPSHOT.md and documentation
      │
      ▼
Goal Complete?
      ├── No → Route back to Planner/Builder for Next Iteration
      └── Yes → Halt and request Human Approval
```

## Why This Pipeline Excels

1. **State Machine Integration**: By updating `PROJECT_SNAPSHOT.md` continuously, the system never loses context of what has been built, what is frozen, and what is next.
2. **Architectural Guardrails**: The `Architecture Guard` acts as a hard boundary, ensuring that "bug fix mode" or "frozen" subsystems (like the core compiler) are not arbitrarily refactored by the AI during a generation loop.
3. **Deterministic Verification**: Relying on the strict AAYU Compiler and VM runtime for the `Verify` stage eliminates hallucinated success. The code either compiles and passes the VM constraints, or the loop continues.
