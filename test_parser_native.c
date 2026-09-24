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
AayuValue _aayu_fn_match(AayuValue _aayu_tokens, AayuValue _aayu_pos, AayuValue _aayu_type, AayuValue _aayu_mat_value);
AayuValue _aayu_fn_check(AayuValue _aayu_tokens, AayuValue _aayu_pos, AayuValue _aayu_type);
AayuValue _aayu_fn_expect(AayuValue _aayu_tokens, AayuValue _aayu_pos, AayuValue _aayu_type, AayuValue _aayu_msg);
AayuValue _aayu_fn_expect_val(AayuValue _aayu_tokens, AayuValue _aayu_pos, AayuValue _aayu_type, AayuValue _aayu_expv_value, AayuValue _aayu_msg);
AayuValue _aayu_fn_make_program(AayuValue _aayu_stmts);
AayuValue _aayu_fn_make_let(AayuValue _aayu_name, AayuValue _aayu_value, AayuValue _aayu_line, AayuValue _aayu_column);
AayuValue _aayu_fn_make_assignment(AayuValue _aayu_target, AayuValue _aayu_value, AayuValue _aayu_line, AayuValue _aayu_column);
AayuValue _aayu_fn_make_if(AayuValue _aayu_cond, AayuValue _aayu_then_b, AayuValue _aayu_else_b, AayuValue _aayu_line, AayuValue _aayu_column);
AayuValue _aayu_fn_make_while(AayuValue _aayu_cond, AayuValue _aayu_body, AayuValue _aayu_line, AayuValue _aayu_column);
AayuValue _aayu_fn_make_action(AayuValue _aayu_name, AayuValue _aayu_args, AayuValue _aayu_stmts, AayuValue _aayu_line, AayuValue _aayu_column);
AayuValue _aayu_fn_make_return(AayuValue _aayu_value, AayuValue _aayu_line, AayuValue _aayu_column);
AayuValue _aayu_fn_make_binary(AayuValue _aayu_left, AayuValue _aayu_op, AayuValue _aayu_right, AayuValue _aayu_line, AayuValue _aayu_column);
AayuValue _aayu_fn_make_call(AayuValue _aayu_name, AayuValue _aayu_args, AayuValue _aayu_line, AayuValue _aayu_column);
AayuValue _aayu_fn_make_subscript(AayuValue _aayu_target, AayuValue _aayu_index, AayuValue _aayu_line, AayuValue _aayu_column);
AayuValue _aayu_fn_make_array(AayuValue _aayu_elements, AayuValue _aayu_line, AayuValue _aayu_column);
AayuValue _aayu_fn_make_dict(AayuValue _aayu_dkeys, AayuValue _aayu_dvals, AayuValue _aayu_line, AayuValue _aayu_column);
AayuValue _aayu_fn_make_literal(AayuValue _aayu_value, AayuValue _aayu_line, AayuValue _aayu_column);
AayuValue _aayu_fn_make_identifier(AayuValue _aayu_name, AayuValue _aayu_line, AayuValue _aayu_column);
AayuValue _aayu_fn_parse_expression(AayuValue _aayu_tokens, AayuValue _aayu_pos);
AayuValue _aayu_fn_parse_equality(AayuValue _aayu_tokens, AayuValue _aayu_pos);
AayuValue _aayu_fn_parse_comparison(AayuValue _aayu_tokens, AayuValue _aayu_pos);
AayuValue _aayu_fn_parse_term(AayuValue _aayu_tokens, AayuValue _aayu_pos);
AayuValue _aayu_fn_parse_factor(AayuValue _aayu_tokens, AayuValue _aayu_pos);
AayuValue _aayu_fn_parse_primary(AayuValue _aayu_tokens, AayuValue _aayu_pos);
AayuValue _aayu_fn_parse_statement(AayuValue _aayu_tokens, AayuValue _aayu_pos);
AayuValue _aayu_fn_parse_action_decl(AayuValue _aayu_tokens, AayuValue _aayu_pos);
AayuValue _aayu_fn_parse(AayuValue _aayu_tokens);
AayuValue _aayu_fn_print_ast(AayuValue _aayu_ast);
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

AayuValue _aayu_fn_match(AayuValue _aayu_tokens, AayuValue _aayu_pos, AayuValue _aayu_type, AayuValue _aayu_mat_value) {
    if (aayu_is_truthy(aayu_less(_aayu_pos, aayu_len(_aayu_tokens)))) {
        AayuValue _aayu_mat_t = aayu_subscript(_aayu_tokens, _aayu_pos);
        if (aayu_is_truthy(aayu_eq(aayu_subscript(_aayu_mat_t, make_str("type")), _aayu_type))) {
            if (aayu_is_truthy(aayu_eq(_aayu_mat_value, make_str("")))) {
                return aayu_eq(make_num(1), make_num(1));
            }
            else {
                if (aayu_is_truthy(aayu_eq(aayu_subscript(_aayu_mat_t, make_str("value")), _aayu_mat_value))) {
                    return aayu_eq(make_num(1), make_num(1));
                }
            }
        }
    }
    return aayu_eq(make_num(1), make_num(0));
    return make_null();
}

AayuValue _aayu_fn_check(AayuValue _aayu_tokens, AayuValue _aayu_pos, AayuValue _aayu_type) {
    if (aayu_is_truthy(aayu_less(_aayu_pos, aayu_len(_aayu_tokens)))) {
        AayuValue _aayu_chk_t = aayu_subscript(_aayu_tokens, _aayu_pos);
        if (aayu_is_truthy(aayu_eq(aayu_subscript(_aayu_chk_t, make_str("type")), _aayu_type))) {
            return aayu_eq(make_num(1), make_num(1));
        }
    }
    return aayu_eq(make_num(1), make_num(0));
    return make_null();
}

AayuValue _aayu_fn_expect(AayuValue _aayu_tokens, AayuValue _aayu_pos, AayuValue _aayu_type, AayuValue _aayu_msg) {
    if (aayu_is_truthy(aayu_less(_aayu_pos, aayu_len(_aayu_tokens)))) {
        AayuValue _aayu_exp_t = aayu_subscript(_aayu_tokens, _aayu_pos);
        if (aayu_is_truthy(aayu_eq(aayu_subscript(_aayu_exp_t, make_str("type")), _aayu_type))) {
            return ({ AayuValue _l = make_list(); aayu_list_append(&_l, aayu_add(_aayu_pos, make_num(1))); aayu_list_append(&_l, _aayu_exp_t); _l; });
        }
    }
    aayu_print(aayu_add(make_str("Syntax Error: "), _aayu_msg));
    return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("EOF")); aayu_dict_set(&_d, "value", make_str("")); aayu_dict_set(&_d, "line", make_num(0)); aayu_dict_set(&_d, "column", make_num(0)); _d; })); _l; });
    return make_null();
}

