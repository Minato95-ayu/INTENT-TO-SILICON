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
cfg = IRPipeline().to_ssa_cfg(semantic_ast)

for b in cfg.blocks:
    print(f"Block: {b.id}")
    for inst in b.instructions:
        print(f"  {inst.opcode} {inst.operands}")
