#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum { VAL_NUM, VAL_STR, VAL_BOOL, VAL_NULL, VAL_LIST, VAL_DICT } AayuType;
typedef struct AayuValue AayuValue;
struct AayuValue {
    AayuType type;
    union {
        double num;
        char* str;
        int boolean;
        struct { AayuValue* items; int count; int capacity; } list;
        struct { char** keys; AayuValue* values; int count; int capacity; } dict;
    } as;
};

AayuValue make_num(double n) { AayuValue v; v.type = VAL_NUM; v.as.num = n; return v; }
AayuValue make_bool(int b) { AayuValue v; v.type = VAL_BOOL; v.as.boolean = b; return v; }
AayuValue make_null() { AayuValue v; v.type = VAL_NULL; return v; }
AayuValue make_str(const char* s) {
    AayuValue v; v.type = VAL_STR;
    v.as.str = malloc(strlen(s) + 1);
    strcpy(v.as.str, s);
    return v;
}
AayuValue make_list() {
    AayuValue v; v.type = VAL_LIST;
    v.as.list.count = 0; v.as.list.capacity = 8;
    v.as.list.items = malloc(sizeof(AayuValue) * 8);
    return v;
}
AayuValue make_dict() {
    AayuValue v; v.type = VAL_DICT;
    v.as.dict.count = 0; v.as.dict.capacity = 8;
    v.as.dict.keys = malloc(sizeof(char*) * 8);
    v.as.dict.values = malloc(sizeof(AayuValue) * 8);
    return v;
}

void aayu_dict_set(AayuValue* dict, const char* key, AayuValue val) {
    if (dict->type != VAL_DICT) return;
    for(int i=0; i<dict->as.dict.count; i++) {
        if(strcmp(dict->as.dict.keys[i], key) == 0) { dict->as.dict.values[i] = val; return; }
    }
    if (dict->as.dict.count >= dict->as.dict.capacity) {
        dict->as.dict.capacity *= 2;
        dict->as.dict.keys = realloc(dict->as.dict.keys, sizeof(char*) * dict->as.dict.capacity);
        dict->as.dict.values = realloc(dict->as.dict.values, sizeof(AayuValue) * dict->as.dict.capacity);
    }
    dict->as.dict.keys[dict->as.dict.count] = malloc(strlen(key) + 1);
    strcpy(dict->as.dict.keys[dict->as.dict.count], key);
    dict->as.dict.values[dict->as.dict.count++] = val;
}

void aayu_print(AayuValue v) {
    if (v.type == VAL_NUM) printf("%g\n", v.as.num);
    else if (v.type == VAL_STR) printf("%s\n", v.as.str);
    else if (v.type == VAL_BOOL) printf("%s\n", v.as.boolean ? "true" : "false");
    else if (v.type == VAL_LIST) printf("[List size=%d]\n", v.as.list.count);
    else if (v.type == VAL_DICT) printf("{Dict size=%d}\n", v.as.dict.count);
    else printf("null\n");
}

void aayu_list_append(AayuValue* lst, AayuValue item) {
    if (lst->type != VAL_LIST) return;
    if (lst->as.list.count >= lst->as.list.capacity) {
        lst->as.list.capacity *= 2;
        lst->as.list.items = realloc(lst->as.list.items, sizeof(AayuValue) * lst->as.list.capacity);
    }
    lst->as.list.items[lst->as.list.count++] = item;
}

AayuValue aayu_add(AayuValue a, AayuValue b) {
    if (a.type == VAL_NUM && b.type == VAL_NUM) return make_num(a.as.num + b.as.num);
    if (a.type == VAL_STR && b.type == VAL_STR) {
        char* res = malloc(strlen(a.as.str) + strlen(b.as.str) + 1);
        strcpy(res, a.as.str); strcat(res, b.as.str);
        return make_str(res);
    }
    if (a.type == VAL_LIST && b.type == VAL_LIST) {
        AayuValue res = make_list();
        for(int i=0; i<a.as.list.count; i++) aayu_list_append(&res, a.as.list.items[i]);
        for(int i=0; i<b.as.list.count; i++) aayu_list_append(&res, b.as.list.items[i]);
        return res;
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
    if (a.type == VAL_STR && b.type == VAL_STR) return make_bool(strcmp(a.as.str, b.as.str) < 0);
    return make_bool(0);
}

AayuValue aayu_eq(AayuValue a, AayuValue b) {
    if (a.type == VAL_NUM && b.type == VAL_NUM) return make_bool(a.as.num == b.as.num);
    if (a.type == VAL_STR && b.type == VAL_STR) return make_bool(strcmp(a.as.str, b.as.str) == 0);
    if (a.type == VAL_BOOL && b.type == VAL_BOOL) return make_bool(a.as.boolean == b.as.boolean);
    if (a.type == VAL_NULL && b.type == VAL_NULL) return make_bool(1);
    return make_bool(0);
}

AayuValue aayu_greater_eq(AayuValue a, AayuValue b) {
    if (a.type == VAL_NUM && b.type == VAL_NUM) return make_bool(a.as.num >= b.as.num);
    if (a.type == VAL_STR && b.type == VAL_STR) return make_bool(strcmp(a.as.str, b.as.str) >= 0);
    return make_bool(0);
}

AayuValue aayu_less_eq(AayuValue a, AayuValue b) {
    if (a.type == VAL_NUM && b.type == VAL_NUM) return make_bool(a.as.num <= b.as.num);
    if (a.type == VAL_STR && b.type == VAL_STR) return make_bool(strcmp(a.as.str, b.as.str) <= 0);
    return make_bool(0);
}

AayuValue aayu_read_file(AayuValue path) {
    if (path.type != VAL_STR) return make_null();
    FILE* f = fopen(path.as.str, "rb");
    if (!f) return make_null();
    fseek(f, 0, SEEK_END); long fsize = ftell(f); fseek(f, 0, SEEK_SET);
    char* string = malloc(fsize + 1);
    fread(string, fsize, 1, f); fclose(f); string[fsize] = 0;
    return make_str(string);
}

AayuValue aayu_subscript(AayuValue target, AayuValue index) {
    if (target.type == VAL_DICT && index.type == VAL_STR) {
        for(int i=0; i<target.as.dict.count; i++) {
            if (strcmp(target.as.dict.keys[i], index.as.str) == 0) return target.as.dict.values[i];
        }
        return make_null();
    }
    if (index.type != VAL_NUM) return make_null();
    int idx = (int)index.as.num;
    if (target.type == VAL_LIST && idx >= 0 && idx < target.as.list.count) return target.as.list.items[idx];
    if (target.type == VAL_STR && idx >= 0 && idx < strlen(target.as.str)) {
        char c[2] = { target.as.str[idx], 0 };
        return make_str(c);
    }
    return make_null();
}

AayuValue aayu_len(AayuValue target) {
    if (target.type == VAL_LIST) return make_num(target.as.list.count);
    if (target.type == VAL_STR) return make_num(strlen(target.as.str));
    return make_num(0);
}


int main() {
    AayuValue _aayu_list1 = make_list();
    aayu_list_append(&_aayu_list1, make_str("A"));
    AayuValue _aayu_list2 = make_list();
    aayu_list_append(&_aayu_list2, make_str("B"));
    AayuValue _aayu_list3 = aayu_add(_aayu_list1, _aayu_list2);
    aayu_print(_aayu_list3);
    aayu_print(aayu_subscript(_aayu_list3, make_num(1)));
    return 0;
}
