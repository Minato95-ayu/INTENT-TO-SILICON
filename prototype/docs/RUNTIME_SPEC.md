# AAYU Runtime Specification (v1.0)

This document freezes the bytecode format, Instruction Set Architecture (ISA), Stack Frame semantics, and execution behavior for AAYU Virtual Machine implementations.

---

## 1. Bytecode Format & Serialization Layout

AAYU bytecode (`.ayc` files) is stored as a structured JSON serialization of the compiled code object. The root object represents the main entry point (main frame) of the script, with nested compiled code objects for local tasks inside the Constant Pool.

### File Structure (JSON Schema)
```json
{
  "name": "string",
  "parameters": ["string"],
  "names": ["string"],
  "constants": [
    "value | BytecodeObject"
  ],
  "instructions": [
    ["OPCODE_NAME", operand_value]
  ]
}
```

- **`name`**: The identifier of the function/task. Empty (`""`) for the main entry point.
- **`parameters`**: An array of parameter names. Empty for the main entry point.
- **`names`**: Global/local identifier names referenced by index in `LOAD_NAME` / `STORE_NAME`.
- **`constants`**: The Constant Pool. Contains immediate values (numbers, strings, `None`) and nested compiled `Bytecode` objects representing task declarations.
- **`instructions`**: An ordered list of instruction tuples. Each instruction consists of:
  - `OPCODE_NAME`: A string representing the opcode.
  - `OPERAND`: An integer index or relative jump offset (or `null` if no operand is required).

---

## 2. AAYU Bytecode ISA (Instruction Set Architecture) v1

The AAYU Instruction Set consists of 18 frozen opcodes grouped into four categories:

### A. Memory & Scope Operations
| Opcode Name | Operand | Description | Stack Action |
|-------------|---------|-------------|--------------|
| `LOAD_CONST` | Index | Pushes constant at `constants[index]` onto stack. | `[] -> [value]` |
| `LOAD_NAME`  | Index | Loads variable at `names[index]` (checks local then global scope) and pushes to stack. | `[] -> [value]` |
| `STORE_NAME` | Index | Pops top of stack and stores in variable name at `names[index]` (in local scope if in task, else global). | `[value] -> []` |
| `POP`        | None    | Pops and discards the top value on the stack. | `[value] -> []` |

### B. Arithmetic Operations (Dynamic Types)
All arithmetic opcodes pop the right-hand operand, then the left-hand operand, and push the result.
| Opcode Name | Operand | Description | Stack Action |
|-------------|---------|-------------|--------------|
| `ADD`        | None    | Pushes `left + right` (supports numbers and strings concatenation). | `[left, right] -> [result]` |
| `SUB`        | None    | Pushes `left - right`. | `[left, right] -> [result]` |
| `MUL`        | None    | Pushes `left * right`. | `[left, right] -> [result]` |
| `DIV`        | None    | Pushes `left / right` (div by zero triggers AAYURuntimeError). | `[left, right] -> [result]` |

### C. Comparison & Logic Operations
| Opcode Name | Operand | Description | Stack Action |
|-------------|---------|-------------|--------------|
| `EQUAL`      | None    | Pushes boolean `left == right`. | `[left, right] -> [bool]` |
| `GREATER`    | None    | Pushes boolean `left > right`. | `[left, right] -> [bool]` |
| `LESS`       | None    | Pushes boolean `left < right`. | `[left, right] -> [bool]` |
| `NOT`        | None    | Pops top of stack and pushes boolean logical negation. | `[value] -> [not_value]` |

### D. Control Flow & Call Operations
Jump offsets are **continue-friendly relative offsets**. Jumps alter the Instruction Pointer (`ip`) directly.
| Opcode Name | Operand | Description | Stack Action |
|-------------|---------|-------------|--------------|
| `JUMP_FORWARD` | Offset | Unconditionally increments current `ip` by `operand`. | `[] -> []` |
| `JUMP_BACKWARD`| Offset | Unconditionally decrements current `ip` by `operand`. | `[] -> []` |
| `JUMP_IF_FALSE`| Offset | Pops condition. If falsy, increments current `ip` by `operand`. | `[cond] -> []` |
| `CALL_TASK`   | NumArgs | Pops task bytecode, pops `NumArgs` values, binds arguments to parameters, pushes a new frame, and sets caller `ip += 1`. | `[arg1...argN, task] -> []` |
| `RETURN`      | None    | Pops return value, pops current frame, and pushes return value onto calling frame's stack. | `[ret_val] -> []` |
| `PRINT`       | None    | Pops top of stack, prints it, and appends to output buffer. | `[value] -> []` |

---

## 3. CallFrame & Execution Semantics

The VM manages execution state via a Frame Stack: `self.frames`.

### CallFrame Layout
Every active execution context is encapsulated in a `CallFrame`:
```python
class CallFrame:
    bytecode: BytecodeObject  # Code block being executed
    locals: dict              # Local variable storage (names -> values)
    ip: int                   # Instruction Pointer (index in bytecode instructions)
    stack: list               # Local evaluation stack for temporary values
    frame_name: str           # For tracebacks and stack tracing
```

### Execution Loop
1. The VM pushes the `main` script bytecode as the first `CallFrame` (`self.frames = [main_frame]`).
2. At each cycle, the VM reads from the current frame: `current_frame = self.frames[-1]`.
3. If `current_frame.ip >= len(instructions)`, the frame has finished executing; the VM pops it and resumes the caller frame.
4. Otherwise, it executes the instruction at `current_frame.ip`:
   - Non-control-flow/non-call instructions automatically increment `current_frame.ip` by 1 at the end of the execution step.
   - Jumps or call operations modify `ip` (or push/pop frames) and invoke `continue` to bypass the step-level `ip` increment.

---

## 4. Scoping & Variable Lookup Rules

AAYU VM implements simple local-global scope resolution:
1. **Reads (`LOAD_NAME`)**:
   - Check `current_frame.locals`.
   - If not found, check `self.globals` (global scope).
   - If still not found, raise `AAYURuntimeError`.
2. **Writes (`STORE_NAME`)**:
   - If the frame stack has size 1 (`len(self.frames) == 1`), the store modifies the global scope `self.globals`.
   - If `len(self.frames) > 1` (executing a nested task), the store creates/updates the local scope `current_frame.locals`. This prevents local variables from leaking or polluting global scope.
