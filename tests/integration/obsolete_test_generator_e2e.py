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
from compiler.backend.app_ir import AppIRBuilder
from compiler.parser.parser import Parser
from compiler.lexer.lexer import Lexer

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
