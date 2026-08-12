Specification: 06_MODULE_SYSTEM.md
Version: 0.1.0
Status:
[x] Draft
[ ] Review
[ ] Frozen
[ ] Deprecated

Owner: Compiler Team
Depends On: 01_LANGUAGE_SPEC
Compiler Version: >=0.5.0
Last Updated: 2026-08-04

---

# 06 Module System Spec (Frozen)

## Purpose
This document defines how AAYU resolves code reusability, scoping, and file imports.

## Definitions
- **Module:** A single `.aayu` file containing valid AAYU code.
- **Package:** A collection of modules governed by a `manifest.json`.

## Core Mechanics

### 1. Importing Modules
Modules can import other modules using the `import` keyword. Imports are resolved relative to the current file or from the standard library.
```aayu
import math.               // Standard library
import "./utils/helper".   // Relative local path
```

### 2. Exporting Symbols
By default, all definitions in a module are private. The `export` keyword exposes them to other modules.
```aayu
export task calculate() {
    return 42.
}

export model Config {
    port: Int
}
```

### 3. Namespacing
Imported modules act as a namespace object.
```aayu
import math.

let result = math.sqrt(16).
```
Developers can also alias imports:
```aayu
import math as m.
let result = m.sqrt(16).
```

## Compiler Rules
1. **Rule M.1:** The Semantic Analyzer MUST throw a `ModuleNotFoundError` if an imported file does not exist.
2. **Rule M.2:** The compiler MUST detect and throw a `CyclicImportError` if modules import each other in an infinite loop.
3. **Rule M.3:** If a module attempts to access an unexported symbol from another module, the Semantic Analyzer MUST throw an `AccessViolationError`.

## Status Update
- Changed from Draft to **Frozen**. Compiler team is authorized to implement.
