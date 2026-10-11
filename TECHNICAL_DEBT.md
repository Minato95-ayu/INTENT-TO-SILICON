# AAYU Technical Debt Tracker

This document tracks known limitations, future optimizations, temporary implementations, and architectural debt across the AAYU ecosystem. It is intended to guide future contributors and maintainers toward areas requiring stabilization or refactoring before 1.0 Release.

## Compiler

- **TODO:** Implement parallel parsing for massive workspaces.
  - **Owner:** Unassigned
  - **Priority:** Low
- **TODO:** Exhaustive AST type checking beyond basic semantic analysis.
  - **Owner:** Unassigned
  - **Priority:** Medium

## Runtime

- **TODO:** Fully async State Runtime mutations (currently mock/synchronous).
  - **Owner:** Unassigned
  - **Priority:** High

## Virtual Machine (VM)

- **TODO:** Migrate pure-Python interpreter loop to C-extension or PyPy optimization for true production throughput (currently ~300k IPS).
  - **Owner:** Unassigned
  - **Priority:** High
- **TODO:** Implement multi-threading/concurrency in VM (currently single-threaded execution).
  - **Owner:** Unassigned
  - **Priority:** Medium

## Debugger

- **TODO:** Implement Reverse Debugging ("Step Back" functionality). Architecture is prepped, but history traversal is not implemented.
  - **Owner:** Unassigned
  - **Priority:** Low

## Package Manager

- **TODO:** Build cloud/backend integration for Official Registry (currently mocked to local filesystem).
  - **Owner:** Unassigned
  - **Priority:** High

## LSP

- **TODO:** Implement Incremental Parsing for `textDocument/didChange`. Currently re-parsing full documents.
  - **Owner:** Unassigned
  - **Priority:** High

## Builder

- **TODO:** Implement native compilation targets (.exe, .app).
  - **Owner:** Unassigned
  - **Priority:** Critical
- **TODO:** Future Native Builder (v2)
  - Replace PyInstaller with Nuitka.
  - Transition VM to Rust Runtime.
  - Implement LLVM Backend for AAYU Bytecode.
  - Enable Static Linking and pure AOT Compilation.
  - **Owner:** Architecture Team
  - **Priority:** Future

## Security

- **TODO:** Implement VM Sandboxing for execution of untrusted third-party AAYU modules.
  - **Owner:** Unassigned
  - **Priority:** High