AayuValue _aayu_fn_expect_val(AayuValue _aayu_tokens, AayuValue _aayu_pos, AayuValue _aayu_type, AayuValue _aayu_expv_value, AayuValue _aayu_msg) {
    if (aayu_is_truthy(aayu_less(_aayu_pos, aayu_len(_aayu_tokens)))) {
        AayuValue _aayu_expv_t = aayu_subscript(_aayu_tokens, _aayu_pos);
        if (aayu_is_truthy(aayu_eq(aayu_subscript(_aayu_expv_t, make_str("type")), _aayu_type))) {
            if (aayu_is_truthy(aayu_eq(aayu_subscript(_aayu_expv_t, make_str("value")), _aayu_expv_value))) {
                return ({ AayuValue _l = make_list(); aayu_list_append(&_l, aayu_add(_aayu_pos, make_num(1))); aayu_list_append(&_l, _aayu_expv_t); _l; });
            }
        }
    }
    aayu_print(aayu_add(make_str("Syntax Error: "), _aayu_msg));
    return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("EOF")); aayu_dict_set(&_d, "value", make_str("")); aayu_dict_set(&_d, "line", make_num(0)); aayu_dict_set(&_d, "column", make_num(0)); _d; })); _l; });
    return make_null();
}

AayuValue _aayu_fn_make_program(AayuValue _aayu_stmts) {
    return ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("Program")); aayu_dict_set(&_d, "statements", _aayu_stmts); _d; });
    return make_null();
}

AayuValue _aayu_fn_make_let(AayuValue _aayu_name, AayuValue _aayu_value, AayuValue _aayu_line, AayuValue _aayu_column) {
    return ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("LetDeclaration")); aayu_dict_set(&_d, "name", _aayu_name); aayu_dict_set(&_d, "value", _aayu_value); aayu_dict_set(&_d, "line", _aayu_line); aayu_dict_set(&_d, "column", _aayu_column); _d; });
    return make_null();
}

AayuValue _aayu_fn_make_assignment(AayuValue _aayu_target, AayuValue _aayu_value, AayuValue _aayu_line, AayuValue _aayu_column) {
    return ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("Assignment")); aayu_dict_set(&_d, "target", _aayu_target); aayu_dict_set(&_d, "value", _aayu_value); aayu_dict_set(&_d, "line", _aayu_line); aayu_dict_set(&_d, "column", _aayu_column); _d; });
    return make_null();
}

AayuValue _aayu_fn_make_if(AayuValue _aayu_cond, AayuValue _aayu_then_b, AayuValue _aayu_else_b, AayuValue _aayu_line, AayuValue _aayu_column) {
    return ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("If")); aayu_dict_set(&_d, "condition", _aayu_cond); aayu_dict_set(&_d, "then_branch", _aayu_then_b); aayu_dict_set(&_d, "else_branch", _aayu_else_b); aayu_dict_set(&_d, "line", _aayu_line); aayu_dict_set(&_d, "column", _aayu_column); _d; });
    return make_null();
}

AayuValue _aayu_fn_make_while(AayuValue _aayu_cond, AayuValue _aayu_body, AayuValue _aayu_line, AayuValue _aayu_column) {
    return ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("While")); aayu_dict_set(&_d, "condition", _aayu_cond); aayu_dict_set(&_d, "body", _aayu_body); aayu_dict_set(&_d, "line", _aayu_line); aayu_dict_set(&_d, "column", _aayu_column); _d; });
    return make_null();
}

AayuValue _aayu_fn_make_action(AayuValue _aayu_name, AayuValue _aayu_args, AayuValue _aayu_stmts, AayuValue _aayu_line, AayuValue _aayu_column) {
    return ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("ActionDeclaration")); aayu_dict_set(&_d, "name", _aayu_name); aayu_dict_set(&_d, "args", _aayu_args); aayu_dict_set(&_d, "statements", _aayu_stmts); aayu_dict_set(&_d, "line", _aayu_line); aayu_dict_set(&_d, "column", _aayu_column); _d; });
    return make_null();
}

AayuValue _aayu_fn_make_return(AayuValue _aayu_value, AayuValue _aayu_line, AayuValue _aayu_column) {
    return ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("Return")); aayu_dict_set(&_d, "value", _aayu_value); aayu_dict_set(&_d, "line", _aayu_line); aayu_dict_set(&_d, "column", _aayu_column); _d; });
    return make_null();
}

AayuValue _aayu_fn_make_binary(AayuValue _aayu_left, AayuValue _aayu_op, AayuValue _aayu_right, AayuValue _aayu_line, AayuValue _aayu_column) {
    return ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("BinaryOp")); aayu_dict_set(&_d, "left", _aayu_left); aayu_dict_set(&_d, "operator", _aayu_op); aayu_dict_set(&_d, "right", _aayu_right); aayu_dict_set(&_d, "line", _aayu_line); aayu_dict_set(&_d, "column", _aayu_column); _d; });
    return make_null();
}

AayuValue _aayu_fn_make_call(AayuValue _aayu_name, AayuValue _aayu_args, AayuValue _aayu_line, AayuValue _aayu_column) {
    AayuValue _aayu_final_name = _aayu_name;
    if (aayu_is_truthy(aayu_eq(aayu_subscript(_aayu_name, make_str("type")), make_str("Identifier")))) {
        _aayu_final_name = aayu_subscript(_aayu_name, make_str("name"));
    }
    return ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("ActionCall")); aayu_dict_set(&_d, "name", _aayu_final_name); aayu_dict_set(&_d, "args", _aayu_args); aayu_dict_set(&_d, "line", _aayu_line); aayu_dict_set(&_d, "column", _aayu_column); _d; });
    return make_null();
}

AayuValue _aayu_fn_make_subscript(AayuValue _aayu_target, AayuValue _aayu_index, AayuValue _aayu_line, AayuValue _aayu_column) {
    return ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("Subscript")); aayu_dict_set(&_d, "target", _aayu_target); aayu_dict_set(&_d, "index", _aayu_index); aayu_dict_set(&_d, "line", _aayu_line); aayu_dict_set(&_d, "column", _aayu_column); _d; });
    return make_null();
}

AayuValue _aayu_fn_make_array(AayuValue _aayu_elements, AayuValue _aayu_line, AayuValue _aayu_column) {
    return ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("Array")); aayu_dict_set(&_d, "elements", _aayu_elements); aayu_dict_set(&_d, "line", _aayu_line); aayu_dict_set(&_d, "column", _aayu_column); _d; });
    return make_null();
}

AayuValue _aayu_fn_make_dict(AayuValue _aayu_dkeys, AayuValue _aayu_dvals, AayuValue _aayu_line, AayuValue _aayu_column) {
    return ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("Dictionary")); aayu_dict_set(&_d, "keys", _aayu_dkeys); aayu_dict_set(&_d, "values", _aayu_dvals); aayu_dict_set(&_d, "line", _aayu_line); aayu_dict_set(&_d, "column", _aayu_column); _d; });
    return make_null();
}

