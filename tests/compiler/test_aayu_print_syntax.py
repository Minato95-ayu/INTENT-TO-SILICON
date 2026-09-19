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


def test_aayu_native_print_syntax_parses_without_parentheses():
    ast = Parser(Lexer('print "Hello AAYU".').tokenize()).parse()

    statement = ast.statements[0]
    assert type(statement).__name__ == "ActionCallNode"
    assert statement.name == "print"
    assert statement.args[0].value == "Hello AAYU"


def test_legacy_print_call_syntax_remains_supported():
    ast = Parser(Lexer('print("Hello AAYU").').tokenize()).parse()

    statement = ast.statements[0]
    assert statement.name == "print"
    assert statement.args[0].value == "Hello AAYU"