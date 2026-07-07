"""
=============================================================================
FILE: benchmark.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import sys
import os
import time
import tracemalloc
import io
import contextlib

sys.path.append(r"D:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\aayu_language")

from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler
from vm import VirtualMachine
from serializer import serialize, deserialize
from run import run_file

filepath = r"D:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\tests\vm_fib.aayu"
ayc_filepath = r"D:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\tests\vm_fib.ayc"

print("=========================================")
print("          AAYU RUNTIME BENCHMARK         ")
print("=========================================\n")

# 1. AST Interpreter
print("[1] Running AST Interpreter...")
tracemalloc.start()
start_time = time.perf_counter()

stdout_buffer = io.StringIO()
with contextlib.redirect_stdout(stdout_buffer):
    run_file(filepath)
    
end_time = time.perf_counter()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

ast_time = (end_time - start_time) * 1000  # ms
ast_mem = peak / 1024  # KB
ast_output = stdout_buffer.getvalue().strip()

print(f"    Time: {ast_time:.2f} ms")
print(f"    Peak Memory: {ast_mem:.2f} KB")
print(f"    Output: {ast_output}")

# 2. Python VM (On-The-Fly Compilation & Run)
print("\n[2] Running Python VM (On-the-fly compilation)...")
tracemalloc.start()
start_time = time.perf_counter()

with open(filepath, 'r', encoding='utf-8') as f:
    source = f.read()

lexer = Lexer(source)
parser = Parser(lexer.tokenize(), filename=filepath)
ast = parser.parse()

compiler = AAYUCompiler()
bytecode = compiler.compile(ast)

vm = VirtualMachine()
stdout_buffer = io.StringIO()
with contextlib.redirect_stdout(stdout_buffer):
    vm.run(bytecode)
    
end_time = time.perf_counter()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

vm_otf_time = (end_time - start_time) * 1000  # ms
vm_otf_mem = peak / 1024  # KB
vm_otf_instr = vm.instruction_count
vm_otf_output = stdout_buffer.getvalue().strip()

print(f"    Time: {vm_otf_time:.2f} ms")
print(f"    Peak Memory: {vm_otf_mem:.2f} KB")
print(f"    Instructions Executed: {vm_otf_instr}")
print(f"    Output: {vm_otf_output}")

# 3. Compile first to .ayc
print("\nCompiling to .ayc for serialized VM test...")
with open(ayc_filepath, 'w', encoding='utf-8') as f:
    f.write(serialize(bytecode))

# 4. .ayc VM (Direct loader and execution)
print("[3] Running .ayc VM (Direct JSON loader)...")
tracemalloc.start()
start_time = time.perf_counter()

with open(ayc_filepath, 'r', encoding='utf-8') as f:
    serialized = f.read()
bytecode_loaded = deserialize(serialized)

vm_loaded = VirtualMachine()
stdout_buffer = io.StringIO()
with contextlib.redirect_stdout(stdout_buffer):
    vm_loaded.run(bytecode_loaded)
    
end_time = time.perf_counter()
current, peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

vm_ayc_time = (end_time - start_time) * 1000  # ms
vm_ayc_mem = peak / 1024  # KB
vm_ayc_instr = vm_loaded.instruction_count
vm_ayc_output = stdout_buffer.getvalue().strip()

print(f"    Time: {vm_ayc_time:.2f} ms")
print(f"    Peak Memory: {vm_ayc_mem:.2f} KB")
print(f"    Instructions Executed: {vm_ayc_instr}")
print(f"    Output: {vm_ayc_output}")

print("\n=========================================")
print("               COMPARISON                ")
print("=========================================")
print(f"AST Interpreter:      {ast_time:7.2f} ms | Peak Memory: {ast_mem:7.2f} KB")
print(f"Python VM (On-the-fly):{vm_otf_time:7.2f} ms | Peak Memory: {vm_otf_mem:7.2f} KB | Instrs: {vm_otf_instr}")
print(f"Python VM (.ayc JSON): {vm_ayc_time:7.2f} ms | Peak Memory: {vm_ayc_mem:7.2f} KB | Instrs: {vm_ayc_instr}")
print("=========================================")
