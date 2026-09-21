#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    double i = 0;
    double sum = 0;
    while ((i < 5)) {
        sum = (sum + i);
        i = (i + 1);
    }
    printf("%f\n", (double)sum);
    return 0;
}
