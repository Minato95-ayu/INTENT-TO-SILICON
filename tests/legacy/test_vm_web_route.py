"""
=============================================================================
FILE: test_vm_web_route.py
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
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "aayu_language"))

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from vm import VirtualMachine
from interpreter import AayuJSONResponse

class TestVMWebRoute(unittest.TestCase):
    def setUp(self):
        self.tests_dir = os.path.dirname(__file__)
        self.db_path = os.path.join(self.tests_dir, "..", "aayu_db_web_route.sqlite")
        self.vm = None
        # Ensure clean DB
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except PermissionError:
                pass

    def tearDown(self):
        if self.vm:
            self.vm.close()
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except PermissionError:
                pass

    def test_routing_and_dispatch(self):
        """Compile vm_web_route.aayu, register routes, and run dispatches."""
        filepath = os.path.join(self.tests_dir, "vm_web_route.aayu")
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()

        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), filename=filepath)
        ast = parser.parse()

        compiler = BytecodeEncoder()
        bytecode = compiler.compile(ast)

        # 1. Run the main route registration script on VM
        self.vm = VirtualMachine(db_path=self.db_path)
        self.vm.run(bytecode)

        # Verify Route Registry
        expected_routes = {
            "/books": {
                "handler": "list_books",
                "method": "GET"
            },
            "/add": {
                "handler": "add_book",
                "method": "POST"
            },
            "/remove": {
                "handler": "delete_book",
                "method": "DELETE"
            }
        }
        self.assertEqual(self.vm.routes, expected_routes)

        # 2. Dispatch GET "/books" on empty DB
        res_get_empty = self.vm.dispatch("/books")
        self.assertIsInstance(res_get_empty, AayuJSONResponse)
        self.assertEqual(json.loads(res_get_empty.data_str), [])

        # 3. Dispatch POST "/add" with form parameters
        res_post = self.vm.dispatch("/add", method="POST", form_data={"title": ["AAYU"]})
        self.assertEqual(res_post.to_python(), "Book Added")

        # 4. Dispatch GET "/books" again to verify matching insertion
        res_get_populated = self.vm.dispatch("/books")
        self.assertIsInstance(res_get_populated, AayuJSONResponse)
        books = json.loads(res_get_populated.data_str)
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["title"], "AAYU")

        # 4.5 Dispatch DELETE "/remove" to delete book
        res_delete = self.vm.dispatch("/remove", method="DELETE")
        self.assertEqual(res_delete.to_python(), "Book Deleted")

        # Verify books is empty again
        res_get_cleared = self.vm.dispatch("/books")
        books_cleared = json.loads(res_get_cleared.data_str)
        self.assertEqual(len(books_cleared), 0)

        # 5. Method verification checks
        with self.assertRaises(Exception) as ctx:
            self.vm.dispatch("/add", method="GET")
        self.assertIn("Method 'GET' not allowed", str(ctx.exception))

        with self.assertRaises(Exception) as ctx:
            self.vm.dispatch("/books", method="POST")
        self.assertIn("Method 'POST' not allowed", str(ctx.exception))

        with self.assertRaises(Exception) as ctx:
            self.vm.dispatch("/invalid-url")
        self.assertIn("Route '/invalid-url' not found", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
