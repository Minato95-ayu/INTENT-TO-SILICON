# Changelog

All notable changes to the AAYU (Intent-to-Silicon) project will be documented in this file.

## [0.1.0] - Phase 2 Ecosystem Release

### Added
- **AAYU CLI**: Introduced the `aayu` command-line utility for bootstrapping (`aayu new`), managing dependencies (`aayu install`), checking environment (`aayu doctor`), and running projects (`aayu run`).
- **Package Manager (V1)**: Mock repository integration that resolves and installs modules directly into the local `.aayu/packages/` directory.
- **Dynamic Module Resolution**: The Interpreter now automatically resolves `use <module>.` statements via the local `.aayu/packages/` directory, removing the need for manual file linking.
- **VS Code Extension (V1)**: Official extension packaged as `aayu-language-0.1.0.vsix` featuring TextMate Syntax Highlighting, Language Configuration, and Snippets (`task`, `entity`, `route`).
- **Web Framework Integration**: Added full built-in HTTP server capabilities to handle JSON API endpoints and HTML template rendering.
- **Database & Authentication Support**: Core language elements like `create`, `find`, `login`, and `guard` map natively to database operations and JWT authentication flows.

### Changed
- Standardized project directory structure (e.g., `src/`, `.aayu/packages/`, `aayu.toml`).
- Shifted the project scope from an experimental Concept-to-Code generator (V2 Compiler) to a full-fledged independent Language Ecosystem.

## [0.0.1] - Intent-to-Silicon Concept Release

### Added
- **Intent IR (Intermediate Representation)**: A deterministic ADL schema defining architecture mathematically rather than using probabilistic LLM generation.
- **V2 Deterministic Compiler**: Included `normalizer.py` and `pain_point_extractor.py` to parse Hindi/English inputs into the strict Intent IR format.
- **Emotion-First Architecture**: Handled negations and contextual cues through a Root Word + Proximity Tagging system.
