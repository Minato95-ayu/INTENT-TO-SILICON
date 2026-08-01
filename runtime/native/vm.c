#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "vm.h"
#include "memory/allocator.h"

void init_vm(VM* vm, AycProgram* prog) {
    vm->prog = prog;
    vm->ip = 0;
    vm->sp = -1;
    vm->call_sp = 0;
    vm->exception_sp = 0;
    memset(vm->state, 0, sizeof(vm->state));
}

static void push(VM* vm, Value v) {
    if (vm->sp >= STACK_MAX - 1) {
        printf("Error: Stack Overflow\n");
        exit(1);
    }
    vm->stack[++vm->sp] = v;
}

static Value pop(VM* vm) {
    if (vm->sp < 0) {
        printf("Error: Stack Underflow\n");
        exit(1);
    }
    return vm->stack[vm->sp--];
}

void run_vm(VM* vm) {
    uint8_t* bc = vm->prog->bytecode;
    uint32_t size = vm->prog->bc_size;

    while (vm->ip < size) {
        uint8_t opcode = bc[vm->ip];
        uint16_t operand = (bc[vm->ip + 1] << 8) | bc[vm->ip + 2];
        
        switch (opcode) {
            case OP_PUSH_CONST: {
                Constant c = vm->prog->constants[operand];
                Value v;
                v.type = c.type;
                if (c.type == TYPE_INT) v.value.i_val = c.value.i_val;
                else if (c.type == TYPE_FLOAT) v.value.f_val = c.value.f_val;
                else if (c.type == TYPE_STRING || c.type == TYPE_DICT) v.value.s_val = c.value.s_val;
                else if (c.type == TYPE_BOOL) v.value.b_val = c.value.b_val;
                push(vm, v);
                break;
            }
            case OP_POP: {
                pop(vm);
                break;
            }
            case OP_ADD:
            case OP_SUB:
            case OP_MUL:
            case OP_DIV: {
                Value b = pop(vm);
                Value a = pop(vm);
                Value res;
                if (a.type == TYPE_INT && b.type == TYPE_INT) {
                    res.type = TYPE_INT;
                    if (opcode == OP_ADD) res.value.i_val = a.value.i_val + b.value.i_val;
                    else if (opcode == OP_SUB) res.value.i_val = a.value.i_val - b.value.i_val;
                    else if (opcode == OP_MUL) res.value.i_val = a.value.i_val * b.value.i_val;
                    else if (opcode == OP_DIV) res.value.i_val = a.value.i_val / (b.value.i_val != 0 ? b.value.i_val : 1);
                } else if (a.type == TYPE_FLOAT || b.type == TYPE_FLOAT || a.type == TYPE_INT || b.type == TYPE_INT) {
                    res.type = TYPE_FLOAT;
                    double fa = a.type == TYPE_INT ? (double)a.value.i_val : a.value.f_val;
                    double fb = b.type == TYPE_INT ? (double)b.value.i_val : b.value.f_val;
                    if (opcode == OP_ADD) res.value.f_val = fa + fb;
                    else if (opcode == OP_SUB) res.value.f_val = fa - fb;
                    else if (opcode == OP_MUL) res.value.f_val = fa * fb;
                    else if (opcode == OP_DIV) res.value.f_val = fa / (fb != 0 ? fb : 1);
                }
                push(vm, res);
                break;
            }
            case OP_CMP_LT:
            case OP_CMP_GT:
            case OP_CMP_LTE:
            case OP_CMP_GTE:
            case OP_CMP_EQ:
            case OP_CMP_NEQ: {
                Value b = pop(vm);
                Value a = pop(vm);
                Value res;
                res.type = TYPE_BOOL;
                res.value.b_val = 0;
                
                double fa = a.type == TYPE_INT ? (double)a.value.i_val : (a.type == TYPE_FLOAT ? a.value.f_val : 0);
                double fb = b.type == TYPE_INT ? (double)b.value.i_val : (b.type == TYPE_FLOAT ? b.value.f_val : 0);
                
                if (opcode == OP_CMP_LT) res.value.b_val = fa < fb;
                else if (opcode == OP_CMP_GT) res.value.b_val = fa > fb;
                else if (opcode == OP_CMP_LTE) res.value.b_val = fa <= fb;
                else if (opcode == OP_CMP_GTE) res.value.b_val = fa >= fb;
                else if (opcode == OP_CMP_EQ) res.value.b_val = fa == fb;
                else if (opcode == OP_CMP_NEQ) res.value.b_val = fa != fb;
                
                push(vm, res);
                break;
            }
            case OP_PRINT: {
                Value v = pop(vm);
                if (v.type == TYPE_INT) printf("%lld\n", v.value.i_val);
                else if (v.type == TYPE_FLOAT) printf("%f\n", v.value.f_val);
                else if (v.type == TYPE_STRING || v.type == TYPE_DICT) printf("%s\n", v.value.s_val);
                else if (v.type == TYPE_BOOL) printf("%s\n", v.value.b_val ? "true" : "false");
                break;
            }
            case OP_CALL: {
                uint16_t target_addr = (bc[vm->ip + 1] << 8) | bc[vm->ip + 2];
                if (vm->call_sp >= 64) {
                    printf("Runtime Error: Call stack overflow\n");
                    exit(1);
                }
                vm->call_stack[vm->call_sp++] = vm->ip + 3;
                vm->ip = target_addr;
                continue;
            }
            case OP_RET: {
                if (vm->call_sp == 0) {
                    printf("Runtime Error: Call stack underflow\n");
                    exit(1);
                }
                vm->ip = vm->call_stack[--vm->call_sp];
                Value null_val;
                null_val.type = TYPE_INT; // Assuming NULL is handled or mapped
                null_val.value.i_val = 0;
                push(vm, null_val);
                continue;
            }
            case OP_RETURN_VALUE: {
                Value ret_val = pop(vm);
                if (vm->call_sp == 0) {
                    printf("Runtime Error: Call stack underflow on return\n");
                    exit(1);
                }
                vm->ip = vm->call_stack[--vm->call_sp];
                push(vm, ret_val);
                continue;
            }
            case OP_INIT_STATE:
            case OP_STORE_STATE: {
                Value v = pop(vm);
                vm->state[operand] = v;
                break;
            }
            case OP_LOAD_STATE: {
                push(vm, vm->state[operand]);
                break;
            }
            case OP_CREATE_ARRAY: {
                AayuArray* arr = (AayuArray*)aayu_alloc(sizeof(AayuArray), OBJ_ARRAY);
                arr->count = operand;
                arr->elements = (Value*)aayu_alloc_buffer(sizeof(Value) * operand)->data;
                for (int i = operand - 1; i >= 0; i--) {
                    arr->elements[i] = pop(vm);
                }
                Value arr_val;
                arr_val.type = TYPE_ARRAY;
                arr_val.value.obj = arr;
                push(vm, arr_val);
                break;
            }
            case OP_BUILD_DICT: {
                Value keys_val = pop(vm);
                int num_keys = 0;
                if (keys_val.value.s_val && strlen(keys_val.value.s_val) > 2) {
                    num_keys = 1;
                    for (char* p = keys_val.value.s_val; *p; p++) {
                        if (*p == ',') num_keys++;
                    }
                }
                AayuDict* dict = (AayuDict*)aayu_alloc(sizeof(AayuDict), OBJ_DICT);
                dict->count = num_keys;
                dict->entries = (DictPair*)aayu_alloc_buffer(sizeof(DictPair) * num_keys)->data;
                for (int i = num_keys - 1; i >= 0; i--) {
                    dict->entries[i].value = pop(vm);
                }
                if (num_keys > 0) {
                    char* s = strdup(keys_val.value.s_val);
                    int idx = 0;
                    char* token = strtok(s, "\"', ][");
                    while (token != NULL && idx < num_keys) {
                        dict->entries[idx].key = aayu_strdup(token);
                        idx++;
                        token = strtok(NULL, "\"', ][");
                    }
                    free(s);
                }
                Value dict_val;
                dict_val.type = TYPE_DICT;
                dict_val.value.obj = dict;
                push(vm, dict_val);
                break;
            }
            case OP_LOAD_SUBSCR: {
                Value index = pop(vm);
                Value target = pop(vm);
                if (target.type == TYPE_ARRAY && index.type == TYPE_INT) {
                    int i = index.value.i_val;
                    AayuArray* arr = (AayuArray*)target.value.obj;
                    if (i >= 0 && i < arr->count) {
                        push(vm, arr->elements[i]);
                    } else {
                        Value n; n.type = TYPE_NULL; push(vm, n);
                    }
                } else if (target.type == TYPE_DICT && index.type == TYPE_STRING) {
                    char* key = index.value.s_val;
                    AayuDict* dict = (AayuDict*)target.value.obj;
                    int found = 0;
                    for (int i = 0; i < dict->count; i++) {
                        if (strcmp(dict->entries[i].key, key) == 0) {
                            push(vm, dict->entries[i].value);
                            found = 1;
                            break;
                        }
                    }
                    if (!found) {
                        Value n; n.type = TYPE_NULL; push(vm, n);
                    }
                } else {
                    Value n; n.type = TYPE_NULL; push(vm, n);
                }
                break;
            }
            case OP_STORE_SUBSCR: {
                Value val = pop(vm);
                Value index = pop(vm);
                Value target = pop(vm);
                if (target.type == TYPE_ARRAY && index.type == TYPE_INT) {
                    int i = index.value.i_val;
                    AayuArray* arr = (AayuArray*)target.value.obj;
                    if (i >= 0 && i < arr->count) {
                        arr->elements[i] = val;
                    }
                } else if (target.type == TYPE_DICT && index.type == TYPE_STRING) {
                    char* key = index.value.s_val;
                    AayuDict* dict = (AayuDict*)target.value.obj;
                    for (int i = 0; i < dict->count; i++) {
                        if (strcmp(dict->entries[i].key, key) == 0) {
                            dict->entries[i].value = val;
                            break;
                        }
                    }
                }
                break;
            }
            case OP_JMP: {
                vm->ip = operand;
                continue; // Skip standard ip increment
            }
            case OP_JMP_IF_FALSE: {
                Value v = pop(vm);
                int is_false = 0;
                if (v.type == TYPE_BOOL && v.value.b_val == 0) is_false = 1;
                else if (v.type == TYPE_INT && v.value.i_val == 0) is_false = 1;
                
                if (is_false) {
                    vm->ip = operand;
                    continue;
                }
                break;
            }
            case OP_OP_ASYNC_CALL: {
                int num_args = operand;
                Value func_name = pop(vm);
                
                Value args[8];
                for (int i = num_args - 1; i >= 0; i--) {
                    args[i] = pop(vm);
                }
                
                Value result;
                result.type = TYPE_STRING;
                result.value.s_val = "";

                if (func_name.type == TYPE_STRING) {
                    if (strcmp(func_name.value.s_val, "fs.read") == 0) {
                        result.type = TYPE_STRING;
                        result.value.s_val = aayu_strdup("content");
                    } else if (strcmp(func_name.value.s_val, "http.get") == 0) {
                        result.type = TYPE_DICT;
                        AayuDict* dict = (AayuDict*)aayu_alloc(sizeof(AayuDict), OBJ_DICT);
                        dict->count = 1;
                        dict->entries = (DictPair*)aayu_alloc_buffer(sizeof(DictPair))->data;
                        dict->entries[0].key = aayu_strdup("status");
                        dict->entries[0].value.type = TYPE_STRING;
                        dict->entries[0].value.value.s_val = aayu_strdup("200");
                        result.value.obj = dict;
                    } else if (strcmp(func_name.value.s_val, "db.query") == 0) {
                        result.type = TYPE_ARRAY;
                        AayuArray* arr = (AayuArray*)aayu_alloc(sizeof(AayuArray), OBJ_ARRAY);
                        arr->count = 1;
                        arr->elements = (Value*)aayu_alloc_buffer(sizeof(Value))->data;
                        
                        AayuDict* dict = (AayuDict*)aayu_alloc(sizeof(AayuDict), OBJ_DICT);
                        dict->count = 1;
                        dict->entries = (DictPair*)aayu_alloc_buffer(sizeof(DictPair))->data;
                        dict->entries[0].key = aayu_strdup("name");
                        dict->entries[0].value.type = TYPE_STRING;
                        dict->entries[0].value.value.s_val = aayu_strdup("AAYU_USER");
                        
                        arr->elements[0].type = TYPE_DICT;
                        arr->elements[0].value.obj = dict;
                        
                        result.value.obj = arr;
                    } else {
                        result = func_name; 
                    }
                }
                
                push(vm, result);
                break;
            }
            case OP_SETUP_EXCEPT: {
                if (vm->exception_sp < 64) {
                    vm->exception_stack[vm->exception_sp].target_ip = operand;
                    vm->exception_stack[vm->exception_sp].sp = vm->sp;
                    vm->exception_sp++;
                }
                break;
            }
            case OP_POP_EXCEPT: {
                if (vm->exception_sp > 0) {
                    vm->exception_sp--;
                }
                break;
            }
            case OP_THROW: {
                Value v = pop(vm);
                if (vm->exception_sp > 0) {
                    vm->exception_sp--;
                    ExceptionHandler handler = vm->exception_stack[vm->exception_sp];
                    vm->sp = handler.sp;
                    push(vm, v); // Push exception object for the catch block
                    vm->ip = handler.target_ip;
                    continue;
                } else {
                    // Unhandled exception, just halt for now or print error
                    printf("Unhandled Exception: ");
                    if (v.type == TYPE_STRING) printf("%s\n", v.value.s_val);
                    else printf("<error object>\n");
                    return; // Halt
                }
            }
            case OP_HALT: {
                return;
            }
            default: {
                // Ignore unsupported opcodes for Phase 11A Core execution
                break;
            }
        }
        vm->ip += 3;
    }
}
