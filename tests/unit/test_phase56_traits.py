"""
=============================================================================
FILE: test_phase56_traits.py
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
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "language")))

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.bytecode.encoder_context import CompilerContext
from aayu.compiler.passes.semantic.scope_builder import ScopeBuilderPass
from aayu.compiler.passes.semantic.type_checker import TypeCheckerPass
from aayu.compiler.passes.semantic.symbol_binding import SymbolBindingPass
from aayu.compiler.resolver.symbols import SymbolTable, ScopeType

class TestTraitsAndExtensions(unittest.TestCase):
    def _run_type_checker(self, source: str) -> CompilerContext:
        ctx = CompilerContext()
        ctx.current_module = "test"
        ctx.symbol_tables["test"] = SymbolTable("test", ScopeType.GLOBAL)
        
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), "test.aayu")
        ast = parser.parse()
        
        ctx.ast = ast
        ctx.asts["test"] = ast
        
        ScopeBuilderPass().run(ctx)
        SymbolBindingPass().run(ctx)
        TypeCheckerPass().run(ctx)
        return ctx

    def test_extension_without_interface(self):
        source = """
        record Dog.
            name
        end.
        
        extend Dog.
            function bark(): Void
            end.
        end.
        """
        ctx = self._run_type_checker(source)
        self.assertFalse(ctx.diagnostics.has_errors(), f"Errors: {ctx.diagnostics.diagnostics}")

    def test_extension_with_valid_interface(self):
        source = """
        interface Animal
            function speak(): Void.
        end.
        
        record Dog.
            name
        end.
        
        extend Dog with Animal.
            function speak(): Void
            end.
        end.
        """
        ctx = self._run_type_checker(source)
        self.assertFalse(ctx.diagnostics.has_errors(), f"Errors: {ctx.diagnostics.diagnostics}")

    def test_extension_with_missing_method(self):
        source = """
        interface Animal
            function speak(): Void.
            function run(): Void.
        end.
        
        record Dog.
            name
        end.
        
        extend Dog with Animal.
            function speak(): Void
            end.
        end.
        """
        ctx = self._run_type_checker(source)
        self.assertTrue(ctx.diagnostics.has_errors())
        self.assertIn("AAYU2005", ctx.diagnostics.diagnostics[0].message)

    def test_extension_with_invalid_signature(self):
        source = """
        interface Animal
            function speak(volume: Number): Void.
        end.
        
        record Dog.
            name
        end.
        
        extend Dog with Animal.
            function speak(): Void
            end.
        end.
        """
        ctx = self._run_type_checker(source)
        self.assertTrue(ctx.diagnostics.has_errors())
        self.assertIn("AAYU2006", ctx.diagnostics.diagnostics[0].message)
        
    def test_extension_with_invalid_interface_name(self):
        source = """
        record Dog.
            name
        end.
        
        extend Dog with UnknownInterface.
            function speak(): Void
            end.
        end.
        """
        ctx = self._run_type_checker(source)
        self.assertTrue(ctx.diagnostics.has_errors())
        self.assertIn("AAYU2004", ctx.diagnostics.diagnostics[0].message)

if __name__ == '__main__':
    unittest.main()
