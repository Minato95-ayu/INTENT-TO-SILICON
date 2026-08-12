Specification: 18_STDLIB_SPEC.md
Version: 0.1.0
Status:
[x] Draft
[ ] Review
[ ] Frozen
[ ] Deprecated

Owner: Compiler Team
Depends On: 00_ARCHITECTURE
Compiler Version: >=0.5.0
Last Updated: 2026-08-04

---

# AAYU Standard Library Specification v1.0

The AAYU Standard Library is natively integrated into the compiler and VM, ensuring that essential infrastructure components are universally available without external dependencies.

## Native Namespaces

### 1. File System (`fs`)
Handles local file I/O operations asynchronously.
- `fs.read(path)`: Returns the string contents of a file.
- `fs.write(path, data)`: Writes string data to a file.

### 2. Networking (`http`)
Handles client networking requests asynchronously.
- `http.get(url)`: Performs an HTTP GET request, returning a dictionary: `{ status: Int, data: String }`.
- `http.post(url, payload)`: Performs an HTTP POST request.

### 3. Storage (`db`)
Handles interactions with the natively abstracted data storage engine.
- `db.query(sql_string)`: Evaluates a query, returning an array of row objects (dictionaries).

## Native Globals

- `print(args...)`: Outputs data to the console or log stream.

## Types

### Dictionaries (`Dict`)
Key-value pair map.
- Keys must be strings.
- Accessible via postfix operator `.` (e.g. `obj.name`) or index operator `[]` (e.g. `obj["name"]`).

### Arrays (`Array`)
Ordered lists of items.
- Accessible via index operator `[]` (e.g. `list[0]`).
- Native function `.length()` returns integer length of the array.

### Strings (`String`)
UTF-8 character sequences.
- Supports native concatenation using `+`.
- Supports length calculation.
