#ifndef AAYU_RUNTIME_H
#define AAYU_RUNTIME_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#ifdef _WIN32
  #define AAYU_EXPORT __declspec(dllexport)
#else
  #define AAYU_EXPORT __attribute__((visibility("default")))
#endif

// ABI Semantic Versioning
#define AAYU_RUNTIME_ABI_MAJOR 1
#define AAYU_RUNTIME_ABI_MINOR 0
#define AAYU_RUNTIME_ABI_PATCH 0
#define AAYU_RUNTIME_VERSION "1.0.0"

// Metadata Exports
AAYU_EXPORT int aayu_runtime_abi_major(void);
AAYU_EXPORT int aayu_runtime_abi_minor(void);
AAYU_EXPORT int aayu_runtime_abi_patch(void);
AAYU_EXPORT const char* aayu_runtime_version(void);
AAYU_EXPORT const char* aayu_compiler_name(void);
AAYU_EXPORT const char* aayu_build_timestamp(void);
AAYU_EXPORT const char* aayu_target_triple(void);

// ---------------------------------------------------------
// Core Types
// ---------------------------------------------------------

typedef struct {
    int64_t length;
    int64_t capacity;
    char* data;
    uint32_t hash;
} AayuString;

typedef struct {
    int64_t length;
    int64_t capacity;
    int64_t element_size;
    void* data;
} AayuArray;

// ---------------------------------------------------------
// Memory ABI
// ---------------------------------------------------------
AAYU_EXPORT void* aayu_alloc(size_t size);
AAYU_EXPORT void  aayu_free(void* ptr);
AAYU_EXPORT void* aayu_realloc(void* ptr, size_t new_size);
AAYU_EXPORT void* aayu_memcpy(void* dest, const void* src, size_t n);
AAYU_EXPORT void* aayu_memmove(void* dest, const void* src, size_t n);
AAYU_EXPORT void* aayu_memset(void* s, int c, size_t n);

// ---------------------------------------------------------
// IO ABI
// ---------------------------------------------------------
AAYU_EXPORT void aayu_print_i64(int64_t val);
AAYU_EXPORT void aayu_print_f64(double val);
AAYU_EXPORT void aayu_print_bool(bool val);
AAYU_EXPORT void aayu_print_string(AayuString* val);

// ---------------------------------------------------------
// Panic ABI
// ---------------------------------------------------------
AAYU_EXPORT void aayu_panic(
    const char* module_name,
    const char* function_name,
    const char* file_name,
    int64_t line,
    int64_t column,
    const char* message
);

// ---------------------------------------------------------
// GC Stubs ABI
// ---------------------------------------------------------
AAYU_EXPORT void  aayu_gc_init(void);
AAYU_EXPORT void  aayu_gc_shutdown(void);
AAYU_EXPORT void* aayu_gc_alloc(size_t size);
AAYU_EXPORT void  aayu_gc_collect(void);

// ---------------------------------------------------------
// Network ABI
// ---------------------------------------------------------

typedef struct {
    int32_t success;
    int32_t latency_ms;
    char ip[64];
} AayuPingResult;

typedef struct {
    int32_t success;
    char ip[64];
} AayuDNSResult;

typedef struct {
    int32_t success;
    int32_t latency_ms;
} AayuTCPResult;

AAYU_EXPORT AayuPingResult aayu_ping(const char* host);
AAYU_EXPORT AayuDNSResult aayu_dns_resolve(const char* host);
AAYU_EXPORT AayuTCPResult aayu_tcp_connect(const char* host, int32_t port);

#endif // AAYU_RUNTIME_H
