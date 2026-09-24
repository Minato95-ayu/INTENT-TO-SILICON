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

AayuValue _aayu_fn_is_alpha(AayuValue _aayu_c);
AayuValue _aayu_fn_is_digit(AayuValue _aayu_c);
AayuValue _aayu_fn_is_alphanumeric(AayuValue _aayu_c);
AayuValue _aayu_fn_tokenize(AayuValue _aayu_src);
AayuValue _aayu_fn_main();

AayuValue _aayu_fn_is_alpha(AayuValue _aayu_c) {
    if (aayu_is_truthy(aayu_greater_eq(_aayu_c, make_str("a")))) {
        if (aayu_is_truthy(aayu_less_eq(_aayu_c, make_str("z")))) {
            return make_num(1);
        }
    }
    if (aayu_is_truthy(aayu_greater_eq(_aayu_c, make_str("A")))) {
        if (aayu_is_truthy(aayu_less_eq(_aayu_c, make_str("Z")))) {
            return make_num(1);
        }
    }
    if (aayu_is_truthy(aayu_eq(_aayu_c, make_str("_")))) {
        return make_num(1);
    }
    return make_num(0);
    return make_null();
}

AayuValue _aayu_fn_is_digit(AayuValue _aayu_c) {
    if (aayu_is_truthy(aayu_greater_eq(_aayu_c, make_str("0")))) {
        if (aayu_is_truthy(aayu_less_eq(_aayu_c, make_str("9")))) {
            return make_num(1);
        }
    }
    return make_num(0);
    return make_null();
}

AayuValue _aayu_fn_is_alphanumeric(AayuValue _aayu_c) {
    if (aayu_is_truthy(_aayu_fn_is_alpha(_aayu_c))) {
        return make_num(1);
    }
    if (aayu_is_truthy(_aayu_fn_is_digit(_aayu_c))) {
        return make_num(1);
    }
    return make_num(0);
    return make_null();
}

