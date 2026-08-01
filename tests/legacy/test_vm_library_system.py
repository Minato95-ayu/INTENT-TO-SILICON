"""
=============================================================================
FILE: test_vm_library_system.py
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

class TestVMLibrarySystem(unittest.TestCase):
    def setUp(self):
        self.tests_dir = os.path.dirname(__file__)
        self.db_path = os.path.join(self.tests_dir, "..", "aayu_db_library.sqlite")
        self.vm = None
        # Clean database
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

    def test_library_system_e2e(self):
        """Compile examples/library-system/library_system.aayu and run the full E2E flow via VM dispatch."""
        filepath = os.path.join(self.tests_dir, "..", "..", "examples", "library-system", "library_system.aayu")
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()

        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), filename=filepath)
        ast = parser.parse()

        compiler = BytecodeEncoder()
        bytecode = compiler.compile(ast)

        # 1. Run main script to register entities and routes on VM
        self.vm = VirtualMachine(db_path=self.db_path)
        # Stub http_serve so it doesn't run the blocking web server during tests
        from aayu.runtime.values.function import NativeFunctionValue
        self.vm.globals["http_serve"] = NativeFunctionValue("http_serve", lambda args, vm=None: None)
        self.vm.run(bytecode)

        # Assert route registrations exist
        self.assertIn("/dashboard", self.vm.routes)
        self.assertIn("/books/add", self.vm.routes)
        self.assertIn("/students/add", self.vm.routes)
        self.assertIn("/issue_process", self.vm.routes)

        # 2. Dispatch GET "/setup"
        res_setup = self.vm.dispatch("/setup")
        self.assertEqual(res_setup.to_python(), "Admin created.")

        # 3. Dispatch POST "/books/add"
        book_data = {
            "title": ["The Pragmatic Programmer"],
            "author": ["Andy Hunt"],
            "isbn": ["978-0201616224"]
        }
        res_add_book = self.vm.dispatch("/books/add", method="POST", form_data=book_data)
        self.assertIn("window.location.href='/books'", res_add_book.to_python())

        # Assert SQLite row exists for Book
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Book")
        self.assertEqual(cursor.fetchone()[0], 1)

        cursor.execute("SELECT title, author, status FROM Book WHERE id = 1")
        book_row = cursor.fetchone()
        self.assertEqual(book_row[0], "The Pragmatic Programmer")
        self.assertEqual(book_row[1], "Andy Hunt")
        self.assertEqual(book_row[2], "Available")

        # 4. Dispatch POST "/students/add"
        student_data = {
            "name": ["John Doe"],
            "email": ["john@doe.com"],
            "student_id": ["S12345"]
        }
        res_add_student = self.vm.dispatch("/students/add", method="POST", form_data=student_data)
        self.assertIn("window.location.href='/students'", res_add_student.to_python())

        # Assert SQLite row exists for Student
        cursor.execute("SELECT COUNT(*) FROM Student")
        self.assertEqual(cursor.fetchone()[0], 1)

        cursor.execute("SELECT name, email FROM Student WHERE id = 1")
        student_row = cursor.fetchone()
        self.assertEqual(student_row[0], "John Doe")
        self.assertEqual(student_row[1], "john@doe.com")

        # 5. Check API Books
        res_api_books = self.vm.dispatch("/api/books")
        self.assertIsInstance(res_api_books, AayuJSONResponse)
        books = json.loads(res_api_books.data_str)
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]["title"], "The Pragmatic Programmer")

        # 6. Check API Students
        res_api_students = self.vm.dispatch("/api/students")
        self.assertIsInstance(res_api_students, AayuJSONResponse)
        students = json.loads(res_api_students.data_str)
        self.assertEqual(len(students), 1)
        self.assertEqual(students[0]["name"], "John Doe")

        # 7. Dispatch POST "/issue_process"
        issue_data = {
            "book_id": ["1"],
            "student_id": ["1"]
        }
        res_issue = self.vm.dispatch("/issue_process", method="POST", form_data=issue_data)
        self.assertIn("window.location.href='/dashboard'", res_issue.to_python())

        # Verify IssueRecord row exists
        cursor.execute("SELECT COUNT(*) FROM IssueRecord")
        self.assertEqual(cursor.fetchone()[0], 1)

        # Verify Book status changed to "Issued"
        cursor.execute("SELECT status FROM Book WHERE id = 1")
        self.assertEqual(cursor.fetchone()[0], "Issued")

        # 8. Dispatch GET "/dashboard" to verify loops and metrics rendering
        res_dashboard = self.vm.dispatch("/dashboard")
        self.assertIsInstance(res_dashboard.to_python(), str)
        
        # Verify rendered metric placeholders
        self.assertIn("1", res_dashboard.to_python()) # Total books: 1, Total students: 1, Issued: 1
        
        conn.close()

if __name__ == "__main__":
    unittest.main()
