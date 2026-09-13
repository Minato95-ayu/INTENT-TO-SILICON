from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline

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

for inst in cfg.entry_block.instructions:
    print(inst.opcode)
