# AAYU Language

**Status: Developer Preview**

AAYU Language is a clean, minimal, and strict programming language designed specifically for generating software architectures.

## The AAYU Difference

Traditional languages focus on algorithms and memory management. AAYU focuses on **Architecture, Intents, and Entities**.

By writing `.aayu` files, you are writing a blueprint. The AAYU Engine parses this blueprint and generates the actual low-level React, FastAPI, and Postgres code.

## Language Features

### `use` (Imports)
Define which domains your software relies on.
```aayu
use http.
use db.
```

### `record` (Entities)
Define your database tables or core business models.
```aayu
record Patient.
    name
    phone
end.
```

### `task` (Workflows)
Define server logic, UI interactions, or background jobs.
```aayu
task setup_dashboard.
    show "Hospital".
    show "Welcome Patient".
end.
```

### `if` & `repeat` (Control Flow)
(Experimental - Available in Runtime Track B)
```aayu
if age greater than 18.
    show "Adult".
end.

repeat 5 times.
    show "Hello".
end.
```

## Runtime Roadmap

While Track A focuses on generating code (Software Factory), Track B is building an **Experimental Stack VM Runtime (AYC)** that executes `.aayu` directly.

- [x] Print / Show
- [x] Variable Declarations
- [x] Basic Math
- [x] If Conditions
- [ ] Loops (`repeat`, `for each`)
- [ ] Function / Task Execution