AayuValue _aayu_fn_make_literal(AayuValue _aayu_value, AayuValue _aayu_line, AayuValue _aayu_column) {
    return ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("Literal")); aayu_dict_set(&_d, "value", _aayu_value); aayu_dict_set(&_d, "line", _aayu_line); aayu_dict_set(&_d, "column", _aayu_column); _d; });
    return make_null();
}

AayuValue _aayu_fn_make_identifier(AayuValue _aayu_name, AayuValue _aayu_line, AayuValue _aayu_column) {
    return ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("Identifier")); aayu_dict_set(&_d, "name", _aayu_name); aayu_dict_set(&_d, "line", _aayu_line); aayu_dict_set(&_d, "column", _aayu_column); _d; });
    return make_null();
}

AayuValue _aayu_fn_parse_expression(AayuValue _aayu_tokens, AayuValue _aayu_pos) {
    return _aayu_fn_parse_equality(_aayu_tokens, _aayu_pos);
    return make_null();
}

AayuValue _aayu_fn_parse_equality(AayuValue _aayu_tokens, AayuValue _aayu_pos) {
    AayuValue _aayu_eq_res = _aayu_fn_parse_comparison(_aayu_tokens, _aayu_pos);
    _aayu_pos = aayu_subscript(_aayu_eq_res, make_num(0));
    AayuValue _aayu_eq_expr = aayu_subscript(_aayu_eq_res, make_num(1));
    AayuValue _aayu_eq_loop = aayu_eq(make_num(1), make_num(1));
    AayuValue _aayu_eq_op_tok = make_list();
    while (aayu_is_truthy(_aayu_eq_loop)) {
        _aayu_eq_op_tok = aayu_subscript(_aayu_tokens, _aayu_pos);
        if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("==")))) {
            _aayu_pos = aayu_add(_aayu_pos, make_num(1));
            _aayu_eq_res = _aayu_fn_parse_comparison(_aayu_tokens, _aayu_pos);
            _aayu_pos = aayu_subscript(_aayu_eq_res, make_num(0));
            _aayu_eq_expr = _aayu_fn_make_binary(_aayu_eq_expr, make_str("=="), aayu_subscript(_aayu_eq_res, make_num(1)), aayu_subscript(_aayu_eq_op_tok, make_str("line")), aayu_subscript(_aayu_eq_op_tok, make_str("column")));
        }
        else {
            if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("!=")))) {
                _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                _aayu_eq_res = _aayu_fn_parse_comparison(_aayu_tokens, _aayu_pos);
                _aayu_pos = aayu_subscript(_aayu_eq_res, make_num(0));
                _aayu_eq_expr = _aayu_fn_make_binary(_aayu_eq_expr, make_str("!="), aayu_subscript(_aayu_eq_res, make_num(1)), aayu_subscript(_aayu_eq_op_tok, make_str("line")), aayu_subscript(_aayu_eq_op_tok, make_str("column")));
            }
            else {
                _aayu_eq_loop = aayu_eq(make_num(1), make_num(0));
            }
        }
    }
    return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_eq_expr); _l; });
    return make_null();
}

AayuValue _aayu_fn_parse_comparison(AayuValue _aayu_tokens, AayuValue _aayu_pos) {
    AayuValue _aayu_comp_res = _aayu_fn_parse_term(_aayu_tokens, _aayu_pos);
    _aayu_pos = aayu_subscript(_aayu_comp_res, make_num(0));
    AayuValue _aayu_comp_expr = aayu_subscript(_aayu_comp_res, make_num(1));
    AayuValue _aayu_comp_loop = aayu_eq(make_num(1), make_num(1));
    AayuValue _aayu_comp_is_comp = aayu_eq(make_num(1), make_num(0));
    AayuValue _aayu_comp_op = make_str("");
    AayuValue _aayu_comp_op_tok = make_list();
    while (aayu_is_truthy(_aayu_comp_loop)) {
        _aayu_comp_is_comp = aayu_eq(make_num(1), make_num(0));
        _aayu_comp_op = make_str("");
        _aayu_comp_op_tok = aayu_subscript(_aayu_tokens, _aayu_pos);
        if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("<")))) {
            _aayu_comp_is_comp = aayu_eq(make_num(1), make_num(1));
            _aayu_comp_op = make_str("<");
        }
        if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str(">")))) {
            _aayu_comp_is_comp = aayu_eq(make_num(1), make_num(1));
            _aayu_comp_op = make_str(">");
        }
        if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("<=")))) {
            _aayu_comp_is_comp = aayu_eq(make_num(1), make_num(1));
            _aayu_comp_op = make_str("<=");
        }
        if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str(">=")))) {
            _aayu_comp_is_comp = aayu_eq(make_num(1), make_num(1));
            _aayu_comp_op = make_str(">=");
        }
        if (aayu_is_truthy(_aayu_comp_is_comp)) {
            _aayu_pos = aayu_add(_aayu_pos, make_num(1));
            _aayu_comp_res = _aayu_fn_parse_term(_aayu_tokens, _aayu_pos);
            _aayu_pos = aayu_subscript(_aayu_comp_res, make_num(0));
            _aayu_comp_expr = _aayu_fn_make_binary(_aayu_comp_expr, _aayu_comp_op, aayu_subscript(_aayu_comp_res, make_num(1)), aayu_subscript(_aayu_comp_op_tok, make_str("line")), aayu_subscript(_aayu_comp_op_tok, make_str("column")));
        }
        else {
            _aayu_comp_loop = aayu_eq(make_num(1), make_num(0));
        }
    }
    return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_comp_expr); _l; });
    return make_null();
}

