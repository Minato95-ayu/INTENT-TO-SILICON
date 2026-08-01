import os
from distutils.ccompiler import new_compiler
from distutils.sysconfig import customize_compiler

def build():
    compiler = new_compiler()
    customize_compiler(compiler)
    
    sources = [
        "tests/native/test_arena.c", 
        "runtime/native/memory/arena.c", 
        "runtime/native/memory/os_mem.c", 
        "runtime/native/memory/manager.c", 
        "runtime/native/memory/allocator.c"
    ]
    print("Compiling test_arena sources...")
    objs = compiler.compile(sources)
    
    print("Linking test_arena executable...")
    compiler.link_executable(objs, "test_arena", output_dir="tests/native")
    print("Build successful.")

if __name__ == "__main__":
    build()
