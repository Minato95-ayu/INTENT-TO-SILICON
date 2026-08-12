#include "runtime.h"

// Defined during compilation by build_runtime.py
#ifndef AAYU_BUILD_COMPILER
#define AAYU_BUILD_COMPILER "unknown"
#endif

#ifndef AAYU_BUILD_TIMESTAMP
#define AAYU_BUILD_TIMESTAMP "unknown"
#endif

#ifndef AAYU_TARGET_TRIPLE
#define AAYU_TARGET_TRIPLE "unknown"
#endif

AAYU_EXPORT int aayu_runtime_abi_major(void) {
    return AAYU_RUNTIME_ABI_MAJOR;
}

AAYU_EXPORT int aayu_runtime_abi_minor(void) {
    return AAYU_RUNTIME_ABI_MINOR;
}

AAYU_EXPORT int aayu_runtime_abi_patch(void) {
    return AAYU_RUNTIME_ABI_PATCH;
}

AAYU_EXPORT const char* aayu_runtime_version(void) {
    return AAYU_RUNTIME_VERSION;
}

AAYU_EXPORT const char* aayu_compiler_name(void) {
    return AAYU_BUILD_COMPILER;
}

AAYU_EXPORT const char* aayu_build_timestamp(void) {
    return AAYU_BUILD_TIMESTAMP;
}

AAYU_EXPORT const char* aayu_target_triple(void) {
    return AAYU_TARGET_TRIPLE;
}
