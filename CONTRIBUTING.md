# Contributing to AAYU

Thank you for your interest in contributing to the **AAYU (Intent-to-Silicon)** ecosystem! AAYU is an open-source research project aimed at building a robust, developer-friendly ecosystem around a deterministic architecture definition language.

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/INTENT-TO-SILICON.git
   ```
3. Ensure you have Python 3.8+ installed. No heavy external dependencies are required.

## Areas to Contribute

- **Language Parser/Interpreter**: Add new language constructs or optimize the AST evaluation in `prototype/aayu_language/`.
- **VS Code Extension**: Improve syntax highlighting, add new snippets, or contribute to the Language Server Protocol (LSP) implementation in `prototype/aayu-vscode-extension/`.
- **Package Manager / CLI**: Expand `aayu install` to resolve dependencies dynamically in `prototype/cli.py`.
- **Standard Library**: Create or improve built-in packages inside `prototype/mock_repo/`.
- **Documentation**: Add tutorials, refine language references, or write blog posts.

## Development Workflow

- Before making changes, check the `ROADMAP.md` and `CHANGELOG.md` to see the current focus.
- Please create an issue to discuss significant changes before submitting a Pull Request.
- Write tests for your changes, particularly if modifying the core AST or interpreter logic.

We welcome all contributions, from fixing typos in the docs to writing core compiler features!
