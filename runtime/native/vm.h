#ifndef AAYU_VM_H
#define AAYU_VM_H

#include "loader.h"
#include "opcodes.h"

#define STACK_MAX 2048
#define STATE_MAX 1024

typedef struct sAayuObject AayuObject;

typedef struct sValue {
    ConstType type;
    union {
        int64_t i_val;
        double f_val;
        char* s_val;
        int b_val;
        AayuObject* obj; // Generic pointer to heap-allocated object
    } value;
} Value;

#include "memory/object.h"


typedef struct {
    uint32_t target_ip;
    int sp;
} ExceptionHandler;

typedef struct {
    AycProgram* prog;
    uint32_t ip; // Instruction pointer
    Value stack[STACK_MAX];
    int sp;      // Stack pointer

    uint32_t call_stack[64];
    int call_sp;
    
    ExceptionHandler exception_stack[64];
    int exception_sp;

    // Global state map (simple array of values since constant pool indexes are used as variable identifiers conceptually, or string indexing)
    // For simplicity, we just use an array indexed by constant pool string index
    Value state[STATE_MAX];
} VM;

void init_vm(VM* vm, AycProgram* prog);
void run_vm(VM* vm);

#endif
