import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'language')))

from lexer import Lexer
from parser import Parser
from compiler_context import CompilerContext
from passes.semantic.scope_builder import ScopeBuilderPass
from passes.semantic.type_checker import TypeCheckerPass
from resolver.symbols import SymbolTable, ScopeType
from resolver.semantic_types import BuiltinTypes, AnyType

class TestTypeCheckerPass(unittest.TestCase):
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
        
        type_checker = TypeCheckerPass()
        type_checker.run(ctx)
        
        return ctx

    def test_explicit_type_assignment_success(self):
        """let x: Number is 5. -> PASS"""
        ctx = self._run_type_checker('let x: Number is 5.')
        self.assertFalse(ctx.diagnostics.has_errors())
        
    def test_explicit_type_assignment_fail(self):
        """let x: Number is "text". -> FAIL with TypeError AAYU2001"""
        ctx = self._run_type_checker('let x: Number is "text".')
        self.assertTrue(ctx.diagnostics.has_errors())
        err = ctx.diagnostics.diagnostics[0]
        self.assertIn("AAYU2001", err.message)
        
    def test_untyped_variable_any_type(self):
        """let x is 5. -> PASS (now inferred as Number due to Phase 5.4)"""
        ctx = self._run_type_checker('let x is 5.')
        self.assertFalse(ctx.diagnostics.has_errors())
        
        # Verify it has been inferred to Number
        sym = ctx.symbol_tables["test"].lookup("x")
        self.assertEqual(sym.resolved_type, BuiltinTypes.Number)
        
    def test_binary_expression_success(self):
        """let x: Number is 5 + 10."""
        ctx = self._run_type_checker('let x: Number is 5 + 10.')
        self.assertFalse(ctx.diagnostics.has_errors())
        
    def test_binary_expression_mismatch(self):
        """let x: Number is 5 + "hello"."""
        ctx = self._run_type_checker('let x: Number is 5 + "hello".')
        self.assertTrue(ctx.diagnostics.has_errors())
        err = ctx.diagnostics.diagnostics[0]
        self.assertIn("AAYU2001", err.message)
        
    def test_function_return_success(self):
        """function get_num(): Number return 5. end."""
        ctx = self._run_type_checker('''
        function get_num(): Number
            return 5.
        end.
        ''')
        self.assertFalse(ctx.diagnostics.has_errors())

    def test_function_return_fail(self):
        """function get_num(): Number return "five". end."""
        ctx = self._run_type_checker('''
        function get_num(): Number
            return "five".
        end.
        ''')
        self.assertTrue(ctx.diagnostics.has_errors())
        err = ctx.diagnostics.diagnostics[0]
        self.assertIn("AAYU2004", err.message)

    def test_unknown_type(self):
        """let x: UnknownRobot is 5."""
        ctx = self._run_type_checker('let x: UnknownRobot is 5.')
        self.assertTrue(ctx.diagnostics.has_errors())
        err = ctx.diagnostics.diagnostics[0]
        self.assertIn("AAYU2002", err.message)
        
if __name__ == "__main__":
    unittest.main()
