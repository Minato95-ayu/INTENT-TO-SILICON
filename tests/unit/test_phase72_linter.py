"""
=============================================================================
FILE: test_phase72_linter.py
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

from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from tools.linter import AAYULinter

class TestPhase72Linter(unittest.TestCase):
    def lint_source(self, source: str):
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), filename="test.aayu")
        ast = parser.parse()
        linter = AAYULinter(filename="test.aayu")
        return linter.lint(ast)

    def test_empty_block_warning(self):
        source = """
if 1.
end.
"""
        messages = self.lint_source(source)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].severity, "WARNING")
        self.assertIn("Empty 'if' block", messages[0].message)

    def test_useless_expression(self):
        source = """
function main()
    let x is 5.
    let y is 10.
    x.
    x + y.
end.
"""
        messages = self.lint_source(source)
        warnings = [m for m in messages if m.severity == "WARNING" and "Useless expression" in m.message]
        self.assertEqual(len(warnings), 2)

    def test_naming_convention(self):
        source = """
function Bad_name()
    let BadVar is 5.
end.
"""
        messages = self.lint_source(source)
        warnings = [m for m in messages if m.severity == "WARNING" and "lowercase letter" in m.message]
        self.assertEqual(len(warnings), 2)

    def test_dead_code_warning(self):
        source = """
function main()
    return 1.
    show "unreachable".
end.
"""
        messages = self.lint_source(source)
        warnings = [m for m in messages if m.severity == "WARNING" and "Unreachable code" in m.message]
        self.assertEqual(len(warnings), 1)

    def test_long_function(self):
        # Create a source with > 50 statements
        body = "\n".join(["    let x is 1."] * 55)
        source = f"function main()\n{body}\nend."
        messages = self.lint_source(source)
        warnings = [m for m in messages if m.severity == "WARNING" and "is too long" in m.message]
        self.assertEqual(len(warnings), 1)

    def test_too_many_parameters(self):
        source = "function main(a, b, c, d, e, f)\nend."
        messages = self.lint_source(source)
        warnings = [m for m in messages if m.severity == "WARNING" and "too many parameters" in m.message]
        self.assertEqual(len(warnings), 1)

if __name__ == '__main__':
    unittest.main()
