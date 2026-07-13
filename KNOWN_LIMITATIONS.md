# AAYU v1.0 Release Candidate: Known Limitations

As AAYU enters the Release Candidate phase for Stable 1.0, the compiler, VM, and ecosystem are functionally complete and highly stable for their intended scopes. However, to ensure production transparency, the following features are deliberately omitted from the 1.0 scope and will be addressed in future phases (e.g., Phase 7 or v2.0).

## 1. Web Transpiler Limitations
The AST-to-Web IDOM transpiler correctly manages routing, state variables, component trees, and basic actions mapping to vanilla JavaScript. It **does not** yet support:
- ✗ Canvas/WebGL graphics context.
- ✗ CSS Grid/Flexbox complex animation transitions natively.
- ✗ Raw WebSockets natively bound via state (requires explicit JS bridging).

## 2. Debugger
The integrated `aayu debug` pipeline leverages source-maps and standard Debug Adapter Protocols. It provides breakpoints, stepping, and local variable inspection. It **does not** support:
- ✗ Live Edit-and-Continue (hot-reloading bytecode injects).
- ✗ Multi-threaded race condition visualization natively.

## 3. Package Management
The `intent` package manager fetches and caches local and remote packages cleanly. It **does not** support:
- ✗ Cryptographic package signing or SHA-256 verification (on the roadmap for Phase 7).
- ✗ Automatic dependency conflict resolution across complex sub-graphs (defaults to flat hoisting).

## 4. UI Widgets (Desktop)
The embedded `pygame`-backed native renderer handles containers, text, buttons, and flex layouts effectively.
- ✗ SVG Vector rendering is primitive.
- ✗ Accessible Screen Reader (A11Y) bindings to OS APIs are incomplete.