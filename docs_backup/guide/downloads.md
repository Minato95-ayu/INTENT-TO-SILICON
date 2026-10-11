# Downloads

AAYU is designed to be easy to install and easy to preview.
This page collects the latest release and distribution options for the CLI, VS Code extension, and future native binaries.

## Distribution Channels

### ✅ VS Code Extension
**Status: Ready for Marketplace**

AAYU syntax highlighting, snippets, and language support are available through the official VS Code extension.

- **Marketplace Installation**: Coming Soon (pending publisher account setup)
- **Local Testing**: Build and install the `.vsix` package from `vscode-aayu/`:

```bash
cd vscode-aayu
npm install
npx @vscode/vsce package
code --install-extension aayu-1.0.0.vsix
```

### ✅ GitHub Repository
**Status: Available**

Access the source code and contribute to AAYU development:

- Repository: [github.com/Minato95-ayu/INTENT-TO-SILICON](https://github.com/Minato95-ayu/INTENT-TO-SILICON)
- Issues & discussions welcome
- Community contributions encouraged

### ⏳ Python Package (PyPI)
**Status: Coming Soon**

Install the AAYU CLI from PyPI:

```bash
pip install aayu-lang
```

For now, local development from the repository root:

```bash
pip install -e .
```

Expected availability: Q3 2026

### ⏳ Native Runtime Binaries
**Status: Planned**

AAYU is preparing native runtime builds using the Rust VM runtime (`aayu-rs`).
These packages will be available as:

- Windows Installer (`.exe`)
- macOS Installer (`.dmg`)
- Linux packages (`.deb`, `.rpm`)

Expected availability: Q4 2026

### ⏳ GitHub Linguist
**Status: PR Pending**

AAYU source files use the `.aayu` extension.
GitHub language recognition improvements are in progress through GitHub Linguist metadata.

Expected availability: Q3 2026

---

## Quick Links

- **Report Issues**: [GitHub Issues](https://github.com/Minato95-ayu/INTENT-TO-SILICON/issues)
- **Documentation**: [Full docs](/guide/syntax)
- **Roadmap**: [2026 Milestones](/platform/roadmap)
- **Author**: [github.com/Minato95-ayu](https://github.com/Minato95-ayu)
