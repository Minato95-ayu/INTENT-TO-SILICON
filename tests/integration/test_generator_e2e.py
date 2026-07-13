import pytest
from compiler.backend.app_ir import AppIRBuilder
from compiler.frontend.parser import Parser
from compiler.frontend.lexer import Lexer

def test_app_ir_builder():
    lexer = Lexer("""
    project App.
    theme light {
        primary "blue".
    }
    """)
    tokens = lexer.tokenize()
    p = Parser(tokens)
    ast = p.parse()
    builder = AppIRBuilder(ast)
    ir = builder.build()
    assert ir["project"] == "App"
    assert len(ir["ui_ir"]["themes"]) == 1
    assert ir["ui_ir"]["themes"][0]["name"] == "light"
