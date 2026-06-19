# AAYU LSP V1 (Language Server Protocol) Design

This document outlines the architecture and scoped feature set for the first iteration (V1) of the AAYU Language Server Protocol integration. 

## V1 Scope (Strictly Enforced)

✅ **Diagnostics**: Real-time syntax and parser error reporting via underlines in the editor.
✅ **Keyword Completion**: Suggestions for built-in AAYU keywords (e.g., `use`, `task`, `entity`).
✅ **Snippet Completion**: Advanced multi-line templates (`task`, `route`).

❌ **Out of Scope for V1**:
- Rename Symbol
- Refactoring
- Go To Definition
- Hover Docs
- Workspace Symbols

## Architecture Flow

The LSP will operate using a standard client-server model over standard input/output (stdio) streams utilizing the JSON-RPC protocol.

```text
VS Code (AAYU Extension Client)
       |
       |  JSON-RPC (stdio)
       v
AAYU LSP Server (Python Process)
       |
       |  File URI & Content
       v
AAYU Parser (lexer.py & parser.py)
       |
       |  Returns AST or SyntaxErrors
       v
AAYU LSP Server
       |
       |  Translates to LSP Diagnostic JSON
       v
VS Code Editor (Red Squigglies)
```

## Implementation Strategy
1. Extend the `aayu-vscode-extension` to include an LSP Client using `vscode-languageclient`.
2. Create a lightweight Python script (`lsp_server.py`) using the `pygls` library or custom JSON-RPC to handle requests.
3. Hook `lsp_server.py` into the existing `parser.py` module to parse documents in real-time. Catch standard `SyntaxError` and `ValueError` exceptions and map their line numbers to VS Code `Diagnostic` objects.
