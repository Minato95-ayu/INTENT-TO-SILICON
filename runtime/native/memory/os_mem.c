#include "os_mem.h"

#ifdef _WIN32
#include <windows.h>
#else
#include <sys/mman.h>
#endif

#include <stdlib.h>
#include <stdio.h>

void* os_alloc_pages(size_t size) {
#ifdef _WIN32
    void* ptr = VirtualAlloc(NULL, size, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (!ptr) {
        printf("Out of memory: VirtualAlloc failed.\n");
        exit(1);
    }
    return ptr;
#elif defined(__linux__) || defined(__APPLE__)
    void* ptr = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (ptr == MAP_FAILED) {
        printf("Out of memory: mmap failed.\n");
        exit(1);
    }
    return ptr;
#else
    void* ptr = malloc(size);
    if (!ptr) {
        printf("Out of memory: malloc failed.\n");
        exit(1);
    }
    return ptr;
#endif
}

void os_free_pages(void* ptr, size_t size) {
    if (!ptr) return;
#ifdef _WIN32
    VirtualFree(ptr, 0, MEM_RELEASE);
#elif defined(__linux__) || defined(__APPLE__)
    munmap(ptr, size);
#else
    free(ptr);
#endif
}
