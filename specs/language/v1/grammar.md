# AAYU Implemented Core Syntax

**Status:** implementation-aligned working reference, not a frozen complete language specification.

This page describes the syntax exercised by the checked-in core examples and supported by the current compiler pipeline. Older drafts describing `system`, `entity`, period-terminated statements, or a mandatory LLVM backend do not describe this implementation.

## Program structure

A source file contains statements. Whitespace separates tokens; blocks end with `end`. Statements do not require a trailing period.

```aayu
let name = "AAYU"
print(name)
```

## Variables and expressions

```aayu
let count = 0
let total = 0
total = total + count
```

The tested expression grammar supports integer, float, and string literals, identifier references, parentheses, calls, unary minus, array/dictionary literals, indexed reads, and these binary operators: `+`, `-`, `*`, `/`, `==`, `!=`, `<`, `>`, `<=`, `>=`.

## Control flow

```aayu
if count < 10
    count = count + 1
else
    print("done")
end

while count < 20
    count = count + 1
end
```

## Actions and returns

The Rust bootstrap compiler and VM support action declarations, positional calls, local frames, returns, and recursion. A representative form is:

```aayu
action add(a, b)
    return a + b
end

let result = add(2, 3)
print(result)
```

See `tests/test_06_functions.aayu` for a recursive factorial regression. Closures, named/default arguments, and nested actions are not supported.

## Syntax covered by the core regression examples

The checked-in AAYU examples cover variable declarations, strings, signed integer and floating-point arithmetic, assignments, `while`, `if`/`else`, user actions, arrays, dictionaries, global state, and output with `print`. See `tests/test_01_vars.aayu` through `tests/test_09_globals.aayu`.

The parser also recognizes higher-level constructs such as `app`, `model`, `route`, and `page`; their end-to-end runtime support is feature-specific and should be checked against the confidence report and tests. Do not assume this page specifies every recognized keyword or guarantees all parsed constructs execute.
