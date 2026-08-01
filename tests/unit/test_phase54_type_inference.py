"""
=============================================================================
FILE: test_phase54_type_inference.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.bytecode.encoder_context import CompilerContext
from aayu.compiler.passes.semantic.scope_builder import ScopeBuilderPass
from aayu.compiler.passes.semantic.type_checker import TypeCheckerPass
from aayu.compiler.resolver.symbols import SymbolTable, ScopeType
from aayu.compiler.resolver.semantic_types import BuiltinTypes, AnyType, VoidType

class TestTypeInferencePass(unittest.TestCase):
    def _run_type_checker(self, source: str) -> CompilerContext:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens, filename="test.aayu")
        ast = parser.parse()

        ctx = CompilerContext()
        ctx.ast = ast
        ctx.current_module = "test"
        ctx.asts["test"] = ast

        ctx.symbol_tables["test"] = SymbolTable("test", ScopeType.GLOBAL)

        scope_pass = ScopeBuilderPass()
        scope_pass.run(ctx)
        
        from aayu.compiler.passes.semantic.symbol_binding import SymbolBindingPass
        sym_pass = SymbolBindingPass()
        sym_pass.run(ctx)
        
        type_checker = TypeCheckerPass()
        type_checker.run(ctx)
        
        return ctx

    def test_variable_type_inference(self):
        """let x is 5. x is "hello" -> fails because x is inferred as Number"""
        ctx = self._run_type_checker('''
        let x is 5.
        x is "hello".
        ''')
        self.assertTrue(ctx.diagnostics.has_errors())
        err = ctx.diagnostics.diagnostics[0]
        self.assertIn("AAYU2001", err.message)
        
        sym = ctx.symbol_tables["test"].lookup("x")
        self.assertEqual(sym.resolved_type, BuiltinTypes.Number)

    def test_function_return_inference(self):
        """function get_val() return 10. end. -> get_val returns Number"""
        ctx = self._run_type_checker('''
        function get_val()
            return 10.
        end.
        
        let y: Text is get_val().
        ''')
        # We don't trace get_val() inside variable assignment properly without full CallNode checking
        # But we CAN check the symbol's resolved type.
        sym = ctx.symbol_tables["test"].lookup("get_val")
        self.assertEqual(sym.resolved_type, BuiltinTypes.Number)

    def test_function_ambiguous_return_fallback(self):
        """function ambiguous(a) if a then return 10. else return "hello". end. end. -> falls back to AnyType"""
        ctx = self._run_type_checker('''
        function ambiguous(a)
            if a
                return 10.
            else
                return "hello".
            end.
        end.
        ''')
        self.assertFalse(ctx.diagnostics.has_errors())
        sym = ctx.symbol_tables["test"].lookup("ambiguous")
        self.assertEqual(sym.resolved_type, BuiltinTypes.Any)
        
    def test_function_no_return_void(self):
        """function log() print(5). end. -> inferred as VoidType"""
        ctx = self._run_type_checker('''
        function log()
            let x is 5.
        end.
        ''')
        sym = ctx.symbol_tables["test"].lookup("log")
        self.assertEqual(sym.resolved_type, BuiltinTypes.Void)

if __name__ == "__main__":
    unittest.main()
