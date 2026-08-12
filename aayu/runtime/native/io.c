#include "runtime.h"
#include <stdio.h>
#include <inttypes.h>

AAYU_EXPORT void aayu_print_i64(int64_t val) {
    printf("%" PRId64 "\n", val);
}

AAYU_EXPORT void aayu_print_f64(double val) {
    printf("%f\n", val);
}

AAYU_EXPORT void aayu_print_bool(bool val) {
    printf("%s\n", val ? "true" : "false");
}

AAYU_EXPORT void aayu_print_string(AayuString* val) {
    if (val && val->data) {
        printf("%.*s\n", (int)val->length, val->data);
    } else {
        printf("null\n");
    }
}
