import sys

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder
from runtime.vm.vm import VirtualMachine
from runtime.vm.config import VMConfig

def trace():
    source = """
state counter = 0
counter = counter + 5
"""
    print("=== 1. SOURCE ===")
    print(source.strip())
    
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    print("\n=== 2. TOKENS ===")
    for t in tokens:
        print(t)
        
    parser = Parser(tokens)
    ast = parser.parse()
    print("\n=== 3. AST ===")
    for stmt in ast.statements:
        print(vars(stmt))
        
    semantic = SemanticAnalyzer()
    sem_ast = semantic.analyze(ast)
    print("\n=== 4. SEMANTIC AST ===")
    for stmt in sem_ast.statements:
        print(vars(stmt))
        
    pipeline = IRPipeline()
    hir = pipeline.to_hir(sem_ast)
    print("\n=== 5. HIR ===")
    for node in hir:
        print(vars(node))
        
    mir = pipeline.to_mir(hir)
    print("\n=== 6. MIR ===")
    for node in mir:
        print(vars(node))
        
    lir = pipeline.to_lir(mir)
    print("\n=== 7. LIR ===")
    for node in lir:
        print(vars(node))
        
    encoder = BytecodeEncoder()
    program = encoder.encode(lir)
    print("\n=== 8. BYTECODE ===")
    print(f"Constant Pool: {program.constant_pool}")
    print("Hex:")
    # Print formatted hex (e.g. 01 00 00)
    hx = program.bytecode.hex()
    formatted_hex = " ".join(hx[i:i+2] for i in range(0, len(hx), 2))
    print(formatted_hex)
    
    print("\n=== 9. VM EXECUTION ===")
    vm = VirtualMachine(VMConfig.development())
    vm.load(program.bytecode, program.constant_pool)
    vm.execute()
    print("VM execution completed!")
    print("VM Heap length:", len(vm.heap.allocator.pool.pool))
    # Try to find the counter value in the VM state
    print("VM Registers:", vm.registers.__dict__)

if __name__ == "__main__":
    trace()
