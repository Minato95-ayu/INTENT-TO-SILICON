import sys, os
sys.path.insert(0, os.path.abspath('.'))
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline

source = '''
action main()
    storage.set("name", "AAYU")
    name = storage.get("name")
    print(name)
end
'''
tokens = Lexer(source).tokenize()
ast = Parser(tokens).parse()
sem = SemanticAnalyzer().analyze(ast)
pipe = IRPipeline()
hir = pipe.to_hir(sem)
mir = pipe.to_mir(hir)
lir = pipe.to_lir(mir)
for l in lir:
    print(l)
