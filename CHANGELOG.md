# Changelog

All notable changes to the AAYU project will be documented in this file.

## [1.0.0] - Stable Release
### Added
- **AAYU Compiler Core (Stable)**
  - Lexer, Parser, AST, and Semantic Analyzer.
  - Bytecode generation for intent-based declarative UI and Logic.
- **AAYU Runtime (Stable)**
  - Native VM with Stack-based execution and robust memory model.
  - Automatic State Management binding UI components to variables.
  - HTTP Server and Storage OS out-of-the-box.
- **Developer Experience (DX)**
  - Polished Command Line Interface (`aayu new`, `aayu run`, `aayu build`).
  - Interactive "Learn AAYU in 15 Minutes" curriculum.
  - Next.js website and comprehensive documentation suite.
  - 10 reference `examples/` spanning Hello World to a WhatsApp Clone.
- **Bug Fixes & Stabilization**
  - Resolved parsing issues with hyphens in project names.
  - Improved error messages and execution stack traces for easier debugging.

### Changed
- Shifted the grammar from a generic imperative structure to a specialized, declarative UI + Logic structure (`page`, `text`, `button`, `state`, `action`).
- Migrated all internal dependencies to be fully offline-capable (zero-dependency build process).

### Removed
- Removed legacy experimental BrainOS widgets that were unstable.
- Removed the dot (`.`) requirement at the end of blocks, improving syntax readability.

---

*This is the first stable release of AAYU.*
