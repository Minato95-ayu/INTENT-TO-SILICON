#include "aayu_runtime.h"
#include <stdio.h>
#include <stdlib.h>

void aayu_panic(const char* msg) {
    fprintf(stderr, "AAYU PANIC: %s\n", msg);
    exit(1);
}
