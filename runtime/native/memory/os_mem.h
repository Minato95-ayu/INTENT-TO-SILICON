#ifndef AAYU_MEMORY_OS_MEM_H
#define AAYU_MEMORY_OS_MEM_H

#include <stddef.h>

// Allocate `size` bytes of raw memory directly from the OS (page-aligned).
void* os_alloc_pages(size_t size);

// Free memory previously allocated by `os_alloc_pages`.
void os_free_pages(void* ptr, size_t size);

#endif // AAYU_MEMORY_OS_MEM_H