AayuValue _aayu_fn_parse_term(AayuValue _aayu_tokens, AayuValue _aayu_pos) {
    AayuValue _aayu_term_res = _aayu_fn_parse_factor(_aayu_tokens, _aayu_pos);
    _aayu_pos = aayu_subscript(_aayu_term_res, make_num(0));
    AayuValue _aayu_term_expr = aayu_subscript(_aayu_term_res, make_num(1));
    AayuValue _aayu_term_loop = aayu_eq(make_num(1), make_num(1));
    AayuValue _aayu_term_is_term = aayu_eq(make_num(1), make_num(0));
    AayuValue _aayu_term_op = make_str("");
    AayuValue _aayu_term_op_tok = make_list();
    while (aayu_is_truthy(_aayu_term_loop)) {
        _aayu_term_is_term = aayu_eq(make_num(1), make_num(0));
        _aayu_term_op = make_str("");
        _aayu_term_op_tok = aayu_subscript(_aayu_tokens, _aayu_pos);
        if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("+")))) {
            _aayu_term_is_term = aayu_eq(make_num(1), make_num(1));
            _aayu_term_op = make_str("+");
        }
        if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("-")))) {
            _aayu_term_is_term = aayu_eq(make_num(1), make_num(1));
            _aayu_term_op = make_str("-");
        }
        if (aayu_is_truthy(_aayu_term_is_term)) {
            _aayu_pos = aayu_add(_aayu_pos, make_num(1));
            _aayu_term_res = _aayu_fn_parse_factor(_aayu_tokens, _aayu_pos);
            _aayu_pos = aayu_subscript(_aayu_term_res, make_num(0));
            _aayu_term_expr = _aayu_fn_make_binary(_aayu_term_expr, _aayu_term_op, aayu_subscript(_aayu_term_res, make_num(1)), aayu_subscript(_aayu_term_op_tok, make_str("line")), aayu_subscript(_aayu_term_op_tok, make_str("column")));
        }
        else {
            _aayu_term_loop = aayu_eq(make_num(1), make_num(0));
        }
    }
    return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_term_expr); _l; });
    return make_null();
}

AayuValue _aayu_fn_parse_factor(AayuValue _aayu_tokens, AayuValue _aayu_pos) {
    AayuValue _aayu_fact_res = _aayu_fn_parse_primary(_aayu_tokens, _aayu_pos);
    _aayu_pos = aayu_subscript(_aayu_fact_res, make_num(0));
    AayuValue _aayu_fact_expr = aayu_subscript(_aayu_fact_res, make_num(1));
    AayuValue _aayu_fact_loop = aayu_eq(make_num(1), make_num(1));
    AayuValue _aayu_fact_is_fact = aayu_eq(make_num(1), make_num(0));
    AayuValue _aayu_fact_op = make_str("");
    AayuValue _aayu_fact_op_tok = make_list();
    while (aayu_is_truthy(_aayu_fact_loop)) {
        _aayu_fact_is_fact = aayu_eq(make_num(1), make_num(0));
        _aayu_fact_op = make_str("");
        _aayu_fact_op_tok = aayu_subscript(_aayu_tokens, _aayu_pos);
        if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("*")))) {
            _aayu_fact_is_fact = aayu_eq(make_num(1), make_num(1));
            _aayu_fact_op = make_str("*");
        }
        if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("/")))) {
            _aayu_fact_is_fact = aayu_eq(make_num(1), make_num(1));
            _aayu_fact_op = make_str("/");
        }
        if (aayu_is_truthy(_aayu_fact_is_fact)) {
            _aayu_pos = aayu_add(_aayu_pos, make_num(1));
            _aayu_fact_res = _aayu_fn_parse_primary(_aayu_tokens, _aayu_pos);
            _aayu_pos = aayu_subscript(_aayu_fact_res, make_num(0));
            _aayu_fact_expr = _aayu_fn_make_binary(_aayu_fact_expr, _aayu_fact_op, aayu_subscript(_aayu_fact_res, make_num(1)), aayu_subscript(_aayu_fact_op_tok, make_str("line")), aayu_subscript(_aayu_fact_op_tok, make_str("column")));
        }
        else {
            _aayu_fact_loop = aayu_eq(make_num(1), make_num(0));
        }
    }
    return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_fact_expr); _l; });
    return make_null();
}

