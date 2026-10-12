# AAYU for VS Code

This extension provides AAYU syntax highlighting, editor configuration, snippets, and a command to run the active `.aayu` file using the Rust VM. It does not provide language-server diagnostics, autocomplete, hover, or a debugger.

## Run a file

Build the Rust VM and bootstrap compiler from this repository, then either put `aayu-vm` and `aayuc` on `PATH` or set the extension's `aayu.executablePath` and `aayu.compilerPath` settings. Open an `.aayu` file and run **AAYU: Run Current File** from the Command Palette. Output appears in the **AAYU** Output channel.

The current CLI supports a small core syntax. See the root [README](../README.md) and [known limitations](../KNOWN_LIMITATIONS.md).
