from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline

code = """action login(email, password)
    return "mock"
end"""
lexer = Lexer(code)
parser = Parser(lexer.tokenize())
ast = parser.parse()
analyzer = SemanticAnalyzer()
sem_ast = analyzer.analyze(ast)

node = sem_ast.statements[0].statements[0]
print("Semantic:", type(node))
print("Semantic Value:", type(node.value))

pipeline = IRPipeline()
hir = pipeline._semantic_to_hir(node)
print("HIR:", type(hir))
print("HIR Value:", type(hir.value))

print("Is HIRPrint:", type(hir.value).__name__ == "HIRPrint")
from aayu.compiler.ir.hir import HIRPrint
print("Isinstance HIRPrint:", isinstance(hir.value, HIRPrint))
