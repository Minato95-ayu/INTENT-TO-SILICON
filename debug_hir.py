from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
code = """
action test()
    return 42
end
"""
lexer = Lexer(code)
ast = Parser(lexer.tokenize()).parse()
sem = SemanticAnalyzer().analyze(ast)
hir = IRPipeline().to_hir(sem)
print(hir[0].body[0])
