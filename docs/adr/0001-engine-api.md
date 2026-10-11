# 0001. AAYU Engine API Freeze

Date: 2026-06-28

## Status
Accepted

## Context
As AAYU evolves, different clients (CLI, VS Code LSP, Chat, and the future Web Playground) have begun duplicating logic to parse, compile, and execute `.aayu` files. This fragmentation leads to inconsistent behavior and makes maintenance difficult. We needed a single source of truth for handling AAYU projects.

## Decision
We have decided to freeze the **AAYU Engine API** as a stateful public interface (`prototype/engine/api.py`).
- All clients must instantiate an `AAYUEngine` object and load a project: `project = engine.load("file.aayu")`.
- The `AAYUProject` object will expose high-level methods: `validate()`, `compile()`, `generate(targets=[...])`, and `run()`.
- No client is allowed to directly import or invoke internal modules such as `Lexer`, `Parser`, `Compiler`, or `VM`. These are now strictly internal implementation details of the Engine.

## Consequences
- **Positive:** Guaranteed consistency across all clients. Easier testing of the core pipeline. Clear boundary between language implementation and ecosystem tools.
- **Negative:** Slightly tighter coupling of pipeline stages inside the Engine. Any new pipeline step must be explicitly exposed through the `AAYUProject` API.
