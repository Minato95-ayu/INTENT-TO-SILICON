import sys
import os
import time
import tracemalloc

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from aayu.compiler.semantic.types import (
    Type, PrimitiveType, UnionType, OptionalType, make_nullable,
    T_INT, T_FLOAT, T_STRING, T_BOOL, T_CHAR, T_BYTE, T_VOID, T_NEVER, T_ANY, T_NULL
)

def benchmark_resolution(count):
    # Setup
    types_list = []
    for i in range(count):
        # Create a deep union nesting for worst-case checks
        t = UnionType(T_INT, OptionalType(UnionType(T_STRING, T_FLOAT)))
        types_list.append(t)
        
    target = UnionType(T_INT, T_STRING, T_FLOAT, OptionalType(UnionType(T_STRING, T_FLOAT)))
    
    # Trace Memory
    tracemalloc.start()
    start_time = time.time()
    
    # Run assignability checks
    for t in types_list:
        t.is_assignable_to(target)
        
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    elapsed_ms = (end_time - start_time) * 1000
    peak_kb = peak / 1024
    
    print(f"| {count:<7} | {elapsed_ms:<8.2f} ms | {peak_kb:<10.2f} KB |")

def run_benchmarks():
    print("## Benchmark: Assignability Check Scale")
    print("| Count   | Time         | Peak Memory   |")
    print("|---------|--------------|---------------|")
    
    for scale in [10, 100, 1000, 10000, 100000]:
        benchmark_resolution(scale)

if __name__ == "__main__":
    run_benchmarks()
