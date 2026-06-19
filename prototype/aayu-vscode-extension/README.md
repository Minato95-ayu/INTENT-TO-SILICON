# AAYU Language Extension

This is the official VS Code extension for the **AAYU** programming language.

## Features

- **Syntax Highlighting**: Full keyword, string, comment, and type highlighting for `.aayu` files.
- **Code Snippets**: Accelerate development with predefined snippets for `task`, `entity`, and `route` declarations.
- **Language Configurations**: Automatic bracket matching, auto-closing pairs, and smart indentation.

## Snippets

- Type `task` + Tab to scaffold a task declaration.
- Type `entity` + Tab to scaffold a database entity.
- Type `route` + Tab to scaffold an HTTP route.

## Installation

You can install this extension locally by compiling it to a `.vsix` package:

```bash
npm install -g @vscode/vsce
vsce package
code --install-extension aayu-language-0.1.0.vsix
```
