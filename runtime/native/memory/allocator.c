#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "../vm.h"
#include "allocator.h"
#include "os_mem.h"
#include "manager.h"

AayuObject* gc_objects;
HeapPage* current_page;

#define NUM_SIZE_CLASSES 16
static const size_t size_classes[NUM_SIZE_CLASSES] = {
    16, 24, 32, 40, 48, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 512
};
AayuObject* free_lists[NUM_SIZE_CLASSES];

static int get_bucket_index(size_t size) {
    for (int i = 0; i < NUM_SIZE_CLASSES; i++) {
        if (size <= size_classes[i]) return i;
    }
    return -1;
}

void aayu_heap_init(void) {
    gc_objects = NULL;
    current_page = NULL;
    for (int i = 0; i < NUM_SIZE_CLASSES; i++) {
        free_lists[i] = NULL;
    }
}

HeapPage* aayu_new_page(void) {
    HeapPage* page = (HeapPage*)os_alloc_pages(AAYU_PAGE_SIZE);
    assert(page != NULL);
    page->next = current_page;
    page->used = 0;
    page->capacity = AAYU_PAGE_SIZE - sizeof(HeapPage);
    page->current = page->data;
    current_page = page;
    memory_stats.heap_pages++;
    return page;
}

void aayu_heap_destroy(void) {
    HeapPage* page = current_page;
    while (page != NULL) {
        HeapPage* next = page->next;
        os_free_pages(page, AAYU_PAGE_SIZE);
        memory_stats.heap_pages--;
        page = next;
    }
    current_page = NULL;
    gc_objects = NULL;
    for (int i = 0; i < NUM_SIZE_CLASSES; i++) {
        free_lists[i] = NULL;
    }
}

int is_heap_object(void* ptr) {
    if (!ptr) return 0;
    HeapPage* page = current_page;
    while (page) {
        if ((uint8_t*)ptr >= page->data && (uint8_t*)ptr < (page->data + page->capacity)) {
            return 1;
        }
        page = page->next;
    }
    return 0;
}

void* aayu_alloc_raw(size_t size) {
    // Alignment to 8 bytes
    size = (size + 7) & ~7;
    
    if (size > AAYU_PAGE_SIZE - sizeof(HeapPage)) {
        printf("Out of memory: Object too large for 4KB page bump allocator.\n");
        exit(1);
    }
    
    if (current_page == NULL || current_page->used + size > current_page->capacity) {
        aayu_new_page();
    }
    
    void* ptr = current_page->current;
    current_page->current += size;
    current_page->used += size;
    
    assert(ptr != NULL);
    assert(((uintptr_t)ptr % 8) == 0);
    
    // Poison fresh allocation
    memset(ptr, 0xAA, size);
    
    return ptr;
}

void* aayu_alloc(size_t size, ObjectType type) {
    size_t aligned_size = (size + 7) & ~7;
    void* mem = NULL;
    
    // Check Free Lists first
    int bucket = get_bucket_index(aligned_size);
    if (bucket != -1 && free_lists[bucket] != NULL) {
        AayuObject* reused = free_lists[bucket];
        free_lists[bucket] = reused->next;
        // Memory poisoning: Unpoison the object
        memset(reused, 0xAA, size_classes[bucket]);
        memory_stats.bytes_reused += size_classes[bucket];
        mem = reused;
    } else {
        mem = aayu_alloc_raw(size);
    }
    
    AayuObject* object = (AayuObject*)mem;
    object->type = type;
    object->flags = 0;
    object->size = aligned_size;
    object->generation = 0;
    object->reserved = 0xCAFEBABE; // Magic value
    
    // Add to global linked list
    object->next = gc_objects;
    gc_objects = object;
    
    // Update stats
    memory_stats.bytes_allocated += aligned_size;
    if (memory_stats.bytes_allocated > memory_stats.peak_heap) {
        memory_stats.peak_heap = memory_stats.bytes_allocated;
    }
    memory_stats.objects_count++;
    if (memory_stats.objects_count > memory_stats.peak_objects) {
        memory_stats.peak_objects = memory_stats.objects_count;
    }
    
    return mem;
}

void aayu_free_object(AayuObject* obj) {
    if (!obj) return;
    
    int bucket = get_bucket_index(obj->size);
    if (bucket != -1) {
        size_t block_size = size_classes[bucket];
        // Poison the freed memory
        memset(obj, 0xDD, block_size);
        
        // Re-establish next pointer inside poisoned memory
        obj->next = free_lists[bucket];
        free_lists[bucket] = obj;
    }
    // If it's larger than 512, it leaks for now (or until page is freed)
}

void aayu_free(void* ptr) {
    // Generic aayu_free could defer to aayu_free_object if it's an AayuObject
    if (!ptr) return;
    AayuObject* obj = (AayuObject*)ptr;
    aayu_free_object(obj);
}

char* aayu_strdup(const char* s) {
    if (!s) return NULL;
    size_t len = strlen(s);
    AayuRawBuffer* buf = (AayuRawBuffer*)aayu_alloc(sizeof(AayuRawBuffer) + len + 1, OBJ_RAW_BUFFER);
    memcpy(buf->data, s, len + 1);
    return (char*)buf->data;
}

AayuRawBuffer* aayu_alloc_buffer(size_t data_size) {
    size_t total_size = sizeof(AayuRawBuffer) + data_size;
    AayuRawBuffer* buffer = (AayuRawBuffer*)aayu_alloc(total_size, OBJ_RAW_BUFFER);
    return buffer;
}

void print_heap_stats(void) {
    aayu_print_memory_stats();
}
