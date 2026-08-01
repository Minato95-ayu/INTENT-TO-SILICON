from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline

code = """action login(email, password)
    if email == "bench@test.com"
        if password == "password"
            return "mock_token_12345"
        end
    end
end"""
lexer = Lexer(code)
parser = Parser(lexer.tokenize())
ast = parser.parse()
analyzer = SemanticAnalyzer()
sem_ast = analyzer.analyze(ast)
pipeline = IRPipeline()
hir = pipeline.to_hir(sem_ast)
mir = pipeline.to_mir(hir)
for m in mir:
    print(f"MIR: {m.opcode} {m.operands}")
