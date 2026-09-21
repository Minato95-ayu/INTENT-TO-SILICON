from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder

with open('src/self_hosted/lexer.aayu', 'r') as f:
    code = f.read()

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
analyzer = SemanticAnalyzer()
sem_ast = analyzer.analyze(ast)
pipeline = IRPipeline()
hir = pipeline.to_hir(sem_ast)
mir = pipeline.to_mir(hir)
lir = pipeline.to_lir(mir)
encoder = BytecodeEncoder()
prog = encoder.encode(lir)
b = prog.bytecode

for ip in [561, 564, 567]:
    val = b[ip+1] | (b[ip+2] << 8)
    print(f"IP {ip} value: {val}")
