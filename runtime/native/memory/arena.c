#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "arena.h"
#include "os_mem.h"
#include "manager.h" // For memory_stats update

static ArenaBlock* alloc_block(size_t block_size) {
    ArenaBlock* block = (ArenaBlock*)os_alloc_pages(block_size);
    block->next = NULL;
    block->used = 0;
    block->capacity = block_size - sizeof(ArenaBlock);
    block->current = block->data;
    
    memory_stats.arena_blocks++;
    return block;
}

AayuArena* aayu_arena_create(size_t block_size) {
    if (block_size == 0) block_size = ARENA_BLOCK_SIZE;
    AayuArena* arena = (AayuArena*)os_alloc_pages(sizeof(AayuArena)); // Standard malloc fallback in os_mem is fine for this small struct
    arena->block_size = block_size;
    arena->first_block = alloc_block(block_size);
    arena->current_block = arena->first_block;
    arena->total_allocated = 0;
    return arena;
}

void* aayu_arena_alloc(AayuArena* arena, size_t size) {
    if (!arena) return NULL;
    
    // 8-byte alignment
    size = (size + 7) & ~7;
    
    if (size > arena->current_block->capacity) {
        printf("Out of memory: Arena object too large!\n");
        exit(1);
    }
    
    if (arena->current_block->used + size > arena->current_block->capacity) {
        if (arena->current_block->next) {
            // Reuse existing block if resetting happened
            arena->current_block = arena->current_block->next;
        } else {
            // Allocate new block
            ArenaBlock* new_block = alloc_block(arena->block_size);
            arena->current_block->next = new_block;
            arena->current_block = new_block;
        }
    }
    
    void* ptr = arena->current_block->current;
    arena->current_block->current += size;
    arena->current_block->used += size;
    
    arena->total_allocated += size;
    memory_stats.bytes_allocated += size;
    if (arena->total_allocated > memory_stats.peak_arena) {
        memory_stats.peak_arena = arena->total_allocated;
    }
    
    return ptr;
}

void aayu_arena_reset(AayuArena* arena) {
    if (!arena) return;
    ArenaBlock* block = arena->first_block;
    while (block != NULL) {
        // Memory Poisoning to catch use-after-reset bugs in debug
        memset(block->data, 0xCC, block->capacity);
        
        block->used = 0;
        block->current = block->data;
        block = block->next;
    }
    arena->current_block = arena->first_block;
    
    // Update stats
    memory_stats.bytes_reused += arena->total_allocated;
    memory_stats.page_reuse_count += 1;
    
    memory_stats.bytes_allocated -= arena->total_allocated;
    arena->total_allocated = 0;
}

void aayu_arena_destroy(AayuArena* arena) {
    if (!arena) return;
    ArenaBlock* block = arena->first_block;
    while (block != NULL) {
        ArenaBlock* next = block->next;
        os_free_pages(block, arena->block_size);
        memory_stats.arena_blocks--;
        block = next;
    }
    
    memory_stats.bytes_allocated -= arena->total_allocated;
    os_free_pages(arena, sizeof(AayuArena));
}
