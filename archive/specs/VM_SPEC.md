# AAYU Native VM Specification v1.0

The AAYU Virtual Machine executes the AAYU Bytecode representation. It is designed to be highly portable, performant, and safe.

## Data Representation (`Value` struct)

All data in the VM is boxed in a uniform `Value` struct.

```c
typedef enum {
    VAL_NULL,
    VAL_INT,
    VAL_FLOAT,
    VAL_BOOL,
    VAL_STRING,
    VAL_WIDGET,
    VAL_ACTION,
    VAL_ARRAY,
    VAL_DICT
} ValueType;

typedef struct {
    ValueType type;
    union {
        long long i_val;
        double f_val;
        int b_val;
        char* s_val;
        struct { ... } widget;
        struct { ... } action;
        struct { ... } array;
        struct { ... } dict;
    } as;
} Value;
```

## Call Stack & Frames

The VM tracks standard function frames containing:
- `Instruction Pointer (ip)`: Index of the current bytecode.
- `Frame Pointer (fp)`: Index of the base stack value for the current frame.
- `Locals`: Scope values mapping variable offsets to `Value` structs.

## Exception Stack

Exceptions are handled via an independent Exception Stack:
- `ExceptionFrame`: Tracks the handler PC, original base pointer, and original stack size.
- A `throw` pops the current handler off the Exception Stack, restores the execution environment, pushes the thrown error value, and jumps to the catch block `ip`.

## Garbage Collection (Phase 11B)
Currently, memory is implicitly managed or relies on simple `free()` drops. Future specs will introduce a formal Mark-and-Sweep Garbage Collector with an Arena Allocator architecture.
