import sys, os
sys.path.insert(0, os.path.abspath('.'))
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder

source = '''
action main()
    data = HTTP.post("https://httpbin.org/post", {name: "AAYU", goal: "Intent-to-Silicon"})
    print(data)
end
'''
tokens = Lexer(source).tokenize()
ast = Parser(tokens).parse()
sem = SemanticAnalyzer().analyze(ast)
pipe = IRPipeline()
prog = BytecodeEncoder().encode(pipe.to_lir(pipe.to_mir(pipe.to_hir(sem))))

for idx in range(0, len(prog.bytecode), 3):
    opcode = prog.bytecode[idx]
    print(f'[{idx}] {hex(opcode)}')
