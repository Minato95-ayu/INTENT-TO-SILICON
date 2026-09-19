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

import sys
sys.path.insert(0, '.')
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.ir.linearizer import Linearizer
from compiler.ir.optimizer import SSAOptimizer
from compiler.bytecode.encoder import BytecodeEncoder
from runtime.vm.instructions import opcode_to_str

code = """
try
    print("normal")
catch (e)
    print("caught")
end
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

for i in range(0, len(prog.bytecode), 3):
    op = prog.bytecode[i]
    arg = (prog.bytecode[i+1]<<8) | prog.bytecode[i+2]
    print(f'{i:02d}: {opcode_to_str(op)} {arg:04X}')
