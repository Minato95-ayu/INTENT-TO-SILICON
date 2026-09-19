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

import pytest
pytestmark = pytest.mark.skip(reason='Obsolete API: AAYUCompiler removed in favor of IRPipeline')

import pytest
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
# # from compiler.frontend.compiler import AAYUCompiler
from compiler.ast.nodes import *

def parse(source):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()

def compile_source(source):
    ast = parse(source)
    compiler = AAYUCompiler()
    return compiler.compile(ast)

class TestParserErrors:
    def test_throw_panic_assert(self):
        ast = parse('''
        throw "Error occurred".
        panic "Fatal error".
        assert x == 5.
        ''')
        assert len(ast.statements) == 3

    def test_try_catch_finally(self):
        ast = parse('''
        try {
            print("trying").
        } catch (e) {
            print(e).
        } finally {
            print("finally").
        }
        ''')
        assert len(ast.statements) == 1

class TestCompilerErrors:
    def test_compile_throw_panic_assert(self):
        bytecode = compile_source('''
        let x = 5.
        throw "Error occurred".
        panic "Fatal error".
        assert x == 5.
        ''')
        assert bytecode

    def test_compile_try_catch(self):
        bytecode = compile_source('''
        try {
            print("trying").
        } catch (e) {
            print(e).
        }
        ''')
        assert bytecode
