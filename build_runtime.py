import os
import sys
from distutils.ccompiler import new_compiler
from distutils.sysconfig import customize_compiler

def build():
    compiler = new_compiler()
    customize_compiler(compiler)
    
    sources = ["runtime/native/main.c", "runtime/native/vm.c", "runtime/native/loader.c", "runtime/native/memory/allocator.c", "runtime/native/memory/os_mem.c", "runtime/native/memory/arena.c", "runtime/native/memory/manager.c", "runtime/native/memory/visitor.c", "runtime/native/memory/gc.c"]
    print("Compiling sources...")
    objs = compiler.compile(sources)
    
    print("Linking executable...")
    compiler.link_executable(objs, "aayu-runtime", output_dir="runtime/native")
    print("Build successful.")

if __name__ == "__main__":
    build()
