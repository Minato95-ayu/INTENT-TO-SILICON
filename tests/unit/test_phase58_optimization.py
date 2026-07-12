"""
=============================================================================
FILE: test_phase58_optimization.py
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
from compiler.frontend.compiler import AAYUCompiler
from compiler.frontend.passes.manager import PassManager
from compiler.frontend.passes.optimizer import StaticOptimizerPass
from compiler.frontend.passes.semantic.type_checker import TypeCheckerPass
from compiler.frontend.passes.semantic.scope_builder import ScopeBuilderPass
from compiler.frontend.passes.semantic.symbol_binding import SymbolBindingPass
from compiler.frontend.compiler_context import CompilerContext
from compiler.frontend.ast_nodes import NumberNode, IfNode, BlockNode, ShowNode

class TestPhase58Optimization(unittest.TestCase):
    def setUp(self):
        self.pass_manager = PassManager()
        self.pass_manager.add_pass(StaticOptimizerPass())

    def run_opt(self, source: str):
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), filename="test")
        ast = parser.parse()
        
        context = CompilerContext(workspace=None)
        context.asts["main"] = ast
        context.current_module = "main"
        
        from compiler.frontend.resolver.symbols import SymbolTable, ScopeType
        context.symbol_tables["main"] = SymbolTable("main", ScopeType.MODULE)
        
        success = self.pass_manager.run(context)
        if not success:
            context.diagnostics.print_all()
        self.assertTrue(success, "Optimization pass failed")
        
        return context.asts["main"]

    def test_constant_folding_binary(self):
        source = "let x is 5 + 10 * 2."
        optimized_ast = self.run_opt(source)
        
        decl = optimized_ast.statements[0]
        self.assertIsInstance(decl.value, NumberNode)
        self.assertEqual(decl.value.value, 25)
        
    def test_constant_folding_unary(self):
        source = "let x is -5."
        optimized_ast = self.run_opt(source)
        decl = optimized_ast.statements[0]
        self.assertIsInstance(decl.value, NumberNode)
        self.assertEqual(decl.value.value, -5)
        
    def test_branch_pruning_truthy(self):
        source = """
        if 1.
            show "true branch".
        else.
            show "false branch".
        end.
        """
        optimized_ast = self.run_opt(source)
        # 1 is truthy. The IfNode should be replaced entirely by its then_branch statements wrapped in a BlockNode by my optimizer.
        first_stmt = optimized_ast.statements[0]
        self.assertIsInstance(first_stmt, BlockNode)
        self.assertEqual(len(first_stmt.statements), 1)
        self.assertIsInstance(first_stmt.statements[0], ShowNode)
        self.assertEqual(first_stmt.statements[0].expression.value, "true branch")

    def test_branch_pruning_falsey(self):
        source = """
        if 0.
            show "true branch".
        else.
            show "false branch".
        end.
        """
        optimized_ast = self.run_opt(source)
        first_stmt = optimized_ast.statements[0]
        self.assertIsInstance(first_stmt, BlockNode)
        self.assertEqual(len(first_stmt.statements), 1)
        self.assertIsInstance(first_stmt.statements[0], ShowNode)
        self.assertEqual(first_stmt.statements[0].expression.value, "false branch")

    def test_dead_code_elimination(self):
        source = """
        function my_func()
            let x is 1.
            return x.
            let y is 2.
            show y.
        end.
        """
        optimized_ast = self.run_opt(source)
        func_decl = optimized_ast.statements[0]
        # Body should only have 2 statements: let x is 1., return x.
        self.assertEqual(len(func_decl.body), 2)
        self.assertEqual(func_decl.body[0].name, "x")
        self.assertEqual(func_decl.body[1].value.name, "x")

if __name__ == '__main__':
    unittest.main()
