#ifndef AAYU_MEMORY_ARENA_H
#define AAYU_MEMORY_ARENA_H

#include <stddef.h>
#include <stdint.h>

#define ARENA_BLOCK_SIZE 65536 // 64KB blocks for Arena

typedef struct ArenaBlock {
    struct ArenaBlock* next;
    size_t used;
    size_t capacity;
    uint8_t* current;
    uint8_t data[];
} ArenaBlock;

typedef struct AayuArena {
    ArenaBlock* current_block;
    ArenaBlock* first_block;
    size_t total_allocated;
    size_t block_size;
} AayuArena;

AayuArena* aayu_arena_create(size_t block_size);
void* aayu_arena_alloc(AayuArena* arena, size_t size);
void aayu_arena_reset(AayuArena* arena); // O(1) bulk free via reuse
void aayu_arena_destroy(AayuArena* arena);

#endif // AAYU_MEMORY_ARENA_H
