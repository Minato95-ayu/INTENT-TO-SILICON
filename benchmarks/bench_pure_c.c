#include <stdio.h>
#include <stdint.h>
#include <windows.h>

int main() {
    int64_t n = 10000000LL;
    volatile int64_t stack[4096];
    int sp = 0;
    volatile int64_t locals[256] = {0};

    LARGE_INTEGER freq, start, end;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&start);

    // Sum 0..n-1
    locals[0] = 0; // sum
    locals[1] = 0; // i

    while (locals[1] < n) {
        locals[0] += locals[1];
        locals[1] += 1;
    }

    QueryPerformanceCounter(&end);
    double ns = ((double)(end.QuadPart - start.QuadPart) * 1000000000.0) / freq.QuadPart;

    printf("PURE_C_RESULT: %lld\n", (long long)locals[0]);
    printf("PURE_C_NS: %.0f\n", ns);
    printf("PURE_C_MS: %.2f ms\n", ns / 1000000.0);

    return 0;
}
