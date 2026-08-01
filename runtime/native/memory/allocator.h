#ifndef AAYU_MEMORY_ALLOCATOR_H
#define AAYU_MEMORY_ALLOCATOR_H

#include <stddef.h>
#include <stdint.h>
#include "../vm.h"
#include "object.h"

extern AayuObject* gc_objects; // Head of the global linked list of all objects

// --- Heap Manager & Page Allocator ---

#define AAYU_PAGE_SIZE 4096

typedef struct HeapPage {
    struct HeapPage* next;
    uint32_t used;
    uint32_t capacity;
    uint8_t* current;
    uint8_t data[];
} HeapPage;

// Initialize the memory subsystem
void aayu_heap_init(void);

// Destroy the heap and free all pages
void aayu_heap_destroy(void);

// Allocate a new page from the OS
HeapPage* aayu_new_page(void);

// Allocate raw bytes from the heap (bump allocator)
void* aayu_alloc_raw(size_t size);

// Allocate an object of a given size, tracking it in the global object list
void* aayu_alloc(size_t size, ObjectType type);

// Duplicate a string onto the AAYU heap
char* aayu_strdup(const char* s);

// Free an AayuObject directly into the segregated Free Lists
void aayu_free_object(AayuObject* obj);

// Allocate a raw buffer managed by GC
AayuRawBuffer* aayu_alloc_buffer(size_t data_size);

// Check if a pointer belongs to the GC heap
int is_heap_object(void* ptr);

// Note: For backwards compatibility with raw frees
void aayu_free(void* ptr);

// Print current heap statistics
void print_heap_stats(void);

#endif // AAYU_MEMORY_ALLOCATOR_H
