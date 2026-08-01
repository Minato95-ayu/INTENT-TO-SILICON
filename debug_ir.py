import sys
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.ast_resolver import resolve_ast_imports
from aayu.compiler.semantic.type_inference import TypeInference
from aayu.compiler.semantic.type_checker import TypeChecker

with open("tests/conformance/013_modules.aayu", "r") as f:
    source = f.read()

lexer = Lexer(source)
parser = Parser(lexer.tokenize())
ast = parser.parse()
semantic_ast = SemanticAnalyzer().analyze(ast)
ir_pipeline = IRPipeline()

hir = ir_pipeline.to_hir(semantic_ast)
print("HIR:", hir)
mir = ir_pipeline.to_mir(hir)
print("MIR:")
for m in mir:
    print(m)
lir = ir_pipeline.to_lir(mir)
print("LIR:")
for l in lir:
    print(l)
