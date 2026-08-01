#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "loader.h"
#include "memory/arena.h"
#include "memory/manager.h"

AycProgram* load_ayc(const char* filepath) {
    AayuArena* arena = aayu_arena_create(ARENA_BLOCK_SIZE);
    FILE* f = fopen(filepath, "rb");
    if (!f) {
        printf("Error: Could not open file %s\n", filepath);
        return NULL;
    }

    char magic[4];
    fread(magic, 1, 4, f);
    if (strncmp(magic, "AAYU", 4) != 0) {
        printf("Error: Invalid AYC format (missing AAYU magic)\n");
        fclose(f);
        return NULL;
    }

    uint8_t version_major, version_minor;
    fread(&version_major, 1, 1, f);
    fread(&version_minor, 1, 1, f);

    AycProgram* temp_prog = (AycProgram*)aayu_arena_alloc(arena, sizeof(AycProgram));
    
    // Read Constant Pool
    fread(&temp_prog->cp_size, 4, 1, f);
    temp_prog->constants = (Constant*)aayu_arena_alloc(arena, sizeof(Constant) * temp_prog->cp_size);

    for (uint32_t i = 0; i < temp_prog->cp_size; i++) {
        uint8_t type_tag;
        fread(&type_tag, 1, 1, f);
        temp_prog->constants[i].type = (ConstType)type_tag;

        if (type_tag == TYPE_INT) {
            fread(&temp_prog->constants[i].value.i_val, 8, 1, f);
        } else if (type_tag == TYPE_FLOAT) {
            fread(&temp_prog->constants[i].value.f_val, 8, 1, f);
        } else if (type_tag == TYPE_STRING || type_tag == TYPE_DICT) {
            uint32_t len;
            fread(&len, 4, 1, f);
            char* str = (char*)aayu_arena_alloc(arena, len + 1);
            fread(str, 1, len, f);
            str[len] = '\0';
            temp_prog->constants[i].value.s_val = str;
        } else if (type_tag == TYPE_BOOL) {
            uint8_t b;
            fread(&b, 1, 1, f);
            temp_prog->constants[i].value.b_val = b;
        }
    }

    // Read Bytecode
    fread(&temp_prog->bc_size, 4, 1, f);
    temp_prog->bytecode = (uint8_t*)aayu_arena_alloc(arena, temp_prog->bc_size);
    fread(temp_prog->bytecode, 1, temp_prog->bc_size, f);

    fclose(f);
    
    // Build AycProgram (Deep Copy to Persistent Memory)
    AycProgram* prog = (AycProgram*)aayu_persistent_alloc(sizeof(AycProgram));
    prog->cp_size = temp_prog->cp_size;
    prog->bc_size = temp_prog->bc_size;
    
    prog->constants = (Constant*)aayu_persistent_alloc(sizeof(Constant) * prog->cp_size);
    for (uint32_t i = 0; i < prog->cp_size; i++) {
        prog->constants[i] = temp_prog->constants[i];
        if (prog->constants[i].type == TYPE_STRING || prog->constants[i].type == TYPE_DICT) {
            size_t len = strlen(temp_prog->constants[i].value.s_val);
            char* str = (char*)aayu_persistent_alloc(len + 1);
            memcpy(str, temp_prog->constants[i].value.s_val, len + 1);
            prog->constants[i].value.s_val = str;
        }
    }
    
    prog->bytecode = (uint8_t*)aayu_persistent_alloc(prog->bc_size);
    memcpy(prog->bytecode, temp_prog->bytecode, prog->bc_size);
    
    // Destroy temporary parsing arena immediately
    aayu_arena_destroy(arena);
    
    return prog;
}

void free_ayc(AycProgram* prog) {
    if (!prog) return;
    for (uint32_t i = 0; i < prog->cp_size; i++) {
        if (prog->constants[i].type == TYPE_STRING || prog->constants[i].type == TYPE_DICT) {
            aayu_persistent_free(prog->constants[i].value.s_val);
        }
    }
    aayu_persistent_free(prog->constants);
    aayu_persistent_free(prog->bytecode);
    aayu_persistent_free(prog);
}