AayuValue _aayu_fn_parse_primary(AayuValue _aayu_tokens, AayuValue _aayu_pos) {
    AayuValue _aayu_prim_res = make_list();
    AayuValue _aayu_prim_res2 = make_list();
    AayuValue _aayu_prim_line = make_num(0);
    AayuValue _aayu_prim_col = make_num(0);
    AayuValue _aayu_prim_elements = make_list();
    AayuValue _aayu_prim_dict_keys = make_list();
    AayuValue _aayu_prim_dict_vals = make_list();
    AayuValue _aayu_prim_expr = make_list();
    AayuValue _aayu_prim_name = make_str("");
    AayuValue _aayu_prim_idx = make_list();
    AayuValue _aayu_prim_args = make_list();
    AayuValue _aayu_prim_loop = aayu_eq(make_num(1), make_num(1));
    AayuValue _aayu_prim_arg_loop = aayu_eq(make_num(1), make_num(1));
    if (aayu_is_truthy(aayu_greater_eq(_aayu_pos, aayu_len(_aayu_tokens)))) {
        aayu_print(make_str("Syntax Error: Unexpected EOF in expression"));
        return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_fn_make_literal(make_str("null"), make_num(0), make_num(0))); _l; });
    }
    AayuValue _aayu_prim_t = aayu_subscript(_aayu_tokens, _aayu_pos);
    if (aayu_is_truthy(aayu_eq(aayu_subscript(_aayu_prim_t, make_str("type")), make_str("NUMBER")))) {
        return ({ AayuValue _l = make_list(); aayu_list_append(&_l, aayu_add(_aayu_pos, make_num(1))); aayu_list_append(&_l, _aayu_fn_make_literal(aayu_subscript(_aayu_prim_t, make_str("value")), aayu_subscript(_aayu_prim_t, make_str("line")), aayu_subscript(_aayu_prim_t, make_str("column")))); _l; });
    }
    if (aayu_is_truthy(aayu_eq(aayu_subscript(_aayu_prim_t, make_str("type")), make_str("STRING")))) {
        return ({ AayuValue _l = make_list(); aayu_list_append(&_l, aayu_add(_aayu_pos, make_num(1))); aayu_list_append(&_l, _aayu_fn_make_literal(aayu_subscript(_aayu_prim_t, make_str("value")), aayu_subscript(_aayu_prim_t, make_str("line")), aayu_subscript(_aayu_prim_t, make_str("column")))); _l; });
    }
    if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("[")))) {
        _aayu_prim_line = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("line"));
        _aayu_prim_col = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("column"));
        _aayu_pos = aayu_add(_aayu_pos, make_num(1));
        _aayu_prim_elements = make_list();
        if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("]")))) {
            _aayu_pos = aayu_add(_aayu_pos, make_num(1));
            return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_fn_make_array(_aayu_prim_elements, _aayu_prim_line, _aayu_prim_col)); _l; });
        }
        else {
            _aayu_prim_loop = aayu_eq(make_num(1), make_num(1));
            while (aayu_is_truthy(_aayu_prim_loop)) {
                _aayu_prim_res = _aayu_fn_parse_expression(_aayu_tokens, _aayu_pos);
                _aayu_pos = aayu_subscript(_aayu_prim_res, make_num(0));
                _aayu_prim_elements = aayu_add(_aayu_prim_elements, ({ AayuValue _l = make_list(); aayu_list_append(&_l, aayu_subscript(_aayu_prim_res, make_num(1))); _l; }));
                if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str(",")))) {
                    _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                }
                else {
                    _aayu_prim_loop = aayu_eq(make_num(1), make_num(0));
                }
            }
            _aayu_prim_res2 = _aayu_fn_expect_val(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("]"), make_str("Expect ']' after array prim_elements."));
            _aayu_pos = aayu_subscript(_aayu_prim_res2, make_num(0));
            return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_fn_make_array(_aayu_prim_elements, _aayu_prim_line, _aayu_prim_col)); _l; });
        }
    }
    if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("{")))) {
        _aayu_prim_line = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("line"));
        _aayu_prim_col = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("column"));
        _aayu_pos = aayu_add(_aayu_pos, make_num(1));
        _aayu_prim_dict_keys = make_list();
        _aayu_prim_dict_vals = make_list();
        if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("}")))) {
            _aayu_pos = aayu_add(_aayu_pos, make_num(1));
            return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_fn_make_dict(_aayu_prim_dict_keys, _aayu_prim_dict_vals, _aayu_prim_line, _aayu_prim_col)); _l; });
        }
        else {
            _aayu_prim_loop = aayu_eq(make_num(1), make_num(1));
            while (aayu_is_truthy(_aayu_prim_loop)) {
                _aayu_prim_res = _aayu_fn_parse_expression(_aayu_tokens, _aayu_pos);
                _aayu_pos = aayu_subscript(_aayu_prim_res, make_num(0));
                _aayu_prim_dict_keys = aayu_add(_aayu_prim_dict_keys, ({ AayuValue _l = make_list(); aayu_list_append(&_l, aayu_subscript(aayu_subscript(_aayu_prim_res, make_num(1)), make_str("value"))); _l; }));
                _aayu_prim_res = _aayu_fn_expect_val(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str(":"), make_str("Expect ':' after dict key."));
                _aayu_pos = aayu_subscript(_aayu_prim_res, make_num(0));
                _aayu_prim_res = _aayu_fn_parse_expression(_aayu_tokens, _aayu_pos);
                _aayu_pos = aayu_subscript(_aayu_prim_res, make_num(0));
                _aayu_prim_dict_vals = aayu_add(_aayu_prim_dict_vals, ({ AayuValue _l = make_list(); aayu_list_append(&_l, aayu_subscript(_aayu_prim_res, make_num(1))); _l; }));
                if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str(",")))) {
                    _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                }
                else {
                    _aayu_prim_loop = aayu_eq(make_num(1), make_num(0));
                }
            }
            _aayu_prim_res2 = _aayu_fn_expect_val(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("}"), make_str("Expect '}' after dict prim_elements."));
            _aayu_pos = aayu_subscript(_aayu_prim_res2, make_num(0));
            return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_fn_make_dict(_aayu_prim_dict_keys, _aayu_prim_dict_vals, _aayu_prim_line, _aayu_prim_col)); _l; });
        }
    }
    if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("(")))) {
        _aayu_pos = aayu_add(_aayu_pos, make_num(1));
        _aayu_prim_res = _aayu_fn_parse_expression(_aayu_tokens, _aayu_pos);
        _aayu_pos = aayu_subscript(_aayu_prim_res, make_num(0));
        _aayu_prim_expr = aayu_subscript(_aayu_prim_res, make_num(1));
        _aayu_prim_res2 = _aayu_fn_expect_val(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str(")"), make_str("Expect ')' after expression."));
        _aayu_pos = aayu_subscript(_aayu_prim_res2, make_num(0));
        return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_prim_expr); _l; });
    }
    if (aayu_is_truthy(aayu_eq(aayu_subscript(_aayu_prim_t, make_str("type")), make_str("IDENTIFIER")))) {
        _aayu_prim_line = aayu_subscript(_aayu_prim_t, make_str("line"));
        _aayu_prim_col = aayu_subscript(_aayu_prim_t, make_str("column"));
        _aayu_prim_name = aayu_subscript(_aayu_prim_t, make_str("value"));
        _aayu_pos = aayu_add(_aayu_pos, make_num(1));
        _aayu_prim_expr = _aayu_fn_make_identifier(_aayu_prim_name, _aayu_prim_line, _aayu_prim_col);
        _aayu_prim_loop = aayu_eq(make_num(1), make_num(1));
        while (aayu_is_truthy(_aayu_prim_loop)) {
            if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("[")))) {
                _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                _aayu_prim_res = _aayu_fn_parse_expression(_aayu_tokens, _aayu_pos);
                _aayu_pos = aayu_subscript(_aayu_prim_res, make_num(0));
                _aayu_prim_idx = aayu_subscript(_aayu_prim_res, make_num(1));
                _aayu_prim_res2 = _aayu_fn_expect_val(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("]"), make_str("Expect ']' after index."));
                _aayu_pos = aayu_subscript(_aayu_prim_res2, make_num(0));
                _aayu_prim_expr = _aayu_fn_make_subscript(_aayu_prim_expr, _aayu_prim_idx, _aayu_prim_line, _aayu_prim_col);
            }
            else {
                if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("(")))) {
                    _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                    _aayu_prim_args = make_list();
                    if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str(")")))) {
                        _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                        _aayu_prim_expr = _aayu_fn_make_call(_aayu_prim_expr, _aayu_prim_args, _aayu_prim_line, _aayu_prim_col);
                    }
                    else {
                        _aayu_prim_arg_loop = aayu_eq(make_num(1), make_num(1));
                        while (aayu_is_truthy(_aayu_prim_arg_loop)) {
                            _aayu_prim_res = _aayu_fn_parse_expression(_aayu_tokens, _aayu_pos);
                            _aayu_pos = aayu_subscript(_aayu_prim_res, make_num(0));
                            _aayu_prim_args = aayu_add(_aayu_prim_args, ({ AayuValue _l = make_list(); aayu_list_append(&_l, aayu_subscript(_aayu_prim_res, make_num(1))); _l; }));
                            if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str(",")))) {
                                _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                            }
                            else {
                                _aayu_prim_arg_loop = aayu_eq(make_num(1), make_num(0));
                            }
                        }
                        _aayu_prim_res2 = _aayu_fn_expect_val(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str(")"), make_str("Expect ')' after arguments."));
                        _aayu_pos = aayu_subscript(_aayu_prim_res2, make_num(0));
                        _aayu_prim_expr = _aayu_fn_make_call(_aayu_prim_expr, _aayu_prim_args, _aayu_prim_line, _aayu_prim_col);
                    }
                }
                else {
                    _aayu_prim_loop = aayu_eq(make_num(1), make_num(0));
                }
            }
        }
        return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_prim_expr); _l; });
    }
    aayu_print(aayu_add(make_str("Syntax Error: Unexpected token "), aayu_subscript(_aayu_prim_t, make_str("value"))));
    return ({ AayuValue _l = make_list(); aayu_list_append(&_l, aayu_add(_aayu_pos, make_num(1))); aayu_list_append(&_l, _aayu_fn_make_literal(make_str("null"), aayu_subscript(_aayu_prim_t, make_str("line")), aayu_subscript(_aayu_prim_t, make_str("column")))); _l; });
    return make_null();
}

