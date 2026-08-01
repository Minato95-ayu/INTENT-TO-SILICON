#include <stdio.h>
#include <stdlib.h>
#include "loader.h"
#include "vm.h"
#include "memory/manager.h"

int main(int argc, char** argv) {
    if (argc < 2) {
        printf("Usage: aayu-runtime <file.aybc>\n");
        return 1;
    }

    aayu_memory_init();

    AycProgram* prog = load_ayc(argv[1]);
    if (!prog) {
        aayu_memory_destroy();
        return 1;
    }

    VM vm;
    init_vm(&vm, prog);
    
    run_vm(&vm);
    
    free_ayc(prog);
    aayu_memory_destroy();
    return 0;
}
