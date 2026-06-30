"""
Phase 5.2 — Symbol Types
Tests that type metadata flows correctly from Parser → ScopeBuilder → Symbols.
No type checking, inference, or validation — purely metadata binding.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'language')))

from lexer import Lexer
from parser import Parser
from compiler import AAYUCompiler
from resolver.symbols import TypeSource, SymbolKind
from passes.semantic.scope_builder import ScopeBuilderPass
from compiler_context import CompilerContext


class TestSymbolTypeMetadata(unittest.TestCase):
    """Verify Symbol.declared_type, resolved_type, and type_source fields."""

    def test_type_source_enum_values(self):
        """TypeSource enum has all four planned variants."""
        self.assertEqual(TypeSource.EXPLICIT.value, "explicit")
        self.assertEqual(TypeSource.INFERRED.value, "inferred")
        self.assertEqual(TypeSource.GENERIC.value, "generic")
        self.assertEqual(TypeSource.BUILTIN.value, "builtin")

    def test_symbol_defaults(self):
        """Fresh symbols have declared_type=None, resolved_type=None, type_source='explicit'."""
        from resolver.symbols import VariableSymbol, SymbolTable, ScopeType
        scope = SymbolTable("test", ScopeType.GLOBAL)
        sym = VariableSymbol("x", scope)
        self.assertIsNone(sym.declared_type)
        self.assertIsNone(sym.resolved_type)
        self.assertEqual(sym.type_source, "explicit")

    def test_symbol_kind_preserved(self):
        """Symbol subclasses retain their SymbolKind."""
        from resolver.symbols import FunctionSymbol, ParameterSymbol, SymbolTable, ScopeType
        scope = SymbolTable("test", ScopeType.GLOBAL)
        fn = FunctionSymbol("sum_values", scope)
        self.assertEqual(fn.kind, SymbolKind.FUNCTION)
        param = ParameterSymbol("a", scope)
        self.assertEqual(param.kind, SymbolKind.PARAMETER)


class TestScopeBuilderTypeBinding(unittest.TestCase):
    """Verify ScopeBuilder correctly binds type annotations to symbols."""

    def _build_scope(self, source: str) -> CompilerContext:
        """Parse source and run ScopeBuilder, return the CompilerContext."""
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens, filename="test.aayu")
        ast = parser.parse()

        ctx = CompilerContext()
        ctx.ast = ast
        ctx.current_module = "test"
        ctx.asts["test"] = ast

        from resolver.symbols import SymbolTable, ScopeType
        ctx.symbol_tables["test"] = SymbolTable("test", ScopeType.GLOBAL)

        scope_pass = ScopeBuilderPass()
        scope_pass.run(ctx)
        return ctx

    def test_variable_with_type_annotation(self):
        """let x: Number is 5. → VariableSymbol.declared_type = NamedTypeNode('Number')."""
        ctx = self._build_scope('let x: Number is 5.')
        sym = ctx.symbol_tables["test"].lookup("x")
        self.assertIsNotNone(sym, "Variable 'x' should be in symbol table")
        self.assertEqual(sym.kind, SymbolKind.VARIABLE)
        self.assertIsNotNone(sym.declared_type)
        self.assertEqual(sym.declared_type.name, "Number")

    def test_variable_without_type_annotation(self):
        """let y is 10. → VariableSymbol.declared_type = None."""
        ctx = self._build_scope('let y is 10.')
        sym = ctx.symbol_tables["test"].lookup("y")
        self.assertIsNotNone(sym, "Variable 'y' should be in symbol table")
        self.assertIsNone(sym.declared_type)

    def test_function_return_type(self):
        """function sum_values(a, b): Number → FunctionSymbol.declared_type = NamedTypeNode('Number')."""
        source = '''function sum_values(a, b): Number
            return a + b.
        end.'''
        ctx = self._build_scope(source)
        sym = ctx.symbol_tables["test"].lookup("sum_values")
        self.assertIsNotNone(sym, "Function 'sum_values' should be in symbol table")
        self.assertEqual(sym.kind, SymbolKind.FUNCTION)
        self.assertIsNotNone(sym.declared_type)
        self.assertEqual(sym.declared_type.name, "Number")

    def test_function_without_return_type(self):
        """function greet_user(name) → FunctionSymbol.declared_type = None."""
        source = '''function greet_user(name)
            return name.
        end.'''
        ctx = self._build_scope(source)
        sym = ctx.symbol_tables["test"].lookup("greet_user")
        self.assertIsNotNone(sym, "Function 'greet_user' should be in symbol table")
        self.assertIsNone(sym.declared_type)

    def test_typed_parameters(self):
        """function sum_values(a: Number, b: Number) → ParameterSymbol.declared_type set."""
        source = '''function sum_values(a: Number, b: Number): Number
            return a + b.
        end.'''
        ctx = self._build_scope(source)
        fn_sym = ctx.symbol_tables["test"].lookup("sum_values")
        self.assertIsNotNone(fn_sym)

        # Parameters are in the function's own scope
        ast_fn = ctx.ast.statements[0]
        self.assertTrue(hasattr(ast_fn, 'func_scope'))
        
        param_a = ast_fn.func_scope.lookup("a")
        self.assertIsNotNone(param_a, "Parameter 'a' should be in function scope")
        self.assertEqual(param_a.kind, SymbolKind.PARAMETER)
        self.assertIsNotNone(param_a.declared_type)
        self.assertEqual(param_a.declared_type.name, "Number")

        param_b = ast_fn.func_scope.lookup("b")
        self.assertIsNotNone(param_b, "Parameter 'b' should be in function scope")
        self.assertIsNotNone(param_b.declared_type)
        self.assertEqual(param_b.declared_type.name, "Number")

    def test_untyped_parameters(self):
        """function sum_values(a, b) → ParameterSymbol.declared_type = None."""
        source = '''function sum_values(a, b)
            return a + b.
        end.'''
        ctx = self._build_scope(source)
        ast_fn = ctx.ast.statements[0]
        
        param_a = ast_fn.func_scope.lookup("a")
        self.assertIsNotNone(param_a, "Parameter 'a' should be in function scope")
        self.assertIsNone(param_a.declared_type)

    def test_resolved_type_stays_none(self):
        """Phase 5.2 contract: resolved_type must remain None. It's for Phase 5.3."""
        ctx = self._build_scope('let x: Number is 5.')
        sym = ctx.symbol_tables["test"].lookup("x")
        self.assertIsNotNone(sym, "Variable 'x' should be in symbol table")
        self.assertIsNone(sym.resolved_type)

    def test_compiler_unchanged(self):
        """Compiler pipeline should work identically with or without type annotations."""
        source_typed = '''function sum_values(a: Number, b: Number): Number
            return a + b.
        end.'''
        source_untyped = '''function sum_values(a, b)
            return a + b.
        end.'''

        for source in [source_typed, source_untyped]:
            lexer = Lexer(source)
            tokens = lexer.tokenize()
            parser = Parser(tokens, filename="test.aayu")
            ast = parser.parse()
            compiler = AAYUCompiler()
            bytecode = compiler.compile(ast)
            # Just verify it compiles without error — compiler is unchanged
            self.assertIsNotNone(bytecode)
            self.assertTrue(len(bytecode.instructions) > 0)


class TestTaskSymbolBinding(unittest.TestCase):
    """Verify task declarations work with ScopeBuilder."""

    def _build_scope(self, source: str) -> CompilerContext:
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens, filename="test.aayu")
        ast = parser.parse()

        ctx = CompilerContext()
        ctx.ast = ast
        ctx.current_module = "test"
        ctx.asts["test"] = ast

        from resolver.symbols import SymbolTable, ScopeType
        ctx.symbol_tables["test"] = SymbolTable("test", ScopeType.GLOBAL)

        scope_pass = ScopeBuilderPass()
        scope_pass.run(ctx)
        return ctx

    def test_task_registered_as_function_symbol(self):
        """task greet_user. ... end. → FunctionSymbol in scope."""
        source = '''task greet_user.
            let x is 1.
        end.'''
        ctx = self._build_scope(source)
        sym = ctx.symbol_tables["test"].lookup("greet_user")
        self.assertIsNotNone(sym, "Task 'greet_user' should be in symbol table")
        self.assertEqual(sym.kind, SymbolKind.FUNCTION)


if __name__ == "__main__":
    unittest.main()
