#ifndef AAYU_MEMORY_OBJECT_H
#define AAYU_MEMORY_OBJECT_H

#include <stdint.h>
#include <stdbool.h>

// Forward declaration of Value to resolve circular dependencies later


typedef enum {
    OBJ_STRING = 0,
    OBJ_ARRAY = 1,
    OBJ_DICT = 2,
    OBJ_CLOSURE = 3,
    OBJ_ACTION = 4,
    OBJ_WIDGET = 5,
    OBJ_NATIVE_HANDLE = 6,
    OBJ_RAW_BUFFER = 7
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

// String Object
typedef struct {
    AayuObject obj;
    uint32_t length;
    uint32_t capacity;
    char* chars;
} AayuString;

// Array Object
typedef struct {
    AayuObject obj;
    uint32_t count;
    uint32_t capacity;
    struct sValue* elements;
} AayuArray;

// Dictionary Entry
typedef struct {
    char* key;
    struct sValue value;
} DictPair;

// Dictionary Object
typedef struct {
    AayuObject obj;
    uint32_t count;
    uint32_t capacity;
    DictPair* entries;
} AayuDict;

typedef void (*NativeDestructor)(void* ptr);

// Native Handle Object
typedef struct {
    AayuObject obj;
    void* handle;
    NativeDestructor dtor;
    uint32_t handle_flags;
} AayuNativeHandle;

// Raw Buffer Object (for strings chars, array elements, etc.)
typedef struct {
    AayuObject obj;
    uint8_t data[]; // Flexible array member
} AayuRawBuffer;

#endif // AAYU_MEMORY_OBJECT_H
