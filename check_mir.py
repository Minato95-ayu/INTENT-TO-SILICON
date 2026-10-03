import sys
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder

with open("test_child3.aayu", "r", encoding="utf-8") as f:
    code = f.read()

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
analyzer = SemanticAnalyzer()
sem_ast = analyzer.analyze(ast)
pipeline = IRPipeline()
hir = pipeline.to_hir(sem_ast)
mir = []
for h in hir:
    pipeline._hir_to_mir(h, mir)
for m in mir:
    if m.opcode == "ACTION_DECL":
        print(f"Action: {m.operands[0]}")
        for stmt in m.operands[1]:
            print("  ", stmt.opcode, stmt.operands)
