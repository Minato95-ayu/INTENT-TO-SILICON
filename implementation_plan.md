# Phase 6.7: Cross-Platform & Independent Production Validation

The goal of this phase is to move AAYU from "architecturally sound" to "production-ready and independently verifiable," fulfilling the final RC0 checklist.

## Open Questions
> [!IMPORTANT]
> - **Web Transpilation Scope:** The AST for the Demo App uses custom components (`page`, `container`, `card`, `heading`). Since this is a massive transpilation task, I will implement a baseline Transpiler that maps fundamental UI constructs to HTML DOM elements (Vanilla JS Web Components) to prove the pipeline works end-to-end. Is this acceptable for Stable 1.0?
> - **Linux Target on Windows:** Since we are executing on a Windows host, creating a native Linux ELF binary via PyInstaller is not possible without WSL or Docker. I will implement the Linux builder logic, but it will only execute correctly if run from a Linux host. Is that acceptable for the RC0 scope?

## Proposed Changes

### 1. Real Desktop Builder (PyInstaller)
The Builder will be upgraded from a mock stub to a real `PyInstaller` invocation.
- Write a `boot.py` generator in `tools/builder/targets/desktop.py`.
- `boot.py` will contain the serialized AAYU bytecode.
- Execute `PyInstaller` programmatically to compile `boot.py` into a standalone native `app.exe` (or `./app`).
- The resulting `.exe` will launch the AAYU VM and run the code.

#### [MODIFY] tools/builder/targets/windows.py
#### [MODIFY] tools/builder/targets/linux.py
#### [MODIFY] tools/builder/targets/macos.py

---

### 2. Real Web Transpiler (AST -> HTML/JS)
The Web builder will transform the AAYU AST into executable HTML/JS.
- Walk the AST for `Page`, `Component`, `View`, and UI widgets.
- Generate standard HTML5 DOM trees.
- Bind `action` methods and `state` variables to Javascript event listeners and proxy objects (Vanilla JS reactivity).

#### [MODIFY] tools/builder/targets/web.py

---

### 3. Production LSP Completion
Currently, the LSP server has basic capabilities. We will upgrade it to support the full VS Code suite requested.
- **Diagnostics:** Parse errors and emit line/column specific diagnostics.
- **Hover:** Return variable scopes and types.
- **Go To Definition:** Map references to source AST nodes.
- **Rename:** Find all references and replace them across the document.

#### [MODIFY] vscode-aayu/extension.js
#### [MODIFY] tools/commands/lsp.py

---

### 4. Developer Documentation
Provide the essential documentation for a new developer to start autonomously.
- Installation Guide
- Hello World Tutorial
- Build & Run Guide

#### [NEW] docs/getting_started.md

## Verification Plan

### Automated Verification
- Run `aayu build` and verify that a real, executable `app.exe` is generated via PyInstaller, not a text mock.
- Run `app.exe` as a subprocess and verify its STDOUT execution.
- Run `aayu build --target web` and verify the output `index.html` contains actual transpiled JS/HTML based on the AST, rather than static mock strings.

### Manual Verification
- Ask the user to double-click `app.exe` to see it run.
- Ask the user to open `index.html` in their browser.
- Ask the user to open VS Code and test Hover, Definitions, and Diagnostics manually.