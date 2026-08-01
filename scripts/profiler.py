import time
import os
import psutil
import sys

# Append root to path so we can import AAYU compiler and runtime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.optimizer.optimizer import Optimizer
from aayu.compiler.bytecode.generator import BytecodeGenerator

from aayu.runtime.kernel.core import RuntimeKernel
from aayu.runtime.vm.vm import VirtualMachine
from aayu.runtime.plugins.state.runtime import StateRuntime

def profile_file(filepath):
    print(f"\n--- Profiling: {os.path.basename(filepath)} ---")
    
    with open(filepath, 'r') as f:
        code = f.read()

    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss
    cpu_before = process.cpu_percent()
    
    # 1. Compile Time Profiling
    start_compile = time.time()
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        semantic = SemanticAnalyzer()
        semantic_ast = semantic.analyze(ast)
        
        ir_pipeline = IRPipeline()
        hir = ir_pipeline.to_hir(semantic_ast)
        mir = ir_pipeline.to_mir(hir)
        lir = ir_pipeline.to_lir(mir)
        
        optimizer = Optimizer()
        optimized_lir = lir # Bypass passes for raw speed test or include them
        
        generator = BytecodeGenerator()
        bytecode = generator.generate(optimized_lir)
        
    except Exception as e:
        print(f"Compilation Error (Parser not fully implemented for this syntax): {e}")
        print("Falling back to profiling a minimal test payload for pipeline metrics...")
        code = "state x = 42\npage Home\ntext \"Hello\"\nend"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        semantic = SemanticAnalyzer()
        semantic_ast = semantic.analyze(ast)
        ir_pipeline = IRPipeline()
        hir = ir_pipeline.to_hir(semantic_ast)
        mir = ir_pipeline.to_mir(hir)
        lir = ir_pipeline.to_lir(mir)
        generator = BytecodeGenerator()
        bytecode = generator.generate(lir)
    
    compile_time = time.time() - start_compile
    
    # Bytecode Size
    import pickle
    bytecode_size = len(pickle.dumps(bytecode))
    
    # 2. Startup Time Profiling
    start_startup = time.time()
    
    kernel = RuntimeKernel()
    state = StateRuntime()
    kernel.registry.register(state)
    vm = VirtualMachine(kernel)
    
    startup_time = time.time() - start_startup
    
    # 3. Frame/Execution Time Profiling
    start_exec = time.time()
    vm.execute(bytecode)
    exec_time = time.time() - start_exec
    
    # Resource Usage
    mem_after = process.memory_info().rss
    cpu_after = process.cpu_percent()
    mem_used = (mem_after - mem_before) / (1024 * 1024) # MB
    
    print(f"Compile Time : {compile_time * 1000:.2f} ms")
    print(f"Bytecode Size: {bytecode_size} bytes")
    print(f"Startup Time : {startup_time * 1000:.2f} ms")
    print(f"Execution    : {exec_time * 1000:.2f} ms")
    print(f"Memory Used  : {mem_used:.2f} MB")
    print(f"CPU Spike    : {cpu_after - cpu_before:.1f}%")

if __name__ == '__main__':
    # Profile a few apps
    apps_dir = os.path.join(os.path.dirname(__file__), '..', 'examples', 'apps')
    apps_to_profile = ['calculator.aayu', 'ecommerce.aayu', 'ide.aayu', 'mini_os_ui.aayu']
    
    for app in apps_to_profile:
        filepath = os.path.join(apps_dir, app)
        if os.path.exists(filepath):
            profile_file(filepath)
        else:
            print(f"File not found: {filepath}")
