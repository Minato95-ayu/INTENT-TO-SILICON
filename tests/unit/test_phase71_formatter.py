"""
=============================================================================
FILE: test_phase71_formatter.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from tools.formatter import AAYUFormatter

class TestPhase71Formatter(unittest.TestCase):
    def setUp(self):
        self.formatter = AAYUFormatter(indent_size=4)

    def format_source(self, source: str) -> str:
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), filename="test.aayu")
        ast = parser.parse()
        return self.formatter.format(ast)

    def test_basic_formatting(self):
        source = """let   x   is    5+  10."""
        expected = "let x is 5 + 10.\n"
        formatted = self.format_source(source)
        self.assertEqual(formatted, expected)

    def test_function_formatting(self):
        source = """
function main ( a : Number, b : Number ) : Number
    let x is a+b.
  return    x.
end .
"""
        expected = """function main(a: Number, b: Number): Number
    let x is a + b.
    return x.
end.\n"""
        formatted = self.format_source(source)
        self.assertEqual(formatted, expected)

    def test_if_else_formatting(self):
        source = """
if 1 .
show "true".
else .
  show "false" .
end.
"""
        expected = """if 1.
    show "true".
else.
    show "false".
end.\n"""
        formatted = self.format_source(source)
        self.assertEqual(formatted, expected)

    def test_idempotence(self):
        source = """
function main()
    let x is 5 * 10.
    if x.
        show "yes".
    else.
        show "no".
    end.
end.
"""
        # First format
        formatted1 = self.format_source(source)
        # Second format (parse the formatted output)
        formatted2 = self.format_source(formatted1)
        
        self.assertEqual(formatted1, formatted2)

if __name__ == '__main__':
    unittest.main()
