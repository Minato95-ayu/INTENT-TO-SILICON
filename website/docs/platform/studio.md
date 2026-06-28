# AAYU Studio

**Status: Preview**

AAYU Studio is the official VS Code Extension that turns your editor into a fully-fledged architecture environment.

## Features

- ✅ **Syntax Highlighting**: Beautiful keywords (`record`, `task`, `system`) and comment highlighting.
- ✅ **Auto-closing Blocks**: Automatically decrements indentation when typing `end.`.
- ✅ **Snippets**: Type `record` + Tab to instantly generate entity scaffolding.
- 🟡 **Autocomplete** (Coming Soon via LSP)
- 🟡 **Diagnostics / Error Underlines** (Coming Soon via LSP)

## Integrated AAYU Chat (Coming Soon)

AAYU Studio will feature a side-panel Chat Interface.

Instead of writing code manually, you can open the AAYU Panel and talk to the architecture engine. 

1. **Ask**: "Create a Hospital Management System"
2. **Intent**: The engine builds the intent and generates `main.aayu` directly into your workspace.
3. **Generate**: Click the **⚡ Generate** button in the VS Code title bar.
4. **Deploy**: The Builder API auto-triggers, generating your React/FastAPI stack!

## Debugger (Coming Soon)

The AAYU Debugger will allow you to run `.aayu` files using the Experimental Runtime directly inside VS Code, supporting breakpoints, variable inspection, and stack traces.
