#ifndef AAYU_RUNTIME_H
#define AAYU_RUNTIME_H

#include <stddef.h>
#include <stdint.h>

// Core Type Definitions
typedef struct AayuObject AayuObject;
typedef struct AayuString AayuString;
typedef struct AayuArray AayuArray;

// GC & Memory
void aayu_gc_init();
void* aayu_alloc(size_t size);
void aayu_gc_collect();

// Strings
AayuString* aayu_string_new(const char* cstr);
AayuString* aayu_string_concat(AayuString* a, AayuString* b);
void aayu_print(AayuString* str);

// Panic & Error Handling
void aayu_panic(const char* msg);

#endif // AAYU_RUNTIME_H