AayuValue _aayu_fn_tokenize(AayuValue _aayu_src) {
    AayuValue _aayu_tokens = make_list();
    AayuValue _aayu_pos = make_num(0);
    AayuValue _aayu_line = make_num(1);
    AayuValue _aayu_column = make_num(1);
    AayuValue _aayu_length = aayu_len(_aayu_src);
    AayuValue _aayu_loop = aayu_eq(make_num(1), make_num(1));
    while (aayu_is_truthy(_aayu_loop)) {
        AayuValue _aayu_start_line = make_num(0);
        AayuValue _aayu_start_col = make_num(0);
        AayuValue _aayu_value = make_str("");
        AayuValue _aayu_ws_loop = aayu_eq(make_num(1), make_num(1));
        while (aayu_is_truthy(_aayu_ws_loop)) {
            if (aayu_is_truthy(aayu_greater_eq(_aayu_pos, _aayu_length))) {
                _aayu_ws_loop = aayu_eq(make_num(1), make_num(0));
            }
            else {
                AayuValue _aayu_c = aayu_subscript(_aayu_src, _aayu_pos);
                if (aayu_is_truthy(aayu_eq(_aayu_c, make_str(" ")))) {
                    _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                    _aayu_column = aayu_add(_aayu_column, make_num(1));
                }
                else {
                    if (aayu_is_truthy(aayu_eq(_aayu_c, make_str("\r")))) {
                        _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                    }
                    else {
                        if (aayu_is_truthy(aayu_eq(_aayu_c, make_str("	")))) {
                            _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                            _aayu_column = aayu_add(_aayu_column, make_num(1));
                        }
                        else {
                            if (aayu_is_truthy(aayu_eq(_aayu_c, make_str("\n")))) {
                                _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                                _aayu_line = aayu_add(_aayu_line, make_num(1));
                                _aayu_column = make_num(1);
                            }
                            else {
                                _aayu_ws_loop = aayu_eq(make_num(1), make_num(0));
                            }
                        }
                    }
                }
            }
        }
        if (aayu_is_truthy(aayu_greater_eq(_aayu_pos, _aayu_length))) {
            _aayu_tokens = aayu_add(_aayu_tokens, ({ AayuValue _l = make_list(); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("EOF")); aayu_dict_set(&_d, "value", make_str("")); aayu_dict_set(&_d, "line", _aayu_line); aayu_dict_set(&_d, "column", _aayu_column); _d; })); _l; }));
            _aayu_loop = aayu_eq(make_num(1), make_num(0));
        }
        else {
            AayuValue _aayu_c = aayu_subscript(_aayu_src, _aayu_pos);
            if (aayu_is_truthy(_aayu_fn_is_alpha(_aayu_c))) {
                _aayu_start_line = _aayu_line;
                _aayu_start_col = _aayu_column;
                _aayu_value = make_str("");
                AayuValue _aayu_id_loop = aayu_eq(make_num(1), make_num(1));
                while (aayu_is_truthy(_aayu_id_loop)) {
                    if (aayu_is_truthy(aayu_greater_eq(_aayu_pos, _aayu_length))) {
                        _aayu_id_loop = aayu_eq(make_num(1), make_num(0));
                    }
                    else {
                        AayuValue _aayu_cur = aayu_subscript(_aayu_src, _aayu_pos);
                        if (aayu_is_truthy(_aayu_fn_is_alphanumeric(_aayu_cur))) {
                            _aayu_value = aayu_add(_aayu_value, _aayu_cur);
                            _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                            _aayu_column = aayu_add(_aayu_column, make_num(1));
                        }
                        else {
                            _aayu_id_loop = aayu_eq(make_num(1), make_num(0));
                        }
                    }
                }
                AayuValue _aayu_tok_type = make_str("IDENTIFIER");
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("run")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("theme")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("page")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("state")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("await")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("navigate")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("while")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("return")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("throw")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("if")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("try")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("respond")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("rethrow")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("animate")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("for")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("task")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("insert")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("catch")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("post")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("else")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("let")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("print")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("model")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("action")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("extern")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("import")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("app")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("widget")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("fn")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("end")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("component")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("server")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("elif")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("useTheme")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("bind")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("get")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("as")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("in")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("event")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("finally")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("find")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("validate")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                if (aayu_is_truthy(aayu_eq(_aayu_value, make_str("route")))) {
                    _aayu_tok_type = make_str("KEYWORD");
                }
                _aayu_tokens = aayu_add(_aayu_tokens, ({ AayuValue _l = make_list(); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", _aayu_tok_type); aayu_dict_set(&_d, "value", _aayu_value); aayu_dict_set(&_d, "line", _aayu_start_line); aayu_dict_set(&_d, "column", _aayu_start_col); _d; })); _l; }));
            }
            else {
                if (aayu_is_truthy(_aayu_fn_is_digit(_aayu_c))) {
                    _aayu_start_line = _aayu_line;
                    _aayu_start_col = _aayu_column;
                    _aayu_value = make_str("");
                    AayuValue _aayu_num_loop = aayu_eq(make_num(1), make_num(1));
                    while (aayu_is_truthy(_aayu_num_loop)) {
                        if (aayu_is_truthy(aayu_greater_eq(_aayu_pos, _aayu_length))) {
                            _aayu_num_loop = aayu_eq(make_num(1), make_num(0));
                        }
                        else {
                            AayuValue _aayu_cur = aayu_subscript(_aayu_src, _aayu_pos);
                            if (aayu_is_truthy(_aayu_fn_is_digit(_aayu_cur))) {
                                _aayu_value = aayu_add(_aayu_value, _aayu_cur);
                                _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                                _aayu_column = aayu_add(_aayu_column, make_num(1));
                            }
                            else {
                                if (aayu_is_truthy(aayu_eq(_aayu_cur, make_str(".")))) {
                                    _aayu_value = aayu_add(_aayu_value, _aayu_cur);
                                    _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                                    _aayu_column = aayu_add(_aayu_column, make_num(1));
                                }
                                else {
                                    _aayu_num_loop = aayu_eq(make_num(1), make_num(0));
                                }
                            }
                        }
                    }
                    _aayu_tokens = aayu_add(_aayu_tokens, ({ AayuValue _l = make_list(); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("NUMBER")); aayu_dict_set(&_d, "value", _aayu_value); aayu_dict_set(&_d, "line", _aayu_start_line); aayu_dict_set(&_d, "column", _aayu_start_col); _d; })); _l; }));
                }
                else {
                    if (aayu_is_truthy(aayu_eq(_aayu_c, make_str("\"")))) {
                        _aayu_start_line = _aayu_line;
                        _aayu_start_col = _aayu_column;
                        _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                        _aayu_column = aayu_add(_aayu_column, make_num(1));
                        _aayu_value = make_str("");
                        AayuValue _aayu_str_loop = aayu_eq(make_num(1), make_num(1));
                        while (aayu_is_truthy(_aayu_str_loop)) {
                            if (aayu_is_truthy(aayu_greater_eq(_aayu_pos, _aayu_length))) {
                                _aayu_str_loop = aayu_eq(make_num(1), make_num(0));
                            }
                            else {
                                AayuValue _aayu_cur = aayu_subscript(_aayu_src, _aayu_pos);
                                if (aayu_is_truthy(aayu_eq(_aayu_cur, make_str("\"")))) {
                                    _aayu_str_loop = aayu_eq(make_num(1), make_num(0));
                                }
                                else {
                                    _aayu_value = aayu_add(_aayu_value, _aayu_cur);
                                    _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                                    _aayu_column = aayu_add(_aayu_column, make_num(1));
                                }
                            }
                        }
                        if (aayu_is_truthy(aayu_less(_aayu_pos, _aayu_length))) {
                            _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                            _aayu_column = aayu_add(_aayu_column, make_num(1));
                        }
                        _aayu_tokens = aayu_add(_aayu_tokens, ({ AayuValue _l = make_list(); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("STRING")); aayu_dict_set(&_d, "value", _aayu_value); aayu_dict_set(&_d, "line", _aayu_start_line); aayu_dict_set(&_d, "column", _aayu_start_col); _d; })); _l; }));
                    }
                    else {
                        _aayu_start_line = _aayu_line;
                        _aayu_start_col = _aayu_column;
                        AayuValue _aayu_punct = _aayu_c;
                        _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                        _aayu_column = aayu_add(_aayu_column, make_num(1));
                        if (aayu_is_truthy(aayu_less(_aayu_pos, _aayu_length))) {
                            AayuValue _aayu_next_c = aayu_subscript(_aayu_src, _aayu_pos);
                            AayuValue _aayu_is_double = aayu_eq(make_num(1), make_num(0));
                            if (aayu_is_truthy(aayu_eq(_aayu_c, make_str("=")))) {
                                if (aayu_is_truthy(aayu_eq(_aayu_next_c, make_str("=")))) {
                                    _aayu_is_double = aayu_eq(make_num(1), make_num(1));
                                }
                            }
                            if (aayu_is_truthy(aayu_eq(_aayu_c, make_str("!")))) {
                                if (aayu_is_truthy(aayu_eq(_aayu_next_c, make_str("=")))) {
                                    _aayu_is_double = aayu_eq(make_num(1), make_num(1));
                                }
                            }
                            if (aayu_is_truthy(aayu_eq(_aayu_c, make_str(">")))) {
                                if (aayu_is_truthy(aayu_eq(_aayu_next_c, make_str("=")))) {
                                    _aayu_is_double = aayu_eq(make_num(1), make_num(1));
                                }
                            }
                            if (aayu_is_truthy(aayu_eq(_aayu_c, make_str("<")))) {
                                if (aayu_is_truthy(aayu_eq(_aayu_next_c, make_str("=")))) {
                                    _aayu_is_double = aayu_eq(make_num(1), make_num(1));
                                }
                            }
                            if (aayu_is_truthy(aayu_eq(_aayu_c, make_str("+")))) {
                                if (aayu_is_truthy(aayu_eq(_aayu_next_c, make_str("=")))) {
                                    _aayu_is_double = aayu_eq(make_num(1), make_num(1));
                                }
                            }
                            if (aayu_is_truthy(aayu_eq(_aayu_c, make_str("-")))) {
                                if (aayu_is_truthy(aayu_eq(_aayu_next_c, make_str("=")))) {
                                    _aayu_is_double = aayu_eq(make_num(1), make_num(1));
                                }
                            }
                            if (aayu_is_truthy(aayu_eq(_aayu_c, make_str("&")))) {
                                if (aayu_is_truthy(aayu_eq(_aayu_next_c, make_str("&")))) {
                                    _aayu_is_double = aayu_eq(make_num(1), make_num(1));
                                }
                            }
                            if (aayu_is_truthy(aayu_eq(_aayu_c, make_str("|")))) {
                                if (aayu_is_truthy(aayu_eq(_aayu_next_c, make_str("|")))) {
                                    _aayu_is_double = aayu_eq(make_num(1), make_num(1));
                                }
                            }
                            if (aayu_is_truthy(aayu_eq(_aayu_c, make_str(":")))) {
                                if (aayu_is_truthy(aayu_eq(_aayu_next_c, make_str(":")))) {
                                    _aayu_is_double = aayu_eq(make_num(1), make_num(1));
                                }
                            }
                            if (aayu_is_truthy(_aayu_is_double)) {
                                _aayu_punct = aayu_add(_aayu_c, _aayu_next_c);
                                _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                                _aayu_column = aayu_add(_aayu_column, make_num(1));
                            }
                        }
                        _aayu_tokens = aayu_add(_aayu_tokens, ({ AayuValue _l = make_list(); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("PUNCTUATION")); aayu_dict_set(&_d, "value", _aayu_punct); aayu_dict_set(&_d, "line", _aayu_start_line); aayu_dict_set(&_d, "column", _aayu_start_col); _d; })); _l; }));
                    }
                }
            }
        }
    }
    return _aayu_tokens;
    return make_null();
}

AayuValue _aayu_fn_main(void) {
    AayuValue _aayu_src = make_str("let x = 10");
    aayu_print(make_str("Lexing Native Code:"));
    aayu_print(_aayu_src);
    AayuValue _aayu_tokens = _aayu_fn_tokenize(_aayu_src);
    AayuValue _aayu_length = aayu_len(_aayu_tokens);
    aayu_print(make_str("Tokens found:"));
    aayu_print(_aayu_length);
    AayuValue _aayu_i = make_num(0);
    while (aayu_is_truthy(aayu_less(_aayu_i, _aayu_length))) {
        AayuValue _aayu_t = aayu_subscript(_aayu_tokens, _aayu_i);
        aayu_print(aayu_subscript(_aayu_t, make_str("type")));
        aayu_print(aayu_subscript(_aayu_t, make_str("value")));
        _aayu_i = aayu_add(_aayu_i, make_num(1));
    }
    return make_null();
}

int main() {
    _aayu_fn_main();
    return 0;
}
