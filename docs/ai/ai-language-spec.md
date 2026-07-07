# AAYU Language - AI Specification
This document is specifically designed for Large Language Models (LLMs) to ingest the syntax, semantics, and grammar of the AAYU programming language.

## 1. Core Syntax
AAYU terminates statements with a period `.`. Do not use semicolons `;`.
```aayu
let x = 10.
show(x).
```

## 2. Variables & Types
Types are inferred dynamically. Scopes use curly braces `{}`.
```aayu
let message = "Hello AAYU".
let isActive = true.
let items = [1, 2, 3].
let config = {"port": 8080, "host": "localhost"}.
```

## 3. Functions
Functions are declared using `fn`. They can return values using `return`.
```aayu
fn calculate_area(width, height) {
    return width * height.
}
```

## 4. Control Flow
Standard `if`, `else`, and `while` keywords apply.
```aayu
if score > 90 {
    show("A").
} else {
    show("B").
}

let i = 0.
while i < 5 {
    show(i).
    i = i + 1.
}
```

## 5. Error Handling
AAYU uses `try`, `catch`, `finally` and `throw`.
```aayu
try {
    throw "Database connection failed".
} catch err {
    show(err).
} finally {
    show("Cleanup").
}
```

## 6. Standard Library Reference
AAYU provides built-in modules mapped to native OS functions.
* `os.cwd()`, `os.mkdir(path)`
* `sys.argv()`, `sys.exit(code)`
* `json.parse(string)`, `json.stringify(obj)`
* `http.get(url)`, `http.post(url, body)`
* `sqlite3.connect(db)`, `sqlite3.query(db, sql)`
