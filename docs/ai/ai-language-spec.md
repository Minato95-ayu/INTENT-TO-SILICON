# AAYU Language - AI Specification
This document is specifically designed for Large Language Models (LLMs) to ingest the syntax, semantics, and grammar of the AAYU programming language.

## 1. Core Syntax
AAYU terminates statements with a period `.`. Do not use semicolons `;`.
Scopes are NOT defined by curly braces `{}`. Instead, blocks use the `end.` keyword.

```aayu
let x is 10.
show(x).
```

## 2. Variables & Types
Types are inferred dynamically. Assignment uses `is`.
```aayu
let message is "Hello AAYU".
let isActive is true.
let items is [1, 2, 3].
let config is {"port": 8080, "host": "localhost"}.
```

## 3. Functions
Functions are declared using `function` (or `task`). They end with `end.`.
```aayu
function calculate_area(width, height)
    return width * height.
end.
```

## 4. Control Flow
Standard `if`, `else`, and `while` keywords apply, but must be closed with `end.`.
```aayu
if score > 90
    show("A").
else
    show("B").
end.

let i is 0.
while i < 5
    show(i).
    i is i + 1.
end.
```

## 5. Error Handling
AAYU uses `try`, `catch`, `finally` and `throw`. They also close with `end.`.
```aayu
try
    throw "Database connection failed".
catch err
    show(err).
finally
    show("Cleanup").
end.
```

## 6. Standard Library Reference
AAYU provides built-in modules using the `::` namespace syntax.
* `file::read(path)`, `file::write(path, content)`, `file::exists(path)`
* `json::parse(string)`, `json::stringify(obj)`
* `math::max(a, b)`, `math::min(a, b)`, `math::floor(n)`
* `list::push(arr, val)`, `list::pop(arr)`, `list::length(arr)`
* `map::put(m, k, v)`, `map::get(m, k)`, `map::keys(m)`
* `crypto::sha256(text)`
* `db::connect(path)`, `db::query(cid, sql)`

