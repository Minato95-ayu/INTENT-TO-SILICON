#include <stdio.h>
#include <assert.h>
#include <stdint.h>
#include "../../runtime/native/vm.h"
#include "../../runtime/native/memory/allocator.h"
#include "../../runtime/native/memory/os_mem.h"

// Expose internal current_page for testing
extern HeapPage* current_page;
extern HeapStats gc_stats;

void test_alignment() {
    printf("Running Alignment Test...\n");
    for (int i = 1; i <= 200; i++) {
        void* ptr = aayu_alloc_raw(i);
        assert(((uintptr_t)ptr % 8) == 0);
    }
    printf("Alignment Test Passed.\n");
}

void test_stress_alloc() {
    printf("Running Stress Alloc Test...\n");
    for (int i = 0; i < 1000000; i++) {
        aayu_alloc_raw(32);
    }
    assert(gc_stats.currently_allocated == 0); // Raw allocs don't bump currently_allocated stats, only aayu_alloc does!
    
    // Test with aayu_alloc
    for (int i = 0; i < 100000; i++) {
        aayu_alloc(64, OBJ_STRING);
    }
    assert(gc_stats.objects_count == 100000);
    printf("Stress Alloc Test Passed.\n");
}

void test_leak_and_fragmentation() {
    printf("Running Leak Test...\n");
    aayu_heap_destroy(); // Free the previous tests
    
    // Re-init
    aayu_heap_init();
    
    // Allocate various sizes
    for (int i = 0; i < 50000; i++) {
        aayu_alloc(16, OBJ_STRING);
        aayu_alloc(128, OBJ_ARRAY);
        aayu_alloc(32, OBJ_DICT);
        aayu_alloc(512, OBJ_STRING);
        aayu_alloc(64, OBJ_ARRAY);
        aayu_alloc(256, OBJ_DICT);
    }
    
    // Now destroy the heap
    aayu_heap_destroy();
    
    assert(current_page == NULL);
    assert(gc_objects == NULL);
    printf("Leak Test Passed (All pages freed).\n");
}

int main() {
    aayu_heap_init();
    
    test_alignment();
    test_stress_alloc();
    test_leak_and_fragmentation();
    
    aayu_heap_destroy();
    
    printf("\nAll Heap Allocator Tests Passed!\n");
    return 0;
}
