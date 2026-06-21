# Installation

Getting started with AAYU is extremely fast. Since AAYU's compiler and CLI are distributed via PyPI, you can install it globally using `pip`.

## 1. Install via Pip

Open your terminal and run:

```bash
pip install aayu-lang
```

Verify that AAYU is installed by checking its version:

```bash
aayu --version
```

## 2. Install the VS Code Extension

For the best AAYU editing experience, install the AAYU VS Code extension from the Visual Studio Marketplace once it is published.

- Search for **AAYU** in the Extensions view
- Install the extension with the purple AAYU icon

If you want to install locally before publication, use the `.vsix` package in `vscode-aayu/`.

## 3. Generate a New Application

You can use AAYU's Native Intent Engine to scaffold a completely functioning enterprise architecture by just describing your intent in English.

```bash
aayu build "Build a Hospital Management System"
```

This command will output:
- `main.aayu` (The full logic, relations, and RBAC definitions)
- `views/` (Auto-generated UI screens)

## 3. Run the Server

To start the server and interact with your new application:

```bash
aayu run main.aayu
```

Navigate to `http://localhost:8080` to see your running web application.

---

## Downloads (Coming Soon)

In the upcoming weeks, AAYU will provide pre-compiled, standalone binaries built using our Rust VM runtime (`aayu-rs`).

- Windows Installer (`.exe`) - **Coming Soon**
- macOS Installer (`.dmg`) - **Coming Soon**
- Linux Installer (`.deb` / `.rpm`) - **Coming Soon**

Until then, the recommended installation method is via `pip`.
