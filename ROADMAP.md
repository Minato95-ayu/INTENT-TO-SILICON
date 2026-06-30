# AAYU Evolution Roadmap

This roadmap outlines the major milestones of AAYU's development. It is organized by Products, Milestones, and Technical Debt to ensure a clear distinction between feature development, platform maturation, and repository health.

---

## Overall Completion Status

| Area                                    |                Status |
| --------------------------------------- | --------------------: |
| Language Frontend (Lexer, Parser, AST)  |                 ✅ 95% |
| Compiler & Bytecode                     |              ✅ 90–95% |
| Runtime & VM                            |              ✅ 90–95% |
| Software Factory                        |                 ✅ 90% |
| Chat & Intent Engine                    |              ✅ 85–90% |
| BrainOS                                 | 🟡 30–40% (Prototype) |
| IDE / Studio                            |             🟡 40–50% |
| Complete Programming Language Ecosystem |             🟡 45–50% |

---

## Products

### 1. AAYU Language
The core declarative intent language, strictly controlled compiler, bytecode specification, and VM runtime.

### 2. AAYU Platform
The surrounding tooling, standard libraries, and generation ecosystem (React, FastAPI, PostgreSQL).

### 3. BrainOS
The autonomous agent operating system that manages the repository, reads the Project State Machine, and accelerates development.

---

## Milestones

### Priority 0: Repository Health
*Focus on stabilizing the CI pipeline and developer experience.*
- [x] VS Code Extension
- [x] LSP Launch
- [x] Validation Pass
- [ ] Broken TODOs Cleanup
- [x] **CI (GitHub Actions)** (Auto-test, build, LSP check, and package build on every commit)
- [ ] Documentation updates

### Milestone 4: Runtime & Debugger (Current)
*Focus on execution, error handling, and runtime insights.*
- [x] Phase 4.1: Exception System
- [x] Phase 4.2: Debug Metadata (Line tables, source spans)
- [x] Phase 4.3: Runtime Diagnostics
- [x] Phase 4.4: Debugger Runtime (Event-driven breakpoints, inspector)
- [x] Phase 4.5: Advanced Modules (Visibility, Aliasing, Export Blocks)
- [x] Phase 4.6: Reflection (Read-Only)

### Milestone 5A: BrainOS Foundation
*Focus on orchestration, state management, and the autonomous loop (Non-AI MVP).*
- [ ] Planner (Parses goal into task graph)
- [ ] Workflow Engine (Executes tasks sequentially)
- [ ] Project State Machine (Snapshot & Roadmap tracker)
- [ ] Architecture Guard (Protects frozen subsystems)
- [ ] Task Queue (Manages execution state)
- [ ] Snapshot Engine (Automates updates to project state)

### Milestone 5B: AAYU Type System
*Focus on type safety and generics, developed via dogfooding BrainOS.*
- [x] Phase 5.1: Type AST
- [x] Phase 5.2: Type Symbols
- [x] Phase 5.3: Type Checker
- [x] Phase 5.4: Inference
- [ ] Phase 5.5: Interfaces
- [ ] Phase 5.6: Traits
- [ ] Phase 5.7: Generics

---

## 🧠 BrainOS Development Rule
**All future AAYU milestones must be executed through the BrainOS pipeline.**
Manual development is strictly reserved for improving BrainOS itself. BrainOS serves as the autonomous kernel managing project state, architecture guards, and regressions.

### Milestone 6: Native Backend
*Focus on performance and cross-platform native execution.*
- [ ] LLVM Backend prototype
- [ ] Ahead-of-Time (AOT) Compilation

### Milestone 7: Self Hosting
*Focus on dogfooding AAYU.*
- [ ] Rewriting the AAYU compiler in AAYU.

---

## Technical Debt

*These items must be addressed but are separate from milestone feature progression.*
- **Legacy Tests:** Clean up deprecated test suites and unify the testing framework.
- **CI Improvements:** Stabilize flaky tests and enhance GitHub Actions coverage.
