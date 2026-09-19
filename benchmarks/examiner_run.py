# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import os
import time
import sys
import contextlib
import io
import traceback

# Add root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder
from runtime.session.manager import SessionManager

def execute_aayu(source_code):
    try:
        tokens = Lexer(source_code).tokenize()
        ast = Parser(tokens).parse()
        semantic_ast = SemanticAnalyzer().analyze(ast)
        
        # Compile
        pipeline = IRPipeline()
        hir = pipeline.to_hir(semantic_ast)
        mir = pipeline.to_mir(hir)
        lir = pipeline.to_lir(mir)
        
        prog = BytecodeEncoder().encode(lir)
        
        # Execute
        manager = SessionManager(prog)
        session = manager.get_or_create_session("bench-session")
        
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            session.vm.execute()
            
        # Ignore output
        return True, None
    except Exception as e:
        traceback.print_exc()
        return False, str(e)

def run_benchmark(file_path):
    print(f"--- Running Benchmark: {os.path.basename(file_path)} ---")
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
    
    mem_before = 0
    start_time = time.time()
    
    success, err = execute_aayu(source)
    
    end_time = time.time()
    mem_after = 0
    
    elapsed_ms = (end_time - start_time) * 1000
    mem_used_kb = (mem_after - mem_before) / 1024.0
    
    if success:
        print(f"[PASS] Execution Time: {elapsed_ms:.2f} ms")
        print(f"[PASS] Memory Delta:   {mem_used_kb:.2f} KB\n")
    else:
        print(f"[FAIL] Error: {err}\n")

if __name__ == "__main__":
    benchmarks = [
        "benchmarks/01_compute_stress.aayu",
        "benchmarks/02_data_crunching.aayu",
        "benchmarks/03_server_mock.aayu",
        "benchmarks/04_ui_render.aayu",
        "benchmarks/mega_test.aayu"
    ]
    for b in benchmarks:
        if os.path.exists(b):
            run_benchmark(b)
        else:
            print(f"Skipping {b} (not found)")
