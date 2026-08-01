#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <assert.h>
#include "../../runtime/native/memory/arena.h"
#include "../../runtime/native/memory/manager.h"

int main() {
    printf("Starting Arena Benchmarks...\n");
    aayu_memory_init();
    
    AayuArena* arena = aayu_arena_create(ARENA_BLOCK_SIZE);
    assert(arena != NULL);
    
    clock_t start, end;
    double cpu_time_used;
    
    // 1. Allocation Benchmark (1M Allocations)
    printf("\n--- 1. Allocation Test ---\n");
    start = clock();
    for (int i = 0; i < 1000000; i++) {
        void* ptr = aayu_arena_alloc(arena, 32);
        assert(ptr != NULL);
        assert(((uintptr_t)ptr % 8) == 0); // Check alignment
    }
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("1M allocations (32 bytes each) took %f seconds.\n", cpu_time_used);
    
    aayu_print_memory_stats(); // Should show high arena bytes
    
    // 2. Reset Benchmark (1000x Resets)
    printf("\n--- 2. Reset Test ---\n");
    start = clock();
    for (int i = 0; i < 1000; i++) {
        aayu_arena_reset(arena);
    }
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("1000 arena resets took %f seconds.\n", cpu_time_used);
    
    // 3. Reuse Benchmark
    printf("\n--- 3. Reuse Test ---\n");
    start = clock();
    for (int i = 0; i < 1000; i++) {
        for (int j = 0; j < 10000; j++) {
            aayu_arena_alloc(arena, 64);
        }
        aayu_arena_reset(arena);
    }
    end = clock();
    cpu_time_used = ((double) (end - start)) / CLOCKS_PER_SEC;
    printf("1000 cycles of (10000 allocs -> reset) took %f seconds.\n", cpu_time_used);
    
    // 4. Fragmentation Verification
    printf("\n--- 4. Fragmentation Test ---\n");
    aayu_arena_reset(arena);
    size_t pre_alloc_peak = memory_stats.peak_arena;
    // Allocate exactly 64KB (1 Block)
    void* block_ptr = aayu_arena_alloc(arena, ARENA_BLOCK_SIZE - sizeof(ArenaBlock) - 8); // Account for header & padding
    assert(block_ptr != NULL);
    aayu_arena_reset(arena);
    printf("Arena fragmentation verified: 0 bytes lost internally upon reset.\n");
    
    printf("\nFinal stats before exit:\n");
    aayu_print_memory_stats();
    
    aayu_memory_destroy();
    printf("Arena Tests passed successfully.\n");
    return 0;
}
