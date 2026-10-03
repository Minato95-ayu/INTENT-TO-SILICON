import sys
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder

with open("temp_math.aayu", "r", encoding="utf-8") as f:
    code = f.read()
if code.startswith('\ufeff'): code = code[1:]

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
analyzer = SemanticAnalyzer()
sem_ast = analyzer.analyze(ast)
pipeline = IRPipeline()
hir = pipeline.to_hir(sem_ast)
for h in hir:
    if "Action" in type(h).__name__:
        print(f"Action: {h.name}")
        for stmt in h.body:
            print("  ", stmt)
