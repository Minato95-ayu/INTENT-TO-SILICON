"""
=============================================================================
FILE: test_vm_errors.py
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
import sqlite3

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "aayu_language"))

from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler
from vm import VirtualMachine
from compiler.frontend.errors import (
    UndefinedVariableError,
    DivisionByZeroError,
    IndexOutOfBoundsError,
    InvalidCallError,
    DatabaseError
)

class TestVMErrors(unittest.TestCase):
    def setUp(self):
        self.tests_dir = os.path.dirname(__file__)
        self.db_path = os.path.join(self.tests_dir, "..", "aayu_db.sqlite")
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except PermissionError:
                pass

    def tearDown(self):
        if getattr(self, 'vm', None):
            self.vm.close()
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except Exception:
                pass

    def run_source(self, source, filename="test.aayu"):
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), filename=filename)
        ast = parser.parse()
        compiler = AAYUCompiler(filename=filename)
        bytecode = compiler.compile(ast)
        vm = VirtualMachine(db_path=self.db_path)
        try:
            vm.run(bytecode)
        finally:
            vm.close()

    def test_undefined_variable(self):
        source = "show x."
        with self.assertRaises(UndefinedVariableError) as ctx:
            self.run_source(source)
        
        err_msg = str(ctx.exception)
        self.assertIn("Variable 'x' not found.", err_msg)
        self.assertIn("Location:", err_msg)
        self.assertIn("Line: 1", err_msg)

    def test_division_by_zero(self):
        source = "number x is 10 / 0."
        with self.assertRaises(DivisionByZeroError) as ctx:
            self.run_source(source)
            
        err_msg = str(ctx.exception)
        self.assertIn("Division by zero.", err_msg)
        self.assertIn("Line: 1", err_msg)

    def test_list_index_out_of_bounds(self):
        source = """list lst.
add 42 to lst.
show get 5 from lst."""
        with self.assertRaises(IndexOutOfBoundsError) as ctx:
            self.run_source(source)
            
        err_msg = str(ctx.exception)
        self.assertIn("List index out of range: 5.", err_msg)
        self.assertIn("Line: 1", err_msg)

    def test_invalid_map_key(self):
        source = """map m.
set "a" to 1 in m.
show get "b" from m."""
        with self.assertRaises(IndexOutOfBoundsError) as ctx:
            self.run_source(source)
            
        err_msg = str(ctx.exception)
        self.assertIn("Key 'b' not found in map.", err_msg)
        self.assertIn("Line: 1", err_msg)

    def test_missing_task(self):
        source = "run nonexistent_task."
        with self.assertRaises(UndefinedVariableError) as ctx:
            self.run_source(source)
            
        err_msg = str(ctx.exception)
        self.assertIn("Variable 'nonexistent_task' not found.", err_msg)

    def test_invalid_call(self):
        source = """number not_callable is 42.
run not_callable."""
        with self.assertRaises(InvalidCallError) as ctx:
            self.run_source(source)
            
        err_msg = str(ctx.exception)
        self.assertIn("Object is not callable", err_msg)
        self.assertIn("Line: 1", err_msg)

    def test_database_failure(self):
        # Trying to select from non-existent table should raise DatabaseError
        source = """list items is find NonExistentTable."""
        with self.assertRaises(DatabaseError) as ctx:
            self.run_source(source)
            
        err_msg = str(ctx.exception)
        self.assertIn("Database query failed", err_msg)

    def test_nested_function_failure(self):
        source = """task inner.
    number division is 10 / 0.
end.

task outer.
    run inner.
end.

run outer."""
        with self.assertRaises(DivisionByZeroError) as ctx:
            self.run_source(source, filename="nested.aayu")
            
        err_msg = str(ctx.exception)
        self.assertIn("Division by zero.", err_msg)
        
        # Verify call stack
        self.assertIn("Location:", err_msg)
        self.assertIn("File: nested.aayu", err_msg)
        self.assertIn("Task: inner", err_msg)
        self.assertIn("Line: 1", err_msg)
        
        # Call Stack hierarchy check
        self.assertIn("Call Stack:", err_msg)
        self.assertIn("main()", err_msg)
        self.assertIn("outer(...)", err_msg)
        self.assertIn("inner(...)", err_msg)

if __name__ == "__main__":
    unittest.main()
