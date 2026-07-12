"""
=============================================================================
FILE: test_vm_serve_e2e.py
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
import urllib.request
import urllib.parse
import json
import threading
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "aayu_language"))

from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler
from vm import VirtualMachine

class TestVMServeE2E(unittest.TestCase):
    def setUp(self):
        self.tests_dir = os.path.dirname(__file__)
        self.db_path = os.path.join(self.tests_dir, "..", "aayu_db_serve.sqlite")
        self.vm = None
        # Ensure clean DB
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except PermissionError:
                pass

    def tearDown(self):
        if self.vm:
            if hasattr(self.vm, "http_server") and self.vm.http_server:
                try:
                    self.vm.http_server.shutdown()
                    self.vm.http_server.server_close()
                except Exception:
                    pass
            self.vm.close()
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except PermissionError:
                pass

    def test_e2e_http_server(self):
        """Compile routing program, run HTTP server in thread, and verify requests."""
        filepath = os.path.join(self.tests_dir, "vm_web_route.aayu")
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()

        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), filename=filepath)
        ast = parser.parse()

        compiler = AAYUCompiler()
        bytecode = compiler.compile(ast)

        # 1. Run main script to register routes
        self.vm = VirtualMachine(db_path=self.db_path)
        self.vm.run(bytecode)

        # 2. Start HTTP serve in a background thread
        port = 8082
        server_thread = threading.Thread(
            target=self.vm.globals["http_serve"],
            args=(port,)
        )
        server_thread.daemon = True
        server_thread.start()

        # Let the server spin up
        time.sleep(0.5)

        # 3. Send GET /books (Expected empty list)
        url_books = f"http://localhost:{port}/books"
        req_get = urllib.request.Request(url_books, method="GET")
        with urllib.request.urlopen(req_get) as resp:
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.headers["Content-Type"], "application/json")
            data = json.loads(resp.read().decode('utf-8'))
            self.assertEqual(data, [])

        # 4. Send POST /add (Expected "Book Added")
        url_add = f"http://localhost:{port}/add"
        post_data = urllib.parse.urlencode({"title": "AAYU"}).encode('utf-8')
        req_post = urllib.request.Request(url_add, data=post_data, method="POST")
        with urllib.request.urlopen(req_post) as resp:
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.headers["Content-Type"], "text/html; charset=utf-8")
            body = resp.read().decode('utf-8')
            self.assertEqual(body, "Book Added")

        # 5. Send GET /books again (Expected list with inserted book)
        with urllib.request.urlopen(req_get) as resp:
            self.assertEqual(resp.status, 200)
            self.assertEqual(resp.headers["Content-Type"], "application/json")
            data = json.loads(resp.read().decode('utf-8'))
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["title"], "AAYU")

        # 5.5 Send DELETE /remove (Expected "Book Deleted")
        url_remove = f"http://localhost:{port}/remove"
        req_delete = urllib.request.Request(url_remove, method="DELETE")
        with urllib.request.urlopen(req_delete) as resp:
            self.assertEqual(resp.status, 200)
            body = resp.read().decode('utf-8')
            self.assertEqual(body, "Book Deleted")

        # Verify books is empty again
        with urllib.request.urlopen(req_get) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode('utf-8'))
            self.assertEqual(data, [])

        # 6. Verify 405 Method Not Allowed
        req_bad_add = urllib.request.Request(url_add, method="GET")
        try:
            urllib.request.urlopen(req_bad_add)
            self.fail("Expected HTTPError 405")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 405)

        # Verify 405 Method Not Allowed for DELETE route on wrong verb (GET)
        req_bad_remove = urllib.request.Request(url_remove, method="GET")
        try:
            urllib.request.urlopen(req_bad_remove)
            self.fail("Expected HTTPError 405")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 405)

        # 7. Verify 404 Not Found
        url_invalid = f"http://localhost:{port}/invalid-route"
        req_invalid = urllib.request.Request(url_invalid, method="GET")
        try:
            urllib.request.urlopen(req_invalid)
            self.fail("Expected HTTPError 404")
        except urllib.error.HTTPError as e:
            self.assertEqual(e.code, 404)

if __name__ == "__main__":
    unittest.main()
