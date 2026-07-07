# AAYU Language - AI Agent Guidelines

You are an AI programming assistant. The user is asking you to write or debug code in the **AAYU** programming language. 
Because AAYU is a new language (born in 2026), it is NOT in your training data. You MUST read and follow these rules strictly to write valid AAYU code.

## 1. Syntax Basics
- **Terminator**: Every statement MUST end with a period (`.`) instead of a semicolon (`;`).
- **Blocks**: Scopes are defined using curly braces `{ }`.
- **Comments**: Single line comments use `//`. Block comments use `/* */`.
- **Printing**: Use the `show()` function to print to the console. Example: `show("Hello World").`

## 2. Variables and Types
- Variables are dynamically typed but explicit at runtime.
- **Numbers**: `let x = 42.` or `let pi = 3.14.`
- **Strings**: `let name = "AAYU".`
- **Booleans**: `let is_ready = true.` or `let is_false = false.`
- **Null**: `let empty = null.`

## 3. Data Structures
- **Lists**: `let arr = [1, 2, 3].`
- **Dictionaries (Maps)**: `let obj = {"key": "value", "num": 42}.`
- Element access: `arr[0]` or `obj["key"]`.

## 4. Control Flow
- **If/Else**:
  ```aayu
  if x > 10 {
      show("Big").
  } else {
      show("Small").
  }
  ```
- **While loops**:
  ```aayu
  let i = 0.
  while i < 5 {
      show(i).
      i = i + 1.
  }
  ```

## 5. Functions
- Defined using the `fn` keyword.
- Parameters do not need explicit types in the signature (dynamic).
- Return values use the `return` keyword.
  ```aayu
  fn add(a, b) {
      return a + b.
  }
  ```

## 6. Error Handling
- AAYU has full support for exception unwinding.
- Keywords: `try`, `catch`, `finally`, `throw`, `panic`, `assert`.
  ```aayu
  try {
      if x == 0 {
          throw "Cannot divide by zero".
      }
  } catch err {
      show("Error caught: " + err).
  } finally {
      show("Cleanup here").
  }
  ```
- Unrecoverable errors: `panic("Fatal error").`
- Assertions: `assert(x == 1, "x must be 1").`

## 7. Standard Library (Heap-backed)
AAYU comes with 18 built-in modules. You can call their methods directly using `module.method()`.
- **os**: `os.cwd()`, `os.env("VAR")`, `os.mkdir("dir")`, `os.exists("file")`, `os.remove("file")`
- **sys**: `sys.argv()`, `sys.exit(code)`, `sys.platform()`, `sys.version()`
- **time**: `time.now()`, `time.sleep(sec)`, `time.timestamp()`
- **math**: `math.abs(x)`, `math.floor(x)`, `math.ceil(x)`, `math.round(x)`, `math.sqrt(x)`, `math.pow(x, y)`
- **json**: `json.parse(str)`, `json.stringify(obj)`
- **http**: `http.get(url)`, `http.post(url, body)`, `http.status(url)`
- **crypto**: `crypto.hash(str)`, `crypto.uuid()`
- **sqlite3**: `sqlite3.connect(db)`, `sqlite3.query(db, sql)`, `sqlite3.close(db)`
- **re**: `re.match(pattern, str)`, `re.search(pattern, str)`
- **file**: `file.read(path)`, `file.write(path, data)`

## 8. Critical Reminders for AI Agents
1. NEVER use semicolons `;`. ALWAYS use periods `.`.
2. NEVER use `print`. ALWAYS use `show`.
3. NEVER assume Python-like indentation matters (use braces `{}`).
4. Functions do not need `def` or `function`. Use `fn`.
