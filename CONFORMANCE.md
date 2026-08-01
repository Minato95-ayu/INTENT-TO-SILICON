# AAYU Conformance Test Suite

To ensure absolute reliability and consistency across different runtime implementations (Python VM vs Native C-VM), AAYU utilizes a strict conformance testing lane.

## Test Lanes

The test lanes are categorized by execution phases, mimicking the compiler pipeline:
- **Phase 1-10 (Core Syntax):** Tests Lexer and Parser.
- **Phase 41-46 (Advanced Structures):** Tests Exceptions, Debugger, Modules, Reflection.
- **Phase 52-58 (Semantics):** Tests Symbol Types, Type Checker, Type Inference, Interfaces, Traits, Generics, Optimization.
- **Phase 71-77 (Tooling & Standard Library):** Tests Formatter, Linter, Package Manager, BrainOS, Intent Engine, Database, Production Stdlib.

## Running the Conformance Suite
To run the full suite against the Python VM:
\\\ash
pytest tests/
\\\

*In future releases (Phase D), a dedicated \un-conformance.ps1\ script will be provided to automatically compile and execute tests against both the Python VM and Native C-VM, verifying 1:1 bytecode execution parity.*