AayuValue _aayu_fn_parse_statement(AayuValue _aayu_tokens, AayuValue _aayu_pos) {
    AayuValue _aayu_stmt_res = make_list();
    AayuValue _aayu_stmt_res2 = make_list();
    AayuValue _aayu_stmt_line = make_num(0);
    AayuValue _aayu_stmt_col = make_num(0);
    AayuValue _aayu_stmt_name_tok = make_list();
    AayuValue _aayu_stmt_value = make_list();
    AayuValue _aayu_stmt_cond = make_list();
    AayuValue _aayu_stmt_then_branch = make_list();
    AayuValue _aayu_stmt_else_branch = make_list();
    AayuValue _aayu_stmt_body = make_list();
    AayuValue _aayu_stmt_next_pos = make_num(0);
    AayuValue _aayu_stmt_next_tok = make_list();
    AayuValue _aayu_stmt_name = make_str("");
    AayuValue _aayu_stmt_loop = aayu_eq(make_num(1), make_num(1));
    AayuValue _aayu_stmt_else_loop = aayu_eq(make_num(1), make_num(1));
    if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("KEYWORD"), make_str("let")))) {
        _aayu_stmt_line = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("line"));
        _aayu_stmt_col = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("column"));
        _aayu_pos = aayu_add(_aayu_pos, make_num(1));
        _aayu_stmt_res = _aayu_fn_expect(_aayu_tokens, _aayu_pos, make_str("IDENTIFIER"), make_str("Expect variable stmt_name."));
        _aayu_pos = aayu_subscript(_aayu_stmt_res, make_num(0));
        _aayu_stmt_name_tok = aayu_subscript(_aayu_stmt_res, make_num(1));
        _aayu_stmt_res = _aayu_fn_expect_val(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("="), make_str("Expect '='."));
        _aayu_pos = aayu_subscript(_aayu_stmt_res, make_num(0));
        _aayu_stmt_res = _aayu_fn_parse_expression(_aayu_tokens, _aayu_pos);
        _aayu_pos = aayu_subscript(_aayu_stmt_res, make_num(0));
        _aayu_stmt_value = aayu_subscript(_aayu_stmt_res, make_num(1));
        return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_fn_make_let(aayu_subscript(_aayu_stmt_name_tok, make_str("value")), _aayu_stmt_value, _aayu_stmt_line, _aayu_stmt_col)); _l; });
    }
    if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("KEYWORD"), make_str("if")))) {
        _aayu_stmt_line = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("line"));
        _aayu_stmt_col = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("column"));
        _aayu_pos = aayu_add(_aayu_pos, make_num(1));
        _aayu_stmt_res = _aayu_fn_parse_expression(_aayu_tokens, _aayu_pos);
        _aayu_pos = aayu_subscript(_aayu_stmt_res, make_num(0));
        _aayu_stmt_cond = aayu_subscript(_aayu_stmt_res, make_num(1));
        _aayu_stmt_then_branch = make_list();
        _aayu_stmt_else_branch = make_list();
        _aayu_stmt_loop = aayu_eq(make_num(1), make_num(1));
        while (aayu_is_truthy(_aayu_stmt_loop)) {
            if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("KEYWORD"), make_str("end")))) {
                _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                _aayu_stmt_loop = aayu_eq(make_num(1), make_num(0));
            }
            else {
                if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("KEYWORD"), make_str("else")))) {
                    _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                    _aayu_stmt_else_loop = aayu_eq(make_num(1), make_num(1));
                    while (aayu_is_truthy(_aayu_stmt_else_loop)) {
                        if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("KEYWORD"), make_str("end")))) {
                            _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                            _aayu_stmt_else_loop = aayu_eq(make_num(1), make_num(0));
                            _aayu_stmt_loop = aayu_eq(make_num(1), make_num(0));
                        }
                        else {
                            _aayu_stmt_res = _aayu_fn_parse_statement(_aayu_tokens, _aayu_pos);
                            _aayu_pos = aayu_subscript(_aayu_stmt_res, make_num(0));
                            _aayu_stmt_else_branch = aayu_add(_aayu_stmt_else_branch, ({ AayuValue _l = make_list(); aayu_list_append(&_l, aayu_subscript(_aayu_stmt_res, make_num(1))); _l; }));
                        }
                    }
                }
                else {
                    _aayu_stmt_res = _aayu_fn_parse_statement(_aayu_tokens, _aayu_pos);
                    _aayu_pos = aayu_subscript(_aayu_stmt_res, make_num(0));
                    _aayu_stmt_then_branch = aayu_add(_aayu_stmt_then_branch, ({ AayuValue _l = make_list(); aayu_list_append(&_l, aayu_subscript(_aayu_stmt_res, make_num(1))); _l; }));
                }
            }
        }
        return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_fn_make_if(_aayu_stmt_cond, _aayu_stmt_then_branch, _aayu_stmt_else_branch, _aayu_stmt_line, _aayu_stmt_col)); _l; });
    }
    if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("KEYWORD"), make_str("while")))) {
        _aayu_stmt_line = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("line"));
        _aayu_stmt_col = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("column"));
        _aayu_pos = aayu_add(_aayu_pos, make_num(1));
        _aayu_stmt_res = _aayu_fn_parse_expression(_aayu_tokens, _aayu_pos);
        _aayu_pos = aayu_subscript(_aayu_stmt_res, make_num(0));
        _aayu_stmt_cond = aayu_subscript(_aayu_stmt_res, make_num(1));
        _aayu_stmt_body = make_list();
        _aayu_stmt_loop = aayu_eq(make_num(1), make_num(1));
        while (aayu_is_truthy(_aayu_stmt_loop)) {
            if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("KEYWORD"), make_str("end")))) {
                _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                _aayu_stmt_loop = aayu_eq(make_num(1), make_num(0));
            }
            else {
                _aayu_stmt_res = _aayu_fn_parse_statement(_aayu_tokens, _aayu_pos);
                _aayu_pos = aayu_subscript(_aayu_stmt_res, make_num(0));
                _aayu_stmt_body = aayu_add(_aayu_stmt_body, ({ AayuValue _l = make_list(); aayu_list_append(&_l, aayu_subscript(_aayu_stmt_res, make_num(1))); _l; }));
            }
        }
        return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_fn_make_while(_aayu_stmt_cond, _aayu_stmt_body, _aayu_stmt_line, _aayu_stmt_col)); _l; });
    }
    if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("KEYWORD"), make_str("return")))) {
        _aayu_stmt_line = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("line"));
        _aayu_stmt_col = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("column"));
        _aayu_pos = aayu_add(_aayu_pos, make_num(1));
        _aayu_stmt_res = _aayu_fn_parse_expression(_aayu_tokens, _aayu_pos);
        _aayu_pos = aayu_subscript(_aayu_stmt_res, make_num(0));
        _aayu_stmt_value = aayu_subscript(_aayu_stmt_res, make_num(1));
        return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_fn_make_return(_aayu_stmt_value, _aayu_stmt_line, _aayu_stmt_col)); _l; });
    }
    if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("KEYWORD"), make_str("print")))) {
        _aayu_stmt_line = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("line"));
        _aayu_stmt_col = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("column"));
        _aayu_pos = aayu_add(_aayu_pos, make_num(1));
        if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("(")))) {
            _aayu_pos = aayu_add(_aayu_pos, make_num(1));
            _aayu_stmt_res = _aayu_fn_parse_expression(_aayu_tokens, _aayu_pos);
            _aayu_pos = aayu_subscript(_aayu_stmt_res, make_num(0));
            _aayu_stmt_value = aayu_subscript(_aayu_stmt_res, make_num(1));
            _aayu_stmt_res2 = _aayu_fn_expect_val(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str(")"), make_str("Expect ')' after print."));
            _aayu_pos = aayu_subscript(_aayu_stmt_res2, make_num(0));
        }
        else {
            _aayu_stmt_res = _aayu_fn_parse_expression(_aayu_tokens, _aayu_pos);
            _aayu_pos = aayu_subscript(_aayu_stmt_res, make_num(0));
            _aayu_stmt_value = aayu_subscript(_aayu_stmt_res, make_num(1));
        }
        return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_fn_make_call(make_str("print"), ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_stmt_value); _l; }), _aayu_stmt_line, _aayu_stmt_col)); _l; });
    }
    if (aayu_is_truthy(_aayu_fn_check(_aayu_tokens, _aayu_pos, make_str("IDENTIFIER")))) {
        _aayu_stmt_next_pos = aayu_add(_aayu_pos, make_num(1));
        if (aayu_is_truthy(aayu_less(_aayu_stmt_next_pos, aayu_len(_aayu_tokens)))) {
            _aayu_stmt_next_tok = aayu_subscript(_aayu_tokens, _aayu_stmt_next_pos);
            if (aayu_is_truthy(aayu_eq(aayu_subscript(_aayu_stmt_next_tok, make_str("type")), make_str("PUNCTUATION")))) {
                if (aayu_is_truthy(aayu_eq(aayu_subscript(_aayu_stmt_next_tok, make_str("value")), make_str("=")))) {
                    _aayu_stmt_line = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("line"));
                    _aayu_stmt_col = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("column"));
                    _aayu_stmt_name = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("value"));
                    _aayu_pos = aayu_add(_aayu_pos, make_num(2));
                    _aayu_stmt_res = _aayu_fn_parse_expression(_aayu_tokens, _aayu_pos);
                    _aayu_pos = aayu_subscript(_aayu_stmt_res, make_num(0));
                    _aayu_stmt_value = aayu_subscript(_aayu_stmt_res, make_num(1));
                    return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_fn_make_assignment(_aayu_stmt_name, _aayu_stmt_value, _aayu_stmt_line, _aayu_stmt_col)); _l; });
                }
            }
        }
    }
    return _aayu_fn_parse_expression(_aayu_tokens, _aayu_pos);
    return make_null();
}

