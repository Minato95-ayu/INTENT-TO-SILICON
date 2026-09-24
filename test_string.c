#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum { VAL_NUM, VAL_STR, VAL_BOOL, VAL_NULL } AayuType;
typedef struct AayuValue {
    AayuType type;
    union {
        double num;
        char* str;
        int boolean;
    } as;
} AayuValue;

AayuValue make_num(double n) { AayuValue v; v.type = VAL_NUM; v.as.num = n; return v; }
AayuValue make_bool(int b) { AayuValue v; v.type = VAL_BOOL; v.as.boolean = b; return v; }
AayuValue make_str(const char* s) {
    AayuValue v; v.type = VAL_STR;
    v.as.str = malloc(strlen(s) + 1);
    strcpy(v.as.str, s);
    return v;
}

void aayu_print(AayuValue v) {
    if (v.type == VAL_NUM) printf("%g\n", v.as.num);
    else if (v.type == VAL_STR) printf("%s\n", v.as.str);
    else if (v.type == VAL_BOOL) printf("%s\n", v.as.boolean ? "true" : "false");
    else printf("null\n");
}

AayuValue aayu_add(AayuValue a, AayuValue b) {
    if (a.type == VAL_NUM && b.type == VAL_NUM) return make_num(a.as.num + b.as.num);
    if (a.type == VAL_STR && b.type == VAL_STR) {
        char* res = malloc(strlen(a.as.str) + strlen(b.as.str) + 1);
        strcpy(res, a.as.str); strcat(res, b.as.str);
        return make_str(res);
    }
    return make_num(0);
}

int aayu_is_truthy(AayuValue v) {
    if (v.type == VAL_NUM) return v.as.num != 0;
    if (v.type == VAL_BOOL) return v.as.boolean;
    if (v.type == VAL_STR) return strlen(v.as.str) > 0;
    return 0;
}

AayuValue aayu_less(AayuValue a, AayuValue b) {
    if (a.type == VAL_NUM && b.type == VAL_NUM) return make_bool(a.as.num < b.as.num);
    return make_bool(0);
}

int main() {
    AayuValue greeting = make_str("Hello from ");
    AayuValue name = make_str("Native AAYU C-Backend!");
    AayuValue full_message = aayu_add(greeting, name);
    aayu_print(full_message);
    AayuValue is_fast = make_bool(1);
    aayu_print(is_fast);
    AayuValue loops = make_num(0);
    while (aayu_is_truthy(aayu_less(loops, make_num(3)))) {
        aayu_print(make_str("Looping native string!"));
        loops = aayu_add(loops, make_num(1));
    }
    return 0;
}
