# AAYU Language Handbook: The Ultimate Specification
*Bridging the Speed of C, the Simplicity of Python, and the Era of AI.*

> **Philosophy:** AI Agents shouldn't hallucinate. Vibe Coders shouldn't configure environments. Legend Developers shouldn't write boilerplate. 

---

## 1. Variables & Data Types (Memory Safety)
**C Problem:** Manual memory, pointers causing segfaults.
**Python Problem:** Everything is mutable, slow dynamic typing.
**AAYU Solution:** Strict immutability by default, explicit state, garbage collected but fast.

```aayu
# Immutable by default (Like Rust, but simple)
let name = "AAYU"
let version = 1.0

# Mutable state (Easy for UI and loops)
state counter = 0
counter = counter + 1

# Data Types
let is_fast = true         # Boolean
let price = 99.99          # Float
let cores = 8              # Int
let missing = null         # Null (Handled safely)
```

---

## 2. Control Flow & Loops (Logic)
**C/Python Problem:** Indentation errors (Python) or missing brackets `{}` (C) confuse AI agents.
**AAYU Solution:** Explicit `end` blocks. Impossible for AI to hallucinate scopes.

```aayu
# If / Else
if cores > 4
    print("Fast PC")
elif cores == 4
    print("Normal PC")
else
    print("Slow PC")
end

# While Loop
state i = 0
while i < 10
    print(i)
    i = i + 1
end

# For Each (Iterators)
let users = ["Ayush", "Rahul", "Aman"]
for u in users
    print(u)
end
```

---

## 3. Functions (Actions)
**Python Problem:** `def` doesn't enforce intent.
**C Problem:** Complex return type declarations.
**AAYU Solution:** `action` block. Action describes exact intent.

```aayu
action calculate_tax(amount, rate)
    let tax = amount * rate
    return tax
end

let total = calculate_tax(1000, 0.18)
```

---

## 4. Data Structures (Built-in)
**C Problem:** No built-in HashMaps, Arrays are manual.
**AAYU Solution:** Native Lists and Maps mapped directly to Rust's memory arena.

```aayu
# Lists (Dynamic Arrays)
state tasks = ["Code", "Eat"]
list::push(tasks, "Sleep")

# Maps (Dictionaries)
let config = {
    "port": 3000,
    "env": "production"
}
```

---

## 5. Structs & Classes (The `model` Revolution)
**C Problem:** `struct` is just memory.
**Python Problem:** `class` needs `__init__` boilerplate, external ORMs (SQLAlchemy) to save to DB.
**AAYU Solution:** `model`. It acts as a Class in memory AND a SQLite table automatically!

```aayu
model User
    id Int
    name String
    is_active Bool = true
end

# Usage (Memory + Database instantly synced)
let u = User.new(name: "Ayush")
u.save() # Instantly writes to built-in SQLite

let all_users = User.all() # Fetch from DB
```

---

## 6. The Standard Library (Zero Dependency)
**Python/Node Problem:** `pip install requests`, `npm install fs`. AI hallucinates wrong versions.
**AAYU Solution:** Everything a Vibe Coder needs is built into the `.aybc` runtime.

```aayu
# 1. File I/O (Native)
let text = file::read("data.txt")
file::write("log.txt", "Server started")

# 2. Web & Network (Native)
let json = http::get("https://api.github.com/zen")

# 3. AI / Math (Native)
let prediction = ai::linear_regression(data_x, data_y)
```

---

## 7. Full-Stack in One File (The Legend Move)
AAYU combines Backend, Frontend, and Database gracefully.

```aayu
app MyLegendApp

model Note
    id Int
    text String
end

# Backend Route
route "/api/notes"
    get
        respond(Note.all())
    end
end

# Frontend UI
Page Home
    Column
        Text("My Notes")
        Button("Fetch", onClick: fetchNotes)
    end
end

run Home
```

---
## Summary of AAYU's Supremacy:
1. **For AI Agents:** Fixed `end` scopes, Zero imports, Built-in Context Map prevents hallucination.
2. **For Vibe Coders:** No environment setup, no SQL queries, just write logic.
3. **For Legend Developers:** C-level memory speed (Rust VM backend), complete control over data architecture.
