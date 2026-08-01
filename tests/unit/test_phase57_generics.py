"""
=============================================================================
FILE: test_phase57_generics.py
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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.passes.semantic.scope_builder import ScopeBuilderPass
from aayu.compiler.passes.semantic.symbol_binding import SymbolBindingPass
from aayu.compiler.passes.semantic.type_checker import TypeCheckerPass
from aayu.compiler.bytecode.encoder_context import CompilerContext
from aayu.compiler.resolver.symbols import SymbolKind
from aayu.compiler.ast_nodes import FunctionDeclNode, RecordDeclarationNode, InterfaceDeclNode, ExtensionDeclNode
from aayu.compiler.type_nodes import GenericTypeNode

class TestGenerics(unittest.TestCase):
    def _run_pipeline(self, source: str) -> CompilerContext:
        ctx = CompilerContext()
        ctx.current_module = "test_module"
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        from aayu.compiler.resolver.symbols import SymbolTable, ScopeType
        ctx.symbol_tables["test_module"] = SymbolTable("test_module", ScopeType.MODULE)
        ctx.asts = {"test_module": ast}
        
        ScopeBuilderPass().run(ctx)
        SymbolBindingPass().run(ctx)
        
        from aayu.compiler.resolver.symbols import Symbol, SymbolKind
        from aayu.compiler.resolver.semantic_types import GenericType, InterfaceType
        box = Symbol("Box", SymbolKind.INTERFACE, ctx.symbol_tables["test_module"])
        box.resolved_type = GenericType("Box", ["T"])
        ctx.symbol_tables["test_module"].define(box)
        
        arr = Symbol("Array", SymbolKind.INTERFACE, ctx.symbol_tables["test_module"])
        arr.resolved_type = GenericType("Array", ["T"])
        ctx.symbol_tables["test_module"].define(arr)
        
        TypeCheckerPass().run(ctx)
        
        return ctx, ast

    def test_generic_function(self):
        source = """
        record Box<T>.
            val: T
        end.
        
        function wrap<T>(val: Box<T>): Box<T>
            return val.
        end.
        """
        ctx, ast = self._run_pipeline(source)
        self.assertFalse(ctx.diagnostics.has_errors(), f"Errors: {ctx.diagnostics.__dict__}")
        
        func_node = ast.statements[1]
        self.assertIsInstance(func_node, FunctionDeclNode)
        self.assertEqual(func_node.type_parameters, ["T"])
        self.assertEqual(func_node.name, "wrap")
        
        type_scope = func_node.type_scope
        self.assertIsNotNone(type_scope)
        self.assertIsNotNone(type_scope.lookup("T", current_only=True))

    def test_generic_record(self):
        source = """
        record Box<T>.
            val: T
        end.
        """
        ctx, ast = self._run_pipeline(source)
        self.assertFalse(ctx.diagnostics.has_errors(), f"Errors: {ctx.diagnostics.__dict__}")
        
        record_node = ast.statements[0]
        self.assertIsInstance(record_node, RecordDeclarationNode)
        self.assertEqual(record_node.type_parameters, ["T"])
        
        type_scope = record_node.type_scope
        self.assertIsNotNone(type_scope)
        self.assertIsNotNone(type_scope.lookup("T", current_only=True))

    def test_generic_interface(self):
        source = """
        interface List<T>
            function add(item: T): Void.
        end.
        """
        ctx, ast = self._run_pipeline(source)
        self.assertFalse(ctx.diagnostics.has_errors(), f"Errors: {ctx.diagnostics.__dict__}")
        
        iface_node = ast.statements[0]
        self.assertIsInstance(iface_node, InterfaceDeclNode)
        self.assertEqual(iface_node.type_parameters, ["T"])
        
        type_scope = iface_node.type_scope
        self.assertIsNotNone(type_scope.lookup("T", current_only=True))

    def test_generic_extension(self):
        source = """
        interface List<T>
            function append(item: T): Void.
        end.
        
        extend Array<T> with List<T>.
            function append(item: T): Void
            end.
        end.
        """
        ctx, ast = self._run_pipeline(source)
        self.assertFalse(ctx.diagnostics.has_errors(), f"Errors: {ctx.diagnostics.__dict__}")
        
        ext_node = ast.statements[1]
        self.assertIsInstance(ext_node, ExtensionDeclNode)
        self.assertEqual(ext_node.type_parameters, ["T"])

if __name__ == '__main__':
    unittest.main()