AayuValue _aayu_fn_parse_action_decl(AayuValue _aayu_tokens, AayuValue _aayu_pos) {
    AayuValue _aayu_act_res = make_list();
    AayuValue _aayu_act_line = make_num(0);
    AayuValue _aayu_act_col = make_num(0);
    AayuValue _aayu_act_name_tok = make_list();
    AayuValue _aayu_act_args = make_list();
    AayuValue _aayu_act_body = make_list();
    AayuValue _aayu_act_loop = aayu_eq(make_num(1), make_num(1));
    AayuValue _aayu_act_arg_loop = aayu_eq(make_num(1), make_num(1));
    _aayu_act_line = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("line"));
    _aayu_act_col = aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("column"));
    _aayu_pos = aayu_add(_aayu_pos, make_num(1));
    _aayu_act_res = _aayu_fn_expect(_aayu_tokens, _aayu_pos, make_str("IDENTIFIER"), make_str("Expect action act_name."));
    _aayu_pos = aayu_subscript(_aayu_act_res, make_num(0));
    _aayu_act_name_tok = aayu_subscript(_aayu_act_res, make_num(1));
    _aayu_act_args = make_list();
    if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str("(")))) {
        _aayu_pos = aayu_add(_aayu_pos, make_num(1));
        if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str(")")))) {
            _aayu_pos = aayu_add(_aayu_pos, make_num(1));
        }
        else {
            _aayu_act_arg_loop = aayu_eq(make_num(1), make_num(1));
            while (aayu_is_truthy(_aayu_act_arg_loop)) {
                _aayu_act_res = _aayu_fn_expect(_aayu_tokens, _aayu_pos, make_str("IDENTIFIER"), make_str("Expect argument act_name."));
                _aayu_pos = aayu_subscript(_aayu_act_res, make_num(0));
                _aayu_act_args = aayu_add(_aayu_act_args, ({ AayuValue _l = make_list(); aayu_list_append(&_l, aayu_subscript(aayu_subscript(_aayu_act_res, make_num(1)), make_str("value"))); _l; }));
                if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str(",")))) {
                    _aayu_pos = aayu_add(_aayu_pos, make_num(1));
                }
                else {
                    _aayu_act_arg_loop = aayu_eq(make_num(1), make_num(0));
                }
            }
            _aayu_act_res = _aayu_fn_expect_val(_aayu_tokens, _aayu_pos, make_str("PUNCTUATION"), make_str(")"), make_str("Expect ')' after arguments."));
            _aayu_pos = aayu_subscript(_aayu_act_res, make_num(0));
        }
    }
    _aayu_act_body = make_list();
    _aayu_act_loop = aayu_eq(make_num(1), make_num(1));
    while (aayu_is_truthy(_aayu_act_loop)) {
        if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("KEYWORD"), make_str("end")))) {
            _aayu_pos = aayu_add(_aayu_pos, make_num(1));
            _aayu_act_loop = aayu_eq(make_num(1), make_num(0));
        }
        else {
            _aayu_act_res = _aayu_fn_parse_statement(_aayu_tokens, _aayu_pos);
            _aayu_pos = aayu_subscript(_aayu_act_res, make_num(0));
            _aayu_act_body = aayu_add(_aayu_act_body, ({ AayuValue _l = make_list(); aayu_list_append(&_l, aayu_subscript(_aayu_act_res, make_num(1))); _l; }));
        }
    }
    return ({ AayuValue _l = make_list(); aayu_list_append(&_l, _aayu_pos); aayu_list_append(&_l, _aayu_fn_make_action(aayu_subscript(_aayu_act_name_tok, make_str("value")), _aayu_act_args, _aayu_act_body, _aayu_act_line, _aayu_act_col)); _l; });
    return make_null();
}

