import sys
import io

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.ir.optimizer import SSAOptimizer
from compiler.ir.linearizer import Linearizer
from compiler.bytecode.encoder import BytecodeEncoder
from runtime.session.manager import SessionManager

code = """
let result = 0
if true
    if false
        result = 100
    else
        result = 200
    end
else
    result = 300
end
print(result)
"""

print("Lexing/Parsing...")
lexer = Lexer(code)
ast = Parser(lexer.tokenize()).parse()
print("Semantic...")
semantic_ast = SemanticAnalyzer().analyze(ast)

print("Pipeline...")
pipeline = IRPipeline()
cfg = pipeline.to_ssa_cfg(semantic_ast)
SSAOptimizer(cfg).optimize()
mir = Linearizer(cfg).lower()
lir = pipeline.to_lir(mir)
prog = BytecodeEncoder().encode(lir)

print("Program length:", len(prog.instructions))
for i, instr in enumerate(prog.instructions):
    print(i, instr)

print("Starting VM...")
manager = SessionManager(prog)
session = manager.get_or_create_session("test-session")
try:
    session.vm.execute()
except Exception as e:
    print("Error:", e)
print("Finished!")
