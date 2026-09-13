from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline

code = """
let x = 10
if true
    x = 20
else
    x = 30
end
print(x)
"""

lexer = Lexer(code)
ast = Parser(lexer.tokenize()).parse()
semantic_ast = SemanticAnalyzer().analyze(ast)

print(type(semantic_ast.statements[1].condition))
