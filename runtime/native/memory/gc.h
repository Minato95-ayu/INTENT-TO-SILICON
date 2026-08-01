#ifndef AAYU_GC_H
#define AAYU_GC_H

#include "../vm.h"
#include "object.h"

// Gray stack structure for Iterative DFS Mark Phase
typedef struct {
    AayuObject** objects;
    uint32_t count;
    uint32_t capacity;
} GrayStack;

void aayu_gc_init(void);
void aayu_gc_destroy(void);

// Run a full GC cycle (Mark & Sweep)
void aayu_gc_collect(VM* vm);

#endif // AAYU_GC_H
