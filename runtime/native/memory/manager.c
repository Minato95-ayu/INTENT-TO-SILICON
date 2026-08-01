#include <stdio.h>
#include <stdlib.h>
#include "manager.h"

MemoryStats memory_stats;

void aayu_memory_init(void) {
    memory_stats.heap_pages = 0;
    memory_stats.arena_blocks = 0;
    memory_stats.objects_count = 0;
    memory_stats.bytes_allocated = 0;
    memory_stats.peak_heap = 0;
    memory_stats.peak_arena = 0;
    memory_stats.peak_objects = 0;
    
    memory_stats.live_objects = 0;
    memory_stats.total_allocations = 0;
    memory_stats.peak_live_objects = 0;
    memory_stats.bytes_reused = 0;
    memory_stats.page_reuse_count = 0;
    
    // Initialize subsystems
    aayu_heap_init();
}

void aayu_memory_destroy(void) {
    aayu_heap_destroy();
}

void* aayu_persistent_alloc(size_t size) {
    void* ptr = malloc(size); // Using stdlib malloc for persistent runtime metadata
    aayu_debug_hook_on_alloc(ptr, size, "Persistent");
    return ptr;
}

void aayu_persistent_free(void* ptr) {
    if (!ptr) return;
    aayu_debug_hook_on_free(ptr, "Persistent");
    free(ptr);
}

void aayu_debug_hook_on_alloc(void* ptr, size_t size, const char* subsystem) {
    // Stub for future sanitizer / leak detector integration
    (void)ptr; (void)size; (void)subsystem;
}

void aayu_debug_hook_on_free(void* ptr, const char* subsystem) {
    // Stub for future sanitizer / leak detector integration
    (void)ptr; (void)subsystem;
}

void aayu_print_memory_stats(void) {
    printf("=== Memory Manager Statistics ===\n");
    printf("Total Allocations: %zu\n", memory_stats.total_allocations);
    printf("Total Bytes Alloc: %zu bytes\n", memory_stats.bytes_allocated);
    printf("Heap Pages:        %u\n", memory_stats.heap_pages);
    printf("Arena Blocks:      %u\n", memory_stats.arena_blocks);
    printf("Live Objects:      %u\n", memory_stats.live_objects);
    printf("Peak Live Objects: %u\n", memory_stats.peak_live_objects);
    printf("Peak Heap:         %zu bytes\n", memory_stats.peak_heap);
    printf("Peak Arena:        %zu bytes\n", memory_stats.peak_arena);
    printf("Bytes Reused:      %zu bytes\n", memory_stats.bytes_reused);
    printf("=================================\n");
}
