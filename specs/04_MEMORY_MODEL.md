Specification: 04_MEMORY_MODEL.md
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

# AAYU Memory Model Specification v1.1

The AAYU Memory Model defines the strict rules for object allocation, lifetime management, and garbage collection within the AAYU Virtual Machine. 

## 1. Object Header Layout

All heap-allocated objects must inherit the base `AayuObject` header (32 bytes aligned). This ensures the Garbage Collector can universally traverse and manage all dynamically allocated memory.

```c
typedef enum {
    OBJ_STRING,
    OBJ_ARRAY,
    OBJ_DICT,
    OBJ_CLOSURE,
    OBJ_ACTION,
    OBJ_WIDGET,
    OBJ_NATIVE_HANDLE
} ObjectType;

// Base Object Header (32 bytes)
typedef struct sAayuObject {
    uint32_t type;          // 4 bytes (ObjectType enum)
    uint32_t flags;         // 4 bytes (e.g., is_marked, is_frozen)
    uint64_t size;          // 8 bytes (total size including header)
    struct sAayuObject* next; // 8 bytes (pointer to next in heap chain)
    uint32_t generation;    // 4 bytes (generational GC)
    uint32_t reserved;      // 4 bytes (magic value / padding)
} AayuObject;
```

## 2. Representation Semantics

Objects are represented dynamically in memory based on their type.

### Strings, Arrays, and Dictionaries
Follow the `AayuObject` header layout, containing lengths and data buffers.

### Native Handles (FFI Wrapper)
To expose C-level resources to AAYU securely, opaque pointers are wrapped:
```c
typedef void (*NativeDestructor)(void* ptr);

typedef struct {
    AayuObject obj;
    void* handle;            // Opaque pointer to native resource
    NativeDestructor dtor;   // Cleanup function called on Sweep
    uint32_t handle_flags;   // FFI specific flags
} AayuNativeHandle;
```

## 3. Reference and Value Semantics

* **Primitives (Value Types):** Small, statically sized types (`Int`, `Float`, `Bool`, `Null`) are passed by value.
* **Complex Types (Reference Types):** Large or dynamically sized types are passed by reference via `AayuObject*`.

## 4. Memory Subsystems

The AAYU Memory Manager isolates memory lifecycles:
1. **Heap Allocator:** Page-based block allocator for runtime objects. Subject to Garbage Collection.
2. **Arena Allocator:** Block-based chunk allocator solely used for compiler IR and temporary structures (like Bytecode Loading). Arena memory is NEVER garbage collected; it is reset or destroyed in bulk (O(1)).

## 5. Garbage Collection (Phase 11B)

The VM employs a Stop-the-World, Mark-and-Sweep Garbage Collector targeting only the Heap Allocator.

### Formal GC Roots
An object is considered a "Root" (alive) if referenced by any of the following mandatory sources, in this priority order:

1. **VM Stack:** Temporary expression values and arguments.
2. **Call Frames:** Explicit root for closures and execution contexts.
3. **Globals:** Top-level module states and variables.
4. **Modules:** Cached module definitions and imports.
5. **Native Handles:** Registered active C bindings/FFI wrappers.
6. **Runtime Constants:** 
   - *Permanent*: String literals and builtin constants.
   - *Module*: Removable constants specific to a module.

### The Mark Phase
Iterates through all formal GC roots, marking objects. It uses a Gray Stack to recursively mark children without C-stack recursion limits.

### The Sweep Phase
Iterates through the Heap's free lists or page blocks. Unmarked objects are finalized (destructors run) and their memory returned to the allocator blocks.