AayuValue _aayu_fn_parse(AayuValue _aayu_tokens) {
    AayuValue _aayu_main_res = make_list();
    AayuValue _aayu_main_stmts = make_list();
    AayuValue _aayu_pos = make_num(0);
    AayuValue _aayu_main_length = aayu_len(_aayu_tokens);
    while (aayu_is_truthy(aayu_less(_aayu_pos, _aayu_main_length))) {
        if (aayu_is_truthy(aayu_eq(aayu_subscript(aayu_subscript(_aayu_tokens, _aayu_pos), make_str("type")), make_str("EOF")))) {
            _aayu_pos = _aayu_main_length;
        }
        else {
            if (aayu_is_truthy(_aayu_fn_match(_aayu_tokens, _aayu_pos, make_str("KEYWORD"), make_str("action")))) {
                _aayu_main_res = _aayu_fn_parse_action_decl(_aayu_tokens, _aayu_pos);
                _aayu_pos = aayu_subscript(_aayu_main_res, make_num(0));
                _aayu_main_stmts = aayu_add(_aayu_main_stmts, ({ AayuValue _l = make_list(); aayu_list_append(&_l, aayu_subscript(_aayu_main_res, make_num(1))); _l; }));
            }
            else {
                _aayu_main_res = _aayu_fn_parse_statement(_aayu_tokens, _aayu_pos);
                _aayu_pos = aayu_subscript(_aayu_main_res, make_num(0));
                _aayu_main_stmts = aayu_add(_aayu_main_stmts, ({ AayuValue _l = make_list(); aayu_list_append(&_l, aayu_subscript(_aayu_main_res, make_num(1))); _l; }));
                aayu_print(make_str("Appended to main_stmts. New len:"));
                aayu_print(aayu_len(_aayu_main_stmts));
            }
        }
    }
    return _aayu_fn_make_program(_aayu_main_stmts);
    return make_null();
}

AayuValue _aayu_fn_print_ast(AayuValue _aayu_ast) {
    AayuValue _aayu_length = aayu_len(aayu_subscript(_aayu_ast, make_str("statements")));
    aayu_print(make_str("Program Statements:"));
    aayu_print(_aayu_length);
    AayuValue _aayu_i = make_num(0);
    while (aayu_is_truthy(aayu_less(_aayu_i, _aayu_length))) {
        AayuValue _aayu_stmt = aayu_subscript(aayu_subscript(_aayu_ast, make_str("statements")), _aayu_i);
        aayu_print(aayu_subscript(_aayu_stmt, make_str("type")));
        _aayu_i = aayu_add(_aayu_i, make_num(1));
    }
    return make_num(0);
    return make_null();
}

AayuValue _aayu_fn_main(void) {
    AayuValue _aayu_src = make_str("let x = 10 \n let y = 20 \n print(x + y)");
    aayu_print(make_str("Parsing Native Code:"));
    aayu_print(_aayu_src);
    AayuValue _aayu_tokens = _aayu_fn_tokenize(_aayu_src);
    AayuValue _aayu_ast = _aayu_fn_parse(_aayu_tokens);
    _aayu_fn_print_ast(_aayu_ast);
    return make_null();
}

int main() {
    AayuValue _aayu_tokens = ({ AayuValue _l = make_list(); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("KEYWORD")); aayu_dict_set(&_d, "value", make_str("action")); aayu_dict_set(&_d, "line", make_num(1)); aayu_dict_set(&_d, "column", make_num(1)); _d; })); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("IDENTIFIER")); aayu_dict_set(&_d, "value", make_str("add")); aayu_dict_set(&_d, "line", make_num(1)); aayu_dict_set(&_d, "column", make_num(8)); _d; })); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("PUNCTUATION")); aayu_dict_set(&_d, "value", make_str("(")); aayu_dict_set(&_d, "line", make_num(1)); aayu_dict_set(&_d, "column", make_num(11)); _d; })); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("IDENTIFIER")); aayu_dict_set(&_d, "value", make_str("a")); aayu_dict_set(&_d, "line", make_num(1)); aayu_dict_set(&_d, "column", make_num(12)); _d; })); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("PUNCTUATION")); aayu_dict_set(&_d, "value", make_str(",")); aayu_dict_set(&_d, "line", make_num(1)); aayu_dict_set(&_d, "column", make_num(13)); _d; })); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("IDENTIFIER")); aayu_dict_set(&_d, "value", make_str("b")); aayu_dict_set(&_d, "line", make_num(1)); aayu_dict_set(&_d, "column", make_num(15)); _d; })); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("PUNCTUATION")); aayu_dict_set(&_d, "value", make_str(")")); aayu_dict_set(&_d, "line", make_num(1)); aayu_dict_set(&_d, "column", make_num(16)); _d; })); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("KEYWORD")); aayu_dict_set(&_d, "value", make_str("return")); aayu_dict_set(&_d, "line", make_num(2)); aayu_dict_set(&_d, "column", make_num(5)); _d; })); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("IDENTIFIER")); aayu_dict_set(&_d, "value", make_str("a")); aayu_dict_set(&_d, "line", make_num(2)); aayu_dict_set(&_d, "column", make_num(12)); _d; })); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("PUNCTUATION")); aayu_dict_set(&_d, "value", make_str("+")); aayu_dict_set(&_d, "line", make_num(2)); aayu_dict_set(&_d, "column", make_num(14)); _d; })); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("IDENTIFIER")); aayu_dict_set(&_d, "value", make_str("b")); aayu_dict_set(&_d, "line", make_num(2)); aayu_dict_set(&_d, "column", make_num(16)); _d; })); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("KEYWORD")); aayu_dict_set(&_d, "value", make_str("end")); aayu_dict_set(&_d, "line", make_num(3)); aayu_dict_set(&_d, "column", make_num(1)); _d; })); aayu_list_append(&_l, ({ AayuValue _d = make_dict(); aayu_dict_set(&_d, "type", make_str("EOF")); aayu_dict_set(&_d, "value", make_str("")); aayu_dict_set(&_d, "line", make_num(3)); aayu_dict_set(&_d, "column", make_num(4)); _d; })); _l; });
    AayuValue _aayu_ast = _aayu_fn_parse(_aayu_tokens);
    aayu_print(make_str("AST parsed successfully!"));
    aayu_print(aayu_subscript(_aayu_ast, make_str("type")));
    aayu_print(aayu_subscript(_aayu_ast, make_str("statements")));
    _aayu_fn_main();
    return 0;
}
