#include "runtime.h"
#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>

#ifdef _WIN32
#include <windows.h>
#else
#include <execinfo.h>
#endif

AAYU_EXPORT void aayu_panic(
    const char* module_name,
    const char* function_name,
    const char* file_name,
    int64_t line,
    int64_t column,
    const char* message
) {
    fprintf(stderr, "\n========================================\n");
    fprintf(stderr, "Runtime Panic\n");
    fprintf(stderr, "========================================\n\n");
    fprintf(stderr, "%s\n\n", message);
    
    fprintf(stderr, "File:\n%s\n\n", file_name);
    fprintf(stderr, "Function:\n%s()\n\n", function_name);
    fprintf(stderr, "Location:\n%" PRId64 ":%" PRId64 "\n\n", line, column);
    
    fprintf(stderr, "Stacktrace:\n");
    
#ifdef _WIN32
    void* stack[100];
    unsigned short frames = CaptureStackBackTrace(0, 100, stack, NULL);
    for (unsigned short i = 0; i < frames; i++) {
        fprintf(stderr, "[%d] %p\n", i, stack[i]);
    }
#else
    void* array[100];
    int size = backtrace(array, 100);
    char** strings = backtrace_symbols(array, size);
    if (strings != NULL) {
        for (int i = 0; i < size; i++) {
            fprintf(stderr, "%s\n", strings[i]);
        }
        free(strings);
    }
#endif
    
    fprintf(stderr, "\n========================================\n");
    
    // In a real runtime, we might unwind the stack gracefully or call abort()
    abort();
}
