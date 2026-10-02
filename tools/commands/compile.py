import os
import sys

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder

def handle(args):
    if not args:
        print("Usage: aayu compile <file.aayu>")
        sys.exit(1)
        
    filename = args[0]
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
        
    # Read the source code
    with open(filename, 'r', encoding='utf-8') as f:
        source = f.read()
        
    print(f"Compiling {filename} to native bytecode...")
    
    # 1. Lexing
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    
    # 2. Parsing
    parser = Parser(tokens)
    ast = parser.parse()
    
    # 3. Semantic Analysis
    analyzer = SemanticAnalyzer()
    semantic_ast = analyzer.analyze(ast)
    
    # 4. IR Pipeline
    pipeline = IRPipeline()
    from compiler.semantic.type_inference import TypeInference
    semantic_ast = TypeInference().infer(semantic_ast)
    from compiler.semantic.type_checker import TypeChecker
    TypeChecker().check(semantic_ast)
    ir_ast = pipeline.to_lir(pipeline.to_mir(pipeline.to_hir(semantic_ast)))
    
    # 5. Bytecode Encoding
    encoder = BytecodeEncoder()
    bytecode_tuple = encoder.encode(ir_ast)
    
    # AAYU encode() returns a tuple with bytearray in the first element and actions dict in second
    if isinstance(bytecode_tuple, tuple):
        bytecode = bytecode_tuple[0]
    else:
        bytecode = bytecode_tuple
        
    out_filename = filename.replace('.aayu', '.aybc')
    
    with open(out_filename, 'wb') as f:
        f.write(bytecode.bytecode if hasattr(bytecode, 'bytecode') else bytecode)
        
    print(f"Success! Bytecode saved to {out_filename}")
    print(f"File size: {os.path.getsize(out_filename)} bytes")
    print(f"Ready for Rust VM.")
