#include <stdio.h>
#include <time.h>

int main() {
    // 1M additions (volatile to prevent optimization)
    clock_t start = clock();
    volatile long long total = 0;
    for (int i = 0; i < 1000000; i++) {
        total += 1;
    }
    clock_t end = clock();
    double ms1 = (double)(end - start) / CLOCKS_PER_SEC * 1000.0;
    printf("C 1M additions: %lld in %.2fms\n", (long long)total, ms1);

    // 10M additions
    start = clock();
    total = 0;
    for (int i = 0; i < 10000000; i++) {
        total += 1;
    }
    end = clock();
    double ms2 = (double)(end - start) / CLOCKS_PER_SEC * 1000.0;
    printf("C 10M additions: %lld in %.2fms\n", (long long)total, ms2);

    // 100M additions
    start = clock();
    total = 0;
    for (int i = 0; i < 100000000; i++) {
        total += 1;
    }
    end = clock();
    double ms3 = (double)(end - start) / CLOCKS_PER_SEC * 1000.0;
    printf("C 100M additions: %lld in %.2fms\n", (long long)total, ms3);

    return 0;
}
