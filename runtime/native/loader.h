#ifndef AAYU_LOADER_H
#define AAYU_LOADER_H

#include <stdint.h>

typedef enum {
    TYPE_INT = 0,
    TYPE_FLOAT = 1,
    TYPE_STRING = 2,
    TYPE_BOOL = 3,
    TYPE_DICT = 4,
    TYPE_ARRAY = 5,
    TYPE_NULL = 6
} ConstType;

typedef struct {
    ConstType type;
    union {
        int64_t i_val;
        double f_val;
        char* s_val;
        int b_val;
    } value;
} Constant;

typedef struct {
    uint32_t cp_size;
    Constant* constants;
    uint32_t bc_size;
    uint8_t* bytecode;
} AycProgram;

AycProgram* load_ayc(const char* filepath);
void free_ayc(AycProgram* prog);

#endif
