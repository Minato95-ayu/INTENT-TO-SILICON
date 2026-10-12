# AAYU Implemented Core Syntax

This is an implementation-aligned reference for the subset exercised through the Rust bootstrap compiler and Rust VM. Syntax being recognized in older AAYU source files does not imply that it can run.

## Variables, output, and expressions

```aayu
let count = 2
count = count + 3
print(count)
```

The tested subset includes integers, floats, strings, declarations, reassignment, unary minus, `+`, `-`, `*`, `/`, comparisons, and `print`.

Array/dictionary literals and indexed reads work, as do string character reads and `len` for strings and arrays:

```aayu
let values = [10, 20, 30]
let token = {"type": "IDENT"}
print(values[1])
print(token["type"])
print(len(values))
```

## Conditions and loops

```aayu
if count == 5
    print("five")
else
    print("not five")
end

let i = 0
while i < 3
    print(i)
    i = i + 1
end
```

The checked-in regression suite covers these forms, including float arithmetic, loops, and Fibonacci expressed with assignments and loops. Negative scalar values are also covered by a dedicated test.

VM integers are signed 48-bit values (`-140737488355328` through `140737488355327`). The compiler rejects literals outside that range; arithmetic that overflows it halts with an error.

## Not currently implemented by the compiler/VM

- Closures, named/default arguments, nested action declarations, indexed writes, and collection iteration helpers.
- Module imports and package dependency resolution. The files under `std/` and `official_packages/` are not a usable installed standard library or registry yet.
- The much broader `fn`, type, entity, `for`, async, and punctuation grammar shown in older design drafts.

User-defined `action` declarations, positional calls, local frames, return values, and recursion are implemented and exercised by `tests/test_06_functions.aayu`.

The VM contains Rust-side database, HTTP, UI, and math components, but the AAYU source language does not currently expose them as stable, tested standard-library APIs. Read [Known Limitations](../KNOWN_LIMITATIONS.md) before relying on them.
