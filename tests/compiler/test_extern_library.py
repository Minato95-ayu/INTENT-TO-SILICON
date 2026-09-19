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
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser


def parse_app(source: str):
    return Parser(Lexer(source).tokenize()).parse()


def test_external_libraries_are_preserved_in_app_ir():
    ast = parse_app(
        """
        app Demo
        extern sqlite as native.
        extern torch as rust.
        extern numpy as python.
        extern chart as js.
        """
    )

    ir = AppIRBuilder(ast).build()

    assert ir["interop_ir"]["libraries"] == [
        {"name": "sqlite", "provider": "native"},
        {"name": "torch", "provider": "rust"},
        {"name": "numpy", "provider": "python"},
        {"name": "chart", "provider": "js"},
    ]


def test_external_library_rejects_unknown_provider():
    with pytest.raises(Exception, match="Unsupported external library provider"):
        parse_app("extern thing as cobol.")