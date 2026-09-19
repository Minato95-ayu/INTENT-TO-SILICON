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
from runtime.vm.instructions import opcode_to_str

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
"""

tokens = Lexer(code).tokenize()
ast = Parser(tokens).parse()
sast = SemanticAnalyzer().analyze(ast)
pipe = IRPipeline()
hir = pipe.to_hir(sast)
mir = pipe.to_mir(hir)
lir = pipe.to_lir(mir)
prog = BytecodeEncoder().encode(lir)

for ip, b in enumerate(prog.bytecode):
    if b < 50:
        print(f"[{ip}] {b} ({opcode_to_str(b)})")
    else:
        print(f"[{ip}] {b}")

