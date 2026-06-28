# AAYU Language Grammar (v1)

Date: 2026-06-28
Status: Accepted

This document defines the official grammar for AAYU v1.0. All compiler and parser implementations must adhere strictly to this specification.

## Core Principles
1. **Human-Readable**: Keywords resemble plain English (e.g., `is`, `with`, `and`).
2. **Deterministic Termination**: Every statement and declaration ends with a period `.`. Blocks terminate with `end.`.
3. **Intent-Driven**: Built around high-level constructs (`system`, `entity`, `task`, `page`, `workflow`) rather than low-level memory operations.

## Lexical Structure
- **Identifiers**: `[a-zA-Z_][a-zA-Z0-9_]*`
- **Keywords**: `system`, `entity`, `task`, `page`, `workflow`, `record`, `is`, `with`, `and`, `end`, `if`, `else`, `while`, `repeat`, `for`, `each`, `in`, `use`, `run`, `return`, `create`, `find`, `update`, `delete`, `serve`, `route`, `render`, `form`, `guard`, `session`, `allow`, `step`.
- **Operators**: `+`, `-`, `*`, `/`, `==`, `<`, `>`, `<=`, `>=`.
- **Strings**: Text enclosed in `"` (double quotes).

## Structural Nodes

### System Definition
```aayu
system Identifier.
    [declarations]
end.
```

### Entity / Record Definition
```aayu
entity Identifier.
    [fields]
end.
```

### Task Definition
```aayu
task Identifier [with Identifier {and Identifier}].
    [statements]
end.
```

### UI Page Definition
```aayu
page Identifier.
    [ui_elements]
end.
```

### Workflow Definition
```aayu
workflow Identifier for EntityName.
    step Identifier [requires Role].
    [statements]
    end.
end.
```

## Statements

### Variables
```aayu
type Identifier is Expression.
```

### Control Flow
```aayu
if Expression is Comparator Expression.
    [statements]
end.
```
```aayu
while Expression.
    [statements]
end.
```
```aayu
repeat Expression times.
    [statements]
end.
```

### Execution
```aayu
run Identifier [with Expression {and Expression}].
```
```aayu
return Expression.
```

### Server & Routing
```aayu
serve on Port.
```
```aayu
route "Path" to TaskName.
```

## Expressions
- Mathematical: `a + b`, `a * 5`
- Functional: `run taskName`
- Database: `find EntityName`, `create EntityName`
- Primitive: Numbers, Strings
