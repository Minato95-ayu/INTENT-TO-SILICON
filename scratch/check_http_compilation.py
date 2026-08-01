import sys, os
sys.path.insert(0, os.path.abspath('.'))
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder

source = '''
action myaction()
    HTTP.post("url")
end
'''
try:
    tokens = Lexer(source).tokenize()
    ast = Parser(tokens).parse()
    sem = SemanticAnalyzer().analyze(ast)
    pipe = IRPipeline()
    prog = BytecodeEncoder().encode(pipe.to_lir(pipe.to_mir(pipe.to_hir(sem))))
    print('Action addresses:', prog.action_addresses)
    for i, inst in enumerate(prog.bytecode):
        print(f"[{i:04d}] {inst}")
except Exception as e:
    import traceback
    traceback.print_exc()
