# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import argparse
import sys
import os
import subprocess

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.ast.nodes import *

def parse_file_recursive(file_path, visited_paths):
    absolute_path = os.path.abspath(file_path)
    if absolute_path in visited_paths:
        return []
    visited_paths.add(absolute_path)
    
    with open(absolute_path, "r", encoding="utf-8") as f:
        src = f.read()
        
    lexer = Lexer(src)
    tokens = lexer.tokenize()
    parser_obj = Parser(tokens)
    ast = parser_obj.parse()
    
    all_statements = []
    base_dir = os.path.dirname(absolute_path)
    
    for stmt in getattr(ast, "statements", []):
        if isinstance(stmt, ImportNode):
            rel_path = stmt.module.replace(".", os.sep) + ".aayu"
            target_path = os.path.join(base_dir, rel_path)
            
            if not os.path.exists(target_path):
                print(f"Error: Module '{stmt.module}' not found at {target_path}")
                sys.exit(1)
                
            imported_stmts = parse_file_recursive(target_path, visited_paths)
            all_statements.extend(imported_stmts)
        else:
            all_statements.append(stmt)
            
    return all_statements

def handle(args):
    parser = argparse.ArgumentParser(description="Compile AAYU to Native Executable via C Backend")
    parser.add_argument("file", help="AAYU file to compile")
    parser.add_argument("-o", "--output", help="Output executable name")
    
    parsed_args, unknown = parser.parse_known_args(args)
    
    file_path = parsed_args.file
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
        
    out_name = parsed_args.output
    if not out_name:
        out_name = os.path.splitext(os.path.basename(file_path))[0]
        if os.name == 'nt':
            out_name += ".exe"
            
    c_out = f"{out_name.replace('.exe', '')}.c"
        
    print(f"[AAYU Native Builder] Parsing {file_path} and resolving imports...")
    visited = set()
    merged_statements = parse_file_recursive(file_path, visited)
    ast = ProgramNode(statements=merged_statements, line=1, column=1)
    
    print("[AAYU Native Builder] Transpiling AST to C Code...")
    c_code = compile_to_c(ast)
    
    with open(c_out, "w", encoding="utf-8") as f:
        f.write(c_code)
        
    c_file = c_out
    exe_file = out_name
    print(f"[AAYU Native Builder] Invoking GCC Compiler on {c_file}...")
    gcc_command = ["gcc", c_file, "-o", exe_file, "-O3", "-Wno-incompatible-pointer-types", "-Wno-implicit-function-declaration", "-Wno-int-conversion", "-Wno-pointer-sign"]
    
    try:
        subprocess.run(gcc_command, check=True)
        print(f"[AAYU Native Builder] Success! Created ultra-fast native executable: {exe_file}")
        
        # Clean up the intermediate .c file to ensure Git doesn't classify this as a C project!
        if os.path.exists(c_file):
            os.remove(c_file)
            
    except subprocess.CalledProcessError as e:
        print(f"[AAYU Native Builder] Compilation failed with error code {e.returncode}")
    except FileNotFoundError:
        print("[AAYU Native Builder] Error: 'gcc' not found. Ensure GCC/MinGW is installed and in PATH.")


