# AAYU Object Model Specification v1.0

The AAYU Object Model defines the strict structural layout, alignment, padding, and inheritance mechanisms for all heap-allocated objects in the VM. This canonical specification ensures stability for future JIT and LLVM integration.

## 1. Base Header (`struct AayuObject`)

Every heap-allocated object must begin with the `AayuObject` header. The VM relies on this header for polymorphism and memory management.

```c
typedef enum {
    OBJ_STRING = 0,
    OBJ_ARRAY = 1,
    OBJ_DICT = 2,
    OBJ_CLOSURE = 3,
    OBJ_ACTION = 4,
    OBJ_WIDGET = 5
} ObjectType;

// Base Object Header
typedef struct sAayuObject {
    ObjectType type;          // 4 bytes (assuming 32-bit enum)
    uint32_t flags;           // 4 bytes (e.g., is_marked, is_frozen)
    uint32_t ref_count;       // 4 bytes (for RC or hybrid analysis)
    // 4 bytes padding on 64-bit systems to ensure pointer alignment
    struct sAayuObject* next; // 8 bytes (pointer to next in heap chain)
} AayuObject;
```
*Note on Alignment: The structure size is explicitly padded to align pointers (e.g., 24 bytes on x64), preventing hardware alignment penalties.*

## 2. Virtual Table (VTable) Concept

While C does not natively support OOP vtables, the AAYU VM implements a pseudo-vtable via switch-dispatch on `type`. Future iterations (for JIT) may map `type` directly to function pointer arrays for O(1) dispatch.

- `type == OBJ_STRING` maps to string operations (`len`, `concat`).
- `type == OBJ_ARRAY` maps to list operations (`push`, `pop`, `len`).

## 3. Concrete Layouts & Inheritance

Structs "inherit" by placing `AayuObject` as their *very first* member. This allows safe C-style casting: `(AayuObject*)my_string_ptr`.

### AayuString
```c
typedef struct {
    AayuObject obj;           // Offset 0
    uint32_t length;          // Offset 24
    uint32_t capacity;        // Offset 28
    char* chars;              // Offset 32 (Heap pointer to utf-8 buffer)
} AayuString;
```

### AayuArray
```c
typedef struct {
    AayuObject obj;           // Offset 0
    uint32_t count;           // Offset 24
    uint32_t capacity;        // Offset 28
    Value* elements;          // Offset 32 (Heap pointer to contiguous Values)
} AayuArray;
```

### AayuDict
```c
typedef struct {
    AayuObject obj;           // Offset 0
    uint32_t count;           // Offset 24
    uint32_t capacity;        // Offset 28
    DictEntry* entries;       // Offset 32 (Heap pointer to hash buckets)
} AayuDict;
```

## 4. Pointer Rules and JIT Assumptions

1. **Header Invariance:** The `AayuObject` header must never shift size dynamically. Its offset must remain `0` in all subclasses.
2. **Buffer Pointers:** Inner pointers (`chars`, `elements`) must point to heap memory allocated by `aayu_alloc()`, NOT static memory, to ensure `aayu_free()` behaves uniformly.
3. **Future JIT Assumption:** The JIT compiler will emit machine code that hardcodes these byte offsets (e.g., `+24` for string length). Any modification to this spec requires recompilation of the LLVM backend.
