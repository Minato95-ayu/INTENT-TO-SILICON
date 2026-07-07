# Runtime Environment

The AAYU Runtime is the experimental execution path for AAYU Bytecode (`.ayc` files).

AAYU's primary verified capability is still the Architecture-First Software Factory: compile AAYU architecture into production-ready application stacks. The runtime is Track B: a growing VM layer that lets AAYU execute its own logic directly.

## Sprint 35 Verification

The current milestone verifies the complete prototype path:

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

Command:

```bash
python -m prototype.cli vm prototype/tests/demo_sprint35.aayu
```

Output:

```text
Founder
```

This is important because it proves AAYU is not only generating software; it can now execute AAYU logic through its own VM path.

## Current Runtime Support

The verified runtime surface is intentionally small:

- Variables
- Print
- If

The following features are still roadmap work:

- Functions
- Loops
- Modules
- Collections
- Packages
- Runtime libraries

## The AAYU Virtual Machine

The current VM is a prototype stack-based execution engine. It consumes bytecode produced by the compiler and executes instructions by maintaining an evaluation stack and runtime scope.

This page should be read as runtime documentation for the experimental track, not as a promise that AAYU is already a fully mature programming platform.

## Next Runtime Milestones

### Sprint 36: Functions

```aayu
function greet(name)
    print(name)
end.

greet("Ayush")
```

### Sprint 37: Loops

```aayu
for i in 1..5
    print(i)
end.
```

### Sprint 38: Modules

```aayu
import users.
```

## Future Rust Runtime

The long-term runtime target is a Rust implementation (`aayu-rs`) that can execute `.ayc` bytecode efficiently and portably. That work should mature only after the Python prototype proves the core execution model.
