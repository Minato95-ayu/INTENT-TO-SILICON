# AAYU Roadmap

**Current runtime CLI version:** 1.2.0 (reported by `runtime_rs/src/main.rs`). This version number does not imply that every ecosystem component is production-ready.

## Current priorities

- [ ] Align the published language specification with parser behavior and tested examples.
- [ ] Add a repeatable self-hosting/bootstrap comparison between the AAYU compiler source and bootstrap compiler.
- [ ] Expand end-to-end compiler/runtime coverage for features currently represented only in parser or emitter code.
- [ ] Harden database persistence with correct JSON escaping and an atomic replace strategy, or adopt a documented database backend.
- [ ] Add CI coverage for the Python tools, VS Code extension, and release-package contents.
- [ ] Reconcile repository license terms and embedded notices before broad redistribution.

## Later work

- [ ] Define and implement stable module/package resolution before publishing package-manager commands.
- [ ] Expand and document relational data support only if it remains a product goal.
- [ ] Improve UI/network feature completeness and production hardening.

Mark an item complete only when implementation, tests, documentation, and release artifacts agree.
