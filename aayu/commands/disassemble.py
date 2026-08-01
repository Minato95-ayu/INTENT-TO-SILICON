import sys
import os

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.compiler.bytecode.disassembler import disassemble_with_header
from aayu.compiler.errors import CompilerError

def handle(args):
    target = args[0] if len(args) > 0 else "main.aayu"
    if not os.path.exists(target):
        print(f"Error: Target file {target} not found.")
        sys.exit(1)
        
    print(f"[AAYU] Disassembling {target}...\n")
    try:
        with open(target, 'r', encoding='utf-8') as f:
            source = f.read()
            
        # Compile through the full pipeline
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        semantic_ast = analyzer.analyze(ast)
        
        ir_pipeline = IRPipeline()
        hir = ir_pipeline.to_hir(semantic_ast)
        mir = ir_pipeline.to_mir(hir)
        lir = ir_pipeline.to_lir(mir)
        
        encoder = BytecodeEncoder()
        program = encoder.encode(lir)
        
        # Disassemble
        output = disassemble_with_header(
            program.bytecode,
            program.constant_pool.values(),
            program.header
        )
        print(output)
        
    except CompilerError as e:
        print(f"\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
