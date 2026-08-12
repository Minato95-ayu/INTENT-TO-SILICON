#include "runtime.h"

// GC Stubs
AAYU_EXPORT void aayu_gc_init(void) {
    // Stub
}

AAYU_EXPORT void aayu_gc_shutdown(void) {
    // Stub
}

AAYU_EXPORT void* aayu_gc_alloc(size_t size) {
    // Fallback to standard alloc for now
    return aayu_alloc(size);
}

AAYU_EXPORT void aayu_gc_collect(void) {
    // Stub
}