def compile_to_c(ast):
    output = []
    def emit(s):
        output.append(s)
        
    # --- AAYU NATIVE C RUNTIME ENGINE ---
    emit("#include <stdio.h>\n")
    emit("#include <stdlib.h>\n")
    emit("#include <string.h>\n")
    emit("#include <setjmp.h>\n\n")
    
    emit("typedef enum { VAL_NUM, VAL_STR, VAL_BOOL, VAL_NULL, VAL_LIST, VAL_DICT } AayuType;\n")
    emit("typedef struct AayuValue AayuValue;\n")
    emit("struct AayuValue {\n")
    emit("    AayuType type;\n")
    emit("    union {\n")
    emit("        double num;\n")
    emit("        char* str;\n")
    emit("        int boolean;\n")
    emit("        struct { AayuValue* items; int count; int capacity; } list;\n")
    emit("        struct { char** keys; AayuValue* values; int count; int capacity; } dict;\n")
    emit("    } as;\n")
    emit("};\n\n")
    
    emit("#define MAX_EXCEPTIONS 256\n")
    emit("jmp_buf aayu_exception_stack[MAX_EXCEPTIONS];\n")
    emit("int aayu_exception_depth = 0;\n")
    emit("AayuValue aayu_current_exception;\n\n")
    
    emit("void aayu_print(AayuValue v);\n")
    emit("void aayu_throw(AayuValue e) {\n")
    emit("    if (aayu_exception_depth == 0) {\n")
    emit("        printf(\"Unhandled Exception: \");\n")
    emit("        aayu_print(e);\n")
    emit("        exit(1);\n")
    emit("    }\n")
    emit("    aayu_current_exception = e;\n")
    emit("    longjmp(aayu_exception_stack[aayu_exception_depth - 1], 1);\n")
    emit("}\n\n")
    
    emit("AayuValue make_num(double n) { AayuValue v; v.type = VAL_NUM; v.as.num = n; return v; }\n")
    emit("AayuValue make_bool(int b) { AayuValue v; v.type = VAL_BOOL; v.as.boolean = b; return v; }\n")
    emit("AayuValue make_null() { AayuValue v; v.type = VAL_NULL; return v; }\n")
    emit("AayuValue make_str(const char* s) {\n")
    emit("    AayuValue v; v.type = VAL_STR;\n")
    emit("    v.as.str = malloc(strlen(s) + 1);\n")
    emit("    strcpy(v.as.str, s);\n")
    emit("    return v;\n")
    emit("}\n")
    emit("AayuValue make_list() {\n")
    emit("    AayuValue v; v.type = VAL_LIST;\n")
    emit("    v.as.list.count = 0; v.as.list.capacity = 8;\n")
    emit("    v.as.list.items = malloc(sizeof(AayuValue) * 8);\n")
    emit("    return v;\n")
    emit("}\n")
    emit("AayuValue make_dict() {\n")
    emit("    AayuValue v; v.type = VAL_DICT;\n")
    emit("    v.as.dict.count = 0; v.as.dict.capacity = 8;\n")
    emit("    v.as.dict.keys = malloc(sizeof(char*) * 8);\n")
    emit("    v.as.dict.values = malloc(sizeof(AayuValue) * 8);\n")
    emit("    return v;\n")
    emit("}\n\n")
    
    emit("void aayu_dict_set(AayuValue* dict, const char* key, AayuValue val) {\n")
    emit("    if (dict->type != VAL_DICT) return;\n")
    emit("    for(int i=0; i<dict->as.dict.count; i++) {\n")
    emit("        if(strcmp(dict->as.dict.keys[i], key) == 0) { dict->as.dict.values[i] = val; return; }\n")
    emit("    }\n")
    emit("    if (dict->as.dict.count >= dict->as.dict.capacity) {\n")
    emit("        dict->as.dict.capacity *= 2;\n")
    emit("        dict->as.dict.keys = realloc(dict->as.dict.keys, sizeof(char*) * dict->as.dict.capacity);\n")
    emit("        dict->as.dict.values = realloc(dict->as.dict.values, sizeof(AayuValue) * dict->as.dict.capacity);\n")
    emit("    }\n")
    emit("    dict->as.dict.keys[dict->as.dict.count] = malloc(strlen(key) + 1);\n")
    emit("    strcpy(dict->as.dict.keys[dict->as.dict.count], key);\n")
    emit("    dict->as.dict.values[dict->as.dict.count++] = val;\n")
    emit("}\n\n")

    emit("void aayu_print(AayuValue v) {\n")
    emit("    if (v.type == VAL_NUM) printf(\"%g\\n\", v.as.num);\n")
    emit("    else if (v.type == VAL_STR) printf(\"%s\\n\", v.as.str);\n")
    emit("    else if (v.type == VAL_BOOL) printf(\"%s\\n\", v.as.boolean ? \"true\" : \"false\");\n")
    emit("    else if (v.type == VAL_LIST) printf(\"[List size=%d]\\n\", v.as.list.count);\n")
    emit("    else if (v.type == VAL_DICT) printf(\"{Dict size=%d}\\n\", v.as.dict.count);\n")
    emit("    else printf(\"null\\n\");\n")
    emit("}\n\n")
    
    emit("void aayu_list_append(AayuValue* lst, AayuValue item) {\n")
    emit("    if (lst->type != VAL_LIST) return;\n")
    emit("    if (lst->as.list.count >= lst->as.list.capacity) {\n")
    emit("        lst->as.list.capacity *= 2;\n")
    emit("        lst->as.list.items = realloc(lst->as.list.items, sizeof(AayuValue) * lst->as.list.capacity);\n")
    emit("    }\n")
    emit("    lst->as.list.items[lst->as.list.count++] = item;\n")
    emit("}\n\n")

    emit("AayuValue aayu_add(AayuValue a, AayuValue b) {\n")
    emit("    if (a.type == VAL_NUM && b.type == VAL_NUM) return make_num(a.as.num + b.as.num);\n")
    emit("    if (a.type == VAL_STR && b.type == VAL_STR) {\n")
    emit("        char* res = malloc(strlen(a.as.str) + strlen(b.as.str) + 1);\n")
    emit("        strcpy(res, a.as.str); strcat(res, b.as.str);\n")
    emit("        return make_str(res);\n")
    emit("    }\n")
    emit("    if (a.type == VAL_LIST && b.type == VAL_LIST) {\n")
    emit("        AayuValue res = make_list();\n")
    emit("        for(int i=0; i<a.as.list.count; i++) aayu_list_append(&res, a.as.list.items[i]);\n")
    emit("        for(int i=0; i<b.as.list.count; i++) aayu_list_append(&res, b.as.list.items[i]);\n")
    emit("        return res;\n")
    emit("    }\n")
    emit("    return make_num(0);\n")
    emit("}\n\n")

    emit("int aayu_is_truthy(AayuValue v) {\n")
    emit("    if (v.type == VAL_NUM) return v.as.num != 0;\n")
    emit("    if (v.type == VAL_BOOL) return v.as.boolean;\n")
    emit("    if (v.type == VAL_STR) return strlen(v.as.str) > 0;\n")
    emit("    return 0;\n")
    emit("}\n\n")
    
    emit("AayuValue aayu_less(AayuValue a, AayuValue b) {\n")
    emit("    if (a.type == VAL_NUM && b.type == VAL_NUM) return make_bool(a.as.num < b.as.num);\n")
    emit("    if (a.type == VAL_STR && b.type == VAL_STR) return make_bool(strcmp(a.as.str, b.as.str) < 0);\n")
    emit("    return make_bool(0);\n")
    emit("}\n\n")

    emit("AayuValue aayu_eq(AayuValue a, AayuValue b) {\n")
    emit("    if (a.type == VAL_NUM && b.type == VAL_NUM) return make_bool(a.as.num == b.as.num);\n")
    emit("    if (a.type == VAL_STR && b.type == VAL_STR) return make_bool(strcmp(a.as.str, b.as.str) == 0);\n")
    emit("    if (a.type == VAL_BOOL && b.type == VAL_BOOL) return make_bool(a.as.boolean == b.as.boolean);\n")
    emit("    if (a.type == VAL_NULL && b.type == VAL_NULL) return make_bool(1);\n")
    emit("    return make_bool(0);\n")
    emit("}\n\n")
    
    emit("AayuValue aayu_greater_eq(AayuValue a, AayuValue b) {\n")
    emit("    if (a.type == VAL_NUM && b.type == VAL_NUM) return make_bool(a.as.num >= b.as.num);\n")
    emit("    if (a.type == VAL_STR && b.type == VAL_STR) return make_bool(strcmp(a.as.str, b.as.str) >= 0);\n")
    emit("    return make_bool(0);\n")
    emit("}\n\n")

    emit("AayuValue aayu_less_eq(AayuValue a, AayuValue b) {\n")
    emit("    if (a.type == VAL_NUM && b.type == VAL_NUM) return make_bool(a.as.num <= b.as.num);\n")
    emit("    if (a.type == VAL_STR && b.type == VAL_STR) return make_bool(strcmp(a.as.str, b.as.str) <= 0);\n")
    emit("    return make_bool(0);\n")
    emit("}\n\n")
    

    # --- HTTP AND JSON LIBRARY ---
    emit("AayuValue aayu_fetch(AayuValue url) {\n")
    emit("    if (url.type != VAL_STR) aayu_throw(make_str(\"fetch expects a string url\"));\n")
    emit("    char cmd[2048];\n")
    emit("    snprintf(cmd, sizeof(cmd), \"curl -s \\\"%s\\\"\", url.as.str);\n")
    # On Windows popen is _popen sometimes, but gcc provides popen.
    emit("    FILE *fp = popen(cmd, \"r\");\n")
    emit("    if (!fp) aayu_throw(make_str(\"Failed to execute curl\"));\n")
    emit("    int capacity = 4096;\n")
    emit("    int length = 0;\n")
    emit("    char* result = malloc(capacity);\n")
    emit("    result[0] = '\\0';\n")
    emit("    char buffer[1024];\n")
    emit("    while (fgets(buffer, sizeof(buffer), fp) != NULL) {\n")
    emit("        int len = strlen(buffer);\n")
    emit("        if (length + len >= capacity) {\n")
    emit("            capacity *= 2;\n")
    emit("            result = realloc(result, capacity);\n")
    emit("        }\n")
    emit("        strcat(result, buffer);\n")
    emit("        length += len;\n")
    emit("    }\n")
    emit("    pclose(fp);\n")
    emit("    return make_str(result);\n")
    emit("}\n\n")

    emit("void aayu_skip_whitespace(const char** c) {\n")
    emit("    while (**c == ' ' || **c == '\\n' || **c == '\\r' || **c == '\\t') (*c)++;\n")
    emit("}\n")
    emit("AayuValue aayu_parse_json_value(const char** c);\n")
    emit("AayuValue aayu_parse_json_string(const char** c) {\n")
    emit("    (*c)++; \n")
    emit("    const char* start = *c;\n")
    emit("    while (**c && **c != '\"') {\n")
    emit("        if (**c == '\\\\' && *(*c + 1)) (*c) += 2; else (*c)++;\n")
    emit("    }\n")
    emit("    int len = *c - start;\n")
    emit("    char* str = malloc(len + 1);\n")
    emit("    strncpy(str, start, len);\n")
    emit("    str[len] = '\\0';\n")
    emit("    (*c)++; \n")
    emit("    return make_str(str);\n")
    emit("}\n")
    emit("AayuValue aayu_parse_json_number(const char** c) {\n")
    emit("    char* end;\n")
    emit("    double val = strtod(*c, &end);\n")
    emit("    *c = end;\n")
    emit("    return make_num(val);\n")
    emit("}\n")
    emit("AayuValue aayu_parse_json_dict(const char** c) {\n")
    emit("    (*c)++; \n")
    emit("    AayuValue dict = make_dict();\n")
    emit("    aayu_skip_whitespace(c);\n")
    emit("    while (**c && **c != '}') {\n")
    emit("        if (**c != '\"') break;\n")
    emit("        AayuValue key = aayu_parse_json_string(c);\n")
    emit("        aayu_skip_whitespace(c);\n")
    emit("        if (**c == ':') (*c)++;\n")
    emit("        AayuValue val = aayu_parse_json_value(c);\n")
    emit("        aayu_dict_set(&dict, key.as.str, val);\n")
    emit("        aayu_skip_whitespace(c);\n")
    emit("        if (**c == ',') (*c)++;\n")
    emit("        aayu_skip_whitespace(c);\n")
    emit("    }\n")
    emit("    if (**c == '}') (*c)++;\n")
    emit("    return dict;\n")
    emit("}\n")
    emit("AayuValue aayu_parse_json_list(const char** c) {\n")
    emit("    (*c)++; \n")
    emit("    AayuValue list = make_list();\n")
    emit("    aayu_skip_whitespace(c);\n")
    emit("    while (**c && **c != ']') {\n")
    emit("        AayuValue val = aayu_parse_json_value(c);\n")
    emit("        aayu_list_append(&list, val);\n")
    emit("        aayu_skip_whitespace(c);\n")
    emit("        if (**c == ',') (*c)++;\n")
    emit("        aayu_skip_whitespace(c);\n")
    emit("    }\n")
    emit("    if (**c == ']') (*c)++;\n")
    emit("    return list;\n")
    emit("}\n")
    emit("AayuValue aayu_parse_json_value(const char** c) {\n")
    emit("    aayu_skip_whitespace(c);\n")
    emit("    if (!**c) return make_null();\n")
    emit("    if (**c == '\"') return aayu_parse_json_string(c);\n")
    emit("    if (**c == '{') return aayu_parse_json_dict(c);\n")
    emit("    if (**c == '[') return aayu_parse_json_list(c);\n")
    emit("    if (strncmp(*c, \"true\", 4) == 0) { *c += 4; return make_bool(1); }\n")
    emit("    if (strncmp(*c, \"false\", 5) == 0) { *c += 5; return make_bool(0); }\n")
    emit("    if (strncmp(*c, \"null\", 4) == 0) { *c += 4; return make_null(); }\n")
    emit("    return aayu_parse_json_number(c);\n")
    emit("}\n")
    emit("AayuValue aayu_json_parse(AayuValue json_str) {\n")
    emit("    if (json_str.type != VAL_STR) aayu_throw(make_str(\"json_parse expects a string\"));\n")
    emit("    const char* c = json_str.as.str;\n")
    emit("    return aayu_parse_json_value(&c);\n")
    emit("}\n\n")
    emit("AayuValue aayu_read_file(AayuValue path) {\n")
    emit("    if (path.type != VAL_STR) return make_null();\n")
    emit("    FILE* f = fopen(path.as.str, \"rb\");\n")
    emit("    if (!f) return make_null();\n")
    emit("    fseek(f, 0, SEEK_END); long fsize = ftell(f); fseek(f, 0, SEEK_SET);\n")
    emit("    char* string = malloc(fsize + 1);\n")
    emit("    fread(string, fsize, 1, f); fclose(f); string[fsize] = 0;\n")
    emit("    return make_str(string);\n")
    emit("}\n\n")
    
    emit("AayuValue aayu_write_file(AayuValue path, AayuValue content) {\n")
    emit("    if (path.type != VAL_STR || content.type != VAL_STR) return make_bool(0);\n")
    emit("    FILE* f = fopen(path.as.str, \"wb\");\n")
    emit("    if (!f) return make_bool(0);\n")
    emit("    fwrite(content.as.str, 1, strlen(content.as.str), f);\n")
    emit("    fclose(f);\n")
    emit("    return make_bool(1);\n")
    emit("}\n\n")
    
    emit("AayuValue aayu_subscript(AayuValue target, AayuValue index) {\n")
    emit("    if (target.type == VAL_DICT && index.type == VAL_STR) {\n")
    emit("        for(int i=0; i<target.as.dict.count; i++) {\n")
    emit("            if (strcmp(target.as.dict.keys[i], index.as.str) == 0) return target.as.dict.values[i];\n")
    emit("        }\n")
    emit("        return make_null();\n")
    emit("    }\n")
    emit("    if (index.type != VAL_NUM) return make_null();\n")
    emit("    int idx = (int)index.as.num;\n")
    emit("    if (target.type == VAL_LIST && idx >= 0 && idx < target.as.list.count) return target.as.list.items[idx];\n")
    emit("    if (target.type == VAL_STR && idx >= 0 && idx < strlen(target.as.str)) {\n")
    emit("        char c[2] = { target.as.str[idx], 0 };\n")
    emit("        return make_str(c);\n")
    emit("    }\n")
    emit("    return make_null();\n")
    emit("}\n\n")
    
    emit("AayuValue aayu_len(AayuValue target) {\n")
    emit("    if (target.type == VAL_LIST) return make_num(target.as.list.count);\n")
    emit("    if (target.type == VAL_STR) return make_num(strlen(target.as.str));\n")
    emit("    return make_num(0);\n")
    emit("}\n\n")

    # Forward Declarations
    for stmt in getattr(ast, "statements", []):
        if isinstance(stmt, ActionDeclarationNode):
            c_args = ", ".join([f"AayuValue _aayu_{arg}" for arg in stmt.args])
            emit(f"AayuValue _aayu_fn_{stmt.name}({c_args});\n")
    emit("\n")

    # --- FUNCTION DEFINITIONS ---
    def compile_expr(node):
        if isinstance(node, LiteralNode):
            if isinstance(node.value, str):
                safe_str = node.value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
                return f'make_str("{safe_str}")'
            elif isinstance(node.value, bool):
                return f'make_bool({1 if node.value else 0})'
            elif node.value is None:
                return "make_null()"
            else:
                return f"make_num({node.value})"
                
        if isinstance(node, IdentifierNode):
            if node.name == "true": return "make_bool(1)"
            if node.name == "false": return "make_bool(0)"
            if node.name == "null": return "make_null()"
            return f"_aayu_{node.name}"
            
        if isinstance(node, BinaryOpNode):
            left = compile_expr(node.left)
            right = compile_expr(node.right)
            if node.operator == '+':
                return f"aayu_add({left}, {right})"
            elif node.operator == '<':
                return f"aayu_less({left}, {right})"
            elif node.operator == '==':
                return f"aayu_eq({left}, {right})"
            elif node.operator == '>=':
                return f"aayu_greater_eq({left}, {right})"
            elif node.operator == '<=':
                return f"aayu_less_eq({left}, {right})"
            else:
                return f"make_num({left}.as.num {node.operator} {right}.as.num)"
                
        if isinstance(node, ActionCallNode):
            if node.name == "print":
                arg = compile_expr(node.args[0])
                return f'aayu_print({arg})'
            if node.name == "read_file":
                arg = compile_expr(node.args[0])
                return f'aayu_read_file({arg})'
            if node.name == "write_file":
                arg0 = compile_expr(node.args[0])
                arg1 = compile_expr(node.args[1])
                return f'aayu_write_file({arg0}, {arg1})'
            if node.name == "fetch":
                arg = compile_expr(node.args[0])
                return f'aayu_fetch({arg})'
            if node.name == "json_parse":
                arg = compile_expr(node.args[0])
                return f'aayu_json_parse({arg})'
            if node.name == "len":
                arg = compile_expr(node.args[0])
                return f'aayu_len({arg})'
            if node.name.endswith(".append"):
                return "make_null()" # Handled in stmts
                
            # User defined function call
            c_args = ", ".join([compile_expr(arg) for arg in node.args])
            return f"_aayu_fn_{node.name}({c_args})"
            
        if isinstance(node, ArrayNode):
            if not node.elements:
                return "make_list()"
            stmts = ["AayuValue _l = make_list();"]
            for el in node.elements:
                val_expr = compile_expr(el)
                stmts.append(f'aayu_list_append(&_l, {val_expr});')
            stmts.append("_l;")
            body = " ".join(stmts)
            return f"({{ {body} }})"
            
        if isinstance(node, DictionaryNode):
            stmts = ["AayuValue _d = make_dict();"]
            for k, v in node.pairs.items():
                val_expr = compile_expr(v)
                stmts.append(f'aayu_dict_set(&_d, "{k}", {val_expr});')
            stmts.append("_d;")
            body = " ".join(stmts)
            return f"({{ {body} }})"
            
        if isinstance(node, SubscriptNode):
            target = compile_expr(node.target)
            index = compile_expr(node.index)
            return f"aayu_subscript({target}, {index})"
                
        return "make_num(0)"

    def compile_stmt(stmt, indent, is_in_main=False):
        ind = "    " * indent
        
        if isinstance(stmt, LetDeclarationNode):
            val = compile_expr(stmt.value)
            if is_in_main:
                emit(f"{ind}_aayu_{stmt.name} = {val};\n")
            else:
                emit(f"{ind}AayuValue _aayu_{stmt.name} = {val};\n")
            
        elif isinstance(stmt, AssignmentNode):
            target = getattr(stmt.target, "name", stmt.target) if hasattr(stmt.target, "name") else stmt.target
            val = compile_expr(stmt.value)
            emit(f"{ind}_aayu_{target} = {val};\n")
            
        elif isinstance(stmt, WhileNode):
            cond = compile_expr(stmt.condition)
            emit(f"{ind}while (aayu_is_truthy({cond})) {{\n")
            for b in stmt.body:
                compile_stmt(b, indent + 1, is_in_main)
            emit(f"{ind}}}\n")
            
        elif isinstance(stmt, ActionCallNode):
            if stmt.name == "print":
                c_args = ", ".join([compile_expr(arg) for arg in stmt.args])
                emit(f"{ind}aayu_print({c_args});\n")
            elif stmt.name == "write_file":
                arg0 = compile_expr(stmt.args[0])
                arg1 = compile_expr(stmt.args[1])
                emit(f"{ind}aayu_write_file({arg0}, {arg1});\n")
            elif stmt.name == "read_file":
                arg = compile_expr(stmt.args[0])
                emit(f"{ind}aayu_read_file({arg});\n")
            elif stmt.name == "fetch":
                arg = compile_expr(stmt.args[0])
                emit(f"{ind}aayu_fetch({arg});\n")
            elif stmt.name == "json_parse":
                arg = compile_expr(stmt.args[0])
                emit(f"{ind}aayu_json_parse({arg});\n")
            else:
                c_args = ", ".join([compile_expr(arg) for arg in stmt.args])
                emit(f'{ind}_aayu_fn_{stmt.name}({c_args});\n')
                
        elif isinstance(stmt, ReturnNode):
            val = compile_expr(stmt.value) if getattr(stmt, "value", None) else "make_null()"
            emit(f"{ind}return {val};\n")
            
        elif isinstance(stmt, IfNode):
            cond = compile_expr(stmt.condition)
            emit(f"{ind}if (aayu_is_truthy({cond})) {{\n")
            for b in getattr(stmt, "then_branch", []):
                compile_stmt(b, indent + 1, is_in_main)
            emit(f"{ind}}}\n")
            if getattr(stmt, "else_branch", None):
                emit(f"{ind}else {{\n")
                for b in stmt.else_branch:
                    compile_stmt(b, indent + 1, is_in_main)
                emit(f"{ind}}}\n")
                
        elif isinstance(stmt, TryNode):
            emit(f"{ind}if (aayu_exception_depth < MAX_EXCEPTIONS) {{\n")
            emit(f"{ind}    if (setjmp(aayu_exception_stack[aayu_exception_depth++]) == 0) {{\n")
            for b in getattr(stmt, "try_block", []):
                compile_stmt(b, indent + 2, is_in_main)
            emit(f"{ind}        aayu_exception_depth--;\n")
            emit(f"{ind}    }} else {{\n")
            emit(f"{ind}        aayu_exception_depth--;\n")
            if getattr(stmt, "catch_var", None):
                if is_in_main:
                    emit(f"{ind}        _aayu_{stmt.catch_var} = aayu_current_exception;\n")
                else:
                    emit(f"{ind}        AayuValue _aayu_{stmt.catch_var} = aayu_current_exception;\n")
            for b in getattr(stmt, "catch_block", []):
                compile_stmt(b, indent + 2, is_in_main)
            emit(f"{ind}    }}\n")
            for b in getattr(stmt, "finally_block", []):
                compile_stmt(b, indent + 1, is_in_main)
            emit(f"{ind}}} else {{\n")
            emit(f"{ind}    printf(\"Exception stack overflow\\n\"); exit(1);\n")
            emit(f"{ind}}}\n")
            
        elif isinstance(stmt, ThrowNode):
            val = compile_expr(stmt.value)
            emit(f"{ind}aayu_throw({val});\n")
            
        elif isinstance(stmt, RethrowNode):
            emit(f"{ind}aayu_throw(aayu_current_exception);\n")

    # Pass 0.5: Global Variable declarations
    def declare_globals(nodes):
        for stmt in getattr(nodes, "statements", []) if hasattr(nodes, "statements") else nodes:
            if isinstance(stmt, LetDeclarationNode):
                emit(f"AayuValue _aayu_{stmt.name};\n")
            elif isinstance(stmt, TryNode):
                if getattr(stmt, "catch_var", None):
                    emit(f"AayuValue _aayu_{stmt.catch_var};\n")
                declare_globals(getattr(stmt, "try_block", []))
                declare_globals(getattr(stmt, "catch_block", []))
                declare_globals(getattr(stmt, "finally_block", []))
            elif isinstance(stmt, IfNode):
                declare_globals(getattr(stmt, "then_branch", []))
                declare_globals(getattr(stmt, "else_branch", []))
            elif isinstance(stmt, WhileNode):
                declare_globals(getattr(stmt, "body", []))

    if isinstance(ast, ProgramNode):
        declare_globals(ast.statements)

    # Pass 1: Actions
    for stmt in getattr(ast, "statements", []):
        if isinstance(stmt, ActionDeclarationNode):
            c_args = ", ".join([f"AayuValue _aayu_{arg}" for arg in getattr(stmt, "args", [])])
            if not c_args: c_args = "void" # No args C warning fix
            emit(f"AayuValue _aayu_fn_{stmt.name}({c_args}) {{\n")
            for b in stmt.statements:
                compile_stmt(b, 1, False)
            emit(f"    return make_null();\n")
            emit(f"}}\n\n")

    # --- MAIN COMPILATION ---
    emit("int main() {\n")
    if isinstance(ast, ProgramNode):
        for stmt in ast.statements:
            if not isinstance(stmt, ActionDeclarationNode):
                compile_stmt(stmt, 1, True)
            
    emit("    return 0;\n")
    emit("}\n")
    
    return "".join(output)

if __name__ == '__main__':
    import sys
    handle(sys.argv[1:])
