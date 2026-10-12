# Release Notes

This file is a status summary, not a record of independently verified release assets. The runtime CLI source reports version **1.2.0**; individual components may have different package versions.

## Current toolchain

- Rust VM CLI with `run`, `build`, `version`, and `help` commands.
- Rust bootstrap compiler for compiling `.aayu` source to `.ayc` bytecode.
- Bytecode validation before VM execution. The experimental C emitter is not enabled for CLI bytecode execution because it does not preserve AAYU types.
- AAYU compiler source, standard-library sources, Python BrainOS/Intent Engine prototypes, website, and VS Code extension in the repository.

## Release notes policy

For each tagged release, record the tag, platform assets, exact build source, tested commands, and known limitations here. Do not describe bytecode output as a native application binary, or claim a capability unless it has a reproducible implementation and verification path.
