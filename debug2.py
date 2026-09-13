from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.ir.optimizer import SSAOptimizer
from compiler.ir.linearizer import Linearizer
from compiler.bytecode.encoder import BytecodeEncoder

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

pipeline = IRPipeline()
cfg = pipeline.to_ssa_cfg(semantic_ast)
SSAOptimizer(cfg).optimize()
mir = Linearizer(cfg).lower()
for inst in mir:
    print(inst.opcode, inst.operands)
