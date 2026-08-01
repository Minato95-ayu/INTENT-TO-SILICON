"""
=============================================================================
FILE: test_collections_runner.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import sys
sys.path.insert(0, r"D:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language")
sys.path.insert(0, r"D:\intent-to-silicon-research\INTENT-TO-SILICON\prototype")

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.passes.lowering import LoweringPass
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.vm import VirtualMachine

filepath = r"D:\intent-to-silicon-research\INTENT-TO-SILICON\test_collections.aayu"
with open(filepath, 'r', encoding='utf-8') as f:
    source = f.read()

print("Lexing...")
lexer = Lexer(source)
tokens = lexer.tokenize()

print("Parsing...")
parser = Parser(tokens, filename=filepath)
ast = parser.parse()

print("Lowering...")
lowering = LoweringPass()
lowered_ast = lowering.lower(ast)

print("Compiling...")
compiler = BytecodeEncoder()
bytecode = compiler.compile(lowered_ast)

print("Executing...")
vm = VirtualMachine()
print("Globals keys:", vm.globals.keys())
vm.run(bytecode)

for out in vm.output:
    print(out)
