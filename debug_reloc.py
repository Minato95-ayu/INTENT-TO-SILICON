from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.ir.optimizer import SSAOptimizer
from compiler.ir.linearizer import Linearizer
from compiler.bytecode.encoder import BytecodeEncoder

code = """
action test()
    return 42
    print(999)
end
let a = test()
print(a)
"""

lexer = Lexer(code)
ast = Parser(lexer.tokenize()).parse()
semantic_ast = SemanticAnalyzer().analyze(ast)

pipeline = IRPipeline()
cfg = pipeline.to_ssa_cfg(semantic_ast)
SSAOptimizer(cfg).optimize()
mir = Linearizer(cfg).lower()
lir = pipeline.to_lir(mir)
encoder = BytecodeEncoder()
prog = encoder.encode(lir)

print(encoder._action_addresses)
print(encoder.relocations)
