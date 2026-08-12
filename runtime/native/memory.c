#include "aayu_runtime.h"
#include <stdlib.h>
#include <stdio.h>

void* aayu_alloc(size_t size) {
    void* ptr = malloc(size);
    if (!ptr) {
        aayu_panic("Out of memory");
    }
    return ptr;
}
