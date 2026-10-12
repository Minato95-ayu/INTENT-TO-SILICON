# Release Checklist

Complete these checks before tagging a public release. The checklist describes required evidence; an unchecked item is not a release claim.

## Build and package

- [ ] Build `runtime_rs` and `compiler_bootstrap` from a clean checkout on Windows, Linux, and macOS.
- [ ] Confirm each release archive contains the VM executable, matching `aayuc` compiler executable, standard library, and examples.
- [ ] Confirm `aayu-vm run <source.aayu>` works from the packaged directory without relying on repository-local files.
- [ ] Confirm `build` emits `.ayc` bytecode and document that output accurately.
- [ ] Verify release version labels agree across runtime source, VS Code extension, docs, archive names, and release notes.

## Verification

- [ ] Run Rust unit tests and both AAYU regression/security scripts on supported platforms.
- [ ] Build the website and check published install, language, CLI, runtime, and limitation pages against the release.
- [ ] Record benchmark hardware, commands, raw output, and scope; remove stale numbers from other docs.
- [ ] Review generated artifacts and confirm datasets/model weights are intended for redistribution.
- [ ] Resolve the repository LICENSE and conflicting file-level licensing notices before publishing affected components.
- [ ] Review network, persistence, and host integration changes for security and failure behavior.
