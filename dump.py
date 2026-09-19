# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder

code = """
model BenchmarkUser {
    username: String
    score: Int
}

let i = 0
while i < 100
    insert BenchmarkUser { username = "User" score = i }
    i = i + 1
end

let users = find BenchmarkUser
print(i)
"""

tokens = Lexer(code).tokenize()
ast = Parser(tokens).parse()
sast = SemanticAnalyzer().analyze(ast)
pipe = IRPipeline()
hir = pipe.to_hir(sast)
mir = pipe.to_mir(hir)
lir = pipe.to_lir(mir)
prog = BytecodeEncoder().encode(lir)

for i, inst in enumerate(prog.instructions):
    print(f"idx={i} {inst}")

from runtime.vm.instructions import opcode_to_str
ip = 0
while ip < len(prog.bytecode):
    op = prog.bytecode[ip]
    print(f"{ip}: {opcode_to_str(op)}")
    if op in (1, 2, 4, 15, 17, 23, 24, 25, 26, 27, 28, 29, 31, 32, 33, 34, 38): # with 1 byte operand
        ip += 3 # wait, most are 2 bytes operand!
    elif op in (5, 6): # jump
        ip += 3
    else:
        ip += 1
