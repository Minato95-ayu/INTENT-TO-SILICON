# Roadmap

AAYU is moving on two tracks.

**Track A: Architecture-First Software Factory**

This is the current verified product story. AAYU accepts business intent or `.aayu` source, builds architecture, and generates full-stack software.

**Track B: Experimental Runtime**

This is now real, but still early. Sprint 35 verifies that AAYU can execute its own logic through the bytecode and VM path.

## Current Status

| Track | Progress | Status |
|------|----------|--------|
| Track A: Software Factory | 100% | Freeze and stabilize |
| Track B: Runtime | 40% | Mature gradually |

## Sprint 35 Complete

Verified command:

```bash
python -m prototype.cli vm prototype/tests/demo_sprint35.aayu
```

Output:

```text
Founder
```

This proves:

```text
AAYU Source
down
Parser
down
Compiler
down
AYC
down
VM
down
Execution
```

## Sprint 36

**Functions**

```aayu
function greet(name)
    print(name)
end.

greet("Ayush")
```

Goal: make the runtime feel actually useful for small reusable logic.

## Sprint 37

**Loops**

```aayu
for i in 1..5
    print(i)
end.
```

Goal: basic repeated execution in the VM.

## Sprint 38

**Modules and Imports**

Goal: allow runtime programs to grow beyond a single file.

## Distribution Roadmap

- PyPI package polish for `pip install aayu`
- VS Code Marketplace release for syntax highlighting and snippets
- GitHub Linguist recognition for `.aayu`
- Documentation examples for real generated apps

## Long-Term Runtime Roadmap

- Collections
- Packages
- Runtime libraries
- Rust VM stabilization
- Standalone binaries for Windows, macOS, and Linux
- WebAssembly and edge deployment research
