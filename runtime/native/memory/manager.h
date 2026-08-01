#ifndef AAYU_MEMORY_MANAGER_H
#define AAYU_MEMORY_MANAGER_H

#include "allocator.h"
#include "arena.h"

// MemoryManager statistics
typedef struct {
    uint32_t heap_pages;
    uint32_t arena_blocks;
    uint32_t objects_count;
    size_t bytes_allocated;
    size_t peak_heap;
    size_t peak_arena;
    uint32_t peak_objects;
    
    // Extended Statistics
    uint32_t live_objects;
    size_t total_allocations;
    uint32_t peak_live_objects;
    size_t bytes_reused;
    uint32_t page_reuse_count;
} MemoryStats;

extern MemoryStats memory_stats;

void aayu_memory_init(void);
void aayu_memory_destroy(void);

// Persistent Allocation for Runtime Program structures (AycProgram)
void* aayu_persistent_alloc(size_t size);
void aayu_persistent_free(void* ptr);

// Debug Hooks
void aayu_debug_hook_on_alloc(void* ptr, size_t size, const char* subsystem);
void aayu_debug_hook_on_free(void* ptr, const char* subsystem);

// Print overall memory statistics
void aayu_print_memory_stats(void);

#endif // AAYU_MEMORY_MANAGER_H
