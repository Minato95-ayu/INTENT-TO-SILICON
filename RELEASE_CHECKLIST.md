# Stable 1.0 Release Checklist

Before certifying AAYU as **Stable 1.0**, the following criteria must be independently verified across Windows, macOS, and Linux:

## 1. Installation & Environment
- [ ] Fresh Machine Virtual Environment installation succeeds (`pip install aayu-lang`).
- [ ] Global `aayu` command works out of the box without manual PATH edits.
- [ ] `aayu doctor` reports healthy environment dependencies.

## 2. CLI & Workflows
- [ ] `aayu new <App>` creates a valid scaffold.
- [ ] `aayu run` successfully launches the VM.
- [ ] `aayu test` executes successfully.
- [ ] `aayu format` works on dirty source files.

## 3. Builder
- [ ] `aayu build` natively invokes PyInstaller and generates `app.exe` (Windows), `app` (Linux/macOS).
- [ ] The generated native executable launches and executes AAYU bytecode correctly.
- [ ] `aayu build --target web` transpiles AST to `index.html` and `app.js`.
- [ ] The Web bundle opens in a browser and reactivity works.

## 4. Editor Experience (LSP)
- [ ] Diagnostics display syntax errors live.
- [ ] Hover reveals type/component metadata.
- [ ] Go To Definition routes to file starts.
- [ ] Rename successfully alters references.
- [ ] Autocomplete suggestions popup.

## 5. Documentation
- [ ] Quick Start works flawlessly.
- [ ] Hello World is understandable for beginners.
- [ ] API Reference is complete.
