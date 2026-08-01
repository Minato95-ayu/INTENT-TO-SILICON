from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder

with open('benchmarks/aayu_app/src/app.aayu', 'r') as f:
    src=f.read()
    
ast=Parser(Lexer(src).tokenize()).parse()
sem=SemanticAnalyzer().analyze(ast)
mir=IRPipeline().to_mir(IRPipeline().to_hir(sem))
program = BytecodeEncoder().encode(IRPipeline().to_lir(mir))
print('action addresses:', program.action_addresses)
if hasattr(program, 'action_params'):
    print('action params:', program.action_params)
else:
    print('no action params')
