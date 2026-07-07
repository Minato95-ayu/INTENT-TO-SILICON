"""
=============================================================================
FILE: dump_bc.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), "prototype", "language"))
from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler

with open(r"prototype\tests\runtime\test_functions.aayu", "r") as f:
    code = f.read()

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
compiler = AAYUCompiler(filename="test_functions.aayu")
bc = compiler.compile(ast)

for i, inst in enumerate(bc.instructions):
    print(f"IP={i} OP={inst.opcode.name} OPERAND={inst.operand}")
