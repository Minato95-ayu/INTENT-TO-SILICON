#include "runtime.h"
#include <stdlib.h>
#include <string.h>

AAYU_EXPORT void* aayu_alloc(size_t size) {
    // Basic wrapper, could hook into GC later
    return malloc(size);
}

AAYU_EXPORT void aayu_free(void* ptr) {
    free(ptr);
}

AAYU_EXPORT void* aayu_realloc(void* ptr, size_t new_size) {
    return realloc(ptr, new_size);
}

AAYU_EXPORT void* aayu_memcpy(void* dest, const void* src, size_t n) {
    return memcpy(dest, src, n);
}

AAYU_EXPORT void* aayu_memmove(void* dest, const void* src, size_t n) {
    return memmove(dest, src, n);
}

AAYU_EXPORT void* aayu_memset(void* s, int c, size_t n) {
    return memset(s, c, n);
}
