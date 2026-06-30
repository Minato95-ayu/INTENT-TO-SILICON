import sys
import os
import time
import tracemalloc
import io
import contextlib
import sqlite3

# Ensure we import from aayu_language directory
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "aayu_language"))

from lexer import Lexer
from parser import Parser
from compiler import AAYUCompiler
from vm import VirtualMachine
from serializer import serialize, deserialize
from interpreter import Interpreter

def cleanup_db():
    db_path = "aayu_db.sqlite"
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except Exception:
            pass

def run_ast_interpreter(filepath):
    cleanup_db()
    with open(filepath, 'r', encoding='utf-8') as f:
        source_code = f.read()
    
    lexer = Lexer(source_code)
    parser = Parser(lexer.tokenize(), filename=os.path.basename(filepath))
    ast = parser.parse()
    
    interpreter = Interpreter()
    try:
        # Redirect output to prevent cluttering benchmark results
        stdout_buffer = io.StringIO()
        with contextlib.redirect_stdout(stdout_buffer):
            interpreter.interpret(ast)
    finally:
        interpreter.db_conn.close()

def run_vm_otf(filepath):
    cleanup_db()
    with open(filepath, 'r', encoding='utf-8') as f:
        source_code = f.read()
        
    lexer = Lexer(source_code)
    parser = Parser(lexer.tokenize(), filename=os.path.basename(filepath))
    ast = parser.parse()
    
    compiler = AAYUCompiler()
    bytecode = compiler.compile(ast)
    
    vm = VirtualMachine()
    try:
        stdout_buffer = io.StringIO()
        with contextlib.redirect_stdout(stdout_buffer):
            vm.run(bytecode)
    finally:
        vm.close()
    return vm.instruction_count

def run_vm_ayc(filepath, ayc_path):
    # Compile first
    cleanup_db()
    with open(filepath, 'r', encoding='utf-8') as f:
        source_code = f.read()
    lexer = Lexer(source_code)
    parser = Parser(lexer.tokenize(), filename=os.path.basename(filepath))
    ast = parser.parse()
    compiler = AAYUCompiler()
    bytecode = compiler.compile(ast)
    
    with open(ayc_path, 'w', encoding='utf-8') as f:
        f.write(serialize(bytecode))
        
    # Now run serialized ayc
    cleanup_db()
    with open(ayc_path, 'r', encoding='utf-8') as f:
        serialized = f.read()
    bytecode_loaded = deserialize(serialized)
    
    vm_loaded = VirtualMachine()
    try:
        stdout_buffer = io.StringIO()
        with contextlib.redirect_stdout(stdout_buffer):
            vm_loaded.run(bytecode_loaded)
    finally:
        vm_loaded.close()
    return vm_loaded.instruction_count

def benchmark_category(name, filepath, ayc_path):
    print(f"Benchmarking category: {name}...")
    
    # 1. AST Interpreter
    tracemalloc.start()
    start_time = time.perf_counter()
    run_ast_interpreter(filepath)
    end_time = time.perf_counter()
    _, peak_ast = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    ast_time = (end_time - start_time) * 1000 # ms
    ast_mem = peak_ast / 1024 # KB
    
    # 2. VM On-the-fly
    tracemalloc.start()
    start_time = time.perf_counter()
    vm_otf_instr = run_vm_otf(filepath)
    end_time = time.perf_counter()
    _, peak_otf = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    otf_time = (end_time - start_time) * 1000 # ms
    otf_mem = peak_otf / 1024 # KB
    
    # 3. VM Loaded (.ayc)
    tracemalloc.start()
    start_time = time.perf_counter()
    vm_ayc_instr = run_vm_ayc(filepath, ayc_path)
    end_time = time.perf_counter()
    _, peak_ayc = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    ayc_time = (end_time - start_time) * 1000 # ms
    ayc_mem = peak_ayc / 1024 # KB
    
    # Clean up generated .ayc file
    if os.path.exists(ayc_path):
        try:
            os.remove(ayc_path)
        except Exception:
            pass
            
    return {
        "ast": {"time": ast_time, "mem": ast_mem},
        "otf": {"time": otf_time, "mem": otf_mem, "instr": vm_otf_instr},
        "ayc": {"time": ayc_time, "mem": ayc_mem, "instr": vm_ayc_instr}
    }

def main():
    tests_dir = os.path.dirname(__file__)
    
    benchmarks = [
        ("CPU (Fibonacci)", os.path.join(tests_dir, "vm_fib.aayu"), os.path.join(tests_dir, "vm_fib.ayc")),
        ("Collections (List/Map)", os.path.join(tests_dir, "vm_collections.aayu"), os.path.join(tests_dir, "vm_collections.ayc")),
        ("Database (CRUD)", os.path.join(tests_dir, "vm_db.aayu"), os.path.join(tests_dir, "vm_db.ayc"))
    ]
    
    results = {}
    for name, filepath, ayc_path in benchmarks:
        results[name] = benchmark_category(name, filepath, ayc_path)
        
    cleanup_db()
    
    print("\n" + "="*80)
    print("                      AAYU RUNTIME BENCHMARK RESULTS                      ")
    print("="*80)
    
    # Print as a nice table
    print(f"{'Category':<22} | {'Runner':<15} | {'Time (ms)':<10} | {'Memory (KB)':<12} | {'Instructions':<12}")
    print("-"*80)
    
    for category, metrics in results.items():
        ast = metrics["ast"]
        otf = metrics["otf"]
        ayc = metrics["ayc"]
        
        print(f"{category:<22} | {'AST Interpreter':<15} | {ast['time']:<10.2f} | {ast['mem']:<12.2f} | {'N/A':<12}")
        print(f"{'':<22} | {'VM (On-the-fly)':<15} | {otf['time']:<10.2f} | {otf['mem']:<12.2f} | {otf['instr']:<12}")
        print(f"{'':<22} | {'VM (.ayc JSON)':<15} | {ayc['time']:<10.2f} | {ayc['mem']:<12.2f} | {ayc['instr']:<12}")
        print("-"*80)
        
        # Calculate speedup
        speedup_otf = ast['time'] / otf['time'] if otf['time'] > 0 else 0
        speedup_ayc = ast['time'] / ayc['time'] if ayc['time'] > 0 else 0
        print(f"OTF VM Speedup: {speedup_otf:.2f}x | .ayc VM Speedup: {speedup_ayc:.2f}x")
        print("="*80)

if __name__ == "__main__":
    main()
