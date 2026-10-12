# Changelog

All notable changes to the AAYU project will be documented in this file.

## Legacy 1.0 draft (the stable-release claims below were not verified)
### Added
- **AAYU Compiler Core (Stable)**
  - Lexer, Parser, AST, and Semantic Analyzer.
  - Bytecode generation for intent-based declarative UI and Logic.
- **AAYU Runtime (Stable)**
  - Native VM with Stack-based execution and robust memory model.
  - Automatic State Management binding UI components to variables.
  - HTTP Server and Storage OS out-of-the-box.
- **Developer Experience (DX)**
  - Older notes listed `aayu new` and other commands that the current VM CLI does not implement. See the current CLI reference.
  - Interactive "Learn AAYU in 15 Minutes" curriculum.
  - Next.js website and comprehensive documentation suite.
  - 10 reference `examples/` spanning Hello World to a WhatsApp Clone.
- **Bug Fixes & Stabilization**
  - Resolved parsing issues with hyphens in project names.
  - Improved error messages and execution stack traces for easier debugging.

### Changed
- Shifted the grammar from a generic imperative structure to a specialized, declarative UI + Logic structure (`page`, `text`, `button`, `state`, `action`).
  - Older zero-dependency and fully offline claims are not accurate for the current Rust toolchain.

### Removed
- Removed legacy experimental BrainOS widgets that were unstable.
- Removed the dot (`.`) requirement at the end of blocks, improving syntax readability.

---

This entry is retained as historical project notes, not a record of verified current features or a claim that AAYU is stable.
