import os
import sys
from distutils.ccompiler import new_compiler
from distutils.sysconfig import customize_compiler
import subprocess

def build_test():
    compiler = new_compiler()
    customize_compiler(compiler)
    
    sources = ["tests/native/test_allocator.c", "runtime/native/memory/allocator.c", "runtime/native/memory/os_mem.c"]
    print("Compiling sources...")
    objs = compiler.compile(sources)
    
    print("Linking executable...")
    compiler.link_executable(objs, "test_allocator", output_dir="build/tests")
    print("Build successful.")
    
    print("\nRunning tests...")
    subprocess.run(["build/tests/test_allocator.exe"], check=True)

if __name__ == "__main__":
    build_test()
