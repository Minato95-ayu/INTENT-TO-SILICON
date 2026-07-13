import sys
import os

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder
from compiler.errors import CompilerError
from runtime.vm.vm import VirtualMachine

def handle(args):
    target = args[0] if len(args) > 0 else "main.aayu"
    if not os.path.exists(target):
        print(f"Error: Target file {target} not found.")
        sys.exit(1)
        
    print(f"[AAYU] Running {target}...")
    try:
        with open(target, 'r', encoding='utf-8') as f:
            source = f.read()
            
        # Stage 1: Lexing
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Stage 2: Parsing
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Stage 3: Semantic Analysis
        analyzer = SemanticAnalyzer()
        semantic_ast = analyzer.analyze(ast)
        
        # Stage 4: IR Lowering (HIR → MIR → LIR)
        ir_pipeline = IRPipeline()
        hir = ir_pipeline.to_hir(semantic_ast)
        mir = ir_pipeline.to_mir(hir)
        lir = ir_pipeline.to_lir(mir)
        
        # Stage 5: Bytecode Encoding (LIR → Binary)
        encoder = BytecodeEncoder()
        program = encoder.encode(lir)
        
        # Stage 6: VM Execution
        vm = VirtualMachine()
        vm.load(program.bytecode, program.constant_pool.values())
        vm.execute()
        
        print("[AAYU] Execution completed successfully.")
        
    except CompilerError as e:
        print(f"\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nRuntime Error: {e}")
        sys.exit(1)
